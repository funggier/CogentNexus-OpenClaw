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

function setup(allowFrom: Array<string | number>) {
  const root = mkdtempSync(join(tmpdir(), "cnx429-owner-fallback-"));
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
    config: {
      agents: { defaults: { workspace: root } },
      channels: { discord: { allowFrom } },
    },
    on: (name: string, handler: any, options?: any) =>
      hooks.set(name, [...(hooks.get(name) ?? []), { handler, options }]),
    registerService: vi.fn(),
    registerTool: vi.fn(),
    registerGatewayMethod: vi.fn(),
    logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
    session: {
      workflow: {
        unscheduleSessionTurnsByTag: vi.fn(async () => undefined),
        scheduleSessionTurn: vi.fn(async () => undefined),
      },
    },
    runtime: {
      tasks: { managedFlows: {} },
      events: { onSessionTranscriptUpdate: vi.fn() },
    },
  };
  (entry as any).register(api);
  return { root, databasePath, hooks, api };
}

function rows(path: string, sql: string, ...params: any[]) {
  const db = new DatabaseSync(path, { readOnly: true });
  try { return db.prepare(sql).all(...params) as any[]; }
  finally { db.close(); }
}

async function runBeforeAgent(
  hooks: Map<string, RegisteredHook[]>,
  input: { senderId: string; channelId?: string; accountId?: string; sessionKey?: string; runId?: string },
) {
  const sessionKey = input.sessionKey ?? "agent:main:discord:channel:1391855033993138217";
  const event = {
    prompt: "CNX429 Discord owner fallback",
    senderIsOwner: false,
    senderId: input.senderId,
    channelId: input.channelId ?? "discord",
    accountId: input.accountId ?? "default",
  };
  const ctx = {
    sessionKey,
    sessionId: "cnx429-session",
    runId: input.runId ?? "cnx429-run",
  };
  const ordered = [...(hooks.get("before_agent_run") ?? [])]
    .sort((a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0));
  const results: any[] = [];
  for (const item of ordered) results.push(await item.handler(event, ctx));
  return results;
}

describe("CNX-429 Discord exact allowFrom owner fallback", () => {
  it("RED: exact Discord allowFrom sender is Ticket-first eligible when OpenClaw owner bit is false", async () => {
    const owner = "407472087322722318";
    const { databasePath, hooks } = setup([owner]);
    const results = await runBeforeAgent(hooks, { senderId: owner });
    expect(results.some((result) => result?.outcome === "block")).toBe(false);
    expect(rows(databasePath, "SELECT run_id,owner_session_key,prompt FROM tickets")).toEqual([
      {
        run_id: "cnx429-run",
        owner_session_key: "agent:main:discord:channel:1391855033993138217",
        prompt: "CNX429 Discord owner fallback",
      },
    ]);
  });

  it("RED: a different Discord sender remains ineligible", async () => {
    const { databasePath, hooks } = setup(["407472087322722318"]);
    await runBeforeAgent(hooks, { senderId: "999999999999999999" });
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: wildcard allowFrom does not confer owner authority", async () => {
    const { databasePath, hooks } = setup(["*"]);
    await runBeforeAgent(hooks, { senderId: "407472087322722318" });
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: channel identity must match the session namespace", async () => {
    const owner = "407472087322722318";
    const { databasePath, hooks } = setup([owner]);
    await runBeforeAgent(hooks, {
      senderId: owner,
      channelId: "discord",
      sessionKey: "agent:main:cli:test",
    });
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });
});
