import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

const OWNER = "agent:main:discord:channel:1531199905673252946";
const textOf = (message: any) => (Array.isArray(message?.content) ? message.content : [])
  .filter((part: any) => part?.type === "text" && typeof part.text === "string")
  .map((part: any) => part.text).join("\n");
const assistant = (text: string) => ({ role: "assistant", content: [{ type: "text", text }] });

type Hook = (event: any, ctx: any) => unknown;
function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v235-topology-"));
  const path = join(root, "tickets.sqlite3");
  sessionAuthority(path, OWNER);
  const hooks = new Map<string, Hook>();
  let transcriptUpdate: ((event: any) => void) | undefined;
  installV091DashboardVerifiedDelivery({
    on(name: string, handler: Hook) { hooks.set(name, handler); },
    runtime: { events: { onSessionTranscriptUpdate(handler: (event: any) => void) { transcriptUpdate = handler; return () => undefined; } } },
    logger: {},
  }, { workspaceDir: root, ticketDatabasePath: path });
  return { root, path, hooks, get transcriptUpdate() { return transcriptUpdate; } };
}

describe("Task 235 exact Dashboard-origin Discord-owner topology", () => {
  it("settles exactly once through native transcript authority without recovery regeneration", async () => {
    const s = setup();
    try {
      const store = new TicketStore(s.path);
      const runId = "task235-dashboard-settlement";
      const ticket = store.accept({ runId, ownerSessionKey: OWNER, prompt: "task235 dashboard" });
      store.route(ticket.ticketId, false);
      const finalize = s.hooks.get("before_agent_finalize")!;
      const write = s.hooks.get("before_message_write")!;
      const answer = assistant("TASK235-NATIVE-ANSWER");
      await finalize({ runId, sessionKey: OWNER, lastAssistantMessage: answer },
        { runId, sessionKey: OWNER, messageProvider: "webchat", channel: "webchat", channelId: "dashboard" });
      const result = await write({ message: answer },
        { runId, sessionKey: OWNER, messageProvider: "webchat", channel: "webchat", channelId: "dashboard" }) as any;
      const persisted = result?.message ?? answer;
      expect(textOf(persisted)).toContain("TASK235-NATIVE-ANSWER");
      expect(textOf(persisted)).toContain("<!-- cogentnexus-openclaw-delivery:");
      let db = new DatabaseSync(s.path, { readOnly: true });
      expect(db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'").get(ticket.ticketId)).toEqual({ n: 1 });
      expect(db.prepare("SELECT status FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "pending" });
      db.close();
      expect(store.recoverUndeliveredDirect({ now: new Date(Date.now() + 10 * 60_000), olderThanMs: 1000 })).toEqual([]);
      s.transcriptUpdate?.({ sessionKey: OWNER, sessionFile: join(s.root, "session.jsonl"), message: persisted, messageId: "task235-native-message", messageSeq: 7, agentId: "main" });
      await Promise.resolve();
      db = new DatabaseSync(s.path, { readOnly: true });
      expect(db.prepare("SELECT status FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "delivered" });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toMatchObject({ status: "completed" });
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='delivery_confirmed'").get(ticket.ticketId)).toEqual({ n: 1 });
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='direct_redelivery_timeout'").get(ticket.ticketId)).toEqual({ n: 0 });
      db.close();
      s.transcriptUpdate?.({ sessionKey: OWNER, sessionFile: join(s.root, "session.jsonl"), message: persisted, messageId: "task235-native-message-duplicate", messageSeq: 8, agentId: "main" });
      await Promise.resolve();
      db = new DatabaseSync(s.path, { readOnly: true });
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='delivery_confirmed'").get(ticket.ticketId)).toEqual({ n: 1 });
      db.close();
    } finally { try { rmSync(s.root, { recursive: true, force: true, maxRetries: 5, retryDelay: 20 }); } catch {} }
  });

  it("keeps true Discord origin and contradictory recognized context out of Dashboard staging", async () => {
    for (const [provider, channel] of [["discord", "discord"], ["discord", "webchat"]]) {
      const s = setup();
      try {
        const store = new TicketStore(s.path); const runId = `task235-negative-${provider}-${channel}`;
        const ticket = store.accept({ runId, ownerSessionKey: OWNER, prompt: "task235 negative" }); store.route(ticket.ticketId, false);
        const finalize = s.hooks.get("before_agent_finalize")!; const write = s.hooks.get("before_message_write")!; const answer = assistant("TASK235-NO-DASHBOARD");
        await finalize({ runId, sessionKey: OWNER, lastAssistantMessage: answer }, { runId, sessionKey: OWNER, messageProvider: provider, channel, channelId: "1531199905673252946" });
        const result = await write({ message: answer }, { runId, sessionKey: OWNER, messageProvider: provider, channel, channelId: "1531199905673252946" }) as any;
        expect(textOf(result?.message ?? answer)).not.toContain("cogentnexus-openclaw-delivery:");
        const db = new DatabaseSync(s.path, { readOnly: true });
        const schema = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='cnx_assistant_delivery'").get() as any;
        expect(schema ? db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId) : { n: 0 }).toEqual({ n: 0 }); db.close();
      } finally { try { rmSync(s.root, { recursive: true, force: true, maxRetries: 5, retryDelay: 20 }); } catch {} }
    }
  });
});
