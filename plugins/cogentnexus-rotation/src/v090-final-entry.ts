import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import entry, { reconcileOpenClawNativeTasks, reconcileV090LiveState } from "./v090-entry.js";
import { createAbortAuthorityApi } from "./v090-abort-authority.js";
import { createCompactionBoundaryApi, installPassiveCompactionObserver } from "./v090-compaction-boundary.js";
import { createContextMaintenanceApi } from "./v090-context-api.js";
import { installContextGuard } from "./v091-context-guard.js";
import { installNativeRestartRecoveryBoundary, reconcileNativeRestartRecoveryTickets } from "./v090-native-restart-boundary.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import { installRecoveryOrderAdmission } from "./v090-recovery-order.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";
import { isDashboardSession, prepareV090RecoveryState } from "./v090.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");
const DASHBOARD_DIRECT_SETTLEMENT = Symbol.for("cogentnexus.v090.dashboard-direct-settlement");

function recoverCrashStaleContextRows(databasePath:string) {
  const db=new DatabaseSync(databasePath),stamp=new Date().toISOString();
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000");
    const table=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_context_maintenance'").get();
    if(!table)return 0;
    return Number(db.prepare(`UPDATE cnx_context_maintenance
      SET state='degraded',next_attempt_at=?,last_error='Gateway restarted during context maintenance',last_action='restart-recovery',updated_at=?
      WHERE state='running' AND EXISTS(
        SELECT 1 FROM tickets t JOIN cnx_sessions s ON s.session_key=t.owner_session_key
        WHERE t.ticket_id=cnx_context_maintenance.ticket_id AND t.status='accepted'
          AND s.state='active' AND s.generation=cnx_context_maintenance.owner_generation)`)
      .run(stamp,stamp).changes);
  } finally {db.close();}
}

/**
 * Dashboard/webchat replies are delivered by the in-process agent stream rather
 * than an external channel dispatch. OpenClaw 2026.7.1 documents that outbound
 * message_sent does not carry runId and dashboard runs may not provide a usable
 * channel receipt. For an exact Dashboard Ticket, successful agent_end with
 * visible output is therefore the delivery authority: complete it immediately
 * instead of waiting for a channel receipt that can never correlate reliably.
 * External channel sessions keep the normal message_sent confirmation path.
 */
export function installDashboardDirectSettlement() {
  const prototype = TicketStore.prototype as any;
  if (prototype[DASHBOARD_DIRECT_SETTLEMENT]) return;
  Object.defineProperty(prototype, DASHBOARD_DIRECT_SETTLEMENT, { value:true });
  const finalize = TicketStore.prototype.finalizeDirectRun;
  TicketStore.prototype.finalizeDirectRun = function(input: Parameters<TicketStore["finalizeDirectRun"]>[0]) {
    if (input.success && input.expectsDelivery !== false) {
      const db = new DatabaseSync(this.databasePath, { readOnly:true });
      try {
        const row = db.prepare(`SELECT owner_session_key FROM tickets
          WHERE run_id=? AND status='accepted' AND workflow_eligible=0
          ORDER BY created_at DESC LIMIT 1`).get(input.runId) as {owner_session_key?:string} | undefined;
        if (row?.owner_session_key && isDashboardSession(row.owner_session_key)) {
          const settled = finalize.call(this, { ...input, expectsDelivery:false });
          return settled === "completed" ? "unchanged" : settled;
        }
      } finally { db.close(); }
    }
    return finalize.call(this, input);
  };
}

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    const cfg = (api.pluginConfig ?? {}) as any;
    const runtimeProxy = createCnxRuntimeSafetyProxy(api, cfg);
    const abortProxy = createAbortAuthorityApi(runtimeProxy, cfg);
    const proxy = createCompactionBoundaryApi(abortProxy);
    const rawRegister=api.registerService?.bind(api);
    let startupRecovery:Promise<void>|undefined;

    installNativeRestartRecoveryBoundary(api);

    if(rawRegister) {
      proxy.registerService=(service:any)=>{
        if(!service||typeof service.start!=="function")return rawRegister(service);
        return rawRegister({
          ...service,
          start:async(ctx:any)=>{
            startupRecovery??=(async()=>{
              const workspaceDir=resolve(cfg.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
              const databasePath=resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
              const nativeRestart=reconcileNativeRestartRecoveryTickets(databasePath);
              const prepared=prepareV090RecoveryState(workspaceDir,cfg);
              const contextRecovered=recoverCrashStaleContextRows(databasePath);
              proxy.logger.info?.(`CogentNexus crash-start recovery: nativeRestartCancelled=${nativeRestart.cancelled} nativeRestartOutboxSuppressed=${nativeRestart.outboxSuppressed} nativeRestartRecoverySuppressed=${nativeRestart.recoverySuppressed} directReopened=${prepared.reopened} cancelledLegacy=${prepared.cancelledLegacy} outboxReset=${prepared.outboxReset} workflowDeliveryReset=${prepared.workflowDeliveryReset} contextRowsRecovered=${contextRecovered}`);
            })().catch((error)=>{startupRecovery=undefined;throw error;});
            await startupRecovery;
            return service.start(ctx);
          },
        });
      };
    }

    register?.(proxy);
    installDashboardDirectSettlement();
    installRecoveryOrderAdmission(proxy,cfg);
    installPassiveCompactionObserver(api,cfg);

    const contextApi=createContextMaintenanceApi(abortProxy,cfg);
    const contextRegistration = Object.create(contextApi);
    if (proxy.registerService) {
      contextRegistration.registerService = (service:any) => {
        if (!/^cogentnexus-context-maintenance-v09[01]$/.test(String(service?.id ?? "")) || typeof service.start !== "function") {
          return proxy.registerService(service);
        }
        return proxy.registerService({
          ...service,
          start:async(ctx:any)=>{
            const workspaceDir=resolve(cfg.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
            const databasePath=resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
            const owners=await reconcileMissingOwnerSessions(runtimeProxy,databasePath,workspaceDir,cfg);
            const live=reconcileV090LiveState(databasePath);
            const native=await reconcileOpenClawNativeTasks(runtimeProxy,ctx,databasePath);
            const failures=owners.failed+owners.workflowFailures+native.failed+native.syntheticFailed;
            runtimeProxy.logger.info?.(`CogentNexus context pre-start fence: ownersSupported=${owners.supported} ownersChecked=${owners.checked} ownersDeleted=${owners.deleted} ownerFailures=${owners.failed} workflowFailures=${owners.workflowFailures} nativeFailed=${native.failed} syntheticFailed=${native.syntheticFailed} liveAbortCancelled=${live.abortFailuresCancelled}`);
            if(failures>0)throw new Error(`CogentNexus context pre-start fence incomplete (${failures} failures)`);
            return service.start(ctx);
          },
        });
      };
    }
    installContextGuard(contextApi, contextRegistration, cfg);
  };
}

wrapFinalEntry();
export default entry;
