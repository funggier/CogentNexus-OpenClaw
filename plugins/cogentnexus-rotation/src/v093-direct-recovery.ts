import { createHash, randomUUID } from "node:crypto";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

export type V093DirectRecoveryConfig = {
  cogentRoot?: string;
  timeoutSeconds?: number;
  pythonCommand?: string;
  agentId?: string;
};

export type V093DirectRecovery = {
  ticket_id: string;
  owner_session_key: string;
  prompt: string;
  mode: "resume" | "redeliver";
  attempt_count: number;
  owner_generation: number;
};

type ClaimIdentity = {
  authorized: boolean;
  reason: string;
};

type OriginalModel = {
  provider?: string;
  model?: string;
};

const CLAIM_POLL_MS = 500;

function now() {
  return new Date().toISOString();
}

function delay(ms: number) {
  return new Promise<void>((resolveDelay) => setTimeout(resolveDelay, ms));
}

function openDb(path: string, readOnly = false) {
  if (!readOnly) new TicketStore(path).snapshot();
  const db = readOnly ? new DatabaseSync(path, { readOnly: true }) : new DatabaseSync(path);
  if (!readOnly) db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  return db;
}

function tableExists(db: DatabaseSync, name: string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

function addEvent(db: DatabaseSync, ticketId: string, eventType: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, eventType, JSON.stringify(payload), stamp);
}

function originalModel(path: string, ticketId: string): OriginalModel {
  const db = openDb(path, true);
  try {
    if (!tableExists(db, "cnx_direct_model_call")) return {};
    const row = db.prepare("SELECT provider,model FROM cnx_direct_model_call WHERE ticket_id=? LIMIT 1")
      .get(ticketId) as { provider?: string | null; model?: string | null } | undefined;
    return {
      ...(typeof row?.provider === "string" && row.provider ? { provider: row.provider } : {}),
      ...(typeof row?.model === "string" && row.model ? { model: row.model } : {}),
    };
  } finally {
    db.close();
  }
}

function claimIdentity(path: string, recovery: V093DirectRecovery, runId?: string): ClaimIdentity {
  const db = openDb(path, true);
  try {
    const row = db.prepare(`SELECT t.status,t.workflow_eligible,t.workflow_id,
      s.state AS session_state,s.generation,
      r.state AS recovery_state,r.active_run_id,r.owner_generation
      FROM tickets t
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id
      WHERE t.ticket_id=?`).get(recovery.ticket_id) as any;
    if (!row) return { authorized: false, reason: "ticket-or-recovery-missing" };
    if (row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.workflow_id) {
      return { authorized: false, reason: `ticket-${String(row.status ?? "missing")}` };
    }
    if (row.session_state !== "active" || Number(row.generation) !== recovery.owner_generation ||
        Number(row.owner_generation) !== recovery.owner_generation) {
      return { authorized: false, reason: "session-authority-superseded" };
    }
    if (row.recovery_state !== "running") {
      return { authorized: false, reason: `recovery-${String(row.recovery_state ?? "missing")}` };
    }
    if (runId && row.active_run_id !== runId) {
      return { authorized: false, reason: "recovery-claim-superseded" };
    }
    return { authorized: true, reason: "authorized" };
  } finally {
    db.close();
  }
}

function claim(path: string, recovery: V093DirectRecovery, runId: string) {
  const db = openDb(path);
  try {
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET state='running',attempt_count=attempt_count+1,
      active_run_id=?,next_attempt_at=NULL,last_error=NULL,updated_at=?
      WHERE ticket_id=? AND state='pending' AND owner_generation=?
        AND EXISTS (SELECT 1 FROM tickets t JOIN cnx_sessions s ON s.session_key=t.owner_session_key
          WHERE t.ticket_id=? AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
            AND s.state='active' AND s.generation=?)`)
      .run(runId, now(), recovery.ticket_id, recovery.owner_generation, recovery.ticket_id, recovery.owner_generation).changes) === 1;
  } finally {
    db.close();
  }
}

function bindRun(path: string, recovery: V093DirectRecovery, oldRunId: string, newRunId: string) {
  if (oldRunId === newRunId) return true;
  const db = openDb(path);
  try {
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET active_run_id=?,updated_at=?
      WHERE ticket_id=? AND state='running' AND active_run_id=? AND owner_generation=?`)
      .run(newRunId, now(), recovery.ticket_id, oldRunId, recovery.owner_generation).changes) === 1;
  } finally {
    db.close();
  }
}

