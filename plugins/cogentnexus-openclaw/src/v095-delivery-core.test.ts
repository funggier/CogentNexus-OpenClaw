import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { confirmDelivery, findExactDelivery, prepareDelivery, stageDelivery, acceptTransport } from "./v095-delivery-core.js";

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v095-delivery-core-"));
  const databasePath = join(root, "tickets.sqlite3");
  const sessionKey = "agent:main:discord:channel:core095001";
  const store = new TicketStore(databasePath);
  sessionAuthority(databasePath, sessionKey);
  const ticket = store.accept({ runId: "core-run-a", ownerSessionKey: sessionKey, prompt: "delivery core" });
  store.route(ticket.ticketId, false);
  const db = new DatabaseSync(databasePath);
  const text = "Discord canonical delivery";
  const payloadSha256 = createHash("sha256").update(text).digest("hex");
  return { root, db, sessionKey, ticket, text, payloadSha256 };
}

describe("v0.9.5 canonical DeliveryAttempt state machine", () => {
  it("enforces prepared -> staged -> transport_accepted -> confirmed and is idempotent", () => {
    const { root, db, sessionKey, ticket, text, payloadSha256 } = setup();
    try {
      const key = {
        ticketId: ticket.ticketId,
        inferenceAttemptId: "cnx-attempt-a",
        runId: "core-run-a",
        ownerSessionKey: sessionKey,
        ownerGeneration: 0,
        surface: "discord" as const,
        payloadSha256,
        idempotencyKey: `cnx-delivery:${ticket.ticketId}:g0:a`,
      };
      const prepared = prepareDelivery(db, { ...key, text });
      expect(prepared.state).toBe("prepared");
      expect(findExactDelivery(db, key)?.deliveryId).toBe(prepared.deliveryId);
      expect(prepareDelivery(db, { ...key, text })).toMatchObject({ deliveryId: prepared.deliveryId, state: "prepared" });

      const staged = stageDelivery(db, key.idempotencyKey, { evidenceType: "discord-final-staged" });
      expect(staged.state).toBe("staged");
      expect(stageDelivery(db, key.idempotencyKey, { evidenceType: "discord-final-staged" }).state).toBe("staged");

      const accepted = acceptTransport(db, key.idempotencyKey, { evidenceType: "discord-send-accepted" });
      expect(accepted.state).toBe("transport_accepted");

      const confirmed = confirmDelivery(db, key.idempotencyKey, { evidenceType: "discord-receipt-confirmed", now: new Date("2026-09-10T10:00:00.000Z") });
      expect(confirmed.state).toBe("confirmed");
      expect(confirmDelivery(db, key.idempotencyKey, { evidenceType: "duplicate-confirm", now: new Date("2026-09-10T10:00:01.000Z") })).toMatchObject({
        deliveryId: confirmed.deliveryId,
        state: "confirmed",
      });

      const row = db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any;
      expect(row).toEqual({ status: "completed", delivery_confirmed_at: "2026-09-10T10:00:00.000Z" });
      const events = db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? AND event_type IN ('delivery_confirmed','completed')").all(ticket.ticketId) as Array<{ event_type?: string }>;
      expect(events.map((item) => item.event_type).sort()).toEqual(["completed", "delivery_confirmed"]);
    } finally {
      db.close();
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("rejects confirmation from a stale generation or incomplete transport state", () => {
    const { root, db, sessionKey, ticket, text, payloadSha256 } = setup();
    try {
      const key = {
        ticketId: ticket.ticketId,
        inferenceAttemptId: "cnx-attempt-b",
        runId: "core-run-a",
        ownerSessionKey: sessionKey,
        ownerGeneration: 0,
        surface: "discord" as const,
        payloadSha256,
        idempotencyKey: `cnx-delivery:${ticket.ticketId}:g0:b`,
      };
      prepareDelivery(db, { ...key, text });
      expect(() => confirmDelivery(db, key.idempotencyKey, { evidenceType: "too-early" })).toThrow(/illegal delivery transition prepared -> confirmed/);
      const session = db.prepare("UPDATE cnx_sessions SET generation=1,updated_at=? WHERE session_key=?").run(new Date("2026-09-10T11:00:00.000Z").toISOString(), sessionKey);
      expect(session.changes).toBe(1);
      expect(() => prepareDelivery(db, { ...key, ownerGeneration: 1, text })).toThrow(/delivery idempotency key is already bound to different exact identity/i);
      expect((db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any).status).toBe("accepted");
    } finally {
      db.close();
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("rejects an otherwise-valid transport acceptance after the owner session generation rotates", () => {
    const { root, db, sessionKey, ticket, text, payloadSha256 } = setup();
    try {
      const key = {
        ticketId: ticket.ticketId,
        inferenceAttemptId: "cnx-attempt-c",
        runId: "core-run-a",
        ownerSessionKey: sessionKey,
        ownerGeneration: 0,
        surface: "discord" as const,
        payloadSha256,
        idempotencyKey: `cnx-delivery:${ticket.ticketId}:g0:c`,
      };
      prepareDelivery(db, { ...key, text });
      stageDelivery(db, key.idempotencyKey, { evidenceType: "discord-final-staged" });
      acceptTransport(db, key.idempotencyKey, { evidenceType: "discord-send-accepted" });
      const rotated = db.prepare("UPDATE cnx_sessions SET generation=1,updated_at=? WHERE session_key=?").run(new Date("2026-09-10T12:00:00.000Z").toISOString(), sessionKey);
      expect(rotated.changes).toBe(1);
      expect(() => confirmDelivery(db, key.idempotencyKey, { evidenceType: "stale-receipt" })).toThrow(/delivery owner generation is stale/i);
      expect((db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any).status).toBe("accepted");
      expect((db.prepare("SELECT status,delivery_state FROM cnx_assistant_delivery WHERE idempotency_key=?").get(key.idempotencyKey) as any)).toEqual({
        status: "pending",
        delivery_state: "transport_accepted",
      });
    } finally {
      db.close();
      rmSync(root, { recursive: true, force: true });
    }
  });
});