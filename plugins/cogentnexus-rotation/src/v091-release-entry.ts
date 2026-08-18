import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import legacyEntry from "./v091-final-entry.js";
import {
  installV091DashboardVerifiedDelivery,
  type DashboardVerifiedDeliveryConfig,
} from "./v091-dashboard-verified-delivery.js";

const POLICY_BEGIN = "<!-- cogentnexus:begin -->";
const POLICY_END = "<!-- cogentnexus:end -->";

type HostControllerState = {
  schemaVersion?: number;
  mode?: string;
  generation?: number;
};

type HostAuthority = {
  authorized: boolean;
  reason: "managed" | "host-activation-staged" | "passthrough" | "maintenance" | "missing" | "invalid";
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

function managedPolicyStaged(workspace: string) {
  const path = resolve(workspace, "AGENTS.md");
  if (!existsSync(path)) return false;
  try {
    const text = readFileSync(path, "utf8");
    return text.includes(POLICY_BEGIN) && text.includes(POLICY_END);
  } catch {
    return false;
  }
}

/**
 * Host authority is the single activation boundary for every inference-capable
 * CogentNexus plugin surface.
 *
 * Normal steady-state activation requires controller.mode=managed. During the
 * transactional enable sequence Host intentionally applies the managed policy
 * after completing its durable pre-recovery classification and immediately
 * before enabling the plugin. That policy marker is therefore the bounded
 * activation-stage proof while controller.mode is still passthrough.
 *
 * A native OpenClaw plugin install/hot-reload in clean PASSTHROUGH has neither
 * managed mode nor the staged policy marker, so registration is inert and no
 * legacy startup recovery can mutate Tickets or wake inference.
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
  if (managedPolicyStaged(workspace)) {
    return { authorized: true, reason: "host-activation-staged", mode, generation, controllerPath };
  }
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
 * Host authority is checked before the compatibility chain is registered. This
 * makes a native plugin install/hot-reload harmless while CogentNexus is in
 * PASSTHROUGH: no hooks, services, startup recovery, Ticket mutation, or
 * inference-capable recovery worker becomes active.
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
    if (authority.reason === "host-activation-staged") {
      api.logger.info?.("CogentNexus v0.9.1 runtime registration authorized by Host transactional activation stage");
    }
    const register = (legacyEntry as { register?: (runtimeApi: OpenClawPluginApi) => void | Promise<void> }).register;
    if (typeof register !== "function") {
      throw new Error("CogentNexus v0.9.1 compatibility entry does not expose register(api)");
    }
    const installVerifiedDelivery = () => installV091DashboardVerifiedDelivery(
      api,
      (api.pluginConfig ?? {}) as DashboardVerifiedDeliveryConfig,
    );
    const registered = register(api);
    if (registered && typeof (registered as Promise<void>).then === "function") {
      return Promise.resolve(registered).then(installVerifiedDelivery);
    }
    installVerifiedDelivery();
  },
});

export default releaseEntry;
