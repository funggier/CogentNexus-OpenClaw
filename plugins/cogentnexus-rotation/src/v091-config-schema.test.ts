import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import entry from "./v091-release-entry.js";

const manifest = JSON.parse(
  readFileSync(new URL("../openclaw.plugin.json", import.meta.url), "utf8"),
) as {
  id?: string;
  configSchema?: { additionalProperties?: boolean; properties?: Record<string, unknown> };
  contracts?: { tools?: string[] };
};

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

const expectedTools = [
  "cogent_rotation",
  "cogent_workflow_start",
  "cogent_ticket_status",
  "cogent_knowledge",
  "cogent_research",
];

describe("v0.9.1 mixed-plugin release boundary", () => {
  it("exports the public runtime register contract", () => {
    expect(entry).toBeTruthy();
    expect((entry as any).id).toBe("cogentnexus-rotation");
    expect(typeof (entry as any).register).toBe("function");
  });

  it("keeps the manifest strict and accepts every key staged by transactional enable", () => {
    expect(manifest.id).toBe("cogentnexus-rotation");
    expect(manifest.configSchema?.additionalProperties).toBe(false);
    const properties = manifest.configSchema?.properties ?? {};
    for (const key of managedKeys) expect(properties).toHaveProperty(key);
  });

  it("preserves complete context/recovery schema and static tool discovery", () => {
    const properties = manifest.configSchema?.properties ?? {};
    for (const key of contextAndRecoveryKeys) expect(properties).toHaveProperty(key);
    expect(manifest.contracts?.tools).toEqual(expectedTools);
  });
});
