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
  const root = mkdtempSync(join(tmpdir(), "cnx424-idempotency-"));
  roots.push(root);
  mkdirSync(join(root, "host"), { recursive: true });
  writeFileSync(
    join(root, "host", "controller.json"),
    JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }),
  );
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
  return { databasePath, hooks };
}

function dispatcher() {
  return {
    sendToolResult: vi.fn(() => true),
    sendBlockReply: vi.fn(() => true),
    sendFinalReply: vi.fn(() => true),
    appendBeforeDeliver: vi.fn(() => undefined),
    waitForIdle: vi.fn(async () => undefined),
    getQueuedCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    getFailedCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    getCancelledCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    markComplete: vi.fn(),
  };
}

async function runReply(
  hooks: Map<string, RegisteredHook[]>,
  input: { runId: string; sourceSessionKey: string; effectiveSessionKey: string; prompt: string },
  dispatchKind: "agent" | "acp",
) {
  const event: any = {
    runId: input.runId,
    sessionKey: input.effectiveSessionKey,
    ctx: {
      SessionKey: input.sourceSessionKey,
      agentText: input.prompt,
      BodyForAgent: input.prompt,
      rawText: input.prompt,
      Body: input.prompt,
      CommandAuthorized: true,
      InboundAccessAuthorized: true,
      GatewayClientScopes: [],
      InputProvenance: { kind: "external_user", sourceChannel: "discord" },
    },
    inboundAudio: false,
    shouldRouteToOriginating: false,
    shouldSendToolSummaries: false,
    shouldSendFullToolDetails: false,
    sendPolicy: "allow",
  };
  const ordered = [...(hooks.get("reply_dispatch") ?? [])].sort(
    (a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0),
  );
  for (const item of ordered) {
    const result = await item.handler(event, {
      cfg: {},
      dispatchKind,
      dispatcher: dispatcher(),
      recordProcessed: vi.fn(),
      markIdle: vi.fn(),
    });
    if (result?.handled === true) break;
  }
}

async function runBeforeAgent(
  hooks: Map<string, RegisteredHook[]>,
  input: { runId: string; sessionKey: string; prompt: string },
) {
  const ordered = [...(hooks.get("before_agent_run") ?? [])].sort(
    (a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0),
  );
  const results: any[] = [];
  for (const item of ordered) {
    results.push(
      await item.handler(
        { prompt: input.prompt, senderIsOwner: true },
        {
          sessionKey: input.sessionKey,
          sessionId: input.runId + "-session",
          runId: input.runId,
          workspaceDir: undefined,
        },
      ),
    );
  }
  return results;
}

function rows(path: string, sql: string) {
  const db = new DatabaseSync(path, { readOnly: true });
  try {
    return db.prepare(sql).all() as any[];
  } finally {
    db.close();
  }
}

const PROMPT = "ตอบกลับว่า CNX-424";

describe("CNX-424 dual-session cross-adapter run idempotency", () => {
  it("RED: bound ACP reply_dispatch then before_agent_run remains one source-owned Ticket", async () => {
    const { databasePath, hooks } = setup();
    const runId = "dual-session-run";
    const source = "agent:main:discord:C123";
    const target = "agent:opencode:acp:bound-session";

    await runReply(
      hooks,
      { runId, sourceSessionKey: source, effectiveSessionKey: target, prompt: PROMPT },
      "acp",
    );
    await runBeforeAgent(hooks, { runId, sessionKey: target, prompt: PROMPT });

    expect(rows(databasePath, "SELECT run_id,owner_session_key FROM tickets ORDER BY created_at,ticket_id")).toEqual([
      { run_id: runId, owner_session_key: source },
    ]);
    expect(rows(databasePath, "SELECT event_type FROM ticket_events WHERE event_type='routed'")).toEqual([
      { event_type: "routed" },
    ]);
  });

  it("same-session reply_dispatch then before_agent_run remains one Ticket", async () => {
    const { databasePath, hooks } = setup();
    const runId = "same-session-run";
    const session = "agent:main:dashboard:same";

    await runReply(
      hooks,
      { runId, sourceSessionKey: session, effectiveSessionKey: session, prompt: PROMPT },
      "agent",
    );
    await runBeforeAgent(hooks, { runId, sessionKey: session, prompt: PROMPT });

    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 1 }]);
    expect(rows(databasePath, "SELECT count(*) AS n FROM ticket_events WHERE event_type='routed'")).toEqual([{ n: 1 }]);
  });

  it("before_agent_run alone still admits when no earlier reply_dispatch admission exists", async () => {
    const { databasePath, hooks } = setup();
    const runId = "before-only-run";
    const session = "agent:main:dashboard:before-only";

    await runBeforeAgent(hooks, { runId, sessionKey: session, prompt: PROMPT });

    expect(rows(databasePath, "SELECT run_id,owner_session_key FROM tickets")).toEqual([
      { run_id: runId, owner_session_key: session },
    ]);
    expect(rows(databasePath, "SELECT count(*) AS n FROM ticket_events WHERE event_type='routed'")).toEqual([{ n: 1 }]);
  });
});
