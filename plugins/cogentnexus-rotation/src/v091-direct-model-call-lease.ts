import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

export const DIRECT_MODEL_CALL_TIMEOUT_MS = 15 * 60_000;

const HOST_RECOVERY_FINALIZE_FENCE = Symbol.for("cogentnexus.v091.host-recovery-finalize-fence");
const HOST_RECOVERY_RESUME_FENCE = Symbol.for("cogentnexus.v091.host-recovery-resume-fence");

type ModelCallStart = {
  runId: string;
  callId: string;
  provider?: string;
  model?: string;
  timeoutMs?: number;
  now?: Date;
};

type ModelCallEnd = {
  runId: string;
  callId: string;
  outcome?: string;
  durationMs?: number;
  now?: Date;
};

function open(databasePath: string) {
  // TicketStore owns the base Ticket schema. Touch it first so this additive
  // lease table can be installed on both fresh and upgraded databases.
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_direct_model_call (
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      run_id TEXT NOT NULL,
      call_id TEXT NOT NULL,
      state TEXT NOT NULL,
      provider TEXT,
      model TEXT,
      started_at TEXT NOT NULL,
      deadline_at TEXT NOT NULL,
      ended_at TEXT,
      outcome TEXT,
      duration_ms INTEGER,
      recovery_started_at TEXT,
      recovery_attempt_count INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_direct_model_call_deadline
      ON cnx_direct_model_call(state, deadline_at);
  `);
  return db;
}

function event(db: DatabaseSync, ticketId: string, eventType: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

function autoResumeTagForRun(runId: string) {
  return `cogent-resume-${runId.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 96)}`;
}

export function recordDirectModelCallStarted(databasePath: string, input: ModelCallStart): boolean {
  if (!input.runId || !input.callId) return false;
  const now = input.now ?? new Date();
  const stamp = now.toISOString();
  const timeoutMs = Math.max(60_000, Math.min(input.timeoutMs ?? DIRECT_MODEL_CALL_TIMEOUT_MS, 3_600_000));
  const deadline = new Date(now.getTime() + timeoutMs).toISOString();
  const db = open(databasePath);
  try {
    db.exec("BEGIN IMMEDIATE");
    const ticket = db.prepare(`SELECT ticket_id FROM tickets
      WHERE run_id=? AND status='accepted' AND workflow_eligible=0
        AND workflow_id IS NULL AND response_ready_at IS NULL
      ORDER BY created_at DESC LIMIT 1`).get(input.runId) as any;
    if (!ticket) { db.exec("COMMIT"); return false; }
    const changed = db.prepare(`INSERT INTO cnx_direct_model_call(
        ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,
        ended_at,outcome,duration_ms,recovery_started_at,recovery_attempt_count,updated_at
      ) VALUES (?,?,?,'active',?,?,?,?,NULL,NULL,NULL,NULL,0,?)
      ON CONFLICT(ticket_id) DO UPDATE SET
        run_id=excluded.run_id,
        call_id=excluded.call_id,
        state='active',
        provider=excluded.provider,
        model=excluded.model,
        started_at=excluded.started_at,
        deadline_at=excluded.deadline_at,
        ended_at=NULL,
        outcome=NULL,
        duration_ms=NULL,
        recovery_started_at=NULL,
        recovery_attempt_count=0,
        updated_at=excluded.updated_at
      WHERE cnx_direct_model_call.state<>'recovering'`)
      .run(ticket.ticket_id, input.runId, input.callId, input.provider ?? null, input.model ?? null, stamp, deadline, stamp);
    if (changed.changes !== 1) {
      db.exec("COMMIT");
      return false;
    }
    event(db, ticket.ticket_id, "direct_model_call_started", {
      runId: input.runId,
      callId: input.callId,
      provider: input.provider,
      model: input.model,
      deadlineAt: deadline,
      timeoutMs,
      source: "openclaw-model-call-hook",
    }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function recordDirectModelCallEnded(databasePath: string, input: ModelCallEnd): boolean {
  if (!input.runId || !input.callId) return false;
  const stamp = (input.now ?? new Date()).toISOString();
  const db = open(databasePath);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT ticket_id FROM cnx_direct_model_call
      WHERE run_id=? AND call_id=? AND state='active' LIMIT 1`).get(input.runId, input.callId) as any;
    if (!row) { db.exec("COMMIT"); return false; }
    const changed = db.prepare(`UPDATE cnx_direct_model_call
      SET state='ended',ended_at=?,outcome=?,duration_ms=?,updated_at=?
      WHERE ticket_id=? AND run_id=? AND call_id=? AND state='active'`)
      .run(stamp, input.outcome ?? null, Number.isFinite(input.durationMs) ? Math.max(0, Math.floor(input.durationMs!)) : null,
        stamp, row.ticket_id, input.runId, input.callId);
    if (changed.changes === 1) {
      event(db, row.ticket_id, "direct_model_call_ended", {
        runId: input.runId,
        callId: input.callId,
        outcome: input.outcome,
        durationMs: input.durationMs,
        source: "openclaw-model-call-hook",
      }, stamp);
    }
    db.exec("COMMIT");
    return changed.changes === 1;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function closeDirectModelCallForRun(databasePath: string, runId: string, outcome: string, now = new Date()): boolean {
  if (!runId) return false;
  const stamp = now.toISOString();
  const db = open(databasePath);
  try {
    const changed = db.prepare(`UPDATE cnx_direct_model_call
      SET state='ended',ended_at=?,outcome=COALESCE(outcome,?),updated_at=?
      WHERE run_id=? AND state='active'`).run(stamp, outcome, stamp, runId);
    return changed.changes > 0;
  } finally { db.close(); }
}

