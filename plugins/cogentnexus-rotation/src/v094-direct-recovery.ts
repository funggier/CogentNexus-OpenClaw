import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { join, resolve } from "node:path";
import { appendFileSync, mkdirSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

export type V094DirectRecoveryConfig = {
  cogentRoot?: string;
  timeoutSeconds?: number;
  pythonCommand?: string;
  agentId?: string;
};

export type V094DirectRecovery = {
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

type RecoveryRuntime = {
  harness?: string;
  provider?: string;
  model?: string;
};

function primitiveDiagnosticValue(value: unknown): unknown {
  if (value === null || value === undefined) return value ?? null;
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return value;
  if (typeof value === "bigint") return value.toString();
  if (value instanceof Error) {
    const nested = value as Error & Record<string, unknown>;
    return {
      name: value.name,
      message: value.message,
      stack: value.stack ?? null,
      code: primitiveDiagnosticValue(nested.code),
      errno: primitiveDiagnosticValue(nested.errno),
      syscall: primitiveDiagnosticValue(nested.syscall),
      path: primitiveDiagnosticValue(nested.path),
    };
  }
  try {
    return String(value);
  } catch {
    return "<unprintable>";
  }
}

function runtimeErrorDiagnostic(error: unknown) {
  const objectLike = error !== null && (typeof error === "object" || typeof error === "function");
  const value = objectLike ? error as Record<string, unknown> : undefined;
  const own: Record<string, unknown> = {};

  if (objectLike) {
    for (const key of Object.getOwnPropertyNames(error)) {
      try {
        own[key] = primitiveDiagnosticValue((error as Record<string, unknown>)[key]);
      } catch {
        own[key] = "<unreadable>";
      }
    }
  }

  const ctor =
    objectLike &&
    typeof (error as { constructor?: { name?: unknown } }).constructor?.name === "string"
      ? String((error as { constructor?: { name?: unknown } }).constructor?.name)
      : null;

  return {
    type: typeof error,
    constructor: ctor,
    name: error instanceof Error ? error.name : primitiveDiagnosticValue(value?.name),
    message: error instanceof Error ? error.message : primitiveDiagnosticValue(value?.message ?? error),
    code: primitiveDiagnosticValue(value?.code),
    errno: primitiveDiagnosticValue(value?.errno),
    syscall: primitiveDiagnosticValue(value?.syscall),
    path: primitiveDiagnosticValue(value?.path),
    stack: error instanceof Error ? error.stack ?? null : primitiveDiagnosticValue(value?.stack),
    cause: primitiveDiagnosticValue(value?.cause),
    own,
  };
}

function appendRuntimeErrorDiagnostic(
  workspace: string,
  recovery: V094DirectRecovery,
  runId: string,
  stage: string,
  error: unknown,
  runtimeStartedRecorded: boolean,
) {
  try {
    const dir = join(workspace, ".cogent", "runtime");
    mkdirSync(dir, { recursive: true });
    appendFileSync(
      join(dir, "v094-runtime-errors.jsonl"),
      `${JSON.stringify({
        timestamp: now(),
        source: "v094-direct-recovery",
        stage,
        ticketId: recovery.ticket_id,
        ownerSessionKey: recovery.owner_session_key,
        ownerGeneration: recovery.owner_generation,
        runId,
        recoveryAttemptBeforeLaunch: recovery.attempt_count,
        runtimeStartedRecorded,
        error: runtimeErrorDiagnostic(error),
      })}\n`,
      "utf8",
    );
  } catch {
    // Telemetry must never alter recovery semantics.
  }
}

const CLAIM_POLL_MS = 500;
const ABORT_SETTLE_MS = 5_000;

function now() {
  return new Date().toISOString();
}

function delay(ms: number) {
  return new Promise<void>((resolveDelay) => setTimeout(resolveDelay, ms));
}

function openDb(path: string, readOnly = false) {
  if (!readOnly) new TicketStore(path).snapshot();
  const db = readOnly ? new DatabaseSync(path, { readOnly: true }) : new DatabaseSync(path);
  if (readOnly) {
    db.exec("PRAGMA busy_timeout=5000;");
  } else {
    db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  }
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

function claimIdentity(path: string, recovery: V094DirectRecovery, runId?: string): ClaimIdentity {
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

function claim(path: string, recovery: V094DirectRecovery, runId: string) {
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

function retry(path: string, recovery: V094DirectRecovery, runId: string, message: string) {
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
      source: "v094-direct-recovery",
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

function agentIdFromSession(sessionKey: string, fallback = "main") {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1] ?? fallback;
}

function recoveryPrompt(recovery: V094DirectRecovery, context: string) {
  const instruction = recovery.mode === "redeliver"
    ? "Reconstruct only the compact final response. Do not repeat external side effects."
    : "Resume the interrupted request from the latest committed state. Do not repeat completed side effects.";
  return [
    "[CogentNexus Internal Direct Recovery]",
    "This is an internal recovery worker run, not a new user instruction.",
    instruction,
    "Preserve the original user intent and use only the supplied committed context.",
    "Do not perform external side effects or send messages directly.",
    "Return only the user-facing assistant response that should be delivered to the owner session.",
    "",
    "Original committed request:", recovery.prompt,
    "",
    "Bounded read-only owner-session context:", context || "(no usable recent context)",
  ].join("\n");
}

function embeddedAssistantText(result: any) {
  const visible = result?.meta?.finalAssistantVisibleText;
  if (typeof visible === "string" && visible.trim()) return visible.trim();
  const raw = result?.meta?.finalAssistantRawText;
  if (typeof raw === "string" && raw.trim()) return raw.trim();
  const payloads = Array.isArray(result?.payloads) ? result.payloads : [];
  const text = payloads
    .filter((payload: any) => payload && payload.isReasoning !== true && typeof payload.text === "string")
    .map((payload: any) => String(payload.text).trim())
    .filter(Boolean)
    .join("\n")
    .trim();
  return text || undefined;
}

function runtimeFromResult(result: any): RecoveryRuntime {
  const meta = result?.meta?.agentMeta;
  return {
    ...(typeof meta?.provider === "string" && meta.provider ? { provider: meta.provider } : {}),
    ...(typeof meta?.model === "string" && meta.model ? { model: meta.model } : {}),
    ...(typeof meta?.agentHarnessId === "string" && meta.agentHarnessId
      ? { harness: meta.agentHarnessId }
      : typeof result?.meta?.executionTrace?.runner === "string" && result.meta.executionTrace.runner
        ? { harness: result.meta.executionTrace.runner }
        : {}),
  };
}

function assertRuntimeMatches(original: OriginalModel, runtime: RecoveryRuntime) {
  if (original.provider && runtime.provider !== original.provider) {
    throw new Error(`Direct recovery provider drifted: expected ${original.provider}, got ${runtime.provider ?? "unknown"}`);
  }
  if (original.model && runtime.model !== original.model) {
    throw new Error(`Direct recovery model drifted: expected ${original.model}, got ${runtime.model ?? "unknown"}`);
  }
}

function kickHostDelivery(workspace: string, cfg: V094DirectRecoveryConfig) {
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

function recordRuntimeStarted(
  path: string,
  recovery: V094DirectRecovery,
  runId: string,
  original: OriginalModel,
  runtime: RecoveryRuntime,
) {
  const db = openDb(path), stamp = now();
  try {
    addEvent(db, recovery.ticket_id, "direct_recovery_runtime_started", {
      runId,
      ownerGeneration: recovery.owner_generation,
      requestedProvider: original.provider ?? null,
      requestedModel: original.model ?? null,
      runtimeHarness: runtime.harness ?? null,
      runtimeProvider: runtime.provider ?? null,
      runtimeModel: runtime.model ?? null,
      execution: "embedded-agent",
      source: "v094-direct-recovery",
    }, stamp);
  } finally {
    db.close();
  }
}

function markResponseReady(
  path: string,
  recovery: V094DirectRecovery,
  runId: string,
  text: string,
  original: OriginalModel,
  runtime: RecoveryRuntime,
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
        originalProvider: original.provider ?? null,
        originalModel: original.model ?? null,
        recoveryProvider: runtime.provider ?? null,
        recoveryModel: runtime.model ?? null,
        recoveryHarness: runtime.harness ?? null,
        recoveryExecution: "embedded-agent",
      }), stamp, stamp, recovery.ticket_id);
    db.prepare(`UPDATE cnx_direct_recovery SET state='awaiting_delivery',active_run_id=NULL,next_attempt_at=NULL,
      last_error=NULL,updated_at=? WHERE ticket_id=? AND state='running' AND active_run_id=?`)
      .run(stamp, recovery.ticket_id, runId);
    addEvent(db, recovery.ticket_id, "direct_recovery_response_ready", {
      runId,
      deliveryMode: "host-chat-inject",
      ownerGeneration: recovery.owner_generation,
      originalProvider: original.provider ?? null,
      originalModel: original.model ?? null,
      recoveryProvider: runtime.provider ?? null,
      recoveryModel: runtime.model ?? null,
      recoveryHarness: runtime.harness ?? null,
      recoveryExecution: "embedded-agent",
      responseReadyFirstCommit: firstReady,
      source: "v094-direct-recovery",
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

function isTransientSqliteBusy(error: unknown) {
  if (!error || (typeof error !== "object" && typeof error !== "function")) return false;
  const value = error as Record<string, unknown>;
  const code = typeof value.code === "string" ? value.code : "";
  const message = typeof value.message === "string" ? value.message : "";
  const errcode = Number(value.errcode);
  const primary = Number.isFinite(errcode) ? (errcode & 0xff) : NaN;

  return (
    code === "SQLITE_BUSY" ||
    primary === 5 ||
    (code === "ERR_SQLITE_ERROR" && /\bdatabase is (?:locked|busy)\b/i.test(message))
  );
}

async function waitForClaimRevocation(
  path: string,
  recovery: V094DirectRecovery,
  runId: string,
  stopped: () => boolean,
) {
  while (!stopped()) {
    await delay(CLAIM_POLL_MS);
    if (stopped()) break;

    try {
      const identity = claimIdentity(path, recovery, runId);
      if (!identity.authorized) return identity.reason;
    } catch (error) {
      if (!isTransientSqliteBusy(error)) throw error;

      // A transient WAL/BUSY read is not evidence that durable authority
      // was revoked and must never reject the revocation watcher. Rejecting
      // here races the still-running embedded inference against retry().
      continue;
    }
  }
  return undefined;
}

function recordRuntimeAbort(
  path: string,
  recovery: V094DirectRecovery,
  runId: string,
  reason: string,
  abortSettled?: boolean,
) {
  const db = openDb(path), stamp = now();
  try {
    addEvent(db, recovery.ticket_id, "direct_recovery_runtime_aborted", {
      runId,
      reason,
      ownerGeneration: recovery.owner_generation,
      abortSettled: abortSettled ?? null,
      execution: "embedded-agent",
      source: "v094-direct-recovery",
    }, stamp);
  } finally {
    db.close();
  }
}

/**
 * Direct recovery executor with five hard boundaries:
 * 1) preserve the original provider/model with no fallback substitution,
 * 2) run outside the request-scoped subagent model-override authorization path,
 * 3) abort embedded inference when Ticket/recovery/session authority is revoked,
 * 4) commit response_ready_at once only,
 * 5) prefer the v0.9.2 durable delivery transport.
 */
export async function launchV094DirectRecovery(
  api: any,
  path: string,
  workspace: string,
  recovery: V094DirectRecovery,
  cfg: V094DirectRecoveryConfig,
) {
  const attempt = Number(recovery.attempt_count) + 1;
  const runId = `cnx-direct-${recovery.ticket_id.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 48)}-${attempt}-g${recovery.owner_generation}`;
  if (!claim(path, recovery, runId)) return;

  const original = originalModel(path, recovery.ticket_id);
  const agentId = agentIdFromSession(recovery.owner_session_key, cfg.agentId ?? "main");
  const abortController = new AbortController();
  let stopFence = false;
  let runtimeStartedRecorded = false;
  let diagnosticStage = "pre-launch";

  try {
    const initialIdentity = claimIdentity(path, recovery, runId);
    if (!initialIdentity.authorized) return;

    diagnosticStage = "owner-session-read";
    const owner = await api.runtime.subagent.getSessionMessages({ sessionKey: recovery.owner_session_key, limit: 24 });
    const beforeLaunch = claimIdentity(path, recovery, runId);
    if (!beforeLaunch.authorized) return;

    const timeoutMs = Math.max(60_000, Math.min((cfg.timeoutSeconds ?? 3600) * 1000, 3_600_000));
    const runtimeConfig = api.runtime.config?.current?.() ?? api.config;
    diagnosticStage = "embedded-run";
    const completionPromise = Promise.resolve(api.runtime.agent.runEmbeddedAgent({
      sessionId: runId,
      agentId,
      workspaceDir: workspace,
      cwd: workspace,
      config: runtimeConfig,
      prompt: recoveryPrompt(recovery, boundedOwnerContext(owner.messages ?? [])),
      transcriptPrompt: recovery.prompt,
      provider: original.provider,
      model: original.model,
      modelFallbacksOverride: [],
      disableTools: true,
      disableMessageTool: true,
      bootstrapContextMode: "lightweight",
      trigger: "manual",
      timeoutMs,
      runTimeoutOverrideMs: timeoutMs,
      runId,
      abortSignal: abortController.signal,
      suppressLiveStreamOutput: true,
      suppressNextUserMessagePersistence: true,
      suppressTranscriptOnlyAssistantPersistence: true,
      suppressAssistantErrorPersistence: true,
      cleanupBundleMcpOnRunEnd: true,
      oneShotCliRun: true,
      onExecutionPhase: (info: any) => {
        if (runtimeStartedRecorded || (!info?.provider && !info?.model)) return;
        const phaseRuntime: RecoveryRuntime = {
          ...(typeof info.provider === "string" && info.provider ? { provider: info.provider } : {}),
          ...(typeof info.model === "string" && info.model ? { model: info.model } : {}),
          ...(typeof info.backend === "string" && info.backend ? { harness: info.backend } : {}),
        };
        try {
          recordRuntimeStarted(path, recovery, runId, original, phaseRuntime);
        } catch (error) {
          appendRuntimeErrorDiagnostic(
            workspace,
            recovery,
            runId,
            "record-runtime-started",
            error,
            runtimeStartedRecorded,
          );
          throw error;
        }
        runtimeStartedRecorded = true;
      },
    })).then(
      (result: any) => ({ kind: "completion" as const, result }),
      (error: unknown) => ({ kind: "error" as const, error }),
    );

    const revocationPromise = waitForClaimRevocation(path, recovery, runId, () => stopFence)
      .then((reason) => ({ kind: "revocation" as const, reason }));
    const outcome = await Promise.race([completionPromise, revocationPromise]);

    if (outcome.kind === "revocation") {
      stopFence = true;
      const reason = outcome.reason ?? "recovery-authority-revoked";
      abortController.abort();
      const abortSettled = await Promise.race([
        completionPromise.then(() => true),
        delay(ABORT_SETTLE_MS).then(() => false),
      ]);
      recordRuntimeAbort(path, recovery, runId, reason, abortSettled);
      return;
    }

    stopFence = true;
    if (outcome.kind === "error") {
      const identity = claimIdentity(path, recovery, runId);
      if (!identity.authorized) {
        recordRuntimeAbort(path, recovery, runId, identity.reason, true);
        return;
      }
      appendRuntimeErrorDiagnostic(
        workspace,
        recovery,
        runId,
        "embedded-promise-rejection",
        outcome.error,
        runtimeStartedRecorded,
      );
      retry(path, recovery, runId, outcome.error instanceof Error ? outcome.error.message : String(outcome.error));
      return;
    }

    const result = outcome.result;
    const identity = claimIdentity(path, recovery, runId);
    if (!identity.authorized) {
      recordRuntimeAbort(path, recovery, runId, identity.reason, true);
      return;
    }

    diagnosticStage = "post-run-result";
    const runtime = runtimeFromResult(result);
    assertRuntimeMatches(original, runtime);
    if (!runtimeStartedRecorded) {
      recordRuntimeStarted(path, recovery, runId, original, runtime);
      runtimeStartedRecorded = true;
    }
    if (result?.meta?.aborted === true) {
      retry(path, recovery, runId, `Direct recovery embedded run aborted${result?.meta?.timeoutPhase ? ` at ${result.meta.timeoutPhase}` : ""}`);
      return;
    }
    if (result?.meta?.error && !embeddedAssistantText(result)) {
      appendRuntimeErrorDiagnostic(
        workspace,
        recovery,
        runId,
        "embedded-result-meta-error",
        result.meta.error,
        runtimeStartedRecorded,
      );
      retry(path, recovery, runId, result.meta.error.message ?? "Direct recovery embedded run failed");
      return;
    }

    const text = embeddedAssistantText(result);
    if (!text) {
      retry(path, recovery, runId, "Direct recovery produced no visible assistant output");
      return;
    }
    diagnosticStage = "response-ready-commit";
    if (markResponseReady(path, recovery, runId, text, original, runtime)) kickHostDelivery(workspace, cfg);
  } catch (error) {
    stopFence = true;
    appendRuntimeErrorDiagnostic(
      workspace,
      recovery,
      runId,
      `outer-catch:${diagnosticStage}`,
      error,
      runtimeStartedRecorded,
    );
    const identity = claimIdentity(path, recovery, runId);
    if (identity.authorized) {
      retry(path, recovery, runId, error instanceof Error ? error.message : String(error));
    } else {
      recordRuntimeAbort(path, recovery, runId, identity.reason, abortController.signal.aborted);
    }
  } finally {
    stopFence = true;
  }
}
