import { resolve } from "node:path";
import entry from "./v090-entry.js";
import { installContextGuard } from "./v090-context-guard.js";
import { externalizeOversizedSyntheticPayload } from "./v090-synthetic-payload.js";

const WRAPPED = Symbol.for("cogentnexus.v090.final-entry");

function wrapFinalEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value:true });
  const register = entry.register?.bind(entry);
  entry.register = (api:any) => {
    const cfg = (api.pluginConfig ?? {}) as any;
    const workspaceDir = resolve(cfg.workspaceDir ?? process.cwd());
    const proxy = Object.create(api);
    const runtime = Object.create(api.runtime ?? {});
    const originalSubagent = api.runtime?.subagent;
    if (originalSubagent?.run) {
      const subagent = Object.create(originalSubagent);
      subagent.run = async (input:any) => {
        const sessionKey = String(input?.sessionKey ?? "");
        const message = typeof input?.message === "string" ? input.message : "";
        if (!sessionKey.includes(":subagent:cnx-") || !/\[CogentNexus Internal/iu.test(message)) {
          return originalSubagent.run(input);
        }
        const bounded = externalizeOversizedSyntheticPayload({ workspaceDir, sessionKey, message, config:cfg });
        if (bounded.externalized) {
          api.logger.info?.(`CogentNexus externalized oversized hidden payload for ${sessionKey}: chunks=${bounded.chunkCount} sha256=${bounded.sha256?.slice(0,16)}`);
        }
        return originalSubagent.run({ ...input, message:bounded.message });
      };
      runtime.subagent = subagent;
      proxy.runtime = runtime;
    }

    register?.(proxy);
    // Register last so owner/native startup fences exist before a durable,
    // human-authorized context-maintenance row can invoke semantic compaction.
    installContextGuard(proxy, proxy, cfg);
  };
}

wrapFinalEntry();
export default entry;
