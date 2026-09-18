import { getGlobalHookRunner } from "openclaw/plugin-sdk/plugin-runtime";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

const PLUGIN_ID = "cogentnexus-openclaw";
const TARGET_HOOK = "before_agent_run";
export const RUNTIME_ATTESTATION_METHOD = "cogentnexus.runtimeAttestation";

export type RuntimeHookAttestationClassification =
  | "PRESENT"
  | "ABSENT"
  | "AMBIGUOUS"
  | "RUNNER_UNAVAILABLE";

export type RuntimeHookAttestation = {
  schemaVersion: 1;
  pluginId: typeof PLUGIN_ID;
  hookName: typeof TARGET_HOOK;
  runnerReady: boolean;
  globalHookCount: number;
  /**
   * Count in OpenClaw's most recently initialized registry.
   *
   * Positive is sufficient evidence that this registry contributes a CNX
   * before_agent_run hook to the composed runner. Zero/null is not sufficient
   * evidence of global absence because the runner composes multiple live
   * registries.
   */
  latestRegistryPluginHookCount: number | null;
  classification: RuntimeHookAttestationClassification;
};

export function classifyRuntimeHookAttestation(input: {
  runnerReady: boolean;
  globalHookCount: number;
  latestRegistryPluginHookCount: number | null;
}): RuntimeHookAttestationClassification {
  if (!input.runnerReady) return "RUNNER_UNAVAILABLE";
  if (input.globalHookCount <= 0) return "ABSENT";
  if ((input.latestRegistryPluginHookCount ?? 0) > 0) return "PRESENT";
  return "AMBIGUOUS";
}

export function readRuntimeHookAttestation(): RuntimeHookAttestation {
  const runner = getGlobalHookRunner();

  const globalHookCount = runner
    ? runner.getHookCount(TARGET_HOOK)
    : 0;

  // OpenClaw v2026.9.4 intentionally keeps the active plugin registry out of
  // the public plugin-runtime SDK. Do not bypass that boundary through a
  // private/internal import merely to identify ownership. A positive global
  // count proves that the composed runner sees this hook name, but without a
  // public plugin-specific registry view ownership remains conservatively
  // AMBIGUOUS rather than being upgraded to PRESENT.
  const latestRegistryPluginHookCount = null;

  const runnerReady = Boolean(runner);

  return {
    schemaVersion: 1,
    pluginId: PLUGIN_ID,
    hookName: TARGET_HOOK,
    runnerReady,
    globalHookCount,
    latestRegistryPluginHookCount,
    classification: classifyRuntimeHookAttestation({
      runnerReady,
      globalHookCount,
      latestRegistryPluginHookCount,
    }),
  };
}

export function registerRuntimeHookAttestation(
  api: Pick<OpenClawPluginApi, "registerGatewayMethod">,
  read: () => RuntimeHookAttestation = readRuntimeHookAttestation,
): void {
  api.registerGatewayMethod(
    RUNTIME_ATTESTATION_METHOD,
    ({ respond }) => {
      respond(true, read());
    },
    { scope: "operator.read" },
  );
}