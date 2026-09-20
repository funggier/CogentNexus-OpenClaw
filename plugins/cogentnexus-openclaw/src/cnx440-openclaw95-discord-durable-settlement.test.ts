import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";
import entry from "./v091-release-entry.js";
import { TicketStore } from "./ticket-store.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";
import { sessionAuthority } from "./v090.js";

describe("CNX-440 OpenClaw 9.5 Discord durable settlement release wiring", () => {
  it("keeps the v095 Discord adapter live through release fences and settles a runId-less marker receipt", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx440-release-discord-"));
    try {
      mkdirSync(join(root, "host"), { recursive: true });
      writeFileSync(join(root, "host", "controller.json"), JSON.stringify({
        schemaVersion: 2,
        cnxMode: "active",
        generation: 440,
      }));

      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:440001";
      const runId = "cnx440-run";
      const store = new TicketStore(databasePath);
      sessionAuthority(databasePath, sessionKey);
      const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "CNX-440 release wiring" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(databasePath);
      const attempt = beginInferenceAttempt(db, {
        ticketId: ticket.ticketId,
        sessionKey,
        sessionGeneration: 0,
        callId: "cnx440-call",
        provider: "ollama",
        model: "qwen3.8:27b",
      });
      bindRunId(db, attempt.attemptId, runId);
      finishInferenceAttempt(db, attempt.attemptId, "completed");
      db.close();

      const registrations: Array<{ name: string; handler: any; options?: any }> = [];
      const api: any = {
        pluginConfig: {
          cogentNexusOpenClawRoot: root,
          workspaceDir: root,
          ticketDatabasePath: databasePath,
          ticketFirst: true,
          preInferenceAdmission: true,
          autoWorkflowCompletion: false,
        },
        config: { agents: { defaults: { workspace: root } } },
        logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
        on: (name: string, handler: any, options?: any) => registrations.push({ name, handler, options }),
        registerService: vi.fn(),
        registerTool: vi.fn(),
        registerGatewayMethod: vi.fn(),
        runtime: { tasks: { managedFlows: {} }, events: {} },
        session: { workflow: { unscheduleSessionTurnsByTag: vi.fn(), scheduleSessionTurn: vi.fn() } },
      };

      await (entry as any).register(api);

      const sending = registrations.find((item) =>
        item.name === "reply_payload_sending"
        && item.options?.registrationId === "cogentnexus-openclaw-v095-discord-delivery"
      )?.handler;
      const sent = registrations.find((item) =>
        item.name === "message_sent"
        && item.options?.registrationId === "cogentnexus-openclaw-v095-discord-delivery-receipt"
      )?.handler;
      expect(sending).toBeTypeOf("function");
      expect(sent).toBeTypeOf("function");

      const staged = await sending(
        { payload: { text: "CNX440_OK" }, kind: "final", channel: "discord", sessionKey, runId },
        { channelId: "discord", sessionKey, runId },
      );
      expect(staged?.payload?.text).toContain("CNX440_OK");
      expect(staged?.payload?.text).toContain("<!-- cogentnexus-openclaw-delivery:");

      await sent(
        { to: "440001", content: staged.payload.text, success: true, sessionKey, messageId: "cnx440-message" },
        { channelId: "discord", sessionKey },
      );

      const check = new DatabaseSync(databasePath, { readOnly: true });
      try {
        expect(check.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
          .get(ticket.ticketId)).toMatchObject({ status: "completed" });
        expect(check.prepare("SELECT run_id,status,delivery_state FROM cnx_assistant_delivery WHERE ticket_id=?")
          .get(ticket.ticketId)).toEqual({ run_id: runId, status: "delivered", delivery_state: "confirmed" });
        expect(check.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='delivery_confirmed'")
          .get(ticket.ticketId)).toEqual({ n: 1 });
      } finally { check.close(); }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
