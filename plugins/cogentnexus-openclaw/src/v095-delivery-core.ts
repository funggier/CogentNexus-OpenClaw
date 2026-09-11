import { createHash } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

export type DeliveryState =
  | "prepared"
  | "staged"
  | "transport_accepted"
  | "confirmed"
  | "failed"
  | "cancelled";

export type DeliverySurface = "webchat" | "discord";

export type DeliveryAttempt = {
  deliveryId: number;
  ticketId: string;
  inferenceAttemptId: string | null;
  runId: string | null;
  ownerSessionKey: string;
  ownerGeneration: number;
  surface: DeliverySurface;
  payloadSha256: string;
  idempotencyKey: string;
  state: DeliveryState;
  text: string;
  evidenceType: string | null;
  attemptCount: number;
  createdAt: string;
  updatedAt: string;
  deliveredAt: string | null;
};

export type ExactDeliveryKey = {
  ticketId: string;
  inferenceAttemptId?: string | null;
  runId?: string | null;
  ownerSessionKey: string;
  ownerGeneration: number;
  surface: DeliverySurface;
  payloadSha256: string;
  idempotencyKey: string;
};

export type PrepareDeliveryInput = ExactDeliveryKey & {
  text: string;
  now?: Date;
};

export type DeliveryEvidence = {
  evidenceType: string;
  details?: Record<string, unknown>;
  now?: Date;
};

function ensureSchema(db: DatabaseSync) {
  const columns = new Set(
    (db.prepare("PRAGMA table_info(cnx_assistant_delivery)").all() as Array<{ name?: string }>).map((row) => row.name),
  );
  const additions: Array<[string, string]> = [
    ["inference_attempt_id", "TEXT"],
    ["run_id", "TEXT"],
    ["surface", "TEXT"],
    ["payload_sha256", "TEXT"],
    ["delivery_state", "TEXT"],
    ["evidence_type", "TEXT"],
  ];
  for (const [name, type] of additions) {
    if (!columns.has(name)) db.exec(`ALTER TABLE cnx_assistant_delivery ADD COLUMN ${name} ${type}`);
  }
  db.exec("CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_exact_run ON cnx_assistant_delivery(run_id,owner_session_key,owner_generation,idempotency_key)");
  db.exec("CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_inference ON cnx_assistant_delivery(inference_attempt_id,owner_session_key,owner_generation,idempotency_key)");
}

function open(databasePath: string) {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  ensureSchema(db);
  return db;
}

function ensureReady(db: DatabaseSync) {
  ensureSchema(db);
}

function stateFromRow(row: any): DeliveryState {
  if (row.delivery_state === "prepared" || row.delivery_state === "staged" || row.delivery_state === "transport_accepted" || row.delivery_state === "confirmed" || row.delivery_state === "failed" || row.delivery_state === "cancelled") {
    return row.delivery_state;
  }
  return row.status === "delivered" ? "confirmed" : "prepared";
}

function rowToAttempt(row: any): DeliveryAttempt {
  if (!row) throw new Error("delivery attempt not found");
  return {
    deliveryId: Number(row.delivery_id),
    ticketId: String(row.ticket_id),
    inferenceAttemptId: row.inference_attempt_id == null ? null : String(row.inference_attempt_id),
    runId: row.run_id == null ? null : String(row.run_id),
    ownerSessionKey: String(row.owner_session_key),
    ownerGeneration: Number(row.owner_generation),
    surface: row.surface === "discord" ? "discord" : "webchat",
    payloadSha256: String(row.payload_sha256 ?? createHash("sha256").update(String(row.text ?? "")).digest("hex")),
    idempotencyKey: String(row.idempotency_key),
    state: stateFromRow(row),
    text: String(row.text),
    evidenceType: row.evidence_type == null ? null : String(row.evidence_type),
    attemptCount: Number(row.attempt_count ?? 0),
    createdAt: String(row.created_at),
    updatedAt: String(row.updated_at),
    deliveredAt: row.delivered_at == null ? null : String(row.delivered_at),
  };
}

function selectByIdempotency(db: DatabaseSync, idempotencyKey: string) {
  ensureReady(db);
  return db.prepare(`SELECT delivery_id,ticket_id,inference_attempt_id,run_id,owner_session_key,owner_generation,
      surface,payload_sha256,delivery_state,idempotency_key,text,status,evidence_type,attempt_count,created_at,updated_at,delivered_at
    FROM cnx_assistant_delivery WHERE idempotency_key=?`).get(idempotencyKey);
}

function assertCurrentOwner(db: DatabaseSync, attempt: DeliveryAttempt) {
  const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(attempt.ownerSessionKey) as { state?: string; generation?: number } | undefined;
  if (!session || session.state !== "active") throw new Error("delivery owner session is not active");
  if (Number(session.generation) !== attempt.ownerGeneration) throw new Error("delivery owner generation is stale");
}

