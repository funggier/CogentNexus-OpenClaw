import { createHash, randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";

export type IntakeTicket = {
  ticketId: string;
  requestKey: string;
  status: "accepted";
  createdAt: string;
  duplicate: boolean;
};

export type TicketLease = {
  ticketId: string;
  workerId: string;
  leaseToken: string;
  leaseGeneration: number;
  leaseExpiresAt: string;
};

export type RecoveryCandidate = {
  ticketId: string;
  previousWorkerId: string | null;
  previousLeaseGeneration: number;
  status: "waiting";
};

export type TicketFailureClass = "transient" | "timeout" | "validation" | "capability" | "authorization" | "interrupted" | "permanent";

export type TicketOutbox = {
  outboxId: number;
  ticketId: string;
  ownerSessionKey: string;
  terminalStatus: "completed" | "failed" | "cancelled";
  payload: unknown;
  deliveryAttempts: number;
  scheduledAt?: string | null;
  deliveryRunId?: string | null;
};

export type TicketRecord = {
  ticketId: string;
  runId: string;
  ownerSessionKey: string;
  prompt: string;
  workflowEligible: boolean;
  workflowId: string | null;
  manifestPath: string | null;
};

export type LinkedTicketLease = TicketLease & { workflowId: string; manifestPath: string };

const SCHEMA = `
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tickets (
  ticket_id TEXT PRIMARY KEY,
  request_key TEXT NOT NULL UNIQUE,
  run_id TEXT NOT NULL,
  owner_session_key TEXT NOT NULL,
  prompt TEXT NOT NULL,
  prompt_sha256 TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('accepted','planned','running','waiting','completed','failed','cancelled')),
  worker_id TEXT,
  lease_token TEXT,
  lease_generation INTEGER NOT NULL DEFAULT 0,
  lease_expires_at TEXT,
  heartbeat_at TEXT,
  attempt_count INTEGER NOT NULL DEFAULT 0,
  max_attempts INTEGER NOT NULL DEFAULT 3,
  failure_class TEXT,
  failure_message TEXT,
  result_json TEXT,
  response_ready_at TEXT,
  delivery_confirmed_at TEXT,
  delivery_last_error TEXT,
  workflow_eligible INTEGER NOT NULL DEFAULT 0,
  workflow_id TEXT,
  manifest_path TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ticket_events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tickets_status_updated ON tickets(status, updated_at);
CREATE INDEX IF NOT EXISTS idx_ticket_events_ticket ON ticket_events(ticket_id, event_id);
CREATE TABLE IF NOT EXISTS ticket_outbox (
  outbox_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_id TEXT NOT NULL UNIQUE REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  owner_session_key TEXT NOT NULL,
  terminal_status TEXT NOT NULL CHECK (terminal_status IN ('completed','failed','cancelled')),
  payload_json TEXT NOT NULL,
  delivery_status TEXT NOT NULL DEFAULT 'pending' CHECK (delivery_status IN ('pending','delivered')),
  delivery_attempts INTEGER NOT NULL DEFAULT 0,
  last_delivery_error TEXT,
  scheduled_at TEXT,
  delivery_run_id TEXT,
  created_at TEXT NOT NULL,
  delivered_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_ticket_outbox_pending ON ticket_outbox(delivery_status, outbox_id);
CREATE TABLE IF NOT EXISTS experiences (
  experience_id TEXT PRIMARY KEY,
  ticket_id TEXT,
  kind TEXT NOT NULL CHECK (kind IN ('attempt','failure','correction','validator_outcome')),
  summary TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  outcome_json TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experiences_ticket_created ON experiences(ticket_id,created_at);
`;

function hash(value: string) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

export function defaultTicketDatabase(workspaceDir: string) {
  return resolve(workspaceDir, ".cogent", "runtime", "cogentnexus.sqlite3");
}

export class TicketStore {
  readonly databasePath: string;

  constructor(databasePath: string) {
    this.databasePath = resolve(databasePath);
  }

  private open() {
    mkdirSync(dirname(this.databasePath), { recursive: true });
    const db = new DatabaseSync(this.databasePath);
    try {
      db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
      db.exec(SCHEMA);
      this.ensureColumn(db,"tickets","worker_id","TEXT");
      this.ensureColumn(db,"tickets","lease_token","TEXT");
      this.ensureColumn(db,"tickets","lease_generation","INTEGER NOT NULL DEFAULT 0");
      this.ensureColumn(db,"tickets","lease_expires_at","TEXT");
      this.ensureColumn(db,"tickets","heartbeat_at","TEXT");
      this.ensureColumn(db,"tickets","attempt_count","INTEGER NOT NULL DEFAULT 0");
      this.ensureColumn(db,"tickets","max_attempts","INTEGER NOT NULL DEFAULT 3");
      this.ensureColumn(db,"tickets","failure_class","TEXT");
      this.ensureColumn(db,"tickets","failure_message","TEXT");
      this.ensureColumn(db,"tickets","result_json","TEXT");
      this.ensureColumn(db,"tickets","response_ready_at","TEXT");
      this.ensureColumn(db,"tickets","delivery_confirmed_at","TEXT");
      this.ensureColumn(db,"tickets","delivery_last_error","TEXT");
      this.ensureColumn(db,"tickets","workflow_eligible","INTEGER NOT NULL DEFAULT 0");
      this.ensureColumn(db,"tickets","workflow_id","TEXT");
      this.ensureColumn(db,"tickets","manifest_path","TEXT");
      this.ensureColumn(db,"ticket_outbox","scheduled_at","TEXT");
      this.ensureColumn(db,"ticket_outbox","delivery_run_id","TEXT");
      db.exec("CREATE INDEX IF NOT EXISTS idx_tickets_recovery ON tickets(status, lease_expires_at)");
      db.exec("CREATE INDEX IF NOT EXISTS idx_tickets_direct_delivery ON tickets(status, workflow_eligible, response_ready_at, delivery_confirmed_at)");
      const applied = new Date().toISOString();
      for (const version of [1,2,3,4,5,6]) db.prepare("INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES (?, ?)").run(version,applied);
      return db;
    } catch (error) {
      db.close();
      throw error;
    }
  }

  route(ticketId: string, workflowEligible: boolean, now = new Date()): boolean {
    const db = this.open();
    const nowIso = now.toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const changed = db.prepare("UPDATE tickets SET workflow_eligible=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(workflowEligible ? 1 : 0,nowIso,ticketId);
      if (changed.changes === 1) this.event(db,ticketId,"routed",{workflowEligible},nowIso);
      db.exec("COMMIT");
      return changed.changes === 1;
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  finalizeDirectRun(input:{runId:string;success:boolean;interrupted:boolean;message?:string;expectsDelivery?:boolean;now?:Date}): "completed"|"awaiting_delivery"|"waiting"|"failed"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      if (input.success) {
        const expectsDelivery=input.expectsDelivery !== false;
        const payload={runId:input.runId,direct:true,expectsDelivery};
        if (!expectsDelivery) {
          db.prepare("UPDATE tickets SET status='completed',result_json=?,response_ready_at=?,delivery_confirmed_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
            .run(JSON.stringify(payload),nowIso,nowIso,nowIso,nowIso,row.ticket_id);
          this.event(db,row.ticket_id,"response_ready",payload,nowIso);
          this.event(db,row.ticket_id,"delivery_confirmed",{runId:input.runId,required:false},nowIso);
          this.event(db,row.ticket_id,"completed",payload,nowIso);
          db.exec("COMMIT"); return "completed";
        }
        db.prepare("UPDATE tickets SET result_json=?,response_ready_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
          .run(JSON.stringify(payload),nowIso,nowIso,row.ticket_id);
        this.event(db,row.ticket_id,"response_ready",payload,nowIso);
        db.exec("COMMIT"); return "awaiting_delivery";
      }
      const status=input.interrupted?"waiting":"failed";
      const classification=input.interrupted?"interrupted":"permanent";
      const message=(input.message??(input.interrupted?"direct run interrupted":"direct run failed")).slice(0,2000);
      db.prepare("UPDATE tickets SET status=?,workflow_eligible=?,failure_class=?,failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(status,input.interrupted?1:0,classification,message,message,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,input.interrupted?"promoted_to_durable":"failed",{runId:input.runId,classification,message},nowIso);
      if (!input.interrupted) this.enqueueTerminal(db,row.ticket_id,"failed",{classification,message},nowIso);
      db.exec("COMMIT"); return status;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  confirmDirectDelivery(input:{runId:string;now?:Date}): "completed"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      db.prepare("UPDATE tickets SET status='completed',delivery_confirmed_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(nowIso,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,"delivery_confirmed",{runId:input.runId},nowIso);
      this.event(db,row.ticket_id,"completed",{runId:input.runId,direct:true,deliveryConfirmed:true},nowIso);
      db.exec("COMMIT"); return "completed";
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  failDirectDelivery(input:{runId:string;message?:string;now?:Date}): "waiting"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    const message=(input.message??"direct reply delivery failed").slice(0,2000);
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(message,message,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,"direct_delivery_failed",{runId:input.runId,message},nowIso);
      db.exec("COMMIT"); return "waiting";
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  pendingDirectRunForSession(sessionKey:string): string|undefined {
    const db=this.open();
    try {
      const row=db.prepare("SELECT run_id FROM tickets WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL ORDER BY response_ready_at DESC LIMIT 1").get(sessionKey) as any;
      return row?.run_id;
    } finally { db.close(); }
  }

  recoverUndeliveredDirect(input:{now?:Date;olderThanMs?:number;limit?:number}={}): Array<{ticketId:string;runId:string}> {
    const db=this.open();
    const now=input.now??new Date();
    const cutoff=new Date(now.getTime()-Math.max(1000,input.olderThanMs??120000)).toISOString();
    const nowIso=now.toISOString();
    const limit=Math.max(1,Math.min(input.limit??100,1000));
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows=db.prepare("SELECT ticket_id,run_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL AND response_ready_at<=? ORDER BY response_ready_at,ticket_id LIMIT ?").all(cutoff,limit) as any[];
      const recovered:Array<{ticketId:string;runId:string}>=[];
      for (const row of rows) {
        const message="direct response was ready but final delivery was not confirmed before the receipt deadline";
        const changed=db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted' AND delivery_confirmed_at IS NULL")
          .run(message,message,nowIso,row.ticket_id);
        if (changed.changes!==1) continue;
        this.event(db,row.ticket_id,"direct_delivery_timeout",{runId:row.run_id,cutoff},nowIso);
        recovered.push({ticketId:row.ticket_id,runId:row.run_id});
      }
      db.exec("COMMIT"); return recovered;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  hasNonTerminalForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM tickets WHERE owner_session_key=? AND status NOT IN ('completed','failed','cancelled') LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }

  hasPendingOutboxForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM ticket_outbox WHERE owner_session_key=? AND delivery_status='pending' LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }

  get(ticketId: string): TicketRecord | undefined {
    const db = this.open();
    try {
      const row = db.prepare(`SELECT ticket_id,run_id,owner_session_key,prompt,workflow_eligible,workflow_id,manifest_path
        FROM tickets WHERE ticket_id=?`).get(ticketId) as any;
      return row ? {ticketId:row.ticket_id,runId:row.run_id,ownerSessionKey:row.owner_session_key,prompt:row.prompt,
        workflowEligible:Boolean(row.workflow_eligible),workflowId:row.workflow_id,manifestPath:row.manifest_path} : undefined;
    } finally { db.close(); }
  }

  linkWorkflow(input: TicketLease & { workflowId: string; manifestPath: string; now?: Date }): boolean {
    const db = this.open();
    const nowIso = (input.now ?? new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const changed = db.prepare(`UPDATE tickets SET workflow_id=?,manifest_path=?,updated_at=? WHERE ticket_id=? AND status='running'
        AND worker_id=? AND lease_token=? AND lease_generation=? AND lease_expires_at>=?
        AND (workflow_id IS NULL OR workflow_id=?)`).run(input.workflowId,input.manifestPath,nowIso,input.ticketId,input.workerId,
          input.leaseToken,input.leaseGeneration,nowIso,input.workflowId);
      if (changed.changes !== 1) throw new Error("stale lease or conflicting workflow link");
      this.event(db,input.ticketId,"workflow_linked",{workflowId:input.workflowId,manifestPath:input.manifestPath,leaseGeneration:input.leaseGeneration},nowIso);
      db.exec("COMMIT");
      return true;
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  linkedRunning(): LinkedTicketLease[] {
    const db = this.open();
    try {
      return (db.prepare(`SELECT ticket_id,worker_id,lease_token,lease_generation,lease_expires_at,workflow_id,manifest_path
        FROM tickets WHERE status='running' AND workflow_id IS NOT NULL AND manifest_path IS NOT NULL`).all() as any[])
        .map((row) => ({ticketId:row.ticket_id,workerId:row.worker_id,leaseToken:row.lease_token,
          leaseGeneration:Number(row.lease_generation),leaseExpiresAt:row.lease_expires_at,
          workflowId:row.workflow_id,manifestPath:row.manifest_path}));
    } finally { db.close(); }
  }

  private ensureColumn(db: DatabaseSync, table: string, column: string, declaration: string) {
    const columns = db.prepare(`PRAGMA table_info(${table})`).all() as Array<{name:string}>;
    if (!columns.some((item) => item.name === column)) db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${declaration}`);
  }

  accept(input: { runId: string; ownerSessionKey: string; prompt: string; maxAttempts?: number }): IntakeTicket {
    const db = this.open();
    const now = new Date().toISOString();
    const requestKey = hash(`${input.ownerSessionKey}\0${input.runId}`);
    const ticketId = `CNXT-${randomUUID()}`;
    try {
      db.exec("BEGIN IMMEDIATE");
      const existing = db.prepare("SELECT ticket_id, status, created_at FROM tickets WHERE request_key = ?").get(requestKey) as
        | { ticket_id: string; status: string; created_at: string }
        | undefined;
      if (existing) {
        db.exec("COMMIT");
        return { ticketId: existing.ticket_id, requestKey, status: "accepted", createdAt: existing.created_at, duplicate: true };
      }
      const maxAttempts = Math.max(1,Math.min(input.maxAttempts ?? 3,20));
      db.prepare(`INSERT INTO tickets(ticket_id,request_key,run_id,owner_session_key,prompt,prompt_sha256,status,max_attempts,created_at,updated_at)
                  VALUES (?,?,?,?,?,?,'accepted',?,?,?)`)
        .run(ticketId, requestKey, input.runId, input.ownerSessionKey, input.prompt, hash(input.prompt), maxAttempts, now, now);
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,'accepted',?,?)")
        .run(ticketId, JSON.stringify({ runId: input.runId, promptSha256: hash(input.prompt) }), now);
      db.exec("COMMIT");
      return { ticketId, requestKey, status: "accepted", createdAt: now, duplicate: false };
    } catch (error) {
      try { db.exec("ROLLBACK"); } catch { /* transaction may not have started */ }
      throw error;
    } finally {
      db.close();
    }
  }

  claim(input: { ticketId: string; workerId: string; leaseMs: number; now?: Date }): TicketLease | undefined {
    if (!input.workerId || input.leaseMs < 1000) throw new Error("claim requires workerId and leaseMs >= 1000");
    const db = this.open();
    const now = input.now ?? new Date();
    const nowIso = now.toISOString();
    const expires = new Date(now.getTime() + input.leaseMs).toISOString();
    const token = randomUUID();
    try {
      db.exec("BEGIN IMMEDIATE");
      const row = db.prepare("SELECT status,lease_expires_at,lease_generation FROM tickets WHERE ticket_id=?").get(input.ticketId) as any;
      if (!row || !["accepted","waiting"].includes(row.status)) { db.exec("COMMIT"); return undefined; }
      const generation = Number(row.lease_generation) + 1;
      db.prepare(`UPDATE tickets SET status='running',worker_id=?,lease_token=?,lease_generation=?,lease_expires_at=?,heartbeat_at=?,attempt_count=attempt_count+1,updated_at=? WHERE ticket_id=?`)
        .run(input.workerId, token, generation, expires, nowIso, nowIso, input.ticketId);
      this.event(db, input.ticketId, "claimed", {workerId:input.workerId,leaseGeneration:generation,leaseExpiresAt:expires}, nowIso);
      this.experience(db,input.ticketId,"attempt",`Ticket claimed by ${input.workerId} generation ${generation}`,`ticket:${input.ticketId}/lease:${generation}`,{leaseExpiresAt:expires},nowIso);
      db.exec("COMMIT");
      return {ticketId:input.ticketId,workerId:input.workerId,leaseToken:token,leaseGeneration:generation,leaseExpiresAt:expires};
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  heartbeat(input: TicketLease & { leaseMs: number; now?: Date }): TicketLease {
    const db = this.open();
    const now = input.now ?? new Date();
    const nowIso = now.toISOString();
    const expires = new Date(now.getTime() + input.leaseMs).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const changed = db.prepare(`UPDATE tickets SET heartbeat_at=?,lease_expires_at=?,updated_at=?
        WHERE ticket_id=? AND status='running' AND worker_id=? AND lease_token=? AND lease_generation=? AND lease_expires_at>=?`)
        .run(nowIso, expires, nowIso, input.ticketId, input.workerId, input.leaseToken, input.leaseGeneration, nowIso);
      if (changed.changes !== 1) throw new Error("stale or expired ticket lease");
      db.exec("COMMIT");
      return {...input,leaseExpiresAt:expires};
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  complete(input: TicketLease & { result: unknown; now?: Date }): void {
    const db = this.open();
    const nowIso = (input.now ?? new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const changed = db.prepare(`UPDATE tickets SET status='completed',result_json=?,lease_expires_at=NULL,heartbeat_at=?,updated_at=?
        WHERE ticket_id=? AND status='running' AND worker_id=? AND lease_token=? AND lease_generation=? AND lease_expires_at>=?`)
        .run(JSON.stringify(input.result), nowIso, nowIso, input.ticketId, input.workerId, input.leaseToken, input.leaseGeneration, nowIso);
      if (changed.changes !== 1) throw new Error("stale or expired ticket lease");
      this.event(db, input.ticketId, "completed", {workerId:input.workerId,leaseGeneration:input.leaseGeneration}, nowIso);
      this.experience(db,input.ticketId,"validator_outcome","Ticket workflow reached verified completion",`ticket:${input.ticketId}/event:completed`,input.result,nowIso);
      this.enqueueTerminal(db,input.ticketId,"completed",input.result,nowIso);
      db.exec("COMMIT");
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  failAttempt(input: TicketLease & { classification: TicketFailureClass; message: string; now?: Date }): "waiting" | "failed" {
    const db = this.open();
    const nowIso = (input.now ?? new Date()).toISOString();
    const retryable = ["transient","timeout","validation","capability"].includes(input.classification);
    try {
      db.exec("BEGIN IMMEDIATE");
      const row = db.prepare(`SELECT attempt_count,max_attempts FROM tickets WHERE ticket_id=? AND status='running' AND worker_id=?
        AND lease_token=? AND lease_generation=? AND lease_expires_at>=?`).get(input.ticketId,input.workerId,input.leaseToken,input.leaseGeneration,nowIso) as any;
      if (!row) throw new Error("stale ticket lease");
      const nextStatus = retryable && Number(row.attempt_count) < Number(row.max_attempts) ? "waiting" : "failed";
      const changed = db.prepare(`UPDATE tickets SET status=?,failure_class=?,failure_message=?,worker_id=NULL,lease_token=NULL,
        lease_expires_at=NULL,heartbeat_at=NULL,updated_at=? WHERE ticket_id=? AND status='running' AND lease_token=? AND lease_generation=?`)
        .run(nextStatus,input.classification,input.message.slice(0,2000),nowIso,input.ticketId,input.leaseToken,input.leaseGeneration);
      if (changed.changes !== 1) throw new Error("stale ticket lease");
      this.event(db,input.ticketId,nextStatus === "waiting" ? "retry_scheduled" : "failed",{
        workerId:input.workerId,leaseGeneration:input.leaseGeneration,classification:input.classification,
        attemptCount:Number(row.attempt_count),maxAttempts:Number(row.max_attempts),message:input.message.slice(0,2000),
      },nowIso);
      this.experience(db,input.ticketId,"failure",`Ticket attempt failed: ${input.classification}`,`ticket:${input.ticketId}/lease:${input.leaseGeneration}`,{message:input.message.slice(0,2000),nextStatus},nowIso);
      if (nextStatus === "failed") this.enqueueTerminal(db,input.ticketId,"failed",{classification:input.classification,message:input.message.slice(0,2000)},nowIso);
      db.exec("COMMIT");
      return nextStatus;
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  ready(limit = 1): Array<{ticketId:string;attemptCount:number;maxAttempts:number}> {
    const db = this.open();
    try {
      return (db.prepare(`SELECT ticket_id,attempt_count,max_attempts FROM tickets WHERE status IN ('accepted','waiting') AND workflow_eligible=1
        ORDER BY created_at,ticket_id LIMIT ?`).all(Math.max(1,Math.min(limit,100))) as any[])
        .map((row) => ({ticketId:row.ticket_id,attemptCount:Number(row.attempt_count),maxAttempts:Number(row.max_attempts)}));
    } finally { db.close(); }
  }

  pendingOutbox(limit = 100, now = new Date(), retryAfterMs = 300_000): TicketOutbox[] {
    const db = this.open();
    const cutoff = new Date(now.getTime() - Math.max(1_000, retryAfterMs)).toISOString();
    try {
      return (db.prepare(`SELECT outbox_id,ticket_id,owner_session_key,terminal_status,payload_json,delivery_attempts,scheduled_at,delivery_run_id
        FROM ticket_outbox WHERE delivery_status='pending' AND (scheduled_at IS NULL OR scheduled_at<=?) ORDER BY outbox_id LIMIT ?`).all(cutoff,Math.max(1,Math.min(limit,1000))) as any[])
        .map((row) => ({outboxId:Number(row.outbox_id),ticketId:row.ticket_id,ownerSessionKey:row.owner_session_key,
          terminalStatus:row.terminal_status,payload:JSON.parse(row.payload_json),deliveryAttempts:Number(row.delivery_attempts),scheduledAt:row.scheduled_at,deliveryRunId:row.delivery_run_id}));
    } finally { db.close(); }
  }

  markOutboxScheduled(outboxId:number, runId?:string, now=new Date()): boolean {
    const db=this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET delivery_attempts=delivery_attempts+1,scheduled_at=?,delivery_run_id=?,last_delivery_error=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(now.toISOString(),runId??null,outboxId).changes===1;
    } finally { db.close(); }
  }

  bindOutboxRun(outboxId:number, runId:string): boolean {
    const db=this.open();
    try {
      return db.prepare("UPDATE ticket_outbox SET delivery_run_id=?,last_delivery_error=NULL WHERE outbox_id=? AND delivery_status='pending'")
        .run(runId,outboxId).changes===1;
    } finally { db.close(); }
  }

  markOutboxDelivered(outboxId: number, now = new Date()): boolean {
    const db = this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET delivery_status='delivered',delivered_at=?,last_delivery_error=NULL,scheduled_at=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(now.toISOString(),outboxId).changes === 1;
    } finally { db.close(); }
  }

  markOutboxFailed(outboxId: number, message: string): boolean {
    const db = this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET last_delivery_error=?,scheduled_at=NULL,delivery_run_id=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(message.slice(0,2000),outboxId).changes === 1;
    } finally { db.close(); }
  }

  snapshot(now = new Date()) {
    const db = this.open();
    try {
      const counts = db.prepare("SELECT status,count(*) AS count FROM tickets GROUP BY status").all() as any[];
      const expired = db.prepare("SELECT count(*) AS count FROM tickets WHERE status='running' AND lease_expires_at<?").get(now.toISOString()) as any;
      const pending = db.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE delivery_status='pending'").get() as any;
      return {capturedAt:now.toISOString(),tickets:Object.fromEntries(counts.map(x=>[x.status,Number(x.count)])),
        expiredRunning:Number(expired.count),pendingOutbox:Number(pending.count)};
    } finally { db.close(); }
  }

  recoverExpired(input: { now?: Date; limit?: number } = {}): RecoveryCandidate[] {
    const db = this.open();
    const nowIso = (input.now ?? new Date()).toISOString();
    const limit = Math.max(1, Math.min(input.limit ?? 100, 1000));
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows = db.prepare(`SELECT ticket_id,worker_id,lease_generation FROM tickets
        WHERE status='running' AND lease_expires_at<? ORDER BY lease_expires_at,ticket_id LIMIT ?`).all(nowIso, limit) as any[];
      const recovered: RecoveryCandidate[] = [];
      for (const row of rows) {
        const changed = db.prepare(`UPDATE tickets SET status='waiting',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,updated_at=?
          WHERE ticket_id=? AND status='running' AND lease_generation=?`).run(nowIso,row.ticket_id,row.lease_generation);
        if (changed.changes !== 1) continue;
        this.event(db,row.ticket_id,"lease_expired",{previousWorkerId:row.worker_id,previousLeaseGeneration:row.lease_generation},nowIso);
        this.experience(db,row.ticket_id,"correction","Expired worker lease reclaimed for deterministic recovery",`ticket:${row.ticket_id}/lease:${row.lease_generation}`,{previousWorkerId:row.worker_id},nowIso);
        recovered.push({ticketId:row.ticket_id,previousWorkerId:row.worker_id,previousLeaseGeneration:row.lease_generation,status:"waiting"});
      }
      db.exec("COMMIT");
      return recovered;
    } catch (error) { try { db.exec("ROLLBACK"); } catch {} throw error; }
    finally { db.close(); }
  }

  private event(db: DatabaseSync, ticketId: string, type: string, payload: unknown, now: string) {
    db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
      .run(ticketId,type,JSON.stringify(payload),now);
  }

  private experience(db: DatabaseSync, ticketId: string, kind: "attempt"|"failure"|"correction"|"validator_outcome", summary: string, evidenceRef: string, outcome: unknown, now: string) {
    db.prepare("INSERT INTO experiences(experience_id,ticket_id,kind,summary,evidence_ref,outcome_json,created_at) VALUES (?,?,?,?,?,?,?)")
      .run(`CNXE-${randomUUID()}`,ticketId,kind,summary,evidenceRef,JSON.stringify(outcome),now);
  }

  private enqueueTerminal(db: DatabaseSync, ticketId: string, status: "completed"|"failed"|"cancelled", payload: unknown, now: string) {
    db.prepare(`INSERT OR IGNORE INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,created_at)
      SELECT ticket_id,owner_session_key,?,?,? FROM tickets WHERE ticket_id=?`).run(status,JSON.stringify(payload),now,ticketId);
  }
}

export function ticketIntakeEligible(prompt: string) {
  return !/\[(?:CogentNexus|Subagent) Context\]|\[CogentNexus (?:Delivery|Continuation):|cogent-workflow-result-|cogent-resume-|The previous run was interrupted\./iu.test(prompt);
}
