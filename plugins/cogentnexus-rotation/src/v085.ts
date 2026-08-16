import { createHash, randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import { existsSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { classifyDurableRequest } from "./admission.js";
import { parseDeliveryMarker, settleDeliveryTarget, type DeliveryTarget } from "./delivery-continuity.js";
import baseEntry from "./index.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type Cfg = {
  cogentRoot?: string;
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  timeoutSeconds?: number;
  admissionMinimumScore?: number;
  pythonCommand?: string;
  agentId?: string;
};

type Recovery = {
  ticket_id: string;
  owner_session_key: string;
  prompt: string;
  mode: "resume" | "redeliver";
  attempt_count: number;
};

type Turn = {
  sessionKey: string;
  delayMs: number;
  deleteAfterRun: boolean;
  deliveryMode: "announce";
  name: string;
  tag: string;
  message: string;
};

type AssistantDeliveryTarget =
  | { kind: "direct"; ticketId: string; runId: string }
  | DeliveryTarget
  | { kind: "notice" };

const PATCH = Symbol.for("cogentnexus.v085.ticket-patch");
const WRAP = Symbol.for("cogentnexus.v085.entry-wrap");
const now = () => new Date().toISOString();
const dbPath = (cfg: Cfg, workspace: string) =>
  resolve(cfg.ticketDatabasePath ?? defaultTicketDatabase(workspace));

function openDb(path: string) {
  new TicketStore(path).snapshot();
  const db = new DatabaseSync(path);
  db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      mode TEXT NOT NULL DEFAULT 'resume',
      state TEXT NOT NULL DEFAULT 'pending',
      attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_cnx_direct_recovery_run
      ON cnx_direct_recovery(active_run_id) WHERE active_run_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_cnx_direct_recovery_due
      ON cnx_direct_recovery(state,next_attempt_at,updated_at);
    CREATE TABLE IF NOT EXISTS cnx_assistant_delivery(
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id TEXT REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      owner_session_key TEXT NOT NULL,
      kind TEXT NOT NULL,
      text TEXT NOT NULL,
      target_json TEXT,
      idempotency_key TEXT NOT NULL UNIQUE,
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','delivered')),
      attempt_count INTEGER NOT NULL DEFAULT 0,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      delivered_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_pending
      ON cnx_assistant_delivery(status,delivery_id);
  `);
  return db;
}

function addEvent(db: DatabaseSync, ticketId: string, type: string, payload: unknown, stamp: string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId, type, JSON.stringify(payload), stamp);
}

function queueRecovery(db: DatabaseSync, ticketId: string, mode: "resume" | "redeliver", message: string, stamp: string) {
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,created_at,updated_at
    ) VALUES (?,?,'pending',0,NULL,?,?,?,?)
    ON CONFLICT(ticket_id) DO UPDATE SET
      mode=excluded.mode,state='pending',active_run_id=NULL,
      next_attempt_at=excluded.next_attempt_at,last_error=excluded.last_error,updated_at=excluded.updated_at`)
    .run(ticketId, mode, stamp, message.slice(0, 2000), stamp, stamp);
}

export function queueAssistantDelivery(path: string, input: {
  ticketId?: string;
  ownerSessionKey: string;
  kind: string;
  text: string;
  target: AssistantDeliveryTarget;
  idempotencyKey: string;
  now?: Date;
}) {
  const db = openDb(path);
  const stamp = (input.now ?? new Date()).toISOString();
  try {
    const changed = db.prepare(`INSERT OR IGNORE INTO cnx_assistant_delivery(
        ticket_id,owner_session_key,kind,text,target_json,idempotency_key,status,
        attempt_count,last_error,created_at,updated_at
      ) VALUES (?,?,?,?,?,?,'pending',0,NULL,?,?)`)
      .run(input.ticketId ?? null,input.ownerSessionKey,input.kind,input.text,
        JSON.stringify(input.target),input.idempotencyKey,stamp,stamp);
    return changed.changes === 1;
  } finally { db.close(); }
}

export function markDirectRecovery(path: string, input: {
  runId: string; mode: "resume" | "redeliver"; message?: string; now?: Date;
}) {
  const db = openDb(path);
  const stamp = (input.now ?? new Date()).toISOString();
  const message = (input.message ?? "Direct run interrupted").slice(0, 2000);
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT ticket_id FROM tickets
      WHERE run_id=? AND status='accepted' AND workflow_eligible=0
      ORDER BY created_at DESC LIMIT 1`).get(input.runId) as any;
    if (!row) { db.exec("COMMIT"); return false; }
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,
      delivery_last_error=?,response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=?
      WHERE ticket_id=?`).run(message,message,stamp,row.ticket_id);
    queueRecovery(db,row.ticket_id,input.mode,message,stamp);
    addEvent(db,row.ticket_id,input.mode === "redeliver" ? "direct_redelivery_pending" : "direct_retry_pending",
      {runId:input.runId,message},stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function markSession(path: string, sessionKey: string, message: string) {
  const db = openDb(path), stamp = now();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT ticket_id,run_id FROM tickets
      WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0
        AND response_ready_at IS NULL ORDER BY created_at DESC LIMIT 1`).get(sessionKey) as any;
    if (!row) { db.exec("COMMIT"); return false; }
    db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=?")
      .run(message,stamp,row.ticket_id);
    queueRecovery(db,row.ticket_id,"resume",message,stamp);
    addEvent(db,row.ticket_id,"direct_retry_pending",{runId:row.run_id,sessionKey,message},stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function isRecoverableDirectFailure(input: { success: boolean; interrupted: boolean; message?: string }) {
  if (input.success) return false;
  return input.interrupted || /reply operation aborted by user/i.test(input.message ?? "");
}

export function patchTicketStore() {
  const proto = TicketStore.prototype as any;
  if (proto[PATCH]) return;
  Object.defineProperty(proto,PATCH,{value:true});
  const finalize = TicketStore.prototype.finalizeDirectRun;
  const failDelivery = TicketStore.prototype.failDirectDelivery;

  TicketStore.prototype.finalizeDirectRun = function(input: Parameters<TicketStore["finalizeDirectRun"]>[0]) {
    if (isRecoverableDirectFailure(input)) {
      return markDirectRecovery(this.databasePath,{runId:input.runId,mode:"resume",message:input.message,now:input.now})
        ? "waiting" : "unchanged";
    }
    return finalize.call(this,input);
  };

  TicketStore.prototype.failDirectDelivery = function(input: Parameters<TicketStore["failDirectDelivery"]>[0]) {
    return markDirectRecovery(this.databasePath,{runId:input.runId,mode:"redeliver",message:input.message,now:input.now})
      ? "waiting" : failDelivery.call(this,input);
  };

  TicketStore.prototype.recoverUndeliveredDirect = function(
    input: Parameters<TicketStore["recoverUndeliveredDirect"]>[0] = {},
  ) {
    const db = openDb(this.databasePath);
    const current = input.now ?? new Date();
    const cutoff = new Date(current.getTime()-Math.max(1000,input.olderThanMs ?? 120000)).toISOString();
    const stamp = current.toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows = db.prepare(`SELECT ticket_id,run_id FROM tickets
        WHERE status='accepted' AND workflow_eligible=0
          AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL
          AND response_ready_at<=? ORDER BY response_ready_at LIMIT ?`)
        .all(cutoff,Math.max(1,Math.min(input.limit ?? 100,1000))) as any[];
      for (const row of rows) {
        const message = "Direct response delivery was not confirmed before deadline";
        db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,
          delivery_last_error=?,response_ready_at=NULL,updated_at=? WHERE ticket_id=?`)
          .run(message,message,stamp,row.ticket_id);
        queueRecovery(db,row.ticket_id,"redeliver",message,stamp);
        addEvent(db,row.ticket_id,"direct_redelivery_timeout",{runId:row.run_id,cutoff},stamp);
      }
      db.exec("COMMIT");
      return [];
    } catch (error) {
      try { db.exec("ROLLBACK"); } catch {}
      throw error;
    } finally { db.close(); }
  };

  TicketStore.prototype.promotePendingDirectForSession = function(
    input: Parameters<TicketStore["promotePendingDirectForSession"]>[0],
  ) {
    markSession(this.databasePath,input.sessionKey,input.reason ?? "Post-compaction continuation");
    return undefined;
  };
}

