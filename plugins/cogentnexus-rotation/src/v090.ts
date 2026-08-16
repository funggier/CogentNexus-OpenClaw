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
  cogentRoot?: string;
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
};

type AssistantDeliveryTarget =
  | { kind: "direct"; ticketId: string; runId: string }
  | DeliveryTarget
  | { kind: "notice" };

type SessionAuthority = { state: "active" | "deleting" | "deleted"; generation: number };
type ActiveSynthetic = { childSessionKey: string; generation: number };

const PATCH = Symbol.for("cogentnexus.v090.ticket-patch");
const WRAP = Symbol.for("cogentnexus.v090.entry-wrap");
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
  `);
  ensureColumn(db, "cnx_direct_recovery", "owner_generation", "INTEGER NOT NULL DEFAULT 0");
  ensureColumn(db, "cnx_assistant_delivery", "owner_generation", "INTEGER NOT NULL DEFAULT 0");
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
  input: { sessionKey: string; message: string; source: string; deleting: boolean; now?: Date },
) {
  const db = openDb(path);
  const stamp = (input.now ?? new Date()).toISOString();
  const reason = input.message.slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const prior = sessionAuthorityFromDb(db, input.sessionKey);
    const nextGeneration = prior.generation + 1;
    db.prepare(`UPDATE cnx_sessions SET state=?,generation=?,updated_at=?,delete_reason=?
      WHERE session_key=?`).run(input.deleting ? "deleting" : "active", nextGeneration, stamp,
        input.deleting ? reason : null, input.sessionKey);
    const rows = db.prepare(`SELECT ticket_id,status,run_id,workflow_id FROM tickets
      WHERE owner_session_key=? AND status IN ('accepted','planned','running','waiting') ORDER BY created_at,ticket_id`)
      .all(input.sessionKey) as any[];
    const pending = db.prepare(`SELECT outbox_id,ticket_id FROM ticket_outbox
      WHERE owner_session_key=? AND delivery_status='pending' ORDER BY outbox_id`).all(input.sessionKey) as any[];
    const cancelled: string[] = [];
    const workflowIds: string[] = [];
    for (const row of rows) {
      const changed = db.prepare(`UPDATE tickets SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,
        failure_class=NULL,failure_message=?,response_ready_at=NULL,delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND status IN ('accepted','planned','running','waiting')`).run(reason, stamp, row.ticket_id);
      if (changed.changes !== 1) continue;
      cancelled.push(row.ticket_id);
      if (typeof row.workflow_id === "string" && row.workflow_id) workflowIds.push(row.workflow_id);
      addEvent(db, row.ticket_id, input.deleting ? "cancelled_by_session_delete" : "cancelled_by_user", {
        source: input.source,
        previousStatus: row.status,
        previousRunId: row.run_id,
        sessionGeneration: nextGeneration,
        message: reason,
      }, stamp);
    }
    for (const item of pending) addEvent(db, item.ticket_id, "delivery_suppressed_by_user", {
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

export function cancelSessionByKey(path: string, input: { sessionKey: string; message?: string; now?: Date }) {
  return revokeSession(path, {
    sessionKey: input.sessionKey,
    message: input.message ?? "Cancelled by user",
    source: "openclaw-ui-stop",
    deleting: false,
    now: input.now,
  });
}

export function deleteSessionByKey(path: string, input: { sessionKey: string; message?: string; now?: Date }) {
  return revokeSession(path, {
    sessionKey: input.sessionKey,
    message: input.message ?? "Owner session deleted",
    source: "openclaw-session-delete",
    deleting: true,
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

function suppressWorkflowCompletion(workspace: string, workflowId: string, reason: string) {
  const path = resolve(workspace, ".cogent", "workflows", workflowId, "completion.json");
  if (!existsSync(path)) return;
  try {
    const value = JSON.parse(readFileSync(path, "utf8"));
    value.deliveryStatus = "delivered";
    value.deliveredAt = now();
    value.suppressedBy = "session-authority";
    value.suppressionReason = reason;
    delete value.scheduledAt;
    delete value.deliveryRunId;
    const tmp = `${path}.${process.pid}.v090-suppress.tmp`;
    writeFileSync(tmp, `${JSON.stringify(value, null, 2)}\n`);
    renameSync(tmp, path);
  } catch {}
}

function suppressSessionWorkflowCompletions(workspace: string, sessionKey: string, reason: string) {
  const root = resolve(workspace, ".cogent", "workflows"), tags: string[] = [];
  if (!existsSync(root)) return tags;
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const path = resolve(root, entry.name, "completion.json");
    if (!existsSync(path)) continue;
    try {
      const value = JSON.parse(readFileSync(path, "utf8"));
      if (value?.ownerSessionKey !== sessionKey || value?.deliveryStatus !== "pending") continue;
      const revision = Number(value.stateRevision ?? 0);
      tags.push(`cogent-workflow-result-${String(value.taskId ?? entry.name).replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 96)}-${Math.trunc(revision)}`);
      value.deliveryStatus = "delivered";
      value.deliveredAt = now();
      value.suppressedBy = "session-authority";
      value.suppressionReason = reason;
      delete value.scheduledAt;
      delete value.deliveryRunId;
      const tmp = `${path}.${process.pid}.v090-session-suppress.tmp`;
      writeFileSync(tmp, `${JSON.stringify(value, null, 2)}\n`);
      renameSync(tmp, path);
    } catch {}
  }
  return tags;
}

function cancelBoundWorkflows(workspace: string, workflowIds: string[], reason: string, cfg: Cfg) {
  const runtime = resolve(workspace, "skills", "cogentnexus", "scripts", "workflow.py");
  const results: Array<{ workflowId: string; ok: boolean; error?: string }> = [];
  for (const workflowId of workflowIds) {
    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u.test(workflowId)) {
      results.push({ workflowId, ok: false, error: "invalid workflow id" });
      continue;
    }
    const run = spawnSync(cfg.pythonCommand ?? "python", [runtime, "--root", workspace, "cancel", workflowId, "--reason", reason], {
      encoding: "utf8", windowsHide: true, timeout: 30_000,
    });
    const ok = !run.error && run.status === 0;
    results.push({ workflowId, ok, error: ok ? undefined : (run.error?.message ?? run.stderr ?? run.stdout ?? "workflow cancellation failed").trim().slice(0, 2000) });
    if (ok) suppressWorkflowCompletion(workspace, workflowId, reason);
  }
  return results;
}

export function isExplicitUserCancellation(message?: string) {
  if (!message) return false;
  const value = message.trim();
  if (value === "agent run aborted") return true;
  if (/^This operation was aborted(?:\s*\|\s*\d+)?$/u.test(value)) return true;
  return /(?:reply operation )?aborted by user|user (?:cancelled|canceled)|(?:cancelled|canceled) by user|explicit user (?:stop|abort|cancel)/iu.test(value);
}

export function markDirectRecovery(path: string, input: { runId: string; mode: "resume" | "redeliver"; message?: string; now?: Date }) {
  if (isExplicitUserCancellation(input.message)) {
    cancelSessionTickets(path, { runId: input.runId, message: input.message, now: input.now });
    return false;
  }
  const db = openDb(path), stamp = (input.now ?? new Date()).toISOString(), message = (input.message ?? "Direct run interrupted").slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT ticket_id,owner_session_key FROM tickets
      WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1`).get(input.runId) as any;
    if (!row || !queueRecovery(db, row.ticket_id, row.owner_session_key, input.mode, message, stamp)) {
      db.exec("COMMIT");
      return false;
    }
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,
      response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=? WHERE ticket_id=?`)
      .run(message, message, stamp, row.ticket_id);
    addEvent(db, row.ticket_id, input.mode === "redeliver" ? "direct_redelivery_pending" : "direct_retry_pending", { runId: input.runId, message }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function markSession(path: string, sessionKey: string, message: string) {
  const db = openDb(path), stamp = now();
  try {
    db.exec("BEGIN IMMEDIATE");
    const authority = sessionAuthorityFromDb(db, sessionKey);
    if (authority.state !== "active") { db.exec("COMMIT"); return false; }
    const row = db.prepare(`SELECT ticket_id,run_id FROM tickets WHERE owner_session_key=? AND status='accepted'
      AND workflow_eligible=0 AND response_ready_at IS NULL ORDER BY created_at DESC LIMIT 1`).get(sessionKey) as any;
    if (!row || !queueRecovery(db, row.ticket_id, sessionKey, "resume", message, stamp)) { db.exec("COMMIT"); return false; }
    db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=?")
      .run(message, stamp, row.ticket_id);
    addEvent(db, row.ticket_id, "direct_retry_pending", { runId: row.run_id, sessionKey, message }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function patchTicketStore() {
  const p = TicketStore.prototype as any;
  if (p[PATCH]) return;
  Object.defineProperty(p, PATCH, { value: true });
  const accept = TicketStore.prototype.accept;
  const finalize = TicketStore.prototype.finalizeDirectRun;
  const failDelivery = TicketStore.prototype.failDirectDelivery;

  TicketStore.prototype.accept = function(input: Parameters<TicketStore["accept"]>[0]) {
    const db = openDb(this.databasePath);
    try {
      const authority = sessionAuthorityFromDb(db, input.ownerSessionKey);
      if (authority.state !== "active") throw new Error(`CogentNexus session is ${authority.state}: ${input.ownerSessionKey}`);
    } finally { db.close(); }
    return accept.call(this, input);
  };

  TicketStore.prototype.finalizeDirectRun = function(input: Parameters<TicketStore["finalizeDirectRun"]>[0]) {
    if (!input.success && isExplicitUserCancellation(input.message)) {
      cancelSessionTickets(this.databasePath, { runId: input.runId, message: input.message, now: input.now });
      return "unchanged";
    }
    if (!input.success && input.interrupted) {
      return markDirectRecovery(this.databasePath, { runId: input.runId, mode: "resume", message: input.message, now: input.now }) ? "waiting" : "unchanged";
    }
    return finalize.call(this, input);
  };

  TicketStore.prototype.failDirectDelivery = function(input: Parameters<TicketStore["failDirectDelivery"]>[0]) {
    return markDirectRecovery(this.databasePath, { runId: input.runId, mode: "redeliver", message: input.message, now: input.now })
      ? "waiting" : failDelivery.call(this, input);
  };

  TicketStore.prototype.recoverUndeliveredDirect = function(input: Parameters<TicketStore["recoverUndeliveredDirect"]>[0] = {}) {
    const db = openDb(this.databasePath), n = input.now ?? new Date();
    const cutoff = new Date(n.getTime() - Math.max(1000, input.olderThanMs ?? 120_000)).toISOString(), stamp = n.toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows = db.prepare(`SELECT ticket_id,run_id,owner_session_key FROM tickets WHERE status='accepted'
        AND workflow_eligible=0 AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL
        AND response_ready_at<=? ORDER BY response_ready_at LIMIT ?`).all(cutoff, Math.max(1, Math.min(input.limit ?? 100, 1000))) as any[];
      for (const row of rows) {
        const message = "Direct response delivery was not confirmed before deadline";
        if (!queueRecovery(db, row.ticket_id, row.owner_session_key, "redeliver", message, stamp)) continue;
        db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,response_ready_at=NULL,updated_at=? WHERE ticket_id=?`)
          .run(message, message, stamp, row.ticket_id);
        addEvent(db, row.ticket_id, "direct_redelivery_timeout", { runId: row.run_id, cutoff }, stamp);
      }
      db.exec("COMMIT");
      return [];
    } catch (error) {
      try { db.exec("ROLLBACK"); } catch {}
      throw error;
    } finally { db.close(); }
  };

  TicketStore.prototype.promotePendingDirectForSession = function(input: Parameters<TicketStore["promotePendingDirectForSession"]>[0]) {
    markSession(this.databasePath, input.sessionKey, input.reason ?? "Post-compaction continuation");
    return undefined;
  };
}

