import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installContextGuard } from "./v091-context-guard.js";

describe("v0.9.7 Direct recovery context isolation", () => {
  it("does not let owner-session context pressure revoke a running Direct recovery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v097-context-recovery-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:main";
      const store = new TicketStore(databasePath);
      const ticket = store.accept({
        runId: "original-run",
        ownerSessionKey: sessionKey,
        prompt: "Reply with exactly RECOVERY_OK and nothing else.",
      });
      store.route(ticket.ticketId, false);

      const recoveryRunId = `cnxclaw-direct-${ticket.ticketId}-1-g0`;
      const db = new DatabaseSync(databasePath);
      const stamp = new Date().toISOString();
      db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
        session_key TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        generation INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        deleted_at TEXT,
        delete_reason TEXT
      );
      CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
        ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
        mode TEXT NOT NULL DEFAULT 'resume',
        state TEXT NOT NULL DEFAULT 'pending',
        attempt_count INTEGER NOT NULL DEFAULT 0,
        active_run_id TEXT,
        next_attempt_at TEXT,
        last_error TEXT,
        owner_generation INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );`);
      db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',0,?,?)")
        .run(sessionKey, stamp, stamp);
      db.prepare(`INSERT INTO cnx_direct_recovery(
        ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
        owner_generation,created_at,updated_at
      ) VALUES (?,'resume','running',1,?,NULL,NULL,0,?,?)`)
        .run(ticket.ticketId, recoveryRunId, stamp, stamp);
      db.close();

      let hook: any;
      const registration = {
        on: (name: string, fn: any) => { if (name === "before_agent_run") hook = fn; },
        registerService: () => {},
      };
      const api = {
        runtime: {
          gateway: {
            request: async (method: string) => {
              if (method === "sessions.describe") {
                return {
                  session: {
                    key: sessionKey,
                    sessionId: "owner-physical-session",
                    contextTokens: 24576,
                    totalTokens: 17216,
                    totalTokensFresh: true,
                  },
                };
              }
              throw new Error(`unexpected ${method}`);
            },
          },
        },
        logger: { info: () => {}, warn: () => {} },
      };

      installContextGuard(api, registration, {
        workspaceDir: root,
        ticketDatabasePath: databasePath,
      });

      const decision = await hook(
        { prompt: "recovery prompt", messages: [], systemPrompt: "" },
        {
          sessionKey,
          runId: recoveryRunId,
          contextTokenBudget: 24576,
          workspaceDir: root,
        },
      );

      expect(decision).toEqual({ outcome: "pass" });
      const check = new DatabaseSync(databasePath, { readOnly: true });
      expect(check.prepare(
        "SELECT state,attempt_count,active_run_id,next_attempt_at,last_error FROM cnx_direct_recovery WHERE ticket_id=?",
      ).get(ticket.ticketId)).toEqual({
        state: "running",
        attempt_count: 1,
        active_run_id: recoveryRunId,
        next_attempt_at: null,
        last_error: null,
      });
      expect(check.prepare(
        "SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='context_pressure_deferred'",
      ).get(ticket.ticketId)).toEqual({ n: 0 });
      check.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
