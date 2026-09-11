import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { beginInferenceAttempt, bindRunId, findInferenceAttempt, finishInferenceAttempt } from "./v095-inference-attempt.js";

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

function ticketIdForRun(db: DatabaseSync, runId: string, sessionKey: string) {
  const rows = db.prepare(`SELECT ticket_id FROM tickets
    WHERE run_id=? AND owner_session_key=? AND status='accepted'
      AND workflow_eligible=0 AND workflow_id IS NULL
    ORDER BY ticket_id`).all(runId, sessionKey) as Array<{ ticket_id?: string }>;
  if (rows.length === 0) throw new Error(`accepted Ticket not found for inference run ${runId}`);
  if (rows.length !== 1 || !rows[0]?.ticket_id) {
    throw new Error(`ambiguous accepted Ticket ownership for inference run ${runId}`);
  }
  return rows[0].ticket_id;
}

/** Translate each OpenClaw model-call observation into one call-scoped canonical attempt. */
export function installV095InferenceHookBridge(api: HookApi) {
  if (typeof api?.on !== "function") return;

  const initialDatabase = databaseFor(api);
  new TicketStore(initialDatabase).snapshot();
  const db = new DatabaseSync(initialDatabase);
  try { ensureCanonicalSchema(db); } finally { db.close(); }

  api.on("model_call_started", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    const sessionKey = text(event?.sessionKey ?? ctx?.sessionKey);
    const callId = text(event?.callId);
    if (!runId || !sessionKey || !callId) return;
    try {
      const path = databaseFor(api, ctx);
      const authority = sessionAuthority(path, sessionKey);
      if (authority.state !== "active") throw new Error(`session ${sessionKey} is not active`);
      const database = new DatabaseSync(path);
      try {
        const existing = findInferenceAttempt(database, runId, callId);
        if (existing) return;
        const attempt = beginInferenceAttempt(database, {
          ticketId: ticketIdForRun(database, runId, sessionKey),
          sessionKey,
          sessionGeneration: authority.generation,
          callId,
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
    const callId = text(event?.callId);
    if (!runId || !callId) return;
    try {
      const path = databaseFor(api, ctx);
      const database = new DatabaseSync(path);
      try {
        const attempt = findInferenceAttempt(database, runId, callId);
        if (!attempt || attempt.state !== "active") return;
        const outcome = text(event?.outcome) || (text(event?.errorCategory) ? `error:${text(event.errorCategory)}` : "model_call_ended");
        finishInferenceAttempt(database, attempt.attemptId, outcome);
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
        const rows = database.prepare(`SELECT attempt_id FROM cnx_inference_attempt
          WHERE run_id=? AND state='active'`).all(runId) as Array<{ attempt_id?: string }>;
        for (const row of rows) {
          if (row.attempt_id) finishInferenceAttempt(database, row.attempt_id, event?.success === true ? "agent_end_ok" : "agent_end_error");
        }
      } finally { database.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to close canonical inference attempts at agent_end: ${error instanceof Error ? error.message : String(error)}`);
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
      call_id TEXT NOT NULL,
      provider TEXT,
      model TEXT,
      state TEXT NOT NULL CHECK(state IN ('active','ended')),
      outcome TEXT,
      started_at TEXT NOT NULL,
      ended_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_ticket ON cnx_inference_attempt(ticket_id,started_at);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run ON cnx_inference_attempt(run_id,started_at);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_run_call ON cnx_inference_attempt(run_id,call_id);
    CREATE INDEX IF NOT EXISTS idx_cnx_inference_attempt_session ON cnx_inference_attempt(session_key,session_generation,started_at);
  `);
}
