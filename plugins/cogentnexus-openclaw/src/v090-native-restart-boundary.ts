import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

/**
 * OpenClaw 2026.7.1-2 main-session restart recovery prompt.
 *
 * OpenClaw core internally tags this turn with inputProvenance.kind="internal_system"
 * and sourceTool=MAIN_SESSION_RESTART_RECOVERY_SOURCE_TOOL, but that provenance is
 * not exposed through the 2026.7.1 before_agent_run plugin hook. Keep this matcher
 * deliberately exact/narrow as a compatibility fence until the host exposes the
 * provenance field to third-party plugins.
 */
export const OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT =
  "[System] Your previous turn was interrupted by a gateway restart while OpenClaw was waiting on tool/model work. Continue from the existing transcript and finish the interrupted response.";

const PENDING_FINAL_PREFIX = `${OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT}\n\nNote: The interrupted final reply was captured: \"`;

export function isOpenClawMainRestartRecoveryPrompt(prompt?: string | null): boolean {
  if (typeof prompt !== "string") return false;
  const value = prompt.trim();
  if (value === OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT) return true;
  return value.startsWith(PENDING_FINAL_PREFIX) && value.endsWith("\"");
}

function messageText(message: any): string {
  const content = message?.content;
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";
  return content
    .map((part: any) => {
      if (typeof part === "string") return part;
      if (!part || typeof part !== "object") return "";
      if (typeof part.text === "string") return part.text;
      if (typeof part.content === "string") return part.content;
      return "";
    })
    .filter(Boolean)
    .join("\n")
    .trim();
}

/**
 * Prevent OpenClaw's native main-session restart recovery from crossing the CNX
 * human-intent boundary while CNXCLAW managed policy is active.
 *
 * Priority 10000 intentionally precedes the legacy Ticket-first admission hook
 * (priority 2000). OpenClaw 2026.7.1 stops before_agent_run evaluation on the
 * first block decision, so the internal system turn cannot become a Ticket or
 * reach model inference.
 */
export function installNativeRestartRecoveryBoundary(api: any) {
  const blockedRuns = new Set<string>();
  const expiryTimers = new Map<string, ReturnType<typeof setTimeout>>();

  const remember = (runId?: string) => {
    if (!runId) return;
    blockedRuns.add(runId);
    const previous = expiryTimers.get(runId);
    if (previous) clearTimeout(previous);
    const timer = setTimeout(() => {
      blockedRuns.delete(runId);
      expiryTimers.delete(runId);
    }, 5 * 60_000);
    timer.unref?.();
    expiryTimers.set(runId, timer);
  };

  api.on?.("before_agent_run", (event: any, ctx: any) => {
    const sessionKey = ctx?.sessionKey;
    if (!sessionKey || sessionKey.includes(":subagent:")) return { outcome:"pass" };
    if (!isOpenClawMainRestartRecoveryPrompt(event?.prompt)) return { outcome:"pass" };
    remember(ctx?.runId);
    return {
      outcome:"block",
      reason:"OpenClaw internal main-session restart recovery is not fresh human intent; CogentNexus-OpenClaw owns durable recovery",
      category:"cnxclaw_native_restart_recovery_fence",
      metadata:{ source:"openclaw-main-session-restart-recovery", sessionKey },
    };
  }, { priority:10_000, timeoutMs:5_000 });

  // Keep the synthetic OpenClaw recovery instruction out of the owner transcript
  // even when the host attempts to persist the recovered user-shaped turn.
  api.on?.("before_message_write", (event: any, ctx: any) => {
    const sessionKey = event?.sessionKey ?? ctx?.sessionKey;
    if (!sessionKey || sessionKey.includes(":subagent:")) return;
    if (event?.message?.role !== "user") return;
    if (isOpenClawMainRestartRecoveryPrompt(messageText(event.message))) return { block:true };
  }, { priority:10_000, timeoutMs:5_000 });

  // A blocked native recovery may produce a generic gate response. It is control
  // plane noise, not user-facing assistant content, so cancel its delivery.
  api.on?.("reply_payload_sending", (event: any) => {
    const runId = event?.runId;
    if (!runId || !blockedRuns.has(runId)) return;
    return { cancel:true, reason:"suppressed OpenClaw internal restart-recovery gate notice" };
  }, { priority:10_000, timeoutMs:5_000 });

  return { blockedRuns };
}

function hasTable(db: DatabaseSync, table: string): boolean {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(table));
}

/**
 * Migrate Tickets that were incorrectly created from OpenClaw's internal restart
 * recovery prompt before the provenance fence existed. This changes only exact
 * synthetic recovery Tickets and does not bump the owner session generation.
 */
export function reconcileNativeRestartRecoveryTickets(databasePath: string, now = new Date()) {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  const stamp = now.toISOString();
  const reason = "Suppressed OpenClaw internal main-session restart recovery turn";
  let cancelled = 0;
  let outboxSuppressed = 0;
  let recoverySuppressed = 0;
  let assistantSuppressed = 0;
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE");
    const rows = db.prepare(`SELECT ticket_id,prompt,status FROM tickets
      WHERE workflow_id IS NULL AND status IN ('accepted','planned','running','waiting','failed')
      ORDER BY created_at,ticket_id`).all() as Array<{ticket_id:string;prompt:string;status:string}>;

    for (const row of rows) {
      if (!isOpenClawMainRestartRecoveryPrompt(row.prompt)) continue;
      const changed = db.prepare(`UPDATE tickets SET status='cancelled',workflow_eligible=0,
        worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,
        failure_class=NULL,failure_message=?,response_ready_at=NULL,delivery_confirmed_at=NULL,
        delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND workflow_id IS NULL
        AND status IN ('accepted','planned','running','waiting','failed')`)
        .run(reason, stamp, row.ticket_id);
      if (changed.changes !== 1) continue;
      cancelled++;
      if (hasTable(db, "ticket_outbox")) {
        outboxSuppressed += Number(db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id).changes);
      }
      if (hasTable(db, "cnx_direct_recovery")) {
        recoverySuppressed += Number(db.prepare(`UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,
          next_attempt_at=NULL,last_error=?,updated_at=? WHERE ticket_id=? AND state<>'cancelled'`)
          .run(reason, stamp, row.ticket_id).changes);
      }
      if (hasTable(db, "cnx_assistant_delivery")) {
        assistantSuppressed += Number(db.prepare("DELETE FROM cnx_assistant_delivery WHERE ticket_id=? AND status='pending'").run(row.ticket_id).changes);
      }
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
        .run(row.ticket_id, "native_restart_recovery_suppressed", JSON.stringify({
          previousStatus:row.status,
          source:"openclaw-main-session-restart-recovery",
          policy:"internal-system-is-not-human-intent",
        }), stamp);
    }
    db.exec("COMMIT");
    return { cancelled, outboxSuppressed, recoverySuppressed, assistantSuppressed };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}
