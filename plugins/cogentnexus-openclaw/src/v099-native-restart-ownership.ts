import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase } from "./ticket-store.js";

export const V099_NATIVE_RESTART_OWNERSHIP_ID =
  "cogentnexus-native-restart-ownership-v099";

export const OPENCLAW_NATIVE_RESTART_RESUME_BODY =
  "Your previous turn was interrupted by a gateway restart while " +
  "OpenClaw was waiting on tool/model work. Continue from the existing " +
  "transcript and finish the interrupted response.";

export const OPENCLAW_QUEUED_USER_PREFIX =
  "[Queued user message that arrived while the previous turn was still active]\n";

type NativeRestartDispatchMatch = {
  queuedPrompt?: string;
};

type Config = {
  workspaceDir?: string;
  ticketDatabasePath?: string;
};

export type DirectRecoveryOwnership = {
  ticketId: string;
  recoveryState: "pending" | "running";
  ownerGeneration: number;
  originalPrompt: string;
};

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(
    db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name),
  );
}

/**
 * Match only OpenClaw's native gateway-restart continuation turn.
 *
 * This deliberately does not fuzzy-match generic phrases such as "gateway
 * restart". The installed 2026.7.1-2 host emits the exact two-sentence system
 * turn below. A pending-final-delivery note may be appended by newer compatible
 * hosts, so that one explicit suffix shape is allowed as well.
 */
function matchesNativeRestartBody(content: string): boolean {
  const bare = OPENCLAW_NATIVE_RESTART_RESUME_BODY;
  const system = `[System] ${bare}`;

  return (
    content === bare ||
    content === system ||
    content.startsWith(
      `${system}\n\nNote: The interrupted final reply was captured:`,
    ) ||
    content.startsWith(
      `${bare}\n\nNote: The interrupted final reply was captured:`,
    )
  );
}

function parseOpenClawNativeRestartDispatch(
  content: unknown,
): NativeRestartDispatchMatch | undefined {
  if (typeof content !== "string") return undefined;

  const normalized = content.replace(/\r\n/g, "\n").trim();

  // Existing native system-only continuation.
  if (matchesNativeRestartBody(normalized)) {
    return {};
  }

  // OpenClaw 2026.7.1-2 can prepend the interrupted queued user
  // message to the native restart continuation.
  if (!normalized.startsWith(OPENCLAW_QUEUED_USER_PREFIX)) {
    return undefined;
  }

  const restartMarker =
    `\n\n[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`;

  const markerIndex = normalized.lastIndexOf(restartMarker);

  if (markerIndex < OPENCLAW_QUEUED_USER_PREFIX.length) {
    return undefined;
  }

  const queuedPrompt = normalized.slice(
    OPENCLAW_QUEUED_USER_PREFIX.length,
    markerIndex,
  );

  if (!queuedPrompt) {
    return undefined;
  }

  const restartTail = normalized.slice(markerIndex + 2);

  if (!matchesNativeRestartBody(restartTail)) {
    return undefined;
  }

  return { queuedPrompt };
}

export function isOpenClawNativeRestartDispatch(content: unknown): boolean {
  return Boolean(parseOpenClawNativeRestartDispatch(content));
}

/**
 * Read-only authority probe.
 *
 * Suppression is authorized only when all durable fences agree that
 * CogentNexus-OpenClaw owns recovery for this exact session:
 * - nonterminal Direct-lane Ticket;
 * - pending/running cnx_direct_recovery;
 * - active owner session at the same fencing generation;
 * - original model call was durably interrupted by Host timeout authority.
 *
 * Any missing schema, lock/read error, generation mismatch, terminal state, or
 * absence of Host timeout authority returns undefined so native OpenClaw
 * recovery remains available rather than stranding a session.
 */