function retry(path: string, recovery: V093DirectRecovery, runId: string, message: string) {
  const db = openDb(path), stamp = new Date();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT r.attempt_count,t.status,t.workflow_eligible,t.workflow_id,
      s.state AS session_state,s.generation
      FROM cnx_direct_recovery r
      JOIN tickets t ON t.ticket_id=r.ticket_id
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      WHERE r.ticket_id=? AND r.state='running' AND r.active_run_id=? AND r.owner_generation=?`)
      .get(recovery.ticket_id, runId, recovery.owner_generation) as any;
    if (!row || row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.workflow_id ||
        row.session_state !== "active" || Number(row.generation) !== recovery.owner_generation) {
      db.exec("COMMIT");
      return false;
    }
    const attempt = Math.max(1, Number(row.attempt_count ?? 1));
    const backoff = [5, 15, 30, 60, 120, 300][Math.min(5, attempt - 1)] * 1000;
    const next = new Date(stamp.getTime() + backoff).toISOString();
    const detail = message.slice(0, 2000);
    db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,
      last_error=?,updated_at=? WHERE ticket_id=? AND state='running' AND active_run_id=?`)
      .run(next, detail, stamp.toISOString(), recovery.ticket_id, runId);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=?
      WHERE ticket_id=? AND status='accepted'`).run(detail, detail, stamp.toISOString(), recovery.ticket_id);
    addEvent(db, recovery.ticket_id, "direct_recovery_retry", {
      runId,
      message: detail,
      nextAttemptAt: next,
      attempt,
      source: "v093-direct-recovery",
    }, stamp.toISOString());
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

function roleText(message: any) {
  const content = message?.content;
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";
  return content.map((part: any) => {
    if (typeof part === "string") return part;
    if (!part || typeof part !== "object") return "";
    return typeof part.text === "string" ? part.text : typeof part.content === "string" ? part.content : "";
  }).filter(Boolean).join("\n").trim();
}

function isInternalControlText(text: string) {
  return /#cogent-direct\b|\[CogentNexus (?:Delivery|Continuation|Internal|Direct Recovery):|\[CogentNexus Internal /iu.test(text);
}

function boundedOwnerContext(messages: unknown[], maxChars = 12_000) {
  const lines: string[] = [];
  for (const raw of messages) {
    const message = raw as any;
    if (!["user", "assistant"].includes(message?.role)) continue;
    const text = roleText(message);
    if (!text || isInternalControlText(text)) continue;
    lines.push(`${String(message.role).toUpperCase()}:\n${text}`);
  }
  let value = lines.join("\n\n");
  if (value.length > maxChars) value = value.slice(value.length - maxChars);
  return value;
}

function lastAssistantText(messages: unknown[]) {
  for (let index = messages.length - 1; index >= 0; index--) {
    const message = messages[index] as any;
    if (message?.role !== "assistant") continue;
    const text = roleText(message);
    if (text) return text;
  }
  return undefined;
}

function agentIdFromSession(sessionKey: string, fallback = "main") {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1] ?? fallback;
}

function hiddenSessionKey(ownerSessionKey: string, purpose: string, generation: number, cfg: V093DirectRecoveryConfig) {
  const agentId = agentIdFromSession(ownerSessionKey, cfg.agentId ?? "main");
  const ownerHash = createHash("sha256").update(ownerSessionKey).digest("hex").slice(0, 12);
  const safePurpose = purpose.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 42);
  return `agent:${agentId}:subagent:cnx-${safePurpose}-${ownerHash}-g${generation}-${randomUUID().slice(0, 8)}`;
}

function recoveryPrompt(recovery: V093DirectRecovery, context: string) {
  const instruction = recovery.mode === "redeliver"
    ? "Reconstruct only the compact final response. Do not repeat external side effects."
    : "Resume the interrupted request from the latest committed state. Do not repeat completed side effects.";
  return [
    "[CogentNexus Internal Direct Recovery]",
    "This is an internal recovery worker session, not a new user instruction.",
    instruction,
    "Preserve the original user intent. Inspect durable state and existing artifacts when useful.",
    "Return only the user-facing assistant response that should be delivered to the owner session.",
    "",
    "Original committed request:", recovery.prompt,
    "",
    "Bounded read-only owner-session context:", context || "(no usable recent context)",
  ].join("\n");
}

function kickHostDelivery(workspace: string, cfg: V093DirectRecoveryConfig) {
  const preferred = resolve(workspace, "skills", "cogentnexus", "scripts", "host_delivery_v092.py");
  const fallback = resolve(workspace, "skills", "cogentnexus", "scripts", "host_delivery.py");
  const script = existsSync(preferred) ? preferred : fallback;
  if (!existsSync(script)) return false;
  const root = resolve(cfg.cogentRoot ?? join(workspace, ".cogent"));
  try {
    const child = spawn(cfg.pythonCommand ?? "python", [script, "--root", root, "flush"], {
      detached: true,
      stdio: "ignore",
      windowsHide: true,
    });
    child.unref();
    return true;
  } catch {
    return false;
  }
}

function markResponseReady(
  path: string,
  recovery: V093DirectRecovery,
  runId: string,
  text: string,
  provenance: OriginalModel,
) {
  const db = openDb(path), stamp = now();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT t.status,t.workflow_eligible,t.workflow_id,t.response_ready_at,
      s.state AS session_state,s.generation,
      r.state AS recovery_state,r.active_run_id,r.owner_generation
      FROM tickets t
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id
      WHERE t.ticket_id=?`).get(recovery.ticket_id) as any;
    if (!row || row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.workflow_id ||
        row.session_state !== "active" || Number(row.generation) !== recovery.owner_generation ||
        row.recovery_state !== "running" || row.active_run_id !== runId ||
        Number(row.owner_generation) !== recovery.owner_generation) {
      db.exec("COMMIT");
      return false;
    }

    const idempotencyKey = `cnx-direct-result:${recovery.ticket_id}:g${recovery.owner_generation}`;
    const existing = db.prepare("SELECT text,status FROM cnx_assistant_delivery WHERE idempotency_key=?")
      .get(idempotencyKey) as { text?: string; status?: string } | undefined;
    if (existing && existing.text !== text) {
      throw new Error(`durable Direct recovery result changed for ${recovery.ticket_id} generation ${recovery.owner_generation}`);
    }
    if (!existing) {
      db.prepare(`INSERT INTO cnx_assistant_delivery(
        ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
        attempt_count,last_error,created_at,updated_at) VALUES (?,?,?,'direct_result',?,?,?,'pending',0,NULL,?,?)`)
        .run(recovery.ticket_id, recovery.owner_session_key, recovery.owner_generation, text,
          JSON.stringify({ kind: "direct", ticketId: recovery.ticket_id, runId }), idempotencyKey, stamp, stamp);
    }

    const firstReady = !row.response_ready_at;
    db.prepare(`UPDATE tickets SET result_json=?,response_ready_at=COALESCE(response_ready_at,?),
      delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`)
      .run(JSON.stringify({
        directRecovery: true,
        runId,
        deliveryPending: true,
        originalProvider: provenance.provider ?? null,
        originalModel: provenance.model ?? null,
        recoveryModel: provenance.model ?? null,
      }), stamp, stamp, recovery.ticket_id);
    db.prepare(`UPDATE cnx_direct_recovery SET state='awaiting_delivery',active_run_id=NULL,next_attempt_at=NULL,
      last_error=NULL,updated_at=? WHERE ticket_id=? AND state='running' AND active_run_id=?`)
      .run(stamp, recovery.ticket_id, runId);
    addEvent(db, recovery.ticket_id, "direct_recovery_response_ready", {
      runId,
      deliveryMode: "host-chat-inject",
      ownerGeneration: recovery.owner_generation,
      originalProvider: provenance.provider ?? null,
      originalModel: provenance.model ?? null,
      recoveryModel: provenance.model ?? null,
      responseReadyFirstCommit: firstReady,
      source: "v093-direct-recovery",
    }, stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally {
    db.close();
  }
}