export const directRecoveryBackoffMs = (attempt: number) =>
  [5,15,30,60,120,300][Math.max(0,Math.min(5,attempt-1))] * 1000;

function resetWorkflowCompletions(workspace: string) {
  const root = resolve(workspace,".cogent","workflows");
  if (!existsSync(root)) return 0;
  let count = 0;
  for (const entry of readdirSync(root,{withFileTypes:true})) {
    if (!entry.isDirectory()) continue;
    const path = join(root,entry.name,"completion.json");
    if (!existsSync(path)) continue;
    try {
      const notice = JSON.parse(readFileSync(path,"utf8"));
      if (notice?.deliveryStatus !== "pending" || (!notice.scheduledAt && !notice.deliveryRunId)) continue;
      delete notice.scheduledAt;
      delete notice.deliveryRunId;
      const temporary = `${path}.${process.pid}.v085.tmp`;
      writeFileSync(temporary,`${JSON.stringify(notice,null,2)}\n`);
      renameSync(temporary,path);
      count += 1;
    } catch {}
  }
  return count;
}

export function prepareV085RecoveryState(workspace: string, cfg: Cfg = {}) {
  const path = dbPath(cfg,workspace), db = openDb(path), stamp = now();
  let reopened = 0, superseded = 0, outboxReset = 0;
  try {
    db.exec("BEGIN IMMEDIATE");
    const rows = db.prepare(`SELECT ticket_id,prompt,status,workflow_eligible,failure_class,failure_message
      FROM tickets WHERE status IN ('waiting','failed') AND workflow_id IS NULL AND (
        (workflow_eligible=1 AND failure_class='interrupted') OR
        (status='failed' AND workflow_eligible=0 AND failure_class='permanent'
          AND failure_message='Reply operation aborted by user')) ORDER BY created_at`).all() as any[];
    for (const row of rows) {
      if (classifyDurableRequest(row.prompt,cfg.admissionMinimumScore ?? 5).lane !== "direct") continue;
      db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id);
      const changed = db.prepare(`UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,
        lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,response_ready_at=NULL,
        delivery_confirmed_at=NULL,delivery_last_error=NULL,result_json=NULL,
        failure_class='interrupted',updated_at=? WHERE ticket_id=? AND workflow_id IS NULL`)
        .run(stamp,row.ticket_id);
      if (!changed.changes) continue;
      const legacyAbort = row.failure_class === "permanent" && row.failure_message === "Reply operation aborted by user";
      const reason = legacyAbort ? "v0.8.5 reopened legacy user-aborted Direct Ticket" : `v0.8.5 reopened ${row.status} Direct Ticket`;
      queueRecovery(db,row.ticket_id,"resume",reason,stamp);
      addEvent(db,row.ticket_id,"v085_direct_recovery_reopened",{previousStatus:row.status,legacyAbort},stamp);
      reopened += 1;
    }

    const staleRows = db.prepare(`SELECT r.ticket_id FROM cnx_direct_recovery r
      JOIN tickets t ON t.ticket_id=r.ticket_id
      WHERE r.state IN ('pending','running','awaiting_delivery') AND NOT (
        t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL)`).all() as any[];
    for (const row of staleRows) {
      const changed = db.prepare(`UPDATE cnx_direct_recovery SET state='done',active_run_id=NULL,
        next_attempt_at=NULL,last_error='superseded by terminal or workflow-owned Ticket state',updated_at=?
        WHERE ticket_id=?`).run(stamp,row.ticket_id);
      if (changed.changes) superseded += 1;
    }

    outboxReset = Number(db.prepare(`UPDATE ticket_outbox SET scheduled_at=NULL,delivery_run_id=NULL
      WHERE delivery_status='pending' AND (scheduled_at IS NOT NULL OR delivery_run_id IS NOT NULL)`).run().changes);
    db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,
      next_attempt_at=?,updated_at=? WHERE state='running'`).run(stamp,stamp);
    db.exec("COMMIT");
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
  return {databasePath:path,reopened,superseded,outboxReset,workflowDeliveryReset:resetWorkflowCompletions(workspace)};
}

function resetStale(path: string, cfg: Cfg) {
  const db = openDb(path);
  try {
    const cutoff = new Date(Date.now()-Math.max(15*60000,
      Math.min((cfg.timeoutSeconds ?? 3600)*1000+60000,4*60*60000))).toISOString();
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,
      next_attempt_at=?,last_error=COALESCE(last_error,'stale Direct recovery reset'),updated_at=?
      WHERE state='running' AND updated_at<=?`).run(now(),now(),cutoff).changes);
  } finally { db.close(); }
}

