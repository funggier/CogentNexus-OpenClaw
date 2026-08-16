import entry from "./v090-entry.js";
import { installContextSafety } from "./v090-context-safety.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    register?.(api);
    // Register last so all ownership/native-task startup fences are installed
    // before context maintenance can process a durable, human-authorized row.
    installContextSafety(api, api, (api.pluginConfig ?? {}) as any);
  };
}

wrapFinalEntry();
export default entry;