export const isDashboardSession = (key: string) => /^agent:[^:]+:dashboard:/u.test(key);
export const directRecoveryBackoffMs = (attempt: number) => [5, 15, 30, 60, 120, 300][Math.max(0, Math.min(5, attempt - 1))] * 1000;

function resetCompletions(workspace: string) {
  const root = resolve(workspace, ".cogent", "workflows");
  if (!existsSync(root)) return 0;
  let count = 0;
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const path = join(root, entry.name, "completion.json");
    if (!existsSync(path)) continue;
    try {
      const value = JSON.parse(readFileSync(path, "utf8"));
      if (value?.deliveryStatus !== "pending" || (!value.scheduledAt && !value.deliveryRunId)) continue;
      delete value.scheduledAt;
      delete value.deliveryRunId;
      const tmp = `${path}.${process.pid}.v090.tmp`;
      writeFileSync(tmp, `${JSON.stringify(value, null, 2)}\n`);
      renameSync(tmp, path);
      count++;
    } catch {}
  }
  return count;
}

export function prepareV090RecoveryState(workspace: string, cfg: Cfg = {}) {
  const path = dbPath(cfg, workspace), db = openDb(path), stamp = now();
  let reopened = 0, outboxReset = 0, cancelledLegacy = 0, cancelledOutboxSuppressed = 0, terminalRecoverySuppressed = 0;
  try {
    db.exec("BEGIN IMMEDIATE");
    registerExistingSessions(db, stamp);
    db.prepare("UPDATE tickets SET failure_class=NULL WHERE status='cancelled' AND failure_class IS NOT NULL").run();
    cancelledOutboxSuppressed = Number(db.prepare(`DELETE FROM ticket_outbox WHERE delivery_status='pending'
      AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status='cancelled')`).run().changes);
    db.prepare(`DELETE FROM cnx_assistant_delivery WHERE status='pending' AND owner_session_key IN
      (SELECT session_key FROM cnx_sessions WHERE state<>'active')`).run();
    terminalRecoverySuppressed = Number(db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,
      next_attempt_at=NULL,last_error=COALESCE(last_error,'terminal ticket fence'),updated_at=? WHERE state<>'cancelled'
      AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status IN ('completed','failed','cancelled'))`).run(stamp).changes);
    const rows = db.prepare(`SELECT ticket_id,prompt,status,workflow_eligible,failure_class,failure_message,owner_session_key
      FROM tickets WHERE status IN ('waiting','failed') AND workflow_id IS NULL AND
      ((workflow_eligible=1 AND failure_class='interrupted') OR
       (status='failed' AND workflow_eligible=0 AND failure_class='permanent' AND failure_message='Reply operation aborted by user'))
      ORDER BY created_at`).all() as any[];
    for (const row of rows) {
      const legacyAbort = row.failure_class === "permanent" && row.failure_message === "Reply operation aborted by user";
      if (legacyAbort) {
        db.prepare(`UPDATE tickets SET status='cancelled',workflow_eligible=0,worker_id=NULL,lease_token=NULL,
          lease_expires_at=NULL,heartbeat_at=NULL,failure_class=NULL,updated_at=? WHERE ticket_id=?`).run(stamp, row.ticket_id);
        db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id);
        db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,
          last_error='legacy user abort migrated to cancelled',updated_at=? WHERE ticket_id=?`).run(stamp, row.ticket_id);
        addEvent(db, row.ticket_id, "v090_user_abort_cancelled", { previousStatus: row.status }, stamp);
        cancelledLegacy++;
        continue;
      }
      if (classifyDurableRequest(row.prompt, cfg.admissionMinimumScore ?? 5).lane !== "direct") continue;
      const authority = sessionAuthorityFromDb(db, row.owner_session_key);
      if (authority.state !== "active") continue;
      db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id);
      const changed = db.prepare(`UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,
        lease_expires_at=NULL,heartbeat_at=NULL,response_ready_at=NULL,delivery_confirmed_at=NULL,delivery_last_error=NULL,
        result_json=NULL,failure_class='interrupted',updated_at=? WHERE ticket_id=? AND workflow_id IS NULL`).run(stamp, row.ticket_id);
      if (changed.changes && queueRecovery(db, row.ticket_id, row.owner_session_key, "resume", `v0.9.0 reopened ${row.status} Direct Ticket`, stamp)) {
        addEvent(db, row.ticket_id, "v090_direct_recovery_reopened", { previousStatus: row.status }, stamp);
        reopened++;
      }
    }
    outboxReset = Number(db.prepare(`UPDATE ticket_outbox SET scheduled_at=NULL,delivery_run_id=NULL
      WHERE delivery_status='pending' AND (scheduled_at IS NOT NULL OR delivery_run_id IS NOT NULL)`).run().changes);
    db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,updated_at=?
      WHERE state='running' AND ticket_id IN (SELECT t.ticket_id FROM tickets t JOIN cnx_sessions s
        ON s.session_key=t.owner_session_key WHERE s.state='active' AND s.generation=cnx_direct_recovery.owner_generation)`).run(stamp, stamp);
    db.exec("COMMIT");
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
  return { databasePath: path, reopened, cancelledLegacy, cancelledOutboxSuppressed, terminalRecoverySuppressed,
    outboxReset, workflowDeliveryReset: resetCompletions(workspace) };
}

function resetStale(path: string, cfg: Cfg) {
  const db = openDb(path);
  try {
    const cutoff = new Date(Date.now() - Math.max(15 * 60_000, Math.min((cfg.timeoutSeconds ?? 3600) * 1000 + 60_000, 4 * 60 * 60_000))).toISOString();
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,
      last_error=COALESCE(last_error,'stale Direct recovery reset'),updated_at=? WHERE state='running' AND updated_at<=?
      AND ticket_id IN (SELECT t.ticket_id FROM tickets t JOIN cnx_sessions s ON s.session_key=t.owner_session_key
        WHERE s.state='active' AND s.generation=cnx_direct_recovery.owner_generation)`).run(now(), now(), cutoff).changes);
  } finally { db.close(); }
}

