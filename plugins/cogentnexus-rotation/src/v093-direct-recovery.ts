/**
 * v0.9.3 compatibility name retained for the already-wired event service.
 *
 * Test A v6 moved recovery off request-scoped subagent model overrides.
 * Test A v7 then proved that OpenClaw 2026.7.1-2 also requires an explicit
 * embedded-agent transcript target and that Direct Recovery must own its lane
 * durably across Host restart reconciliation. v0.9.5 supplies the isolated
 * temporary session target and installs the durable Direct-lane fence while
 * preserving the proven v0.9.4 executor underneath.
 */
export type {
  V095DirectRecoveryConfig as V093DirectRecoveryConfig,
  V095DirectRecovery as V093DirectRecovery,
} from "./v095-direct-recovery.js";

export { launchV095DirectRecovery as launchV093DirectRecovery } from "./v095-direct-recovery.js";
