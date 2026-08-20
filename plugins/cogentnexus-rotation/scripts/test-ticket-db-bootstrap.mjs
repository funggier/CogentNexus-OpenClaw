import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { bootstrapTicketDatabase } from "./bootstrap-ticket-db.mjs";

const workspace = mkdtempSync(join(tmpdir(), "cnx-ticket-bootstrap-"));
const requiredTables = [
  "schema_migrations",
  "tickets",
  "ticket_events",
  "ticket_outbox",
  "experiences",
];

try {
  const first = bootstrapTicketDatabase(workspace);
  const db = new DatabaseSync(first.database, { readOnly: true });
  try {
    const rows = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all();
    const tables = new Set(rows.map((row) => String(row.name)));
    const missing = requiredTables.filter((name) => !tables.has(name));
    if (missing.length) throw new Error(`ticket DB bootstrap missing tables: ${missing.join(", ")}`);
  } finally {
    db.close();
  }

  const second = bootstrapTicketDatabase(workspace);
  if (second.database !== first.database) throw new Error("ticket DB bootstrap path changed across idempotent run");
  console.log(`CogentNexus ticket DB bootstrap: PASS (${requiredTables.length} required tables)`);
} finally {
  rmSync(workspace, { recursive: true, force: true });
}
