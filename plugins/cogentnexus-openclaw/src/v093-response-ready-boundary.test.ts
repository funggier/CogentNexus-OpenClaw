import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery, stageDashboardDirectResult } from "./v091-dashboard-verified-delivery.js";
import { installV092DurableDeliveryBoundary } from "./v092-durable-delivery-boundary.js";

describe("v0.9.3 durable response-ready boundary", () => {
  it("never refreshes response_ready_at after a durable direct_result exists", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v093-ready-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:ready";
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "run-ready", ownerSessionKey: sessionKey, prompt: "hello" });
      store.route(ticket.ticketId, false);

      installV092DurableDeliveryBoundary();
      installV091DashboardVerifiedDelivery({ on: () => {}, logger: {} }, {
        workspaceDir: root,
        ticketDatabasePath: path,
      });

      const firstReady = new Date("2026-08-20T00:00:00.000Z");
      expect(stageDashboardDirectResult(path, {
        runId: "run-ready",
        text: "CNX-LIVE-A-01",
        now: firstReady,
      }).staged).toBe(true);

      let db = new DatabaseSync(path, { readOnly: true });
      const before = db.prepare("SELECT response_ready_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId) as { response_ready_at: string };
      expect(before.response_ready_at).toBe(firstReady.toISOString());
      db.close();

      // Repeated stale-delivery scans are allowed to schedule transport work only.
      // They must not move the first-ready timestamp and must not queue inference recovery.
      for (const stamp of [
        "2026-08-20T00:10:00.000Z",
        "2026-08-20T01:00:00.000Z",
        "2026-08-21T00:00:00.000Z",
      ]) {
        expect(store.recoverUndeliveredDirect({ now: new Date(stamp), olderThanMs: 1000 })).toEqual([]);
      }

      db = new DatabaseSync(path, { readOnly: true });
      const after = db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId) as any;
      expect(after).toEqual({
        status: "accepted",
        response_ready_at: firstReady.toISOString(),
        delivery_confirmed_at: null,
      });
      expect(db.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'")
        .get(ticket.ticketId)).toEqual({ n: 1 });
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='direct_redelivery_timeout'")
        .get(ticket.ticketId)).toEqual({ n: 0 });
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
