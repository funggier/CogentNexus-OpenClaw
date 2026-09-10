import { createHash } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { defaultTicketDatabase } from "./ticket-store.js";
import { acceptTransport, confirmDelivery, prepareDelivery, stageDelivery } from "./v095-delivery-core.js";

export type DiscordDeliveryContext = {
  runId: string;
  sessionKey: string;
  channel?: string;
  messageProvider?: string;
  workspaceDir?: string;
};

type DiscordAdapterApi = {
  pluginConfig?: Record<string, unknown>;
  config?: any;
  on?: (...args: any[]) => void;
  logger?: { info?: (message: string) => void; warn?: (message: string) => void };
};

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function isDiscordSession(sessionKey: string) {
  return /^agent:[^:]+:discord:channel:\d+$/u.test(sessionKey);
}

function databaseFor(api: DiscordAdapterApi, ctx?: DiscordDeliveryContext) {
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  const workspace = resolve(
    text(ctx?.workspaceDir)
      || text(cfg.workspaceDir)
      || text(api.config?.agents?.defaults?.workspace)
      || process.cwd(),
  );
  return resolve(text(cfg.ticketDatabasePath) || defaultTicketDatabase(workspace));
}

function exactRun(db: DatabaseSync, runId: string, sessionKey: string) {
  if (!runId || !isDiscordSession(sessionKey)) return undefined;
  return db.prepare(`SELECT ticket_id,owner_session_key FROM tickets
    WHERE run_id=? AND owner_session_key=? AND status='accepted'
      AND workflow_eligible=0 AND workflow_id IS NULL
    LIMIT 1`).get(runId, sessionKey) as { ticket_id?: string; owner_session_key?: string } | undefined;
}

function exactInference(db: DatabaseSync, runId: string, sessionKey: string) {
  return db.prepare(`SELECT attempt_id,session_generation FROM cnx_inference_attempt
    WHERE run_id=? AND session_key=?
    ORDER BY started_at DESC LIMIT 1`).get(runId, sessionKey) as
    { attempt_id?: string; session_generation?: number } | undefined;
}

function payloadSha256(payload: string) {
  return createHash("sha256").update(payload).digest("hex");
}

export function discordDeliveryMarker(idempotencyKey: string) {
  const digest = createHash("sha256").update(idempotencyKey).digest("hex").slice(0, 32);
  return `<!-- cogentnexus-openclaw-delivery:${digest} -->`;
}

function markedText(textValue: string, idempotencyKey: string) {
  const marker = discordDeliveryMarker(idempotencyKey);
  return textValue.includes(marker) ? textValue : `${textValue.replace(/\s+$/u, "")}\n\n${marker}`;
}

export function stageDiscordDelivery(databasePath: string, context: DiscordDeliveryContext, payload: string) {
  const runId = text(context.runId);
  const sessionKey = text(context.sessionKey);
  const value = text(payload);
  if (!runId || !sessionKey || !isDiscordSession(sessionKey) || !value) return { staged: false as const, reason: "missing-exact-discord-identity" };

  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  try {
    const ticket = exactRun(db, runId, sessionKey);
    const inference = exactInference(db, runId, sessionKey);
    if (!ticket || !inference?.attempt_id) return { staged: false as const, reason: "exact-run-or-inference-not-found" };
    const generation = Number(inference.session_generation);
    if (!Number.isSafeInteger(generation) || generation < 0) return { staged: false as const, reason: "invalid-session-generation" };
    const key = {
      ticketId: ticket.ticket_id!,
      inferenceAttemptId: inference.attempt_id!,
      runId,
      ownerSessionKey: sessionKey,
      ownerGeneration: generation,
      surface: "discord" as const,
      payloadSha256: payloadSha256(value),
      idempotencyKey: `cnx-discord:${ticket.ticket_id}:g${generation}:${inference.attempt_id}`,
    };
    const prepared = prepareDelivery(db, { ...key, text: value });
    const staged = prepared.state === "prepared"
      ? stageDelivery(db, prepared.idempotencyKey, { evidenceType: "discord-final-staged" })
      : prepared;
    return { staged: true as const, ...staged, nativeText: markedText(value, staged.idempotencyKey) };
  } finally { db.close(); }
}

export function acceptDiscordTransport(databasePath: string, context: DiscordDeliveryContext) {
  const runId = text(context.runId);
  const sessionKey = text(context.sessionKey);
  if (!runId || !sessionKey || !isDiscordSession(sessionKey)) return { accepted: false as const, reason: "missing-exact-discord-identity" };
  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  try {
    const row = db.prepare(`SELECT idempotency_key FROM cnx_assistant_delivery
      WHERE run_id=? AND owner_session_key=? AND surface='discord' AND status='pending'
      ORDER BY delivery_id DESC LIMIT 2`).all(runId, sessionKey) as Array<{ idempotency_key?: string }>;
    if (row.length !== 1 || !row[0]?.idempotency_key) return { accepted: false as const, reason: "ambiguous-discord-receipt" };
    const accepted = acceptTransport(db, row[0].idempotency_key, { evidenceType: "discord-message-sent" });
    return { accepted: true as const, ...accepted };
  } finally { db.close(); }
}

export function confirmDiscordDelivery(databasePath: string, context: DiscordDeliveryContext) {
  const accepted = acceptDiscordTransport(databasePath, context);
  if (!accepted.accepted) return { confirmed: false as const, reason: accepted.reason };
  const db = new DatabaseSync(databasePath);
  try {
    const confirmed = confirmDelivery(db, accepted.idempotencyKey, { evidenceType: "discord-message-receipt" });
    return { confirmed: true as const, ...confirmed };
  } finally { db.close(); }
}

/** Evidence-only Discord adapter. A run-less receipt is deliberately ignored. */
export function registerDiscordDeliveryAdapter(api: DiscordAdapterApi) {
  if (typeof api?.on !== "function") return;
  api.on("reply_payload_sending", async (event: any, ctx: DiscordDeliveryContext) => {
    if (text(ctx?.channel) !== "discord" && text(ctx?.messageProvider) !== "discord") return;
    const databasePath = databaseFor(api, ctx);
    const payload = Array.isArray(event?.payload?.content)
      ? event.payload.content.filter((part: any) => part?.type === "text" && typeof part.text === "string").map((part: any) => part.text).join("\n")
      : text(event?.payload?.text);
    const staged = stageDiscordDelivery(databasePath, ctx, payload);
    if (!staged.staged) return;
    return { ...event, payload: { ...(event.payload ?? {}), text: staged.nativeText } };
  }, { registrationId: "cogentnexus-openclaw-v095-discord-delivery" });

  api.on("message_sent", (event: any, ctx: DiscordDeliveryContext) => {
    if (text(ctx?.channel) !== "discord" && text(ctx?.messageProvider) !== "discord") return;
    const runId = text(event?.runId ?? ctx?.runId);
    const sessionKey = text(event?.sessionKey ?? ctx?.sessionKey);
    if (!runId || !sessionKey) {
      api.logger?.info?.("CogentNexus-OpenClaw ignored ambiguous Discord message_sent receipt without exact run identity");
      return;
    }
    try { return confirmDiscordDelivery(databaseFor(api, ctx), { runId, sessionKey, channel: "discord", messageProvider: "discord" }); }
    catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw Discord delivery receipt rejected: ${error instanceof Error ? error.message : String(error)}`);
      return;
    }
  }, { registrationId: "cogentnexus-openclaw-v095-discord-delivery-receipt" });
}
