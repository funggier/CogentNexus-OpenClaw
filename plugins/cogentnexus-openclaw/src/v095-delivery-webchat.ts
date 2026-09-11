import { createHash } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { defaultTicketDatabase } from "./ticket-store.js";
import { acceptTransport, confirmDelivery, prepareDelivery, stageDelivery } from "./v095-delivery-core.js";

export type WebchatDeliveryContext = {
  runId: string;
  sessionKey: string;
  callId?: string;
  channel?: string;
  messageProvider?: string;
  workspaceDir?: string;
};

type WebchatAdapterApi = {
  pluginConfig?: Record<string, unknown>;
  config?: any;
  on?: (...args: any[]) => void;
  logger?: { info?: (message: string) => void; warn?: (message: string) => void };
};

type ExactRunResult = {
  ticket?: { ticket_id?: string; owner_session_key?: string };
  ambiguous: boolean;
};

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function isWebchatSession(sessionKey: string) {
  return /^agent:[^:]+:webchat:channel:[^:]+$/u.test(sessionKey);
}

function databaseFor(api: WebchatAdapterApi, ctx?: WebchatDeliveryContext) {
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  const workspace = resolve(
    text(ctx?.workspaceDir)
      || text(cfg.workspaceDir)
      || text(api.config?.agents?.defaults?.workspace)
      || process.cwd(),
  );
  return resolve(text(cfg.ticketDatabasePath) || defaultTicketDatabase(workspace));
}

function exactRun(db: DatabaseSync, runId: string, sessionKey: string): ExactRunResult {
  if (!runId || !isWebchatSession(sessionKey)) return { ambiguous: false };
  const rows = db.prepare(`SELECT ticket_id,owner_session_key,status FROM tickets
    WHERE run_id=? AND owner_session_key=?
    ORDER BY ticket_id`).all(runId, sessionKey) as Array<{ ticket_id?: string; owner_session_key?: string; status?: string }>;
  if (rows.length !== 1 || !rows[0]?.ticket_id || rows[0].status !== "accepted") {
    return { ticket: undefined, ambiguous: rows.length > 1 };
  }
  return { ticket: rows[0], ambiguous: false };
}

function exactInference(db: DatabaseSync, runId: string, sessionKey: string, callId?: string) {
  if (callId) {
    return db.prepare(`SELECT attempt_id,session_generation FROM cnx_inference_attempt
      WHERE run_id=? AND session_key=? AND call_id=?`).get(runId, sessionKey, callId) as
      { attempt_id?: string; session_generation?: number } | undefined;
  }
  const rows = db.prepare(`SELECT attempt_id,session_generation FROM cnx_inference_attempt
    WHERE run_id=? AND session_key=?`).all(runId, sessionKey) as Array<{ attempt_id?: string; session_generation?: number }>;
  return rows.length === 1 ? rows[0] : undefined;
}

function payloadSha256(payload: string) {
  return createHash("sha256").update(payload).digest("hex");
}

export function webchatDeliveryMarker(idempotencyKey: string) {
  const digest = createHash("sha256").update(idempotencyKey).digest("hex").slice(0, 32);
  return `<!-- cogentnexus-openclaw-delivery:${digest} -->`;
}

function markedText(textValue: string, idempotencyKey: string) {
  const marker = webchatDeliveryMarker(idempotencyKey);
  return textValue.includes(marker) ? textValue : `${textValue.replace(/\s+$/u, "")}\n\n${marker}`;
}

export function stageWebchatDelivery(databasePath: string, context: WebchatDeliveryContext, payload: string) {
  const runId = text(context.runId);
  const sessionKey = text(context.sessionKey);
  const value = text(payload);
  if (!runId || !sessionKey || !isWebchatSession(sessionKey) || !value) {
    return { staged: false as const, reason: "missing-exact-webchat-identity" };
  }

  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  try {
    const exactTicket = exactRun(db, runId, sessionKey);
    if (exactTicket.ambiguous) return { staged: false as const, reason: "ambiguous-run-ticket" };
    const ticket = exactTicket.ticket;
    const inference = exactInference(db, runId, sessionKey, text(context.callId) || undefined);
    if (!ticket || !inference?.attempt_id) {
      return { staged: false as const, reason: context.callId ? "exact-run-or-inference-not-found" : "ambiguous-inference-attempt" };
    }
    const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(sessionKey) as
      { state?: string; generation?: number } | undefined;
    if (!session || session.state !== "active") return { staged: false as const, reason: "stale-webchat-generation" };
    const generation = Number(session.generation);
    if (!Number.isSafeInteger(generation) || generation < 0) return { staged: false as const, reason: "invalid-session-generation" };
    if (generation !== Number(inference.session_generation)) return { staged: false as const, reason: "stale-webchat-generation" };
    const key = {
      ticketId: ticket.ticket_id!,
      inferenceAttemptId: inference.attempt_id!,
      runId,
      ownerSessionKey: sessionKey,
      ownerGeneration: generation,
      surface: "webchat" as const,
      payloadSha256: payloadSha256(value),
      idempotencyKey: `cnx-webchat:${ticket.ticket_id}:g${generation}:${inference.attempt_id}`,
    };
    const prepared = prepareDelivery(db, { ...key, text: value });
    const staged = prepared.state === "prepared"
      ? stageDelivery(db, prepared.idempotencyKey, { evidenceType: "webchat-final-staged" })
      : prepared;
    return { staged: true as const, ...staged, nativeText: markedText(value, staged.idempotencyKey) };
  } finally { db.close(); }
}