export function findExactDelivery(db: DatabaseSync, key: ExactDeliveryKey): DeliveryAttempt | null {
  ensureReady(db);
  const row = db.prepare(`SELECT delivery_id,ticket_id,inference_attempt_id,run_id,owner_session_key,owner_generation,
      surface,payload_sha256,delivery_state,idempotency_key,text,status,evidence_type,attempt_count,created_at,updated_at,delivered_at
    FROM cnx_assistant_delivery
    WHERE ticket_id=? AND COALESCE(inference_attempt_id,'')=COALESCE(?, '')
      AND COALESCE(run_id,'')=COALESCE(?, '')
      AND owner_session_key=? AND owner_generation=? AND surface=?
      AND payload_sha256=? AND idempotency_key=?`).get(
    key.ticketId,
    key.inferenceAttemptId ?? null,
    key.runId ?? null,
    key.ownerSessionKey,
    key.ownerGeneration,
    key.surface,
    key.payloadSha256,
    key.idempotencyKey,
  );
  return row ? rowToAttempt(row) : null;
}

function assertIdentity(existing: DeliveryAttempt, input: ExactDeliveryKey & { text?: string }) {
  if (existing.ticketId !== input.ticketId
    || existing.inferenceAttemptId !== (input.inferenceAttemptId ?? null)
    || existing.runId !== (input.runId ?? null)
    || existing.ownerSessionKey !== input.ownerSessionKey
    || existing.ownerGeneration !== input.ownerGeneration
    || existing.surface !== input.surface
    || existing.payloadSha256 !== input.payloadSha256
    || (input.text !== undefined && existing.text !== input.text)) {
    throw new Error("delivery idempotency key is already bound to different exact identity");
  }
}

function transition(db: DatabaseSync, idempotencyKey: string, from: DeliveryState, to: DeliveryState, evidence: DeliveryEvidence, stamp: string) {
  ensureReady(db);
  const current = selectByIdempotency(db, idempotencyKey);
  const state = current ? stateFromRow(current) : null;
  if (!current) return null;
  if (state === to) return rowToAttempt(current);
  if (state !== from) throw new Error(`illegal delivery transition ${state} -> ${to}`);
  const details = evidence.details == null ? undefined : JSON.stringify(evidence.details);
  const result = db.prepare(`UPDATE cnx_assistant_delivery
    SET delivery_state=?,evidence_type=?,attempt_count=attempt_count+1,updated_at=?
    WHERE idempotency_key=? AND COALESCE(delivery_state,CASE WHEN status='delivered' THEN 'confirmed' ELSE 'prepared' END)=?`).run(
    to,
    evidence.evidenceType,
    stamp,
    idempotencyKey,
    from,
  );
  if (result.changes !== 1) throw new Error("delivery transition lost race");
  if (details) db.prepare("UPDATE cnx_assistant_delivery SET target_json=? WHERE idempotency_key=?").run(details, idempotencyKey);
  return rowToAttempt(selectByIdempotency(db, idempotencyKey));
}

