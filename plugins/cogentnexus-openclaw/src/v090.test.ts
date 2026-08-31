import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore, ticketIntakeEligible } from "./ticket-store.js";
import {
  cancelSessionByKey,
  cancelSessionTickets,
  directRecoveryBackoffMs,
  isExplicitUserCancellation,
  markDirectRecovery,
  patchTicketStore,
  prepareV090RecoveryState,
} from "./v090.js";

describe("CogentNexus-OpenClaw v0.9.0 intent boundary", () => {
  patchTicketStore();

  it("cancels the current and queued Tickets for the same owner session", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-cancel-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const current = store.accept({ runId:"run-current", ownerSessionKey:"agent:main:dashboard:owner", prompt:"ทำต่อครับ" });
      const queued = store.accept({ runId:"run-queued", ownerSessionKey:"agent:main:dashboard:owner", prompt:"งานถัดไป" });
      const other = store.accept({ runId:"run-other", ownerSessionKey:"agent:main:dashboard:other", prompt:"อีก session" });
      store.route(current.ticketId,false);
      store.route(queued.ticketId,true);
      store.route(other.ticketId,true);

      expect(markDirectRecovery(path,{runId:"run-current",mode:"resume",message:"provider interrupted"})).toBe(true);
      const result = store.finalizeDirectRun({
        runId:"run-current",
        success:false,
        interrupted:true,
        message:"Reply operation aborted by user",
      });
      expect(result).toBe("unchanged");

      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(current.ticketId)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(queued.ticketId)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(other.ticketId)).toEqual({status:"accepted"});
      expect(db.prepare("SELECT state,active_run_id,next_attempt_at FROM cnx_direct_recovery WHERE ticket_id=?").get(current.ticketId))
        .toEqual({state:"cancelled",active_run_id:null,next_attempt_at:null});
      const events = db.prepare("SELECT ticket_id,event_type FROM ticket_events WHERE event_type='cancelled_by_user' ORDER BY ticket_id").all();
      expect(events).toHaveLength(2);
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("UI Stop suppresses pending synthetic delivery even when no non-terminal Ticket remains", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-v090-synthetic-stop-"));
    try{
      const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
      const ticket=store.accept({runId:"old-human",ownerSessionKey:"agent:main:dashboard:owner",prompt:"old"});
      store.route(ticket.ticketId,false);
      expect(markDirectRecovery(path,{runId:"old-human",mode:"resume",message:"connection refused"})).toBe(true);
      const db=new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='cancelled',failure_class='interrupted' WHERE ticket_id=?").run(ticket.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'cancelled','{}','pending',3,?)")
        .run(ticket.ticketId,"agent:main:dashboard:owner",new Date().toISOString());
      db.close();
      const cancelled=cancelSessionByKey(path,{sessionKey:"agent:main:dashboard:owner",message:"agent run aborted"});
      expect(cancelled.cancelled).toEqual([]);
      expect(cancelled.outboxTags).toEqual([`cogent-ticket-result-${ticket.ticketId}`]);
      const verify=new DatabaseSync(path,{readOnly:true});
      expect(verify.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE delivery_status='pending'").get()).toEqual({count:0});
      expect(verify.prepare("SELECT state,active_run_id,next_attempt_at FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"cancelled",active_run_id:null,next_attempt_at:null});
      verify.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("keeps a generic interruption recoverable instead of guessing user intent", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-interrupt-"));
    try {
      const path = join(root,"tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({runId:"generic-interrupt",ownerSessionKey:"agent:main:dashboard:test",prompt:"สวัสดี"});
      store.route(ticket.ticketId,false);
      expect(store.finalizeDirectRun({runId:"generic-interrupt",success:false,interrupted:true,message:"provider interrupted"})).toBe("waiting");
      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:"interrupted"});
      expect(db.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({state:"pending"});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("migrates the legacy exact user-abort state to cancelled instead of resurrecting it", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-legacy-abort-"));
    try {
      const path = join(root,"tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({runId:"legacy-abort",ownerSessionKey:"agent:main:dashboard:test",prompt:"สวัสดี"});
      store.route(ticket.ticketId,false);
      const db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='failed',workflow_eligible=0,failure_class='permanent',failure_message='Reply operation aborted by user' WHERE ticket_id=?").run(ticket.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'failed','{}','pending',1,?)")
        .run(ticket.ticketId,"agent:main:dashboard:test",new Date().toISOString());
      db.close();

      const prepared = prepareV090RecoveryState(root,{ticketDatabasePath:path});
      expect(prepared.cancelledLegacy).toBe(1);
      expect(prepared.reopened).toBe(0);
      const verify = new DatabaseSync(path,{readOnly:true});
      expect(verify.prepare("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"cancelled",workflow_eligible:0,failure_class:null});
      expect(verify.prepare("SELECT COUNT(*) AS count FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").get(ticket.ticketId))
        .toEqual({count:0});
      verify.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("keeps Direct Recovery synthetic prompts outside human Ticket intake", () => {
    expect(ticketIntakeEligible("#cogent-direct\n[CogentNexus-OpenClaw Continuation: direct-recovery:CNXT-test]\nResume committed state.")).toBe(false);
    expect(ticketIntakeEligible("ทำงานนี้ต่อให้ผมครับ")).toBe(true);
  });

  it("uses a narrow user-cancellation classifier and bounded recovery backoff", () => {
    expect(isExplicitUserCancellation("Reply operation aborted by user")).toBe(true);
    expect(isExplicitUserCancellation("agent run aborted")).toBe(true);
    expect(isExplicitUserCancellation("agent run aborted for restart")).toBe(false);
    expect(isExplicitUserCancellation("explicit user stop")).toBe(true);
    expect(isExplicitUserCancellation("provider interrupted")).toBe(false);
    expect(isExplicitUserCancellation("connection refused by provider endpoint")).toBe(false);
    expect([1,2,3,4,5,6,99].map(directRecoveryBackoffMs))
      .toEqual([5000,15000,30000,60000,120000,300000,300000]);
  });

  it("can apply the session cancellation barrier directly", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-direct-cancel-"));
    try {
      const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
      const a=store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:test",prompt:"a"});
      const b=store.accept({runId:"b",ownerSessionKey:"agent:main:dashboard:test",prompt:"b"});
      store.route(a.ticketId,false); store.route(b.ticketId,true);
      const db=new DatabaseSync(path);db.prepare("UPDATE tickets SET status='running',workflow_id='WF-CANCELLED' WHERE ticket_id=?").run(a.ticketId);db.close();
      const cancelled=cancelSessionTickets(path,{runId:"a",message:"explicit user stop"});
      expect(cancelled.cancelled.sort()).toEqual([a.ticketId,b.ticketId].sort());
      expect(cancelled.workflowIds).toEqual(["WF-CANCELLED"]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
});
