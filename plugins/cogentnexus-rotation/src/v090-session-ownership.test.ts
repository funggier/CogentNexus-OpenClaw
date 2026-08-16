import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  boundedOwnerContext,
  cancelSessionByKey,
  deleteSessionByKey,
  executeCompatibilityWake,
  finalizeSessionDeletion,
  patchTicketStore,
  queueAssistantDelivery,
  resetSessionByKey,
  sessionAuthority,
} from "./v090.js";

describe("v0.9 session ownership isolation", () => {
  patchTicketStore();

  it("UI Stop revokes only the exact owner session and advances its generation", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-session-stop-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const a1 = store.accept({ runId:"a1", ownerSessionKey:"agent:main:dashboard:A", prompt:"A1" });
      const a2 = store.accept({ runId:"a2", ownerSessionKey:"agent:main:dashboard:A", prompt:"A2" });
      const b1 = store.accept({ runId:"b1", ownerSessionKey:"agent:main:dashboard:B", prompt:"B1" });
      store.route(a1.ticketId,false); store.route(a2.ticketId,true); store.route(b1.ticketId,true);
      const beforeA = sessionAuthority(path,"agent:main:dashboard:A");
      const beforeB = sessionAuthority(path,"agent:main:dashboard:B");

      const cancelled = cancelSessionByKey(path,{sessionKey:"agent:main:dashboard:A",message:"agent run aborted"});
      expect(cancelled.cancelled.sort()).toEqual([a1.ticketId,a2.ticketId].sort());
      expect(sessionAuthority(path,"agent:main:dashboard:A")).toEqual({state:"active",generation:beforeA.generation+1});
      expect(sessionAuthority(path,"agent:main:dashboard:B")).toEqual(beforeB);

      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a1.ticketId)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a2.ticketId)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(b1.ticketId)).toEqual({status:"accepted"});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("Reset creates a new generation on the same session key without touching another session", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-session-reset-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const a = store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:A",prompt:"A work"});
      const b = store.accept({runId:"b",ownerSessionKey:"agent:main:dashboard:B",prompt:"B work"});
      store.route(a.ticketId,true); store.route(b.ticketId,true);
      const before = sessionAuthority(path,"agent:main:dashboard:A");
      const other = sessionAuthority(path,"agent:main:dashboard:B");

      const reset = resetSessionByKey(path,{sessionKey:"agent:main:dashboard:A",message:"session reset"});
      expect(reset.cancelled).toEqual([a.ticketId]);
      expect(sessionAuthority(path,"agent:main:dashboard:A")).toEqual({state:"active",generation:before.generation+1});
      expect(sessionAuthority(path,"agent:main:dashboard:B")).toEqual(other);

      const next = store.accept({runId:"a-next",ownerSessionKey:"agent:main:dashboard:A",prompt:"new generation"});
      expect(next.ownerSessionKey).toBe("agent:main:dashboard:A");
      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a.ticketId)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(b.ticketId)).toEqual({status:"accepted"});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=? AND event_type='cancelled_by_session_reset'").get(a.ticketId))
        .toEqual({count:1});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("Delete tombstones one session, preserves its durable history, and does not transfer ownership", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-session-delete-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const a = store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:A",prompt:"A work"});
      const b = store.accept({runId:"b",ownerSessionKey:"agent:main:dashboard:B",prompt:"B work"});
      store.route(a.ticketId,true); store.route(b.ticketId,true);

      const deletion = deleteSessionByKey(path,{sessionKey:"agent:main:dashboard:A",message:"session deleted"});
      finalizeSessionDeletion(path,"agent:main:dashboard:A","session deleted");
      expect(deletion.cancelled).toEqual([a.ticketId]);
      expect(sessionAuthority(path,"agent:main:dashboard:A").state).toBe("deleted");
      expect(sessionAuthority(path,"agent:main:dashboard:B").state).toBe("active");

      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT owner_session_key,status FROM tickets WHERE ticket_id=?").get(a.ticketId))
        .toEqual({owner_session_key:"agent:main:dashboard:A",status:"cancelled"});
      expect(db.prepare("SELECT owner_session_key,status FROM tickets WHERE ticket_id=?").get(b.ticketId))
        .toEqual({owner_session_key:"agent:main:dashboard:B",status:"accepted"});
      db.close();

      expect(() => store.accept({runId:"a-new",ownerSessionKey:"agent:main:dashboard:A",prompt:"must not revive"}))
        .toThrow(/session is deleted/i);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("rejects late assistant delivery from a superseded session generation", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-generation-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:A",prompt:"work"});
      store.route(ticket.ticketId,false);
      const generation = sessionAuthority(path,"agent:main:dashboard:A").generation;
      expect(queueAssistantDelivery(path,{
        ticketId:ticket.ticketId,
        ownerSessionKey:"agent:main:dashboard:A",
        ownerGeneration:generation,
        kind:"notice",
        text:"old result",
        target:{kind:"notice"},
        idempotencyKey:"old-result",
      })).toBe(true);

      cancelSessionByKey(path,{sessionKey:"agent:main:dashboard:A",message:"stop"});
      expect(queueAssistantDelivery(path,{
        ticketId:ticket.ticketId,
        ownerSessionKey:"agent:main:dashboard:A",
        ownerGeneration:generation,
        kind:"notice",
        text:"late result",
        target:{kind:"notice"},
        idempotencyKey:"late-result",
      })).toBe(false);

      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT count(*) AS count FROM cnx_assistant_delivery WHERE status='pending'").get())
        .toEqual({count:0});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("does not execute a scheduled synthetic turn captured before Reset", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-stale-timer-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:A",prompt:"work"});
      const oldGeneration = sessionAuthority(path,"agent:main:dashboard:A").generation;
      resetSessionByKey(path,{sessionKey:"agent:main:dashboard:A",message:"reset"});
      let runs = 0;
      const api = { runtime:{ subagent:{
        getSessionMessages:async()=>({messages:[]}),
        run:async()=>{ runs++; return {runId:"must-not-run"}; },
        waitForRun:async()=>({status:"ok"}),
        deleteSession:async()=>{},
      }}, tasks:{} }, logger:{warn:()=>{}} };
      const result = await executeCompatibilityWake(api,{workspaceDir:root,ticketDatabasePath:path},{
        sessionKey:"agent:main:dashboard:A",
        ownerGeneration:oldGeneration,
        delayMs:0,
        deleteAfterRun:true,
        deliveryMode:"announce",
        name:"stale",
        tag:"stale-before-reset",
        message:"old scheduled internal work",
      } as any);
      expect(runs).toBe(0);
      expect(result).toMatchObject({queued:false,suppressed:true,reason:"session generation superseded"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("cross-session context is read-only and internal synthetic turns are excluded", () => {
    const context = boundedOwnerContext([
      {role:"user",content:"real message from another session"},
      {role:"assistant",content:"useful prior result"},
      {role:"user",content:"#cogent-direct\n[CogentNexus Continuation: internal]"},
      {role:"user",content:"[CogentNexus Delivery: ticket:9]\ninternal"},
    ]);
    expect(context).toContain("real message from another session");
    expect(context).toContain("useful prior result");
    expect(context).not.toContain("#cogent-direct");
    expect(context).not.toContain("CogentNexus Delivery");
  });
});
