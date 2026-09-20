import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { isControlCommandMessage } from "openclaw/plugin-sdk/command-detection";
import { classifyDurableRequest } from "./admission.js";
import {
  defaultTicketDatabase,
  TicketStore,
  ticketIntakeEligible,
  type IntakeTicket,
} from "./ticket-store.js";

export type TicketAdmissionConfig = {
  ticketFirst?: boolean;
  providerMode?: "managed" | "passthrough";
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketMaximumAttempts?: number;
  admissionMinimumScore?: number;
};

export type SharedTicketAdmissionInput = {
  sessionKey?: string;
  runId?: string;
  prompt?: string;
  trusted: boolean;
  identityConflict?: boolean;
  workspaceDir?: string;
  config: TicketAdmissionConfig;
};

export type SharedTicketAdmissionResult =
  | {
      state: "skipped";
      reason: "disabled" | "excluded";
    }
  | {
      state: "blocked";
      reason:
        | "identity-conflict"
        | "missing-session-key"
        | "missing-run-id"
        | "missing-prompt"
        | "untrusted-ingress"
        | "persistence-failure";
      error?: string;
    }
  | {
      state: "admitted";
      runId: string;
      sessionKey: string;
      prompt: string;
      workspaceDir: string;
      databasePath: string;
      lane: "direct" | "durable";
      score: number;
      componentCount: number;
      ticket: IntakeTicket;
      routed: boolean;
      providerMode: "managed" | "passthrough" | undefined;
    };

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

/**
 * Single Ticket-first admission kernel shared by all host adapters.
 *
 * Adapter responsibilities are deliberately narrow: establish trusted host
 * identity, select the host's exact run/session identifiers, and normalize the
 * prompt. This kernel owns the policy transition from eligible semantic turn
 * to one idempotent Ticket + one route event.
 */
