import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installDashboardDirectSettlement } from "./v090-final-entry.js";
import { sessionAuthority } from "./v090.js";
import {
  deliveryMarker,
  installV091DashboardVerifiedDelivery,
  settleDashboardNativeDelivery,
  stageDashboardDirectResult,
} from "./v091-dashboard-verified-delivery.js";

describe("v0.9.1 Dashboard verified delivery", () => {
  it("supersedes the legacy no-receipt bypass and preserves exact durable text until verified delivery", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-dashboard-delivery-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:owner";
      expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
      const ticket = store.accept({
        runId: "dashboard-v091-run",
        ownerSessionKey: sessionKey,
        prompt: "ตอบเพียง CNX-LIVE-42",
      });
      store.route(ticket.ticketId, false);

      // Reproduce the shipped compatibility layering: v0.9 installs its historical
      // Dashboard auto-settlement first; v0.9.1 must supersede it at the release boundary.
      installDashboardDirectSettlement();
      let replyDispatch: ((event: any, ctx: any) => void) | undefined;
      installV091DashboardVerifiedDelivery({
        on: (name: string, handler: (event: any, ctx: any) => void) => {
          if (name === "reply_dispatch") replyDispatch = handler;
        },
        logger: {},
      }, { workspaceDir: root, ticketDatabasePath: path });

      // OpenClaw message/reply hooks expose stable turn correlation on ctx.runId when
      // available. The event itself may not carry runId, so exercise the registered hook
      // exactly that way instead of calling the staging helper directly.
      expect(replyDispatch).toBeTypeOf("function");

      // A legitimate second plugin registration in the same Node process must
      // receive its own runtime hook even though TicketStore was already patched.
      let secondReplyDispatch: ((event: any, ctx: any) => void) | undefined;
      installV091DashboardVerifiedDelivery({
        on: (name: string, handler: (event: any, ctx: any) => void) => {
          if (name === "reply_dispatch") secondReplyDispatch = handler;
        },
        logger: {},
      }, { workspaceDir: root, ticketDatabasePath: path });
      expect(secondReplyDispatch).toBeTypeOf("function");

      let beforeDeliver: ((payload: any, info: any) => any) | undefined;
      const dispatcher = {
        appendBeforeDeliver(handler: (payload: any, info: any) => any) {
          beforeDeliver = handler;
        },
        getQueuedCounts() { return { final: 1 }; },
        waitForIdle() { return new Promise<void>(() => undefined); },
        getFailedCounts() { return { final: 0 }; },
        getCancelledCounts() { return { final: 0 }; },
      };
      replyDispatch?.({}, { runId: "dashboard-v091-run", dispatcher });
      expect(beforeDeliver).toBeTypeOf("function");
      const nativePayload = beforeDeliver?.({ text: "CNX-LIVE-42" }, { kind: "final" });
      expect(nativePayload?.text).toContain("CNX-LIVE-42");

      let db = new DatabaseSync(path, { readOnly: true });
      const durable = db.prepare(`SELECT kind,text,target_json,idempotency_key,status FROM cnx_assistant_delivery
        WHERE ticket_id=?`).get(ticket.ticketId) as any;
      expect(durable).toMatchObject({ kind: "direct_result", text: "CNX-LIVE-42", status: "pending" });
      expect(nativePayload?.text).toContain(deliveryMarker(String(durable.idempotency_key)));
      expect(JSON.parse(String(durable.target_json))).toEqual({
        kind: "direct",
        ticketId: ticket.ticketId,
        runId: "dashboard-v091-run",
      });
      expect(db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ n: 1 });
      expect(db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toMatchObject({ status: "accepted", delivery_confirmed_at: null });
      db.close();

      // Idempotent re-observation of the same final does not duplicate the durable row.
      expect(stageDashboardDirectResult(path, {
        runId: "dashboard-v091-run",
        text: "CNX-LIVE-42",
        now: new Date("2026-01-01T00:00:01Z"),
      }).staged).toBe(true);
      expect(() => stageDashboardDirectResult(path, {
        runId: "dashboard-v091-run",
        text: "DIFFERENT RESULT",
        now: new Date("2026-01-01T00:00:02Z"),
      })).toThrow(/durable Dashboard result changed/u);

      // Even when the base agent_end event claims no visible output, the v0.9.1
      // durable row owns settlement. The legacy Dashboard required:false path is bypassed.
      expect(store.finalizeDirectRun({
        runId: "dashboard-v091-run",
        success: true,
        interrupted: false,
        expectsDelivery: false,
        now: new Date("2026-01-01T00:00:03Z"),
      })).toBe("unchanged");

      // Generic/early receipts cannot terminal a staged result; only the final dispatcher
      // verifier below or host_delivery.py marker dedup/injection owns confirmation.
      expect(store.confirmDirectDelivery({
        runId: "dashboard-v091-run",
        now: new Date("2026-01-01T00:00:04Z"),
      })).toBe("unchanged");

      // Delivery timeout scans must not regenerate while the exact answer is pending.
      expect(store.recoverUndeliveredDirect({
        now: new Date("2026-01-01T01:00:00Z"),
        olderThanMs: 1000,
      })).toEqual([]);

      db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT status,workflow_eligible,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status: "accepted", workflow_eligible: 0, delivery_confirmed_at: null });
      db.close();

      expect(settleDashboardNativeDelivery(path, "dashboard-v091-run", new Date("2026-01-01T01:00:01Z"))).toBe(true);

      db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT status,delivery_confirmed_at,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toMatchObject({ status: "completed", failure_class: null, failure_message: null });
      expect(db.prepare("SELECT status,delivered_at FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId))
        .toMatchObject({ status: "delivered" });
      const event = db.prepare(`SELECT payload_json FROM ticket_events WHERE ticket_id=? AND event_type='delivery_confirmed'
        ORDER BY event_id DESC LIMIT 1`).get(ticket.ticketId) as { payload_json: string };
      expect(JSON.parse(event.payload_json)).toMatchObject({ source: "native-dashboard-marker" });
      db.close();

      // If response_ready exists but the final payload was never durably captured, recovery
      // must fail closed rather than regenerate a reply that may already be visible.
      const unverifiable = store.accept({
        runId: "dashboard-v091-unverifiable",
        ownerSessionKey: sessionKey,
        prompt: "legacy RC response",
      });
      store.route(unverifiable.ticketId, false);
      expect(store.finalizeDirectRun({
        runId: "dashboard-v091-unverifiable",
        success: true,
        interrupted: false,
        expectsDelivery: true,
        now: new Date("2026-01-01T02:00:00Z"),
      })).toBe("awaiting_delivery");

      db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT result_json,status FROM tickets WHERE ticket_id=?").get(unverifiable.ticketId))
        .toMatchObject({ status: "accepted" });
      expect(db.prepare("SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?").get(unverifiable.ticketId))
        .toEqual({ n: 0 });
      db.close();

      expect(store.recoverUndeliveredDirect({
        now: new Date("2026-01-01T03:00:00Z"),
        olderThanMs: 1000,
      })).toEqual([]);

      db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT status,workflow_eligible,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(unverifiable.ticketId))
        .toMatchObject({
          status: "failed",
          workflow_eligible: 0,
          failure_class: "permanent",
          failure_message: "direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output",
        });
      expect(db.prepare("SELECT count(*) AS n FROM ticket_outbox WHERE ticket_id=?").get(unverifiable.ticketId))
        .toEqual({ n: 1 });
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("does not claim durable replay ownership for non-Dashboard Direct tickets", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-external-delivery-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:discord:channel";
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "external-run", ownerSessionKey: sessionKey, prompt: "hello" });
      store.route(ticket.ticketId, false);
      expect(stageDashboardDirectResult(path, { runId: "external-run", text: "hello" }))
        .toMatchObject({ staged: false, reason: "not-dashboard-direct" });
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
