import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { beginInferenceAttempt, bindRunId, findInferenceAttempt, finishInferenceAttempt } from "./v095-inference-attempt.js";

describe("v0.9.5 canonical inference attempt identity", () => {
  it("keeps Ticket/session identity stable while each inference retry gets a new call-scoped attempt identity", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-inference-attempt-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:webchat:channel:v095-attempt";
      const store = new TicketStore(databasePath);
      sessionAuthority(databasePath, sessionKey);
      const ticket = store.accept({ runId: "legacy-run-a", ownerSessionKey: sessionKey, prompt: "identity test" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(databasePath);
      try {
        const first = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey,
          sessionGeneration: 0,
          callId: "call-a",
          provider: "ollama",
          model: "m1",
          now: new Date("2026-09-10T08:00:00.000Z"),
        });
        expect(first).toMatchObject({
          ticketId: ticket.ticketId,
          sessionKey,
          sessionGeneration: 0,
          callId: "call-a",
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
          sessionKey,
          sessionGeneration: 0,
          callId: "call-b",
          provider: "openai",
          model: "m2",
          now: new Date("2026-09-10T08:00:01.000Z"),
        });
        expect(bindRunId(db, second.attemptId, "run-a").runId).toBe("run-a");
        expect(second.ticketId).toBe(first.ticketId);
        expect(second.sessionKey).toBe(first.sessionKey);
        expect(second.sessionGeneration).toBe(0);
        expect(second.attemptId).not.toBe(first.attemptId);
        expect(second.callId).not.toBe(first.callId);
        expect(second.provider).toBe("openai");
        expect(second.model).toBe("m2");
        expect(findInferenceAttempt(db, "run-a", "call-a")?.attemptId).toBe(first.attemptId);
        expect(findInferenceAttempt(db, "run-a", "call-b")?.attemptId).toBe(second.attemptId);
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
      const sessionKey = "agent:main:webchat:channel:v095-db";
      const store = new TicketStore(databasePath);
      sessionAuthority(databasePath, sessionKey);
      const ticket = store.accept({ runId: "legacy-run-b", ownerSessionKey: sessionKey, prompt: "db proof" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(databasePath);
      try {
        const attempt = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey,
          sessionGeneration: 0,
          callId: "call-db",
          provider: null,
          model: null,
          now: new Date("2026-09-10T09:00:00.000Z"),
        });
        expect(() => bindRunId(db, attempt.attemptId, "run-b")).not.toThrow();
        const ended = finishInferenceAttempt(db, attempt.attemptId, "completed");
        expect(ended).toMatchObject({ state: "ended", outcome: "completed", runId: "run-b", callId: "call-db" });
        expect(() => finishInferenceAttempt(db, attempt.attemptId, "late-error")).toThrow(/not active/i);

        expect(db.prepare("SELECT attempt_id,ticket_id,session_key,session_generation,run_id,call_id,provider,model,state,outcome FROM cnx_inference_attempt WHERE attempt_id=?").get(attempt.attemptId)).toMatchObject({
          attempt_id: attempt.attemptId,
          ticket_id: ticket.ticketId,
          session_key: sessionKey,
          session_generation: 0,
          run_id: "run-b",
          call_id: "call-db",
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
