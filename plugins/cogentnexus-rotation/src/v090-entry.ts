import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { classifyDurableRequest } from "./admission.js";
import entry, { cancelSessionTickets, prepareV090RecoveryState } from "./v090.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type Config = {
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  admissionMinimumScore?: number;
};

const WRAPPED = Symbol.for("cogentnexus.v090.entry.host-reconciliation");
const LIVE_POLICY_PATCH = Symbol.for("cogentnexus.v090.live-policy-patch");

export function isOpenClawAbortMessage(message?: string | null): boolean {
  if (!message) return false;
  const value = message.trim();
  return /^This operation was aborted(?:\s*\|\s*\d+)?$/u.test(value);
}

function addEvent(db: DatabaseSync, ticketId: string, type: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, type, JSON.stringify(payload), stamp);
}

export function suppressFailedOutboxForTicket(databasePath: string, ticketId: string, reason: string, now = new Date()): number {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  const stamp = now.toISOString();
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE");
    const removed = Number(db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND terminal_status='failed' AND delivery_status='pending'")
      .run(ticketId).changes);
    if (removed > 0) addEvent(db, ticketId, "failure_delivery_suppressed", { reason, removed, policy:"non-inference-terminal-failure" }, stamp);
    db.exec("COMMIT");
    return removed;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

export function suppressFailedOutboxForRun(databasePath: string, runId: string, reason: string, now = new Date()): number {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly:true });
  let ticketId: string | undefined;
  try {
    const row = db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='failed' ORDER BY created_at DESC LIMIT 1").get(runId) as {ticket_id?:string} | undefined;
    ticketId = row?.ticket_id;
  } finally {
    db.close();
  }
  return ticketId ? suppressFailedOutboxForTicket(databasePath, ticketId, reason, now) : 0;
}

export function reconcileV090LiveState(databasePath: string, now = new Date()) {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  const stamp = now.toISOString();
  let abortFailuresCancelled = 0;
  let abortOutboxSuppressed = 0;
  let failedOutboxSuppressed = 0;
  let terminalRecoverySuppressed = 0;
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE");
    const rows = db.prepare(`SELECT ticket_id,failure_message FROM tickets
      WHERE status='failed' AND workflow_id IS NULL AND workflow_eligible=0 AND failure_class='permanent'`).all() as Array<{ticket_id:string;failure_message:string|null}>;
    for (const row of rows) {
      if (!isOpenClawAbortMessage(row.failure_message)) continue;
      const changed = db.prepare(`UPDATE tickets SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,
        failure_class=NULL,response_ready_at=NULL,delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND status='failed' AND workflow_id IS NULL AND workflow_eligible=0 AND failure_class='permanent'`)
        .run(stamp, row.ticket_id);
      if (changed.changes !== 1) continue;
      abortFailuresCancelled++;
      abortOutboxSuppressed += Number(db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id).changes);
      addEvent(db, row.ticket_id, "v090_openclaw_abort_cancelled", { previousStatus:"failed", message:row.failure_message }, stamp);
    }
    failedOutboxSuppressed = Number(db.prepare("DELETE FROM ticket_outbox WHERE terminal_status='failed' AND delivery_status='pending'").run().changes);
    const recoveryTable = db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get();
    if (recoveryTable) {
      terminalRecoverySuppressed = Number(db.prepare(`UPDATE cnx_direct_recovery
        SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=COALESCE(last_error,'terminal ticket fence'),updated_at=?
        WHERE state<>'cancelled' AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status IN ('completed','failed','cancelled'))`).run(stamp).changes);
    }
    db.exec("COMMIT");
    return { abortFailuresCancelled, abortOutboxSuppressed, failedOutboxSuppressed, terminalRecoverySuppressed };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

