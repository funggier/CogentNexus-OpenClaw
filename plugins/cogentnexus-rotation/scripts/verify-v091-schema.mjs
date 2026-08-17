import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

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

const expectedTools = [
  "cogent_rotation",
  "cogent_workflow_start",
  "cogent_ticket_status",
  "cogent_knowledge",
  "cogent_research",
];

if (manifest?.id !== "cogentnexus-rotation") {
  throw new Error(`unexpected plugin id: ${JSON.stringify(manifest?.id)}`);
}
if (manifest?.configSchema?.additionalProperties !== false) {
  throw new Error("CogentNexus config schema must remain strict (additionalProperties=false)");
}
const missing = requiredKeys.filter((key) => !Object.prototype.hasOwnProperty.call(properties, key));
if (missing.length > 0) {
  throw new Error(`CogentNexus manifest schema is missing: ${missing.join(", ")}`);
}
if (JSON.stringify(manifest?.contracts?.tools ?? []) !== JSON.stringify(expectedTools)) {
  throw new Error(`CogentNexus manifest tool contract drifted: ${JSON.stringify(manifest?.contracts?.tools ?? [])}`);
}

const extensions = pkg?.openclaw?.extensions ?? [];
if (!Array.isArray(extensions) || !extensions.includes("./dist/v091-release-entry.js")) {
  throw new Error(`package.json does not retain v0.9.1 mixed-plugin entry: ${JSON.stringify(extensions)}`);
}

const entryUrl = pathToFileURL(resolve(new URL("..", import.meta.url).pathname, "dist/v091-release-entry.js"));
const module = await import(entryUrl.href);
const entry = module?.default;
if (!entry || entry.id !== "cogentnexus-rotation" || typeof entry.register !== "function") {
  throw new Error(`v0.9.1 mixed-plugin runtime entry has invalid export shape: ${JSON.stringify(Object.keys(entry ?? {}))}`);
}

console.log(
  `CogentNexus mixed-plugin artifact verification: PASS (${Object.keys(properties).length} config properties, ${expectedTools.length} tools)`,
);
