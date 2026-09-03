import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx-task234-ingress-"));
  const path = join(root, "tickets.sqlite3");
  const sessionKey = "agent:main:discord:channel:1531199905673252946";
  const store = new TicketStore(path);
  return { root, path, sessionKey, store };
}

function hooks(path: string) {
  let finalize: any;
  let write: any;
  const api = {
    on(name: string, handler: any) {
      if (name === "before_agent_finalize") finalize = handler;
      if (name === "before_message_write") write = handler;
    },
    logger: {},
  };
  installV091DashboardVerifiedDelivery(api, { workspaceDir: path, ticketDatabasePath: path });
  return { finalize, write };
}

describe("Task 234 trusted ingress-surface durable staging", () => {
  it("stages a Dashboard-origin final on a Discord-associated owner", () => {
    const { root, path, sessionKey, store } = setup();
    try {
      const ticket = store.accept({
        runId: "task234-dashboard-run",
        ownerSessionKey: sessionKey,
        prompt: "Dashboard-origin request",
      });
      store.route(ticket.ticketId, false);
      const { finalize, write } = hooks(path);
      const message = { role: "assistant", content: [{ type: "text", text: "Dashboard answer" }] };

      finalize(
        { runId: ticket.runId, sessionKey, lastAssistantMessage: message },
        { runId: ticket.runId, sessionKey, messageProvider: "webchat", channel: "webchat", channelId: "dashboard" },
      );
      const result = write(
        { message },
        { runId: ticket.runId, sessionKey, messageProvider: "webchat", channel: "webchat", channelId: "dashboard" },
      );

      expect(result).toBeDefined();
      expect(result?.message?.content?.[0]?.text).toContain("cogentnexus-openclaw-delivery:");
      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT kind,status,text FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId))
        .toMatchObject({ kind: "direct_result", status: "pending", text: "Dashboard answer" });
      db.close();
    } finally {
      try { rmSync(root, { recursive: true, force: true }); } catch {}
    }
  });

  it("does not let a real Discord-origin final claim Dashboard staging on the same owner", () => {
    const { root, path, sessionKey, store } = setup();
    try {
      const ticket = store.accept({
        runId: "task234-discord-run",
        ownerSessionKey: sessionKey,
        prompt: "Discord-origin request",
      });
      store.route(ticket.ticketId, false);
      const { finalize, write } = hooks(path);
      const message = { role: "assistant", content: [{ type: "text", text: "Discord answer" }] };

      finalize(
        { runId: ticket.runId, sessionKey, lastAssistantMessage: message },
        { runId: ticket.runId, sessionKey, messageProvider: "discord", channel: "discord", channelId: "1531199905673252946" },
      );
      const result = write(
        { message },
        { runId: ticket.runId, sessionKey, messageProvider: "discord", channel: "discord", channelId: "1531199905673252946" },
      );

      expect(result).toBeUndefined();
      const db = new DatabaseSync(path, { readOnly: true });
      const schema = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='cnx_assistant_delivery'").get() as { name?: string } | undefined;
      const deliveries = schema?.name
        ? db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)
        : { n: 0 };
      expect(deliveries).toEqual({ n: 0 });
      db.close();
    } finally {
      try { rmSync(root, { recursive: true, force: true }); } catch {}
    }
  });
});
