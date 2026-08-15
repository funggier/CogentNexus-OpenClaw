import { existsSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import type { TicketStore } from "./ticket-store.js";

export type DeliveryTarget =
  | { kind: "ticket"; outboxId: number }
  | { kind: "workflow"; taskId: string; stateRevision: number };

export type WorkflowDeliveryNotice = {
  schemaVersion: number;
  taskId: string;
  ownerSessionKey: string;
  workflowStatus: string;
  stateRevision?: number;
  createdAt: string;
  deliveryStatus: string;
  deliveredAt?: string;
  deliveryAttempts?: number;
  lastDeliveryAttemptAt?: string;
  lastDeliveryError?: string;
  scheduledAt?: string;
  deliveryRunId?: string;
};

export function hasVisibleAssistantOutput(messages: unknown[]): boolean {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    const message = messages[index] as any;
    if (!message || message.role !== "assistant") continue;
    const content = message.content;
    if (typeof content === "string") return content.trim().length > 0;
    if (Array.isArray(content)) {
      return content.some((part) => {
        if (typeof part === "string") return part.trim().length > 0;
        if (!part || typeof part !== "object") return false;
        const text = typeof part.text === "string" ? part.text : typeof part.content === "string" ? part.content : "";
        if (text.trim()) return true;
        return ["image", "audio", "video", "file", "media"].includes(String(part.type ?? "").toLowerCase());
      });
    }
    return false;
  }
  return false;
}

function cleanTagPart(value: string, limit = 96): string {
  return value.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, limit);
}

export function postCompactionResumeTag(sessionKey: string): string {
  return `cogent-post-compact-${cleanTagPart(sessionKey, 80)}`;
}

export function ticketDeliveryMarker(outboxId: number): string {
  return `[CogentNexus Delivery: ticket:${Math.trunc(outboxId)}]`;
}

export function workflowDeliveryMarker(taskId: string, stateRevision = 0): string {
  return `[CogentNexus Delivery: workflow:${cleanTagPart(taskId, 96)}:${Math.trunc(stateRevision)}]`;
}

export function parseDeliveryMarker(prompt: string): DeliveryTarget | undefined {
  const ticket = prompt.match(/\[CogentNexus Delivery: ticket:(\d+)\]/u);
  if (ticket) return { kind: "ticket", outboxId: Number(ticket[1]) };
  const workflow = prompt.match(/\[CogentNexus Delivery: workflow:([A-Za-z0-9_-]{1,96}):(\d+)\]/u);
  if (workflow) return { kind: "workflow", taskId: workflow[1], stateRevision: Number(workflow[2]) };
  return undefined;
}

function completionPath(workspaceDir: string, target: Extract<DeliveryTarget, { kind: "workflow" }>): string {
  return resolve(workspaceDir, ".cogent", "workflows", target.taskId, "completion.json");
}

function readCompletion(path: string): WorkflowDeliveryNotice | undefined {
  if (!existsSync(path)) return undefined;
  try {
    return JSON.parse(readFileSync(path, "utf8")) as WorkflowDeliveryNotice;
  } catch {
    return undefined;
  }
}

function writeCompletion(path: string, notice: WorkflowDeliveryNotice) {
  const temporary = `${path}.${process.pid}.tmp`;
  writeFileSync(temporary, `${JSON.stringify(notice, null, 2)}\n`, "utf8");
  renameSync(temporary, path);
}

export function bindDeliveryRun(input: {
  workspaceDir: string;
  store: TicketStore;
  target: DeliveryTarget;
  runId: string;
  now?: Date;
}): boolean {
  if (input.target.kind === "ticket") return input.store.bindOutboxRun(input.target.outboxId, input.runId);
  const path = completionPath(input.workspaceDir, input.target);
  const notice = readCompletion(path);
  if (!notice || notice.deliveryStatus !== "pending" || notice.taskId !== input.target.taskId || Number(notice.stateRevision ?? 0) !== input.target.stateRevision) return false;
  writeCompletion(path, { ...notice, deliveryRunId: input.runId, lastDeliveryAttemptAt: (input.now ?? new Date()).toISOString() });
  return true;
}

export function settleDeliveryTarget(input: {
  workspaceDir: string;
  store: TicketStore;
  target: DeliveryTarget;
  success: boolean;
  error?: string;
  now?: Date;
}): boolean {
  if (input.target.kind === "ticket") {
    return input.success
      ? input.store.markOutboxDelivered(input.target.outboxId, input.now)
      : input.store.markOutboxFailed(input.target.outboxId, input.error ?? "delivery failed");
  }
  const path = completionPath(input.workspaceDir, input.target);
  const notice = readCompletion(path);
  if (!notice || notice.deliveryStatus !== "pending" || notice.taskId !== input.target.taskId || Number(notice.stateRevision ?? 0) !== input.target.stateRevision) return false;
  const nowIso = (input.now ?? new Date()).toISOString();
  if (input.success) {
    writeCompletion(path, { ...notice, deliveryStatus: "delivered", deliveredAt: nowIso, lastDeliveryError: undefined, scheduledAt: undefined });
  } else {
    writeCompletion(path, { ...notice, deliveryStatus: "pending", lastDeliveryError: (input.error ?? "delivery failed").slice(0, 2000), scheduledAt: undefined, deliveryRunId: undefined });
  }
  return true;
}

export function markWorkflowDeliveryScheduled(path: string, notice: WorkflowDeliveryNotice, now = new Date()): WorkflowDeliveryNotice {
  const nowIso = now.toISOString();
  const next: WorkflowDeliveryNotice = {
    ...notice,
    deliveryStatus: "pending",
    deliveryAttempts: (notice.deliveryAttempts ?? 0) + 1,
    lastDeliveryAttemptAt: nowIso,
    lastDeliveryError: undefined,
    scheduledAt: nowIso,
    deliveryRunId: undefined,
  };
  writeCompletion(path, next);
  return next;
}

export function markWorkflowDeliveryScheduleFailed(path: string, notice: WorkflowDeliveryNotice, error: string): WorkflowDeliveryNotice {
  const next: WorkflowDeliveryNotice = { ...notice, deliveryStatus: "pending", lastDeliveryError: error.slice(0, 2000), scheduledAt: undefined, deliveryRunId: undefined };
  writeCompletion(path, next);
  return next;
}

export function workflowDeliveryIsRetryable(notice: WorkflowDeliveryNotice, now = new Date(), retryAfterMs = 300_000): boolean {
  if (notice.deliveryStatus !== "pending") return false;
  if (!notice.scheduledAt) return true;
  const scheduled = Date.parse(notice.scheduledAt);
  return !Number.isFinite(scheduled) || scheduled <= now.getTime() - Math.max(1_000, retryAfterMs);
}

export function hasPendingWorkflowDeliveryForSession(workspaceDir: string, sessionKey: string): boolean {
  const base = resolve(workspaceDir, ".cogent", "workflows");
  if (!existsSync(base)) return false;
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const notice = readCompletion(join(base, entry.name, "completion.json"));
    if (notice?.deliveryStatus === "pending" && notice.ownerSessionKey === sessionKey) return true;
  }
  return false;
}

export function hasPendingSessionWork(workspaceDir: string, store: TicketStore, sessionKey: string): boolean {
  return store.hasNonTerminalForSession(sessionKey) || store.hasPendingOutboxForSession(sessionKey) || hasPendingWorkflowDeliveryForSession(workspaceDir, sessionKey);
}

export function hasPendingDirectExecutionForSession(store: TicketStore, sessionKey: string): boolean {
  return store.hasPendingDirectExecutionForSession(sessionKey);
}
