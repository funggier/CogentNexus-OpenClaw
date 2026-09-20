import { existsSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { join } from "node:path";

export type HostRunTerminalEvidence =
  | { state: "pending" }
  | {
      state: "terminal";
      runId: string;
      status: string;
      stopReason?: string;
      aborted?: boolean;
      externalAbort?: boolean;
      timedOut?: boolean;
      promptError?: string;
      sessionId?: string;
      createdAt?: number;
    };

export function readHostRunTerminalEvidence(input: {
  databasePath: string;
  runId: string;
}): HostRunTerminalEvidence {
  if (!input.databasePath || !input.runId || !existsSync(input.databasePath)) return { state: "pending" };
  const db = new DatabaseSync(input.databasePath, { readOnly: true });
  try {
    const row = db.prepare(`
      SELECT session_id,event_json,created_at
      FROM trajectory_runtime_events
      WHERE run_id=?
        AND json_extract(event_json,'$.type')='session.ended'
      ORDER BY seq DESC
      LIMIT 1
    `).get(input.runId) as { session_id?: string; event_json?: string; created_at?: number } | undefined;
    if (!row?.event_json) return { state: "pending" };
    const event = JSON.parse(row.event_json) as any;
    const status = typeof event?.data?.status === "string" ? event.data.status : "";
    if (!status) return { state: "pending" };
    return {
      state: "terminal",
      runId: input.runId,
      status,
      ...(typeof event?.data?.stopReason === "string" ? { stopReason: event.data.stopReason } : {}),
      ...(typeof event?.data?.aborted === "boolean" ? { aborted: event.data.aborted } : {}),
      ...(typeof event?.data?.externalAbort === "boolean" ? { externalAbort: event.data.externalAbort } : {}),
      ...(typeof event?.data?.timedOut === "boolean" ? { timedOut: event.data.timedOut } : {}),
      ...(typeof event?.data?.promptError === "string" ? { promptError: event.data.promptError } : {}),
      ...(typeof row.session_id === "string" ? { sessionId: row.session_id } : {}),
      ...(typeof row.created_at === "number" ? { createdAt: row.created_at } : {}),
    };
  } catch {
    return { state: "pending" };
  } finally {
    db.close();
  }
}

function agentIdFromSessionKey(sessionKey: string): string | undefined {
  return /^agent:([^:]+):/u.exec(sessionKey.trim())?.[1];
}

export function resolveHostAgentDatabasePath(api: any, sessionKey: string): string | undefined {
  const agentId = agentIdFromSessionKey(sessionKey);
  if (!agentId) return undefined;
  const resolveAgentDir = api?.runtime?.agent?.resolveAgentDir;
  if (typeof resolveAgentDir !== "function") return undefined;
  try {
    const agentDir = resolveAgentDir(api?.config ?? {}, agentId);
    if (typeof agentDir !== "string" || !agentDir.trim()) return undefined;
    const databasePath = join(agentDir, "openclaw-agent.sqlite");
    return existsSync(databasePath) ? databasePath : undefined;
  } catch {
    return undefined;
  }
}


export async function waitForHostRunTerminalEvidence(input: {
  api: any;
  sessionKey: string;
  runId: string;
  timeoutMs?: number;
  pollMs?: number;
}): Promise<HostRunTerminalEvidence> {
  const databasePath = resolveHostAgentDatabasePath(input.api, input.sessionKey);
  if (!databasePath) return { state: "pending" };
  const timeoutMs = Math.max(0, Math.min(input.timeoutMs ?? 1500, 5000));
  const pollMs = Math.max(10, Math.min(input.pollMs ?? 25, 250));
  const deadline = Date.now() + timeoutMs;
  while (true) {
    const evidence = readHostRunTerminalEvidence({ databasePath, runId: input.runId });
    if (evidence.state === "terminal") return evidence;
    const remaining = deadline - Date.now();
    if (remaining <= 0) return { state: "pending" };
    await new Promise<void>((resolve) => {
      const timer = setTimeout(resolve, Math.min(pollMs, remaining));
      timer.unref?.();
    });
  }
}

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

function columnExists(db: DatabaseSync, table: string, column: string) {
  if (!tableExists(db, table)) return false;
  return (db.prepare(`PRAGMA table_info(${table})`).all() as Array<{ name?: string }>).some((row) => row.name === column);
}

function addTicketEvent(db: DatabaseSync, ticketId: string, eventType: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

function ensureRecoveryTable(db: DatabaseSync) {
  db.exec(`
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
  `);
}

function ownerGeneration(db: DatabaseSync, sessionKey: string) {
  if (!tableExists(db, "cnx_sessions")) return 0;
  const row = db.prepare("SELECT generation FROM cnx_sessions WHERE session_key=?").get(sessionKey) as { generation?: number } | undefined;
  return Number(row?.generation ?? 0);
}

function parseResult(value: unknown): any {
  if (typeof value !== "string" || !value.trim()) return {};
  try { return JSON.parse(value); } catch { return {}; }
}

function deliveryEvidence(db: DatabaseSync, ticketId: string) {
  if (!tableExists(db, "cnx_assistant_delivery")) {
    return { confirmed: false, transportAccepted: false, suppressible: 0 };
  }
  const hasDeliveryState = columnExists(db, "cnx_assistant_delivery", "delivery_state");
  if (!hasDeliveryState) {
    const confirmed = Boolean(db.prepare(
      "SELECT 1 FROM cnx_assistant_delivery WHERE ticket_id=? AND status='delivered' LIMIT 1",
    ).get(ticketId));
    const suppressible = Number((db.prepare(
      "SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND status='pending'",
    ).get(ticketId) as any)?.n ?? 0);
    return { confirmed, transportAccepted: false, suppressible };
  }
  const confirmed = Boolean(db.prepare(`
    SELECT 1 FROM cnx_assistant_delivery
    WHERE ticket_id=? AND (status='delivered' OR delivery_state='confirmed')
    LIMIT 1
  `).get(ticketId));
  const transportAccepted = Boolean(db.prepare(`
    SELECT 1 FROM cnx_assistant_delivery
    WHERE ticket_id=? AND status='pending' AND delivery_state='transport_accepted'
    LIMIT 1
  `).get(ticketId));
  const suppressible = Number((db.prepare(`
    SELECT COUNT(*) AS n FROM cnx_assistant_delivery
    WHERE ticket_id=? AND status='pending'
      AND COALESCE(delivery_state,'prepared') IN ('prepared','staged','failed','cancelled')
  `).get(ticketId) as any)?.n ?? 0);
  return { confirmed, transportAccepted, suppressible };
}

function recordConflictOnce(
  db: DatabaseSync,
  ticketId: string,
  payload: unknown,
  stamp: string,
) {
  const prior = db.prepare(
    "SELECT 1 FROM ticket_events WHERE ticket_id=? AND event_type='host_terminal_conflict' LIMIT 1",
  ).get(ticketId);
  if (!prior) addTicketEvent(db, ticketId, "host_terminal_conflict", payload, stamp);
}

export function settleSilentHostSuccess(input: {
  ticketDatabasePath: string;
  evidence: Extract<HostRunTerminalEvidence, { state: "terminal" }>;
  now?: Date;
}): "completed" | "unchanged" | "conflict" {
  const terminal = input.evidence.status.trim().toLowerCase();
  if (!["success","completed","ok"].includes(terminal)) return "unchanged";
  const db = new DatabaseSync(input.ticketDatabasePath);
  const stamp = (input.now ?? new Date()).toISOString();
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE;");
    const row = db.prepare(`
      SELECT ticket_id,status,workflow_eligible,response_ready_at,delivery_confirmed_at,result_json
      FROM tickets WHERE run_id=? ORDER BY created_at DESC LIMIT 1
    `).get(input.evidence.runId) as any;
    if (!row || row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.response_ready_at == null) {
      db.exec("COMMIT");
      return "unchanged";
    }
    const delivery = deliveryEvidence(db, row.ticket_id);
    if (row.delivery_confirmed_at != null || delivery.confirmed || delivery.transportAccepted) {
      recordConflictOnce(db, row.ticket_id, {
        runId: input.evidence.runId,
        hostStatus: input.evidence.status,
        reason: "silent host success conflicts with existing delivery evidence",
      }, stamp);
      db.exec("COMMIT");
      return "conflict";
    }
    const result = {
      runId: input.evidence.runId,
      direct: true,
      expectsDelivery: false,
      hostTerminal: true,
      hostStatus: input.evidence.status,
    };
    db.prepare(`
      UPDATE tickets SET status='completed',result_json=?,delivery_confirmed_at=?,
        delivery_last_error=NULL,failure_class=NULL,failure_message=NULL,updated_at=?
      WHERE ticket_id=? AND status='accepted' AND delivery_confirmed_at IS NULL
    `).run(JSON.stringify(result), stamp, stamp, row.ticket_id);
    addTicketEvent(db, row.ticket_id, "delivery_confirmed", {
      runId: input.evidence.runId,
      required: false,
      authority: "host-session-ended",
      hostStatus: input.evidence.status,
    }, stamp);
    addTicketEvent(db, row.ticket_id, "completed", result, stamp);
    db.exec("COMMIT");
    return "completed";
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

export function isAuthoritativeUserStop(
  evidence: Extract<HostRunTerminalEvidence, { state: "terminal" }>,
) {
  const stopReason = (evidence.stopReason ?? "").trim().toLowerCase();
  return evidence.aborted === true
    && evidence.externalAbort === true
    && evidence.timedOut !== true
    && stopReason === "aborted";
}

export function cancelDirectOwnerSessionForAuthoritativeUserStop(input: {
  ticketDatabasePath: string;
  sessionKey: string;
  evidence: Extract<HostRunTerminalEvidence, { state: "terminal" }>;
  now?: Date;
}): { state: "cancelled" | "unchanged" | "conflict"; cancelled: string[]; generation?: number } {
  if (!isAuthoritativeUserStop(input.evidence)) return { state:"unchanged", cancelled:[] };
  const db = new DatabaseSync(input.ticketDatabasePath);
  const stamp = (input.now ?? new Date()).toISOString();
  const reason = "Reply operation aborted by user";
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE;");
    const active = db.prepare(`
      SELECT ticket_id,status,owner_session_key,delivery_confirmed_at
      FROM tickets
      WHERE run_id=? AND owner_session_key=?
      ORDER BY created_at DESC LIMIT 1
    `).get(input.evidence.runId, input.sessionKey) as any;
    if (!active) {
      db.exec("COMMIT");
      return { state:"unchanged", cancelled:[] };
    }
    const delivery = deliveryEvidence(db, active.ticket_id);
    if (active.delivery_confirmed_at != null || delivery.confirmed || delivery.transportAccepted) {
      recordConflictOnce(db, active.ticket_id, {
        runId: input.evidence.runId,
        hostStatus: input.evidence.status,
        stopReason: input.evidence.stopReason,
        reason: "authoritative user stop conflicts with delivery evidence",
      }, stamp);
      db.exec("COMMIT");
      return { state:"conflict", cancelled:[] };
    }

    const rows = db.prepare(`
      SELECT ticket_id,status,run_id
      FROM tickets
      WHERE owner_session_key=? AND workflow_eligible=0
        AND (
          status IN ('accepted','planned','running','waiting')
          OR (run_id=? AND status='failed')
        )
      ORDER BY created_at,ticket_id
    `).all(input.sessionKey, input.evidence.runId) as any[];
    if (!rows.length) {
      db.exec("COMMIT");
      return { state:"unchanged", cancelled:[] };
    }

    let generation = 0;
    if (tableExists(db, "cnx_sessions")) {
      const row = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(input.sessionKey) as any;
      generation = Number(row?.generation ?? 0);
      if (row?.state === "active") {
        generation += 1;
        db.prepare(`
          UPDATE cnx_sessions
          SET generation=?,updated_at=?,delete_reason=NULL
          WHERE session_key=? AND state='active'
        `).run(generation, stamp, input.sessionKey);
      }
    }

    const cancelled: string[] = [];
    for (const row of rows) {
      const changed = db.prepare(`
        UPDATE tickets
        SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,
          heartbeat_at=NULL,result_json=NULL,response_ready_at=NULL,
          failure_class=NULL,failure_message=?,delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND (
          status IN ('accepted','planned','running','waiting')
          OR (run_id=? AND status='failed')
        )
      `).run(reason, stamp, row.ticket_id, input.evidence.runId);
      if (changed.changes !== 1) continue;
      cancelled.push(row.ticket_id);
      addTicketEvent(db, row.ticket_id, "cancelled_by_user", {
        source: "host-terminal-external-abort",
        previousStatus: row.status,
        previousRunId: row.run_id,
        runId: input.evidence.runId,
        sessionGeneration: generation,
        message: reason,
      }, stamp);
    }

    if (cancelled.length) {
      if (tableExists(db, "ticket_outbox")) {
        db.prepare(`
          DELETE FROM ticket_outbox
          WHERE owner_session_key=? AND delivery_status='pending'
            AND ticket_id IN (SELECT ticket_id FROM tickets WHERE owner_session_key=? AND status='cancelled')
        `).run(input.sessionKey, input.sessionKey);
      }
      if (tableExists(db, "cnx_assistant_delivery")) {
        db.prepare(`
          DELETE FROM cnx_assistant_delivery
          WHERE owner_session_key=? AND status='pending'
            AND ticket_id IN (SELECT ticket_id FROM tickets WHERE owner_session_key=? AND status='cancelled')
        `).run(input.sessionKey, input.sessionKey);
      }
      if (tableExists(db, "cnx_direct_recovery")) {
        db.prepare(`
          UPDATE cnx_direct_recovery
          SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=?
          WHERE ticket_id IN (
            SELECT ticket_id FROM tickets WHERE owner_session_key=? AND status='cancelled'
          ) AND state<>'cancelled'
        `).run(reason, stamp, input.sessionKey);
      }
    }
    db.exec("COMMIT");
    return { state:"cancelled", cancelled, generation };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

export function reconcileHostTerminalFailure(input: {
  ticketDatabasePath: string;
  evidence: Extract<HostRunTerminalEvidence, { state: "terminal" }>;
  now?: Date;
}): "recovery_pending" | "unchanged" | "conflict" {
  const terminal = input.evidence.status.trim().toLowerCase();
  if (["success","completed","ok"].includes(terminal)) return "unchanged";
  const db = new DatabaseSync(input.ticketDatabasePath);
  const stamp = (input.now ?? new Date()).toISOString();
  const reason = `OpenClaw host terminal ${input.evidence.status}${input.evidence.stopReason ? `: ${input.evidence.stopReason}` : ""}`.slice(0, 2000);
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE;");
    const row = db.prepare(`
      SELECT ticket_id,status,workflow_eligible,owner_session_key,result_json,
        response_ready_at,delivery_confirmed_at
      FROM tickets WHERE run_id=? ORDER BY created_at DESC LIMIT 1
    `).get(input.evidence.runId) as any;
    if (!row) {
      db.exec("COMMIT");
      return "unchanged";
    }
    const result = parseResult(row.result_json);
    const syntheticNoDeliveryCompletion =
      row.status === "completed" && result?.direct === true && result?.expectsDelivery === false;
    const delivery = deliveryEvidence(db, row.ticket_id);
    const realConfirmed =
      delivery.confirmed || (row.delivery_confirmed_at != null && !syntheticNoDeliveryCompletion);
    if (realConfirmed || delivery.transportAccepted) {
      recordConflictOnce(db, row.ticket_id, {
        runId: input.evidence.runId,
        hostStatus: input.evidence.status,
        stopReason: input.evidence.stopReason,
        confirmedDelivery: realConfirmed,
        transportAccepted: delivery.transportAccepted,
      }, stamp);
      db.exec("COMMIT");
      return "conflict";
    }
    if (row.status !== "accepted" && !syntheticNoDeliveryCompletion) {
      db.exec("COMMIT");
      return "unchanged";
    }

    let suppressed = 0;
    if (tableExists(db, "cnx_assistant_delivery")) {
      if (columnExists(db, "cnx_assistant_delivery", "delivery_state")) {
        suppressed = Number(db.prepare(`
          DELETE FROM cnx_assistant_delivery
          WHERE ticket_id=? AND status='pending'
            AND COALESCE(delivery_state,'prepared') IN ('prepared','staged','failed','cancelled')
        `).run(row.ticket_id).changes);
      } else {
        suppressed = Number(db.prepare(
          "DELETE FROM cnx_assistant_delivery WHERE ticket_id=? AND status='pending'",
        ).run(row.ticket_id).changes);
      }
    }

    ensureRecoveryTable(db);
    const generation = ownerGeneration(db, String(row.owner_session_key ?? ""));
    db.prepare(`
      UPDATE tickets SET status='accepted',workflow_eligible=0,result_json=NULL,
        response_ready_at=NULL,delivery_confirmed_at=NULL,failure_class='interrupted',
        failure_message=?,delivery_last_error=?,updated_at=?
      WHERE ticket_id=?
    `).run(reason, reason, stamp, row.ticket_id);
    db.prepare(`
      INSERT INTO cnx_direct_recovery(
        ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
        owner_generation,created_at,updated_at
      ) VALUES (?,'resume','pending',0,NULL,?,?,?, ?,?)
      ON CONFLICT(ticket_id) DO UPDATE SET
        mode='resume',state='pending',active_run_id=NULL,next_attempt_at=excluded.next_attempt_at,
        last_error=excluded.last_error,owner_generation=excluded.owner_generation,updated_at=excluded.updated_at
    `).run(row.ticket_id, stamp, reason, generation, stamp, stamp);
    addTicketEvent(db, row.ticket_id, "host_terminal_recovery_pending", {
      runId: input.evidence.runId,
      hostStatus: input.evidence.status,
      stopReason: input.evidence.stopReason,
      previousStatus: row.status,
      syntheticNoDeliveryCompletion,
      suppressedPendingDeliveries: suppressed,
      ownerGeneration: generation,
    }, stamp);
    db.exec("COMMIT");
    return "recovery_pending";
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

export function scheduleHostRunTerminalReconcile(input: {
  api: any;
  sessionKey: string;
  runId: string;
  delayMs?: number;
  pollMs?: number;
  maxAttempts?: number;
  onTerminal: (evidence: Extract<HostRunTerminalEvidence, { state: "terminal" }>) => void | Promise<void>;
}) {
  const databasePath = resolveHostAgentDatabasePath(input.api, input.sessionKey);
  if (!databasePath) return { scheduled: false as const, cancel: () => {} };

  let cancelled = false;
  let timer: ReturnType<typeof setTimeout> | undefined;
  let attempts = 0;
  const maxAttempts = Math.max(1, input.maxAttempts ?? 25);
  const pollMs = Math.max(25, input.pollMs ?? 200);

  const tick = () => {
    if (cancelled) return;
    attempts += 1;
    const evidence = readHostRunTerminalEvidence({ databasePath, runId: input.runId });
    if (evidence.state === "terminal") {
      void Promise.resolve(input.onTerminal(evidence));
      return;
    }
    if (attempts >= maxAttempts) return;
    timer = setTimeout(tick, pollMs);
    timer.unref?.();
  };

  timer = setTimeout(tick, Math.max(0, input.delayMs ?? 100));
  timer.unref?.();
  return {
    scheduled: true as const,
    databasePath,
    cancel: () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    },
  };
}