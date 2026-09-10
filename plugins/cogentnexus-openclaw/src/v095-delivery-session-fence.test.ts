import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { deleteSessionByKey, finalizeSessionDeletion, sessionAuthority } from "./v090.js";
import { TicketStore } from "./ticket-store.js";
import { confirmDelivery, findExactDelivery, prepareDelivery, stageDelivery, acceptTransport } from "./v095-delivery-core.js";

describe("v0.9.5 delivery session-generation fence", () => {
  it("blocks stale staging/transport/confirmation after the owner lifecycle is deleted", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-delivery-session-fence-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:delivery-fence";
      const store = new TicketStore(path);
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "run-delivery-fence", ownerSessionKey: sessionKey, prompt: "stale delivery" });
      store.route(ticket.ticketId, false);
      const text = "delivery tied to S1";
      const payloadSha256 = createHash("sha256").update(text).digest("hex");
      const db = new DatabaseSync(path);
      try {
        const key = {
          ticketId: ticket.ticketId,
          inferenceAttemptId: "attempt-S1",
          runId: "run-delivery-fence",
          ownerSessionKey: sessionKey,
          ownerGeneration: 0,
          surface: "discord" as const,
          payloadSha256,
          idempotencyKey: `cnx-delivery:${ticket.ticketId}:s1`,
        };
        prepareDelivery(db, { ...key, text });
        deleteSessionByKey(path, { sessionKey, sessionId: "S1", message: "session deleted" });
        finalizeSessionDeletion(path, sessionKey, "session deleted");

        expect(() => stageDelivery(db, key.idempotencyKey, { evidenceType: "late-stage" }))
          .toThrow(/delivery owner session is not active|generation is stale/i);
        expect(() => acceptTransport(db, key.idempotencyKey, { evidenceType: "late-transport" }))
          .toThrow(/illegal delivery transition|delivery owner session is not active|generation is stale/i);
        expect(() => confirmDelivery(db, key.idempotencyKey, { evidenceType: "late-receipt" }))
          .toThrow(/delivery owner session is not active|generation is stale|illegal delivery transition/i);
        expect(findExactDelivery(db, { ...key, inferenceAttemptId: "attempt-S2" })).toBeNull();
        expect(store.get(ticket.ticketId)?.status).toBe("cancelled");
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
