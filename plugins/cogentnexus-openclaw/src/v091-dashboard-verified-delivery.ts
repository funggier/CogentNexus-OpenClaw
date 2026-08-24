import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";
import { isDashboardSession, sessionAuthority } from "./v090.js";
import { pulseManagedWorkers } from "./v091-final-entry.js";

const PATCH = Symbol.for("cogentnexus.v091.dashboard-verified-delivery");

export type DashboardVerifiedDeliveryConfig = {
  cogentNexusOpenClawRoot?: string;
  workspaceDir?: string;
  ticketDatabasePath?: string;
  pythonCommand?: string;
};

type DashboardTicket = {
  ticket_id: string;
  owner_session_key: string;
  response_ready_at: string | null;
};

type PendingDirectResult = {
  delivery_id: number;
  ticket_id: string;
  owner_session_key: string;
  owner_generation: number;
  text: string;
  idempotency_key: string;
};

function openDb(path: string, readOnly = false) {
  new TicketStore(path).snapshot();
  const db = readOnly ? new DatabaseSync(path, { readOnly: true }) : new DatabaseSync(path);
  if (!readOnly) db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  return db;
}

function addEvent(db: DatabaseSync, ticketId: string, type: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, type, JSON.stringify(payload), stamp);
}

function dashboardTicket(path: string, runId: string): DashboardTicket | undefined {
  const db = openDb(path, true);
  try {
    const row = db.prepare(`SELECT ticket_id,owner_session_key,response_ready_at FROM tickets
      WHERE run_id=? AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL
      ORDER BY created_at DESC LIMIT 1`).get(runId) as DashboardTicket | undefined;
    return row?.owner_session_key && isDashboardSession(row.owner_session_key) ? row : undefined;
  } finally { db.close(); }
}

function pendingDirectResult(path: string, runId: string): PendingDirectResult | undefined {
  const db = openDb(path, true);
  try {
    return db.prepare(`SELECT d.delivery_id,d.ticket_id,d.owner_session_key,d.owner_generation,d.text,d.idempotency_key
      FROM cnx_assistant_delivery d JOIN tickets t ON t.ticket_id=d.ticket_id
      WHERE t.run_id=? AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND d.kind='direct_result' AND d.status='pending'
      ORDER BY d.delivery_id DESC LIMIT 1`).get(runId) as PendingDirectResult | undefined;
  } finally { db.close(); }
}

export function deliveryMarker(idempotencyKey: string) {
  const digest = createHash("sha256").update(idempotencyKey).digest("hex").slice(0, 32);
  return `<!-- cogentnexus-delivery:${digest} -->`;
}

function nativePayloadText(text: string, idempotencyKey: string) {
  const marker = deliveryMarker(idempotencyKey);
  return text.includes(marker) ? text : `${text.replace(/\s+$/u, "")}\n\n${marker}`;
}

