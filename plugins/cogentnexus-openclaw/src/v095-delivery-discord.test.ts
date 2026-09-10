import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";
import { confirmDiscordDelivery, registerDiscordDeliveryAdapter, stageDiscordDelivery } from "./v095-delivery-discord.js";

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v095-discord-adapter-"));
  const databasePath = join(root, "tickets.sqlite3");
  const sessionKey = "agent:main:discord:channel:095902";
  const store = new TicketStore(databasePath);
  sessionAuthority(databasePath, sessionKey);
  const ticketA = store.accept({ runId: "discord-adapter-a", ownerSessionKey: sessionKey, prompt: "A" });
  const ticketB = store.accept({ runId: "discord-adapter-b", ownerSessionKey: sessionKey, prompt: "B" });
  store.route(ticketA.ticketId, false);
  store.route(ticketB.ticketId, false);
  const db = new DatabaseSync(databasePath);
  const attemptA = beginInferenceAttempt(db, { ticketId: ticketA.ticketId, sessionKey, sessionGeneration: 0, provider: "openai", model: "m1" });
  bindRunId(db, attemptA.attemptId, "discord-adapter-a");
  finishInferenceAttempt(db, attemptA.attemptId, "completed");
  const attemptB = beginInferenceAttempt(db, { ticketId: ticketB.ticketId, sessionKey, sessionGeneration: 0, provider: "ollama", model: "m2" });
  bindRunId(db, attemptB.attemptId, "discord-adapter-b");
  finishInferenceAttempt(db, attemptB.attemptId, "completed");
  db.close();
  return { root, databasePath, sessionKey };
}

describe("v0.9.5 Discord delivery adapter", () => {
  it("stages the exact run and does not cross-settle concurrent Discord runs", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const a = stageDiscordDelivery(databasePath, { runId: "discord-adapter-a", sessionKey, channel: "discord" }, "reply A");
      const b = stageDiscordDelivery(databasePath, { runId: "discord-adapter-b", sessionKey, channel: "discord" }, "reply B");
      expect(a.staged).toBe(true);
      expect(b.staged).toBe(true);
      expect(a.ticketId).not.toBe(b.ticketId);
      expect(a.idempotencyKey).not.toBe(b.idempotencyKey);

      expect(confirmDiscordDelivery(databasePath, { runId: "discord-adapter-a", sessionKey, channel: "discord" }).confirmed).toBe(true);
      const db = new DatabaseSync(databasePath, { readOnly: true });
      try {
        expect(db.prepare("SELECT run_id,status FROM tickets WHERE run_id IN (?,?) ORDER BY run_id").all("discord-adapter-a", "discord-adapter-b")).toEqual([
          { run_id: "discord-adapter-a", status: "completed" },
          { run_id: "discord-adapter-b", status: "accepted" },
        ]);
      } finally { db.close(); }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("ignores a message_sent receipt without event runId even when ctx has a runId", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      stageDiscordDelivery(databasePath, { runId: "discord-adapter-a", sessionKey, channel: "discord" }, "reply A");
      const handlers = new Map<string, any>();
      const logs: string[] = [];
      registerDiscordDeliveryAdapter({
        pluginConfig: { ticketDatabasePath: databasePath, workspaceDir: root },
        on: (name: string, handler: any) => handlers.set(name, handler),
        logger: { info: (message: string) => logs.push(message) },
      });
      handlers.get("message_sent")?.({ sessionKey, success: true }, { runId: "discord-adapter-a", sessionKey, channel: "discord", workspaceDir: root });
      expect(logs.some((line) => line.includes("ignored ambiguous Discord message_sent receipt"))).toBe(true);
      const db = new DatabaseSync(databasePath, { readOnly: true });
      try {
        expect(db.prepare("SELECT status FROM tickets WHERE run_id=?").get("discord-adapter-a")).toEqual({ status: "accepted" });
      } finally { db.close(); }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("returns the same native marker for duplicate staging", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const first = stageDiscordDelivery(databasePath, { runId: "discord-adapter-b", sessionKey, channel: "discord" }, "same reply");
      const second = stageDiscordDelivery(databasePath, { runId: "discord-adapter-b", sessionKey, channel: "discord" }, "same reply");
      expect(first.staged && second.staged).toBe(true);
      expect(first.idempotencyKey).toBe(second.idempotencyKey);
      expect(first.nativeText).toBe(second.nativeText);
      expect(first.nativeText).toContain("<!-- cogentnexus-openclaw-delivery:");
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