export function patchV090LivePolicy() {
  const prototype = TicketStore.prototype as any;
  if (prototype[LIVE_POLICY_PATCH]) return;
  Object.defineProperty(prototype, LIVE_POLICY_PATCH, { value:true });
  const finalize = TicketStore.prototype.finalizeDirectRun;
  const failAttempt = TicketStore.prototype.failAttempt;

  TicketStore.prototype.finalizeDirectRun = function(input: Parameters<TicketStore["finalizeDirectRun"]>[0]) {
    if (!input.success && isOpenClawAbortMessage(input.message)) {
      cancelSessionTickets(this.databasePath, { runId:input.runId, message:input.message, now:input.now });
      return "unchanged";
    }
    const result = finalize.call(this, input);
    if (result === "failed") suppressFailedOutboxForRun(this.databasePath, input.runId, input.message ?? "direct run failed", input.now);
    return result;
  };

  TicketStore.prototype.failAttempt = function(input: Parameters<TicketStore["failAttempt"]>[0]) {
    const result = failAttempt.call(this, input);
    if (result === "failed") suppressFailedOutboxForTicket(this.databasePath, input.ticketId, input.message, input.now);
    return result;
  };
}

export function hasLegacyDirectPromotion(databasePath: string, admissionMinimumScore = 5): boolean {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    const rows = db.prepare(`SELECT prompt FROM tickets
      WHERE status IN ('waiting','failed')
        AND workflow_id IS NULL
        AND ((workflow_eligible=1 AND failure_class='interrupted')
          OR (status='failed' AND workflow_eligible=0 AND failure_class='permanent' AND failure_message='Reply operation aborted by user'))
      ORDER BY created_at
      LIMIT 32`).all() as Array<{ prompt: string }>;
    return rows.some((row) => classifyDurableRequest(row.prompt, admissionMinimumScore).lane === "direct") || rows.length > 0;
  } finally {
    db.close();
  }
}

function wrapEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value: true });
  const register = entry.register?.bind(entry);
  entry.register = (api: any) => {
    const config = (api.pluginConfig ?? {}) as Config;
    register?.(api);
    patchV090LivePolicy();

    const configuredWorkspace = resolve(config.workspaceDir ?? process.cwd());
    const configuredDatabase = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(configuredWorkspace));
    try {
      const live = reconcileV090LiveState(configuredDatabase);
      if (live.abortFailuresCancelled || live.abortOutboxSuppressed || live.failedOutboxSuppressed || live.terminalRecoverySuppressed) {
        api.logger.info?.(`CogentNexus v0.9.0 live policy reconciliation: abortFailuresCancelled=${live.abortFailuresCancelled} abortOutboxSuppressed=${live.abortOutboxSuppressed} failedOutboxSuppressed=${live.failedOutboxSuppressed} terminalRecoverySuppressed=${live.terminalRecoverySuppressed}`);
      }
    } catch (error) {
      api.logger.warn?.(`CogentNexus v0.9.0 live policy registration reconciliation failed: ${error instanceof Error ? error.message : String(error)}`);
    }

    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    api.registerService?.({
      id: "cogentnexus-v090-host-reconciliation",
      start: async (ctx: any) => {
        const workspaceDir = resolve(config.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
        const tick = () => {
          if (active) return;
          active = true;
          try {
            const live = reconcileV090LiveState(databasePath);
            if (live.abortFailuresCancelled || live.abortOutboxSuppressed || live.failedOutboxSuppressed || live.terminalRecoverySuppressed) {
              api.logger.info?.(`CogentNexus v0.9.0 live policy reconciliation: abortFailuresCancelled=${live.abortFailuresCancelled} abortOutboxSuppressed=${live.abortOutboxSuppressed} failedOutboxSuppressed=${live.failedOutboxSuppressed} terminalRecoverySuppressed=${live.terminalRecoverySuppressed}`);
            }
            if (!hasLegacyDirectPromotion(databasePath, config.admissionMinimumScore ?? 5)) return;
            const result = prepareV090RecoveryState(workspaceDir, config);
            if (result.reopened > 0 || result.cancelledLegacy > 0) {
              api.logger.info?.(`CogentNexus v0.9.0 reconciled Direct Tickets: reopened=${result.reopened} cancelledLegacy=${result.cancelledLegacy}`);
            }
          } catch (error) {
            api.logger.warn(`CogentNexus v0.9.0 Host reconciliation failed: ${error instanceof Error ? error.message : String(error)}`);
          } finally {
            active = false;
          }
        };
        tick();
        interval = setInterval(tick, Math.max(1000, Math.min(config.ticketRecoveryPollMs ?? 5000, 30_000)));
        interval.unref?.();
      },
      stop: async () => {
        if (interval) clearInterval(interval);
        interval = undefined;
      },
    });
  };
}

wrapEntry();
export default entry;
