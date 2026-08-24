import { readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, resolve } from "node:path";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const pluginRoot = resolve(scriptDir, "..");
const manifest = JSON.parse(readFileSync(resolve(pluginRoot, "openclaw.plugin.json"), "utf8"));
const pkg = JSON.parse(readFileSync(resolve(pluginRoot, "package.json"), "utf8"));
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

const expectedTools = [
  "cnxclaw_rotation",
  "cnxclaw_workflow_start",
  "cnxclaw_ticket_status",
  "cnxclaw_knowledge",
  "cnxclaw_research",
];

if (manifest?.id !== "cogentnexus-openclaw") {
  throw new Error(`unexpected plugin id: ${JSON.stringify(manifest?.id)}`);
}
if (manifest?.configSchema?.additionalProperties !== false) {
  throw new Error("CogentNexus-OpenClaw config schema must remain strict (additionalProperties=false)");
}
const missing = requiredKeys.filter((key) => !Object.prototype.hasOwnProperty.call(properties, key));
if (missing.length > 0) {
  throw new Error(`CogentNexus-OpenClaw manifest schema is missing: ${missing.join(", ")}`);
}
if (JSON.stringify(manifest?.contracts?.tools ?? []) !== JSON.stringify(expectedTools)) {
  throw new Error(`CogentNexus-OpenClaw manifest tool contract drifted: ${JSON.stringify(manifest?.contracts?.tools ?? [])}`);
}

const extensions = pkg?.openclaw?.extensions ?? [];
if (!Array.isArray(extensions) || !extensions.includes("./dist/v091-release-entry.js")) {
  throw new Error(`package.json does not retain v0.9.1 mixed-plugin entry: ${JSON.stringify(extensions)}`);
}

const module = await import(pathToFileURL(resolve(pluginRoot, "dist/v091-release-entry.js")).href);
const entry = module?.default;
if (!entry || entry.id !== "cogentnexus-openclaw" || typeof entry.register !== "function") {
  throw new Error(`v0.9.1 mixed-plugin runtime entry has invalid export shape: ${JSON.stringify(Object.keys(entry ?? {}))}`);
}

console.log(
  `CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (${Object.keys(properties).length} config properties, ${expectedTools.length} tools)`,
);