/**
 * Once the external Host changes a provider-call lease to `recovering`, the
 * Host owns classification for that run. A failing agent_end emitted while
 * Gateway is being quiesced must therefore be observation-only: legacy direct
 * finalization cannot fail, promote, or queue recovery ahead of the Host.
 *
 * A successful original run is allowed to finalize. Its response_ready/durable
 * delivery evidence must win the race so the Host can fail closed or redeliver
 * without ever regenerating that response.
 */
export function hostRecoveryOwnsRun(databasePath: string, runId: string): boolean {
  if (!runId || !existsSync(databasePath)) return false;
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    db.exec("PRAGMA busy_timeout=5000;");
    const table = db.prepare(
      "SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_model_call'",
    ).get();
    if (!table) return false;
    return Boolean(db.prepare(
      "SELECT 1 FROM cnx_direct_model_call WHERE run_id=? AND state='recovering' LIMIT 1",
    ).get(runId));
  } finally {
    db.close();
  }
}

export function hostRecoveryOwnsResumeTag(databasePath: string, tag: string): boolean {
  if (!tag.startsWith("cogent-resume-") || !existsSync(databasePath)) return false;
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    db.exec("PRAGMA busy_timeout=5000;");
    const table = db.prepare(
      "SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_model_call'",
    ).get();
    if (!table) return false;
    const rows = db.prepare(
      "SELECT run_id FROM cnx_direct_model_call WHERE state='recovering'",
    ).all() as Array<{ run_id?: string }>;
    return rows.some((row) => typeof row.run_id === "string" && autoResumeTagForRun(row.run_id) === tag);
  } finally {
    db.close();
  }
}

function installHostRecoveryFinalizeFence() {
  const prototype = TicketStore.prototype as any;
  if (prototype[HOST_RECOVERY_FINALIZE_FENCE]) return;
  Object.defineProperty(prototype, HOST_RECOVERY_FINALIZE_FENCE, { value: true });
  const finalize = TicketStore.prototype.finalizeDirectRun;
  TicketStore.prototype.finalizeDirectRun = function(
    this: TicketStore,
    input: Parameters<TicketStore["finalizeDirectRun"]>[0],
  ): ReturnType<TicketStore["finalizeDirectRun"]> {
    if (!input.success && hostRecoveryOwnsRun(this.databasePath, input.runId)) return "unchanged";
    return finalize.call(this, input);
  };
}

function configFor(api: any, event?: any) {
  const fromEvent = event?.context?.pluginConfig;
  return fromEvent && typeof fromEvent === "object" ? fromEvent : (api.pluginConfig ?? {});
}

function databaseFor(api: any, event?: any, ctx?: any) {
  const cfg = configFor(api, event) as Record<string, unknown>;
  const workspace = resolve(
    typeof ctx?.workspaceDir === "string" && ctx.workspaceDir
      ? ctx.workspaceDir
      : typeof cfg.workspaceDir === "string" && cfg.workspaceDir
        ? cfg.workspaceDir
        : api?.config?.agents?.defaults?.workspace ?? process.cwd(),
  );
  return resolve(
    typeof cfg.ticketDatabasePath === "string" && cfg.ticketDatabasePath
      ? cfg.ticketDatabasePath
      : defaultTicketDatabase(workspace),
  );
}

