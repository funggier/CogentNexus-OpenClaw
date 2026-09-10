import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  deleteSessionByKey,
  finalizeSessionDeletion,
  queueAssistantDelivery,
  reactivateSessionForLifecycle,
  sessionAuthority,
} from "./v090.js";

describe("v0.9.5 canonical session deletion ownership", () => {
  it("invalidates operational ownership, preserves history, and recreates a new Discord lifecycle", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-session-delete-contract-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:contract-delete";
      const store = new TicketStore(path);
      const oldTicket = store.accept({ runId: "old-run", ownerSessionKey: key, prompt: "old work" });
      store.route(oldTicket.ticketId, false);
      const oldGeneration = sessionAuthority(path, key).generation;
      const text = "old pending assistant delivery";
      const db = new DatabaseSync(path);
      try {
        db.prepare(`INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at)
          VALUES (?,?,?,?,'pending',0,?)`).run(
          oldTicket.ticketId,
          key,
          "completed",
          JSON.stringify({ text }),
          "2026-09-10T13:00:00.000Z",
        );
        queueAssistantDelivery(path, {
          ticketId: oldTicket.ticketId,
          ownerSessionKey: key,
          ownerGeneration: oldGeneration,
          kind: "notice",
          text,
          target: { kind: "notice" },
          idempotencyKey: `cnx-delete-contract:${oldTicket.ticketId}`,
        });
        db.prepare(`INSERT INTO cnx_direct_recovery(
          ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at
        ) VALUES (?,?, 'pending',0,NULL,?,?,?, ?,?)`).run(
          oldTicket.ticketId,
          "resume",
          "2026-09-10T13:01:00.000Z",
          "pending before delete",
          oldGeneration,
          "2026-09-10T13:00:00.000Z",
          "2026-09-10T13:00:00.000Z",
        );
      } finally {
        db.close();
      }

      const deletion = deleteSessionByKey(path, { sessionKey: key, sessionId: "S1", message: "user deleted Discord session" });
      finalizeSessionDeletion(path, key, "user deleted Discord session");

      expect(deletion.cancelled).toEqual([oldTicket.ticketId]);
      expect(sessionAuthority(path, key)).toEqual({ state: "deleted", generation: oldGeneration + 1 });

      const afterDelete = new DatabaseSync(path, { readOnly: true });
      try {
        expect(afterDelete.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE owner_session_key=? AND delivery_status='pending'").get(key))
          .toEqual({ count: 0 });
        expect(afterDelete.prepare("SELECT count(*) AS count FROM cnx_assistant_delivery WHERE owner_session_key=? AND status='pending'").get(key))
          .toEqual({ count: 0 });
        expect(afterDelete.prepare("SELECT count(*) AS count FROM cnx_direct_recovery WHERE owner_generation=? AND state<>'cancelled'").get(oldGeneration))
          .toEqual({ count: 0 });
        const eventCount = afterDelete.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=?").get(oldTicket.ticketId) as { count: number };
        expect(eventCount.count).toBeGreaterThan(0);
        expect(afterDelete.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(oldTicket.ticketId))
          .toEqual({ status: "cancelled" });
      } finally {
        afterDelete.close();
      }

      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "S1" }))
        .toMatchObject({ state: "deleted", accepted: false, lifecycleMatches: false });
      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "S2" }))
        .toMatchObject({ state: "active", accepted: true, lifecycleMatches: true, generation: oldGeneration + 1 });
      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "S2" }))
        .toMatchObject({ state: "active", accepted: true, lifecycleMatches: true, generation: oldGeneration + 1 });
      expect(sessionAuthority(path, key)).toEqual({ state: "active", generation: oldGeneration + 1 });

      const fresh = store.accept({ runId: "new-run", ownerSessionKey: key, prompt: "fresh lifecycle work" });
      expect(fresh.ticketId).not.toBe(oldTicket.ticketId);
      const currentDb = new DatabaseSync(path, { readOnly: true });
      try {
        expect(currentDb.prepare("SELECT status,owner_session_key FROM tickets WHERE ticket_id=?").get(oldTicket.ticketId))
          .toEqual({ status: "cancelled", owner_session_key: key });
        expect(currentDb.prepare("SELECT status,owner_session_key FROM tickets WHERE ticket_id=?").get(fresh.ticketId))
          .toEqual({ status: "accepted", owner_session_key: key });
      } finally {
        currentDb.close();
      }

      const evidence = new DatabaseSync(path, { readOnly: true });
      try {
        const events = evidence.prepare("SELECT event_type,payload_json FROM ticket_events WHERE ticket_id=? ORDER BY created_at").all(oldTicket.ticketId) as Array<{ event_type: string; payload_json: string }>;
        expect(events.some((event) => event.event_type === "cancelled_by_session_delete")).toBe(true);
        expect(events.some((event) => event.payload_json.includes("user deleted Discord session"))).toBe(true);
      } finally {
        evidence.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
