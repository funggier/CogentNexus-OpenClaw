import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installDashboardDirectSettlement } from "./v090-final-entry.js";

describe("v0.9 Dashboard Direct delivery authority", () => {
  installDashboardDirectSettlement();

  it("completes an exact Dashboard Direct Ticket and signals run-map cleanup", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-dashboard-direct-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({
        runId:"dashboard-run",
        ownerSessionKey:"agent:main:dashboard:owner",
        prompt:"สวัสดีครับ",
      });
      store.route(ticket.ticketId, false);

      // "unchanged" is intentionally returned to the base agent_end handler as
      // its no-receipt-pending cleanup signal. Durable state is completed below.
      expect(store.finalizeDirectRun({
        runId:"dashboard-run",
        success:true,
        interrupted:false,
        expectsDelivery:true,
      })).toBe("unchanged");

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId)).toMatchObject({ status:"completed" });
      const row = db.prepare("SELECT response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId) as {response_ready_at:string|null;delivery_confirmed_at:string|null};
      expect(row.response_ready_at).toBeTruthy();
      expect(row.delivery_confirmed_at).toBeTruthy();
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("keeps external-channel Direct Tickets on receipt-confirmed delivery", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-channel-direct-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({
        runId:"discord-run",
        ownerSessionKey:"agent:main:discord:channel",
        prompt:"hello",
      });
      store.route(ticket.ticketId, false);

      expect(store.finalizeDirectRun({
        runId:"discord-run",
        success:true,
        interrupted:false,
        expectsDelivery:true,
      })).toBe("awaiting_delivery");

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status:"accepted", delivery_confirmed_at:null });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });
});
