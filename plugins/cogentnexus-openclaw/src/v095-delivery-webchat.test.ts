import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";
import { sessionAuthority } from "./v090.js";
import {
  confirmWebchatDelivery,
  registerWebchatDeliveryAdapter,
  stageWebchatDelivery,
} from "./v095-delivery-webchat.js";

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v095-webchat-adapter-"));
  const databasePath = join(root, "tickets.sqlite3");
  const sessionKey = "agent:main:webchat:channel:v095902";
  const store = new TicketStore(databasePath);
  sessionAuthority(databasePath, sessionKey);
  const ticketA = store.accept({ runId: "webchat-adapter-a", ownerSessionKey: sessionKey, prompt: "A" });
  const ticketB = store.accept({ runId: "webchat-adapter-b", ownerSessionKey: sessionKey, prompt: "B" });
  store.route(ticketA.ticketId, false);
  store.route(ticketB.ticketId, false);
  const db = new DatabaseSync(databasePath);
  const attemptA = beginInferenceAttempt(db, {
    ticketId: ticketA.ticketId,
    sessionKey,
    sessionGeneration: 0,
    callId: "call-a",
    provider: "openai",
    model: "m1",
  });
  bindRunId(db, attemptA.attemptId, "webchat-adapter-a");
  finishInferenceAttempt(db, attemptA.attemptId, "completed");
  const attemptB = beginInferenceAttempt(db, {
    ticketId: ticketB.ticketId,
    sessionKey,
    sessionGeneration: 0,
    callId: "call-b",
    provider: "ollama",
    model: "m2",
  });
  bindRunId(db, attemptB.attemptId, "webchat-adapter-b");
  finishInferenceAttempt(db, attemptB.attemptId, "completed");
  db.close();
  return { root, databasePath, sessionKey };
}

describe("v0.9.5 Web Chat delivery adapter", () => {
  it("stages the exact run and does not cross-settle concurrent Web Chat runs", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const a = stageWebchatDelivery(databasePath, {
        runId: "webchat-adapter-a",
        sessionKey,
        channel: "webchat",
      }, "reply A");
      const b = stageWebchatDelivery(databasePath, {
        runId: "webchat-adapter-b",
        sessionKey,
        channel: "webchat",
      }, "reply B");
      expect(a.staged).toBe(true);
      expect(b.staged).toBe(true);
      if (!a.staged || !b.staged) throw new Error("expected both deliveries to stage");
      expect(a.ticketId).not.toBe(b.ticketId);
      expect(a.idempotencyKey).not.toBe(b.idempotencyKey);

      expect(confirmWebchatDelivery(databasePath, {
        runId: "webchat-adapter-a",
        sessionKey,
        channel: "webchat",
      }).confirmed).toBe(true);

      const db = new DatabaseSync(databasePath, { readOnly: true });
      try {
        expect(db.prepare("SELECT run_id,status FROM tickets WHERE run_id IN (?,?) ORDER BY run_id")
          .all("webchat-adapter-a", "webchat-adapter-b"))
          .toEqual([
            { run_id: "webchat-adapter-a", status: "completed" },
            { run_id: "webchat-adapter-b", status: "accepted" },
          ]);
      } finally { db.close(); }
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("rejects stale owner generation rather than staging new Web Chat delivery", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const first = stageWebchatDelivery(databasePath, {
        runId: "webchat-adapter-a",
        sessionKey,
        channel: "webchat",
      }, "reply A");
      expect(first.staged).toBe(true);
      const db = new DatabaseSync(databasePath);
      try {
        db.prepare("UPDATE cnx_sessions SET generation=1 WHERE session_key=?").run(sessionKey);
      } finally { db.close(); }
      const second = stageWebchatDelivery(databasePath, {
        runId: "webchat-adapter-b",
        sessionKey,
        channel: "webchat",
      }, "reply B");
      expect(second).toEqual({ staged: false, reason: "stale-webchat-generation" });
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("registers only exact Web Chat evidence and ignores another surface", () => {
    const { root, databasePath, sessionKey } = setup();
    try {
      const handlers = new Map<string, any>();
      registerWebchatDeliveryAdapter({
        pluginConfig: { ticketDatabasePath: databasePath, workspaceDir: root },
        on: (name: string, handler: any) => handlers.set(name, handler),
      });
      expect(handlers.has("reply_payload_sending")).toBe(true);
      const ignored = handlers.get("reply_payload_sending")?.(
        { runId: "webchat-adapter-a", payload: { text: "ignored" } },
        { runId: "webchat-adapter-a", sessionKey, channel: "discord", workspaceDir: root },
      );
      expect(ignored).toBeUndefined();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
