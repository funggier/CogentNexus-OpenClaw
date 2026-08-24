import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { launchV094DirectRecovery } from "./v094-direct-recovery.js";

type Seed = { path: string; ticketId: string; recovery: any };
type Capture = {
  provider?: string;
  model?: string;
  modelFallbacksOverride?: unknown;
  disableTools?: boolean;
  disableMessageTool?: boolean;
  aborted?: boolean;
  runId?: string;
};

function seed(root: string): Seed {
  const path = join(root, "tickets.sqlite3");
  const store = new TicketStore(path);
  const ticket = store.accept({
    runId: "run-owner",
    ownerSessionKey: "agent:main:dashboard:test",
    prompt: "hello",
  });
  const db = new DatabaseSync(path);
  const stamp = new Date("2026-08-20T00:00:00.000Z").toISOString();
  db.prepare("UPDATE tickets SET workflow_eligible=0 WHERE ticket_id=?").run(ticket.ticketId);
  db.exec(`
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT NOT NULL,
      state TEXT NOT NULL,
      attempt_count INTEGER NOT NULL,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      owner_generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE cnx_assistant_delivery(
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id TEXT,
      owner_session_key TEXT NOT NULL,
      owner_generation INTEGER NOT NULL,
      kind TEXT NOT NULL,
      text TEXT NOT NULL,
      target_json TEXT,
      idempotency_key TEXT NOT NULL UNIQUE,
      status TEXT NOT NULL,
      attempt_count INTEGER NOT NULL,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      delivered_at TEXT
    );
    CREATE TABLE cnx_direct_model_call(
      ticket_id TEXT PRIMARY KEY,
      run_id TEXT NOT NULL,
      call_id TEXT NOT NULL,
      state TEXT NOT NULL,
      provider TEXT,
      model TEXT,
      started_at TEXT NOT NULL,
      deadline_at TEXT NOT NULL,
      ended_at TEXT,
      outcome TEXT,
      duration_ms INTEGER,
      recovery_started_at TEXT,
      recovery_attempt_count INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL
    );
  `);
  db.prepare("INSERT INTO cnx_sessions VALUES (?,?,?)")
    .run("agent:main:dashboard:test", "active", 0);
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
      owner_generation,created_at,updated_at
    ) VALUES (?,'resume','pending',0,NULL,NULL,NULL,0,?,?)`)
    .run(ticket.ticketId, stamp, stamp);
  db.prepare(`INSERT INTO cnx_direct_model_call(
      ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,
      ended_at,outcome,duration_ms,recovery_started_at,recovery_attempt_count,updated_at
    ) VALUES (?,?,?,'recovering','ollama','qwen3.5:9b',?,?,NULL,NULL,NULL,?,1,?)`)
    .run(ticket.ticketId, "run-owner", "call-owner", stamp, new Date("2026-08-20T00:15:00.000Z").toISOString(), stamp, stamp);
  db.close();
  return {
    path,
    ticketId: ticket.ticketId,
    recovery: {
      ticket_id: ticket.ticketId,
      owner_session_key: "agent:main:dashboard:test",
      prompt: "hello",
      mode: "resume",
      attempt_count: 0,
      owner_generation: 0,
    },
  };
}

function ownerMessages() {
  return {
    getSessionMessages: async ({ sessionKey }: any) => {
      expect(sessionKey).toBe("agent:main:dashboard:test");
      return { messages: [{ role: "user", content: "hello" }] };
    },
  };
}

function successfulApi(captured: Capture, actualModel = "qwen3.5:9b") {
  return {
    config: {},
    runtime: {
      config: { current: () => ({}) },
      subagent: ownerMessages(),
      agent: {
        runEmbeddedAgent: async (input: any) => {
          captured.provider = input.provider;
          captured.model = input.model;
          captured.modelFallbacksOverride = input.modelFallbacksOverride;
          captured.disableTools = input.disableTools;
          captured.disableMessageTool = input.disableMessageTool;
          captured.runId = input.runId;
          input.onExecutionPhase?.({
            phase: "model",
            provider: "ollama",
            model: actualModel,
            backend: "openclaw",
            firstModelCallStarted: true,
          });
          return {
            meta: {
              durationMs: 25,
              finalAssistantVisibleText: "CNX-LIVE-A-01",
              agentMeta: {
                sessionId: input.sessionId,
                provider: "ollama",
                model: actualModel,
                agentHarnessId: "openclaw",
              },
              executionTrace: { runner: "embedded" },
            },
            payloads: [{ text: "CNX-LIVE-A-01" }],
          };
        },
      },
    },
  };
}

describe("v0.9.4 embedded Direct Recovery boundary", () => {
  it("pins original provider/model with no fallback, records actual runtime, and preserves first response_ready_at", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v094-model-"));
    try {
      const seeded = seed(root);
      const captured: Capture = {};
      await launchV094DirectRecovery(successfulApi(captured), seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });

      expect(captured.provider).toBe("ollama");
      expect(captured.model).toBe("qwen3.5:9b");
      expect(captured.modelFallbacksOverride).toEqual([]);
      expect(captured.disableTools).toBe(true);
      expect(captured.disableMessageTool).toBe(true);
      expect(captured.runId).toMatch(/^cnxclaw-direct-/u);

      let db = new DatabaseSync(seeded.path);
      const first = db.prepare("SELECT response_ready_at,result_json FROM tickets WHERE ticket_id=?")
        .get(seeded.ticketId) as any;
      expect(first.response_ready_at).toBeTruthy();
      const result = JSON.parse(first.result_json);
      expect(result.originalProvider).toBe("ollama");
      expect(result.originalModel).toBe("qwen3.5:9b");
      expect(result.recoveryProvider).toBe("ollama");
      expect(result.recoveryModel).toBe("qwen3.5:9b");
      expect(result.recoveryHarness).toBe("openclaw");
      expect(result.recoveryExecution).toBe("embedded-agent");
      expect(db.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'")
        .get(seeded.ticketId)).toMatchObject({ n: 1 });
      expect(db.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(seeded.ticketId))
        .toMatchObject({ state: "awaiting_delivery" });

      const started = db.prepare("SELECT payload_json FROM ticket_events WHERE ticket_id=? AND event_type='direct_recovery_runtime_started' ORDER BY event_id DESC LIMIT 1")
        .get(seeded.ticketId) as any;
      const startedPayload = JSON.parse(started.payload_json);
      expect(startedPayload.requestedProvider).toBe("ollama");
      expect(startedPayload.requestedModel).toBe("qwen3.5:9b");
      expect(startedPayload.runtimeProvider).toBe("ollama");
      expect(startedPayload.runtimeModel).toBe("qwen3.5:9b");
      expect(startedPayload.execution).toBe("embedded-agent");

      db.prepare("UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=NULL WHERE ticket_id=?")
        .run(seeded.ticketId);
      db.close();

      await launchV094DirectRecovery(successfulApi({}), seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });
      db = new DatabaseSync(seeded.path, { readOnly: true });
      const second = db.prepare("SELECT response_ready_at FROM tickets WHERE ticket_id=?").get(seeded.ticketId) as any;
      expect(second.response_ready_at).toBe(first.response_ready_at);
      expect(db.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'")
        .get(seeded.ticketId)).toMatchObject({ n: 1 });
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("aborts embedded inference and refuses output when durable authority becomes terminal", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v094-terminal-"));
    try {
      const seeded = seed(root);
      const captured: Capture = {};
      let launched = false;
      const api = {
        config: {},
        runtime: {
          config: { current: () => ({}) },
          subagent: ownerMessages(),
          agent: {
            runEmbeddedAgent: async (input: any) => {
              launched = true;
              input.onExecutionPhase?.({ phase: "model", provider: "ollama", model: "qwen3.5:9b", backend: "openclaw" });
              return await new Promise((resolve, reject) => {
                input.abortSignal.addEventListener("abort", () => {
                  captured.aborted = true;
                  reject(new Error("aborted by durable authority fence"));
                }, { once: true });
              });
            },
          },
        },
      };

      const work = launchV094DirectRecovery(api, seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });
      for (let i = 0; i < 50 && !launched; i++) await new Promise((resolve) => setTimeout(resolve, 10));
      expect(launched).toBe(true);

      const db = new DatabaseSync(seeded.path);
      db.prepare("UPDATE tickets SET status='failed',updated_at=? WHERE ticket_id=?")
        .run(new Date().toISOString(), seeded.ticketId);
      db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,last_error='terminal ticket fence',updated_at=? WHERE ticket_id=?")
        .run(new Date().toISOString(), seeded.ticketId);
      db.close();

      await work;
      expect(captured.aborted).toBe(true);

      const check = new DatabaseSync(seeded.path, { readOnly: true });
      expect(check.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?")
        .get(seeded.ticketId)).toMatchObject({ n: 0 });
      expect(check.prepare("SELECT response_ready_at FROM tickets WHERE ticket_id=?").get(seeded.ticketId))
        .toMatchObject({ response_ready_at: null });
      const abort = check.prepare("SELECT payload_json FROM ticket_events WHERE ticket_id=? AND event_type='direct_recovery_runtime_aborted' ORDER BY event_id DESC LIMIT 1")
        .get(seeded.ticketId) as any;
      const abortPayload = JSON.parse(abort.payload_json);
      expect(abortPayload.reason).toMatch(/ticket-failed|recovery-cancelled/);
      expect(abortPayload.abortSettled).toBe(true);
      expect(abortPayload.execution).toBe("embedded-agent");
      check.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  }, 5000);

  it("fails closed if the embedded runtime substitutes a different model", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v094-drift-"));
    try {
      const seeded = seed(root);
      await launchV094DirectRecovery(successfulApi({}, "qwen3.8:27b"), seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });

      const db = new DatabaseSync(seeded.path, { readOnly: true });
      expect(db.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?")
        .get(seeded.ticketId)).toMatchObject({ n: 0 });
      expect(db.prepare("SELECT response_ready_at FROM tickets WHERE ticket_id=?").get(seeded.ticketId))
        .toMatchObject({ response_ready_at: null });
      const recovery = db.prepare("SELECT state,attempt_count,last_error FROM cnx_direct_recovery WHERE ticket_id=?")
        .get(seeded.ticketId) as any;
      expect(recovery.state).toBe("pending");
      expect(recovery.attempt_count).toBe(1);
      expect(recovery.last_error).toMatch(/model drifted/u);
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
