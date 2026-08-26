import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore, ticketIntakeEligible } from "./ticket-store.js";

describe("TicketStore", () => {
  it("commits the full command and accepted event before returning", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const path = join(root, "tickets.sqlite3");
    const accepted = new TicketStore(path).accept({runId:"run-1",ownerSessionKey:"owner",prompt:"สร้างแผนเที่ยวเชียงใหม่"});
    const db = new DatabaseSync(path, { readOnly: true });
    const ticket = db.prepare("SELECT prompt,status FROM tickets WHERE ticket_id=?").get(accepted.ticketId) as any;
    const events = db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=?").get(accepted.ticketId) as any;
    expect(ticket).toEqual({prompt:"สร้างแผนเที่ยวเชียงใหม่",status:"accepted"});
    expect(events.count).toBe(1);
    db.close();
    rmSync(root, {recursive:true,force:true});
  });

  it("is idempotent for the same owner run", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const store = new TicketStore(join(root, "tickets.sqlite3"));
    const first = store.accept({runId:"same-run",ownerSessionKey:"owner",prompt:"command"});
    const second = store.accept({runId:"same-run",ownerSessionKey:"owner",prompt:"command"});
    expect(second.ticketId).toBe(first.ticketId);
    expect(second.duplicate).toBe(true);
    rmSync(root,{recursive:true,force:true});
  });

  it("routes a Ticket exactly once and rejects conflicting reroutes", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-route-idempotency-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    try {
      const ticket=store.accept({runId:"route-once",ownerSessionKey:"owner",prompt:"durable"});
      expect(store.route(ticket.ticketId,true)).toBe(true);
      expect(store.route(ticket.ticketId,true)).toBe(false);
      expect(() => store.route(ticket.ticketId,false)).toThrow(/conflicting route/i);
      const db=new DatabaseSync(path,{readOnly:true});
      expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type)).toEqual(["accepted","routed"]);
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("does not ticket internal continuation and delivery messages", () => {
    expect(ticketIntakeEligible("The previous run was interrupted. Resume automatically")).toBe(false);
    expect(ticketIntakeEligible("[CogentNexus-OpenClaw Delivery: ticket:7]\nDeliver the committed result")).toBe(false);
    expect(ticketIntakeEligible("[CogentNexus-OpenClaw Continuation: post-compaction]\nResume committed work")).toBe(false);
    expect(ticketIntakeEligible("ช่วยสรุปเรื่องนี้")).toBe(true);
  });

  it("throws instead of allowing an uncommitted command when storage is invalid", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const path = join(root, "not-a-database.sqlite3");
    writeFileSync(path, "this is not sqlite", "utf8");
    expect(() => new TicketStore(path).accept({runId:"run-2",ownerSessionKey:"owner",prompt:"must persist"})).toThrow();
    rmSync(root,{recursive:true,force:true});
  });

  it("rejects supplied run settlement when Ticket outbox has no durable binding", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-unbound-run-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    try {
      const makeOutbox=(runId:string) => {
        const ticket=store.accept({runId,ownerSessionKey:"owner-a",prompt:"terminal work"});
        const lease=store.claim({ticketId:ticket.ticketId,workerId:`worker-${runId}`,leaseMs:10_000})!;
        store.complete({...lease,result:{ok:true}});
        return store.pendingOutbox().filter((item) => item.ticketId === ticket.ticketId).at(-1)!;
      };
      const successOutbox=makeOutbox("unbound-success"),failureOutbox=makeOutbox("unbound-failure");
      expect(store.markOutboxDelivered(successOutbox.outboxId,new Date("2026-08-15T00:00:01.000Z"),"unbound-ticket-run","owner-a")).toBe(false);
      expect(store.markOutboxFailed(failureOutbox.outboxId,"must remain pending","unbound-ticket-run","owner-a")).toBe(false);
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT delivery_status,delivery_run_id,last_delivery_error FROM ticket_outbox WHERE outbox_id=?").get(successOutbox.outboxId)).toEqual({delivery_status:"pending",delivery_run_id:null,last_delivery_error:null});
      expect(db.prepare("SELECT delivery_status,delivery_run_id,last_delivery_error FROM ticket_outbox WHERE outbox_id=?").get(failureOutbox.outboxId)).toEqual({delivery_status:"pending",delivery_run_id:null,last_delivery_error:null});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("requires the exact bound Ticket delivery run and owner to settle", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-bound-run-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    try {
      const ticket=store.accept({runId:"bound-ticket",ownerSessionKey:"owner-a",prompt:"terminal work"});
      const lease=store.claim({ticketId:ticket.ticketId,workerId:"worker-bound",leaseMs:10_000})!;
      store.complete({...lease,result:{ok:true}});
      const outbox=store.pendingOutbox()[0];
      expect(store.bindOutboxRun(outbox.outboxId,"run-a","owner-a")).toBe(true);
      expect(store.bindOutboxRun(outbox.outboxId,"run-a","owner-a")).toBe(true);
      expect(store.bindOutboxRun(outbox.outboxId,"run-b","owner-a")).toBe(false);
      expect(store.markOutboxDelivered(outbox.outboxId,new Date(),"run-b","owner-a")).toBe(false);
      expect(store.markOutboxDelivered(outbox.outboxId,new Date(),"run-a","owner-b")).toBe(false);
      expect(store.markOutboxDelivered(outbox.outboxId,new Date("2026-08-15T00:00:01.000Z"),"run-a","owner-a")).toBe(true);
      expect(store.markOutboxDelivered(outbox.outboxId,new Date(),"run-a","owner-a")).toBe(false);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("keeps a successful direct Ticket response-ready until delivery is confirmed", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-direct-delivery-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    const ticket=store.accept({runId:"direct-ok",ownerSessionKey:"owner",prompt:"simple work"});
    store.route(ticket.ticketId,false);
    expect(store.finalizeDirectRun({runId:"direct-ok",success:true,interrupted:false,expectsDelivery:true,now:new Date("2026-08-15T00:00:00.000Z")})).toBe("awaiting_delivery");

    let db=new DatabaseSync(path,{readOnly:true});
    const ready=db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any;
    expect(ready.status).toBe("accepted");
    expect(ready.response_ready_at).toBe("2026-08-15T00:00:00.000Z");
    expect(ready.delivery_confirmed_at).toBeNull();
    expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type))
      .toEqual(["accepted","routed","response_ready"]);
    db.close();

    expect(store.confirmDirectDelivery({runId:"direct-ok",now:new Date("2026-08-15T00:00:05.000Z")})).toBe("completed");
    db=new DatabaseSync(path,{readOnly:true});
    const delivered=db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any;
    expect(delivered).toEqual({status:"completed",delivery_confirmed_at:"2026-08-15T00:00:05.000Z"});
    expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type))
      .toEqual(["accepted","routed","response_ready","delivery_confirmed","completed"]);
    db.close();
    rmSync(root,{recursive:true,force:true});
  });

  it("promotes interrupted direct work to durable recovery", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-direct-interrupt-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    const interrupted=store.accept({runId:"direct-stop",ownerSessionKey:"owner",prompt:"create several related files"});
    store.route(interrupted.ticketId,false);
    expect(store.finalizeDirectRun({runId:"direct-stop",success:false,interrupted:true,message:"operation aborted"})).toBe("waiting");
    expect(store.ready().map(x=>x.ticketId)).toEqual([interrupted.ticketId]);
    const db=new DatabaseSync(path,{readOnly:true});
    expect(db.prepare("SELECT status,failure_class,workflow_eligible FROM tickets WHERE ticket_id=?").get(interrupted.ticketId))
      .toEqual({status:"waiting",failure_class:"interrupted",workflow_eligible:1});
    db.close();
    rmSync(root,{recursive:true,force:true});
  });

  it("promotes a response-ready Ticket when final delivery fails", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-delivery-fail-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    const ticket=store.accept({runId:"partial-output",ownerSessionKey:"owner",prompt:"write a long answer"});
    store.route(ticket.ticketId,false);
    expect(store.finalizeDirectRun({runId:"partial-output",success:true,interrupted:false,expectsDelivery:true})).toBe("awaiting_delivery");
    expect(store.failDirectDelivery({runId:"partial-output",message:"final reply interrupted after partial output"})).toBe("waiting");
    const db=new DatabaseSync(path,{readOnly:true});
    expect(db.prepare("SELECT status,workflow_eligible,failure_class,delivery_last_error FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
      .toEqual({status:"waiting",workflow_eligible:1,failure_class:"interrupted",delivery_last_error:"final reply interrupted after partial output"});
    expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type))
      .toEqual(["accepted","routed","response_ready","direct_delivery_failed"]);
    db.close(); rmSync(root,{recursive:true,force:true});
  });

  it("recovers a response-ready Ticket only after the delivery receipt deadline", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-delivery-timeout-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    const ticket=store.accept({runId:"receipt-timeout",ownerSessionKey:"owner",prompt:"long answer"});
    store.route(ticket.ticketId,false);
    store.finalizeDirectRun({runId:"receipt-timeout",success:true,interrupted:false,expectsDelivery:true,now:new Date("2026-08-15T00:00:00.000Z")});
    expect(store.recoverUndeliveredDirect({now:new Date("2026-08-15T00:00:20.000Z"),olderThanMs:30_000})).toEqual([]);
    expect(store.recoverUndeliveredDirect({now:new Date("2026-08-15T00:00:31.000Z"),olderThanMs:30_000})).toEqual([{ticketId:ticket.ticketId,runId:"receipt-timeout"}]);
    const db=new DatabaseSync(path,{readOnly:true});
    expect(db.prepare("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
      .toEqual({status:"waiting",workflow_eligible:1,failure_class:"interrupted"});
    db.close(); rmSync(root,{recursive:true,force:true});
  });

  it("claims once and advances a generation after lease recovery", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const store = new TicketStore(join(root, "tickets.sqlite3"));
    const ticket = store.accept({runId:"claim-run",ownerSessionKey:"owner",prompt:"work"});
    store.route(ticket.ticketId,true);
    const start = new Date("2026-08-13T00:00:00.000Z");
    const first = store.claim({ticketId:ticket.ticketId,workerId:"worker-a",leaseMs:1000,now:start})!;
    expect(store.claim({ticketId:ticket.ticketId,workerId:"worker-b",leaseMs:1000,now:start})).toBeUndefined();
    expect(store.recoverExpired({now:new Date("2026-08-13T00:00:02.000Z")})).toEqual([{
      ticketId:ticket.ticketId,previousWorkerId:"worker-a",previousLeaseGeneration:1,status:"waiting",
    }]);
    const second = store.claim({ticketId:ticket.ticketId,workerId:"worker-b",leaseMs:1000,now:new Date("2026-08-13T00:00:02.000Z")})!;
    expect(second.leaseGeneration).toBe(2);
    expect(second.leaseToken).not.toBe(first.leaseToken);
    rmSync(root,{recursive:true,force:true});
  });

  it("fences an old worker after recovery and lets the current worker complete", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const store = new TicketStore(join(root, "tickets.sqlite3"));
    const ticket = store.accept({runId:"fence-run",ownerSessionKey:"owner",prompt:"work"});
    store.route(ticket.ticketId,true);
    const t0 = new Date("2026-08-13T00:00:00.000Z");
    const oldLease = store.claim({ticketId:ticket.ticketId,workerId:"worker-a",leaseMs:1000,now:t0})!;
    store.recoverExpired({now:new Date("2026-08-13T00:00:02.000Z")});
    const current = store.claim({ticketId:ticket.ticketId,workerId:"worker-b",leaseMs:5000,now:new Date("2026-08-13T00:00:02.000Z")})!;
    expect(() => store.heartbeat({...oldLease,leaseMs:5000,now:new Date("2026-08-13T00:00:02.500Z")})).toThrow(/stale/);
    expect(() => store.complete({...oldLease,result:{bad:true},now:new Date("2026-08-13T00:00:02.500Z")})).toThrow(/stale/);
    const renewed = store.heartbeat({...current,leaseMs:5000,now:new Date("2026-08-13T00:00:03.000Z")});
    store.complete({...renewed,result:{ok:true},now:new Date("2026-08-13T00:00:04.000Z")});
    const db = new DatabaseSync(join(root,"tickets.sqlite3"),{readOnly:true});
    expect(db.prepare("SELECT status,result_json,lease_generation FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
      .toEqual({status:"completed",result_json:'{"ok":true}',lease_generation:2});
    expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type))
      .toEqual(["accepted","routed","claimed","lease_expired","claimed","completed"]);
    db.close();
    rmSync(root,{recursive:true,force:true});
  }, 15_000);
});