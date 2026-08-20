import {
  launchV095DirectRecovery,
  type V095DirectRecovery,
  type V095DirectRecoveryConfig,
} from "./v095-direct-recovery.js";

export type V096DirectRecoveryConfig = V095DirectRecoveryConfig;
export type V096DirectRecovery = V095DirectRecovery;

function safeIdentity(value: unknown, fallback: string) {
  const raw = typeof value === "string" && value.trim() ? value.trim() : fallback;
  return raw.replace(/[^A-Za-z0-9._-]/gu, "-").slice(0, 96) || fallback;
}

/**
 * Test A v8 proved that a temporary embedded-agent session is still visible to
 * CogentNexus Ticket-first admission when its session key looks like a normal
 * owner session. The embedded recovery prompt was therefore accepted again as
 * a new Direct Ticket, recursively contending on the same SQLite database and
 * forcing a retry with `database is locked`.
 *
 * Existing admission deliberately ignores every `:subagent:` session. Reuse
 * that proven internal-session boundary while keeping v0.9.5's temporary
 * sessionFile/transcript cleanup and v0.9.4's recovery executor unchanged.
 */
export function withV096InternalRecoveryAdmissionFence(api: any) {
  const owner = api?.runtime?.agent;
  const runEmbeddedAgent = owner?.runEmbeddedAgent;
  if (typeof runEmbeddedAgent !== "function") {
    throw new Error("OpenClaw embedded-agent runtime is unavailable for v0.9.6 Direct Recovery");
  }

  return {
    ...api,
    runtime: {
      ...api.runtime,
      agent: {
        ...owner,
        runEmbeddedAgent: async (input: any) => {
          const agentId = safeIdentity(input?.agentId, "main");
          const identity = safeIdentity(input?.sessionId ?? input?.runId, "recovery");
          return await runEmbeddedAgent.call(owner, {
            ...input,
            sessionKey: `agent:${agentId}:subagent:cnx-recovery-${identity}`,
          });
        },
      },
    },
  };
}

/**
 * v0.9.6 is intentionally narrow: mark the embedded helper as an internal
 * subagent-shaped session before v0.9.5 supplies the ephemeral transcript
 * target. This prevents recursive Ticket intake without changing durable
 * recovery, model, abort, lane-ownership, result, or delivery semantics.
 */
export async function launchV096DirectRecovery(
  api: any,
  path: string,
  workspace: string,
  recovery: V096DirectRecovery,
  cfg: V096DirectRecoveryConfig,
) {
  return await launchV095DirectRecovery(
    withV096InternalRecoveryAdmissionFence(api),
    path,
    workspace,
    recovery,
    cfg,
  );
}
