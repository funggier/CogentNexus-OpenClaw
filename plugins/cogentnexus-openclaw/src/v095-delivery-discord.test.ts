import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";
import { sessionAuthority } from "./v090.js";
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
  const attemptA = beginInferenceAttempt(db, { ticketId: ticketA.ticketId, sessionKey, sessionGeneration: 0, callId: "call-a", provider: "openai", model: "m1" });
  bindRunId(db, attemptA.attemptId, "discord-adapter-a");
  finishInferenceAttempt(db, attemptA.attemptId, "completed");
  const attemptB = beginInferenceAttempt(db, { ticketId: ticketB.ticketId, sessionKey, sessionGeneration: 0, callId: "call-b", provider: "ollama", model: "m2" });
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
      if (!a.staged || !b.staged) throw new Error(`expected staged deliveries: ${a.staged ? "a" : a.reason}/${b.staged ? "b" : b.reason}`);
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

  it("rejects ambiguous Ticket ownership instead of selecting a latest matching Ticket", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-discord-ambiguous-ticket-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:ambiguous-ticket";
      const store = new TicketStore(databasePath);
      sessionAuthority(databasePath, sessionKey);
      const first = store.accept({ runId: "same-run", ownerSessionKey: sessionKey, prompt: "first" });
      store.route(first.ticketId, false);
      const db = new DatabaseSync(databasePath);
      try {
        const now = new Date().toISOString();
        const secondTicketId = "CNXT-duplicate-same-run";
        const secondPrompt = "second";
        const secondRequestKey = createHash("sha256").update(`${sessionKey}\0same-run\0duplicate`).digest("hex");
        const secondPromptHash = createHash("sha256").update(secondPrompt, "utf8").digest("hex");
        db.prepare(`INSERT INTO tickets(ticket_id,request_key,run_id,owner_session_key,prompt,prompt_sha256,status,max_attempts,created_at,updated_at)
                    VALUES (?,?,?,?,?,?,'accepted',?,?,?)`)
          .run(secondTicketId, secondRequestKey, "same-run", sessionKey, secondPrompt, secondPromptHash, 3, now, now);
        store.route(secondTicketId, false);
        const attemptA = beginInferenceAttempt(db, { ticketId: first.ticketId, sessionKey, sessionGeneration: 0, callId: "same-run-call-a" });
        bindRunId(db, attemptA.attemptId, "same-run");
        finishInferenceAttempt(db, attemptA.attemptId, "completed");
        const attemptB = beginInferenceAttempt(db, { ticketId: secondTicketId, sessionKey, sessionGeneration: 0, callId: "same-run-call-b" });
        bindRunId(db, attemptB.attemptId, "same-run");
        finishInferenceAttempt(db, attemptB.attemptId, "completed");
      } finally {
        db.close();
      }
      const staged = stageDiscordDelivery(databasePath, { runId: "same-run", sessionKey, channel: "discord" }, "must not guess");
      expect(staged).toEqual({ staged: false, reason: "ambiguous-run-ticket" });
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("ignores a message_sent receipt without event runId even when ctx has a runId", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const staged = stageDiscordDelivery(databasePath, { runId: "discord-adapter-a", sessionKey, channel: "discord" }, "reply A");
      if (!staged.staged) throw new Error(staged.reason);
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
      if (!first.staged || !second.staged) throw new Error(`expected duplicate staging: ${first.staged ? "first" : first.reason}/${second.staged ? "second" : second.reason}`);
      expect(first.idempotencyKey).toBe(second.idempotencyKey);
      expect(first.nativeText).toBe(second.nativeText);
      expect(first.nativeText).toContain("<!-- cogentnexus-openclaw-delivery:");
      expect(createHash("sha256").update("same reply").digest("hex")).toBeTruthy();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});