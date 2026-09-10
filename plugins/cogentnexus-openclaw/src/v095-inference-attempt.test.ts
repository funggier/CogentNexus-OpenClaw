import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";

describe("v0.9.5 canonical inference attempt identity", () => {
  it("keeps Ticket/session identity stable while each inference retry gets a new attempt identity", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-inference-attempt-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const ticket = store.accept({ runId: "legacy-run-a", ownerSessionKey: "agent:main:webchat:channel:v095-attempt", prompt: "identity test" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(databasePath);
      try {
        const first = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey: ticket.ownerSessionKey,
          sessionGeneration: 3,
          provider: "ollama",
          model: "m1",
          now: new Date("2026-09-10T08:00:00.000Z"),
        });
        expect(first).toMatchObject({
          ticketId: ticket.ticketId,
          sessionKey: ticket.ownerSessionKey,
          sessionGeneration: 3,
          provider: "ollama",
          model: "m1",
          state: "active",
          runId: null,
          outcome: null,
          endedAt: null,
        });
        expect(first.attemptId).toBeTruthy();

        expect(bindRunId(db, first.attemptId, "run-a").runId).toBe("run-a");
        expect(finishInferenceAttempt(db, first.attemptId, "provider_connection_refused").state).toBe("ended");

        const second = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey: ticket.ownerSessionKey,
          sessionGeneration: 3,
          provider: "openai",
          model: "m2",
          now: new Date("2026-09-10T08:00:01.000Z"),
        });
        expect(second.ticketId).toBe(first.ticketId);
        expect(second.sessionKey).toBe(first.sessionKey);
        expect(second.sessionGeneration).toBe(3);
        expect(second.attemptId).not.toBe(first.attemptId);
        expect(second.provider).toBe("openai");
        expect(second.model).toBe("m2");
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("persists exact attempt identity and rejects duplicate terminal transition", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-inference-attempt-db-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const ticket = store.accept({ runId: "legacy-run-b", ownerSessionKey: "agent:main:webchat:channel:v095-db", prompt: "db proof" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(databasePath);
      try {
        const attempt = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey: ticket.ownerSessionKey,
          sessionGeneration: 4,
          provider: null,
          model: null,
          now: new Date("2026-09-10T09:00:00.000Z"),
        });
        expect(() => bindRunId(db, attempt.attemptId, "run-b")).not.toThrow();
        const ended = finishInferenceAttempt(db, attempt.attemptId, "completed");
        expect(ended).toMatchObject({ state: "ended", outcome: "completed", runId: "run-b" });
        expect(() => finishInferenceAttempt(db, attempt.attemptId, "late-error")).toThrow(/not active/i);

        expect(db.prepare("SELECT attempt_id,ticket_id,session_key,session_generation,run_id,provider,model,state,outcome FROM cnx_inference_attempt WHERE attempt_id=?").get(attempt.attemptId)).toMatchObject({
          attempt_id: attempt.attemptId,
          ticket_id: ticket.ticketId,
          session_key: ticket.ownerSessionKey,
          session_generation: 4,
          run_id: "run-b",
          provider: null,
          model: null,
          state: "ended",
          outcome: "completed",
        });
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
