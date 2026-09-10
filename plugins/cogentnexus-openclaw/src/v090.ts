import { spawn, spawnSync } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { existsSync, readFileSync, readdirSync, renameSync, statfsSync, writeFileSync } from "node:fs";
import { freemem } from "node:os";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { classifyDurableRequest, compileDurableIntake, durableRequestFingerprint } from "./admission.js";
import { parseDeliveryMarker, settleDeliveryTarget, type DeliveryTarget } from "./delivery-continuity.js";
import baseEntry, {
  deliverTicketOutbox,
  reconcileTicketWorkflows,
  startBoundWorkflow,
  ticketResourceAdmission,
} from "./index.js";
import { defaultTicketDatabase, TicketStore, type TicketLease } from "./ticket-store.js";

type Cfg = {
  cogentNexusOpenClawRoot?: string;
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  ticketOutboxPollMs?: number;
  ticketDispatchPollMs?: number;
  ticketDispatchLimit?: number;
  ticketLeaseMs?: number;
  ticketMinimumFreeMemoryBytes?: number;
  ticketMinimumFreeDiskBytes?: number;
  ticketMaximumRunning?: number;
  ticketMaximumAttempts?: number;
  directDeliveryTimeoutMs?: number;
  outboxDeliveryTimeoutMs?: number;
  durableWorkerModel?: string;
  timeoutSeconds?: number;
  admissionMinimumScore?: number;
  pythonCommand?: string;
  agentId?: string;
};

type Recovery = {
  ticket_id: string;
  owner_session_key: string;
  prompt: string;
  mode: "resume" | "redeliver";
  attempt_count: number;
  owner_generation: number;
};

type Turn = {
  sessionKey: string;
  delayMs: number;
  deleteAfterRun: boolean;
  deliveryMode: "announce";
  name: string;
  tag: string;
  message: string;
  ownerGeneration?: number;
};

type AssistantDeliveryTarget =
  | { kind: "direct"; ticketId: string; runId: string }
  | DeliveryTarget
  | { kind: "notice" };

type SessionAuthority = { state: "active" | "deleting" | "deleted"; generation: number };
type SessionLifecycleResult = SessionAuthority & { accepted: boolean; lifecycleMatches: boolean; sessionId?: string | null };
type ActiveSynthetic = { childSessionKey: string; generation: number };

const PATCH = Symbol.for("cogentnexus-openclaw.v090.ticket-patch");
const WRAP = Symbol.for("cogentnexus-openclaw.v090.entry-wrap");
const now = () => new Date().toISOString();
const dbPath = (cfg: Cfg, workspace: string) => resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspace));
const activeSynthetic = new Map<string, Map<string, ActiveSynthetic>>();

function ensureColumn(db: DatabaseSync, table: string, column: string, declaration: string) {
  const columns = db.prepare(`PRAGMA table_info(${table})`).all() as Array<{ name: string }>;
  if (!columns.some((item) => item.name === column)) db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${declaration}`);
}

function openDb(path: string) {
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
      delete_reason TEXT,
      session_id TEXT
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
  `);
  ensureColumn(db, "cnx_direct_recovery", "owner_generation", "INTEGER NOT NULL DEFAULT 0");
  ensureColumn(db, "cnx_assistant_delivery", "owner_generation", "INTEGER NOT NULL DEFAULT 0");
  ensureColumn(db, "cnx_sessions", "session_id", "TEXT");
  return db;
}

function addEvent(db: DatabaseSync, ticketId: string, type: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, type, JSON.stringify(payload), stamp);
}

function ensureSession(db: DatabaseSync, sessionKey: string, stamp = now()): SessionAuthority {
  const key = sessionKey.trim();
  if (!key) throw new Error("session key required");
  db.prepare(`INSERT OR IGNORE INTO cnx_sessions(session_key,state,generation,created_at,updated_at)
    VALUES (?,'active',0,?,?)`).run(key, stamp, stamp);
  const row = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(key) as any;
  return { state: row.state, generation: Number(row.generation) };
}

