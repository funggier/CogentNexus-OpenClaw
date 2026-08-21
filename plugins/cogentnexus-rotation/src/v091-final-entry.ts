import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import entry from "./v090-final-entry.js";
import {
  hasLegacyDirectPromotion,
  reconcileOpenClawNativeTasks,
  reconcileV090LiveState,
} from "./v090-entry.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import { prepareV090RecoveryState } from "./v090.js";
import { defaultTicketDatabase } from "./ticket-store.js";

const WRAPPED = Symbol.for("cogentnexus.v091.release-entry");
const HOST_RECONCILIATION_ID = "cogentnexus-v090-host-reconciliation";
export const IDLE_RECONCILE_MS = 120_000;
export const ACTIVE_RECONCILE_MS = 15_000;
export const DEEP_RECONCILE_MS = 10 * 60_000;

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

/**
 * Read-only idle gate. No durable mutation is performed merely because a timer
 * fired. Heavy recovery reconciliation runs only when actionable work is visible
 * or during the infrequent deep safety sweep.
 */
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
    // A locked/older schema is not proof of quiescence. Let the bounded safety
    // sweep inspect it rather than silently suppressing recovery.
    return true;
  } finally {
    db.close();
  }
}

function createAdaptiveHostReconciliation(api: any, config: any) {
  let timer: ReturnType<typeof setTimeout> | undefined;
  let active = false;
  let stopped = false;
  let lastDeepReconcileAt = 0;

  return {
    id: HOST_RECONCILIATION_ID,
    start: async (ctx: any) => {
      const workspaceDir = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));

      const tick = async (forceDeep = false): Promise<boolean> => {
        if (active || stopped) return false;
        active = true;
        try {
          const now = Date.now();
          const deep = forceDeep || now - lastDeepReconcileAt >= DEEP_RECONCILE_MS;
          const hinted = idleWorkHint(databasePath);
          if (!deep && !hinted) return false;

          let activity = hinted;
          if (deep) {
            const owners = await reconcileMissingOwnerSessions(api, databasePath, workspaceDir, config);
            lastDeepReconcileAt = now;
            const ownerActivity = owners.deleted > 0 || owners.failed > 0 || owners.workflowFailures > 0;
            activity ||= ownerActivity;
            if (ownerActivity) {
              api.logger.info?.(`CogentNexus owner reconciliation: checked=${owners.checked} deleted=${owners.deleted} failed=${owners.failed} workflowFailures=${owners.workflowFailures}`);
            }
          }

          const live = reconcileV090LiveState(databasePath);
          const liveActivity = Boolean(live.abortFailuresCancelled || live.abortOutboxSuppressed || live.failedOutboxSuppressed || live.terminalRecoverySuppressed);
          activity ||= liveActivity;
          if (liveActivity) {
            api.logger.info?.(`CogentNexus live policy reconciliation: abortFailuresCancelled=${live.abortFailuresCancelled} abortOutboxSuppressed=${live.abortOutboxSuppressed} failedOutboxSuppressed=${live.failedOutboxSuppressed} terminalRecoverySuppressed=${live.terminalRecoverySuppressed}`);
          }

          if (deep || hinted) {
            const native = await reconcileOpenClawNativeTasks(api, ctx, databasePath);
            const nativeActivity = native.fenced > 0 || native.failed > 0 || native.syntheticFenced > 0 || native.syntheticFailed > 0;
            activity ||= nativeActivity;
            if (nativeActivity) {
              api.logger.info?.(`CogentNexus native task fence: supported=${native.supported} scanned=${native.scanned} fenced=${native.fenced} failed=${native.failed} syntheticScanned=${native.syntheticScanned} syntheticFenced=${native.syntheticFenced} syntheticFailed=${native.syntheticFailed}`);
            }
          }

          if (hasLegacyDirectPromotion(databasePath, config.admissionMinimumScore ?? 5)) {
            const result = prepareV090RecoveryState(workspaceDir, config);
            const promoted = result.reopened > 0 || result.cancelledLegacy > 0;
            activity ||= promoted;
            if (promoted) {
              api.logger.info?.(`CogentNexus reconciled Direct Tickets: reopened=${result.reopened} cancelledLegacy=${result.cancelledLegacy}`);
            }
          }
          return activity;
        } catch (error) {
          api.logger.warn(`CogentNexus adaptive Host reconciliation failed: ${error instanceof Error ? error.message : String(error)}`);
          return true;
        } finally {
          active = false;
        }
      };

      const schedule = (delay: number) => {
        if (stopped) return;
        timer = setTimeout(() => {
          void tick(false).then((activity) => schedule(activity ? ACTIVE_RECONCILE_MS : IDLE_RECONCILE_MS));
        }, delay);
        timer.unref?.();
      };

      const startupActivity = await tick(true);
      schedule(startupActivity ? ACTIVE_RECONCILE_MS : IDLE_RECONCILE_MS);
    },
    stop: async () => {
      stopped = true;
      if (timer) clearTimeout(timer);
      timer = undefined;
    },
  };
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
        if (service?.id === HOST_RECONCILIATION_ID) {
          return rawRegister(createAdaptiveHostReconciliation(api, config));
        }
        return rawRegister(service);
      };
    }
    return register?.(proxy);
  };
}

wrapReleaseEntry();
export default entry;
