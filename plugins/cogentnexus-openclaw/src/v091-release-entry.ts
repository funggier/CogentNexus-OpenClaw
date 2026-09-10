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
import { installV095InferenceHookBridge } from "./v095-inference-hook-bridge.js";
import { registerDiscordDeliveryAdapter } from "./v095-delivery-discord.js";
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

function isDiscordContext(ctx: any) {
  return ctx?.channel === "discord" || ctx?.messageProvider === "discord";
}

const LEGACY_DISCORD_DELIVERY_HOOKS = new Set([
  "reply_dispatch",
  "reply_payload_sending",
  "message_sent",
  "before_message_write",
]);

function withDiscordLegacyDeliveryFence(api: OpenClawPluginApi, pluginConfig: Record<string, unknown>) {
  const runtimeApi: any = {
    ...api,
    pluginConfig,
    on: (name: string, handler: (...args: any[]) => any, options?: any) => {
      if (!LEGACY_DISCORD_DELIVERY_HOOKS.has(name)) {
        return api.on(name as any, handler as any, options);
      }
      const fenced = (...args: any[]) => {
        const ctx = args[1];
        if (isDiscordContext(ctx)) return undefined;
        return handler(...args);
      };
      return api.on(name as any, fenced as any, options);
    },
  };
  return runtimeApi;
}

/**
 * Host controller.mode=managed/passthrough authorizes the CogentNexus-OpenClaw
 * plugin surface; provider/auth/routing ownership remains an OpenClaw concern.
 *
 * Neither provider mode nor provider selection is a capability switch. A valid
 * Host authority commit therefore allows the same Ticket, continuity, recovery,
 * delivery, and workflow surfaces regardless of which provider OpenClaw routes
 * an inference attempt to.
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
  if (mode === "managed" || mode === "passthrough") return { authorized: true, reason: mode, mode, generation, controllerPath };
  if (mode === "maintenance") return { authorized: false, reason: "maintenance", mode, generation, controllerPath };
  return { authorized: false, reason: "passthrough", mode, generation, controllerPath };
}

/**
 * v0.9.1 public mixed-plugin boundary.
 *
 * Host authority controls whether the plugin is active. Provider ownership is
 * deliberately not translated into capability suppression: PASSTHROUGH means
 * OpenClaw owns provider/auth/routing, while CogentNexus-OpenClaw continuity,
 * durable Ticket/recovery, delivery, and workflow capabilities remain active.
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

    const config = {
      ...((api.pluginConfig ?? {}) as DashboardVerifiedDeliveryConfig),
      ...(authority.reason === "passthrough" ? { providerMode: undefined } : { providerMode: "managed" as const }),
    };

    // ProviderMode is retained only as compatibility metadata. The legacy
    // capability gates inspect it, so PASSTHROUGH is normalized to undefined
    // here rather than being allowed to disable CNX continuity/recovery.
    // Legacy Discord delivery hooks are fenced at this boundary so Discord has
    // exactly one v0.9.5 delivery authority: the canonical adapter below.
    const runtimeApi = withDiscordLegacyDeliveryFence(api, config);

    // OpenClaw 2026.7.1-2 can start its own main-session restart recovery
    // concurrently with Host-owned CogentNexus-OpenClaw Direct Recovery. Consume only
    // the exact native restart system turn when durable CNX ownership exists, before
    // the legacy before_agent_run Ticket-first gate can see it.
    installV099NativeRestartOwnershipFence(api, config);

    const installManagedRuntimeGuards = () => {
      // Provider/auth/routing remain outside CNX authority, but continuity and
      // durable recovery surfaces are valid in both managed and pass-through mode.
      installV092DurableDeliveryBoundary();
      const ticketDatabase = resolve(pluginCogentRoot(api), "runtime", "cogentnexus-openclaw.sqlite3");
      if (existsSync(ticketDatabase)) installV095DirectRecoveryLaneFence(ticketDatabase);
      installV091DirectModelCallLease(api);
      installV095InferenceHookBridge(runtimeApi);
      installV091DashboardVerifiedDelivery(runtimeApi, config);
      registerDiscordDeliveryAdapter(api);
    };

    const registered = register(runtimeApi);
    // Keep startup-liveness ownership provider-independent: a Host restart must
    // not strand a durable direct-recovery lane merely because OpenClaw uses a
    // pass-through provider route.
    installV097DirectRecoveryStartupLiveness(api, config);
    if (registered && typeof (registered as Promise<void>).then === "function") {
      return Promise.resolve(registered).then(installManagedRuntimeGuards);
    }
    installManagedRuntimeGuards();
  },
});

export default releaseEntry;
