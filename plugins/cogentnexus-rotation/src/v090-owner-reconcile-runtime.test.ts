import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";

describe("CogentNexus v0.9 owner reconciliation runtime seam", () => {
  it("uses the public agent.session accessor and never privileged Gateway RPC", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-owner-runtime-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const missing = store.accept({
        runId:"missing-owner-run",
        ownerSessionKey:"agent:main:dashboard:missing",
        prompt:"unfinished work",
      });
      store.route(missing.ticketId, false);

      const getSessionEntry = vi.fn(() => undefined);
      const gatewayRequest = vi.fn(() => {
        throw new Error("Gateway requests are only available to bundled or trusted official plugins.");
      });
      const result = await reconcileMissingOwnerSessions({
        runtime:{
          agent:{ session:{ getSessionEntry } },
          gateway:{ request:gatewayRequest },
        },
        logger:{ warn:vi.fn(), info:vi.fn() },
      }, path, root);

      expect(result).toMatchObject({ supported:true, checked:1, deleted:1, failed:0, workflowFailures:0 });
      expect(getSessionEntry).toHaveBeenCalledWith({
        agentId:"main",
        sessionKey:"agent:main:dashboard:missing",
        readConsistency:"latest",
      });
      expect(gatewayRequest).not.toHaveBeenCalled();

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(missing.ticketId))
        .toEqual({ status:"cancelled" });
      expect(db.prepare("SELECT state FROM cnx_sessions WHERE session_key=?").get("agent:main:dashboard:missing"))
        .toEqual({ state:"deleted" });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("preserves an owner that still exists", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-owner-present-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({
        runId:"present-owner-run",
        ownerSessionKey:"agent:main:dashboard:present",
        prompt:"current work",
      });
      store.route(ticket.ticketId, false);

      const result = await reconcileMissingOwnerSessions({
        runtime:{ agent:{ session:{ getSessionEntry:() => ({ sessionId:"physical-session" }) } } },
        logger:{ warn:vi.fn(), info:vi.fn() },
      }, path, root);

      expect(result).toMatchObject({ supported:true, checked:1, deleted:0, failed:0 });
      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status:"accepted" });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("fails closed for a malformed owner session key without touching another session", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-owner-malformed-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const malformed = store.accept({ runId:"bad", ownerSessionKey:"bad-session-key", prompt:"bad" });
      const other = store.accept({ runId:"other", ownerSessionKey:"agent:main:dashboard:other", prompt:"other" });
      store.route(malformed.ticketId, false);
      store.route(other.ticketId, false);

      const result = await reconcileMissingOwnerSessions({
        runtime:{ agent:{ session:{ getSessionEntry:({sessionKey}:{sessionKey:string}) => sessionKey.endsWith(":other") ? ({sessionId:"ok"}) : undefined } } },
        logger:{ warn:vi.fn(), info:vi.fn() },
      }, path, root);

      expect(result.failed).toBe(1);
      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(malformed.ticketId)).toEqual({ status:"accepted" });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(other.ticketId)).toEqual({ status:"accepted" });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });
});