function due(path: string): Recovery | undefined {
  const db = openDb(path);
  try {
    return db.prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count,r.owner_generation
      FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      WHERE r.state='pending' AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND s.state='active' AND s.generation=r.owner_generation
        AND (r.next_attempt_at IS NULL OR r.next_attempt_at<=?)
      ORDER BY COALESCE(r.next_attempt_at,r.created_at) LIMIT 1`).get(now()) as Recovery | undefined;
  } finally { db.close(); }
}

function claim(path: string, recovery: Recovery, runId: string) {
  const db = openDb(path);
  try {
    return db.prepare(`UPDATE cnx_direct_recovery SET state='running',attempt_count=attempt_count+1,active_run_id=?,
      next_attempt_at=NULL,last_error=NULL,updated_at=? WHERE ticket_id=? AND state='pending' AND owner_generation=?
      AND EXISTS (SELECT 1 FROM cnx_sessions WHERE session_key=? AND state='active' AND generation=?)`)
      .run(runId, now(), recovery.ticket_id, recovery.owner_generation, recovery.owner_session_key, recovery.owner_generation).changes === 1;
  } finally { db.close(); }
}

function bindRun(path: string, ticketId: string, oldRun: string, newRun: string) {
  if (oldRun === newRun) return;
  const db = openDb(path);
  try { db.prepare(`UPDATE cnx_direct_recovery SET active_run_id=?,updated_at=? WHERE ticket_id=? AND state='running' AND active_run_id=?`)
    .run(newRun, now(), ticketId, oldRun); }
  finally { db.close(); }
}

function retry(path: string, recovery: Recovery, runId: string, message: string) {
  const db = openDb(path), stamp = new Date();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT attempt_count FROM cnx_direct_recovery WHERE ticket_id=? AND state='running'
      AND active_run_id=? AND owner_generation=?`).get(recovery.ticket_id, runId, recovery.owner_generation) as any;
    if (!row) { db.exec("COMMIT"); return; }
    const authority = sessionAuthorityFromDb(db, recovery.owner_session_key);
    if (authority.state !== "active" || authority.generation !== recovery.owner_generation) {
      db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=? WHERE ticket_id=?`)
        .run("session authority superseded", stamp.toISOString(), recovery.ticket_id);
      db.exec("COMMIT");
      return;
    }
    const next = new Date(stamp.getTime() + directRecoveryBackoffMs(Number(row.attempt_count))).toISOString();
    db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,last_error=?,updated_at=? WHERE ticket_id=?`)
      .run(next, message.slice(0, 2000), stamp.toISOString(), recovery.ticket_id);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=?
      WHERE ticket_id=? AND status='accepted'`).run(message.slice(0, 2000), message.slice(0, 2000), stamp.toISOString(), recovery.ticket_id);
    addEvent(db, recovery.ticket_id, "direct_recovery_retry", { runId, message, nextAttemptAt: next, attempt: Number(row.attempt_count) }, stamp.toISOString());
    db.exec("COMMIT");
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function roleText(message: any) {
  const content = message?.content;
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";
  return content.map((part: any) => {
    if (typeof part === "string") return part;
    if (!part || typeof part !== "object") return "";
    return typeof part.text === "string" ? part.text : typeof part.content === "string" ? part.content : "";
  }).filter(Boolean).join("\n").trim();
}

function isInternalControlText(text: string) {
  return /#cogent-direct\b|\[CogentNexus (?:Delivery|Continuation|Internal|Direct Recovery):|\[CogentNexus Internal /iu.test(text);
}

export function boundedOwnerContext(messages: unknown[], maxChars = 12_000) {
  const lines: string[] = [];
  for (const raw of messages) {
    const message = raw as any;
    if (!["user", "assistant"].includes(message?.role)) continue;
    const text = roleText(message);
    if (!text || isInternalControlText(text)) continue;
    lines.push(`${String(message.role).toUpperCase()}:\n${text}`);
  }
  let value = lines.join("\n\n");
  if (value.length > maxChars) value = value.slice(value.length - maxChars);
  return value;
}

function lastAssistantText(messages: unknown[]) {
  for (let index = messages.length - 1; index >= 0; index--) {
    const message = messages[index] as any;
    if (message?.role !== "assistant") continue;
    const text = roleText(message);
    if (text) return text;
  }
  return undefined;
}

function agentIdFromSession(sessionKey: string, fallback = "main") {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1] ?? fallback;
}

function hiddenSessionKey(ownerSessionKey: string, purpose: string, generation: number, cfg: Cfg) {
  const agentId = agentIdFromSession(ownerSessionKey, cfg.agentId ?? "main");
  const ownerHash = createHash("sha256").update(ownerSessionKey).digest("hex").slice(0, 12);
  const safePurpose = purpose.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 42);
  return `agent:${agentId}:subagent:cnx-${safePurpose}-${ownerHash}-g${generation}-${randomUUID().slice(0, 8)}`;
}

function recoveryPrompt(recovery: Recovery, context: string) {
  const instruction = recovery.mode === "redeliver"
    ? "Reconstruct only the compact final response. Do not repeat external side effects."
    : "Resume the interrupted request from the latest committed state. Do not repeat completed side effects.";
  return [
    "[CogentNexus Internal Direct Recovery]",
    "This is an internal recovery worker session, not a new user instruction.",
    instruction,
    "Preserve the original user intent. Inspect durable state and existing artifacts when useful.",
    "Return only the user-facing assistant response that should be delivered to the owner session.",
    "",
    "Original committed request:", recovery.prompt,
    "",
    "Bounded read-only owner-session context:", context || "(no usable recent context)",
  ].join("\n");
}

function compatibilityPrompt(input: Turn, context: string) {
  return [
    "[CogentNexus Internal Delivery Worker]",
    "This is an internal control-plane task. It is not a new user instruction.",
    "Produce only the compact assistant-facing result that should be shown to the owner.",
    "Do not repeat external side effects and do not claim success without committed evidence.",
    "",
    input.message,
    "",
    "Bounded read-only owner-session context:", context || "(no usable recent context)",
  ].join("\n");
}

function targetId(target: DeliveryTarget | undefined, input: Turn) {
  if (target?.kind === "ticket") return `ticket:${target.outboxId}`;
  if (target?.kind === "workflow") return `workflow:${target.taskId}:${target.stateRevision}`;
  return `turn:${createHash("sha256").update(`${input.sessionKey}\0${input.tag}`).digest("hex").slice(0, 32)}`;
}

function hostDeliveryScript(workspace: string) {
  return resolve(workspace, "skills", "cogentnexus", "scripts", "host_delivery.py");
}

function kickHostDelivery(workspace: string, cfg: Cfg) {
  const script = hostDeliveryScript(workspace);
  if (!existsSync(script)) return false;
  const root = resolve(cfg.cogentRoot ?? join(workspace, ".cogent"));
  try {
    const child = spawn(cfg.pythonCommand ?? "python", [script, "--root", root, "flush"], {
      detached: true, stdio: "ignore", windowsHide: true,
    });
    child.unref();
    return true;
  } catch { return false; }
}

export function queueAssistantDelivery(path: string, input: {
  ticketId?: string;
  ownerSessionKey: string;
  ownerGeneration: number;
  kind: string;
  text: string;
  target: AssistantDeliveryTarget;
  idempotencyKey: string;
  now?: Date;
}) {
  const db = openDb(path), stamp = (input.now ?? new Date()).toISOString();
  try {
    const authority = sessionAuthorityFromDb(db, input.ownerSessionKey);
    if (authority.state !== "active" || authority.generation !== input.ownerGeneration) return false;
    return db.prepare(`INSERT OR IGNORE INTO cnx_assistant_delivery(
      ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
      attempt_count,last_error,created_at,updated_at) VALUES (?,?,?,?,?,?,?,'pending',0,NULL,?,?)`)
      .run(input.ticketId ?? null, input.ownerSessionKey, input.ownerGeneration, input.kind, input.text,
        JSON.stringify(input.target), input.idempotencyKey, stamp, stamp).changes === 1;
  } finally { db.close(); }
}

function markResponseReady(path: string, recovery: Recovery, runId: string, text: string) {
  const db = openDb(path), stamp = now();
  try {
    db.exec("BEGIN IMMEDIATE");
    const authority = sessionAuthorityFromDb(db, recovery.owner_session_key);
    const row = db.prepare(`SELECT t.status,t.workflow_eligible,t.workflow_id,r.state,r.active_run_id,r.owner_generation
      FROM tickets t JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id WHERE t.ticket_id=?`).get(recovery.ticket_id) as any;
    if (!row || authority.state !== "active" || authority.generation !== recovery.owner_generation ||
        row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.workflow_id || row.state !== "running" ||
        row.active_run_id !== runId || Number(row.owner_generation) !== recovery.owner_generation) {
      db.exec("COMMIT");
      return false;
    }
    const idempotencyKey = `cnx-direct-result:${recovery.ticket_id}:g${recovery.owner_generation}`;
    db.prepare(`INSERT OR IGNORE INTO cnx_assistant_delivery(
      ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
      attempt_count,last_error,created_at,updated_at) VALUES (?,?,?,'direct_result',?,?,?,'pending',0,NULL,?,?)`)
      .run(recovery.ticket_id, recovery.owner_session_key, recovery.owner_generation, text,
        JSON.stringify({ kind: "direct", ticketId: recovery.ticket_id, runId }), idempotencyKey, stamp, stamp);
    db.prepare(`UPDATE tickets SET result_json=?,response_ready_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=?`)
      .run(JSON.stringify({ directRecovery: true, runId, deliveryPending: true }), stamp, stamp, recovery.ticket_id);
    db.prepare(`UPDATE cnx_direct_recovery SET state='awaiting_delivery',active_run_id=NULL,next_attempt_at=NULL,
      last_error=NULL,updated_at=? WHERE ticket_id=?`).run(stamp, recovery.ticket_id);
    addEvent(db, recovery.ticket_id, "direct_recovery_response_ready", { runId, deliveryMode: "host-chat-inject", ownerGeneration: recovery.owner_generation }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function trackSynthetic(ownerSessionKey: string, runId: string, childSessionKey: string, generation: number) {
  const runs = activeSynthetic.get(ownerSessionKey) ?? new Map<string, ActiveSynthetic>();
  runs.set(runId, { childSessionKey, generation });
  activeSynthetic.set(ownerSessionKey, runs);
}

function untrackSynthetic(ownerSessionKey: string, runId: string) {
  const runs = activeSynthetic.get(ownerSessionKey);
  if (!runs) return;
  runs.delete(runId);
  if (runs.size === 0) activeSynthetic.delete(ownerSessionKey);
}

function cnxOwnedTask(task: any) {
  return task?.label === "plugin:cogentnexus-rotation"
    || String(task?.runId ?? "").startsWith("cnx-")
    || String(task?.sourceId ?? "").startsWith("cnx-")
    || String(task?.runId ?? "").startsWith("cogent-");
}

async function cancelTasksInSession(api: any, sessionKey: string) {
  const taskRuns = api.runtime?.tasks?.runs;
  if (!taskRuns?.bindSession) return { scanned: 0, cancelled: 0, failed: 0 };
  const agentId = agentIdFromSession(sessionKey);
  let bound: any;
  try { bound = taskRuns.bindSession({ sessionKey, agentId }); }
  catch { return { scanned: 0, cancelled: 0, failed: 1 }; }
  let scanned = 0, cancelled = 0, failed = 0;
  for (const task of (bound.list?.() ?? []) as any[]) {
    if (!task?.id || !["queued", "running"].includes(String(task.status ?? "")) || !cnxOwnedTask(task)) continue;
    scanned++;
    try {
      const result = await bound.cancel({ taskId: task.id, cfg: {} });
      if (result?.cancelled) cancelled++;
      else failed++;
    } catch { failed++; }
  }
  return { scanned, cancelled, failed };
}

async function cancelTrackedSynthetic(api: any, ownerSessionKey: string) {
  const runs = [...(activeSynthetic.get(ownerSessionKey)?.entries() ?? [])];
  activeSynthetic.delete(ownerSessionKey);
  for (const [, item] of runs) {
    try { await cancelTasksInSession(api, item.childSessionKey); } catch {}
    try { await api.runtime?.subagent?.deleteSession?.({ sessionKey: item.childSessionKey, deleteTranscript: true }); } catch {}
  }
  try { await cancelTasksInSession(api, ownerSessionKey); } catch {}
  return runs.length;
}

export async function launchRecovery(api: any, path: string, workspace: string, recovery: Recovery, cfg: Cfg) {
  const attempt = Number(recovery.attempt_count) + 1;
  const planned = `cnx-direct-${recovery.ticket_id.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 48)}-${attempt}-g${recovery.owner_generation}`;
  if (!claim(path, recovery, planned)) return;
  const childSessionKey = hiddenSessionKey(recovery.owner_session_key, `recovery-${recovery.ticket_id}`, recovery.owner_generation, cfg);
  trackSynthetic(recovery.owner_session_key, planned, childSessionKey, recovery.owner_generation);
  let runId = planned;
  try {
    if (!sessionIsCurrent(path, recovery.owner_session_key, recovery.owner_generation)) return;
    const owner = await api.runtime.subagent.getSessionMessages({ sessionKey: recovery.owner_session_key, limit: 24 });
    const context = boundedOwnerContext(owner.messages ?? []);
    const launched = await api.runtime.subagent.run({
      sessionKey: childSessionKey,
      message: recoveryPrompt(recovery, context),
      deliver: false,
      lightContext: true,
      idempotencyKey: planned,
    });
    runId = launched.runId;
    untrackSynthetic(recovery.owner_session_key, planned);
    trackSynthetic(recovery.owner_session_key, runId, childSessionKey, recovery.owner_generation);
    bindRun(path, recovery.ticket_id, planned, runId);
    const waited = await api.runtime.subagent.waitForRun({
      runId,
      timeoutMs: Math.max(60_000, Math.min((cfg.timeoutSeconds ?? 3600) * 1000, 3_600_000)),
    });
    if (!sessionIsCurrent(path, recovery.owner_session_key, recovery.owner_generation)) return;
    if (waited.status === "timeout") { retry(path, recovery, runId, "Direct recovery run timed out"); return; }
    if (waited.status !== "ok") { retry(path, recovery, runId, waited.error ?? "Direct recovery run failed"); return; }
    const child = await api.runtime.subagent.getSessionMessages({ sessionKey: childSessionKey, limit: 24 });
    const text = lastAssistantText(child.messages ?? []);
    if (!text) { retry(path, recovery, runId, "Direct recovery produced no visible assistant output"); return; }
    if (markResponseReady(path, recovery, runId, text)) kickHostDelivery(workspace, cfg);
  } catch (error) {
    retry(path, recovery, runId, error instanceof Error ? error.message : String(error));
  } finally {
    untrackSynthetic(recovery.owner_session_key, runId);
    untrackSynthetic(recovery.owner_session_key, planned);
    try { await api.runtime.subagent.deleteSession({ sessionKey: childSessionKey, deleteTranscript: true }); } catch {}
  }
}

function recoveryService(api: any, cfg: Cfg) {
  let timer: ReturnType<typeof setInterval> | undefined, active = false;
  return {
    id: "cogentnexus-direct-recovery-v090",
    start: async (ctx: any) => {
      const workspace = resolve(cfg.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
      const path = dbPath(cfg, workspace);
      const tick = async () => {
        if (active) return;
        active = true;
        try {
          resetStale(path, cfg);
          kickHostDelivery(workspace, cfg);
          const recovery = due(path);
          if (recovery) void launchRecovery(api, path, workspace, recovery, cfg);
        } catch (error) {
          api.logger.warn(`CogentNexus Direct recovery scan failed: ${error instanceof Error ? error.message : String(error)}`);
        } finally { active = false; }
      };
      await tick();
      timer = setInterval(() => { void tick(); }, Math.max(1000, Math.min(cfg.ticketRecoveryPollMs ?? 5000, 30_000)));
      timer.unref?.();
    },
    stop: async () => { if (timer) clearInterval(timer); timer = undefined; },
  };
}

export async function executeCompatibilityWake(api: any, cfg: Cfg, input: Turn) {
  const workspace = resolve(cfg.workspaceDir ?? process.cwd()), path = dbPath(cfg, workspace);
  const target = parseDeliveryMarker(input.message), store = new TicketStore(path);
  const authority = sessionAuthority(path, input.sessionKey);
  if (authority.state !== "active") return { queued: false, suppressed: true, reason: "session not active" };

  if (/reached terminal status (?:failed|blocked|cancelled)\./iu.test(input.message)) {
    if (target) settleDeliveryTarget({ workspaceDir: workspace, store, target, success: true });
    return { queued: false, suppressed: true, reason: "terminal non-success is durable and silent" };
  }

  const childSessionKey = hiddenSessionKey(input.sessionKey, `delivery-${input.tag}`, authority.generation, cfg);
  const planned = `cnx-hidden-${createHash("sha256").update(`${input.sessionKey}\0${input.tag}\0${authority.generation}`).digest("hex").slice(0, 40)}`;
  trackSynthetic(input.sessionKey, planned, childSessionKey, authority.generation);
  let runId = planned;
  try {
    const owner = await api.runtime.subagent.getSessionMessages({ sessionKey: input.sessionKey, limit: 24 });
    const context = boundedOwnerContext(owner.messages ?? []);
    const run = await api.runtime.subagent.run({
      sessionKey: childSessionKey,
      message: compatibilityPrompt(input, context),
      deliver: false,
      lightContext: true,
      idempotencyKey: planned,
    });
    runId = run.runId;
    untrackSynthetic(input.sessionKey, planned);
    trackSynthetic(input.sessionKey, runId, childSessionKey, authority.generation);
    const waited = await api.runtime.subagent.waitForRun({
      runId,
      timeoutMs: Math.max(60_000, Math.min((cfg.timeoutSeconds ?? 3600) * 1000, 3_600_000)),
    });
    if (!sessionIsCurrent(path, input.sessionKey, authority.generation)) return { waited, queued: false, suppressed: true };
    if (waited.status !== "ok") {
      const error = waited.status === "timeout" ? "Compatibility delivery worker timed out" : waited.error ?? "Compatibility delivery worker failed";
      if (target) settleDeliveryTarget({ workspaceDir: workspace, store, target, success: false, error });
      return { waited, queued: false };
    }
    const child = await api.runtime.subagent.getSessionMessages({ sessionKey: childSessionKey, limit: 24 });
    const text = lastAssistantText(child.messages ?? []);
    if (!text) {
      const error = "Compatibility delivery worker produced no visible assistant output";
      if (target) settleDeliveryTarget({ workspaceDir: workspace, store, target, success: false, error });
      return { waited: { status: "error", error }, queued: false };
    }
    const id = targetId(target, input);
    const queued = queueAssistantDelivery(path, {
      ownerSessionKey: input.sessionKey,
      ownerGeneration: authority.generation,
      kind: "compatibility_result",
      text,
      target: target ?? { kind: "notice" },
      idempotencyKey: `cnx-delivery:${createHash("sha256").update(input.sessionKey).digest("hex").slice(0, 16)}:${id}:g${authority.generation}`,
    });
    if (queued) kickHostDelivery(workspace, cfg);
    return { waited, queued };
  } catch (error) {
    if (target) settleDeliveryTarget({ workspaceDir: workspace, store, target, success: false, error: error instanceof Error ? error.message : String(error) });
    api.logger.warn(`CogentNexus compatibility wake failed for ${input.tag}: ${error instanceof Error ? error.message : String(error)}`);
    throw error;
  } finally {
    untrackSynthetic(input.sessionKey, runId);
    untrackSynthetic(input.sessionKey, planned);
    try { await api.runtime.subagent.deleteSession({ sessionKey: childSessionKey, deleteTranscript: true }); } catch {}
  }
}

function compatWorkflow(api: any, cfg: Cfg) {
  const timers = new Map<string, ReturnType<typeof setTimeout>>();
  const key = (sessionKey: string, tag: string) => `${sessionKey}\0${tag}`;
  const unschedule = async (input: { sessionKey: string; tag: string }) => {
    const id = key(input.sessionKey, input.tag), timer = timers.get(id);
    if (timer) { clearTimeout(timer); timers.delete(id); }
    return { removed: timer ? 1 : 0, failed: 0 };
  };
  const cancelSessionTimers = (sessionKey: string) => {
    let removed = 0;
    for (const [id, timer] of [...timers]) {
      if (!id.startsWith(`${sessionKey}\0`)) continue;
      clearTimeout(timer); timers.delete(id); removed++;
    }
    return removed;
  };
  const schedule = async (input: Turn) => {
    await unschedule(input);
    const path = dbPath(cfg, resolve(cfg.workspaceDir ?? process.cwd()));
    const authority = sessionAuthority(path, input.sessionKey);
    if (authority.state !== "active") return { scheduled: false, compatibilityMode: "session-suppressed" };
    if (input.tag.startsWith("cogent-resume-") || input.tag.startsWith("cogent-post-compact-")) {
      markSession(path, input.sessionKey, input.tag.startsWith("cogent-post-compact-") ? "Post-compaction continuation" : "Interrupted Direct continuation");
      return { scheduled: true, compatibilityMode: "direct-recovery" };
    }
    const id = key(input.sessionKey, input.tag), timer = setTimeout(() => {
      timers.delete(id);
      void executeCompatibilityWake(api, cfg, input).catch(() => {});
    }, Math.max(0, input.delayMs ?? 0));
    timer.unref?.(); timers.set(id, timer);
    return { scheduled: true, compatibilityMode: "hidden-worker-host-delivery" };
  };
  return { unscheduleSessionTurnsByTag: unschedule, scheduleSessionTurn: schedule, cancelSessionTimers };
}

function activeWorkflowForSession(workspace: string, requestHash: string, ownerSessionKey: string) {
  const base = resolve(workspace, ".cogent", "workflows");
  if (!existsSync(base)) return undefined;
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    try {
      const flowDir = resolve(base, entry.name);
      const manifest = JSON.parse(readFileSync(resolve(flowDir, "manifest.json"), "utf8"));
      const state = JSON.parse(readFileSync(resolve(flowDir, "state.json"), "utf8"));
      const owner = JSON.parse(readFileSync(resolve(flowDir, "owner.json"), "utf8"));
      if (manifest?.admission?.requestHash === requestHash && owner?.ownerSessionKey === ownerSessionKey
          && !["completed", "blocked", "failed", "cancelled"].includes(state?.status)) {
        return { taskId: entry.name, status: state.status, controllerPid: state.controllerPid };
      }
    } catch {}
  }
  return undefined;
}

const artifactPattern = /(?:^|[\s`"'(])([\w./\\-]+\.(?:md|csv|json|ya?ml|txt|py|js|mjs|cjs|ts|tsx|jsx|html|css|sql|mq[45]|mqh|xml|toml|ini|svg))(?![\w.])/giu;
function requestedWorkspaceWrites(prompt: string) {
  const found = [...prompt.matchAll(artifactPattern)].map((match) => match[1].replace(/\\/g, "/"));
  return [...new Set(found)].filter((path) => !path.startsWith("/") && !/^[A-Za-z]:/u.test(path) && !path.split("/").includes(".."));
}
function resourceKey(workspace: string, value: string) {
  const key = resolve(workspace, value);
  return process.platform === "win32" ? key.toLowerCase() : key;
}
function activeResourceClaims(workspace: string) {
  const claims = new Map<string, { taskId: string; ownerSessionKey?: string }>();
  const base = resolve(workspace, ".cogent", "workflows");
  if (!existsSync(base)) return claims;
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    try {
      const flowDir = resolve(base, entry.name);
      const state = JSON.parse(readFileSync(resolve(flowDir, "state.json"), "utf8"));
      if (["completed", "blocked", "failed", "cancelled"].includes(state?.status)) continue;
      const manifest = JSON.parse(readFileSync(resolve(flowDir, "manifest.json"), "utf8"));
      let ownerSessionKey: string | undefined;
      try { ownerSessionKey = JSON.parse(readFileSync(resolve(flowDir, "owner.json"), "utf8"))?.ownerSessionKey; } catch {}
      for (const step of manifest?.steps ?? []) for (const output of step?.outputs ?? []) {
        if (typeof output !== "string" || output.replace(/\\/g, "/").startsWith(".cogent/")) continue;
        claims.set(resourceKey(workspace, output), { taskId: entry.name, ownerSessionKey });
      }
    } catch {}
  }
  return claims;
}

