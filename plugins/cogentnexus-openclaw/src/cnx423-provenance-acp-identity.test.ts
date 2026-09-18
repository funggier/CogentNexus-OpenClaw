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
  const root = mkdtempSync(join(tmpdir(), "cnx423-admission-"));
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
  return { root, databasePath, hooks, api };
}

function dispatcher() {
  const final: any[] = [];
  return {
    final,
    sendToolResult: vi.fn(() => true),
    sendBlockReply: vi.fn(() => true),
    sendFinalReply: vi.fn((payload: any) => {
      final.push(payload);
      return true;
    }),
    appendBeforeDeliver: vi.fn(() => undefined),
    waitForIdle: vi.fn(async () => undefined),
    getQueuedCounts: vi.fn(() => ({ tool: 0, block: 0, final: final.length })),
    getFailedCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    getCancelledCounts: vi.fn(() => ({ tool: 0, block: 0, final: 0 })),
    markComplete: vi.fn(),
  };
}

function event(input: {
  prompt?: string;
  runId?: string;
  eventSessionKey?: string;
  sourceSessionKey?: string;
  authorized?: boolean;
  scopes?: string[];
  provenance?: { kind: string; sourceTool?: string; sourceSessionKey?: string; sourceChannel?: string };
  internalTurnSource?: string;
}) {
  const prompt = input.prompt ?? "ตอบกลับว่า CNX-423";
  const sourceSessionKey = input.sourceSessionKey ?? "agent:main:dashboard:source";
  const eventSessionKey = input.eventSessionKey ?? sourceSessionKey;
  return {
    runId: input.runId ?? "cnx423-run",
    sessionKey: eventSessionKey,
    provider: "openai",
    model: "gpt-5.6-luna",
    harnessId: "codex",
    ctx: {
      SessionKey: sourceSessionKey,
      commandText: prompt,
      agentText: prompt,
      rawText: prompt,
      Body: prompt,
      BodyForAgent: prompt,
      CommandAuthorized: true,
      InboundAccessAuthorized: input.authorized,
      GatewayClientScopes: input.scopes ?? [],
      InputProvenance: input.provenance,
      InternalTurnSource: input.internalTurnSource,
      Provider: "internal",
      Surface: "internal",
      ChatType: "direct",
    },
    inboundAudio: false,
    shouldRouteToOriginating: false,
    shouldSendToolSummaries: false,
    shouldSendFullToolDetails: false,
    sendPolicy: "allow",
  };
}

async function runReply(
  hooks: Map<string, RegisteredHook[]>,
  replyEvent: any,
  dispatchKind: "agent" | "acp" = "agent",
) {
  const d = dispatcher();
  const ctx: any = {
    cfg: {},
    dispatchKind,
    dispatcher: d,
    recordProcessed: vi.fn(),
    markIdle: vi.fn(),
  };
  const ordered = [...(hooks.get("reply_dispatch") ?? [])].sort(
    (a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0),
  );
  let claimed: any;
  for (const item of ordered) {
    const result = await item.handler(replyEvent, ctx);
    if (result?.handled === true) {
      claimed = result;
      break;
    }
  }
  return { claimed, event: replyEvent, ctx, dispatcher: d };
}

function rows(path: string, sql: string, ...params: any[]) {
  const db = new DatabaseSync(path, { readOnly: true });
  try {
    return db.prepare(sql).all(...params) as any[];
  } finally {
    db.close();
  }
}

describe("CNX-423 reply_dispatch provenance and ACP identity semantics", () => {
  it("RED: restart-sentinel internal recovery with operator.admin is excluded", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "restart-sentinel-run",
        scopes: ["operator.admin"],
        provenance: { kind: "internal_system", sourceTool: "restart-sentinel" },
      }),
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toBeUndefined();
  });

  it("RED: generic internal_system provenance is excluded", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "internal-system-run",
        authorized: true,
        provenance: { kind: "internal_system", sourceTool: "system-control" },
      }),
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toBeUndefined();
  });

  it("RED: explicit InternalTurnSource is excluded", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "cron-control-run",
        scopes: ["operator.admin"],
        internalTurnSource: "cron",
      }),
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toBeUndefined();
  });

  it("RED: inter_session subagent completion into owner session is excluded", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "subagent-completion-run",
        authorized: true,
        sourceSessionKey: "agent:main:dashboard:owner",
        eventSessionKey: "agent:main:dashboard:owner",
        provenance: {
          kind: "inter_session",
          sourceTool: "subagent_announce",
          sourceSessionKey: "agent:main:subagent:worker",
          sourceChannel: "internal",
        },
      }),
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toBeUndefined();
  });

  it("RED: bound ACP retarget uses source owner for Ticket and leaves effective target untouched", async () => {
    const { databasePath, hooks } = setup();
    const sourceSessionKey = "agent:main:discord:C123";
    const effectiveAcpSessionKey = "agent:opencode:acp:bound-session";
    const replyEvent = event({
      runId: "bound-acp-run",
      sourceSessionKey,
      eventSessionKey: effectiveAcpSessionKey,
      authorized: true,
      provenance: { kind: "external_user", sourceChannel: "discord" },
    });
    const before = JSON.stringify({
      sessionKey: replyEvent.sessionKey,
      ctxSessionKey: replyEvent.ctx.SessionKey,
      provider: replyEvent.provider,
      model: replyEvent.model,
      harnessId: replyEvent.harnessId,
    });
    const result = await runReply(hooks, replyEvent, "acp");
    expect(rows(databasePath, "SELECT run_id,owner_session_key FROM tickets")).toEqual([
      { run_id: "bound-acp-run", owner_session_key: sourceSessionKey },
    ]);
    expect(result.claimed).toBeUndefined();
    expect(
      JSON.stringify({
        sessionKey: replyEvent.sessionKey,
        ctxSessionKey: replyEvent.ctx.SessionKey,
        provider: replyEvent.provider,
        model: replyEvent.model,
        harnessId: replyEvent.harnessId,
      }),
    ).toBe(before);
  });

  it("same-role agent identity contradiction still fails closed", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "agent-identity-conflict",
        sourceSessionKey: "agent:main:dashboard:A",
        eventSessionKey: "agent:main:dashboard:B",
        authorized: true,
        provenance: { kind: "external_user", sourceChannel: "webchat" },
      }),
      "agent",
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });

  it("external ACP owner turn remains Ticket-first", async () => {
    const { databasePath, hooks } = setup();
    await runReply(
      hooks,
      event({
        runId: "external-acp",
        authorized: true,
        provenance: { kind: "external_user", sourceChannel: "webchat" },
      }),
      "acp",
    );
    expect(rows(databasePath, "SELECT run_id FROM tickets")).toEqual([{ run_id: "external-acp" }]);
  });

  it("missing trust for explicit external_user still fails closed", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(
      hooks,
      event({
        runId: "external-untrusted",
        authorized: false,
        scopes: ["operator.admin"],
        provenance: { kind: "external_user", sourceChannel: "discord" },
      }),
    );
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });
});
