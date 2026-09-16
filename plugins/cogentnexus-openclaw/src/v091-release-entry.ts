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
import { registerWebchatDeliveryAdapter } from "./v095-delivery-webchat.js";
import { installV092DurableDeliveryBoundary } from "./v092-durable-delivery-boundary.js";
import { installV095DirectRecoveryLaneFence } from "./v095-direct-recovery.js";
import { installV097DirectRecoveryStartupLiveness } from "./v097-direct-recovery-liveness.js";
import { installV099NativeRestartOwnershipFence } from "./v099-native-restart-ownership.js";


type HostControllerState = {
  schemaVersion?: number;
  mode?: string;
  cnxMode?: string;
  generation?: number;
};

const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set([1, 2]);
const CANONICAL_TO_LEGACY_MODE: Record<string, string> = {
  active: "managed",
  disabled: "passthrough",
  maintenance: "maintenance",
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

function isWebchatContext(ctx: any) {
  return ctx?.channel === "webchat" || ctx?.messageProvider === "webchat";
}

const LEGACY_DISCORD_DELIVERY_HOOKS = new Set([
  "reply_dispatch",
  "reply_payload_sending",
  "message_sent",
  "before_message_write",
]);

const LEGACY_WEBCHAT_DELIVERY_HOOKS = LEGACY_DISCORD_DELIVERY_HOOKS;

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

function withWebchatLegacyDeliveryFence(api: OpenClawPluginApi, pluginConfig: Record<string, unknown>) {
  const runtimeApi: any = {
    ...api,
    pluginConfig,
    on: (name: string, handler: (...args: any[]) => any, options?: any) => {
      if (!LEGACY_WEBCHAT_DELIVERY_HOOKS.has(name)) {
        return api.on(name as any, handler as any, options);
      }
      const fenced = (...args: any[]) => {
        const ctx = args[1];
        if (isWebchatContext(ctx)) return undefined;
        return handler(...args);
      };
      return api.on(name as any, fenced as any, options);
    },
  };
  return runtimeApi;
}

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
  const schemaVersion = state?.schemaVersion;
  if (typeof schemaVersion !== "number" || !Number.isInteger(schemaVersion) || !SUPPORTED_CONTROLLER_SCHEMA_VERSIONS.has(schemaVersion)) {
    return { authorized: false, reason: "invalid", mode, generation, controllerPath };
  }
  const effectiveMode = schemaVersion === 2
    ? (typeof state?.cnxMode === "string" ? CANONICAL_TO_LEGACY_MODE[state.cnxMode] : undefined)
    : mode;
  if (!effectiveMode || !["managed", "passthrough", "maintenance"].includes(effectiveMode)) {
    return { authorized: false, reason: "invalid", mode: effectiveMode, generation, controllerPath };
  }
  if (effectiveMode === "managed" || effectiveMode === "passthrough") return { authorized: true, reason: effectiveMode, mode: effectiveMode, generation, controllerPath };
  if (effectiveMode === "maintenance") return { authorized: false, reason: "maintenance", mode: effectiveMode, generation, controllerPath };
  return { authorized: false, reason: "passthrough", mode, generation, controllerPath };
}

/**
 * v0.9.5 mixed-plugin boundary with registry wiring fix.
 *
 * CNX-374 root cause: OpenClaw 2026.7.1-2 host checks the plugin DEFINITION's
 * `hooks.allowConversationAccess` property (entry?.hooks) to gate conversation
 * hooks such as `before_agent_run`. This is NOT the runtime config
 * `plugins.entries.<id>.hooks.allowConversationAccess` (which only feeds
 * pluginConfig, not the gate). When the definition lacks `hooks`, the host
 * blocks dynamic registration before it reaches the global hook registry,
 * producing `hookCount: 0` and leaving the Dashboard runner's `hookRunner`
 * without `before_agent_run` at dispatch time.
 *
 * The fix preserves the host-supported definition shape and adds the declaration
 * to the exported entry object after `definePluginEntry(...)` (the installed
 * helper itself does not preserve unknown properties).
 */
const releaseEntry: ReturnType<typeof definePluginEntry> & {
  hooks: { allowConversationAccess: boolean };
} = {
  ...definePluginEntry({
  id: "cogentnexus-openclaw",
  name: "CogentNexus-OpenClaw Bridge",
  description:
    "Ticket-first OpenClaw bridge for CogentNexus-OpenClaw Host-managed continuity, durable execution, recovery, context handoff, and verified delivery.",
  register(api: OpenClawPluginApi) {
    const authority = hostPluginAuthority(api);
    if (!authority.authorized) {
      api.logger.info?.(
        `CogentNexus-OpenClaw v0.9.5 runtime registration suppressed: Host authority=${authority.reason} mode=${authority.mode ?? "unknown"}`,
      );
      return;
    }
    const register = (legacyEntry as { register?: (runtimeApi: OpenClawPluginApi) => void | Promise<void> }).register;
    if (typeof register !== "function") {
      throw new Error("CogentNexus-OpenClaw v0.9.5 compatibility entry does not expose register(api)");
    }

    const config = {
      ...((api.pluginConfig ?? {}) as DashboardVerifiedDeliveryConfig),
      ...(authority.reason === "passthrough" ? { providerMode: undefined } : { providerMode: "managed" as const }),
    };

    const discordFencedApi = withDiscordLegacyDeliveryFence(api, config);
    const runtimeApi = withWebchatLegacyDeliveryFence(discordFencedApi, config);

    installV099NativeRestartOwnershipFence(api, config);

    const installManagedRuntimeGuards = () => {
      installV092DurableDeliveryBoundary();
      const ticketDatabase = resolve(pluginCogentRoot(api), "runtime", "cogentnexus-openclaw.sqlite3");
      if (existsSync(ticketDatabase)) installV095DirectRecoveryLaneFence(ticketDatabase);
      installV091DirectModelCallLease(api);
      installV095InferenceHookBridge(runtimeApi);
      installV091DashboardVerifiedDelivery(runtimeApi, config);
      registerWebchatDeliveryAdapter(api);
      registerDiscordDeliveryAdapter(api);
    };

    const registered = register(runtimeApi);
    installV097DirectRecoveryStartupLiveness(api, config);
    if (registered && typeof (registered as Promise<void>).then === "function") {
      return Promise.resolve(registered).then(installManagedRuntimeGuards);
    }
    installManagedRuntimeGuards();
  },
}),
  hooks: {
    allowConversationAccess: true,
  },
};

export default releaseEntry;
