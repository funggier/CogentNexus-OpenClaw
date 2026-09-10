import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";

type HookApi = {
  pluginConfig?: Record<string, unknown>;
  config?: any;
  on?: (...args: any[]) => void;
  logger?: { warn?: (message: string) => void };
};

function databaseFor(api: HookApi, ctx?: any) {
  const cfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
  const workspace = resolve(
    typeof ctx?.workspaceDir === "string" && ctx.workspaceDir
      ? ctx.workspaceDir
      : typeof cfg.workspaceDir === "string" && cfg.workspaceDir
        ? cfg.workspaceDir
        : api.config?.agents?.defaults?.workspace ?? process.cwd(),
  );
  return resolve(
    typeof cfg.ticketDatabasePath === "string" && cfg.ticketDatabasePath
      ? cfg.ticketDatabasePath
      : defaultTicketDatabase(workspace),
  );
}

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function hasCanonicalSchema(db: DatabaseSync) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_inference_attempt'").get());
}

function existingAttemptId(path: string, runId: string) {
  const db = new DatabaseSync(path);
  try {
    if (!hasCanonicalSchema(db)) return undefined;
    const row = db.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? ORDER BY started_at LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
    return row?.attempt_id;
  } finally { db.close(); }
}

function ticketIdForRun(db: DatabaseSync, runId: string, sessionKey: string) {
  const row = db.prepare(`SELECT ticket_id FROM tickets
    WHERE run_id=? AND owner_session_key=? AND status='accepted'
      AND workflow_eligible=0 AND workflow_id IS NULL
    ORDER BY created_at DESC LIMIT 1`).get(runId, sessionKey) as { ticket_id?: string } | undefined;
  if (!row?.ticket_id) throw new Error(`accepted Ticket not found for inference run ${runId}`);
  return row.ticket_id;
}

/**
 * Translate OpenClaw's model-call observation hooks into canonical
 * InferenceAttempt identities. Provider/model remain attempt provenance only.
 */
export function installV095InferenceHookBridge(api: HookApi) {
  if (typeof api?.on !== "function") return;

  const initialDatabase = databaseFor(api);
  const bootstrap = new TicketStore(initialDatabase);
  bootstrap.snapshot();
  const db = new DatabaseSync(initialDatabase);
  try {
    ensureCanonicalSchema(db);
  } finally {
    db.close();
  }

  api.on("model_call_started", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    const sessionKey = text(event?.sessionKey ?? ctx?.sessionKey);
    const callId = text(event?.callId);
    if (!runId || !sessionKey || !callId) return;
    try {
      const path = databaseFor(api, ctx);
      if (existingAttemptId(path, runId)) return;
      const authority = sessionAuthority(path, sessionKey);
      if (authority.state !== "active") throw new Error(`session ${sessionKey} is not active`);
      const database = new DatabaseSync(path);
      try {
        const ticketId = ticketIdForRun(database, runId, sessionKey);
        const attempt = beginInferenceAttempt(database, {
          ticketId,
          sessionKey,
          sessionGeneration: authority.generation,
          provider: typeof event?.provider === "string" ? event.provider : null,
          model: typeof event?.model === "string" ? event.model : null,
        });
        bindRunId(database, attempt.attemptId, runId);
      } finally { database.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to bridge inference attempt start: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-start" });

  api.on("model_call_ended", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    if (!runId) return;
    try {
      const path = databaseFor(api, ctx);
      const database = new DatabaseSync(path);
      try {
        const row = database.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? AND state='active' LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
        if (!row?.attempt_id) return;
        const outcome = text(event?.outcome) || (text(event?.errorCategory) ? `error:${text(event.errorCategory)}` : "model_call_ended");
        finishInferenceAttempt(database, row.attempt_id, outcome);
      } finally { database.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to bridge inference attempt end: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-end" });

  api.on("agent_end", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    if (!runId) return;
    try {
      const path = databaseFor(api, ctx);
      const database = new DatabaseSync(path);
      try {
        const row = database.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? AND state='active' LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
        if (!row?.attempt_id) return;
        finishInferenceAttempt(database, row.attempt_id, event?.success === true ? "agent_end_ok" : "agent_end_error");
      } finally { database.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to close canonical inference attempt at agent_end: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-agent-end" });
}

function ensureCanonicalSchema(db: DatabaseSync) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_inference_attempt(
      attempt_id TEXT PRIMARY KEY,
      ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      session_key TEXT NOT NULL,
      session_generation INTEGER NOT NULL,
      run_id TEXT,
      provider TEXT,
      model TEXT,
      state TEXT NOT NULL CHECK(state IN ('active','ended')),
      outcome TEXT,
      started_at TEXT NOT NULL,
      ended_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_ticket ON cnx_inference_attempt(ticket_id,started_at);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run ON cnx_inference_attempt(run_id) WHERE run_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_session ON cnx_inference_attempt(session_key,session_generation,started_at);
  `);
}
