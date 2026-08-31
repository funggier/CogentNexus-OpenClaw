import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { patchTicketStore } from "./v090.js";
import {
  isOpenClawAbortMessage,
  patchV090LivePolicy,
  reconcileV090LiveState,
} from "./v090-entry.js";

describe("CogentNexus-OpenClaw v0.9.0 live policy hardening", () => {
  patchTicketStore();
  patchV090LivePolicy();

  it("recognizes the installed OpenClaw AbortError rendering narrowly", () => {
    expect(isOpenClawAbortMessage("This operation was aborted")).toBe(true);
    expect(isOpenClawAbortMessage("This operation was aborted | 20")).toBe(true);
    expect(isOpenClawAbortMessage("  This operation was aborted | 20  ")).toBe(true);
    expect(isOpenClawAbortMessage("This operation was aborted | provider")).toBe(false);
    expect(isOpenClawAbortMessage("provider aborted operation")).toBe(false);
  });

  it("turns the live OpenClaw UI Stop form into session cancellation instead of permanent failure", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-live-abort-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const current = store.accept({ runId:"live-abort", ownerSessionKey:"agent:main:dashboard:owner", prompt:"long task" });
      const queued = store.accept({ runId:"queued", ownerSessionKey:"agent:main:dashboard:owner", prompt:"next task" });
      store.route(current.ticketId, false);
      store.route(queued.ticketId, true);

      expect(store.finalizeDirectRun({
        runId:"live-abort",
        success:false,
        interrupted:false,
        message:"This operation was aborted | 20",
      })).toBe("unchanged");

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(current.ticketId))
        .toEqual({ status:"cancelled", failure_class:null });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(queued.ticketId))
        .toEqual({ status:"cancelled" });
      expect(db.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE delivery_status='pending'").get())
        .toEqual({ count:0 });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("keeps a genuine permanent failure durable but does not wake inference to announce it", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-silent-failure-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId:"permanent-failure", ownerSessionKey:"agent:main:dashboard:owner", prompt:"task" });
      store.route(ticket.ticketId, false);

      expect(store.finalizeDirectRun({
        runId:"permanent-failure",
        success:false,
        interrupted:false,
        message:"provider rejected request permanently",
      })).toBe("failed");

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status:"failed", failure_class:"permanent", failure_message:"provider rejected request permanently" });
      expect(db.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").get(ticket.ticketId))
        .toEqual({ count:0 });
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=? AND event_type='failure_delivery_suppressed'").get(ticket.ticketId))
        .toEqual({ count:1 });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("migrates the exact real-machine failed abort fixture and suppresses stale failed outboxes", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-live-fixture-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const aborted = store.accept({ runId:"real-machine-abort", ownerSessionKey:"agent:main:dashboard:owner", prompt:"task" });
      const failed = store.accept({ runId:"real-failure", ownerSessionKey:"agent:main:dashboard:other", prompt:"other task" });
      store.route(aborted.ticketId, false);
      store.route(failed.ticketId, false);

      const db = new DatabaseSync(path);
      const stamp = new Date().toISOString();
      db.prepare("UPDATE tickets SET status='failed',failure_class='permanent',failure_message='This operation was aborted | 20' WHERE ticket_id=?").run(aborted.ticketId);
      db.prepare("UPDATE tickets SET status='failed',failure_class='permanent',failure_message='real permanent failure' WHERE ticket_id=?").run(failed.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'failed','{}','pending',2,?)")
        .run(aborted.ticketId,"agent:main:dashboard:owner",stamp);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'failed','{}','pending',3,?)")
        .run(failed.ticketId,"agent:main:dashboard:other",stamp);
      db.close();

      const result = reconcileV090LiveState(path);
      expect(result.abortFailuresCancelled).toBe(1);
      expect(result.abortOutboxSuppressed).toBe(1);
      expect(result.failedOutboxSuppressed).toBe(1);

      const verify = new DatabaseSync(path, { readOnly:true });
      expect(verify.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(aborted.ticketId))
        .toEqual({ status:"cancelled", failure_class:null });
      expect(verify.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(failed.ticketId))
        .toEqual({ status:"failed", failure_class:"permanent" });
      expect(verify.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE delivery_status='pending'").get())
        .toEqual({ count:0 });
      verify.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });
});