async function waitForClaimRevocation(
  path: string,
  recovery: V093DirectRecovery,
  runId: string,
  stopped: () => boolean,
) {
  while (!stopped()) {
    await delay(CLAIM_POLL_MS);
    if (stopped()) break;
    const identity = claimIdentity(path, recovery, runId);
    if (!identity.authorized) return identity.reason;
  }
  return undefined;
}

function recordRuntimeAbort(path: string, recovery: V093DirectRecovery, runId: string, reason: string) {
  const db = openDb(path), stamp = now();
  try {
    addEvent(db, recovery.ticket_id, "direct_recovery_runtime_aborted", {
      runId,
      reason,
      ownerGeneration: recovery.owner_generation,
      source: "v093-direct-recovery",
    }, stamp);
  } finally {
    db.close();
  }
}

/**
 * Direct recovery executor with four hard boundaries:
 * 1) preserve the original model when it was durably observed,
 * 2) terminate the hidden worker when Ticket/recovery/session authority is revoked,
 * 3) commit response_ready_at once only,
 * 4) prefer the v0.9.2 durable delivery transport.
 */
export async function launchV093DirectRecovery(
  api: any,
  path: string,
  workspace: string,
  recovery: V093DirectRecovery,
  cfg: V093DirectRecoveryConfig,
) {
  const attempt = Number(recovery.attempt_count) + 1;
  const planned = `cnx-direct-${recovery.ticket_id.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 48)}-${attempt}-g${recovery.owner_generation}`;
  if (!claim(path, recovery, planned)) return;

  const childSessionKey = hiddenSessionKey(
    recovery.owner_session_key,
    `recovery-${recovery.ticket_id}`,
    recovery.owner_generation,
    cfg,
  );
  const provenance = originalModel(path, recovery.ticket_id);
  let runId = planned;
  let stopFence = false;

  try {
    const initialIdentity = claimIdentity(path, recovery, planned);
    if (!initialIdentity.authorized) return;

    const owner = await api.runtime.subagent.getSessionMessages({ sessionKey: recovery.owner_session_key, limit: 24 });
    const beforeLaunch = claimIdentity(path, recovery, planned);
    if (!beforeLaunch.authorized) return;

    const launched = await api.runtime.subagent.run({
      sessionKey: childSessionKey,
      message: recoveryPrompt(recovery, boundedOwnerContext(owner.messages ?? [])),
      deliver: false,
      lightContext: true,
      idempotencyKey: planned,
      ...(provenance.model ? { model: provenance.model } : {}),
    });
    runId = launched.runId;
    if (!bindRun(path, recovery, planned, runId)) {
      try { await api.runtime.subagent.deleteSession({ sessionKey: childSessionKey, deleteTranscript: true }); } catch {}
      return;
    }

    const timeoutMs = Math.max(60_000, Math.min((cfg.timeoutSeconds ?? 3600) * 1000, 3_600_000));
    const completionPromise = api.runtime.subagent.waitForRun({ runId, timeoutMs })
      .then((waited: any) => ({ kind: "completion" as const, waited }));
    const revocationPromise = waitForClaimRevocation(path, recovery, runId, () => stopFence)
      .then((reason) => ({ kind: "revocation" as const, reason }));
    const outcome = await Promise.race([completionPromise, revocationPromise]);
    stopFence = true;

    if (outcome.kind === "revocation") {
      const reason = outcome.reason ?? "recovery-authority-revoked";
      try { await api.runtime.subagent.deleteSession({ sessionKey: childSessionKey, deleteTranscript: true }); } catch {}
      recordRuntimeAbort(path, recovery, runId, reason);
      return;
    }

    const waited = outcome.waited;
    const identity = claimIdentity(path, recovery, runId);
    if (!identity.authorized) {
      recordRuntimeAbort(path, recovery, runId, identity.reason);
      return;
    }
    if (waited.status === "timeout") {
      retry(path, recovery, runId, "Direct recovery run timed out");
      return;
    }
    if (waited.status !== "ok") {
      retry(path, recovery, runId, waited.error ?? "Direct recovery run failed");
      return;
    }

    const child = await api.runtime.subagent.getSessionMessages({ sessionKey: childSessionKey, limit: 24 });
    const afterRead = claimIdentity(path, recovery, runId);
    if (!afterRead.authorized) {
      recordRuntimeAbort(path, recovery, runId, afterRead.reason);
      return;
    }
    const text = lastAssistantText(child.messages ?? []);
    if (!text) {
      retry(path, recovery, runId, "Direct recovery produced no visible assistant output");
      return;
    }
    if (markResponseReady(path, recovery, runId, text, provenance)) kickHostDelivery(workspace, cfg);
  } catch (error) {
    const identity = claimIdentity(path, recovery, runId);
    if (identity.authorized) retry(path, recovery, runId, error instanceof Error ? error.message : String(error));
  } finally {
    stopFence = true;
    try { await api.runtime.subagent.deleteSession({ sessionKey: childSessionKey, deleteTranscript: true }); } catch {}
  }
}