function reconcileOrphans(path: string) {
  const db = openDb(path), stamp = now();
  try {
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET state='done',active_run_id=NULL,
      next_attempt_at=NULL,last_error='superseded by terminal or workflow-owned Ticket state',updated_at=?
      WHERE state IN ('pending','running','awaiting_delivery') AND EXISTS (
        SELECT 1 FROM tickets t WHERE t.ticket_id=cnx_direct_recovery.ticket_id AND NOT (
          t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL))`)
      .run(stamp).changes);
  } finally { db.close(); }
}

function due(path: string) {
  const db = openDb(path);
  try {
    return db.prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count
      FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id
      WHERE r.state='pending' AND t.status='accepted' AND t.workflow_eligible=0
        AND t.workflow_id IS NULL AND (r.next_attempt_at IS NULL OR r.next_attempt_at<=?)
      ORDER BY COALESCE(r.next_attempt_at,r.created_at) LIMIT 1`).get(now()) as Recovery | undefined;
  } finally { db.close(); }
}

function claim(path: string, ticketId: string, runId: string) {
  const db = openDb(path);
  try {
    return db.prepare(`UPDATE cnx_direct_recovery SET state='running',attempt_count=attempt_count+1,
      active_run_id=?,next_attempt_at=NULL,last_error=NULL,updated_at=?
      WHERE ticket_id=? AND state='pending'`).run(runId,now(),ticketId).changes === 1;
  } finally { db.close(); }
}

