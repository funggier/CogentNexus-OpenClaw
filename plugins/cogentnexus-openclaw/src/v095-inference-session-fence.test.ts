import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { deleteSessionByKey, finalizeSessionDeletion, sessionAuthority } from "./v090.js";
import { TicketStore } from "./ticket-store.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";

describe("v0.9.5 inference session-generation fence", () => {
  it("rejects terminal inference evidence from a deleted lifecycle", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-inference-session-fence-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:inference-fence";
      const store = new TicketStore(path);
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "legacy-run", ownerSessionKey: sessionKey, prompt: "stale inference" });
      store.route(ticket.ticketId, false);
      const generation = sessionAuthority(path, sessionKey).generation;
      const db = new DatabaseSync(path);
      try {
        const attempt = beginInferenceAttempt(db, {
          ticketId: ticket.ticketId,
          sessionKey,
          sessionGeneration: generation,
          callId: "call-old-lifecycle",
          provider: "openai",
          model: "m1",
        });
        bindRunId(db, attempt.attemptId, "run-old");
        deleteSessionByKey(path, { sessionKey, sessionId: "S1", message: "session deleted" });
        finalizeSessionDeletion(path, sessionKey, "session deleted");
        expect(sessionAuthority(path, sessionKey)).toEqual({ state: "deleted", generation: generation + 1 });
        expect(() => finishInferenceAttempt(db, attempt.attemptId, "late-success"))
          .toThrow(/session|generation|stale/i);
        expect(db.prepare("SELECT state,outcome,session_generation FROM cnx_inference_attempt WHERE attempt_id=?").get(attempt.attemptId))
          .toMatchObject({ state: "active", outcome: null, session_generation: generation });
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
