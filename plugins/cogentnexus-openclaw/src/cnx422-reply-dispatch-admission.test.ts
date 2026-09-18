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
  const root = mkdtempSync(join(tmpdir(), "cnx422-admission-"));
  roots.push(root);
  mkdirSync(join(root, "host"), { recursive: true });
  writeFileSync(
    join(root, "host", "controller.json"),
    JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }),
  );
  const databasePath = join(root, "tickets.sqlite3");
  const hooks = new Map<string, RegisteredHook[]>();
  const register = (name: string, handler: any, options?: any) => {
    hooks.set(name, [...(hooks.get(name) ?? []), { handler, options }]);
  };
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
    on: register,
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

function replyEvent(input: {
  prompt: string;
  runId?: string;
  sessionKey?: string;
  authorized?: boolean;
  scopes?: string[];
  ctxSessionKey?: string;
}) {
  const sessionKey = input.sessionKey ?? "agent:main:dashboard:cnx422";
  return {
    runId: input.runId,
    sessionKey,
    ctx: {
      SessionKey: input.ctxSessionKey ?? sessionKey,
      commandText: input.prompt,
      agentText: input.prompt,
      rawText: input.prompt,
      Body: input.prompt,
      BodyForAgent: input.prompt,
      CommandAuthorized: true,
      InboundAccessAuthorized: input.authorized,
      GatewayClientScopes: input.scopes ?? ["operator.write"],
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
  event: any,
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
    const result = await item.handler(event, ctx);
    if (result?.handled === true) {
      claimed = result;
      break;
    }
  }
  return { claimed, dispatcher: d, event, ctx };
}

async function runBeforeAgent(
  hooks: Map<string, RegisteredHook[]>,
  prompt: string,
  runId: string,
  sessionKey = "agent:main:dashboard:cnx422",
) {
  const ordered = [...(hooks.get("before_agent_run") ?? [])].sort(
    (a, b) => Number(b.options?.priority ?? 0) - Number(a.options?.priority ?? 0),
  );
  const results: any[] = [];
  for (const item of ordered) {
    results.push(
      await item.handler(
        { prompt, senderIsOwner: true },
        { sessionKey, sessionId: `${runId}-session`, runId, workspaceDir: undefined },
      ),
    );
  }
  return results;
}

function rows(path: string, sql: string, ...params: any[]) {
  const db = new DatabaseSync(path, { readOnly: true });
  try {
    return db.prepare(sql).all(...params) as any[];
  } finally {
    db.close();
  }
}

const DIRECT = "ตอบกลับสั้น ๆ ว่า CNX-422-DIRECT";
const DURABLE = "PHASE 1\nDesign\nPHASE 2\nBuild\nPHASE 3\nVerify\nทำจนเสร็จและตรวจสอบทุกขั้น";

describe("CNX-422 reply_dispatch Ticket-first admission", () => {
  it("RED: admits Dashboard agent/embedded dispatch before any before_agent_run hook", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({ prompt: DIRECT, runId: "agent-direct", authorized: true }), "agent");
    expect(rows(databasePath, "SELECT run_id,prompt,workflow_eligible FROM tickets")).toEqual([
      { run_id: "agent-direct", prompt: DIRECT, workflow_eligible: 0 },
    ]);
  });

  it("RED: admits ACP/Codex-style dispatch before harness execution", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({ prompt: DIRECT, runId: "acp-direct", authorized: true }), "acp");
    expect(rows(databasePath, "SELECT run_id,workflow_eligible FROM tickets")).toEqual([
      { run_id: "acp-direct", workflow_eligible: 0 },
    ]);
  });

  it("RED: durable dispatch is committed and claimed before conversational inference", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(hooks, replyEvent({ prompt: DURABLE, runId: "durable-run", authorized: true }), "acp");
    expect(rows(databasePath, "SELECT run_id,workflow_eligible FROM tickets")).toEqual([
      { run_id: "durable-run", workflow_eligible: 1 },
    ]);
    expect(result.claimed).toMatchObject({ handled: true });
  });

  it("RED: reply_dispatch then before_agent_run is one logical Ticket", async () => {
    const { databasePath, hooks } = setup();
    const sessionKey = "agent:main:dashboard:dedupe";
    await runReply(hooks, replyEvent({ prompt: DIRECT, runId: "same-run", sessionKey, authorized: true }));
    await runBeforeAgent(hooks, DIRECT, "same-run", sessionKey);
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 1 }]);
  });

  it("RED: route event cardinality stays exactly one across both adapters", async () => {
    const { databasePath, hooks } = setup();
    const sessionKey = "agent:main:dashboard:route";
    await runReply(hooks, replyEvent({ prompt: DIRECT, runId: "route-run", sessionKey, authorized: true }));
    await runBeforeAgent(hooks, DIRECT, "route-run", sessionKey);
    expect(rows(databasePath, "SELECT event_type FROM ticket_events ORDER BY event_id")).toEqual([
      { event_type: "accepted" },
      { event_type: "routed" },
    ]);
  });

  it("RED: direct request remains unclaimed so OpenClaw keeps model/harness authority", async () => {
    const { hooks } = setup();
    const result = await runReply(hooks, replyEvent({ prompt: DIRECT, runId: "direct-pass", authorized: true }), "acp");
    expect(result.claimed).toBeUndefined();
  });

  it("RED: canonical agentText is persisted without provider/model rewriting", async () => {
    const { databasePath, hooks, api } = setup();
    const event = replyEvent({ prompt: DIRECT, runId: "canonical-run", authorized: true });
    event.ctx.Body = "legacy body must not win";
    (event as any).provider = "openai";
    (event as any).model = "gpt-5.6-luna";
    (event as any).harnessId = "codex";
    const before = JSON.stringify({ provider: (event as any).provider, model: (event as any).model, harnessId: (event as any).harnessId, cfg: api.config });
    await runReply(hooks, event, "acp");
    expect(rows(databasePath, "SELECT prompt FROM tickets")).toEqual([{ prompt: DIRECT }]);
    expect(JSON.stringify({ provider: (event as any).provider, model: (event as any).model, harnessId: (event as any).harnessId, cfg: api.config })).toBe(before);
  });

  it("RED: internal delivery marker does not create a new owner Ticket", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({
      prompt: "[CogentNexus-OpenClaw Delivery: ticket:999999]\nDeliver committed output",
      runId: "delivery-marker",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: post-compaction continuation does not create a duplicate owner Ticket", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({
      prompt: "[CogentNexus-OpenClaw Continuation: post-compaction]\nResume committed work",
      runId: "post-compaction",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: direct-recovery continuation does not create a duplicate owner Ticket", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({
      prompt: "#cogent-direct\n[CogentNexus-OpenClaw Continuation: direct-recovery:CNXT-test]\nResume committed state.",
      runId: "direct-recovery",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: subagent/synthetic session is excluded", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({
      prompt: DIRECT,
      runId: "subagent",
      sessionKey: "agent:main:subagent:worker",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
  });

  it("RED: explicit v2026.9.4 InboundAccessAuthorized=true is a valid trust proof", async () => {
    const { databasePath, hooks } = setup();
    await runReply(hooks, replyEvent({
      prompt: DIRECT,
      runId: "authorized-ingress",
      sessionKey: "agent:main:discord:channel:123",
      authorized: true,
      scopes: [],
    }));
    expect(rows(databasePath, "SELECT run_id,owner_session_key FROM tickets")).toEqual([
      { run_id: "authorized-ingress", owner_session_key: "agent:main:discord:channel:123" },
    ]);
  });

  it("RED: missing/untrusted ingress proof fails closed without creating a privileged Ticket", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(hooks, replyEvent({
      prompt: DIRECT,
      runId: "untrusted",
      sessionKey: "agent:main:discord:channel:123",
      authorized: false,
      scopes: [],
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });

  it("explicit denied ingress cannot be overridden by privileged Gateway scopes", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(hooks, replyEvent({
      prompt: DIRECT,
      runId: "contradictory-trust",
      sessionKey: "agent:main:dashboard:trust-conflict",
      authorized: false,
      scopes: ["operator.write", "operator.admin"],
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });

  it("RED: contradictory session identity fails closed", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(hooks, replyEvent({
      prompt: DIRECT,
      runId: "identity-conflict",
      sessionKey: "agent:main:dashboard:A",
      ctxSessionKey: "agent:main:dashboard:B",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });

  it("RED: trusted external owner turn without exact runId fails closed", async () => {
    const { databasePath, hooks } = setup();
    const result = await runReply(hooks, replyEvent({
      prompt: DIRECT,
      sessionKey: "agent:main:dashboard:no-run",
      authorized: true,
    }));
    expect(rows(databasePath, "SELECT count(*) AS n FROM tickets")).toEqual([{ n: 0 }]);
    expect(result.claimed).toMatchObject({ handled: true });
  });
});
