import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

const discordOwnerSession = "agent:main:discord:channel:1531199905673252946";

describe("Task 207 direct Discord NO_REPLY visible-final boundary", () => {
  it("requests one bounded same-run revision for an accepted direct Discord owner Ticket", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v207-discord-no-reply-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      sessionAuthority(path, discordOwnerSession);
      const ticket = store.accept({
        runId: "v207-discord-revise-run",
        ownerSessionKey: discordOwnerSession,
        prompt: "ตอบกลับข้อความนี้เพียงว่า CNX207-DISCORD",
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
        runId: "v207-discord-revise-run",
        sessionKey: discordOwnerSession,
        lastAssistantMessage: "NO_REPLY",
      }, { runId: "v207-discord-revise-run", sessionKey: discordOwnerSession });

      expect(decision).toMatchObject({
        action: "revise",
        retry: {
          idempotencyKey: "cnxclaw-discord-visible-final:v207-discord-revise-run",
          maxAttempts: 1,
        },
      });
      expect(String(decision?.retry?.instruction ?? "")).toMatch(/visible answer/iu);
      expect(String(decision?.retry?.instruction ?? "")).toMatch(/NO_REPLY/iu);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it.each([
    ["visible final", "CNX207-VISIBLE"],
    ["mixed sentinel text", "Actual answer: NO_REPLY is a sentinel"],
  ])("does not revise a %s", async (_label, text) => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v207-discord-negative-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      sessionAuthority(path, discordOwnerSession);
      const ticket = store.accept({
        runId: "v207-discord-negative-run",
        ownerSessionKey: discordOwnerSession,
        prompt: "Explain the result",
      });
      store.route(ticket.ticketId, false);
      let beforeAgentFinalize: any;
      installV091DashboardVerifiedDelivery({
        on: (name: string, handler: any) => {
          if (name === "before_agent_finalize") beforeAgentFinalize = handler;
        },
        logger: {},
      }, { workspaceDir: root, ticketDatabasePath: path });

      await expect(beforeAgentFinalize({
        runId: "v207-discord-negative-run",
        sessionKey: discordOwnerSession,
        lastAssistantMessage: text,
      }, { runId: "v207-discord-negative-run", sessionKey: discordOwnerSession })).resolves.toBeUndefined();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("does not revise a non-ticketed Discord run or a mismatched session", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v207-discord-fences-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      sessionAuthority(path, discordOwnerSession);
      const ticket = store.accept({
        runId: "v207-discord-mismatch-run",
        ownerSessionKey: discordOwnerSession,
        prompt: "Mismatch fence",
      });
      store.route(ticket.ticketId, false);
      let beforeAgentFinalize: any;
      installV091DashboardVerifiedDelivery({
        on: (name: string, handler: any) => {
          if (name === "before_agent_finalize") beforeAgentFinalize = handler;
        },
        logger: {},
      }, { workspaceDir: root, ticketDatabasePath: path });

      await expect(beforeAgentFinalize({
        runId: "v207-not-ticketed",
        sessionKey: discordOwnerSession,
        lastAssistantMessage: "NO_REPLY",
      }, { runId: "v207-not-ticketed", sessionKey: discordOwnerSession })).resolves.toBeUndefined();

      await expect(beforeAgentFinalize({
        runId: "v207-discord-mismatch-run",
        sessionKey: "agent:main:discord:channel:other",
        lastAssistantMessage: "NO_REPLY",
      }, { runId: "v207-discord-mismatch-run", sessionKey: "agent:main:discord:channel:other" })).resolves.toBeUndefined();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
