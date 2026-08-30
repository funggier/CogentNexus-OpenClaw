import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

function assistantMessage(text: string) {
  return { role: "assistant", content: [{ type: "text", text }], stopReason: "stop" };
}

function messageText(message: any): string {
  const content = Array.isArray(message?.content) ? message.content : [];
  return content
    .filter((part: any) => part?.type === "text" && typeof part?.text === "string")
    .map((part: any) => part.text)
    .join("\n");
}

describe("Task 167 native delivery staging order", () => {
  it("stages and marks the assistant write before the post-write finalize gate", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v167-native-order-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const runId = "dashboard-v167-native-order-run";
      const sessionKey = "agent:main:dashboard:v167-native-order";
      const text = "CNX-V167-NATIVE-ORDER-ACK";
      const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "v167 prompt" });
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

      const beforeAgentFinalize = hooks.get("before_agent_finalize");
      const beforeMessageWrite = hooks.get("before_message_write");
      expect(beforeAgentFinalize).toBeTypeOf("function");
      expect(beforeMessageWrite).toBeTypeOf("function");
      expect(transcriptUpdate).toBeTypeOf("function");

      // Pinned OpenClaw ordering: the native SessionManager write invokes
      // before_message_write first, appends the message, then emits the public
      // transcript update. The terminal before_agent_finalize gate runs later.
      const originalMessage = assistantMessage(text);
      const writeResult = beforeMessageWrite?.(
        { message: originalMessage },
        { agentId: "main", sessionKey },
      ) as any;
      const persistedMessage = writeResult?.message ?? originalMessage;
      expect(messageText(persistedMessage)).toContain("<!-- cogentnexus-openclaw-delivery:");

      transcriptUpdate?.({
        sessionFile: join(root, "session-v167-native-order.jsonl"),
        sessionKey,
        message: persistedMessage,
        messageId: "native-message-v167",
        messageSeq: 1,
        agentId: "main",
        sessionId: "session-v167-native-order",
      });

      const db = new DatabaseSync(path, { readOnly: true });
      const staged = db.prepare(`SELECT status,text,idempotency_key,claim_token
        FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`).get(ticket.ticketId) as any;
      expect(staged).toMatchObject({ status: "delivered", text });
      expect(typeof staged?.idempotency_key).toBe("string");
      expect(staged?.claim_token).toBeNull();
      const settled = db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId) as any;
      expect(settled).toMatchObject({ status: "completed" });
      expect(typeof settled?.delivery_confirmed_at).toBe("string");
      db.close();

      // This is the actual terminal hook shape from OpenClaw: the final text is
      // projected to a string and the hook executes after the native write.
      await beforeAgentFinalize?.(
        {
          runId,
          sessionId: "session-v167-native-order",
          sessionKey,
          lastAssistantMessage: text,
          messages: [originalMessage],
        },
        { runId, sessionKey, sessionId: "session-v167-native-order", agentId: "main" },
      );
    } finally {
      try {
        rmSync(root, { recursive: true, force: true, maxRetries: 5, retryDelay: 20 });
      } catch {
        // Windows may release SQLite handles after the assertion completes.
      }
    }
  });
});