/** Commit one replayable Dashboard final before native transport begins. */
export function stageDashboardDirectResult(path: string, input: { runId: string; text: string; now?: Date }) {
  const text = input.text.trim();
  if (!text) return { staged: false as const, reason: "empty-text" };
  const initial = dashboardTicket(path, input.runId);
  if (!initial) return { staged: false as const, reason: "not-dashboard-direct" };

  // sessionAuthority owns creation/migration of the v0.9 session + assistant-delivery schema.
  const authority = sessionAuthority(path, initial.owner_session_key);
  if (authority.state !== "active") return { staged: false as const, reason: `session-${authority.state}` };

  const db = openDb(path), stamp = (input.now ?? new Date()).toISOString();
  try {
    db.exec("BEGIN IMMEDIATE");
    const ticket = db.prepare(`SELECT ticket_id,owner_session_key,response_ready_at FROM tickets
      WHERE run_id=? AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL
      ORDER BY created_at DESC LIMIT 1`).get(input.runId) as DashboardTicket | undefined;
    if (!ticket?.owner_session_key || !isDashboardSession(ticket.owner_session_key)) {
      db.exec("COMMIT");
      return { staged: false as const, reason: "ticket-no-longer-dashboard-direct" };
    }
    const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?")
      .get(ticket.owner_session_key) as { state?: string; generation?: number } | undefined;
    if (session?.state !== "active") {
      db.exec("COMMIT");
      return { staged: false as const, reason: "session-authority-revoked" };
    }
    const generation = Number(session.generation ?? -1);
    if (!Number.isSafeInteger(generation) || generation < 0) throw new Error("invalid Dashboard owner generation");

    const idempotencyKey = `cnxclaw-direct-result:${ticket.ticket_id}:g${generation}`;
    const existing = db.prepare(`SELECT delivery_id,text,status FROM cnx_assistant_delivery
      WHERE idempotency_key=?`).get(idempotencyKey) as { delivery_id?: number; text?: string; status?: string } | undefined;
    if (existing && existing.text !== text) {
      throw new Error(`durable Dashboard result changed for ${ticket.ticket_id} generation ${generation}`);
    }
    let inserted = false;
    if (!existing) {
      const created = db.prepare(`INSERT INTO cnx_assistant_delivery(
        ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
        attempt_count,last_error,created_at,updated_at) VALUES (?,?,?,'direct_result',?,?,?,'pending',0,NULL,?,?)`)
        .run(ticket.ticket_id, ticket.owner_session_key, generation, text,
          JSON.stringify({ kind: "direct", ticketId: ticket.ticket_id, runId: input.runId }),
          idempotencyKey, stamp, stamp);
      inserted = created.changes === 1;
    }

    const payload = {
      runId: input.runId,
      direct: true,
      expectsDelivery: true,
      durableDelivery: true,
      deliveryPending: true,
      payloadSha256: createHash("sha256").update(text).digest("hex"),
      idempotencyKey,
    };
    const firstReady = !ticket.response_ready_at;
    db.prepare(`UPDATE tickets SET result_json=?,response_ready_at=COALESCE(response_ready_at,?),
      delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`)
      .run(JSON.stringify(payload), stamp, stamp, ticket.ticket_id);
    if (firstReady) addEvent(db, ticket.ticket_id, "response_ready", payload, stamp);
    if (inserted) addEvent(db, ticket.ticket_id, "direct_response_durable", {
      runId: input.runId,
      ownerGeneration: generation,
      idempotencyKey,
      payloadSha256: payload.payloadSha256,
    }, stamp);
    db.exec("COMMIT");
    return {
      staged: true as const,
      ticketId: ticket.ticket_id,
      ownerGeneration: generation,
      idempotencyKey,
      nativeText: nativePayloadText(text, idempotencyKey),
    };
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function markDashboardAwaiting(path: string, runId: string, now = new Date()) {
  const initial = dashboardTicket(path, runId);
  if (!initial) return "not-dashboard" as const;
  const pending = pendingDirectResult(path, runId);
  if (pending) return "durable-owned" as const;

  const db = openDb(path), stamp = now.toISOString();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT ticket_id,response_ready_at FROM tickets WHERE run_id=? AND status='accepted'
      AND workflow_eligible=0 AND workflow_id IS NULL ORDER BY created_at DESC LIMIT 1`).get(runId) as
      { ticket_id?: string; response_ready_at?: string | null } | undefined;
    if (!row?.ticket_id) { db.exec("COMMIT"); return "not-dashboard" as const; }
    if (!row.response_ready_at) {
      const payload = { runId, direct: true, expectsDelivery: true, durableDelivery: false };
      db.prepare("UPDATE tickets SET result_json=?,response_ready_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(JSON.stringify(payload), stamp, stamp, row.ticket_id);
      addEvent(db, row.ticket_id, "response_ready", payload, stamp);
    }
    db.exec("COMMIT");
    return "native-awaiting" as const;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

export function settleDashboardNativeDelivery(path: string, runId: string, now = new Date()) {
  const db = openDb(path), stamp = now.toISOString();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT t.ticket_id,d.delivery_id,d.idempotency_key FROM tickets t
      JOIN cnx_assistant_delivery d ON d.ticket_id=t.ticket_id
      WHERE t.run_id=? AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND t.response_ready_at IS NOT NULL AND d.kind='direct_result' AND d.status='pending'
      ORDER BY d.delivery_id DESC LIMIT 1`).get(runId) as
      { ticket_id?: string; delivery_id?: number; idempotency_key?: string } | undefined;
    if (!row?.ticket_id || !row.delivery_id) { db.exec("COMMIT"); return false; }
    db.prepare(`UPDATE tickets SET status='completed',delivery_confirmed_at=?,delivery_last_error=NULL,
      failure_class=NULL,failure_message=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`)
      .run(stamp, stamp, row.ticket_id);
    db.prepare(`UPDATE cnx_assistant_delivery SET status='delivered',last_error=NULL,updated_at=?,delivered_at=?
      WHERE delivery_id=? AND status='pending'`).run(stamp, stamp, row.delivery_id);
    addEvent(db, row.ticket_id, "delivery_confirmed", {
      runId,
      source: "native-dashboard-marker",
      idempotencyKey: row.idempotency_key,
    }, stamp);
    addEvent(db, row.ticket_id, "completed", {
      runId,
      direct: true,
      deliveryConfirmed: true,
      durablePayload: true,
      deliveryMode: "native-dashboard-marker",
    }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function recordPendingDeliveryFailure(path: string, runId: string, message: string, now = new Date()) {
  const db = openDb(path), stamp = now.toISOString(), detail = message.slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT t.ticket_id,d.delivery_id FROM tickets t JOIN cnx_assistant_delivery d ON d.ticket_id=t.ticket_id
      WHERE t.run_id=? AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND d.kind='direct_result' AND d.status='pending' ORDER BY d.delivery_id DESC LIMIT 1`).get(runId) as
      { ticket_id?: string; delivery_id?: number } | undefined;
    if (!row?.ticket_id) { db.exec("COMMIT"); return false; }
    db.prepare("UPDATE tickets SET delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
      .run(detail, stamp, row.ticket_id);
    addEvent(db, row.ticket_id, "direct_native_delivery_failed", { runId, message: detail, durableRetry: true }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function unverifiableDashboardRuns(path: string, input: { now: Date; olderThanMs?: number; limit?: number }) {
  const cutoff = new Date(input.now.getTime() - Math.max(1000, input.olderThanMs ?? 120000)).toISOString();
  const limit = Math.max(1, Math.min(input.limit ?? 100, 1000));
  const db = openDb(path, true);
  try {
    const rows = db.prepare(`SELECT run_id,owner_session_key FROM tickets
      WHERE status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL
        AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL AND response_ready_at<=?
        AND NOT EXISTS (SELECT 1 FROM cnx_assistant_delivery d
          WHERE d.ticket_id=tickets.ticket_id AND d.kind='direct_result')
      ORDER BY response_ready_at,ticket_id LIMIT ?`).all(cutoff, limit) as
      Array<{ run_id?: string; owner_session_key?: string }>;
    return rows
      .filter((row) => typeof row.run_id === "string" && typeof row.owner_session_key === "string" && isDashboardSession(row.owner_session_key))
      .map((row) => String(row.run_id));
  } finally { db.close(); }
}

function kickHostDelivery(workspace: string, cfg: DashboardVerifiedDeliveryConfig) {
  const script = resolve(workspace, "skills", "cogentnexus-openclaw", "scripts", "host_delivery.py");
  if (!existsSync(script)) return false;
  const root = resolve(cfg.cogentNexusOpenClawRoot ?? join(workspace, ".cogentnexus-openclaw"));
  try {
    const child = spawn(cfg.pythonCommand ?? "python", [script, "--root", root, "flush"], {
      detached: true,
      stdio: "ignore",
      windowsHide: true,
    });
    child.unref();
    return true;
  } catch { return false; }
}

/** Supersede the v0.9 Dashboard no-receipt bypass only at the v0.9.1 release boundary. */
export function installV091DashboardVerifiedDelivery(api: any, cfg: DashboardVerifiedDeliveryConfig = {}) {
  const prototype = TicketStore.prototype as any;
  if (prototype[PATCH]) return;
  Object.defineProperty(prototype, PATCH, { value: true });

  const finalize = TicketStore.prototype.finalizeDirectRun;
  const confirm = TicketStore.prototype.confirmDirectDelivery;
  const fail = TicketStore.prototype.failDirectDelivery;
  const recover = TicketStore.prototype.recoverUndeliveredDirect;

  TicketStore.prototype.finalizeDirectRun = function(input: Parameters<TicketStore["finalizeDirectRun"]>[0]) {
    if (input.success) {
      const state = markDashboardAwaiting(this.databasePath, input.runId, input.now ?? new Date());
      // Durable Dashboard text is already response-ready before transport. Returning unchanged
      // intentionally makes the legacy run maps clean up instead of consuming an unrelated
      // message_sent receipt; the durable delivery row now owns terminal settlement.
      if (state === "durable-owned") return "unchanged";
      if (state === "native-awaiting") return "awaiting_delivery";
    }
    return finalize.call(this, input);
  };

  TicketStore.prototype.confirmDirectDelivery = function(input: Parameters<TicketStore["confirmDirectDelivery"]>[0]) {
    // A staged text result is settled only by the final dispatcher outcome below (or by
    // host_delivery.py after marker-based replay/deduplication). Ignore generic receipts.
    if (pendingDirectResult(this.databasePath, input.runId)) return "unchanged";
    return confirm.call(this, input);
  };

  TicketStore.prototype.failDirectDelivery = function(input: Parameters<TicketStore["failDirectDelivery"]>[0]) {
    if (pendingDirectResult(this.databasePath, input.runId)) {
      recordPendingDeliveryFailure(this.databasePath, input.runId, input.message ?? "native Dashboard delivery failed", input.now ?? new Date());
      return "waiting";
    }
    return fail.call(this, input);
  };

  TicketStore.prototype.recoverUndeliveredDirect = function(input: Parameters<TicketStore["recoverUndeliveredDirect"]>[0] = {}) {
    const now = input.now ?? new Date();
    // v0.9.2 owns the durable-result boundary. Once a direct_result row exists,
    // response_ready_at is the immutable first-ready timestamp and must never be
    // refreshed to postpone a legacy timeout. The inner v0.9.2 recovery wrapper
    // filters those durable rows before legacy promotion can regenerate inference.
    // A response that reached response_ready without a durable payload is still
    // unverifiable: fail it closed after the receipt deadline instead of regenerating.
    const message = "direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output";
    for (const runId of unverifiableDashboardRuns(this.databasePath, { now, olderThanMs: input.olderThanMs, limit: input.limit })) {
      finalize.call(this, { runId, success: false, interrupted: false, message, now });
    }
    return recover.call(this, { ...input, now });
  };

  api.on?.("reply_dispatch", (event: any, ctx: any) => {
    const runId = typeof event?.runId === "string" ? event.runId
      : typeof ctx?.runId === "string" ? ctx.runId : undefined;
    if (!runId || typeof ctx?.dispatcher?.appendBeforeDeliver !== "function") return;
    let owned = false;
    let waiterStarted = false;
    const workspace = resolve(cfg.workspaceDir ?? process.cwd());
    const path = resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspace));

    ctx.dispatcher.appendBeforeDeliver((payload: any, info: any) => {
      if (info?.kind !== "final" || owned) return payload;
      const text = typeof payload?.text === "string" ? payload.text.trim() : "";
      const finalCount = Number(ctx.dispatcher.getQueuedCounts?.().final ?? 1);
      const hasMedia = Boolean(payload?.mediaUrl || (Array.isArray(payload?.mediaUrls) && payload.mediaUrls.length > 0));
      // Exact replay currently owns only the normal one-text-final Dashboard case. Rich or
      // multi-final replies remain on OpenClaw's native receipt-confirmed path rather than
      // pretending a partial payload is durably replayable.
      if (!text || hasMedia || finalCount !== 1) return payload;

      const staged = stageDashboardDirectResult(path, { runId, text });
      if (!staged.staged) return payload;
      owned = true;
      pulseManagedWorkers(); // arm the 30s durable-delivery retry deadline before transport
      api.logger?.info?.(`CogentNexus-OpenClaw durably staged Dashboard Direct result ${staged.ticketId} before native delivery`);

      if (!waiterStarted) {
        waiterStarted = true;
        queueMicrotask(() => { void (async () => {
          try {
            await ctx.dispatcher.waitForIdle();
            const failed = Number(ctx.dispatcher.getFailedCounts?.().final ?? 0);
            const cancelled = Number(ctx.dispatcher.getCancelledCounts?.().final ?? 0);
            if (failed === 0 && cancelled === 0) {
              settleDashboardNativeDelivery(path, runId);
            } else {
              const message = failed > 0 ? `final delivery failed count=${failed}` : `final delivery cancelled count=${cancelled}`;
              recordPendingDeliveryFailure(path, runId, message);
              kickHostDelivery(workspace, cfg);
              pulseManagedWorkers();
            }
          } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            recordPendingDeliveryFailure(path, runId, message);
            kickHostDelivery(workspace, cfg);
            pulseManagedWorkers();
          }
        })(); });
      }
      return { ...payload, text: staged.nativeText };
    });
  }, { priority: 600 });
}