function bindRun(path: string, ticketId: string, oldRunId: string, runId: string) {
  if (oldRunId === runId) return;
  const db = openDb(path);
  try {
    db.prepare(`UPDATE cnx_direct_recovery SET active_run_id=?,updated_at=?
      WHERE ticket_id=? AND state='running' AND active_run_id=?`)
      .run(runId,now(),ticketId,oldRunId);
  } finally { db.close(); }
}

function retry(path: string, ticketId: string, runId: string, message: string) {
  const db = openDb(path), stamp = new Date();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT attempt_count FROM cnx_direct_recovery
      WHERE ticket_id=? AND state='running' AND active_run_id=?`).get(ticketId,runId) as any;
    if (!row) { db.exec("COMMIT"); return false; }
    const next = new Date(stamp.getTime()+directRecoveryBackoffMs(Number(row.attempt_count))).toISOString();
    db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,
      next_attempt_at=?,last_error=?,updated_at=? WHERE ticket_id=?`)
      .run(next,message.slice(0,2000),stamp.toISOString(),ticketId);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=?
      WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0`)
      .run(message.slice(0,2000),message.slice(0,2000),stamp.toISOString(),ticketId);
    addEvent(db,ticketId,"direct_recovery_retry",
      {runId,message,nextAttemptAt:next,attempt:Number(row.attempt_count)},stamp.toISOString());
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function markResponseReady(path: string, input: {
  ticketId: string; runId: string; text: string; ownerSessionKey: string;
}) {
  const db = openDb(path), stamp = now();
  try {
    db.exec("BEGIN IMMEDIATE");
    const row = db.prepare(`SELECT t.status,t.workflow_eligible,t.workflow_id,r.state,r.active_run_id
      FROM tickets t JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id WHERE t.ticket_id=?`)
      .get(input.ticketId) as any;
    if (!row || row.status !== "accepted" || Number(row.workflow_eligible) !== 0 || row.workflow_id ||
        row.state !== "running" || row.active_run_id !== input.runId) {
      db.exec("COMMIT"); return false;
    }
    const idempotencyKey = `cnx-direct-result:${input.ticketId}`;
    db.prepare(`INSERT OR IGNORE INTO cnx_assistant_delivery(
      ticket_id,owner_session_key,kind,text,target_json,idempotency_key,status,
      attempt_count,last_error,created_at,updated_at)
      VALUES (?,?,'direct_result',?,?,?,'pending',0,NULL,?,?)`)
      .run(input.ticketId,input.ownerSessionKey,input.text,
        JSON.stringify({kind:"direct",ticketId:input.ticketId,runId:input.runId}),idempotencyKey,stamp,stamp);
    db.prepare(`UPDATE tickets SET result_json=?,response_ready_at=?,delivery_last_error=NULL,updated_at=?
      WHERE ticket_id=?`).run(JSON.stringify({directRecovery:true,runId:input.runId,deliveryPending:true}),
      stamp,stamp,input.ticketId);
    db.prepare(`UPDATE cnx_direct_recovery SET state='awaiting_delivery',active_run_id=NULL,
      next_attempt_at=NULL,last_error=NULL,updated_at=? WHERE ticket_id=?`).run(stamp,input.ticketId);
    addEvent(db,input.ticketId,"direct_recovery_response_ready",
      {runId:input.runId,deliveryMode:"host-chat-inject"},stamp);
    db.exec("COMMIT");
    return true;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
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

function lastAssistantText(messages: unknown[]) {
  for (let index=messages.length-1; index>=0; index-=1) {
    const message = messages[index] as any;
    if (message?.role !== "assistant") continue;
    const text = roleText(message);
    if (text) return text;
  }
  return undefined;
}

function isInternalTranscriptText(text: string) {
  return /#cogent-direct\b/iu.test(text) || /\[CogentNexus (?:Delivery|Continuation|Direct Recovery):/iu.test(text);
}

export function boundedOwnerContext(messages: unknown[], maxChars=12000) {
  const lines: string[] = [];
  for (const raw of messages) {
    const message = raw as any;
    if (!["user","assistant"].includes(message?.role)) continue;
    const text = roleText(message);
    if (!text || isInternalTranscriptText(text)) continue;
    lines.push(`${String(message.role).toUpperCase()}:\n${text}`);
  }
  let value = lines.join("\n\n");
  if (value.length > maxChars) value = value.slice(value.length-maxChars);
  return value;
}

function hiddenSessionKey(ownerSessionKey: string, cfg: Cfg) {
  const match = ownerSessionKey.match(/^agent:([^:]+):/u);
  const agentId = match?.[1] || cfg.agentId || "main";
  return `agent:${agentId}:subagent:cnx-recovery-${randomUUID()}`;
}

function recoveryPrompt(recovery: Recovery, context: string) {
  const instruction = recovery.mode === "redeliver"
    ? "Reconstruct only the compact final response. Do not repeat external side effects."
    : "Resume the interrupted request from the latest committed state. Do not repeat completed side effects.";
  return ["[CogentNexus Internal Direct Recovery]",
    "This is an internal recovery worker session, not a new user instruction.",instruction,
    "Preserve the original user intent. Inspect durable state and existing artifacts when useful.",
    "Return only the user-facing assistant response that should be delivered to the owner session.","",
    "Original committed request:",recovery.prompt,"","Bounded recent owner-session context:",
    context || "(no usable recent context)"].join("\n");
}

function statusText(prompt: string) {
  return /[\u0E00-\u0E7F]/u.test(prompt)
    ? "CogentNexus กำลังกู้คืนคำขอที่ถูกขัดจังหวะจากสถานะที่บันทึกไว้…"
    : "CogentNexus is resuming the interrupted request from committed state…";
}

function hostDeliveryScript(workspace: string) {
  return resolve(workspace,"skills","cogentnexus","scripts","host_delivery.py");
}

export function kickHostDelivery(workspace: string, cfg: Cfg) {
  const script = hostDeliveryScript(workspace);
  if (!existsSync(script)) return false;
  const root = resolve(cfg.cogentRoot ?? join(workspace,".cogent"));
  try {
    const child = spawn(cfg.pythonCommand ?? "python",[script,"--root",root,"flush"],
      {detached:true,stdio:"ignore",windowsHide:true});
    child.unref();
    return true;
  } catch { return false; }
}

function queueRecoveryStatus(path: string, workspace: string, cfg: Cfg, recovery: Recovery) {
  const inserted = queueAssistantDelivery(path,{ticketId:recovery.ticket_id,
    ownerSessionKey:recovery.owner_session_key,kind:"recovery_status",text:statusText(recovery.prompt),
    target:{kind:"notice"},idempotencyKey:`cnx-direct-status:${recovery.ticket_id}`});
  if (inserted) kickHostDelivery(workspace,cfg);
}

export async function launchRecovery(api: any, path: string, workspace: string, recovery: Recovery, cfg: Cfg) {
  const attempt = Number(recovery.attempt_count)+1;
  const plannedRunId = `cnx-direct-${recovery.ticket_id.replace(/[^A-Za-z0-9_-]/g,"-").slice(0,48)}-${attempt}-${randomUUID().slice(0,8)}`;
  if (!claim(path,recovery.ticket_id,plannedRunId)) return;
  queueRecoveryStatus(path,workspace,cfg,recovery);
  const childSessionKey = hiddenSessionKey(recovery.owner_session_key,cfg);
  let runId = plannedRunId;
  try {
    const owner = await api.runtime.subagent.getSessionMessages({sessionKey:recovery.owner_session_key,limit:24});
    const context = boundedOwnerContext(owner.messages ?? []);
    const launched = await api.runtime.subagent.run({sessionKey:childSessionKey,
      message:recoveryPrompt(recovery,context),deliver:false,lightContext:true,idempotencyKey:plannedRunId});
    runId = launched.runId;
    bindRun(path,recovery.ticket_id,plannedRunId,runId);
    const waited = await api.runtime.subagent.waitForRun({runId,
      timeoutMs:Math.max(60000,Math.min((cfg.timeoutSeconds ?? 3600)*1000,3600000))});
    if (waited.status === "timeout") {
      retry(path,recovery.ticket_id,runId,"Direct recovery run timed out");
      return;
    }
    if (waited.status !== "ok") {
      retry(path,recovery.ticket_id,runId,waited.error ?? "Direct recovery run failed");
      return;
    }
    const child = await api.runtime.subagent.getSessionMessages({sessionKey:childSessionKey,limit:24});
    const text = lastAssistantText(child.messages ?? []);
    if (!text) {
      retry(path,recovery.ticket_id,runId,"Direct recovery produced no visible assistant output");
      return;
    }
    if (markResponseReady(path,{ticketId:recovery.ticket_id,runId,text,
        ownerSessionKey:recovery.owner_session_key})) kickHostDelivery(workspace,cfg);
  } catch (error) {
    retry(path,recovery.ticket_id,runId,error instanceof Error ? error.message : String(error));
  } finally {
    try { await api.runtime.subagent.deleteSession({sessionKey:childSessionKey,deleteTranscript:true}); } catch {}
  }
}

function recoveryService(api: any, cfg: Cfg) {
  let timer: ReturnType<typeof setInterval> | undefined, active = false;
  return {id:"cogentnexus-direct-recovery-v085",start:async(ctx:any)=>{
    const workspace = resolve(cfg.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
    const path = dbPath(cfg,workspace);
    const tick = async()=>{
      if (active) return;
      active = true;
      try {
        resetStale(path,cfg);
        reconcileOrphans(path);
        kickHostDelivery(workspace,cfg);
        const recovery = due(path);
        if (recovery) await launchRecovery(api,path,workspace,recovery,cfg);
      } catch (error) {
        api.logger.warn(`CogentNexus Direct recovery scan failed: ${error instanceof Error ? error.message : String(error)}`);
      } finally { active = false; }
    };
    await tick();
    timer = setInterval(()=>void tick(),Math.max(1000,Math.min(cfg.ticketRecoveryPollMs ?? 5000,30000)));
    timer.unref?.();
  },stop:async()=>{if(timer)clearInterval(timer);timer=undefined;}};
}

function compatibilityPrompt(input: Turn, context: string) {
  return ["[CogentNexus Internal Delivery Worker]",
    "This is an internal control-plane task. Do not reinterpret it as a new user request.",
    "Produce only the compact assistant-facing result or status that should be shown to the owner.",
    "Do not repeat external side effects. Do not claim success without the committed evidence described below.","",
    input.message,"","Bounded recent owner-session context:",context || "(no usable recent context)"].join("\n");
}

function targetId(target: DeliveryTarget | undefined, input: Turn) {
  if (target?.kind === "ticket") return `ticket:${target.outboxId}`;
  if (target?.kind === "workflow") return `workflow:${target.taskId}:${target.stateRevision}`;
  return `turn:${createHash("sha256").update(`${input.sessionKey}\0${input.tag}`).digest("hex").slice(0,32)}`;
}

export async function executeCompatibilityWake(api: any, cfg: Cfg, input: Turn) {
  const workspace = resolve(cfg.workspaceDir ?? process.cwd()), path = dbPath(cfg,workspace);
  const target = parseDeliveryMarker(input.message), store = new TicketStore(path);
  const childSessionKey = hiddenSessionKey(input.sessionKey,cfg);
  try {
    const owner = await api.runtime.subagent.getSessionMessages({sessionKey:input.sessionKey,limit:24});
    const context = boundedOwnerContext(owner.messages ?? []);
    const run = await api.runtime.subagent.run({sessionKey:childSessionKey,
      message:compatibilityPrompt(input,context),deliver:false,lightContext:true,
      idempotencyKey:`cnx-hidden-${targetId(target,input)}-${randomUUID().slice(0,8)}`});
    const waited = await api.runtime.subagent.waitForRun({runId:run.runId,
      timeoutMs:Math.max(60000,Math.min((cfg.timeoutSeconds ?? 3600)*1000,3600000))});
    if (waited.status !== "ok") {
      const error = waited.status === "timeout" ? "Compatibility delivery worker timed out" :
        waited.error ?? "Compatibility delivery worker failed";
      if (target) settleDeliveryTarget({workspaceDir:workspace,store,target,success:false,error});
      return {waited,queued:false};
    }
    const child = await api.runtime.subagent.getSessionMessages({sessionKey:childSessionKey,limit:24});
    const text = lastAssistantText(child.messages ?? []);
    if (!text) {
      const error = "Compatibility delivery worker produced no visible assistant output";
      if (target) settleDeliveryTarget({workspaceDir:workspace,store,target,success:false,error});
      return {waited:{status:"error",error},queued:false};
    }
    const queued = queueAssistantDelivery(path,{ownerSessionKey:input.sessionKey,
      kind:"compatibility_result",text,target:target ?? {kind:"notice"},
      idempotencyKey:`cnx-delivery:${targetId(target,input)}`});
    if (queued) kickHostDelivery(workspace,cfg);
    return {waited,queued};
  } catch (error) {
    if (target) settleDeliveryTarget({workspaceDir:workspace,store,target,success:false,
      error:error instanceof Error ? error.message : String(error)});
    api.logger.warn(`CogentNexus compatibility wake failed for ${input.tag}: ${error instanceof Error ? error.message : String(error)}`);
    throw error;
  } finally {
    try { await api.runtime.subagent.deleteSession({sessionKey:childSessionKey,deleteTranscript:true}); } catch {}
  }
}

function compatWorkflow(api: any, cfg: Cfg) {
  const timers = new Map<string,ReturnType<typeof setTimeout>>();
  const key = (sessionKey:string,tag:string)=>`${sessionKey}\0${tag}`;
  const unschedule = async(input:{sessionKey:string;tag:string})=>{
    const id=key(input.sessionKey,input.tag),timer=timers.get(id);
    if(timer){clearTimeout(timer);timers.delete(id);}
    return {removed:timer?1:0,failed:0};
  };
  const schedule = async(input:Turn)=>{
    await unschedule(input);
    const path=dbPath(cfg,resolve(cfg.workspaceDir ?? process.cwd()));
    if(input.tag.startsWith("cogent-resume-") || input.tag.startsWith("cogent-post-compact-")){
      markSession(path,input.sessionKey,input.tag.startsWith("cogent-post-compact-")
        ? "Post-compaction continuation" : "Interrupted Direct continuation");
      return {scheduled:true,compatibilityMode:"direct-recovery"};
    }
    const id=key(input.sessionKey,input.tag),timer=setTimeout(()=>{
      timers.delete(id);void executeCompatibilityWake(api,cfg,input).catch(()=>{});
    },Math.max(0,input.delayMs ?? 0));
    timer.unref?.();timers.set(id,timer);
    return {scheduled:true,compatibilityMode:"hidden-worker-host-delivery"};
  };
  return {unscheduleSessionTurnsByTag:unschedule,scheduleSessionTurn:schedule};
}

function rebindPendingAssistantDelivery(path:string,fromSessionKey:string,toSessionKey:string){
  const db=openDb(path);
  try{return Number(db.prepare(`UPDATE cnx_assistant_delivery SET owner_session_key=?,updated_at=?
    WHERE owner_session_key=? AND status='pending'`).run(toSessionKey,now(),fromSessionKey).changes);}
  finally{db.close();}
}

function wrap(){
  const entry=baseEntry as any;
  if(entry[WRAP])return;
  Object.defineProperty(entry,WRAP,{value:true});
  const register=baseEntry.register?.bind(baseEntry);
  baseEntry.register=(api:any)=>{
    patchTicketStore();
    const cfg=(api.pluginConfig ?? {}) as Cfg,reg=api.registerService?.bind(api),proxy=Object.create(api);
    proxy.session={...api.session,workflow:{...api.session?.workflow,...compatWorkflow(api,cfg)}};
    proxy.registerService=(service:any)=>{
      if(!reg)return;
      if(service?.id!=="cogentnexus-ticket-recovery" || typeof service.start!=="function")return reg(service);
      reg({...service,start:async(ctx:any)=>{
        const workspace=resolve(cfg.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const prepared=prepareV085RecoveryState(workspace,cfg);
        api.logger.info?.(`CogentNexus v0.8.5 recovery migration: reopened=${prepared.reopened} superseded=${prepared.superseded} outboxReset=${prepared.outboxReset} workflowDeliveryReset=${prepared.workflowDeliveryReset}`);
        return service.start(ctx);
      }});
    };
    register?.(proxy);
    reg?.(recoveryService(api,cfg));
    api.on?.("session_end",(event:any)=>{
      if(event?.reason!=="new" || !event.sessionKey || !event.nextSessionKey || event.sessionKey===event.nextSessionKey)return;
      const workspace=resolve(cfg.workspaceDir ?? process.cwd());
      rebindPendingAssistantDelivery(dbPath(cfg,workspace),event.sessionKey,event.nextSessionKey);
    },{priority:450,timeoutMs:10000});
  };
}

wrap();
export default baseEntry;
