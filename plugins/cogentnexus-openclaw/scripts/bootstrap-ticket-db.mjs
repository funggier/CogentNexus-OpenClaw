import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase, TicketStore } from "../dist/ticket-store.js";

function bootstrapManagedRuntimeSchema(database) {
  const db = new DatabaseSync(database);
  try {
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
      CREATE UNIQUE INDEX IF NOT EXISTS idx_cnx_direct_recovery_run
        ON cnx_direct_recovery(active_run_id) WHERE active_run_id IS NOT NULL;
      CREATE INDEX IF NOT EXISTS idx_cnx_direct_recovery_due
        ON cnx_direct_recovery(state,next_attempt_at,updated_at);
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
      CREATE TABLE IF NOT EXISTS cnx_direct_model_call(
        ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
        run_id TEXT NOT NULL,
        call_id TEXT NOT NULL,
        state TEXT NOT NULL,
        provider TEXT,
        model TEXT,
        started_at TEXT NOT NULL,
        deadline_at TEXT NOT NULL,
        ended_at TEXT,
        outcome TEXT,
        duration_ms INTEGER,
        recovery_started_at TEXT,
        recovery_attempt_count INTEGER NOT NULL DEFAULT 0,
        updated_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_cnx_direct_model_call_deadline
        ON cnx_direct_model_call(state,deadline_at);
    `);
  } finally {
    db.close();
  }
}

export function bootstrapTicketDatabase(workspace) {
  const resolvedWorkspace = resolve(workspace);
  const database = defaultTicketDatabase(resolvedWorkspace);
  // TicketStore owns the base schema. Registration-time recovery fences also
  // require additive managed-runtime tables before OpenClaw loads the plugin.
  new TicketStore(database).snapshot();
  bootstrapManagedRuntimeSchema(database);
  const snapshot = new TicketStore(database).snapshot();
  return { workspace: resolvedWorkspace, database, snapshot };
}

function parseWorkspace(argv) {
  const index = argv.indexOf("--workspace");
  if (index < 0 || !argv[index + 1]) {
    throw new Error("Usage: node scripts/bootstrap-ticket-db.mjs --workspace <path>");
  }
  return argv[index + 1];
}

const invokedPath = process.argv[1] ? pathToFileURL(resolve(process.argv[1])).href : null;
if (invokedPath && import.meta.url === invokedPath) {
  try {
    const result = bootstrapTicketDatabase(parseWorkspace(process.argv.slice(2)));
    console.log(JSON.stringify({ result: "ok", ...result }, null, 2));
  } catch (error) {
    console.error(error instanceof Error ? error.stack ?? error.message : String(error));
    process.exitCode = 1;
  }
}
