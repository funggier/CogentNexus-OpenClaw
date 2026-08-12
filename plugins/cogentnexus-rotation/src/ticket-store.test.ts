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
    rmSync(root, {recursive:true,force:true});
  });

  it("does not ticket internal continuation messages", () => {
    expect(ticketIntakeEligible("The previous run was interrupted. Resume automatically")).toBe(false);
    expect(ticketIntakeEligible("ช่วยสรุปเรื่องนี้")).toBe(true);
  });

  it("throws instead of allowing an uncommitted command when storage is invalid", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-ticket-"));
    const path = join(root, "not-a-database.sqlite3");
    writeFileSync(path, "this is not sqlite", "utf8");
    expect(() => new TicketStore(path).accept({runId:"run-2",ownerSessionKey:"owner",prompt:"must persist"})).toThrow();
    rmSync(root, {recursive:true,force:true});
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
