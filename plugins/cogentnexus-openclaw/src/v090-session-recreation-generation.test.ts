import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  deleteSessionByKey,
  finalizeSessionDeletion,
  reactivateSessionForLifecycle,
  sessionAuthority,
} from "./v090.js";

describe("v0.9 session recreation generation", () => {
  it("reuses the tombstoned generation for a genuinely new lifecycle", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-recreate-generation-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:K";
      const store = new TicketStore(path);
      const old = store.accept({ runId: "old", ownerSessionKey: key, prompt: "old work" });
      store.route(old.ticketId, true);

      const before = sessionAuthority(path, key);
      deleteSessionByKey(path, { sessionKey: key, message: "deleted", sessionId: "A" });
      finalizeSessionDeletion(path, key, "deleted");
      const deleted = sessionAuthority(path, key);
      expect(deleted.state).toBe("deleted");
      expect(deleted.generation).toBe(before.generation + 1);

      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "A" }))
        .toMatchObject({ state: "deleted", accepted: false, lifecycleMatches: false, generation: deleted.generation });

      const recreated = reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "B" });
      expect(recreated).toMatchObject({
        state: "active",
        accepted: true,
        lifecycleMatches: true,
        generation: deleted.generation,
        sessionId: "B",
      });
      expect(sessionAuthority(path, key)).toEqual({ state: "active", generation: deleted.generation });

      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "A" }))
        .toMatchObject({ state: "active", accepted: false, lifecycleMatches: false, generation: deleted.generation, sessionId: "B" });
      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "C" }))
        .toMatchObject({ state: "active", accepted: false, lifecycleMatches: false, generation: deleted.generation, sessionId: "B" });
      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "B" }))
        .toMatchObject({ state: "active", accepted: true, lifecycleMatches: true, generation: deleted.generation, sessionId: "B" });

      expect(() => store.accept({ runId: "new", ownerSessionKey: key, prompt: "fresh work" })).not.toThrow();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
