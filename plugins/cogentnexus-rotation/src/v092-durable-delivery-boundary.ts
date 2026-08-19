import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

const PATCH = Symbol.for("cogentnexus.v092.durable-direct-delivery-boundary");

function ensureBoundaryTables(path: string) {
  new TicketStore(path).snapshot();
  const db = new DatabaseSync(path);
  db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL DEFAULT 'active' CHECK(state IN ('active','deleting','deleted')),
      generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      deleted_at TEXT,
      delete_reason TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      mode TEXT NOT NULL DEFAULT 'resume',
      state TEXT NOT NULL DEFAULT 'pending',
      attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      owner_generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS cnx_assistant_delivery(
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id TEXT REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      owner_session_key TEXT NOT NULL,
      owner_generation INTEGER NOT NULL DEFAULT 0,
      kind TEXT NOT NULL,
      text TEXT NOT NULL,
      target_json TEXT,
      idempotency_key TEXT NOT NULL UNIQUE,
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','delivered')),
      attempt_count INTEGER NOT NULL DEFAULT 0,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      delivered_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_pending
      ON cnx_assistant_delivery(status,owner_session_key,delivery_id);
  `);
  return db;
}

function ensureActiveSession(db: DatabaseSync, sessionKey: string, stamp: string) {
  db.prepare(`INSERT OR IGNORE INTO cnx_sessions(session_key,state,generation,created_at,updated_at)
    VALUES (?,'active',0,?,?)`).run(sessionKey, stamp, stamp);
  return db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?")
    .get(sessionKey) as { state?: string; generation?: number } | undefined;
}

function queueLegacyRedelivery(
  db: DatabaseSync,
  row: { ticket_id: string; owner_session_key: string },
  message: string,
  stamp: string,
) {
  const authority = ensureActiveSession(db, row.owner_session_key, stamp);
  if (authority?.state !== "active") return false;
  const generation = Number(authority.generation ?? 0);
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at
    ) VALUES (?,'redeliver','pending',0,NULL,?,?,?, ?,?)
    ON CONFLICT(ticket_id) DO UPDATE SET
      mode='redeliver',state='pending',active_run_id=NULL,next_attempt_at=excluded.next_attempt_at,
      last_error=excluded.last_error,owner_generation=excluded.owner_generation,updated_at=excluded.updated_at`)
    .run(row.ticket_id, stamp, message.slice(0, 2000), generation, stamp, stamp);
  return true;
}

/**
 * Once a direct_result is committed, inference is finished for that Ticket.
 * Delivery retries may observe/retry transport, but must never clear the first
 * response_ready_at timestamp or queue a new recovery inference run.
 */
export function installV092DurableDeliveryBoundary() {
  const prototype = TicketStore.prototype as any;
  if (prototype[PATCH]) return;
  Object.defineProperty(prototype, PATCH, { value: true });

  TicketStore.prototype.recoverUndeliveredDirect = function(
    input: Parameters<TicketStore["recoverUndeliveredDirect"]>[0] = {},
  ) {
    const n = input.now ?? new Date();
    const cutoff = new Date(n.getTime() - Math.max(1000, input.olderThanMs ?? 120_000)).toISOString();
    const stamp = n.toISOString();
    const limit = Math.max(1, Math.min(input.limit ?? 100, 1000));
    const db = ensureBoundaryTables(this.databasePath);
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows = db.prepare(`SELECT ticket_id,run_id,owner_session_key FROM tickets
        WHERE status='accepted' AND workflow_eligible=0
          AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL
          AND response_ready_at<=?
        ORDER BY response_ready_at LIMIT ?`).all(cutoff, limit) as Array<{
          ticket_id: string;
          run_id: string;
          owner_session_key: string;
        }>;

      for (const row of rows) {
        const durable = db.prepare(`SELECT delivery_id,status FROM cnx_assistant_delivery
          WHERE ticket_id=? AND kind='direct_result' AND status IN ('pending','delivered')
          ORDER BY delivery_id DESC LIMIT 1`).get(row.ticket_id) as
          { delivery_id?: number; status?: string } | undefined;

        // Durable response exists: transport owns the next action. Never
        // regenerate inference and never rewrite response_ready_at.
        if (durable) continue;

        const message = "Direct response delivery was not confirmed before deadline";
        if (!queueLegacyRedelivery(db, row, message, stamp)) continue;
        db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,
          response_ready_at=NULL,updated_at=? WHERE ticket_id=?`)
          .run(message, message, stamp, row.ticket_id);
        db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
          .run(row.ticket_id, "direct_redelivery_timeout", JSON.stringify({ runId: row.run_id, cutoff }), stamp);
      }
      db.exec("COMMIT");
      return [];
    } catch (error) {
      try { db.exec("ROLLBACK"); } catch {}
      throw error;
    } finally {
      db.close();
    }
  };
}
