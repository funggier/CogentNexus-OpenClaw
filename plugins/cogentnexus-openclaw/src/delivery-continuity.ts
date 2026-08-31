import { randomUUID } from "node:crypto";
import { existsSync, linkSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
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
  return `[CogentNexus-OpenClaw Delivery: ticket:${Math.trunc(outboxId)}]`;
}

export function workflowDeliveryMarker(taskId: string, stateRevision = 0): string {
  return `[CogentNexus-OpenClaw Delivery: workflow:${cleanTagPart(taskId, 96)}:${Math.trunc(stateRevision)}]`;
}

export function parseDeliveryMarker(prompt: string): DeliveryTarget | undefined {
  const ticket = prompt.match(/\[CogentNexus-OpenClaw Delivery: ticket:(\d+)\]/u);
  if (ticket) return { kind: "ticket", outboxId: Number(ticket[1]) };
  const workflow = prompt.match(/\[CogentNexus-OpenClaw Delivery: workflow:([A-Za-z0-9_-]{1,96}):(\d+)\]/u);
  if (workflow) return { kind: "workflow", taskId: workflow[1], stateRevision: Number(workflow[2]) };
  return undefined;
}

function completionPath(workspaceDir: string, target: Extract<DeliveryTarget, { kind: "workflow" }>): string {
  return resolve(workspaceDir, ".cogentnexus-openclaw", "workflows", target.taskId, "completion.json");
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

type CompletionLock = { pid: number; token: string; acquiredAt: string };

function readCompletionLock(path: string): CompletionLock | undefined {
  try {
    const lock = JSON.parse(readFileSync(`${path}.lock`, "utf8")) as CompletionLock;
    if (!Number.isInteger(lock.pid) || lock.pid <= 0 || typeof lock.token !== "string" || !lock.token || typeof lock.acquiredAt !== "string") return undefined;
    return lock;
  } catch { return undefined; }
}

function processIsAlive(pid: number): boolean {
  try { process.kill(pid, 0); return true; } catch { return false; }
}

export function publishCompletionLock(lockPath: string, record: CompletionLock, publish: typeof linkSync = linkSync): void {
  const temporary = `${lockPath}.${record.pid}.${record.token}.tmp`;
  try {
    writeFileSync(temporary, JSON.stringify(record), "utf8");
    publish(temporary, lockPath);
  } finally {
    try { unlinkSync(temporary); } catch {}
  }
}

export function withCompletionLock<T>(path: string, callback: () => T): T | undefined {
  const lockPath = `${path}.lock`;
  const record: CompletionLock = { pid: process.pid, token: randomUUID(), acquiredAt: new Date().toISOString() };
  let published = false;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    try {
      publishCompletionLock(lockPath, record);
      published = true;
      break;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") return undefined;
      const existing = readCompletionLock(path);
      if (!existing || processIsAlive(existing.pid)) return undefined;
      try { unlinkSync(lockPath); } catch { return undefined; }
    }
  }
  if (!published) return undefined;
  try { return callback(); } finally {
    const current = readCompletionLock(path);
    if (current?.pid === process.pid && current.token === record.token) { try { unlinkSync(lockPath); } catch {} }
  }
}

export function bindDeliveryRun(input: {
  workspaceDir: string;
  store: TicketStore;
  target: DeliveryTarget;
  runId: string;
  sessionKey?: string;
  now?: Date;
}): boolean {
  if (input.target.kind === "ticket") return input.store.bindOutboxRun(input.target.outboxId, input.runId, input.sessionKey);
  const path = completionPath(input.workspaceDir, input.target);
  const workflowTarget = input.target as Extract<DeliveryTarget, { kind: "workflow" }>;
  return withCompletionLock(path, () => {
    const notice = readCompletion(path);
    if (!notice || notice.deliveryStatus !== "pending" || notice.taskId !== workflowTarget.taskId || Number(notice.stateRevision ?? 0) !== workflowTarget.stateRevision) return false;
    if (input.sessionKey && notice.ownerSessionKey !== input.sessionKey) return false;
    if (notice.deliveryRunId && notice.deliveryRunId !== input.runId) return false;
    writeCompletion(path, { ...notice, deliveryRunId: input.runId, lastDeliveryAttemptAt: (input.now ?? new Date()).toISOString() });
    return true;
  }) ?? false;
}

