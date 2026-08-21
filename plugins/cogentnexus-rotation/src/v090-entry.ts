import { randomUUID } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { classifyDurableRequest } from "./admission.js";
import entry, { cancelSessionTickets, prepareV090RecoveryState } from "./v090.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import {
  recordSyntheticSpawn,
  settleSyntheticRun,
  staleSyntheticRuns,
} from "./v090-synthetic-registry.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type Config = {
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  admissionMinimumScore?: number;
  pythonCommand?: string;
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

type NativeFenceOwnerRow = {
  owner_session_key: string | null;
};

type NativeFenceOwnerScope = {
  sessionKey: string;
  agentId: string;
};

type PreRuntimeFenceResult = {
  owners: Awaited<ReturnType<typeof reconcileMissingOwnerSessions>>;
  live: ReturnType<typeof reconcileV090LiveState>;
  native: Awaited<ReturnType<typeof reconcileOpenClawNativeTasks>>;
};

const WRAPPED = Symbol.for("cogentnexus.v090.entry.host-reconciliation");
const LIVE_POLICY_PATCH = Symbol.for("cogentnexus.v090.live-policy-patch");
const CNX_PLUGIN_LABEL = "plugin:cogentnexus-rotation";
const ACTIVE_NATIVE_TASK_STATUSES = new Set(["queued", "running"]);
const TERMINAL_NATIVE_TICKET_STATUSES = new Set(["failed", "cancelled"]);
const RUNTIME_INSTANCE = randomUUID();

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

export function nativeFenceOwnerScopes(rows: ReadonlyArray<NativeFenceOwnerRow>): NativeFenceOwnerScope[] {
  const scopes = new Map<string, string>();
  for (const row of rows) {
    const sessionKey = (row.owner_session_key ?? "").trim();
    const match = /^agent:([^:]+):/u.exec(sessionKey);
    if (!sessionKey || !match?.[1]) continue;
    scopes.set(sessionKey, match[1]);
  }
  return [...scopes.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([sessionKey, agentId]) => ({ sessionKey, agentId }));
}

function readNativeFenceSnapshot(databasePath: string): {
  ownerScopes: NativeFenceOwnerScope[];
  ticketStatuses: Map<string, string>;
} {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly:true });
  const ticketStatuses = new Map<string, string>();
  const ownerRows: NativeFenceOwnerRow[] = [];
  try {
    const rows = db.prepare("SELECT ticket_id,status,owner_session_key FROM tickets").all() as Array<{
      ticket_id:string;
      status:string;
      owner_session_key:string | null;
    }>;
    for (const row of rows) {
      ticketStatuses.set(row.ticket_id, row.status);
      ownerRows.push({ owner_session_key:row.owner_session_key });
    }
  } finally {
    db.close();
  }
  return { ownerScopes:nativeFenceOwnerScopes(ownerRows), ticketStatuses };
}

function ticketIdFromNativeTask(task: NativeTaskView): string | undefined {
  for (const value of [task.title, task.runId, task.sourceId]) {
    const match = /\b(CNXT-[A-Za-z0-9-]+)\b/u.exec(value ?? "");
    if (match?.[1]) return match[1];
  }
  return undefined;
}

function cnxOwnedNativeTask(task: NativeTaskView) {
  return task.label === CNX_PLUGIN_LABEL
    || (task.runId ?? "").startsWith("cnx-")
    || (task.sourceId ?? "").startsWith("cnx-")
    || (task.runId ?? "").startsWith("cogent-");
}

