import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  DIRECT_MODEL_CALL_TIMEOUT_MS,
  recordDirectModelCallEnded,
  recordDirectModelCallStarted,
} from "./v091-direct-model-call-lease.js";

describe("v0.9.1 Direct model-call durable lease", () => {
  it("tracks the actual provider call for a pre-response Direct Ticket", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-direct-call-"));
    const path = join(root, "tickets.sqlite3");
    try {
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "run-live", ownerSessionKey: "agent:main:dashboard:test", prompt: "ตอบสั้น ๆ" });
      store.route(ticket.ticketId, false);
      const startedAt = new Date("2026-08-18T13:00:00.000Z");
      expect(recordDirectModelCallStarted(path, {
        runId: "run-live",
        callId: "call-1",
        provider: "ollama",
        model: "qwen3.5:9b",
        now: startedAt,
      })).toBe(true);

      let db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare(`SELECT ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at
        FROM cnx_direct_model_call WHERE ticket_id=?`).get(ticket.ticketId)).toEqual({
        ticket_id: ticket.ticketId,
        run_id: "run-live",
        call_id: "call-1",
        state: "active",
        provider: "ollama",
        model: "qwen3.5:9b",
        started_at: "2026-08-18T13:00:00.000Z",
        deadline_at: new Date(startedAt.getTime() + DIRECT_MODEL_CALL_TIMEOUT_MS).toISOString(),
      });
      db.close();

      expect(recordDirectModelCallEnded(path, {
        runId: "run-live",
        callId: "call-1",
        outcome: "ok",
        durationMs: 1234,
        now: new Date("2026-08-18T13:00:01.234Z"),
      })).toBe(true);
      db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare(`SELECT state,ended_at,outcome,duration_ms FROM cnx_direct_model_call WHERE ticket_id=?`).get(ticket.ticketId))
        .toEqual({ state: "ended", ended_at: "2026-08-18T13:00:01.234Z", outcome: "ok", duration_ms: 1234 });
      expect((db.prepare(`SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id`).all(ticket.ticketId) as any[]).map(x => x.event_type))
        .toEqual(["accepted", "routed", "direct_model_call_started", "direct_model_call_ended"]);
      db.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("does not let a late model_call_ended revoke a Host recovery claim", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-direct-call-race-"));
    const path = join(root, "tickets.sqlite3");
    try {
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "run-race", ownerSessionKey: "agent:main:dashboard:test", prompt: "work" });
      store.route(ticket.ticketId, false);
      recordDirectModelCallStarted(path, { runId: "run-race", callId: "call-race", now: new Date("2026-08-18T13:00:00.000Z") });
      const db = new DatabaseSync(path);
      db.prepare(`UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,recovery_attempt_count=1 WHERE ticket_id=?`)
        .run("2026-08-18T13:15:01.000Z", ticket.ticketId);
      db.close();

      expect(recordDirectModelCallEnded(path, {
        runId: "run-race",
        callId: "call-race",
        outcome: "ok",
        now: new Date("2026-08-18T13:15:02.000Z"),
      })).toBe(false);
      const verify = new DatabaseSync(path, { readOnly: true });
      expect(verify.prepare(`SELECT state,recovery_attempt_count FROM cnx_direct_model_call WHERE ticket_id=?`).get(ticket.ticketId))
        .toEqual({ state: "recovering", recovery_attempt_count: 1 });
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("does not let a later model_call_started revoke a Host recovery claim", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-direct-call-next-race-"));
    const path = join(root, "tickets.sqlite3");
    try {
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "run-next-race", ownerSessionKey: "agent:main:dashboard:test", prompt: "work" });
      store.route(ticket.ticketId, false);
      recordDirectModelCallStarted(path, {
        runId: "run-next-race",
        callId: "call-first",
        now: new Date("2026-08-18T13:00:00.000Z"),
      });
      const db = new DatabaseSync(path);
      db.prepare(`UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,recovery_attempt_count=1 WHERE ticket_id=?`)
        .run("2026-08-18T13:15:01.000Z", ticket.ticketId);
      db.close();

      expect(recordDirectModelCallStarted(path, {
        runId: "run-next-race",
        callId: "call-second",
        now: new Date("2026-08-18T13:15:02.000Z"),
      })).toBe(false);

      const verify = new DatabaseSync(path, { readOnly: true });
      expect(verify.prepare(`SELECT call_id,state,recovery_started_at,recovery_attempt_count FROM cnx_direct_model_call WHERE ticket_id=?`)
        .get(ticket.ticketId)).toEqual({
          call_id: "call-first",
          state: "recovering",
          recovery_started_at: "2026-08-18T13:15:01.000Z",
          recovery_attempt_count: 1,
        });
      expect((verify.prepare(`SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id`).all(ticket.ticketId) as any[])
        .map((row) => row.event_type)).toEqual(["accepted", "routed", "direct_model_call_started"]);
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("ignores durable/workflow and already response-ready Tickets", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-direct-call-filter-"));
    const path = join(root, "tickets.sqlite3");
    try {
      const store = new TicketStore(path);
      const durable = store.accept({ runId: "run-durable", ownerSessionKey: "owner", prompt: "durable" });
      store.route(durable.ticketId, true);
      expect(recordDirectModelCallStarted(path, { runId: "run-durable", callId: "call-durable" })).toBe(false);

      const ready = store.accept({ runId: "run-ready", ownerSessionKey: "owner", prompt: "ready" });
      store.route(ready.ticketId, false);
      store.finalizeDirectRun({ runId: "run-ready", success: true, interrupted: false, expectsDelivery: true });
      expect(recordDirectModelCallStarted(path, { runId: "run-ready", callId: "call-ready" })).toBe(false);
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
