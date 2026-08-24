/**
 * v0.9.3 compatibility name retained for the already-wired event service.
 *
 * Test A v6 moved recovery off request-scoped subagent model overrides.
 * Test A v7 added the explicit embedded transcript target and durable Direct
 * lane ownership fence. Test A v8 then proved that the helper session itself
 * must be invisible to Ticket-first admission; otherwise its recovery prompt
 * recursively creates new Direct Tickets and contends on the same SQLite DB.
 * v0.9.6 adds that internal-admission fence while preserving v0.9.5/v0.9.4.
 */
export type {
  V096DirectRecoveryConfig as V093DirectRecoveryConfig,
  V096DirectRecovery as V093DirectRecovery,
} from "./v096-direct-recovery.js";

export { launchV096DirectRecovery as launchV093DirectRecovery } from "./v096-direct-recovery.js";
