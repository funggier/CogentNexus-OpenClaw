import entry from "./v090-entry.js";
import { installContextGuard } from "./v090-context-guard.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";

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
    // Register last so owner/native startup fences exist before a durable,
    // human-authorized context-maintenance row can invoke semantic compaction.
    installContextGuard(proxy, proxy, cfg);
  };
}

wrapFinalEntry();
export default entry;
