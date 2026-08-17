import { readFileSync } from "node:fs";

const manifest = JSON.parse(readFileSync(new URL("../openclaw.plugin.json", import.meta.url), "utf8"));
const pkg = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));
const properties = manifest?.configSchema?.properties ?? {};

const requiredKeys = [
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
];

const missing = requiredKeys.filter((key) => !Object.prototype.hasOwnProperty.call(properties, key));
if (missing.length > 0) {
  throw new Error(`generated CogentNexus plugin schema is missing: ${missing.join(", ")}`);
}

const extensions = pkg?.openclaw?.extensions ?? [];
if (!Array.isArray(extensions) || !extensions.includes("./dist/v091-release-entry.js")) {
  throw new Error(`generated package.json does not retain v0.9.1 release entry: ${JSON.stringify(extensions)}`);
}

console.log(`CogentNexus generated schema verification: PASS (${Object.keys(properties).length} properties)`);
