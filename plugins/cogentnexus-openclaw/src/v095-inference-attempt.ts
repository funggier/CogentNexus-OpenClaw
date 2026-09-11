import { randomUUID } from "node:crypto";
import { DatabaseSync } from "node:sqlite";

export type InferenceAttempt = {
  attemptId: string;
  ticketId: string;
  sessionKey: string;
  sessionGeneration: number;
  runId: string | null;
  callId: string;
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
  callId: string;
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
      call_id TEXT NOT NULL,
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
      ON cnx_inference_attempt(run_id,started_at) WHERE run_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run_call
      ON cnx_inference_attempt(run_id,call_id);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_session
      ON cnx_inference_attempt(session_key,session_generation,started_at);
  `);
  const columns = new Set((db.prepare("PRAGMA table_info(cnx_inference_attempt)").all() as Array<{ name?: string }>).map((row) => row.name));
  if (!columns.has("call_id")) {
    db.exec("ALTER TABLE cnx_inference_attempt ADD COLUMN call_id TEXT NOT NULL DEFAULT 'legacy'");
    db.exec("CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run_call ON cnx_inference_attempt(run_id,call_id)");
  }
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
    callId: String(row.call_id),
    provider: row.provider == null ? null : String(row.provider),
    model: row.model == null ? null : String(row.model),
    state: row.state === "ended" ? "ended" : "active",
    outcome: row.outcome == null ? null : String(row.outcome),
    startedAt: String(row.started_at),
    endedAt: row.ended_at == null ? null : String(row.ended_at),
  };
}

function load(db: DatabaseSync, attemptId: string): InferenceAttempt {
  return rowToAttempt(db.prepare(`SELECT attempt_id,ticket_id,session_key,session_generation,run_id,call_id,
      provider,model,state,outcome,started_at,ended_at
    FROM cnx_inference_attempt WHERE attempt_id=?`).get(attemptId));
}

function addEvent(db: DatabaseSync, ticketId: string, eventType: string, payload: Record<string, unknown>, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

function assertCurrentSessionGeneration(db: DatabaseSync, attempt: InferenceAttempt) {
  const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(attempt.sessionKey) as { state?: string; generation?: number } | undefined;
  if (!session || session.state !== "active") throw new Error("inference attempt owner session is not active");
  if (Number(session.generation) !== attempt.sessionGeneration) throw new Error("inference attempt owner generation is stale");
}

export function findInferenceAttempt(db: DatabaseSync, runId: string, callId: string): InferenceAttempt | null {
  if (!runId || !callId) return null;
  ensureBase(db);
  const row = db.prepare(`SELECT attempt_id,ticket_id,session_key,session_generation,run_id,call_id,
      provider,model,state,outcome,started_at,ended_at
    FROM cnx_inference_attempt WHERE run_id=? AND call_id=?`).get(runId, callId);
  return row ? rowToAttempt(row) : null;
}

export function beginInferenceAttempt(db: DatabaseSync, input: BeginAttemptInput): InferenceAttempt {
  if (!input.ticketId || !input.sessionKey || !input.callId) throw new Error("ticketId, sessionKey and callId are required");
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
    const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(input.sessionKey) as { state?: string; generation?: number } | undefined;
    if (!session || session.state !== "active") throw new Error("inference attempt owner session is not active");
    if (Number(session.generation) !== input.sessionGeneration) throw new Error("inference attempt owner generation is stale");
    const duplicate = db.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE call_id=? LIMIT 1").get(input.callId) as { attempt_id?: string } | undefined;
    if (duplicate) throw new Error("callId is already bound to an inference attempt");

    const attemptId = `cnx-attempt-${randomUUID()}`;
    db.prepare(`INSERT INTO cnx_inference_attempt(
      attempt_id,ticket_id,session_key,session_generation,run_id,call_id,provider,model,state,outcome,started_at,ended_at
    ) VALUES (?,?,?,?,?,?,?,?,'active',NULL,?,NULL)`).run(
      attemptId,
      input.ticketId,
      input.sessionKey,
      input.sessionGeneration,
      null,
      input.callId,
      input.provider ?? null,
      input.model ?? null,
      stamp,
    );
    addEvent(db, input.ticketId, "inference_attempt_started", {
      attemptId,
      callId: input.callId,
      sessionKey: input.sessionKey,
      sessionGeneration: input.sessionGeneration,
      provider: input.provider ?? undefined,
      model: input.model ?? undefined,
      source: "cogentnexus-openclaw-canonical-attempt",
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
    assertCurrentSessionGeneration(db, current);
    if (current.runId !== null && current.runId !== runId) throw new Error("inference attempt already bound to another run");
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
    assertCurrentSessionGeneration(db, current);
    const changed = db.prepare(`UPDATE cnx_inference_attempt
      SET state='ended',outcome=?,ended_at=?
      WHERE attempt_id=? AND state='active'`).run(outcome, stamp, attemptId);
    if (changed.changes !== 1) throw new Error("inference attempt is not active");
    addEvent(db, current.ticketId, "inference_attempt_ended", {
      attemptId,
      callId: current.callId,
      runId: current.runId ?? undefined,
      outcome,
      source: "cogentnexus-openclaw-canonical-attempt",
    }, stamp);
    const result = load(db, attemptId);
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}