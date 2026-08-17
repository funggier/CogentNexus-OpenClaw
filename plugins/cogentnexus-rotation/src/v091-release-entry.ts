import { Type } from "typebox";
import entry from "./v091-final-entry.js";

/**
 * v0.9.1 release schema extension.
 *
 * OpenClaw's plugin build regenerates openclaw.plugin.json from the exported
 * runtime configSchema.  The v0.9 context/recovery keys were present in the
 * checked-in manifest but not in the TypeBox schema owned by index.ts, so a
 * build silently removed them and transactional enable then failed validation.
 *
 * Keep the compatibility layers intact and extend the exported schema at the
 * final release boundary so build-time and runtime validation share one
 * authoritative definition.
 */
const schema = (entry as any)?.configSchema;
if (!schema || typeof schema !== "object" || !schema.properties || typeof schema.properties !== "object") {
  throw new Error("CogentNexus v0.9.1 release entry could not locate the plugin config schema");
}

Object.assign(schema.properties, {
  contextSafetyEnabled: Type.Optional(Type.Boolean({
    description: "Enable pre-inference context pressure admission and durable background compaction for ticketed owner sessions.",
  })),
  contextSoftRatio: Type.Optional(Type.Number({
    minimum: 0.35,
    maximum: 0.95,
    description: "Optional projected context ratio that defers owner inference to bounded recovery before overflow. Defaults adapt to the model window.",
  })),
  contextHardRatio: Type.Optional(Type.Number({
    minimum: 0.50,
    maximum: 0.97,
    description: "Projected context ratio that authorizes deterministic hard transcript trimming if semantic compaction cannot reclaim enough headroom.",
  })),
  contextMinimumHeadroomTokens: Type.Optional(Type.Integer({
    minimum: 2048,
    maximum: 131072,
    description: "Minimum headroom kept before owner inference; automatically capped relative to the active model window.",
  })),
  contextMaintenancePollMs: Type.Optional(Type.Integer({
    minimum: 1000,
    maximum: 30000,
    description: "Compatibility interval for context-maintenance layers. v0.9.1 production maintenance is event/deadline driven.",
  })),
  contextMaintenanceMaxAttempts: Type.Optional(Type.Integer({
    minimum: 1,
    maximum: 10,
    description: "Maximum automatic context-maintenance attempts for one session generation before maintenance stops until a new human request authorizes another attempt.",
  })),
  contextCompactionTimeoutMs: Type.Optional(Type.Integer({
    minimum: 30000,
    maximum: 1800000,
    description: "Gateway RPC timeout for semantic context compaction.",
  })),
  contextHardTrimMaxLines: Type.Optional(Type.Integer({
    minimum: 20,
    maximum: 1000,
    description: "First deterministic last-lines fallback when a hard-pressure session cannot be made safe by semantic compaction. OpenClaw archives the prior transcript.",
  })),
  contextRecoveryHoldPollMs: Type.Optional(Type.Integer({
    minimum: 250,
    maximum: 5000,
    description: "Polling interval while a committed Direct Recovery waits for its same-generation context-maintenance hold to settle.",
  })),
  contextRecoveryHoldMaxMs: Type.Optional(Type.Integer({
    minimum: 30000,
    maximum: 3600000,
    description: "Maximum bounded wait for context maintenance before the hidden recovery attempt fails and returns to durable retry policy.",
  })),
  recoveryOrderPollMs: Type.Optional(Type.Integer({
    minimum: 100,
    maximum: 5000,
    description: "Polling interval while a claimed hidden Direct Recovery waits behind an older accepted Direct Recovery in the same session generation.",
  })),
  syntheticPromptInlineChars: Type.Optional(Type.Integer({
    minimum: 4000,
    maximum: 48000,
    description: "Maximum internal hidden-worker payload kept inline before exact content is externalized to a durable SHA-256 chunk bundle.",
  })),
  syntheticPromptChunkChars: Type.Optional(Type.Integer({
    minimum: 2000,
    maximum: 24000,
    description: "Maximum characters per deterministic chunk for an externalized internal hidden-worker payload.",
  })),
});

export const V091_RELEASE_CONFIG_KEYS = Object.freeze(Object.keys(schema.properties).sort());
export default entry;