export function shouldFenceNativeCnxTask(
  task: NativeTaskView,
  ticketStatuses: ReadonlyMap<string, string>,
): boolean {
  if (!ACTIVE_NATIVE_TASK_STATUSES.has(task.status ?? "")) return false;
  if (!cnxOwnedNativeTask(task)) return false;

  const ticketId = ticketIdFromNativeTask(task);
  if (ticketId && TERMINAL_NATIVE_TICKET_STATUSES.has(ticketStatuses.get(ticketId) ?? "")) return true;

  const title = task.title ?? "";
  if (/^\[CogentNexus Delivery: ticket:\d+\]/u.test(title)
      && /reached terminal status (?:failed|cancelled)\./u.test(title)) return true;
  if (/^\[CogentNexus Delivery: workflow:/u.test(title)
      && /reached terminal status (?:failed|blocked|cancelled)\./u.test(title)) return true;
  return false;
}

async function fenceStaleSyntheticRuns(
  api: any,
  ctx: any,
  databasePath: string,
): Promise<{ scanned:number; fenced:number; failed:number }> {
  const rows = staleSyntheticRuns(databasePath, RUNTIME_INSTANCE);
  if (rows.length === 0) return { scanned:0, fenced:0, failed:0 };
  const taskRuns = api.runtime?.tasks?.runs;
  let scanned = 0, fenced = 0, failed = 0;

  for (const row of rows) {
    scanned++;
    const agentId = /^agent:([^:]+):/u.exec(row.childSessionKey)?.[1] ?? "main";
    let rowFailed = false;
    if (taskRuns?.bindSession) {
      try {
        const bound = taskRuns.bindSession({ sessionKey:row.childSessionKey, agentId });
        for (const task of (bound.list?.() ?? []) as NativeTaskView[]) {
          if (!task.id || !ACTIVE_NATIVE_TASK_STATUSES.has(task.status ?? "")) continue;
          if (!cnxOwnedNativeTask(task) && task.runId !== row.runId && task.sourceId !== row.runId) continue;
          const result = await bound.cancel({ taskId:task.id, cfg:ctx.config ?? {} });
          if (!result?.cancelled && result?.reason !== "Task not found.") rowFailed = true;
        }
      } catch (error) {
        rowFailed = true;
        api.logger.warn?.(`CogentNexus stale synthetic fence could not cancel ${row.childSessionKey}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
    if (!rowFailed) {
      try { await api.runtime?.subagent?.deleteSession?.({ sessionKey:row.childSessionKey, deleteTranscript:true }); }
      catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        if (!/not found|unknown session|does not exist/iu.test(message)) {
          rowFailed = true;
          api.logger.warn?.(`CogentNexus stale synthetic fence could not delete ${row.childSessionKey}: ${message}`);
        }
      }
    }
    if (rowFailed) {
      failed++;
      continue;
    }
    settleSyntheticRun(databasePath, {
      runId:row.runId,
      state:"cancelled",
      outcome:"stale-runtime-fenced-before-recovery",
    });
    fenced++;
  }
  return { scanned, fenced, failed };
}

export async function reconcileOpenClawNativeTasks(
  api: any,
  ctx: any,
  databasePath: string,
): Promise<{
  supported:boolean;
  scanned:number;
  fenced:number;
  failed:number;
  syntheticScanned:number;
  syntheticFenced:number;
  syntheticFailed:number;
}> {
  const synthetic = await fenceStaleSyntheticRuns(api, ctx, databasePath);
  const taskRuns = api.runtime?.tasks?.runs;
  if (!taskRuns?.bindSession) return {
    supported:false, scanned:0, fenced:0, failed:0,
    syntheticScanned:synthetic.scanned, syntheticFenced:synthetic.fenced, syntheticFailed:synthetic.failed,
  };

  const { ownerScopes, ticketStatuses } = readNativeFenceSnapshot(databasePath);
  const mainKey = String(ctx.config?.session?.mainKey ?? "main").trim() || "main";
  const scopes = ownerScopes.length > 0
    ? ownerScopes
    : [{ sessionKey:`agent:main:${mainKey}`, agentId:"main" }];
  const seen = new Set<string>();
  let scanned = 0;
  let fenced = 0;
  let failed = 0;

  for (const { sessionKey, agentId } of scopes) {
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
  return {
    supported:true, scanned, fenced, failed,
    syntheticScanned:synthetic.scanned, syntheticFenced:synthetic.fenced, syntheticFailed:synthetic.failed,
  };
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
    let preStartPromise: Promise<PreRuntimeFenceResult> | undefined;

    const resolvePaths = (ctx: any) => {
      const workspaceDir = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
      return { workspaceDir, databasePath };
    };

    const runPreRuntimeFence = async (ctx: any): Promise<PreRuntimeFenceResult> => {
      const { workspaceDir, databasePath } = resolvePaths(ctx);
      const owners = await reconcileMissingOwnerSessions(api, databasePath, workspaceDir, config);
      const live = reconcileV090LiveState(databasePath);
      const native = await reconcileOpenClawNativeTasks(api, ctx, databasePath);
      const failures = owners.failed + owners.workflowFailures + native.failed + native.syntheticFailed;
      api.logger.info?.(`CogentNexus v0.9.0 pre-runtime fence: ownersChecked=${owners.checked} ownersDeleted=${owners.deleted} ownerFailures=${owners.failed} workflowFailures=${owners.workflowFailures} nativeScanned=${native.scanned} nativeFenced=${native.fenced} nativeFailed=${native.failed} syntheticScanned=${native.syntheticScanned} syntheticFenced=${native.syntheticFenced} syntheticFailed=${native.syntheticFailed}`);
      if (failures > 0) throw new Error(`CogentNexus pre-runtime fence incomplete (${failures} failures); inference-capable CNX services will remain stopped`);
      return { owners, live, native };
    };

    const ensurePreRuntimeFence = (ctx: any) => {
      preStartPromise ??= runPreRuntimeFence(ctx).catch((error) => {
        preStartPromise = undefined;
        throw error;
      });
      return preStartPromise;
    };

    const registrationProxy = Object.create(api);
    if (api.registerService) {
      registrationProxy.registerService = (service: any) => {
        if (!service || typeof service.start !== "function") return api.registerService(service);
        api.registerService({
          ...service,
          start: async (ctx: any) => {
            await ensurePreRuntimeFence(ctx);
            return service.start(ctx);
          },
        });
      };
    }

    register?.(registrationProxy);
    patchV090LivePolicy();

    const databasePathForHooks = () => {
      const workspaceDir = resolve(config.workspaceDir ?? process.cwd());
      return resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
    };

    api.on?.("subagent_spawned", (event: any, ctx: any) => {
      const childSessionKey = event?.childSessionKey ?? ctx?.childSessionKey;
      const runId = event?.runId ?? ctx?.runId;
      if (typeof childSessionKey !== "string" || !childSessionKey.includes(":subagent:cnx-") || typeof runId !== "string" || !runId) return;
      try {
        recordSyntheticSpawn(databasePathForHooks(), { runId, childSessionKey, runtimeInstance:RUNTIME_INSTANCE });
      } catch (error) {
        api.logger.warn?.(`CogentNexus synthetic registry spawn failed for ${childSessionKey}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }, { priority:2000, timeoutMs:5000 });

    api.on?.("subagent_ended", (event: any, ctx: any) => {
      const childSessionKey = event?.targetSessionKey ?? ctx?.childSessionKey;
      const runId = event?.runId ?? ctx?.runId;
      if (typeof childSessionKey !== "string" || !childSessionKey.includes(":subagent:cnx-")) return;
      if (event?.outcome === "reset") return;
      try {
        settleSyntheticRun(databasePathForHooks(), {
          runId:typeof runId === "string" ? runId : undefined,
          childSessionKey,
          state:event?.outcome === "killed" || event?.outcome === "deleted" ? "cancelled" : "done",
          outcome:String(event?.outcome ?? event?.reason ?? "ended"),
        });
      } catch (error) {
        api.logger.warn?.(`CogentNexus synthetic registry settlement failed for ${childSessionKey}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }, { priority:2000, timeoutMs:5000 });

    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    let lastOwnerReconcileAt = 0;
    api.registerService?.({
      id: "cogentnexus-v090-host-reconciliation",
      start: async (ctx: any) => {
        await ensurePreRuntimeFence(ctx);
        const { workspaceDir, databasePath } = resolvePaths(ctx);
        const tick = async () => {
          if (active) return;
          active = true;
          try {
            const current = Date.now();
            if (current - lastOwnerReconcileAt >= 30_000) {
              const owners = await reconcileMissingOwnerSessions(api, databasePath, workspaceDir, config);
              lastOwnerReconcileAt = current;
              if (owners.deleted > 0 || owners.failed > 0 || owners.workflowFailures > 0) {
                api.logger.info?.(`CogentNexus owner reconciliation: checked=${owners.checked} deleted=${owners.deleted} failed=${owners.failed} workflowFailures=${owners.workflowFailures}`);
              }
            }
            const live = reconcileV090LiveState(databasePath);
            if (live.abortFailuresCancelled || live.abortOutboxSuppressed || live.failedOutboxSuppressed || live.terminalRecoverySuppressed) {
              api.logger.info?.(`CogentNexus v0.9.0 live policy reconciliation: abortFailuresCancelled=${live.abortFailuresCancelled} abortOutboxSuppressed=${live.abortOutboxSuppressed} failedOutboxSuppressed=${live.failedOutboxSuppressed} terminalRecoverySuppressed=${live.terminalRecoverySuppressed}`);
            }
            const native = await reconcileOpenClawNativeTasks(api, ctx, databasePath);
            if (native.fenced > 0 || native.failed > 0 || native.syntheticFenced > 0 || native.syntheticFailed > 0) {
              api.logger.info?.(`CogentNexus v0.9.0 native task fence: supported=${native.supported} scanned=${native.scanned} fenced=${native.fenced} failed=${native.failed} syntheticScanned=${native.syntheticScanned} syntheticFenced=${native.syntheticFenced} syntheticFailed=${native.syntheticFailed}`);
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