function ticketResourceSnapshot(workspace: string, store: TicketStore) {
  const disk = statfsSync(workspace);
  return { freeMemoryBytes: freemem(), freeDiskBytes: Number(disk.bavail) * Number(disk.bsize), running: store.linkedRunning().length };
}

export function safeDispatchTicketWorkflows(input: { workspaceDir: string; store: TicketStore; config: Cfg; now?: Date }) {
  const limit = Math.max(1, Math.min(input.config.ticketDispatchLimit ?? 1, 32));
  const leases: TicketLease[] = [], deferred: Array<{ ticketId: string; reason: string }> = [];
  const claims = activeResourceClaims(input.workspaceDir);
  const initial = ticketResourceAdmission(ticketResourceSnapshot(input.workspaceDir, input.store), input.config as any);
  if (!initial.admitted) return { admission: initial, leases, deferred };

  for (const candidate of input.store.ready(Math.max(32, limit * 8))) {
    if (leases.length >= limit) break;
    const admission = ticketResourceAdmission(ticketResourceSnapshot(input.workspaceDir, input.store), input.config as any);
    if (!admission.admitted) break;
    const ticket = input.store.get(candidate.ticketId);
    if (!ticket || !ticket.workflowEligible) continue;
    const authority = sessionAuthority(dbPath(input.config, input.workspaceDir), ticket.ownerSessionKey);
    if (authority.state !== "active") { deferred.push({ ticketId: ticket.ticketId, reason: `session-${authority.state}` }); continue; }
    const conflict = requestedWorkspaceWrites(ticket.prompt)
      .map((path) => ({ path, claim: claims.get(resourceKey(input.workspaceDir, path)) }))
      .find((item) => item.claim);
    if (conflict) {
      deferred.push({ ticketId: ticket.ticketId, reason: `resource-conflict:${conflict.path}:${conflict.claim!.taskId}` });
      continue;
    }
    const lease = input.store.claim({ ticketId: candidate.ticketId, workerId: `ticket-worker-${candidate.ticketId}`,
      leaseMs: input.config.ticketLeaseMs ?? 60_000, now: input.now });
    if (!lease) continue;
    try {
      const classified = classifyDurableRequest(ticket.prompt, input.config.admissionMinimumScore ?? 5);
      const decision = classified.lane === "durable" ? classified : {
        ...classified, lane: "durable" as const,
        score: Math.max(classified.score, input.config.admissionMinimumScore ?? 5),
        reasons: [...classified.reasons, "direct-interruption-recovery"],
      };
      const requestHash = durableRequestFingerprint(ticket.prompt);
      const duplicate = activeWorkflowForSession(input.workspaceDir, requestHash, ticket.ownerSessionKey);
      const intake = duplicate ? undefined : compileDurableIntake({
        workspaceDir: input.workspaceDir,
        prompt: ticket.prompt,
        runId: ticket.runId,
        decision,
        model: input.config.durableWorkerModel ?? "qwen3.5:9b-32k",
      });
      const started = duplicate ?? startBoundWorkflow({
        workspaceDir: input.workspaceDir,
        manifestPath: intake!.manifestPath,
        ownerSessionKey: ticket.ownerSessionKey,
        pythonCommand: input.config.pythonCommand,
      });
      const manifestPath = intake?.manifestPath ?? `.cogent/workflows/${started.taskId}/manifest.json`;
      input.store.linkWorkflow({ ...lease, workflowId: started.taskId, manifestPath, now: input.now });
      if (intake) for (const path of requestedWorkspaceWrites(ticket.prompt)) {
        claims.set(resourceKey(input.workspaceDir, path), { taskId: started.taskId, ownerSessionKey: ticket.ownerSessionKey });
      }
      leases.push(lease);
    } catch (error) {
      input.store.failAttempt({ ...lease, classification: "transient", message: error instanceof Error ? error.message : String(error), now: input.now });
    }
  }
  return { admission: initial, leases, deferred };
}

