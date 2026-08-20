import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase } from "./ticket-store.js";
import { pulseManagedWorkers } from "./v091-final-entry.js";

export const DIRECT_RECOVERY_LIVENESS_ID = "cogentnexus-direct-recovery-v097-liveness";
export const DIRECT_RECOVERY_STARTUP_WAKE_DELAYS_MS = [250, 1_000, 3_000, 10_000, 30_000] as const;

type Config = {
  workspaceDir?: string;
  ticketDatabasePath?: string;
};

export type DirectRecoveryStartupState = "idle" | "waiting" | "ready" | "unknown";

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

/**
 * Classify startup liveness without changing durable authority.
 *
 * v0.9.1's Direct Recovery worker intentionally claims only an active owner
 * session and a model call that is no longer active/recovering. Test A v9
 * proved that Gateway restart can start the worker before those readiness
 * fences settle. In that instant its own deadline scheduler sees no eligible
 * row and arms no timer, even though a durable pending recovery already exists.
 *
 * This helper deliberately sees the broader pending row while preserving the
 * exact generation/lane fences. It never makes the row claimable itself.
 */
export function directRecoveryStartupState(path: string): DirectRecoveryStartupState {
  if (!existsSync(path)) return "idle";
  let db: DatabaseSync | undefined;
  try {
    db = new DatabaseSync(path, { readOnly: true });
    db.exec("PRAGMA busy_timeout=250");
    if (!tableExists(db, "tickets") || !tableExists(db, "cnx_sessions") || !tableExists(db, "cnx_direct_recovery")) {
      return "idle";
    }
    const modelCallExists = tableExists(db, "cnx_direct_model_call");
    const modelBlocked = modelCallExists
      ? `EXISTS (SELECT 1 FROM cnx_direct_model_call m
           WHERE m.ticket_id=r.ticket_id AND m.state IN ('active','recovering'))`
      : "0";
    const row = db.prepare(`SELECT s.state AS session_state, ${modelBlocked} AS model_blocked
      FROM cnx_direct_recovery r
      JOIN tickets t ON t.ticket_id=r.ticket_id
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      WHERE r.state='pending'
        AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND s.generation=r.owner_generation
      ORDER BY COALESCE(r.next_attempt_at,r.created_at),r.ticket_id
      LIMIT 1`).get() as { session_state?: string; model_blocked?: number } | undefined;
    if (!row) return "idle";
    return row.session_state === "active" && Number(row.model_blocked ?? 0) === 0 ? "ready" : "waiting";
  } catch {
    // A transient read/lock/schema race during Gateway startup is not evidence
    // of quiescence. Fail toward a later pulse, never toward inference.
    return "unknown";
  } finally {
    db?.close();
  }
}

export function startupLivenessDelayMs(attempt: number) {
  const index = Math.max(0, Math.min(DIRECT_RECOVERY_STARTUP_WAKE_DELAYS_MS.length - 1, attempt));
  return DIRECT_RECOVERY_STARTUP_WAKE_DELAYS_MS[index];
}

/**
 * Register a tiny startup bridge for the event-driven Direct Recovery worker.
 * It does not poll idle systems: the timeout chain stops as soon as no durable
 * pending Direct Recovery row remains. While a row exists it emits the same
 * managed-worker pulse used by Ticket mutations, with bounded backoff.
 */
export function installV097DirectRecoveryStartupLiveness(
  api: any,
  config: Config,
  pulse: () => void = pulseManagedWorkers,
) {
  let timer: ReturnType<typeof setTimeout> | undefined;
  let stopped = false;
  let attempt = 0;

  const clearWake = () => {
    if (timer) clearTimeout(timer);
    timer = undefined;
  };

  api.registerService({
    id: DIRECT_RECOVERY_LIVENESS_ID,
    start: async (ctx: any) => {
      stopped = false;
      attempt = 0;
      clearWake();
      const workspace = resolve(config.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
      const path = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspace));

      const check = () => {
        if (stopped) return;
        const state = directRecoveryStartupState(path);
        if (state === "idle") {
          clearWake();
          return;
        }
        pulse();
        const delay = startupLivenessDelayMs(attempt++);
        timer = setTimeout(check, delay);
        timer.unref?.();
      };

      // Defer the first pulse until all plugin services have had a chance to
      // install their listeners, regardless of service start order.
      timer = setTimeout(check, DIRECT_RECOVERY_STARTUP_WAKE_DELAYS_MS[0]);
      timer.unref?.();
    },
    stop: async () => {
      stopped = true;
      clearWake();
    },
  });
}