function installHostRecoveryResumeFence(api: any) {
  const workflow = api?.session?.workflow as any;
  if (!workflow || typeof workflow.scheduleSessionTurn !== "function" || workflow[HOST_RECOVERY_RESUME_FENCE]) return;
  Object.defineProperty(workflow, HOST_RECOVERY_RESUME_FENCE, { value: true });
  const schedule = workflow.scheduleSessionTurn;
  workflow.scheduleSessionTurn = function(input: any) {
    const tag = typeof input?.tag === "string" ? input.tag : "";
    if (tag.startsWith("cogent-resume-")) {
      try {
        if (hostRecoveryOwnsResumeTag(databaseFor(api), tag)) {
          api.logger?.info?.(`CogentNexus suppressed legacy auto-resume ${tag}: Host Direct model-call recovery owns classification`);
          return Promise.resolve({
            scheduled: false,
            suppressed: true,
            reason: "host-direct-model-recovery-claim",
          });
        }
      } catch (error) {
        api.logger?.warn?.(`CogentNexus failed closed while checking Host Direct recovery before ${tag}: ${error instanceof Error ? error.message : String(error)}`);
        return Promise.resolve({
          scheduled: false,
          suppressed: true,
          reason: "host-direct-model-recovery-authority-uncertain",
        });
      }
    }
    return schedule.call(this, input);
  };
}

/**
 * Persist a bounded lease around the actual provider model call, not around the
 * whole Ticket age. OpenClaw exposes model_call_started/model_call_ended as
 * sanitized observation hooks with stable runId/callId metadata. The Host is
 * the only component allowed to act on an expired lease.
 */
export function installV091DirectModelCallLease(api: any) {
  if (typeof api?.on !== "function") return;
  // Ensure the additive table exists before the first model call can begin.
  try { open(databaseFor(api)).close(); }
  catch (error) { throw new Error(`CogentNexus Direct model-call lease schema failed: ${error instanceof Error ? error.message : String(error)}`); }
  installHostRecoveryFinalizeFence();
  installHostRecoveryResumeFence(api);

  api.on("model_call_started", (event: any, ctx: any) => {
    const runId = String(event?.runId ?? ctx?.runId ?? "").trim();
    const callId = String(event?.callId ?? "").trim();
    if (!runId || !callId) return;
    try {
      recordDirectModelCallStarted(databaseFor(api, event, ctx), {
        runId,
        callId,
        provider: typeof event?.provider === "string" ? event.provider : undefined,
        model: typeof event?.model === "string" ? event.model : undefined,
      });
    } catch (error) {
      api.logger?.error?.(`CogentNexus failed to persist Direct model-call start: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-v091-direct-model-call-start" });

  api.on("model_call_ended", (event: any, ctx: any) => {
    const runId = String(event?.runId ?? ctx?.runId ?? "").trim();
    const callId = String(event?.callId ?? "").trim();
    if (!runId || !callId) return;
    try {
      recordDirectModelCallEnded(databaseFor(api, event, ctx), {
        runId,
        callId,
        outcome: typeof event?.outcome === "string" ? event.outcome : undefined,
        durationMs: Number.isFinite(event?.durationMs) ? Number(event.durationMs) : undefined,
      });
    } catch (error) {
      api.logger?.warn?.(`CogentNexus failed to persist Direct model-call end: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-v091-direct-model-call-end" });

  // agent_end is a fallback close only while the lease is still active. A Host
  // recovery claim changes state to `recovering`, which this hook cannot undo.
  api.on("agent_end", (event: any, ctx: any) => {
    const runId = String(event?.runId ?? ctx?.runId ?? "").trim();
    if (!runId) return;
    try { closeDirectModelCallForRun(databaseFor(api, event, ctx), runId, event?.success ? "agent_end_ok" : "agent_end_error"); }
    catch (error) { api.logger?.warn?.(`CogentNexus failed to close Direct model-call lease at agent_end: ${error instanceof Error ? error.message : String(error)}`); }
  }, { registrationId: "cogentnexus-v091-direct-model-call-agent-end" });
}