export function prepareDelivery(db: DatabaseSync, input: PrepareDeliveryInput): DeliveryAttempt {
  ensureReady(db);
  const text = input.text.trim();
  if (!text) throw new Error("delivery text is required");
  if (!input.ticketId || !input.ownerSessionKey || !input.idempotencyKey || !input.payloadSha256) throw new Error("exact delivery identity is incomplete");
  if (!Number.isSafeInteger(input.ownerGeneration) || input.ownerGeneration < 0) throw new Error("ownerGeneration must be a non-negative safe integer");
  const expectedPayloadSha256 = createHash("sha256").update(text).digest("hex");
  if (input.payloadSha256 !== expectedPayloadSha256) throw new Error("payloadSha256 does not match delivery text");
  const stamp = (input.now ?? new Date()).toISOString();
  const existing = findExactDelivery(db, input);
  if (existing) {
    assertIdentity(existing, input);
    return existing;
  }
  const conflicting = selectByIdempotency(db, input.idempotencyKey);
  if (conflicting) {
    assertIdentity(rowToAttempt(conflicting), input);
    return rowToAttempt(conflicting);
  }

  db.exec("BEGIN IMMEDIATE");
  try {
    ensureReady(db);
    const ticket = db.prepare("SELECT owner_session_key,status FROM tickets WHERE ticket_id=?").get(input.ticketId) as { owner_session_key?: string; status?: string } | undefined;
    if (!ticket) throw new Error("delivery Ticket not found");
    if (ticket.owner_session_key !== input.ownerSessionKey) throw new Error("delivery owner session mismatch");
    if (ticket.status !== "accepted") throw new Error("delivery Ticket is not accepted");
    const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(input.ownerSessionKey) as { state?: string; generation?: number } | undefined;
    if (!session || session.state !== "active") throw new Error("delivery owner session is not active");
    if (Number(session.generation) !== input.ownerGeneration) throw new Error("delivery owner generation is stale");
    const created = db.prepare(`INSERT INTO cnx_assistant_delivery(
      ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
      attempt_count,last_error,created_at,updated_at,delivered_at,
      inference_attempt_id,run_id,surface,payload_sha256,delivery_state,evidence_type
    ) VALUES (?,?,?,?,?,NULL,?,'pending',0,NULL,?,?,NULL,?,?,?,?,?,NULL)`).run(
      input.ticketId,
      input.ownerSessionKey,
      input.ownerGeneration,
      "direct_result",
      text,
      input.idempotencyKey,
      stamp,
      stamp,
      input.inferenceAttemptId ?? null,
      input.runId ?? null,
      input.surface,
      input.payloadSha256,
      "prepared",
    );
    if (created.changes !== 1) throw new Error("delivery preparation insert failed");
    const row = selectByIdempotency(db, input.idempotencyKey);
    db.exec("COMMIT");
    return rowToAttempt(row);
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}

export function stageDelivery(db: DatabaseSync, attemptId: string, evidence: DeliveryEvidence): DeliveryAttempt {
  ensureReady(db);
  if (!attemptId) throw new Error("delivery idempotencyKey is required");
  db.exec("BEGIN IMMEDIATE");
  try {
    const row = selectByIdempotency(db, attemptId);
    if (!row) throw new Error("delivery attempt not found");
    const current = rowToAttempt(row);
    if (current.state === "staged") {
      assertCurrentOwner(db, current);
      db.exec("COMMIT");
      return current;
    }
    assertCurrentOwner(db, current);
    const result = transition(db, attemptId, "prepared", "staged", evidence, (evidence.now ?? new Date()).toISOString())!;
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}

export function acceptTransport(db: DatabaseSync, attemptId: string, evidence: DeliveryEvidence): DeliveryAttempt {
  ensureReady(db);
  if (!attemptId) throw new Error("delivery idempotencyKey is required");
  db.exec("BEGIN IMMEDIATE");
  try {
    const row = selectByIdempotency(db, attemptId);
    if (!row) throw new Error("delivery attempt not found");
    const current = rowToAttempt(row);
    if (current.state === "transport_accepted") {
      db.exec("COMMIT");
      return current;
    }
    assertCurrentOwner(db, current);
    const result = transition(db, attemptId, "staged", "transport_accepted", evidence, (evidence.now ?? new Date()).toISOString())!;
    db.exec("COMMIT");
    return result;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}

export function confirmDelivery(db: DatabaseSync, attemptId: string, evidence: DeliveryEvidence): DeliveryAttempt {
  ensureReady(db);
  if (!attemptId) throw new Error("delivery idempotencyKey is required");
  const stamp = (evidence.now ?? new Date()).toISOString();
  db.exec("BEGIN IMMEDIATE");
  try {
    const current = selectByIdempotency(db, attemptId);
    if (!current) throw new Error("delivery attempt not found");
    const state = stateFromRow(current);
    if (state === "confirmed") {
      db.exec("COMMIT");
      return rowToAttempt(current);
    }
    if (state !== "transport_accepted") throw new Error(`illegal delivery transition ${state} -> confirmed`);
    const delivery = rowToAttempt(current);
    assertCurrentOwner(db, delivery);
    const changed = db.prepare(`UPDATE cnx_assistant_delivery
      SET delivery_state='confirmed',status='delivered',evidence_type=?,attempt_count=attempt_count+1,delivered_at=?,updated_at=?
      WHERE idempotency_key=? AND COALESCE(delivery_state,CASE WHEN status='delivered' THEN 'confirmed' ELSE 'prepared' END)='transport_accepted'`).run(
      evidence.evidenceType,
      stamp,
      stamp,
      attemptId,
    );
    if (changed.changes !== 1) throw new Error("delivery confirmation lost race");
    const updatedDelivery = rowToAttempt(selectByIdempotency(db, attemptId));
    const updated = db.prepare(`UPDATE tickets SET status='completed',delivery_confirmed_at=?,delivery_last_error=NULL,
      failure_class=NULL,failure_message=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`).run(stamp, stamp, updatedDelivery.ticketId);
    if (updated.changes === 1) {
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
        .run(updatedDelivery.ticketId, "delivery_confirmed", JSON.stringify({ runId: updatedDelivery.runId, source: `${updatedDelivery.surface}-delivery-core`, idempotencyKey: updatedDelivery.idempotencyKey }), stamp);
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
        .run(updatedDelivery.ticketId, "completed", JSON.stringify({ runId: updatedDelivery.runId, direct: true, deliveryConfirmed: true, durablePayload: true, deliveryMode: `${updatedDelivery.surface}-delivery-core` }), stamp);
    }
    db.exec("COMMIT");
    return updatedDelivery;
  } catch (error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  }
}