export function admitTicketFirstTurn(input: SharedTicketAdmissionInput): SharedTicketAdmissionResult {
  if (input.config.ticketFirst !== true) return { state: "skipped", reason: "disabled" };

  if (input.identityConflict === true) {
    return { state: "blocked", reason: "identity-conflict" };
  }

  const prompt = typeof input.prompt === "string" ? input.prompt : "";
  if (!prompt.trim()) return { state: "blocked", reason: "missing-prompt" };

  // Internal delivery/continuation/recovery turns already carry durable
  // authority and must never be re-admitted as new owner intent.
  if (!ticketIntakeEligible(prompt)) return { state: "skipped", reason: "excluded" };

  const sessionKey = text(input.sessionKey);
  if (!sessionKey) return { state: "blocked", reason: "missing-session-key" };
  if (sessionKey.includes(":subagent:")) return { state: "skipped", reason: "excluded" };

  if (!input.trusted) return { state: "blocked", reason: "untrusted-ingress" };

  const runId = text(input.runId);
  if (!runId) return { state: "blocked", reason: "missing-run-id" };

  const decision = classifyDurableRequest(prompt, input.config.admissionMinimumScore ?? 5);
  const workspaceDir = resolve(input.workspaceDir ?? input.config.workspaceDir ?? process.cwd());
  const databasePath = resolve(input.config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));

  try {
    const store = new TicketStore(databasePath);
    const ticket = store.accept({
      runId,
      ownerSessionKey: sessionKey,
      prompt,
      maxAttempts: input.config.ticketMaximumAttempts,
    });
    const routed = store.route(ticket.ticketId, decision.lane === "durable");
    return {
      state: "admitted",
      runId,
      sessionKey,
      prompt,
      workspaceDir,
      databasePath,
      lane: decision.lane,
      score: decision.score,
      componentCount: decision.sections.length,
      ticket,
      routed,
      providerMode: input.config.providerMode,
    };
  } catch (error) {
    return {
      state: "blocked",
      reason: "persistence-failure",
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

export function canonicalReplyDispatchPrompt(ctx: any): string | undefined {
  for (const candidate of [ctx?.agentText, ctx?.BodyForAgent, ctx?.rawText, ctx?.Body]) {
    if (typeof candidate === "string" && candidate.length > 0) return candidate;
  }
  return undefined;
}

export function replyDispatchProvenanceExcluded(event: any): boolean {
  const provenanceKind = text(event?.ctx?.InputProvenance?.kind).toLowerCase();
  if (provenanceKind === "internal_system" || provenanceKind === "inter_session") return true;

  const internalTurnSource = text(event?.ctx?.InternalTurnSource).toLowerCase();
  if (internalTurnSource === "heartbeat" || internalTurnSource === "cron" || internalTurnSource === "exec") {
    return true;
  }

  return false;
}

export function replyDispatchIdentity(event: any, runtimeCtx?: any) {
  const effectiveDispatchSessionKey = text(event?.sessionKey) || undefined;
  const sourceSessionKey = text(event?.ctx?.SessionKey) || effectiveDispatchSessionKey;
  const dispatchKind = text(runtimeCtx?.dispatchKind).toLowerCase();
  const identityConflict = Boolean(
    dispatchKind !== "acp" &&
      effectiveDispatchSessionKey &&
      sourceSessionKey &&
      effectiveDispatchSessionKey !== sourceSessionKey,
  );
  const runId = text(event?.runId) || text(runtimeCtx?.runId) || undefined;
  return {
    sessionKey: sourceSessionKey,
    sourceSessionKey,
    effectiveDispatchSessionKey,
    runId,
    identityConflict,
  };
}

export function replyDispatchTrusted(event: any): boolean {
  if (event?.ctx?.InboundAccessAuthorized === false) return false;
  if (event?.ctx?.InboundAccessAuthorized === true) return true;
  const scopes = Array.isArray(event?.ctx?.GatewayClientScopes)
    ? event.ctx.GatewayClientScopes.filter((scope: unknown): scope is string => typeof scope === "string")
    : [];
  return scopes.includes("operator.write") || scopes.includes("operator.admin");
}

export function replyDispatchNativeCommandExcluded(event: any, runtimeCtx?: any): boolean {
  const ctx = event?.ctx ?? {};
  const eventKind = text(ctx?.InboundEventKind).toLowerCase();
  if (eventKind === "slash-command" || eventKind === "native-command") return true;

  if (ctx?.CommandAuthorized !== true) return false;
  const cfg = runtimeCtx?.cfg;
  const botUsername = text(ctx?.BotUsername) || undefined;
  for (const candidate of [ctx?.CommandBody, ctx?.BodyForCommands, ctx?.RawBody, ctx?.rawText]) {
    const value = text(candidate);
    if (!value) continue;
    try {
      if (isControlCommandMessage(value, cfg, { botUsername })) return true;
    } catch {
      // Host command facts remain authoritative; detection failure must not
      // turn ordinary conversational text into a command exclusion.
    }
  }
  return false;
}

export function beforeDispatchPrompt(event: any): string | undefined {
  for (const candidate of [event?.body, event?.content]) {
    if (typeof candidate === "string" && candidate.length > 0) return candidate;
  }
  return undefined;
}

function sourceMessageIdentity(input: {
  sessionKey?: unknown;
  channel?: unknown;
  accountId?: unknown;
  messageId?: unknown;
}) {
  const sessionKey = text(input.sessionKey);
  const channel = text(input.channel).toLowerCase();
  const accountId = text(input.accountId);
  const messageId = text(input.messageId);
  if (!sessionKey || !channel || !messageId) return undefined;
  const sourceKey = createHash("sha256")
    .update(JSON.stringify([sessionKey, channel, accountId, messageId]), "utf8")
    .digest("hex");
  return { sourceKey, sessionKey, channel, accountId, messageId };
}

export function beforeDispatchSourceIdentity(event: any, ctx?: any) {
  return sourceMessageIdentity({
    sessionKey: event?.sessionKey ?? ctx?.sessionKey,
    channel: event?.channel ?? ctx?.channelId,
    accountId: ctx?.accountId,
    messageId: event?.messageId ?? ctx?.messageId,
  });
}

export function replyDispatchSourceIdentity(event: any) {
  const ctx = event?.ctx ?? {};
  return sourceMessageIdentity({
    sessionKey: ctx?.SessionKey ?? event?.sessionKey,
    channel: ctx?.OriginatingChannel ?? ctx?.Surface ?? ctx?.Provider,
    accountId: ctx?.AccountId,
    messageId: ctx?.MessageSidFull ?? ctx?.MessageSid ?? ctx?.MessageSidFirst ?? ctx?.MessageSidLast,
  });
}

export function beforeDispatchNativeCommandExcluded(event: any, cfg?: any): boolean {
  const prompt = beforeDispatchPrompt(event);
  if (!prompt) return false;
  try {
    return isControlCommandMessage(prompt, cfg);
  } catch {
    return false;
  }
}
