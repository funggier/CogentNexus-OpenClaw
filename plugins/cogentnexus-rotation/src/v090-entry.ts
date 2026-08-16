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

type NativeTaskView = {
  id?: string;
  runtime?: string;
  sourceId?: string;
  runId?: string;
  label?: string;
  title?: string;
  status?: string;
};

const WRAPPED = Symbol.for("cogentnexus.v090.entry.host-reconciliation");
const LIVE_POLICY_PATCH = Symbol.for("cogentnexus.v090.live-policy-patch");
const CNX_PLUGIN_LABEL = "plugin:cogentnexus-rotation";
const ACTIVE_NATIVE_TASK_STATUSES = new Set(["queued", "running"]);
const TERMINAL_NATIVE_TICKET_STATUSES = new Set(["failed", "cancelled"]);

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

function readNativeFenceSnapshot(databasePath: string): {
  agentIds: string[];
  ticketStatuses: Map<string, string>;
} {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly:true });
  const agentIds = new Set<string>();
  const ticketStatuses = new Map<string, string>();
  try {
    const rows = db.prepare("SELECT ticket_id,status,owner_session_key FROM tickets").all() as Array<{
      ticket_id:string;
      status:string;
      owner_session_key:string | null;
    }>;
    for (const row of rows) {
      ticketStatuses.set(row.ticket_id, row.status);
      const match = /^agent:([^:]+):/u.exec(row.owner_session_key ?? "");
      if (match?.[1]) agentIds.add(match[1]);
    }
  } finally {
    db.close();
  }
  if (agentIds.size === 0) agentIds.add("main");
  return { agentIds:[...agentIds].sort(), ticketStatuses };
}

function ticketIdFromNativeTask(task: NativeTaskView): string | undefined {
  for (const value of [task.title, task.runId, task.sourceId]) {
    const match = /\b(CNXT-[A-Za-z0-9-]+)\b/u.exec(value ?? "");
    if (match?.[1]) return match[1];
  }
  return undefined;
}

export function shouldFenceNativeCnxTask(
  task: NativeTaskView,
  ticketStatuses: ReadonlyMap<string, string>,
): boolean {
  if (!ACTIVE_NATIVE_TASK_STATUSES.has(task.status ?? "")) return false;
  const cnxOwned = task.label === CNX_PLUGIN_LABEL
    || (task.runId ?? "").startsWith("cnx-")
    || (task.sourceId ?? "").startsWith("cnx-");
  if (!cnxOwned) return false;

  const ticketId = ticketIdFromNativeTask(task);
  if (ticketId && TERMINAL_NATIVE_TICKET_STATUSES.has(ticketStatuses.get(ticketId) ?? "")) return true;

  const title = task.title ?? "";
  if (/^\[CogentNexus Delivery: ticket:\d+\]/u.test(title)
      && /reached terminal status (?:failed|cancelled)\./u.test(title)) return true;
  if (/^\[CogentNexus Delivery: workflow:/u.test(title)
      && /reached terminal status (?:failed|blocked|cancelled)\./u.test(title)) return true;
  return false;
}

export async function reconcileOpenClawNativeTasks(
  api: any,
  ctx: any,
  databasePath: string,
): Promise<{ supported:boolean; scanned:number; fenced:number; failed:number }> {
  const taskRuns = api.runtime?.tasks?.runs;
  if (!taskRuns?.bindSession) return { supported:false, scanned:0, fenced:0, failed:0 };

  const { agentIds, ticketStatuses } = readNativeFenceSnapshot(databasePath);
  const mainKey = String(ctx.config?.session?.mainKey ?? "main").trim() || "main";
  const seen = new Set<string>();
  let scanned = 0;
  let fenced = 0;
  let failed = 0;

  for (const agentId of agentIds) {
    const sessionKey = `agent:${agentId}:${mainKey}`;
    let bound: any;
    try {
      bound = taskRuns.bindSession({ sessionKey, agentId });
    } catch (error) {
      api.logger.warn?.(`CogentNexus native task fence could not bind ${sessionKey}: ${error instanceof Error ? error.message : String(error)}`);
      failed++;
      continue;
    }
    const tasks = (bound.list?.() ?? []) as NativeTaskView[];
    for (const task of tasks) {
      if (!task.id || seen.has(task.id)) continue;
      seen.add(task.id);
      scanned++;
      if (!shouldFenceNativeCnxTask(task, ticketStatuses)) continue;
      try {
        const result = await bound.cancel({ taskId:task.id, cfg:ctx.config ?? {} });
        if (result?.cancelled) fenced++;
        else {
          failed++;
          api.logger.warn?.(`CogentNexus native task fence did not cancel ${task.id}: ${result?.reason ?? "unknown reason"}`);
        }
      } catch (error) {
        failed++;
        api.logger.warn?.(`CogentNexus native task fence failed for ${task.id}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
  }
  return { supported:true, scanned, fenced, failed };
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

    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    api.registerService?.({
      id: "cogentnexus-v090-host-reconciliation",
      start: async (ctx: any) => {
        const workspaceDir = resolve(config.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
        const tick = async () => {
          if (active) return;
          active = true;
          try {
            const live = reconcileV090LiveState(databasePath);
            if (live.abortFailuresCancelled || live.abortOutboxSuppressed || live.failedOutboxSuppressed || live.terminalRecoverySuppressed) {
              api.logger.info?.(`CogentNexus v0.9.0 live policy reconciliation: abortFailuresCancelled=${live.abortFailuresCancelled} abortOutboxSuppressed=${live.abortOutboxSuppressed} failedOutboxSuppressed=${live.failedOutboxSuppressed} terminalRecoverySuppressed=${live.terminalRecoverySuppressed}`);
            }
            const native = await reconcileOpenClawNativeTasks(api, ctx, databasePath);
            if (native.fenced > 0 || native.failed > 0) {
              api.logger.info?.(`CogentNexus v0.9.0 native task fence: supported=${native.supported} scanned=${native.scanned} fenced=${native.fenced} failed=${native.failed}`);
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
        await tick();
        interval = setInterval(() => { void tick(); }, Math.max(1000, Math.min(config.ticketRecoveryPollMs ?? 5000, 30_000)));
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
