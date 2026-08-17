import { existsSync, mkdirSync, watch, type FSWatcher } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import entry, { STARTUP_RECOVERY_FENCE } from "./v090-final-entry.js";
import {
  deliverTicketOutbox,
  deliverWorkflowCompletion,
  dispatchTicketWorkflows,
  pendingWorkflowCompletions,
  reconcileTicketWorkflows,
} from "./index.js";
import {
  hasLegacyDirectPromotion,
  reconcileOpenClawNativeTasks,
  reconcileV090LiveState,
} from "./v090-entry.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import { prepareV090RecoveryState } from "./v090.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

const WRAPPED = Symbol.for("cogentnexus.v091.release-entry");
const ADAPTIVE_HOST_RECONCILIATION = Symbol.for("cogentnexus.v091.adaptive-host-reconciliation");
const EVENT_DRIVEN_SERVICE = Symbol.for("cogentnexus.v091.event-driven-service");
export const HOST_RECONCILIATION_ID = "cogentnexus-v090-host-reconciliation";
export const WORKFLOW_COMPLETION_ID = "cogentnexus-workflow-completion";
export const TICKET_RECOVERY_ID = "cogentnexus-ticket-recovery";
export const IDLE_RECONCILE_MS = 120_000;
export const ACTIVE_RECONCILE_MS = 15_000;
export const DEEP_RECONCILE_MS = 10 * 60_000;
export const SAFETY_SWEEP_MS = 10 * 60_000;

type StartupFence = ((ctx:any)=>Promise<void>)|undefined;
const pulseListeners = new Set<() => void>();

export function pulseManagedWorkers() {
  for (const listener of [...pulseListeners]) {
    try { listener(); } catch { /* each worker owns its own logging */ }
  }
}

export function managedIdleConfig(config: any) {
  if (config?.ticketFirst !== true || config?.enforcedMode !== true) return config ?? {};
  const floor = (value: unknown, minimum: number) => {
    const parsed = typeof value === "number" && Number.isFinite(value) ? value : minimum;
    return Math.max(minimum, parsed);
  };
  return {
    ...(config ?? {}),
    ticketRecoveryPollMs: floor(config?.ticketRecoveryPollMs, 60_000),
    ticketOutboxPollMs: floor(config?.ticketOutboxPollMs, 60_000),
    ticketDispatchPollMs: floor(config?.ticketDispatchPollMs, 60_000),
    completionPollMs: floor(config?.completionPollMs, 60_000),
    contextMaintenancePollMs: floor(config?.contextMaintenancePollMs, 30_000),
  };
}

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

export function idleWorkHint(databasePath: string): boolean {
  if (!existsSync(databasePath)) return false;
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    db.exec("PRAGMA busy_timeout=250");
    if (!tableExists(db, "tickets")) return false;
    if (db.prepare("SELECT 1 FROM tickets WHERE status NOT IN ('completed','failed','cancelled') LIMIT 1").get()) return true;
    if (tableExists(db, "ticket_outbox")
        && db.prepare("SELECT 1 FROM ticket_outbox WHERE delivery_status='pending' LIMIT 1").get()) return true;
    if (tableExists(db, "cnx_direct_recovery")
        && db.prepare("SELECT 1 FROM cnx_direct_recovery WHERE state IN ('pending','claimed','running','degraded') LIMIT 1").get()) return true;
    if (tableExists(db, "cnx_context_maintenance")
        && db.prepare("SELECT 1 FROM cnx_context_maintenance WHERE state IN ('pending','running','degraded') LIMIT 1").get()) return true;
    return false;
  } catch {
    return true;
  } finally {
    db.close();
  }
}

export function shouldRunDeepReconcile(forceDeep: boolean, hinted: boolean, elapsedMs: number): boolean {
  if (forceDeep) return true;
  return hinted && elapsedMs >= DEEP_RECONCILE_MS;
}

export function isAdaptiveHostReconciliation(service: any): boolean {
  return Boolean(service?.[ADAPTIVE_HOST_RECONCILIATION]);
}

export function isEventDrivenService(service: any): boolean {
  return Boolean(service?.[EVENT_DRIVEN_SERVICE]);
}