export function settleDeliveryTarget(input: {
  workspaceDir: string;
  store: TicketStore;
  target: DeliveryTarget;
  success: boolean;
  runId?: string;
  sessionKey?: string;
  error?: string;
  now?: Date;
}): boolean {
  if (input.target.kind === "ticket") {
    return input.success
      ? input.store.markOutboxDelivered(input.target.outboxId, input.now, input.runId, input.sessionKey)
      : input.store.markOutboxFailed(input.target.outboxId, input.error ?? "delivery failed", input.runId, input.sessionKey);
  }
    const path = completionPath(input.workspaceDir, input.target);
    const workflowTarget = input.target as Extract<DeliveryTarget, { kind: "workflow" }>;
    return withCompletionLock(path, () => {
      const notice = readCompletion(path);
      if (!notice || notice.deliveryStatus !== "pending" || notice.taskId !== workflowTarget.taskId || Number(notice.stateRevision ?? 0) !== workflowTarget.stateRevision) return false;
    if (input.sessionKey && notice.ownerSessionKey !== input.sessionKey) return false;
    if (input.runId && notice.deliveryRunId !== input.runId) return false;
    const nowIso = (input.now ?? new Date()).toISOString();
    if (input.success) {
      writeCompletion(path, { ...notice, deliveryStatus: "delivered", deliveredAt: nowIso, lastDeliveryError: undefined, scheduledAt: undefined });
    } else {
      writeCompletion(path, { ...notice, deliveryStatus: "pending", lastDeliveryError: (input.error ?? "delivery failed").slice(0, 2000), scheduledAt: undefined, deliveryRunId: undefined });
    }
    return true;
  }) ?? false;
}

export function markWorkflowDeliveryScheduled(path: string, notice: WorkflowDeliveryNotice, now = new Date()): WorkflowDeliveryNotice | undefined {
  return withCompletionLock(path, () => {
    const current = readCompletion(path);
    if (!current || current.taskId !== notice.taskId || Number(current.stateRevision ?? 0) !== Number(notice.stateRevision ?? 0) || current.ownerSessionKey !== notice.ownerSessionKey || current.deliveryStatus !== notice.deliveryStatus || current.deliveryStatus === "delivered" || !workflowDeliveryIsRetryable(current, now)) return undefined;
    const nowIso = now.toISOString();
    const next: WorkflowDeliveryNotice = {
      ...current,
      deliveryStatus: "pending",
      deliveryAttempts: (current.deliveryAttempts ?? 0) + 1,
      lastDeliveryAttemptAt: nowIso,
      lastDeliveryError: undefined,
      scheduledAt: nowIso,
      deliveryRunId: undefined,
    };
    writeCompletion(path, next);
    return next;
  });
}

export function markWorkflowDeliveryScheduleFailed(path: string, notice: WorkflowDeliveryNotice, error: string): WorkflowDeliveryNotice | undefined {
  return withCompletionLock(path, () => {
    const current = readCompletion(path);
    if (!current || current.taskId !== notice.taskId || Number(current.stateRevision ?? 0) !== Number(notice.stateRevision ?? 0) || current.ownerSessionKey !== notice.ownerSessionKey || current.deliveryStatus !== "pending" || current.deliveryStatus !== notice.deliveryStatus || current.deliveryAttempts !== notice.deliveryAttempts || current.scheduledAt !== notice.scheduledAt || current.lastDeliveryAttemptAt !== notice.lastDeliveryAttemptAt || current.deliveryRunId !== notice.deliveryRunId) return undefined;
    const next: WorkflowDeliveryNotice = { ...current, deliveryStatus: "pending", lastDeliveryError: error.slice(0, 2000), scheduledAt: undefined, deliveryRunId: undefined };
    writeCompletion(path, next);
    return next;
  });
}

export function workflowDeliveryIsRetryable(notice: WorkflowDeliveryNotice, now = new Date(), retryAfterMs = 300_000): boolean {
  if (notice.deliveryStatus !== "pending") return false;
  if (!notice.scheduledAt) return true;
  const scheduled = Date.parse(notice.scheduledAt);
  return !Number.isFinite(scheduled) || scheduled <= now.getTime() - Math.max(1_000, retryAfterMs);
}

export function hasPendingWorkflowDeliveryForSession(workspaceDir: string, sessionKey: string): boolean {
  const base = resolve(workspaceDir, ".cogentnexus-openclaw", "workflows");
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
