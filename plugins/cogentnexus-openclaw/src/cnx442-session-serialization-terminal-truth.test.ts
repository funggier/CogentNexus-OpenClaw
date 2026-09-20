import { afterEach, describe, expect, it, vi } from "vitest";
import { DatabaseSync } from "node:sqlite";
import { join } from "node:path";
import { existsSync, mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { replyDispatchNativeCommandExcluded } from "./ticket-admission-kernel.js";
import {
  enforceOwnerSessionFollowupQueue,
  ownerConversationSessionEligible,
} from "./v095-session-serialization.js";
import { readHostRunTerminalEvidence, resolveHostAgentDatabasePath, scheduleHostRunTerminalReconcile } from "./v095-host-terminal-evidence.js";
import { TicketStore } from "./ticket-store.js";
import { retireHistoricalNativeCommandTickets } from "./v095-native-command-retirement.js";
import entry from "./index.js";

afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); });

function ensureCommandRetirementEvidenceTables(db: DatabaseSync) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_direct_model_call(
      call_id TEXT PRIMARY KEY,
      ticket_id TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_inference_attempt(
      attempt_id TEXT PRIMARY KEY,
      ticket_id TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_assistant_delivery(
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id TEXT,
      status TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT,
      state TEXT
    );
  `);
}

function bestEffortRemove(path: string) {
  try { rmSync(path, { recursive: true, force: true, maxRetries: 10, retryDelay: 50 }); } catch { /* Windows may retain SQLite handles until worker exit. */ }
}

describe("CNX-442 session serialization and terminal truth", () => {
  it.each([
    ["discord", "agent:main:discord:channel:1391855033993138217"],
    ["dashboard", "agent:main:dashboard:main"],
    ["webchat/generic", "agent:main:webchat:conversation-1"],
  ])("bypasses host-native /context before Ticket admission on %s", (_surface, sessionKey) => {
    const cfg = { commands: { native: "auto" } };
    const event = {
      sessionKey,
      ctx: {
        SessionKey: sessionKey,
        InboundEventKind: "slash-command",
        CommandAuthorized: true,
        CommandBody: "/context",
        BodyForAgent: "/context",
        RawBody: "/context",
      },
    };
    expect(replyDispatchNativeCommandExcluded(event, { cfg })).toBe(true);
  });

  it("does not create a Ticket when reply_dispatch receives an authorized native command", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-command-bypass-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const admission = hooks.get("reply_dispatch")?.[0];
      expect(admission).toBeTypeOf("function");
      const sessionKey = "agent:main:dashboard:main";
      await admission({
        runId: "command-run",
        sessionKey,
        ctx: {
          SessionKey: sessionKey,
          InboundEventKind: "slash-command",
          CommandAuthorized: true,
          CommandBody: "/context",
          BodyForAgent: "/context",
          RawBody: "/context",
          InboundAccessAuthorized: true,
        },
      }, { cfg: {}, dispatchKind: "agent", dispatcher: {} });
      if (existsSync(databasePath)) {
        const db = new DatabaseSync(databasePath, { readOnly: true });
        expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({ n: 0 });
        db.close();
      }
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not treat unknown slash-looking conversational text as a native command without host command facts", () => {
    const event = {
      sessionKey: "agent:main:dashboard:main",
      ctx: {
        SessionKey: "agent:main:dashboard:main",
        InboundEventKind: "message",
        CommandAuthorized: false,
        BodyForAgent: "/this-is-user-text please explain it",
        RawBody: "/this-is-user-text please explain it",
      },
    };
    expect(replyDispatchNativeCommandExcluded(event, { cfg: {} })).toBe(false);
  });

  it("applies followup queue policy through the supported OpenClaw session API without channel special-casing", async () => {
    const entries = new Map<string, any>([
      ["agent:main:discord:channel:1", { sessionId: "d1", queueMode: "steer" }],
      ["agent:main:dashboard:main", { sessionId: "w1" }],
      ["agent:main:webchat:conversation-1", { sessionId: "x1", queueMode: "collect" }],
    ]);
    const patches: string[] = [];
    const sessionApi = {
      resolveStorePath: (_store?: string, opts?: { agentId?: string }) => `/state/agents/${opts?.agentId}/agent/openclaw-agent.sqlite`,
      getSessionEntry: ({ sessionKey }: { sessionKey: string }) => entries.get(sessionKey),
      patchSessionEntry: async ({ sessionKey, update }: any) => {
        const current = entries.get(sessionKey);
        const patch = await update(current, { existingEntry: current });
        entries.set(sessionKey, { ...current, ...patch });
        patches.push(sessionKey);
        return entries.get(sessionKey);
      },
    };
    const api: any = { runtime: { agent: { session: sessionApi } } };

    for (const key of entries.keys()) {
      expect(ownerConversationSessionEligible(key)).toBe(true);
      await expect(enforceOwnerSessionFollowupQueue(api, key)).resolves.toMatchObject({ state: "updated", queueMode: "followup" });
      expect(entries.get(key).queueMode).toBe("followup");
    }
    expect(patches).toEqual([...entries.keys()]);
  });

  it("does not apply owner followup serialization to subagent/internal session keys", () => {
    expect(ownerConversationSessionEligible("agent:main:subagent:worker-1")).toBe(false);
    expect(ownerConversationSessionEligible("agent:main:cron:job-1")).toBe(false);
    expect(ownerConversationSessionEligible("agent:main:cogent-rotate-task")).toBe(false);
  });

  it("retires only stranded historical native-command Tickets with zero execution or delivery evidence", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-retirement-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const old = new Date("2026-09-20T07:36:00Z");
      const a = store.accept({ runId:"run-context", ownerSessionKey:"agent:main:discord:channel:1", prompt:"/context" });
      store.route(a.ticketId, false, old);
      const b = store.accept({ runId:"run-context-detail", ownerSessionKey:"agent:main:dashboard:main", prompt:"/context detail" });
      store.route(b.ticketId, false, old);
      const ordinary = store.accept({ runId:"run-ordinary", ownerSessionKey:"agent:main:webchat:1", prompt:"/this-is-user-text please explain it" });
      store.route(ordinary.ticketId, false, old);

      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id IN (?,?,?)")
        .run(old.toISOString(),old.toISOString(),a.ticketId,b.ticketId,ordinary.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: { commands:{ native:"auto" } },
        now: new Date("2026-09-20T07:40:00Z"),
        minAgeMs: 60_000,
      });
      expect(result).toMatchObject({ retired:2, skippedForEvidence:0, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a.ticketId)).toEqual({status:"cancelled"});
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(b.ticketId)).toEqual({status:"cancelled"});
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ordinary.ticketId)).toEqual({status:"accepted"});
      expect(check.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE event_type='native_command_ticket_retired'").get()).toEqual({n:2});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not retire a native-command Ticket once execution evidence exists", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-evidence-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const old = new Date("2026-09-20T07:36:00Z");
      const ticket = store.accept({ runId:"run-context-evidence", ownerSessionKey:"agent:main:discord:channel:1", prompt:"/context" });
      store.route(ticket.ticketId, false, old);

      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id=?")
        .run(old.toISOString(),old.toISOString(),ticket.ticketId);
      db.prepare("INSERT INTO cnx_direct_model_call(call_id,ticket_id) VALUES (?,?)").run("call-1",ticket.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: {},
        now: new Date("2026-09-20T07:40:00Z"),
      });
      expect(result).toMatchObject({ retired:0, skippedForEvidence:1, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({status:"accepted"});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not retire a fresh native-command Ticket inside the bounded migration age", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-fresh-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const fresh = new Date("2026-09-20T07:39:30Z");
      const ticket = store.accept({ runId:"run-context-fresh", ownerSessionKey:"agent:main:dashboard:main", prompt:"/context" });
      store.route(ticket.ticketId, false, fresh);
      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id=?")
        .run(fresh.toISOString(),fresh.toISOString(),ticket.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: {},
        now: new Date("2026-09-20T07:40:00Z"),
        minAgeMs: 60_000,
      });
      expect(result).toMatchObject({ retired:0, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({status:"accepted"});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("reads authoritative host terminal error evidence by exact run id", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-terminal-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      const db = new DatabaseSync(dbPath);
      db.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      db.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-1",
        9,
        "run-failed",
        JSON.stringify({
          type: "session.ended",
          runId: "run-failed",
          data: { status: "error", stopReason: "error", aborted: false, timedOut: false },
        }),
        1,
      );
      db.close();

      expect(readHostRunTerminalEvidence({ databasePath: dbPath, runId: "run-failed" })).toMatchObject({
        state: "terminal",
        status: "error",
        runId: "run-failed",
      });
      expect(readHostRunTerminalEvidence({ databasePath: dbPath, runId: "other-run" })).toEqual({ state: "pending" });
    } finally {
      bestEffortRemove(root);
    }
  });

  it("resolves terminal evidence from openclaw-agent.sqlite rather than the legacy sessions.json store", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-db-path-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      new DatabaseSync(dbPath).close();
      const api: any = {
        config: {},
        runtime: { agent: {
          resolveAgentDir: () => root,
          session: { resolveStorePath: () => join(root, "sessions.json") },
        } },
      };
      expect(resolveHostAgentDatabasePath(api, "agent:main:dashboard:main")).toBe(dbPath);
    } finally {
      bestEffortRemove(root);
    }
  });

  it("schedules host terminal reconciliation after agent_end can return", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-reconcile-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      const db = new DatabaseSync(dbPath);
      db.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      db.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-2",
        1,
        "run-error",
        JSON.stringify({ type: "session.ended", runId: "run-error", data: { status: "error", stopReason: "error" } }),
        2,
      );
      db.close();

      const onTerminal = vi.fn();
      const api: any = {
        config: {},
        runtime: { agent: {
          resolveAgentDir: () => root,
          session: { resolveStorePath: () => join(root, "sessions.json") },
        } },
      };
      const scheduled = scheduleHostRunTerminalReconcile({
        api,
        sessionKey: "agent:main:dashboard:main",
        runId: "run-error",
        delayMs: 100,
        pollMs: 50,
        maxAttempts: 2,
        onTerminal,
      });
      expect(scheduled.scheduled).toBe(true);
      await vi.advanceTimersByTimeAsync(100);
      expect(onTerminal).toHaveBeenCalledTimes(1);
      expect(onTerminal.mock.calls[0][0]).toMatchObject({ state: "terminal", status: "error", runId: "run-error" });
      scheduled.cancel();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("settles a silent direct Ticket only after authoritative Host success", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-silent-success-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const agentDir = join(root, "agent");
      const dbPath = join(agentDir, "openclaw-agent.sqlite");
      mkdirSync(agentDir, { recursive: true });
      const host = new DatabaseSync(dbPath);
      host.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      host.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-success", 1, "run-silent",
        JSON.stringify({ type:"session.ended", runId:"run-silent", data:{ status:"success", stopReason:"stop" } }),
        1,
      );
      host.close();

      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { agent:{ resolveAgentDir:()=>agentDir }, tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:silent", runId: "run-silent", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "silent user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);

      let db = new DatabaseSync(databasePath, { readOnly: true });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId)).toEqual({
        status:"accepted", delivery_confirmed_at:null,
      });
      db.close();

      await vi.advanceTimersByTimeAsync(150);

      db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).toBe("completed");
      expect(row.response_ready_at).toEqual(expect.any(String));
      expect(row.delivery_confirmed_at).toEqual(expect.any(String));
      const events=(db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=(SELECT ticket_id FROM tickets WHERE run_id=?) ORDER BY event_id").all(owner.runId) as any[]).map(x=>x.event_type);
      expect(events).toEqual(["accepted","routed","response_ready","delivery_confirmed","completed"]);
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("retracts response_ready and promotes recovery when authoritative Host terminal is error", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-error-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const agentDir = join(root, "agent");
      const dbPath = join(agentDir, "openclaw-agent.sqlite");
      mkdirSync(agentDir, { recursive: true });
      const host = new DatabaseSync(dbPath);
      host.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      host.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-error", 1, "run-host-error",
        JSON.stringify({ type:"session.ended", runId:"run-host-error", data:{ status:"error", stopReason:"error" } }),
        1,
      );
      host.close();

      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { agent:{ resolveAgentDir:()=>agentDir }, tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:error", runId: "run-host-error", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);
      await vi.advanceTimersByTimeAsync(150);

      const db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,workflow_eligible,response_ready_at,delivery_confirmed_at,failure_class FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).not.toBe("completed");
      expect(row.response_ready_at).toBeNull();
      expect(row.delivery_confirmed_at).toBeNull();
      expect(row.failure_class).toBe("interrupted");
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("never completes a ticketed conversational run merely because agent_end had no visible output", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-terminal-ticket-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:main", runId: "run-race", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);

      const db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).toBe("accepted");
      expect(row.response_ready_at).toEqual(expect.any(String));
      expect(row.delivery_confirmed_at).toBeNull();
      expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=(SELECT ticket_id FROM tickets WHERE run_id=?) ORDER BY event_id").all(owner.runId) as any[]).map(x=>x.event_type))
        .toEqual(["accepted","routed","response_ready"]);
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });
});