export function acceptWebchatTransport(databasePath: string, context: WebchatDeliveryContext) {
  const runId = text(context.runId);
  const sessionKey = text(context.sessionKey);
  if (!runId || !sessionKey || !isWebchatSession(sessionKey)) {
    return { accepted: false as const, reason: "missing-exact-webchat-identity" };
  }
  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  try {
    const rows = db.prepare(`SELECT idempotency_key,owner_generation FROM cnx_assistant_delivery
      WHERE run_id=? AND owner_session_key=? AND surface='webchat' AND status='pending'
      ORDER BY delivery_id`).all(runId, sessionKey) as Array<{ idempotency_key?: string; owner_generation?: number }>;
    if (rows.length !== 1 || !rows[0]?.idempotency_key) return { accepted: false as const, reason: "ambiguous-webchat-receipt" };
    const session = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(sessionKey) as { state?: string; generation?: number } | undefined;
    if (!session || session.state !== "active" || Number(session.generation) !== Number(rows[0].owner_generation)) {
      return { accepted: false as const, reason: "stale-webchat-generation" };
    }
    const accepted = acceptTransport(db, rows[0].idempotency_key, { evidenceType: "webchat-message-sent" });
    return { accepted: true as const, ...accepted };
  } finally { db.close(); }
}

export function confirmWebchatDelivery(databasePath: string, context: WebchatDeliveryContext) {
  const accepted = acceptWebchatTransport(databasePath, context);
  if (!accepted.accepted) return { confirmed: false as const, reason: accepted.reason };
  const db = new DatabaseSync(databasePath);
  try {
    const confirmed = confirmDelivery(db, accepted.idempotencyKey, { evidenceType: "webchat-message-receipt" });
    return { confirmed: true as const, ...confirmed };
  } finally { db.close(); }
}

/** Evidence-only Web Chat adapter. Exact run/session identity is mandatory. */
export function registerWebchatDeliveryAdapter(api: WebchatAdapterApi) {
  if (typeof api?.on !== "function") return;
  api.on("reply_payload_sending", async (event: any, ctx: WebchatDeliveryContext) => {
    if (text(ctx?.channel) !== "webchat" && text(ctx?.messageProvider) !== "webchat") return;
    const databasePath = databaseFor(api, ctx);
    const payload = Array.isArray(event?.payload?.content)
      ? event.payload.content.filter((part: any) => part?.type === "text" && typeof part.text === "string").map((part: any) => part.text).join("\n")
      : text(event?.payload?.text);
    const staged = stageWebchatDelivery(databasePath, {
      ...ctx,
      callId: text(event?.callId) || text(ctx?.callId) || undefined,
    }, payload);
    if (!staged.staged) return;
    return { ...event, payload: { ...(event.payload ?? {}), text: staged.nativeText } };
  }, { registrationId: "cogentnexus-openclaw-v095-webchat-delivery" });

  api.on("message_sent", (event: any, ctx: WebchatDeliveryContext) => {
    if (text(ctx?.channel) !== "webchat" && text(ctx?.messageProvider) !== "webchat") return;
    const runId = text(event?.runId);
    const sessionKey = text(event?.sessionKey ?? ctx?.sessionKey);
    const callId = text(event?.callId) || text(ctx?.callId) || undefined;
    if (!runId || !sessionKey) {
      api.logger?.info?.("CogentNexus-OpenClaw ignored ambiguous Web Chat message_sent receipt without exact run identity");
      return;
    }
    try {
      return confirmWebchatDelivery(databaseFor(api, ctx), {
        runId,
        sessionKey,
        callId,
        channel: "webchat",
        messageProvider: "webchat",
      });
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw Web Chat delivery receipt rejected: ${error instanceof Error ? error.message : String(error)}`);
      return;
    }
  }, { registrationId: "cogentnexus-openclaw-v095-webchat-delivery-receipt" });
}
