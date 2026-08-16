import entry from "./v090-entry.js";
import { installContextGuard } from "./v090-context-guard.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    register?.(api);
    // Register last so owner/native startup fences exist before a durable,
    // human-authorized context-maintenance row can invoke semantic compaction.
    installContextGuard(api, api, (api.pluginConfig ?? {}) as any);
  };
}

wrapFinalEntry();
export default entry;
