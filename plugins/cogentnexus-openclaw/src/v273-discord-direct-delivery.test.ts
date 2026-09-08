import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

describe("Task273 Discord Direct durable delivery boundary", () => {
  it("stages the ctx.runId Discord final before native transport without message_sent.runId", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task273-discord-direct-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:273001";
      const runId = "task273-discord-run";
      const text = "CNX-T273-DISCORD-ACK";
      const store = new TicketStore(path);
      expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
      const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "Task273 Discord prompt" });
      store.route(ticket.ticketId, false);

      let replyDispatch: ((event: any, ctx: any) => unknown) | undefined;
      let replyPayloadSending: ((event: any, ctx: any) => unknown) | undefined;
      const logs: string[] = [];
      installV091DashboardVerifiedDelivery(
        {
          on: (name: string, handler: (event: any, ctx: any) => unknown) => {
            if (name === "reply_dispatch") replyDispatch = handler;
            if (name === "reply_payload_sending") replyPayloadSending = handler;
          },
          logger: { info: (message: string) => logs.push(message) },
        },
        { workspaceDir: root, ticketDatabasePath: path },
      );
      expect(replyDispatch).toBeTypeOf("function");
      expect(replyPayloadSending).toBeTypeOf("function");

      let releaseIdle: (() => void) | undefined;
      let waitForIdleCalls = 0;
      const idle = new Promise<void>((resolve) => { releaseIdle = resolve; });
      const dispatcher = {
        sendToolResult: () => true,
        sendBlockReply: () => true,
        sendFinalReply: () => true,
        waitForIdle: () => { waitForIdleCalls += 1; return idle; },
        getQueuedCounts: () => ({ tool: 0, block: 0, final: 1 }),
        getFailedCounts: () => ({ tool: 0, block: 0, final: 0 }),
        getCancelledCounts: () => ({ tool: 0, block: 0, final: 0 }),
        markComplete: () => undefined,
      };

      // Installed OpenClaw shape: runId is on ctx, not reply_dispatch event,
      // and the abort-aware dispatcher lacks appendBeforeDeliver.
      replyDispatch?.({ }, { runId, sessionKey, channel: "discord", messageProvider: "discord", dispatcher });
      expect(logs.some((line) => line.includes("public-hook-fallback-armed"))).toBe(true);
      const result = await replyPayloadSending?.(
        { kind: "final", payload: { text } },
        { runId, sessionKey, channel: "discord", messageProvider: "discord" },
      ) as any;
      const firstNativeText = result?.payload?.text;
      expect(firstNativeText).toContain(text);
      expect(firstNativeText).toContain("<!-- cogentnexus-openclaw-delivery:");
      await Promise.resolve();
      expect(waitForIdleCalls).toBe(1);

      const duplicate = await replyPayloadSending?.(
        { kind: "final", payload: { text } },
        { runId, sessionKey, channel: "discord", messageProvider: "discord" },
      ) as any;
      expect(duplicate?.payload?.text).toBe(firstNativeText);
      expect(waitForIdleCalls).toBe(1);
      expect(() => replyPayloadSending?.(
        { kind: "final", payload: { text: `${text}-CHANGED` } },
        { runId, sessionKey, channel: "discord", messageProvider: "discord" },
      )).toThrow(/durable Dashboard result changed/);

      const db = new DatabaseSync(path, { readOnly: true });
      try {
        expect(db.prepare("SELECT ticket_id,owner_session_key,owner_generation,text,status FROM cnx_assistant_delivery WHERE ticket_id=?")
          .get(ticket.ticketId)).toMatchObject({
            ticket_id: ticket.ticketId,
            owner_session_key: sessionKey,
            owner_generation: 0,
            text,
            status: "pending",
          });
      } finally { db.close(); }

      releaseIdle?.();
      await new Promise<void>((resolve) => setImmediate(resolve));
      const settled = new DatabaseSync(path, { readOnly: true });
      try {
        expect(settled.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "completed" });
        expect(settled.prepare("SELECT status FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "delivered" });
      } finally { settled.close(); }
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
