import { DatabaseSync } from "node:sqlite";
import { isControlCommandMessage } from "openclaw/plugin-sdk/command-detection";

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

function addEvent(db: DatabaseSync, ticketId: string, eventType: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

function noEvidence(db: DatabaseSync, ticketId: string) {
  const evidenceTables = [
    "cnx_direct_model_call",
    "cnx_inference_attempt",
    "cnx_assistant_delivery",
    "cnx_direct_recovery",
  ];
  if (!evidenceTables.every((name) => tableExists(db, name))) return false;
  return evidenceTables.every((name) => {
    const row = db.prepare(`SELECT 1 FROM ${name} WHERE ticket_id=? LIMIT 1`).get(ticketId);
    return !row;
  });
}

function isNativeCommand(prompt: string, cfg: any) {
  try {
    return isControlCommandMessage(prompt, cfg ?? {});
  } catch {
    return false;
  }
}

export function retireHistoricalNativeCommandTickets(input: {
  ticketDatabasePath: string;
  cfg?: any;
  now?: Date;
  minAgeMs?: number;
}) {
  const db = new DatabaseSync(input.ticketDatabasePath);
  const now = input.now ?? new Date();
  const stamp = now.toISOString();
  const minAgeMs = Math.max(1_000, input.minAgeMs ?? 60_000);
  const cutoff = new Date(now.getTime() - minAgeMs).toISOString();
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
    if (!tableExists(db, "tickets") || !tableExists(db, "ticket_events")) {
      return { scanned: 0, retired: 0, skippedForEvidence: 0, schemaReady: false };
    }
    const evidenceTables = [
      "cnx_direct_model_call",
      "cnx_inference_attempt",
      "cnx_assistant_delivery",
      "cnx_direct_recovery",
    ];
    if (!evidenceTables.every((name) => tableExists(db, name))) {
      return { scanned: 0, retired: 0, skippedForEvidence: 0, schemaReady: false };
    }

    const rows = db.prepare(`
      SELECT ticket_id,run_id,owner_session_key,prompt,created_at
      FROM tickets
      WHERE status='accepted'
        AND workflow_eligible=0
        AND response_ready_at IS NULL
        AND delivery_confirmed_at IS NULL
        AND created_at<=?
      ORDER BY created_at,ticket_id
    `).all(cutoff) as Array<{
      ticket_id: string;
      run_id: string;
      owner_session_key: string;
      prompt: string;
      created_at: string;
    }>;

    let retired = 0;
    let skippedForEvidence = 0;
    db.exec("BEGIN IMMEDIATE");
    for (const row of rows) {
      if (!isNativeCommand(String(row.prompt ?? ""), input.cfg)) continue;
      if (!noEvidence(db, row.ticket_id)) {
        skippedForEvidence += 1;
        continue;
      }
      const reason = "Retired stranded native OpenClaw command Ticket during CNX-442 migration";
      const changed = db.prepare(`
        UPDATE tickets SET status='cancelled',failure_class=NULL,failure_message=?,
          result_json=NULL,response_ready_at=NULL,delivery_confirmed_at=NULL,
          delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0
          AND response_ready_at IS NULL AND delivery_confirmed_at IS NULL
      `).run(reason, stamp, row.ticket_id);
      if (changed.changes !== 1) continue;
      addEvent(db, row.ticket_id, "native_command_ticket_retired", {
        runId: row.run_id,
        ownerSessionKey: row.owner_session_key,
        createdAt: row.created_at,
        source: "cnx442-startup-retirement",
      }, stamp);
      retired += 1;
    }
    db.exec("COMMIT");
    return { scanned: rows.length, retired, skippedForEvidence, schemaReady: true };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}