function safeTicketRecoveryService(api: any, cfg: Cfg) {
  let interval: ReturnType<typeof setInterval> | undefined, active = false;
  return {
    id: "cogentnexus-ticket-recovery",
    start: async (ctx: any) => {
      const workspace = resolve(cfg.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
      const path = dbPath(cfg, workspace);
      const prepared = prepareV090RecoveryState(workspace, cfg);
      api.logger.info?.(`CogentNexus v0.9.0 recovery migration: reopened=${prepared.reopened} cancelledLegacy=${prepared.cancelledLegacy} cancelledOutboxSuppressed=${prepared.cancelledOutboxSuppressed} terminalRecoverySuppressed=${prepared.terminalRecoverySuppressed} outboxReset=${prepared.outboxReset} workflowDeliveryReset=${prepared.workflowDeliveryReset}`);
      const tick = async () => {
        if (active) return;
        active = true;
        try {
          const store = new TicketStore(path);
          store.recoverUndeliveredDirect({ olderThanMs: 120_000 });
          const recovered = store.recoverExpired();
          for (const item of recovered) api.logger.warn(`CogentNexus recovered expired Ticket ${item.ticketId} from worker ${item.previousWorkerId ?? "unknown"} generation ${item.previousLeaseGeneration}`);
          for (const item of reconcileTicketWorkflows({ workspaceDir: workspace, store, config: cfg as any })) api.logger.info?.(`CogentNexus Ticket ${item.ticketId} workflow action ${item.action}`);
          const dispatched = safeDispatchTicketWorkflows({ workspaceDir: workspace, store, config: cfg });
          for (const item of dispatched.deferred) api.logger.info?.(`CogentNexus Ticket ${item.ticketId} deferred: ${item.reason}`);
          for (const item of store.pendingOutbox(100, new Date(), 300_000)) {
            try { await deliverTicketOutbox(api, store, item); }
            catch (error) { api.logger.warn(`CogentNexus Ticket completion delivery failed for ${item.ticketId}: ${error instanceof Error ? error.message : String(error)}`); }
          }
        } catch (error) {
          api.logger.error(`CogentNexus Ticket recovery scan failed: ${error instanceof Error ? error.message : String(error)}`);
        } finally { active = false; }
      };
      await tick();
      interval = setInterval(() => { void tick(); }, Math.min(cfg.ticketRecoveryPollMs ?? 15_000, cfg.ticketOutboxPollMs ?? 5000, cfg.ticketDispatchPollMs ?? 5000));
      interval.unref?.();
    },
    stop: async () => { if (interval) clearInterval(interval); interval = undefined; },
  };
}

function wrap() {
  const entry = baseEntry as any;
  if (entry[WRAP]) return;
  Object.defineProperty(entry, WRAP, { value: true });
  const register = baseEntry.register?.bind(baseEntry);
  baseEntry.register = (api: any) => {
    patchTicketStore();
    const cfg = (api.pluginConfig ?? {}) as Cfg, reg = api.registerService?.bind(api), proxy = Object.create(api);
    const compat = compatWorkflow(api, cfg), workflow = { ...api.session?.workflow, ...compat };
    proxy.session = { ...api.session, workflow };

    const originalOn = api.on?.bind(api);
    if (originalOn) proxy.on = (name: string, handler: any, options?: any) => {
      if (name !== "session_end") return originalOn(name, handler, options);
      return originalOn(name, (event: any, ctx: any) => {
        // A UI "new session" is a new ownership domain. Do not silently transfer old mutable state.
        if (event?.reason === "new") return;
        return handler(event, ctx);
      }, options);
    };

    api.on?.("before_agent_run", (event: any, ctx: any) => {
      if (!ctx.sessionKey || ctx.sessionKey.includes(":subagent:")) return { outcome: "pass" };
      if (!isInternalControlText(String(event.prompt ?? ""))) return { outcome: "pass" };
      return { outcome: "block", reason: "CogentNexus internal control prompt is forbidden in an owner session", category: "cogentnexus_internal_owner_fence" };
    }, { priority: 5000, timeoutMs: 5000 });

    api.on?.("before_message_write", (event: any, ctx: any) => {
      const sessionKey = event?.sessionKey ?? ctx?.sessionKey;
      if (!sessionKey || sessionKey.includes(":subagent:")) return;
      const text = roleText(event?.message);
      if (text && isInternalControlText(text)) return { block: true };
    }, { priority: 5000, timeoutMs: 5000 });

    api.on?.("session_start", (event: any, ctx: any) => {
      const sessionKey = event?.sessionKey ?? ctx?.sessionKey;
      if (!sessionKey) return;
      const workspace = resolve(ctx?.workspaceDir ?? cfg.workspaceDir ?? process.cwd());
      const path = dbPath(cfg, workspace);
      const authority = sessionAuthority(path, sessionKey);
      if (authority.state !== "active") api.logger.warn?.(`CogentNexus refused to reactivate tombstoned session ${sessionKey} (${authority.state})`);
    }, { priority: 1500, timeoutMs: 5000 });

    api.on?.("agent_end", async (event: any, ctx: any) => {
      const sessionKey = ctx.sessionKey;
      if (event.success || !isExplicitUserCancellation(event.error) || !sessionKey || sessionKey.includes(":subagent:")) return;
      const workspace = resolve(ctx.workspaceDir ?? cfg.workspaceDir ?? process.cwd()), path = dbPath(cfg, workspace);
      const reason = (event.error ?? "agent run aborted").slice(0, 2000);
      const cancelled = cancelSessionByKey(path, { sessionKey, message: reason });
      compat.cancelSessionTimers(sessionKey);
      const completionTags = suppressSessionWorkflowCompletions(workspace, sessionKey, reason);
      for (const tag of [...cancelled.outboxTags, ...completionTags]) {
        try { await workflow.unscheduleSessionTurnsByTag({ sessionKey, tag }); }
        catch (error) { api.logger.warn?.(`CogentNexus cancellation unschedule failed for ${tag}: ${error instanceof Error ? error.message : String(error)}`); }
      }
      const results = cancelBoundWorkflows(workspace, cancelled.workflowIds, reason, cfg);
      for (const result of results) if (!result.ok) api.logger.warn?.(`CogentNexus workflow cancellation failed for ${result.workflowId}: ${result.error}`);
      await cancelTrackedSynthetic(api, sessionKey);
    }, { priority: 1000, timeoutMs: 60_000 });

    api.on?.("session_end", async (event: any, ctx: any) => {
      if (event?.reason !== "deleted") return;
      const sessionKey = event.sessionKey ?? ctx.sessionKey;
      if (!sessionKey) return;
      const workspace = resolve(ctx.workspaceDir ?? cfg.workspaceDir ?? process.cwd()), path = dbPath(cfg, workspace);
      const reason = "OpenClaw owner session deleted";
      const deletion = deleteSessionByKey(path, { sessionKey, message: reason });
      compat.cancelSessionTimers(sessionKey);
      const completionTags = suppressSessionWorkflowCompletions(workspace, sessionKey, reason);
      for (const tag of [...deletion.outboxTags, ...completionTags]) {
        try { await workflow.unscheduleSessionTurnsByTag({ sessionKey, tag }); } catch {}
      }
      const results = cancelBoundWorkflows(workspace, deletion.workflowIds, reason, cfg);
      for (const result of results) if (!result.ok) api.logger.warn?.(`CogentNexus session deletion workflow cancellation failed for ${result.workflowId}: ${result.error}`);
      await cancelTrackedSynthetic(api, sessionKey);
      finalizeSessionDeletion(path, sessionKey, reason);
      api.logger.info?.(`CogentNexus session deletion barrier completed for ${sessionKey}: generation=${deletion.generation} tickets=${deletion.cancelled.length} assistantSuppressed=${deletion.assistantSuppressed}`);
    }, { priority: 2000, timeoutMs: 60_000 });

    proxy.registerService = (service: any) => {
      if (!reg) return;
      if (service?.id === "cogentnexus-ticket-recovery") return reg(safeTicketRecoveryService(proxy, cfg));
      return reg(service);
    };

    register?.(proxy);
    reg?.(recoveryService(api, cfg));
  };
}

wrap();
export default baseEntry;