function createCoalescedRunner(work: () => Promise<void>, logger: any) {
  let active = false;
  let rerun = false;
  let stopped = false;
  const run = () => {
    if (stopped) return;
    if (active) { rerun = true; return; }
    active = true;
    void (async () => {
      try {
        do {
          rerun = false;
          await work();
        } while (rerun && !stopped);
      } catch (error) {
        logger.warn?.(`CogentNexus event worker failed: ${error instanceof Error ? error.message : String(error)}`);
      } finally {
        active = false;
      }
    })();
  };
  return { run, stop: () => { stopped = true; rerun = false; } };
}

function createEventDrivenWorkflowCompletion(api: any, config: any, startupFence:StartupFence) {
  let watcher: FSWatcher | undefined;
  let safety: ReturnType<typeof setTimeout> | undefined;
  let removePulse: (() => void) | undefined;
  let runner: ReturnType<typeof createCoalescedRunner> | undefined;
  const service: any = {
    id: WORKFLOW_COMPLETION_ID,
    start: async (ctx: any) => {
      await startupFence?.(ctx);
      const workspaceDir = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const workflowsDir = resolve(workspaceDir, ".cogent", "workflows");
      mkdirSync(workflowsDir, { recursive: true });
      const work = async () => {
        for (const item of pendingWorkflowCompletions(workspaceDir, new Date(), config.outboxDeliveryTimeoutMs ?? 300000)) {
          try { await deliverWorkflowCompletion(api, item.path, item.notice); }
          catch (error) { api.logger.warn(`CogentNexus workflow completion delivery failed for ${item.notice.taskId}: ${error instanceof Error ? error.message : String(error)}`); }
        }
      };
      runner = createCoalescedRunner(work, api.logger);
      const pulse = () => runner?.run();
      pulseListeners.add(pulse);
      removePulse = () => pulseListeners.delete(pulse);
      try {
        watcher = watch(workflowsDir, { recursive: true, persistent: false }, (_event, filename) => {
          if (!filename || String(filename).endsWith("completion.json")) pulse();
        });
        watcher.on("error", (error) => api.logger.warn(`CogentNexus workflow filesystem watcher degraded: ${error.message}`));
      } catch (error) {
        api.logger.warn(`CogentNexus workflow filesystem watcher unavailable: ${error instanceof Error ? error.message : String(error)}`);
      }
      const scheduleSafety = () => {
        safety = setTimeout(() => {
          pulse();
          scheduleSafety();
        }, SAFETY_SWEEP_MS);
        safety.unref?.();
      };
      await work();
      scheduleSafety();
    },
    stop: async () => {
      removePulse?.(); removePulse = undefined;
      runner?.stop(); runner = undefined;
      watcher?.close(); watcher = undefined;
      if (safety) clearTimeout(safety); safety = undefined;
    },
  };
  Object.defineProperty(service, EVENT_DRIVEN_SERVICE, { value: true });
  return service;
}

function createEventDrivenTicketRecovery(api: any, config: any, startupFence:StartupFence) {
  let safety: ReturnType<typeof setTimeout> | undefined;
  let removePulse: (() => void) | undefined;
  let runner: ReturnType<typeof createCoalescedRunner> | undefined;
  const service: any = {
    id: TICKET_RECOVERY_ID,
    start: async (ctx: any) => {
      await startupFence?.(ctx);
      const workspaceDir = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const databasePath = config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir);
      const store = new TicketStore(databasePath);
      const work = async () => {
        const undelivered = store.recoverUndeliveredDirect({ olderThanMs: config.directDeliveryTimeoutMs ?? 120000 });
        for (const item of undelivered) api.logger.warn(`CogentNexus promoted unconfirmed direct delivery ${item.ticketId} (${item.runId}) to durable recovery`);
        const recovered = store.recoverExpired();
        for (const item of recovered) api.logger.warn(`CogentNexus recovered expired Ticket ${item.ticketId} from worker ${item.previousWorkerId ?? "unknown"} generation ${item.previousLeaseGeneration}`);
        for (const item of reconcileTicketWorkflows({ workspaceDir, store, config })) api.logger.info?.(`CogentNexus Ticket ${item.ticketId} workflow action ${item.action}`);
        const dispatched = dispatchTicketWorkflows({ workspaceDir, store, config });
        if (!dispatched.admission.admitted) api.logger.info?.(`CogentNexus Ticket dispatch deferred: ${dispatched.admission.reasons.join(",")}`);
        for (const item of store.pendingOutbox(100, new Date(), config.outboxDeliveryTimeoutMs ?? 300000)) {
          try { await deliverTicketOutbox(api, store, item); }
          catch (error) { api.logger.warn(`CogentNexus Ticket completion delivery failed for ${item.ticketId}: ${error instanceof Error ? error.message : String(error)}`); }
        }
      };
      runner = createCoalescedRunner(work, api.logger);
      const pulse = () => runner?.run();
      pulseListeners.add(pulse);
      removePulse = () => pulseListeners.delete(pulse);
      const scheduleSafety = () => {
        safety = setTimeout(() => {
          if (idleWorkHint(databasePath)) pulse();
          scheduleSafety();
        }, SAFETY_SWEEP_MS);
        safety.unref?.();
      };
      await work();
      scheduleSafety();
    },
    stop: async () => {
      removePulse?.(); removePulse = undefined;
      runner?.stop(); runner = undefined;
      if (safety) clearTimeout(safety); safety = undefined;
    },
  };
  Object.defineProperty(service, EVENT_DRIVEN_SERVICE, { value: true });
  return service;
}