export function sessionAuthority(path: string, sessionKey: string): SessionAuthority {
  const db = openDb(path);
  try { return ensureSession(db, sessionKey); }
  finally { db.close(); }
}

export function reactivateSessionForLifecycle(path: string, input: { sessionKey: string; sessionId: string }): SessionLifecycleResult {
  const sessionKey = input.sessionKey.trim(), sessionId = input.sessionId.trim();
  if (!sessionKey || !sessionId) throw new Error("session key and lifecycle session id required");
  const db = openDb(path);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare("SELECT state,generation,session_id FROM cnx_sessions WHERE session_key=?").get(sessionKey) as any;
    if (!row) {
      const stamp = now();
      db.prepare(`INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id)
        VALUES (?,'active',0,?,?,?)`).run(sessionKey, stamp, stamp, sessionId);
      db.exec("COMMIT");
      return { state: "active", generation: 0, accepted: true, lifecycleMatches: true, sessionId };
    }
    const currentGeneration = Number(row.generation);
    const currentSessionId = typeof row.session_id === "string" ? row.session_id : null;
    if (row.state === "active") {
      if (currentSessionId === null) {
        const stamp = now();
        db.prepare("UPDATE cnx_sessions SET session_id=?,updated_at=? WHERE session_key=? AND state='active' AND session_id IS NULL")
          .run(sessionId, stamp, sessionKey);
        db.exec("COMMIT");
        return { state: "active", generation: currentGeneration, accepted: true, lifecycleMatches: true, sessionId };
      }
      const matches = currentSessionId === sessionId;
      db.exec("COMMIT");
      return { state: "active", generation: currentGeneration, accepted: matches, lifecycleMatches: matches, sessionId: currentSessionId };
    }
    if (row.state === "deleted" && currentSessionId === sessionId) {
      db.exec("COMMIT");
      return { state: "deleted", generation: currentGeneration, accepted: false, lifecycleMatches: false, sessionId: currentSessionId };
    }
    if (row.state !== "deleted") {
      db.exec("COMMIT");
      return { state: row.state as SessionAuthority["state"], generation: currentGeneration, accepted: false, lifecycleMatches: false, sessionId: currentSessionId };
    }
    const stamp = now(), generation = currentGeneration;
    db.prepare(`UPDATE cnx_sessions SET state='active',generation=?,updated_at=?,deleted_at=NULL,delete_reason=NULL,session_id=?
      WHERE session_key=? AND state='deleted' AND (session_id IS NULL OR session_id<>?)`)
      .run(generation, stamp, sessionId, sessionKey, sessionId);
    db.exec("COMMIT");
    return { state: "active", generation, accepted: true, lifecycleMatches: true, sessionId };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function isCurrentSessionLifecycle(path: string, input: { sessionKey: string; sessionId: string }): boolean {
  const sessionKey = input.sessionKey.trim(), sessionId = input.sessionId.trim();
  if (!sessionKey || !sessionId) return false;
  const db = openDb(path);
  try {
    const row = db.prepare("SELECT state,session_id FROM cnx_sessions WHERE session_key=?").get(sessionKey) as any;
    return Boolean(row?.state === "active" && row.session_id && row.session_id === sessionId);
  } finally { db.close(); }
}

function sessionAuthorityFromDb(db: DatabaseSync, sessionKey: string): SessionAuthority {
  return ensureSession(db, sessionKey);
}

function registerExistingSessions(db: DatabaseSync, stamp: string) {
  const rows = db.prepare("SELECT DISTINCT owner_session_key FROM tickets WHERE owner_session_key<>''").all() as Array<{ owner_session_key: string }>;
  for (const row of rows) ensureSession(db, row.owner_session_key, stamp);
}

function sessionIsCurrent(path: string, sessionKey: string, generation: number): boolean {
  const db = openDb(path);
  try {
    const row = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(sessionKey) as any;
    return Boolean(row && row.state === "active" && Number(row.generation) === generation);
  } finally { db.close(); }
}

function queueRecovery(
  db: DatabaseSync,
  ticketId: string,
  ownerSessionKey: string,
  mode: "resume" | "redeliver",
  message: string,
  stamp: string,
): boolean {
  const authority = sessionAuthorityFromDb(db, ownerSessionKey);
  if (authority.state !== "active") return false;
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at
    ) VALUES (?,?,'pending',0,NULL,?,?,?, ?,?)
    ON CONFLICT(ticket_id) DO UPDATE SET
      mode=excluded.mode,state='pending',active_run_id=NULL,next_attempt_at=excluded.next_attempt_at,
      last_error=excluded.last_error,owner_generation=excluded.owner_generation,updated_at=excluded.updated_at`)
    .run(ticketId, mode, stamp, message.slice(0, 2000), authority.generation, stamp, stamp);
  return true;
}

function revokeSession(
  path: string,
  input: { sessionKey: string; message: string; source: string; deleting: boolean; sessionId?: string; now?: Date },
) {
  const db = openDb(path);
  const stamp = (input.now ?? new Date()).toISOString();
  const reason = input.message.slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const prior = sessionAuthorityFromDb(db, input.sessionKey);
    const nextGeneration = prior.generation + 1;
    db.prepare(`UPDATE cnx_sessions SET state=?,generation=?,updated_at=?,delete_reason=?,session_id=COALESCE(?,session_id)
      WHERE session_key=?`).run(input.deleting ? "deleting" : "active", nextGeneration, stamp,
        input.deleting ? reason : null, input.sessionId ?? null, input.sessionKey);
    const rows = db.prepare(`SELECT ticket_id,status,run_id,workflow_id FROM tickets
      WHERE owner_session_key=? AND status IN ('accepted','planned','running','waiting') ORDER BY created_at,ticket_id`)
      .all(input.sessionKey) as any[];
    const pending = db.prepare(`SELECT outbox_id,ticket_id FROM ticket_outbox
      WHERE owner_session_key=? AND delivery_status='pending' ORDER BY outbox_id`).all(input.sessionKey) as any[];
    const cancelled: string[] = [];
    const workflowIds: string[] = [];
    const cancellationEvent = input.deleting
      ? "cancelled_by_session_delete"
      : input.source === "openclaw-session-reset"
        ? "cancelled_by_session_reset"
        : "cancelled_by_user";
    const deliveryEvent = input.source === "openclaw-ui-stop"
      ? "delivery_suppressed_by_user"
      : "delivery_suppressed_by_session_boundary";
    for (const row of rows) {
      const changed = db.prepare(`UPDATE tickets SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,
        failure_class=NULL,failure_message=?,response_ready_at=NULL,delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND status IN ('accepted','planned','running','waiting')`).run(reason, stamp, row.ticket_id);
      if (changed.changes !== 1) continue;
      cancelled.push(row.ticket_id);
      if (typeof row.workflow_id === "string" && row.workflow_id) workflowIds.push(row.workflow_id);
      addEvent(db, row.ticket_id, cancellationEvent, {
        source: input.source,
        previousStatus: row.status,
        previousRunId: row.run_id,
        sessionGeneration: nextGeneration,
        message: reason,
      }, stamp);
    }
    for (const item of pending) addEvent(db, item.ticket_id, deliveryEvent, {
      source: input.source,
      outboxId: Number(item.outbox_id),
      sessionGeneration: nextGeneration,
      message: reason,
    }, stamp);
    db.prepare("DELETE FROM ticket_outbox WHERE owner_session_key=? AND delivery_status='pending'").run(input.sessionKey);
    const assistantSuppressed = Number(db.prepare(
      "DELETE FROM cnx_assistant_delivery WHERE owner_session_key=? AND status='pending'",
    ).run(input.sessionKey).changes);
    db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=?
      WHERE ticket_id IN (SELECT ticket_id FROM tickets WHERE owner_session_key=?) AND state<>'cancelled'`)
      .run(reason, stamp, input.sessionKey);
    db.exec("COMMIT");
    return {
      ownerSessionKey: input.sessionKey,
      generation: nextGeneration,
      cancelled,
      workflowIds: [...new Set(workflowIds)],
      assistantSuppressed,
      outboxTags: pending.map((item) => `cogent-ticket-result-${String(item.ticket_id).replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 96)}`),
    };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function cancelSessionByKey(path: string, input: { sessionKey: string; message?: string; now?: Date; source?: string }) {
  return revokeSession(path, {
    sessionKey: input.sessionKey,
    message: input.message ?? "Cancelled by user",
    source: input.source ?? "openclaw-ui-stop",
    deleting: false,
    now: input.now,
  });
}

