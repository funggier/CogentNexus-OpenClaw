import { createHash } from "node:crypto";
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";

export const V091_DELIVERY_TELEMETRY_FILE = "v091-delivery-hooks.jsonl";

function cleanString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function digest(value: string): string {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

function redactedText(value: unknown) {
  if (typeof value !== "string") return { present: false, chars: 0 };
  return {
    present: value.length > 0,
    chars: value.length,
    sha256: digest(value),
  };
}

function payloadText(event: any): unknown {
  const candidates = [
    event?.payload?.text,
    event?.message?.text,
    event?.text,
    event?.prompt,
    event?.content,
  ];
  return candidates.find((value) => typeof value === "string");
}

function payloadMedia(event: any) {
  const payload = event?.payload ?? event?.message ?? {};
  const urls = Array.isArray(payload?.mediaUrls)
    ? payload.mediaUrls
    : typeof payload?.mediaUrl === "string"
      ? [payload.mediaUrl]
      : [];
  return {
    count: urls.length,
    hasMedia: urls.length > 0,
  };
}

function queuedCounts(ctx: any) {
  try {
    const counts = ctx?.dispatcher?.getQueuedCounts?.();
    if (!counts || typeof counts !== "object") return undefined;
    return {
      tool: Number.isFinite(counts.tool) ? Number(counts.tool) : undefined,
      block: Number.isFinite(counts.block) ? Number(counts.block) : undefined,
      final: Number.isFinite(counts.final) ? Number(counts.final) : undefined,
    };
  } catch {
    return { error: "unavailable" };
  }
}

function errorMeta(error: unknown) {
  if (typeof error !== "string" || !error) return undefined;
  return { chars: error.length, sha256: digest(error) };
}

export function v091DeliveryTelemetryPath(cogentRoot: string) {
  return resolve(cogentRoot, "runtime", V091_DELIVERY_TELEMETRY_FILE);
}

export function buildV091DeliveryTelemetryRecord(
  hook: string,
  event: any,
  ctx: any,
  now = new Date(),
) {
  const text = redactedText(payloadText(event));
  return {
    schemaVersion: 1,
    at: now.toISOString(),
    hook,
    eventRunId: cleanString(event?.runId),
    contextRunId: cleanString(ctx?.runId),
    eventSessionKey: cleanString(event?.sessionKey),
    contextSessionKey: cleanString(ctx?.sessionKey),
    channelId: cleanString(ctx?.channelId ?? event?.channelId),
    accountId: cleanString(ctx?.accountId ?? event?.accountId),
    conversationId: cleanString(ctx?.conversationId ?? event?.conversationId),
    kind: cleanString(event?.kind),
    success: typeof event?.success === "boolean" ? event.success : undefined,
    error: errorMeta(event?.error),
    payload: {
      text,
      media: payloadMedia(event),
    },
    dispatcher: {
      present: Boolean(ctx?.dispatcher),
      appendBeforeDeliver: typeof ctx?.dispatcher?.appendBeforeDeliver === "function",
      waitForIdle: typeof ctx?.dispatcher?.waitForIdle === "function",
      queuedCounts: queuedCounts(ctx),
    },
    eventKeys: event && typeof event === "object" ? Object.keys(event).sort() : [],
    contextKeys: ctx && typeof ctx === "object" ? Object.keys(ctx).sort() : [],
  };
}

export function appendV091DeliveryTelemetry(path: string, record: unknown) {
  try {
    mkdirSync(dirname(path), { recursive: true });
    appendFileSync(path, `${JSON.stringify(record)}\n`, "utf8");
  } catch {
    // Diagnostic telemetry must never affect Ticket, inference, or delivery semantics.
  }
}

export function installV091NativeDeliveryTelemetry(api: any, cogentRoot: string) {
  if (typeof api?.on !== "function") return;
  const path = v091DeliveryTelemetryPath(cogentRoot);
  const hooks = [
    "before_agent_run",
    "model_call_started",
    "model_call_ended",
    "reply_dispatch",
    "reply_payload_sending",
    "message_sent",
    "agent_end",
  ];

  for (const hook of hooks) {
    try {
      api.on(
        hook,
        (event: any, ctx: any) => {
          appendV091DeliveryTelemetry(
            path,
            buildV091DeliveryTelemetryRecord(hook, event, ctx),
          );
          return undefined;
        },
        {
          registrationId: `cogentnexus-v091-native-delivery-telemetry-${hook.replace(/_/g, "-")}`,
          priority: -20_000,
        },
      );
    } catch {
      // Hook registration failure is observation-only and must fail open.
    }
  }
}
