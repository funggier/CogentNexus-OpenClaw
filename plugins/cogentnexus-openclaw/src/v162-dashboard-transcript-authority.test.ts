import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

function assistantMessage(text: string) {
  return { role: "assistant", content: [{ type: "text", text }] };
}

function messageText(message: any): string {
  const content = Array.isArray(message?.content) ? message.content : [];
  return content
    .filter((part: any) => part?.type === "text" && typeof part?.text === "string")
    .map((part: any) => part.text)
    .join("\n");
}

describe("Task 162 Dashboard native transcript authority", () => {
  it("settles only after the marker-bearing native append and fences Host recovery while native write owns delivery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v162-transcript-authority-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const runId = "dashboard-v162-native-run";
      const sessionKey = "agent:main:dashboard:v162-native";
      const text = "CNX-V162-NATIVE-ACK";

      expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
      const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "v162 prompt" });
      store.route(ticket.ticketId, false);

      const hooks = new Map<string, (event: any, ctx: any) => unknown>();
      let transcriptUpdate: ((event: any) => void) | undefined;
      installV091DashboardVerifiedDelivery(
        {
          on(name: string, handler: (event: any, ctx: any) => unknown) {
            hooks.set(name, handler);
          },
          runtime: {
            events: {
              onSessionTranscriptUpdate(handler: (event: any) => void) {
                transcriptUpdate = handler;
                return () => undefined;
              },
            },
          },
          logger: {},
        },
        { workspaceDir: root, ticketDatabasePath: path },
      );

      const replyDispatch = hooks.get("reply_dispatch");
      const beforeAgentFinalize = hooks.get("before_agent_finalize");
      const beforeMessageWrite = hooks.get("before_message_write");
      expect(replyDispatch).toBeTypeOf("function");
      expect(beforeAgentFinalize).toBeTypeOf("function");
      expect(beforeMessageWrite).toBeTypeOf("function");
      expect(transcriptUpdate).toBeTypeOf("function");

      // Exact v2026.7.1-2 production fact: pre-model reply_dispatch sees the
      // abort-aware wrapper and therefore has no appendBeforeDeliver capability.
      const abortAwareDispatcher = {
        sendToolResult: () => true,
        sendBlockReply: () => true,
        sendFinalReply: () => true,
        waitForIdle: async () => undefined,
        getQueuedCounts: () => ({ tool: 0, block: 0, final: 1 }),
        getFailedCounts: () => ({ tool: 0, block: 0, final: 0 }),
        getCancelledCounts: () => ({ tool: 0, block: 0, final: 0 }),
        markComplete: () => undefined,
      };
      replyDispatch?.({ runId }, { runId, sessionKey, dispatcher: abortAwareDispatcher });
      expect("appendBeforeDeliver" in abortAwareDispatcher).toBe(false);

      // The real post-model hook carries the resolved terminal assistant candidate.
      await beforeAgentFinalize?.(
        {
          runId,
          sessionId: "session-v162-native",
          sessionKey,
          lastAssistantMessage: assistantMessage(text),
          messages: [assistantMessage(text)],
        },
        { runId, sessionKey },
      );

      // OpenClaw calls before_message_write before SessionManager.originalAppend.
      const writeResult = await beforeMessageWrite?.(
        { message: assistantMessage(text) },
        { runId, sessionKey },
      ) as any;
      const persistedMessage = writeResult?.message ?? assistantMessage(text);
      const persistedText = messageText(persistedMessage);
      expect(persistedText).toContain(text);
      expect(persistedText).toContain("<!-- cogentnexus-openclaw-delivery:");

      // Native ownership must be durable before originalAppend. host_delivery.py
      // may claim only pending rows whose claim is absent/expired; this query mirrors
      // that authority predicate and must find nothing while native append is active.
      let db = new DatabaseSync(path, { readOnly: true });
      let row = db.prepare(`SELECT status,claim_token,claim_expires_at,idempotency_key
        FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`).get(ticket.ticketId) as any;
      expect(row?.status).toBe("pending");
      expect(typeof row?.claim_token).toBe("string");
      expect(String(row?.claim_token ?? "").length).toBeGreaterThan(0);
      expect(typeof row?.claim_expires_at).toBe("string");
      expect(Date.parse(String(row.claim_expires_at))).toBeGreaterThan(Date.now());
      expect(db.prepare(`SELECT count(*) AS n FROM cnx_assistant_delivery
        WHERE ticket_id=? AND status='pending'
          AND (claim_token IS NULL OR claim_expires_at IS NULL OR claim_expires_at<=?)`)
        .get(ticket.ticketId, new Date().toISOString())).toEqual({ n: 0 });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId)).toEqual({ status: "accepted", delivery_confirmed_at: null });
      db.close();

      // Existing no-regeneration fence remains authoritative while the exact durable
      // result is pending; the model result is not generated a second time.
      expect(store.recoverUndeliveredDirect({
        now: new Date(Date.now() + 10 * 60_000),
        olderThanMs: 1000,
      })).toEqual([]);

      // Simulate only OpenClaw's already-proven ordering boundary: originalAppend has
      // completed, then runtime.events.onSessionTranscriptUpdate emits the exact row.
      transcriptUpdate?.({
        sessionKey,
        sessionFile: join(root, "session-v162-native.jsonl"),
        message: persistedMessage,
        messageId: "native-message-v162",
        messageSeq: 42,
        agentId: "main",
      });
      await Promise.resolve();

      db = new DatabaseSync(path, { readOnly: true });
      row = db.prepare(`SELECT status,claim_token,claim_expires_at
        FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`).get(ticket.ticketId) as any;
      expect(row).toEqual({ status: "delivered", claim_token: null, claim_expires_at: null });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId)).toMatchObject({ status: "completed" });
      expect((db.prepare("SELECT delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId) as any).delivery_confirmed_at).not.toBeNull();

      // Native persistence is terminal authority: Host recovery has no pending row
      // left to claim, so native-send cannot be followed by recovery chat.inject.
      expect(db.prepare(`SELECT count(*) AS n FROM cnx_assistant_delivery
        WHERE ticket_id=? AND status='pending'
          AND (claim_token IS NULL OR claim_expires_at IS NULL OR claim_expires_at<=?)`)
        .get(ticket.ticketId, new Date(Date.now() + 60 * 60_000).toISOString())).toEqual({ n: 0 });
      expect(db.prepare(`SELECT count(*) AS n FROM ticket_events
        WHERE ticket_id=? AND event_type='delivery_confirmed'`).get(ticket.ticketId)).toEqual({ n: 1 });
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
