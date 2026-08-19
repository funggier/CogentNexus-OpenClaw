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

/**
 * Host controller.mode=managed is the only activation authority for every
 * inference-capable CogentNexus plugin surface.
 *
 * No policy marker, plugin config bit, installer phase, or Gateway hot-reload
 * can substitute for that durable Host commit. This deliberately makes a
 * power loss during transactional enable fail closed: until Host commits
 * MANAGED, a restarted Gateway can discover the plugin but cannot register any
 * CogentNexus hook, service, recovery worker, or Ticket mutation surface.
 */
export function hostPluginAuthority(api: OpenClawPluginApi): HostAuthority {
  const workspace = pluginWorkspace(api);
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  const root = resolve(
    typeof cfg.cogentRoot === "string" && cfg.cogentRoot.trim()
      ? cfg.cogentRoot.trim()
      : join(workspace, ".cogent"),
  );
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
 * CogentNexus registers tools together with hooks and services, so the shipped
 * runtime entry must use OpenClaw's mixed-plugin contract rather than the
 * defineToolPlugin metadata generator. Configuration remains authoritative in
 * openclaw.plugin.json, which OpenClaw reads before runtime code is loaded.
 *
 * Host authority is checked before the compatibility chain is registered. A
 * native plugin install/hot-reload in PASSTHROUGH or MAINTENANCE is therefore
 * inert even when the plugin is temporarily enabled by OpenClaw itself.
 */
const releaseEntry: ReturnType<typeof definePluginEntry> = definePluginEntry({
  id: "cogentnexus-rotation",
  name: "CogentNexus OpenClaw Bridge",
  description:
    "Ticket-first OpenClaw bridge for CogentNexus Host-managed continuity, durable execution, recovery, context handoff, and verified delivery.",
  register(api: OpenClawPluginApi) {
    const authority = hostPluginAuthority(api);
    if (!authority.authorized) {
      api.logger.info?.(
        `CogentNexus v0.9.1 runtime registration suppressed: Host authority=${authority.reason} mode=${authority.mode ?? "unknown"}`,
      );
      return;
    }
    const register = (legacyEntry as { register?: (runtimeApi: OpenClawPluginApi) => void | Promise<void> }).register;
    if (typeof register !== "function") {
      throw new Error("CogentNexus v0.9.1 compatibility entry does not expose register(api)");
    }
    const installManagedRuntimeGuards = () => {
      // Once direct_result is durable, transport owns all remaining retries;
      // legacy delivery timeout recovery must not regenerate inference.
      installV092DurableDeliveryBoundary();
      // The model-call lease is observation-only. It records a bounded provider
      // call deadline; only the external Host may act on an expired lease.
      installV091DirectModelCallLease(api);
      installV091DashboardVerifiedDelivery(
        api,
        (api.pluginConfig ?? {}) as DashboardVerifiedDeliveryConfig,
      );
    };
    const registered = register(api);
    if (registered && typeof (registered as Promise<void>).then === "function") {
      return Promise.resolve(registered).then(installManagedRuntimeGuards);
    }
    installManagedRuntimeGuards();
  },
});

export default releaseEntry;