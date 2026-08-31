import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import {
  installV091DashboardVerifiedDelivery,
  stageDashboardDirectResult,
} from "./v091-dashboard-verified-delivery.js";

describe("Task 191 direct Dashboard NO_REPLY boundary", () => {
  it("does not stage a bare OpenClaw silent sentinel as a durable visible Dashboard result", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v191-silent-stage-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:v191-silent-stage";
      sessionAuthority(path, sessionKey);

      const upper = store.accept({
        runId: "v191-no-reply-upper",
        ownerSessionKey: sessionKey,
        prompt: "ตอบกลับข้อความนี้เพียงว่า CNX191-UPPER",
      });
      store.route(upper.ticketId, false);
      expect(stageDashboardDirectResult(path, {
        runId: "v191-no-reply-upper",
        text: "NO_REPLY",
      })).toMatchObject({ staged: false, reason: "silent-reply" });

      const lower = store.accept({
        runId: "v191-no-reply-lower",
        ownerSessionKey: sessionKey,
        prompt: "ตอบกลับข้อความนี้เพียงว่า CNX191-LOWER",
      });
      store.route(lower.ticketId, false);
      expect(stageDashboardDirectResult(path, {
        runId: "v191-no-reply-lower",
        text: "  no_reply  ",
      })).toMatchObject({ staged: false, reason: "silent-reply" });

      const mixed = store.accept({
        runId: "v191-no-reply-mixed",
        ownerSessionKey: sessionKey,
        prompt: "Explain the sentinel",
      });
      store.route(mixed.ticketId, false);
      expect(stageDashboardDirectResult(path, {
        runId: "v191-no-reply-mixed",
        text: "Actual answer: NO_REPLY is a sentinel",
      })).toMatchObject({ staged: true });

      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id IN (?,?)")
        .get(upper.ticketId, lower.ticketId)).toEqual({ n: 0 });
      expect(db.prepare("SELECT text FROM cnx_assistant_delivery WHERE ticket_id=?")
        .get(mixed.ticketId)).toEqual({ text: "Actual answer: NO_REPLY is a sentinel" });
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("requests one bounded same-run revision when a genuine direct Dashboard final is bare NO_REPLY", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v191-silent-revise-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:v191-silent-revise";
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({
        runId: "v191-revise-run",
        ownerSessionKey: sessionKey,
        prompt: "ตอบกลับข้อความนี้เพียงว่า CNX191-REVISION",
      });
      store.route(ticket.ticketId, false);

      let beforeAgentFinalize: ((event: any, ctx: any) => Promise<any> | any) | undefined;
      installV091DashboardVerifiedDelivery({
        on: (name: string, handler: any) => {
          if (name === "before_agent_finalize") beforeAgentFinalize = handler;
        },
        logger: {},
      }, { workspaceDir: root, ticketDatabasePath: path });

      expect(beforeAgentFinalize).toBeTypeOf("function");
      const decision = await beforeAgentFinalize?.({
        runId: "v191-revise-run",
        sessionKey,
        lastAssistantMessage: "NO_REPLY",
      }, { runId: "v191-revise-run", sessionKey });

      expect(decision).toMatchObject({
        action: "revise",
        retry: {
          idempotencyKey: "cnxclaw-dashboard-visible-final:v191-revise-run",
          maxAttempts: 1,
        },
      });
      expect(String(decision?.retry?.instruction ?? "")).toMatch(/visible answer/iu);
      expect(String(decision?.retry?.instruction ?? "")).toMatch(/NO_REPLY/iu);

      expect(await beforeAgentFinalize?.({
        runId: "v191-revise-run",
        sessionKey,
        lastAssistantMessage: "CNX191-REVISION",
      }, { runId: "v191-revise-run", sessionKey })).toBeUndefined();

      expect(await beforeAgentFinalize?.({
        runId: "v191-revise-run",
        sessionKey,
        lastAssistantMessage: "Actual answer mentioning NO_REPLY is visible",
      }, { runId: "v191-revise-run", sessionKey })).toBeUndefined();

      expect(await beforeAgentFinalize?.({
        runId: "v191-not-ticketed",
        sessionKey: "agent:main:dashboard:not-ticketed",
        lastAssistantMessage: "NO_REPLY",
      }, { runId: "v191-not-ticketed", sessionKey: "agent:main:dashboard:not-ticketed" })).toBeUndefined();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