function createAdaptiveHostReconciliation(api: any, config: any, startupFence:StartupFence) {
  let stopped = false;
  let active = false;
  let rerun = false;
  let lastDeepReconcileAt = 0;
  let removePulse: (() => void) | undefined;

  const service: any = {
    id: HOST_RECONCILIATION_ID,
    start: async (ctx: any) => {
      await startupFence?.(ctx);
      const workspaceDir = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
      const tick = async (forceDeep = false) => {
        if (stopped) return;
        if (active) { rerun = true; return; }
        active = true;
        try {
          do {
            rerun = false;
            const now = Date.now();
            const hinted = idleWorkHint(databasePath);
            const deep = shouldRunDeepReconcile(forceDeep, hinted, now - lastDeepReconcileAt);
            forceDeep = false;
            if (!deep && !hinted) continue;
            if (deep) {
              await reconcileMissingOwnerSessions(api, databasePath, workspaceDir, config);
              lastDeepReconcileAt = now;
            }
            reconcileV090LiveState(databasePath);
            await reconcileOpenClawNativeTasks(api, ctx, databasePath);
            if (hasLegacyDirectPromotion(databasePath, config.admissionMinimumScore ?? 5)) {
              prepareV090RecoveryState(workspaceDir, config);
            }
          } while (rerun && !stopped);
        } catch (error) {
          api.logger.warn(`CogentNexus adaptive Host reconciliation failed: ${error instanceof Error ? error.message : String(error)}`);
        } finally {
          active = false;
        }
      };
      const pulse = () => { void tick(false); };
      pulseListeners.add(pulse);
      removePulse = () => pulseListeners.delete(pulse);
      await tick(true);
    },
    stop: async () => {
      stopped = true;
      removePulse?.(); removePulse = undefined;
    },
  };
  Object.defineProperty(service, ADAPTIVE_HOST_RECONCILIATION, { value: true });
  Object.defineProperty(service, EVENT_DRIVEN_SERVICE, { value: true });
  return service;
}

function wrapReleaseEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value: true });
  const register = entry.register?.bind(entry);

  entry.register = (api: any) => {
    const config = managedIdleConfig(api.pluginConfig ?? {});
    const proxy = Object.create(api);
    proxy.pluginConfig = config;

    const rawRegister = api.registerService?.bind(api);
    if (rawRegister) {
      proxy.registerService = (service: any) => {
        const startupFence = service?.[STARTUP_RECOVERY_FENCE] as StartupFence;
        if (service?.id === HOST_RECONCILIATION_ID) return rawRegister(createAdaptiveHostReconciliation(api, config, startupFence));
        if (service?.id === WORKFLOW_COMPLETION_ID) return rawRegister(createEventDrivenWorkflowCompletion(api, config, startupFence));
        if (service?.id === TICKET_RECOVERY_ID) return rawRegister(createEventDrivenTicketRecovery(api, config, startupFence));
        return rawRegister(service);
      };
    }

    const result = register?.(proxy);
    for (const eventName of ["before_prompt_build", "agent_end", "message_sent", "session_end", "after_compaction", "reply_dispatch"]) {
      api.on?.(eventName, () => { pulseManagedWorkers(); }, { priority: -1000 });
    }
    return result;
  };
}

wrapReleaseEntry();
export default entry;
