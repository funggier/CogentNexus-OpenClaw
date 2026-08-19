import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { launchV093DirectRecovery } from "./v093-direct-recovery.js";

type Seed = { path: string; ticketId: string; recovery: any };

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

function successfulApi(captured: { model?: string; deletes: string[] }) {
  let childKey = "";
  return {
    runtime: {
      subagent: {
        getSessionMessages: async ({ sessionKey }: any) => {
          if (sessionKey === "agent:main:dashboard:test") return { messages: [{ role: "user", content: "hello" }] };
          expect(sessionKey).toBe(childKey);
          return { messages: [{ role: "assistant", content: "CNX-LIVE-A-01" }] };
        },
        run: async (input: any) => {
          childKey = input.sessionKey;
          captured.model = input.model;
          return { runId: "recovery-run-1" };
        },
        waitForRun: async () => ({ status: "ok" }),
        deleteSession: async ({ sessionKey }: any) => {
          captured.deletes.push(sessionKey);
          return { deleted: true };
        },
      },
    },
  };
}

describe("v0.9.3 Direct Recovery execution boundary", () => {
  it("preserves the original model and keeps response_ready_at at its first commit", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v093-model-"));
    try {
      const seeded = seed(root);
      const captured: { model?: string; deletes: string[] } = { deletes: [] };
      const api = successfulApi(captured);

      await launchV093DirectRecovery(api, seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });
      expect(captured.model).toBe("qwen3.5:9b");

      let db = new DatabaseSync(seeded.path);
      const first = db.prepare("SELECT response_ready_at,result_json FROM tickets WHERE ticket_id=?")
        .get(seeded.ticketId) as any;
      expect(first.response_ready_at).toBeTruthy();
      expect(JSON.parse(first.result_json).originalModel).toBe("qwen3.5:9b");
      expect(JSON.parse(first.result_json).recoveryModel).toBe("qwen3.5:9b");
      expect(db.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'")
        .get(seeded.ticketId)).toMatchObject({ n: 1 });
      expect(db.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(seeded.ticketId))
        .toMatchObject({ state: "awaiting_delivery" });

      // Re-arm only as a regression fixture. Production v0.9.2 prevents this path,
      // while v0.9.3 itself must still never move the first-ready timestamp.
      db.prepare("UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=NULL WHERE ticket_id=?")
        .run(seeded.ticketId);
      db.close();

      const captured2: { model?: string; deletes: string[] } = { deletes: [] };
      await launchV093DirectRecovery(successfulApi(captured2), seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });

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

  it("deletes the hidden worker and refuses output when durable authority becomes terminal", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v093-terminal-"));
    try {
      const seeded = seed(root);
      const deletes: string[] = [];
      let childKey = "";
      let launched = false;
      const api = {
        runtime: {
          subagent: {
            getSessionMessages: async ({ sessionKey }: any) => {
              if (sessionKey === "agent:main:dashboard:test") return { messages: [] };
              return { messages: [{ role: "assistant", content: "MUST-NOT-DELIVER" }] };
            },
            run: async (input: any) => {
              childKey = input.sessionKey;
              launched = true;
              return { runId: "recovery-run-terminal" };
            },
            waitForRun: async () => await new Promise(() => {}),
            deleteSession: async ({ sessionKey }: any) => {
              deletes.push(sessionKey);
              return { deleted: true };
            },
          },
        },
      };

      const work = launchV093DirectRecovery(api, seeded.path, root, seeded.recovery, { timeoutSeconds: 60 });
      for (let i = 0; i < 50 && !launched; i++) await new Promise((resolve) => setTimeout(resolve, 10));
      expect(launched).toBe(true);

      const db = new DatabaseSync(seeded.path);
      db.prepare("UPDATE tickets SET status='failed',updated_at=? WHERE ticket_id=?")
        .run(new Date().toISOString(), seeded.ticketId);
      db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,last_error='terminal ticket fence',updated_at=? WHERE ticket_id=?")
        .run(new Date().toISOString(), seeded.ticketId);
      db.close();

      await work;
      expect(deletes).toContain(childKey);

      const check = new DatabaseSync(seeded.path, { readOnly: true });
      expect(check.prepare("SELECT COUNT(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=?")
        .get(seeded.ticketId)).toMatchObject({ n: 0 });
      expect(check.prepare("SELECT response_ready_at FROM tickets WHERE ticket_id=?").get(seeded.ticketId))
        .toMatchObject({ response_ready_at: null });
      const abort = check.prepare("SELECT event_type,payload_json FROM ticket_events WHERE ticket_id=? AND event_type='direct_recovery_runtime_aborted' ORDER BY event_id DESC LIMIT 1")
        .get(seeded.ticketId) as any;
      expect(abort?.event_type).toBe("direct_recovery_runtime_aborted");
      expect(JSON.parse(abort.payload_json).reason).toMatch(/ticket-failed|recovery-cancelled/);
      check.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  }, 5000);
});
