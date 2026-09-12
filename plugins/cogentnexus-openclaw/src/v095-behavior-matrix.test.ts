import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { confirmDelivery, prepareDelivery, stageDelivery, acceptTransport } from "./v095-delivery-core.js";
import { stageDiscordDelivery } from "./v095-delivery-discord.js";
import { shouldAdvanceSessionGeneration } from "./v095-session-generation.js";

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v095-matrix-"));
  const databasePath = join(root, "tickets.sqlite3");
  const sessionKey = "agent:main:dashboard:matrix095001";
  const store = new TicketStore(databasePath);
  sessionAuthority(databasePath, sessionKey);
  const ticket = store.accept({ runId: "matrix-run-a", ownerSessionKey: sessionKey, prompt: "matrix" });
  store.route(ticket.ticketId, false);
  const db = new DatabaseSync(databasePath);
  return { root, db, sessionKey, ticket };
}

describe("v0.9.5 provider-independent behavior matrix", () => {
  it.each(["normal", "gateway_restart", "provider_switch", "idle_tick"])(
    "does not advance lifecycle generation for %s",
    (event) => {
      expect(shouldAdvanceSessionGeneration(event === "provider_switch" ? "provider_change" : event as any, false)).toBe(false);
    },
  );

  it("keeps exact delivery fenced when provider class changes", () => {
    const { root, db, sessionKey, ticket } = setup();
    try {
      const text = "matrix delivery";
      const payloadSha256 = createHash("sha256").update(text).digest("hex");
      const key = {
        ticketId: ticket.ticketId,
        inferenceAttemptId: "matrix-attempt-a",
        runId: "matrix-run-a",
        ownerSessionKey: sessionKey,
        ownerGeneration: 0,
        surface: "webchat" as const,
        payloadSha256,
        idempotencyKey: `cnx-delivery:${ticket.ticketId}:matrix`,
      };

      expect(prepareDelivery(db, { ...key, text }).state).toBe("prepared");
      expect(stageDelivery(db, key.idempotencyKey, { evidenceType: "webchat-final-staged" }).state).toBe("staged");
      expect(acceptTransport(db, key.idempotencyKey, { evidenceType: "webchat-send-accepted" }).state).toBe("transport_accepted");

      db.prepare("UPDATE cnx_sessions SET generation=1,updated_at=? WHERE session_key=?").run(
        "2026-09-12T00:00:00.000Z",
        sessionKey,
      );

      expect(() => confirmDelivery(db, key.idempotencyKey, { evidenceType: "stale-after-provider-switch" })).toThrow(
        /delivery owner generation is stale/i,
      );
      expect((db.prepare("SELECT status,delivery_state FROM cnx_assistant_delivery WHERE idempotency_key=?").get(key.idempotencyKey) as any)).toEqual({
        status: "pending",
        delivery_state: "transport_accepted",
      });
    } finally {
      db.close();
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("allows exact Discord delivery while rejecting ambiguous receipt identity", () => {
    const { root, db, sessionKey, ticket } = setup();
    try {
      const text = "discord matrix delivery";
      const payloadSha256 = createHash("sha256").update(text).digest("hex");
      const key = {
        ticketId: ticket.ticketId,
        inferenceAttemptId: "matrix-attempt-b",
        runId: "matrix-run-b",
        ownerSessionKey: sessionKey,
        ownerGeneration: 0,
        surface: "discord" as const,
        payloadSha256,
        idempotencyKey: `cnx-delivery:${ticket.ticketId}:discord-matrix`,
      };
      prepareDelivery(db, { ...key, text });
      stageDelivery(db, key.idempotencyKey, { evidenceType: "discord-final-staged" });
      acceptTransport(db, key.idempotencyKey, { evidenceType: "discord-send-accepted" });
      const confirmed = confirmDelivery(db, key.idempotencyKey, { evidenceType: "discord-receipt-confirmed", now: new Date("2026-09-12T00:00:00.000Z") });
      expect(confirmed.state).toBe("confirmed");
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "completed" });
    } finally {
      db.close();
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("rejects ambiguous Discord run identity before staging", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-discord-ambiguous-"));
    const databasePath = join(root, "tickets.sqlite3");
    const sessionKey = "agent:main:discord:channel:matrix095002";
    const store = new TicketStore(databasePath);
    sessionAuthority(databasePath, sessionKey);
    const first = store.accept({ runId: "matrix-ambiguous-run", ownerSessionKey: sessionKey, prompt: "first" });
    store.route(first.ticketId, false);

    const createdAt = "2026-09-12T00:00:00.000Z";
    const secondTicketId = "CNXT-ambiguous-matrix-second";
    const secondRequestKey = "matrix-ambiguous-request-key-2";
    const secondPrompt = "second";
    const secondPromptSha256 = createHash("sha256").update(secondPrompt).digest("hex");
    const db = new DatabaseSync(databasePath);
    db.prepare(`INSERT INTO tickets(
      ticket_id,request_key,run_id,owner_session_key,prompt,prompt_sha256,status,max_attempts,created_at,updated_at
    ) VALUES (?,?,?,?,?,?,'accepted',?,?,?)`).run(
      secondTicketId,
      secondRequestKey,
      "matrix-ambiguous-run",
      sessionKey,
      secondPrompt,
      secondPromptSha256,
      3,
      createdAt,
      createdAt,
    );
    db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,'accepted',?,?)")
      .run(secondTicketId, JSON.stringify({ runId: "matrix-ambiguous-run", promptSha256: secondPromptSha256 }), createdAt);
    db.close();
    store.route(secondTicketId, false);

    try {
      const result = stageDiscordDelivery(
        databasePath,
        { runId: "matrix-ambiguous-run", sessionKey, channel: "discord", messageProvider: "discord" },
        "ambiguous delivery",
      );
      expect(result).toEqual({ staged: false, reason: "ambiguous-run-ticket" });

      const check = new DatabaseSync(databasePath);
      try {
        expect(check.prepare("SELECT COUNT(*) AS count FROM cnx_assistant_delivery").get()).toEqual({ count: 0 });
      } finally {
        check.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
