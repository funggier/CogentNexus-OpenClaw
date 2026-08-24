import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import {
  launchV094DirectRecovery,
  type V094DirectRecovery,
  type V094DirectRecoveryConfig,
} from "./v094-direct-recovery.js";

export type V095DirectRecoveryConfig = V094DirectRecoveryConfig;
export type V095DirectRecovery = V094DirectRecovery;

const DIRECT_RECOVERY_LANE_TRIGGER = "cnx_v095_direct_recovery_lane_lock";

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

/**
 * Durable lane ownership fence.
 *
 * Test A v7 proved that legacy Host recovery can still promote an interrupted
 * Direct Ticket to workflow_eligible=1 after cnx_direct_recovery has already
 * taken ownership. The trigger makes that state transition impossible for
 * every writer/process, including a legacy Host process running across a
 * Gateway restart. A Direct Recovery row therefore becomes the durable lane
 * owner until the Ticket reaches terminal/delivery state.
 */
export function installV095DirectRecoveryLaneFence(path: string) {
  const db = new DatabaseSync(path);
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
    if (!tableExists(db, "tickets") || !tableExists(db, "cnx_direct_recovery")) {
      throw new Error("v0.9.5 Direct Recovery lane fence requires tickets and cnx_direct_recovery tables");
    }
    db.exec(`
      CREATE TRIGGER IF NOT EXISTS ${DIRECT_RECOVERY_LANE_TRIGGER}
      BEFORE UPDATE OF workflow_eligible, workflow_id ON tickets
      FOR EACH ROW
      WHEN OLD.workflow_eligible=0
        AND EXISTS (SELECT 1 FROM cnx_direct_recovery r WHERE r.ticket_id=OLD.ticket_id)
        AND (NEW.workflow_eligible<>0 OR NEW.workflow_id IS NOT NULL)
      BEGIN
        SELECT RAISE(IGNORE);
      END;
    `);
  } finally {
    db.close();
  }
}

function safeSessionIdentity(value: unknown) {
  const raw = typeof value === "string" && value.trim() ? value.trim() : "recovery";
  return raw.replace(/[^A-Za-z0-9._-]/gu, "-").slice(0, 96) || "recovery";
}

/**
 * OpenClaw 2026.7.1-2 requires either an explicit sessionFile or a sessionKey
 * when resolving an embedded-agent transcript target. Direct Recovery is an
 * isolated helper run, so give it both a unique temporary key and temporary
 * transcript file and erase the directory on every completion/error/abort.
 *
 * This follows the same one-off embedded-run pattern used by OpenClaw's own
 * 2026.7.1-2 slug helper rather than writing into the owner Dashboard session.
 */
export function withV095EphemeralEmbeddedSession(api: any) {
  const owner = api?.runtime?.agent;
  const runEmbeddedAgent = owner?.runEmbeddedAgent;
  if (typeof runEmbeddedAgent !== "function") {
    throw new Error("OpenClaw embedded-agent runtime is unavailable for v0.9.5 Direct Recovery");
  }

  return {
    ...api,
    runtime: {
      ...api.runtime,
      agent: {
        ...owner,
        runEmbeddedAgent: async (input: any) => {
          const directory = mkdtempSync(join(tmpdir(), "cogentnexus-openclaw-direct-recovery-"));
          const sessionFile = join(directory, "session.jsonl");
          const identity = safeSessionIdentity(input?.sessionId ?? input?.runId);
          const sessionKey = `temp:cogentnexus-openclaw-direct-recovery:${identity}`;
          try {
            return await runEmbeddedAgent.call(owner, {
              ...input,
              sessionKey,
              sessionFile,
              disableTrajectory: true,
            });
          } finally {
            rmSync(directory, { recursive: true, force: true });
          }
        },
      },
    },
  };
}

/**
 * v0.9.5 keeps the proven v0.9.4 claim/model/abort/result executor intact and
 * narrows this layer to OpenClaw session-target compatibility. Lane ownership
 * is enforced separately by the durable SQLite trigger installed at startup.
 */
export async function launchV095DirectRecovery(
  api: any,
  path: string,
  workspace: string,
  recovery: V095DirectRecovery,
  cfg: V095DirectRecoveryConfig,
) {
  return await launchV094DirectRecovery(
    withV095EphemeralEmbeddedSession(api),
    path,
    workspace,
    recovery,
    cfg,
  );
}
