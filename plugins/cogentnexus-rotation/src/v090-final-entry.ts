import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import entry, { reconcileOpenClawNativeTasks, reconcileV090LiveState } from "./v090-entry.js";
import { createContextMaintenanceApi } from "./v090-context-api.js";
import { installContextGuard } from "./v090-context-guard.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";
import { prepareV090RecoveryState } from "./v090.js";
import { defaultTicketDatabase } from "./ticket-store.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");

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

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    const cfg = (api.pluginConfig ?? {}) as any;
    const proxy = createCnxRuntimeSafetyProxy(api, cfg);
    const rawRegister=api.registerService?.bind(api);
    let startupRecovery:Promise<void>|undefined;

    if(rawRegister) {
      proxy.registerService=(service:any)=>{
        if(!service||typeof service.start!=="function")return rawRegister(service);
        return rawRegister({
          ...service,
          start:async(ctx:any)=>{
            startupRecovery??=(async()=>{
              const workspaceDir=resolve(cfg.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
              const databasePath=resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
              const prepared=prepareV090RecoveryState(workspaceDir,cfg);
              const contextRecovered=recoverCrashStaleContextRows(databasePath);
              proxy.logger.info?.(`CogentNexus crash-start recovery: directReopened=${prepared.reopened} cancelledLegacy=${prepared.cancelledLegacy} outboxReset=${prepared.outboxReset} workflowDeliveryReset=${prepared.workflowDeliveryReset} contextRowsRecovered=${contextRecovered}`);
            })().catch((error)=>{startupRecovery=undefined;throw error;});
            await startupRecovery;
            return service.start(ctx);
          },
        });
      };
    }

    register?.(proxy);

    // Context maintenance intentionally sees CNX generation as the ownership
    // boundary. OpenClaw may rotate physical sessionId during a user/manual
    // Compact; that is a transcript revision, not Reset/Delete/Stop.
    const contextApi=createContextMaintenanceApi(proxy);
    const contextRegistration = Object.create(contextApi);
    if (proxy.registerService) {
      contextRegistration.registerService = (service:any) => {
        if (service?.id !== "cogentnexus-context-maintenance-v090" || typeof service.start !== "function") {
          return proxy.registerService(service);
        }
        return proxy.registerService({
          ...service,
          start:async(ctx:any)=>{
            const workspaceDir=resolve(cfg.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
            const databasePath=resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
            const owners=await reconcileMissingOwnerSessions(proxy,databasePath,workspaceDir,cfg);
            const live=reconcileV090LiveState(databasePath);
            const native=await reconcileOpenClawNativeTasks(proxy,ctx,databasePath);
            const failures=owners.failed+owners.workflowFailures+native.failed+native.syntheticFailed;
            proxy.logger.info?.(`CogentNexus context pre-start fence: ownersChecked=${owners.checked} ownersDeleted=${owners.deleted} ownerFailures=${owners.failed} workflowFailures=${owners.workflowFailures} nativeFailed=${native.failed} syntheticFailed=${native.syntheticFailed} liveAbortCancelled=${live.abortFailuresCancelled}`);
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
