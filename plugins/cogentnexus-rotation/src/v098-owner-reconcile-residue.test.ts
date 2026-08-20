import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";

import { TicketStore } from "./ticket-store.js";
import {
  reconcileMissingOwnerSessions,
  retiredLegacyInternalRecoverySession,
} from "./v090-owner-reconcile.js";

function withFixture(name: string, run: (root: string, path: string) => Promise<void> | void) {
  return async () => {
    const root = mkdtempSync(join(tmpdir(), name));
    const path = join(root, "tickets.sqlite3");
    try {
      await run(root, path);
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  };
}

function ensureActiveCnxSession(path: string, sessionKey: string) {
  const db = new DatabaseSync(path);
  try {
    db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      deleted_at TEXT,
      delete_reason TEXT
    )`);
    db.prepare(`INSERT OR REPLACE INTO cnx_sessions(
      session_key,state,generation,created_at,updated_at,deleted_at,delete_reason
    ) VALUES (?,'active',0,?,?,NULL,NULL)`).run(
      sessionKey,
      "2026-08-20T03:00:00.000Z",
      "2026-08-20T03:00:00.000Z",
    );
  } finally {
    db.close();
  }
}

describe("v0.9.8 retired internal recovery owner residue", () => {
  it("does not block the pre-runtime owner fence for terminal v0.9.5 temp-session residue", withFixture(
    "cnx-v098-retired-residue-",
    async (root, path) => {
      const store = new TicketStore(path);
      const sessionKey = "temp:cogentnexus-direct-recovery:cnx-direct-CNXT-old-1-g0";
      const ticket = store.accept({ runId:"legacy-internal", ownerSessionKey:sessionKey, prompt:"internal recovery" });
      store.route(ticket.ticketId, false);

      let db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='cancelled',failure_message='historical Test A residue' WHERE ticket_id=?")
        .run(ticket.ticketId);
      db.close();
      ensureActiveCnxSession(path, sessionKey);

      expect(retiredLegacyInternalRecoverySession(path, sessionKey)).toBe(true);
      const getSessionEntry = vi.fn(() => {
        throw new Error("retired internal residue must never reach OpenClaw owner lookup");
      });
      const logger = { warn:vi.fn(), info:vi.fn() };
      const result = await reconcileMissingOwnerSessions({
        runtime:{ agent:{ session:{ getSessionEntry } } },
        logger,
      }, path, root);

      expect(result).toEqual({ supported:true, checked:0, deleted:0, workflowFailures:0, failed:0 });
      expect(getSessionEntry).not.toHaveBeenCalled();
      expect(logger.warn).not.toHaveBeenCalled();
      expect(logger.info).toHaveBeenCalledWith(
        expect.stringContaining("ignored retired internal Direct recovery residue"),
      );
    },
  ));

  it("still fails closed when a temp recovery key owns nonterminal durable work", withFixture(
    "cnx-v098-live-temp-owner-",
    async (root, path) => {
      const store = new TicketStore(path);
      const sessionKey = "temp:cogentnexus-direct-recovery:cnx-direct-CNXT-live-1-g0";
      const ticket = store.accept({ runId:"live-internal", ownerSessionKey:sessionKey, prompt:"still active" });
      store.route(ticket.ticketId, false);
      ensureActiveCnxSession(path, sessionKey);

      expect(retiredLegacyInternalRecoverySession(path, sessionKey)).toBe(false);
      const getSessionEntry = vi.fn(() => undefined);
      const logger = { warn:vi.fn(), info:vi.fn() };
      const result = await reconcileMissingOwnerSessions({
        runtime:{ agent:{ session:{ getSessionEntry } } },
        logger,
      }, path, root);

      expect(result).toEqual({ supported:true, checked:1, deleted:0, workflowFailures:0, failed:1 });
      expect(getSessionEntry).not.toHaveBeenCalled();
      expect(logger.warn).toHaveBeenCalledWith(
        expect.stringContaining("could not resolve agent id"),
      );

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status:"accepted" });
      db.close();
    },
  ));

  it("does not weaken the existing malformed-owner fail-closed boundary", withFixture(
    "cnx-v098-malformed-owner-",
    async (root, path) => {
      const store = new TicketStore(path);
      const ticket = store.accept({ runId:"malformed", ownerSessionKey:"bad-session-key", prompt:"bad" });
      store.route(ticket.ticketId, false);
      ensureActiveCnxSession(path, "bad-session-key");

      expect(retiredLegacyInternalRecoverySession(path, "bad-session-key")).toBe(false);
      const result = await reconcileMissingOwnerSessions({
        runtime:{ agent:{ session:{ getSessionEntry:vi.fn(() => undefined) } } },
        logger:{ warn:vi.fn(), info:vi.fn() },
      }, path, root);

      expect(result.failed).toBe(1);
      expect(result.checked).toBe(1);
    },
  ));
});
