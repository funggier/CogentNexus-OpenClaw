import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import entry, { V091_RELEASE_CONFIG_KEYS } from "./v091-release-entry.js";

const manifest = JSON.parse(
  readFileSync(new URL("../openclaw.plugin.json", import.meta.url), "utf8"),
) as { configSchema?: { properties?: Record<string, unknown> } };

const managedKeys = [
  "ticketFirst",
  "preInferenceAdmission",
  "autoWorkflowCompletion",
  "enforcedMode",
  "autoResume",
  "workspaceDir",
  "ticketDispatchLimit",
  "ticketMaximumRunning",
  "ticketMaximumAttempts",
  "ticketRecoveryPollMs",
  "ticketDispatchPollMs",
  "ticketOutboxPollMs",
  "completionPollMs",
  "contextMaintenancePollMs",
] as const;

const contextAndRecoveryKeys = [
  "contextSafetyEnabled",
  "contextSoftRatio",
  "contextHardRatio",
  "contextMinimumHeadroomTokens",
  "contextMaintenancePollMs",
  "contextMaintenanceMaxAttempts",
  "contextCompactionTimeoutMs",
  "contextHardTrimMaxLines",
  "contextRecoveryHoldPollMs",
  "contextRecoveryHoldMaxMs",
  "recoveryOrderPollMs",
  "syntheticPromptInlineChars",
  "syntheticPromptChunkChars",
] as const;

describe("v0.9.1 release config schema", () => {
  it("keeps runtime and checked-in manifest property sets identical", () => {
    const manifestKeys = Object.keys(manifest.configSchema?.properties ?? {}).sort();
    expect(V091_RELEASE_CONFIG_KEYS).toEqual(manifestKeys);
  });

  it("accepts every key staged by transactional managed enable", () => {
    const runtimeProperties = (entry as any).configSchema?.properties ?? {};
    for (const key of managedKeys) expect(runtimeProperties).toHaveProperty(key);
  });

  it("preserves the complete v0.9 context/recovery schema across plugin builds", () => {
    const runtimeProperties = (entry as any).configSchema?.properties ?? {};
    for (const key of contextAndRecoveryKeys) expect(runtimeProperties).toHaveProperty(key);
  });
});
