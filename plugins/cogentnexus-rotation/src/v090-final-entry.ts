import { resolve } from "node:path";
import entry, { reconcileOpenClawNativeTasks, reconcileV090LiveState } from "./v090-entry.js";
import { installContextGuard } from "./v090-context-guard.js";
import { reconcileMissingOwnerSessions } from "./v090-owner-reconcile.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";
import { defaultTicketDatabase } from "./ticket-store.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    const cfg = (api.pluginConfig ?? {}) as any;
    const proxy = createCnxRuntimeSafetyProxy(api, cfg);
    register?.(proxy);

    const contextRegistration = Object.create(proxy);
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
    installContextGuard(proxy, contextRegistration, cfg);
  };
}

wrapFinalEntry();
export default entry;
