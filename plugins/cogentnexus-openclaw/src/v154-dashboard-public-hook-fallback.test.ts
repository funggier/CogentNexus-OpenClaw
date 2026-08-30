import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

describe("Task 154 Dashboard public-hook durable capture fallback", () => {
  it("captures exactly once through reply_payload_sending when reply_dispatch lacks appendBeforeDeliver", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v154-dashboard-public-hook-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const runId = "dashboard-v154-public-hook-run";
      const sessionKey = "agent:main:dashboard:v154";
      const text = "CNX-V154-ACK";

      expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
      const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "v154 prompt" });
      store.route(ticket.ticketId, false);

      let replyDispatch: ((event: any, ctx: any) => unknown) | undefined;
      let replyPayloadSending: ((event: any, ctx: any) => unknown) | undefined;
      installV091DashboardVerifiedDelivery(
        {
          on: (name: string, handler: (event: any, ctx: any) => unknown) => {
            if (name === "reply_dispatch") replyDispatch = handler;
            if (name === "reply_payload_sending") replyPayloadSending = handler;
          },
          logger: {},
        },
        { workspaceDir: root, ticketDatabasePath: path },
      );

      expect(replyDispatch).toBeTypeOf("function");

      let releaseIdle: (() => void) | undefined;
      const idle = new Promise<void>((resolve) => { releaseIdle = resolve; });

      // Match the exact OpenClaw v2026.7.1-2 production hook shape: reply_dispatch
      // receives an abort-aware wrapper that deliberately does not forward the
      // underlying dispatcher's optional appendBeforeDeliver capability.
      const productionHookDispatcher = {
        sendToolResult: () => true,
        sendBlockReply: () => true,
        sendFinalReply: () => true,
        waitForIdle: () => idle,
        getQueuedCounts: () => ({ tool: 0, block: 0, final: 1 }),
        getFailedCounts: () => ({ tool: 0, block: 0, final: 0 }),
        getCancelledCounts: () => ({ tool: 0, block: 0, final: 0 }),
        markComplete: () => undefined,
      };
      replyDispatch?.({ runId }, { dispatcher: productionHookDispatcher });

      // OpenClaw installs reply_payload_sending on the original dispatcher through
      // its own before-delivery chain. CogentNexus-OpenClaw must use that public hook as the
      // durable-capture fallback instead of requiring appendBeforeDeliver here.
      expect(replyPayloadSending).toBeTypeOf("function");
      const result = await replyPayloadSending?.(
        { runId, sessionKey, kind: "final", payload: { text } },
        { channelId: "webchat", sessionKey, runId },
      ) as any;

      expect(result?.payload?.text).toContain(text);
      expect(result?.payload?.text).toContain("<!-- cogentnexus-openclaw-delivery:");

      let db = new DatabaseSync(path, { readOnly: true });
      try {
        expect(db.prepare(`SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`)
          .get(ticket.ticketId)).toEqual({ n: 1 });
        expect(db.prepare(`SELECT text,status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`)
          .get(ticket.ticketId)).toEqual({ text, status: "pending" });
      } finally {
        db.close();
      }

      // A duplicate observation of the same final must not stage a second durable row.
      const duplicate = await replyPayloadSending?.(
        { runId, sessionKey, kind: "final", payload: { text } },
        { channelId: "webchat", sessionKey, runId },
      );
      expect(duplicate).toBeUndefined();
      db = new DatabaseSync(path, { readOnly: true });
      try {
        expect(db.prepare(`SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`)
          .get(ticket.ticketId)).toEqual({ n: 1 });
      } finally {
        db.close();
      }

      // Release the deterministic native-delivery waiter and wait one event-loop turn so
      // settlement completes before the temporary database is removed.
      releaseIdle?.();
      await new Promise<void>((resolve) => setImmediate(resolve));

      db = new DatabaseSync(path, { readOnly: true });
      try {
        expect(db.prepare(`SELECT status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'`)
          .get(ticket.ticketId)).toEqual({ status: "delivered" });
        expect(db.prepare(`SELECT status FROM tickets WHERE ticket_id=?`).get(ticket.ticketId))
          .toEqual({ status: "completed" });
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
