/**
 * v0.9.3 compatibility name retained for the already-wired event service.
 *
 * Test A v6 proved that OpenClaw 2026.7.1-2 rejects request-scoped
 * `runtime.subagent.run({ provider, model })` overrides before a recovery run
 * can start. v0.9.4 moves Direct Recovery to `runtime.agent.runEmbeddedAgent`,
 * which owns provider/model selection directly and accepts an AbortSignal.
 * Keep this module as a narrow compatibility alias so the proven v0.9.1
 * scheduler/service wiring does not need to change.
 */
export type {
  V094DirectRecoveryConfig as V093DirectRecoveryConfig,
  V094DirectRecovery as V093DirectRecovery,
} from "./v094-direct-recovery.js";

export { launchV094DirectRecovery as launchV093DirectRecovery } from "./v094-direct-recovery.js";
