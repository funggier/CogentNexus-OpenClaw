import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it, vi } from "vitest";
import entry from "./v091-release-entry.js";

type RegisteredHook = { handler: (event: any, ctx: any) => any; options?: any };

const roots: string[] = [];
afterEach(() => {
  for (const root of roots.splice(0)) rmSync(root, { recursive: true, force: true });
});

function setup() {
  const root = mkdtempSync(join(tmpdir(), "cnx427-discord-runid-"));
  roots.push(root);
  mkdirSync(join(root, "host"), { recursive: true });
  writeFileSync(join(root, "host", "controller.json"), JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }));
  const databasePath = join(root, "tickets.sqlite3");
  const hooks = new Map<string, RegisteredHook[]>();
  const api: any = {
    pluginConfig: {
      cogentNexusOpenClawRoot: root,
      workspaceDir: root,
      ticketDatabasePath: databasePath,
      ticketFirst: true,
      preInferenceAdmission: true,
      autoWorkflowCompletion: false,
      autoResume: false,
    },
    config: { agents: { defaults: { workspace: root } } },
    on: (name: string, handler: any, options?: any) => hooks.set(name, [...(hooks.get(name) ?? []), { handler, options }]),
    registerService: vi.fn(),
    registerTool: vi.fn(),
    registerGatewayMethod: vi.fn(),
    logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
    session: { workflow: { unscheduleSessionTurnsByTag: vi.fn(async () => undefined), scheduleSessionTurn: vi.fn(async () => undefined) } },
    runtime: { tasks: { managedFlows: {} }, events: { onSessionTranscriptUpdate: vi.fn() } },
  };
  (entry as any).register(api);
  return { root, databasePath, hooks, api };
}

function discordEvent(prompt: string, options: { runId?: string; authorized?: boolean; sessionKey?: string } = {}) {
  const sessionKey = options.sessionKey ?? "agent:main:discord:channel:1391855033993138217";
  return {
    runId: options.runId,
    sessionKey,
    ctx: {
      SessionKey: sessionKey,
      agentText: prompt,
      BodyForAgent: prompt,
      rawText: prompt,
      Body: prompt,
      InboundAccessAuthorized: options.authorized ?? true,
      GatewayClientScopes: [],
      Provider: "discord",
      Surface: "discord",
      OriginatingChannel: "discord",
      ChatType: "channel",
    },
  };
}

function dispatcher() {
  return {
    sendFinalReply: vi.fn(() => true),
    appendBeforeDeliver: vi.fn(),
    waitForIdle: vi.fn(async () => undefined),
    getQueuedCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    getFailedCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    getCancelledCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
  };
}

async function runReply(hooks: Map<string, RegisteredHook[]>, event: any) {
  const ctx: any = { dispatchKind: "agent", dispatcher: dispatcher() };
  const ordered = [...(hooks.get("reply_dispatch") ?? [])].sort((a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0));
  let claimed: any;
  for (const item of ordered) {
    const result = await item.handler(event, ctx);
    if (result?.handled === true) {
      claimed = result;
      break;
    }
  }
  return claimed;
}

async function runBeforeAgent(hooks: Map<string, RegisteredHook[]>, prompt: string, ctx: any) {
  const ordered = [...(hooks.get("before_agent_run") ?? [])].sort((a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0));
  const results: any[] = [];
  for (const item of ordered) results.push(await item.handler({ prompt, senderIsOwner: true }, ctx));
  return results;
}

function rows(path: string, sql: string, ...params: any[]) {
  const db = new DatabaseSync(path, { readOnly: true });
  try { return db.prepare(sql).all(...params) as any[]; }
  finally { db.close(); }
}

const DIRECT = "Discord CNX-427 direct ingress";

describe("CNX-427 external ingress run identity deferral", () => {
  it("RED: trusted Discord reply_dispatch without runId defers instead of claiming the turn", async () => {
    const { databasePath, hooks } = setup();
    const claimed = await runReply(hooks, discordEvent(DIRECT));
    expect(claimed).toBeUndefined();
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: later authoritative before_agent_run creates exactly one Ticket", async () => {
    const { databasePath, hooks } = setup();
    const sessionKey = "agent:main:discord:channel:1391855033993138217";
    await runReply(hooks, discordEvent(DIRECT, { sessionKey }));
    const results = await runBeforeAgent(hooks, DIRECT, {
      sessionKey,
      sessionId: "discord-session",
      runId: "discord-authoritative-run",
    });
    expect(results.some((result) => result?.outcome === "block")).toBe(false);
    expect(rows(databasePath, "SELECT run_id,owner_session_key,prompt FROM tickets")).toEqual([
      { run_id: "discord-authoritative-run", owner_session_key: sessionKey, prompt: DIRECT },
    ]);
  });

  it("RED: early runId path plus before_agent_run remains exactly one Ticket", async () => {
    const { databasePath, hooks } = setup();
    const sessionKey = "agent:main:discord:channel:1391855033993138217";
    await runReply(hooks, discordEvent(DIRECT, { runId: "discord-known-run", sessionKey }));
    await runBeforeAgent(hooks, DIRECT, { sessionKey, sessionId: "discord-session", runId: "discord-known-run" });
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 1 }]);
  });

  it("RED: untrusted ingress is still fail-closed even when runId is absent", async () => {
    const { databasePath, hooks, api } = setup();
    const claimed = await runReply(hooks, discordEvent(DIRECT, { authorized: false }));
    expect(claimed).toMatchObject({ handled: true });
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(api.logger.warn).toHaveBeenCalledWith(expect.stringContaining("untrusted-ingress"));
  });

  it("RED: execution boundary still fails closed if authoritative runId is absent", async () => {
    const { hooks } = setup();
    const results = await runBeforeAgent(hooks, DIRECT, {
      sessionKey: "agent:main:discord:channel:1391855033993138217",
      sessionId: "discord-session",
    });
    expect(results).toContainEqual(expect.objectContaining({
      outcome: "block",
      category: "cnxclaw_ticket_admission_integrity",
      metadata: { reason: "missing-run-id" },
    }));
  });
});
