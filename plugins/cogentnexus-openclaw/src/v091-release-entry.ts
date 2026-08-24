import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import legacyEntry from "./v091-final-entry.js";
import {
  installV091DashboardVerifiedDelivery,
  type DashboardVerifiedDeliveryConfig,
} from "./v091-dashboard-verified-delivery.js";
import { installV091DirectModelCallLease } from "./v091-direct-model-call-lease.js";
import { installV092DurableDeliveryBoundary } from "./v092-durable-delivery-boundary.js";
import { installV095DirectRecoveryLaneFence } from "./v095-direct-recovery.js";
import { installV097DirectRecoveryStartupLiveness } from "./v097-direct-recovery-liveness.js";
import { installV099NativeRestartOwnershipFence } from "./v099-native-restart-ownership.js";

type HostControllerState = {
  schemaVersion?: number;
  mode?: string;
  generation?: number;
};

type HostAuthority = {
  authorized: boolean;
  reason: "managed" | "passthrough" | "maintenance" | "missing" | "invalid";
  mode?: string;
  generation?: number;
  controllerPath: string;
};

function pluginWorkspace(api: OpenClawPluginApi) {
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  const configured = typeof cfg.workspaceDir === "string" && cfg.workspaceDir.trim() ? cfg.workspaceDir.trim() : undefined;
  const runtimeWorkspace = typeof (api as any)?.config?.agents?.defaults?.workspace === "string"
    ? String((api as any).config.agents.defaults.workspace).trim()
    : undefined;
  return resolve(configured ?? runtimeWorkspace ?? join(homedir(), ".openclaw", "workspace"));
}

function pluginCogentRoot(api: OpenClawPluginApi) {
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  return resolve(
    typeof cfg.cogentNexusOpenClawRoot === "string" && cfg.cogentNexusOpenClawRoot.trim()
      ? cfg.cogentNexusOpenClawRoot.trim()
      : join(pluginWorkspace(api), ".cogentnexus-openclaw"),
  );
}

/**
 * Host controller.mode=managed is the only activation authority for every
 * inference-capable CogentNexus-OpenClaw plugin surface.
 *
 * No policy marker, plugin config bit, installer phase, or Gateway hot-reload
 * can substitute for that durable Host commit. This deliberately makes a
 * power loss during transactional enable fail closed: until Host commits
 * MANAGED, a restarted Gateway can discover the plugin but cannot register any
 * CogentNexus-OpenClaw hook, service, recovery worker, or Ticket mutation surface.
 */
export function hostPluginAuthority(api: OpenClawPluginApi): HostAuthority {
  const root = pluginCogentRoot(api);
  const controllerPath = resolve(root, "host", "controller.json");
  if (!existsSync(controllerPath)) return { authorized: false, reason: "missing", controllerPath };
  let state: HostControllerState;
  try {
    state = JSON.parse(readFileSync(controllerPath, "utf8")) as HostControllerState;
  } catch {
    return { authorized: false, reason: "invalid", controllerPath };
  }
  const mode = typeof state?.mode === "string" ? state.mode : undefined;
  const generation = Number.isSafeInteger(state?.generation) ? Number(state.generation) : undefined;
  if (state?.schemaVersion !== 1 || !["managed", "passthrough", "maintenance"].includes(mode ?? "")) {
    return { authorized: false, reason: "invalid", mode, generation, controllerPath };
  }
  if (mode === "managed") return { authorized: true, reason: "managed", mode, generation, controllerPath };
  if (mode === "maintenance") return { authorized: false, reason: "maintenance", mode, generation, controllerPath };
  return { authorized: false, reason: "passthrough", mode, generation, controllerPath };
}

/**
 * v0.9.1 public mixed-plugin boundary.
 *
 * CogentNexus-OpenClaw registers tools together with hooks and services, so the shipped
 * runtime entry must use OpenClaw's mixed-plugin contract rather than the
 * defineToolPlugin metadata generator. Configuration remains authoritative in
 * openclaw.plugin.json, which OpenClaw reads before runtime code is loaded.
 *
 * Host authority is checked before the compatibility chain is registered. A
 * native plugin install/hot-reload in PASSTHROUGH or MAINTENANCE is therefore
 * inert even when the plugin is temporarily enabled by OpenClaw itself.
 */
const releaseEntry: ReturnType<typeof definePluginEntry> = definePluginEntry({
  id: "cogentnexus-openclaw",
  name: "CogentNexus-OpenClaw Bridge",
  description:
    "Ticket-first OpenClaw bridge for CogentNexus-OpenClaw Host-managed continuity, durable execution, recovery, context handoff, and verified delivery.",
  register(api: OpenClawPluginApi) {
    const authority = hostPluginAuthority(api);
    if (!authority.authorized) {
      api.logger.info?.(
        `CogentNexus-OpenClaw v0.9.1 runtime registration suppressed: Host authority=${authority.reason} mode=${authority.mode ?? "unknown"}`,
      );
      return;
    }
    const register = (legacyEntry as { register?: (runtimeApi: OpenClawPluginApi) => void | Promise<void> }).register;
    if (typeof register !== "function") {
      throw new Error("CogentNexus-OpenClaw v0.9.1 compatibility entry does not expose register(api)");
    }
    const config = (api.pluginConfig ?? {}) as DashboardVerifiedDeliveryConfig;
    // OpenClaw 2026.7.1-2 can start its own main-session restart recovery
    // concurrently with Host-owned CogentNexus-OpenClaw Direct Recovery. Consume only
    // the exact native restart system turn when durable CNXCLAW ownership exists,
    // before the legacy before_agent_run Ticket-first gate can see it.
    installV099NativeRestartOwnershipFence(api, config);
    const installManagedRuntimeGuards = () => {
      // Once direct_result is durable, transport owns all remaining retries;
      // legacy delivery timeout recovery must not regenerate inference.
      installV092DurableDeliveryBoundary();
      // A cnx_direct_recovery row durably owns the Direct lane. Legacy Host
      // reconciliation must never promote that Ticket into workflow execution.
      installV095DirectRecoveryLaneFence(
        resolve(pluginCogentRoot(api), "runtime", "cogentnexus-openclaw.sqlite3"),
      );
      // The model-call lease is observation-only. It records a bounded provider
      // call deadline; only the external Host may act on an expired lease.
      installV091DirectModelCallLease(api);
      installV091DashboardVerifiedDelivery(api, config);
    };
    const registered = register(api);
    // Test A v9 proved that the Direct Recovery service can start while the
    // owner-session/model-call readiness fences are still settling after a
    // Host-driven Gateway restart. Register a durable-work-only pulse bridge
    // after the legacy services so the pending recovery cannot become unwoken.
    installV097DirectRecoveryStartupLiveness(api, config);
    if (registered && typeof (registered as Promise<void>).then === "function") {
      return Promise.resolve(registered).then(installManagedRuntimeGuards);
    }
    installManagedRuntimeGuards();
  },
});

export default releaseEntry;