export function authoritativeCnxDirectRecovery(
  path: string,
  sessionKey: string,
): DirectRecoveryOwnership | undefined {
  if (!sessionKey || !existsSync(path)) return undefined;

  let db: DatabaseSync | undefined;
  try {
    db = new DatabaseSync(path, { readOnly: true });
    db.exec("PRAGMA busy_timeout=250");

    for (const table of [
      "tickets",
      "cnx_sessions",
      "cnx_direct_recovery",
      "cnx_direct_model_call",
    ]) {
      if (!tableExists(db, table)) return undefined;
    }

    const row = db
      .prepare(
        `SELECT r.ticket_id AS ticket_id,
                r.state AS recovery_state,
                r.owner_generation AS owner_generation,
                t.prompt AS original_prompt
           FROM cnx_direct_recovery r
           JOIN tickets t ON t.ticket_id=r.ticket_id
           JOIN cnx_sessions s ON s.session_key=t.owner_session_key
          WHERE t.owner_session_key=?
            AND t.status='accepted'
            AND t.workflow_eligible=0
            AND t.workflow_id IS NULL
            AND r.mode='resume'
            AND r.state IN ('pending','running')
            AND s.state='active'
            AND s.generation=r.owner_generation
            AND EXISTS (
              SELECT 1
                FROM cnx_direct_model_call m
               WHERE m.ticket_id=r.ticket_id
                 AND m.state='interrupted'
                 AND m.outcome='host-timeout-authorized'
            )
          ORDER BY COALESCE(r.next_attempt_at,r.created_at),r.ticket_id
          LIMIT 1`,
      )
      .get(sessionKey) as
      | {
          ticket_id?: string;
          recovery_state?: "pending" | "running";
          owner_generation?: number;
          original_prompt?: string;
        }
      | undefined;

    if (
      !row?.ticket_id ||
      (row.recovery_state !== "pending" && row.recovery_state !== "running") ||
      !Number.isSafeInteger(row.owner_generation) ||
      typeof row.original_prompt !== "string"
    ) {
      return undefined;
    }

    return {
      ticketId: row.ticket_id,
      recoveryState: row.recovery_state,
      ownerGeneration: Number(row.owner_generation),
      originalPrompt: row.original_prompt,
    };
  } catch {
    // Do not suppress native recovery without durable positive ownership proof.
    return undefined;
  } finally {
    db?.close();
  }
}

/**
 * OpenClaw 2026.7.1-2 compatibility fence.
 *
 * Its native main-session restart recovery has no persisted "external owner"
 * field. Test A v11 proved that it can resume the same owner session while
 * CogentNexus-OpenClaw Direct Recovery is already running, creating a second recovery
 * lifecycle and a second Ticket admission attempt.
 *
 * before_dispatch is the earliest plugin gate available in that host and is
 * explicitly defined as pre-model-dispatch. Returning handled:true consumes
 * only the duplicate native restart system turn; CogentNexus-OpenClaw keeps the durable
 * recovery/delivery responsibility it already owns.
 */
export function installV099NativeRestartOwnershipFence(api: any, config: Config) {
  /**
   * OpenClaw 2026.7.1-2 constructs the restart continuation as the final
   * agent prompt after queued/orphaned user text has been merged. Therefore
   * this ownership fence must run at before_agent_run, ahead of Ticket-first
   * admission, rather than at the outbound before_dispatch surface.
   *
   * Suppression still requires both proofs:
   *   1) exact native restart syntax;
   *   2) positive durable same-session CogentNexus-OpenClaw Direct Recovery authority.
   *
   * For a queued-user envelope, the queued body must additionally equal the
   * durable original Ticket.prompt exactly. New user intent passes through.
   */
  api.on(
    "before_agent_run",
    (event: any, ctx: any) => {
      const dispatch = parseOpenClawNativeRestartDispatch(event?.prompt);
      if (!dispatch) return;

      const sessionKey =
        (typeof ctx?.sessionKey === "string" && ctx.sessionKey.trim()) ||
        (typeof event?.sessionKey === "string" && event.sessionKey.trim()) ||
        undefined;
      if (!sessionKey) return;

      const workspaceHint =
        (typeof ctx?.workspaceDir === "string" && ctx.workspaceDir) ||
        (typeof config.workspaceDir === "string" && config.workspaceDir) ||
        (typeof api?.config?.agents?.defaults?.workspace === "string" &&
          api.config.agents.defaults.workspace) ||
        process.cwd();
      const workspace = resolve(workspaceHint);
      const path = resolve(
        config.ticketDatabasePath ?? defaultTicketDatabase(workspace),
      );

      const ownership = authoritativeCnxDirectRecovery(path, sessionKey);
      if (!ownership) return;

      if (
        dispatch.queuedPrompt !== undefined &&
        dispatch.queuedPrompt !== ownership.originalPrompt
      ) {
        return;
      }

      api.logger.info?.(
        `CogentNexus-OpenClaw v0.9.9 suppressed OpenClaw native restart recovery ` +
          `for ${sessionKey}: durable Direct recovery ${ownership.ticketId} ` +
          `state=${ownership.recoveryState} generation=${ownership.ownerGeneration}`,
      );

      return {
        outcome: "block",
        reason:
          "duplicate OpenClaw native restart continuation is already owned by CogentNexus-OpenClaw Direct Recovery",
        category: "cogentnexus_v099_native_restart_ownership",
        metadata: {
          ticketId: ownership.ticketId,
          recoveryState: ownership.recoveryState,
          ownerGeneration: ownership.ownerGeneration,
        },
      };
    },
    { priority: 20_000, timeoutMs: 5_000 },
  );
}