export function resetSessionByKey(path: string, input: { sessionKey: string; message?: string; now?: Date }) {
  return revokeSession(path, {
    sessionKey: input.sessionKey,
    message: input.message ?? "Owner session reset",
    source: "openclaw-session-reset",
    deleting: false,
    now: input.now,
  });
}

export function deleteSessionByKey(path: string, input: { sessionKey: string; message?: string; sessionId?: string; now?: Date }) {
  return revokeSession(path, {
    sessionKey: input.sessionKey,
    message: input.message ?? "Owner session deleted",
    source: "openclaw-session-delete",
    deleting: true,
    sessionId: input.sessionId,
    now: input.now,
  });
}

export function finalizeSessionDeletion(path: string, sessionKey: string, reason = "Owner session deleted", date = new Date()) {
  const db = openDb(path), stamp = date.toISOString();
  try {
    db.prepare(`UPDATE cnx_sessions SET state='deleted',updated_at=?,deleted_at=?,delete_reason=? WHERE session_key=?`)
      .run(stamp, stamp, reason.slice(0, 2000), sessionKey);
  } finally { db.close(); }
}

export function cancelSessionTickets(path: string, input: { runId: string; message?: string; now?: Date }) {
  const db = openDb(path);
  try {
    const owner = db.prepare(`SELECT owner_session_key FROM tickets WHERE run_id=?
      UNION ALL
      SELECT t.owner_session_key FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.active_run_id=?
      LIMIT 1`).get(input.runId, input.runId) as any;
    if (!owner?.owner_session_key) return {
      ownerSessionKey: null,
      generation: null,
      cancelled: [] as string[],
      workflowIds: [] as string[],
      assistantSuppressed: 0,
      outboxTags: [] as string[],
    };
    return cancelSessionByKey(path, { sessionKey: owner.owner_session_key, message: input.message, now: input.now });
  } finally { db.close(); }
}

export function disposeDirectRecoveryTicket(path: string, input: {
  ticketId: string;
  ownerSessionKey: string;
  ownerGeneration: number;
  message?: string;
  now?: Date;
}) {
  const db = openDb(path), stamp = (input.now ?? new Date()).toISOString();
  const reason = (input.message ?? "Direct recovery dispositioned").slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT owner_session_key,owner_generation,state FROM cnx_direct_recovery WHERE ticket_id=?`).get(input.ticketId) as any;
    if (!row) { db.exec("COMMIT"); return false; }
    if (row.owner_session_key !== input.ownerSessionKey || Number(row.owner_generation) !== input.ownerGeneration) {
      db.exec("COMMIT"); return false;
    }
    db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=? WHERE ticket_id=?`).run(reason, stamp, input.ticketId);
    db.exec("COMMIT");
    return true;
  } catch(error){ try{db.exec("ROLLBACK")}catch{}; throw error; } finally{db.close();}
}
