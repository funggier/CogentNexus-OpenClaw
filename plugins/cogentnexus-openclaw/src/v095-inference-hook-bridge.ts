import { resolve } from "node:path";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { beginInferenceAttempt, bindRunId, finishInferenceAttempt } from "./v095-inference-attempt.js";

type HookApi = {
  pluginConfig?: Record<string, unknown>;
  config?: any;
  on?: (name: string, handler: (event: any, ctx: any) => unknown, options?: any) => void;
  logger?: { warn?: (message: string) => void; error?: (message: string) => void };
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

function existingAttemptId(path: string, runId: string) {
  const store = new TicketStore(path);
  const db = (store as any).open?.();
  if (db) {
    try {
      const row = db.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? ORDER BY started_at LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
      return row?.attempt_id;
    } finally { db.close(); }
  }
  return undefined;
}

/**
 * Translate OpenClaw's model-call observation hooks into the canonical
 * InferenceAttempt identity. The bridge is observation-only: provider/model are
 * stored as attempt provenance and never affect CNX lifecycle/routing authority.
 */
export function installV095InferenceHookBridge(api: HookApi) {
  if (typeof api?.on !== "function") return;

  // Force the additive canonical table to exist before the first hook arrives.
  const initialDatabase = databaseFor(api);
  new TicketStore(initialDatabase).snapshot();
  const sessionAuthorityCache = new Map<string, number>();

  const generationFor = (path: string, sessionKey: string) => {
    const cached = sessionAuthorityCache.get(`${path}\0${sessionKey}`);
    if (cached !== undefined) return cached;
    const authority = sessionAuthority(path, sessionKey);
    if (authority.state !== "active") throw new Error(`session ${sessionKey} is not active`);
    sessionAuthorityCache.set(`${path}\0${sessionKey}`, authority.generation);
    return authority.generation;
  };

  api.on("model_call_started", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    const sessionKey = text(event?.sessionKey ?? ctx?.sessionKey);
    const callId = text(event?.callId);
    if (!runId || !sessionKey || !callId) return;
    try {
      const path = databaseFor(api, ctx);
      // One OpenClaw run maps to one canonical inference attempt. Duplicate
      // start notifications therefore become idempotent observations.
      if (existingAttemptId(path, runId)) return;
      const db = new (requireDatabaseSync())(path);
      try {
        const attempt = beginInferenceAttempt(db, {
          ticketId: ticketIdForRun(db, runId, sessionKey),
          sessionKey,
          sessionGeneration: generationFor(path, sessionKey),
          provider: typeof event?.provider === "string" ? event.provider : null,
          model: typeof event?.model === "string" ? event.model : null,
        });
        bindRunId(db, attempt.attemptId, runId);
      } finally { db.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to bridge inference attempt start: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-start" });

  api.on("model_call_ended", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    if (!runId) return;
    try {
      const path = databaseFor(api, ctx);
      const Database = requireDatabaseSync();
      const db = new Database(path);
      try {
        const row = db.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? AND state='active' LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
        if (!row?.attempt_id) return;
        const outcome = text(event?.outcome) || (text(event?.errorCategory) ? `error:${text(event.errorCategory)}` : "model_call_ended");
        finishInferenceAttempt(db, row.attempt_id, outcome);
      } finally { db.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to bridge inference attempt end: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-end" });

  api.on("agent_end", (event: any, ctx: any) => {
    const runId = text(event?.runId ?? ctx?.runId);
    if (!runId) return;
    try {
      const path = databaseFor(api, ctx);
      const Database = requireDatabaseSync();
      const db = new Database(path);
      try {
        const row = db.prepare("SELECT attempt_id FROM cnx_inference_attempt WHERE run_id=? AND state='active' LIMIT 1").get(runId) as { attempt_id?: string } | undefined;
        if (!row?.attempt_id) return;
        finishInferenceAttempt(db, row.attempt_id, event?.success === true ? "agent_end_ok" : "agent_end_error");
      } finally { db.close(); }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw failed to close canonical inference attempt at agent_end: ${error instanceof Error ? error.message : String(error)}`);
    }
  }, { registrationId: "cogentnexus-openclaw-v095-inference-attempt-agent-end" });
}

function ticketIdForRun(db: any, runId: string, sessionKey: string) {
  const row = db.prepare(`SELECT ticket_id FROM tickets
    WHERE run_id=? AND owner_session_key=? AND status='accepted'
      AND workflow_eligible=0 AND workflow_id IS NULL
    ORDER BY created_at DESC LIMIT 1`).get(runId, sessionKey) as { ticket_id?: string } | undefined;
  if (!row?.ticket_id) throw new Error(`accepted Ticket not found for inference run ${runId}`);
  return row.ticket_id;
}

function requireDatabaseSync() {
  // Kept isolated so this bridge cannot accidentally become a lifecycle owner.
  return class DatabaseSync {
    private readonly db: any;
    constructor(path: string) {
      const module = requireNodeSqlite();
      this.db = new module.DatabaseSync(path);
      this.db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
      if (!this.db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_inference_attempt'").get()) {
        throw new Error("canonical inference attempt schema is not installed");
      }
    }
    prepare(sql: string) { return this.db.prepare(sql); }
    close() { this.db.close(); }
  };
}

function requireNodeSqlite() {
  // eslint-compatible runtime import without introducing a second SQLite owner.
  return require("node:sqlite");
}
