import { randomUUID } from "node:crypto";
import { DatabaseSync } from "node:sqlite";

export type InferenceAttempt = {
  attemptId: string;
  ticketId: string;
  sessionKey: string;
  sessionGeneration: number;
  runId: string | null;
  provider: string | null;
  model: string | null;
  state: "active" | "ended";
  outcome: string | null;
  startedAt: string;
  endedAt: string | null;
};

export type BeginAttemptInput = {
  ticketId: string;
  sessionKey: string;
  sessionGeneration: number;
  provider?: string | null;
  model?: string | null;
  now?: Date;
};

function ensureSchema(db: DatabaseSync) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_inference_attempt(
      attempt_id TEXT PRIMARY KEY,
      ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      session_key TEXT NOT NULL,
      session_generation INTEGER NOT NULL,
      run_id TEXT,
      provider TEXT,
      model TEXT,
      state TEXT NOT NULL CHECK(state IN ('active','ended')),
      outcome TEXT,
      started_at TEXT NOT NULL,
      ended_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_ticket
      ON cnx_inference_attempt(ticket_id,started_at);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run
      ON cnx_inference_attempt(run_id) WHERE run_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_session
      ON cnx_inference_attempt(session_key,session_generation,started_at);
  `);
}

function ensureBase(db: DatabaseSync) {
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  ensureSchema(db);
}

function rowToAttempt(row: any): InferenceAttempt {
  if (!row) throw new Error("inference attempt not found");
  return {
    attemptId: String(row.attempt_id),
    ticketId: String(row.ticket_id),
    sessionKey: String(row.session_key),
    sessionGeneration: Number(row.session_generation),
    runId: row.run_id == null ? null : String(row.run_id),
    provider: row.provider == null ? null : String(row.provider),
    model: row.model == null ? null : String(row.model),
    state: row.state === "ended" ? "ended" : "active",
    outcome: row.outcome == null ? null : String(row.outcome),
    startedAt: String(row.started_at),
    endedAt: row.ended_at == null ? null : String(row.ended_at),
  };
}

function load(db: DatabaseSync, attemptId: string): InferenceAttempt {
  return rowToAttempt(db.prepare(`SELECT attempt_id,ticket_id,session_key,session_generation,run_id,
      provider,model,state,outcome,started_at,ended_at
    FROM cnx_inference_attempt WHERE attempt_id=?`).get(attemptId));
}

function addEvent(db: DatabaseSync, ticketId: string, eventType: string, payload: Record<string, unknown>, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

export function beginInferenceAttempt(db: DatabaseSync, input: BeginAttemptInput): InferenceAttempt {
  if (!input.ticketId || !input.sessionKey) throw new Error("ticketId and sessionKey are required");
  if (!Number.isSafeInteger(input.sessionGeneration) || input.sessionGeneration < 0) {
    throw new Error("sessionGeneration must be a non-negative safe integer");
  }
  const stamp = (input.now ?? new Date()).toISOString();
  ensureBase(db);
  db.exec("BEGIN IMMEDIATE");
  try {
    const ticket = db.prepare("SELECT owner_session_key FROM tickets WHERE ticket_id=?").get(input.ticketId) as { owner_session_key?: string } | undefined;
    if (!ticket) throw new Error(`ticket ${input.ticketId} not found`);
    if (ticket.owner_session_key !== input.sessionKey) throw new Error("inference attempt owner session mismatch");

    const attemptId = `cnx-attempt-${randomUUID()}`;
    db.prepare(`INSERT INTO cnx_inference_attempt(
      attempt_id,ticket_id,session_key,session_generation,run_id,provider,model,state,outcome,started_at,ended_at
    ) VALUES (?,?,?,?,?,?,?,'active',NULL,?,NULL)`).run(
      attemptId,
      input.ticketId,
      input.sessionKey,
      input.sessionGeneration,
      null,
      input.provider ?? null,
      input.model ?? null,
      stamp,
    );
    addEvent(db, input.ticketId, "inference_attempt_started", {
      attemptId,
      sessionKey: input.sessionKey,
      sessionGeneration: input.sessionGeneration,
      provider: input.provider ?? undefined,
      model: input.model ?? undefined,
      source: "cogentnexus-v095-canonical-attempt",
    }, stamp);
    const result = load(db, attemptId);
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}

export function bindRunId(db: DatabaseSync, attemptId: string, runId: string): InferenceAttempt {
  if (!attemptId || !runId) throw new Error("attemptId and runId are required");
  ensureBase(db);
  db.exec("BEGIN IMMEDIATE");
  try {
    const current = load(db, attemptId);
    if (current.state !== "active") throw new Error("inference attempt is not active");
    if (current.runId !== null && current.runId !== runId) throw new Error("inference attempt already bound to another run");
    const owner = db.prepare("SELECT 1 FROM cnx_inference_attempt WHERE run_id=? AND attempt_id<>? LIMIT 1").get(runId, attemptId);
    if (owner) throw new Error("runId is already bound to another inference attempt");
    db.prepare("UPDATE cnx_inference_attempt SET run_id=? WHERE attempt_id=? AND state='active'").run(runId, attemptId);
    const result = load(db, attemptId);
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}

export function finishInferenceAttempt(db: DatabaseSync, attemptId: string, outcome: string, now = new Date()): InferenceAttempt {
  if (!attemptId || !outcome) throw new Error("attemptId and outcome are required");
  const stamp = now.toISOString();
  ensureBase(db);
  db.exec("BEGIN IMMEDIATE");
  try {
    const current = load(db, attemptId);
    if (current.state !== "active") throw new Error("inference attempt is not active");
    const changed = db.prepare(`UPDATE cnx_inference_attempt
      SET state='ended',outcome=?,ended_at=?
      WHERE attempt_id=? AND state='active'`).run(outcome, stamp, attemptId);
    if (changed.changes !== 1) throw new Error("inference attempt is not active");
    addEvent(db, current.ticketId, "inference_attempt_ended", {
      attemptId,
      runId: current.runId ?? undefined,
      outcome,
      source: "cogentnexus-v095-canonical-attempt",
    }, stamp);
    const result = load(db, attemptId);
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}
