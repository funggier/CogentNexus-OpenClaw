import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { bootstrapTicketDatabase } from "./bootstrap-ticket-db.mjs";
import { installV095DirectRecoveryLaneFence } from "../dist/v095-direct-recovery.js";

const workspace = mkdtempSync(join(tmpdir(), "cnx-ticket-bootstrap-"));
const requiredTables = [
  "schema_migrations",
  "tickets",
  "ticket_events",
  "ticket_outbox",
  "experiences",
  "cnx_sessions",
  "cnx_direct_recovery",
  "cnx_assistant_delivery",
  "cnx_direct_model_call",
];

try {
  const first = bootstrapTicketDatabase(workspace);
  // Reproduce the exact registration-time precondition that failed on a clean
  // v0.9.1 install: v095 must be able to install its durable lane trigger
  // before any Chat turn has lazily opened the runtime schema.
  installV095DirectRecoveryLaneFence(first.database);

  const db = new DatabaseSync(first.database, { readOnly: true });
  try {
    const rows = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all();
    const tables = new Set(rows.map((row) => String(row.name)));
    const missing = requiredTables.filter((name) => !tables.has(name));
    if (missing.length) throw new Error(`ticket DB bootstrap missing tables: ${missing.join(", ")}`);
    const trigger = db.prepare("SELECT 1 FROM sqlite_master WHERE type='trigger' AND name='cnx_v095_direct_recovery_lane_lock'").get();
    if (!trigger) throw new Error("ticket DB bootstrap did not satisfy v095 lane-fence registration");
  } finally {
    db.close();
  }

  const second = bootstrapTicketDatabase(workspace);
  if (second.database !== first.database) throw new Error("ticket DB bootstrap path changed across idempotent run");
  console.log(`CogentNexus-OpenClaw ticket DB bootstrap: PASS (${requiredTables.length} required tables + v095 registration fence)`);
} finally {
  rmSync(workspace, { recursive: true, force: true });
}
