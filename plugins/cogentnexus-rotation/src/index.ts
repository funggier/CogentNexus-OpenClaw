import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { randomUUID } from "node:crypto";
import { existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";

type Handoff = {
  taskId: string;
  generation: number;
  status: string;
  goal?: string;
  nextAction?: string;
  contractHash: string;
  contextDecision?: { action?: string };
};

type RotationConfig = {
  cogentRoot?: string;
  pythonCommand?: string;
  agentId?: string;
  model?: string;
  timeoutSeconds?: number;
  autoResume?: boolean;
  autoResumeDelayMs?: number;
};

export function isResumableInterruption(success: boolean, error?: string): boolean {
  if (success || !error) return false;
  return /(interrupt|context[_ -]?length[_ -]?exceeded|compaction|summari[sz]ation failed|timed?\s*out)/i.test(error);
}

export function autoResumeTag(runId: string): string {
  return `cogent-resume-${runId.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 96)}`;
}

type ResumeWorkflow = {
  unscheduleSessionTurnsByTag(input: { sessionKey: string; tag: string }): Promise<unknown>;
  scheduleSessionTurn(input: {
    sessionKey: string;
    delayMs: number;
    deleteAfterRun: boolean;
    deliveryMode: "announce";
    name: string;
    tag: string;
    message: string;
  }): Promise<unknown>;
};

export async function scheduleInterruptedResume(input: {
  success: boolean;
  error?: string;
  runId?: string;
  sessionKey?: string;
  delayMs?: number;
  workflow: ResumeWorkflow;
  scheduledRuns: Set<string>;
}): Promise<boolean> {
  const { runId, sessionKey } = input;
  if (!runId || !sessionKey || input.scheduledRuns.has(runId) || !isResumableInterruption(input.success, input.error)) return false;
  const tag = autoResumeTag(runId);
  await input.workflow.unscheduleSessionTurnsByTag({ sessionKey, tag });
  await input.workflow.scheduleSessionTurn({
    sessionKey,
    delayMs: input.delayMs ?? 2000,
    deleteAfterRun: true,
    deliveryMode: "announce",
    name: `CogentNexus resume ${runId.slice(0, 12)}`,
    tag,
    message: [
      "The previous run was interrupted.",
      "Resume automatically from committed CogentNexus durable state and the latest valid handoff.",
      "Recover prepared transactions first, verify completed artifacts, and continue only the smallest recorded next action.",
      "Do not repeat external side effects and do not claim completion without verification.",
    ].join("\n"),
  });
  input.scheduledRuns.add(runId);
  return true;
}

export function inspectHandoff(
  taskId: string,
  workspaceDir: string,
  config: RotationConfig,
): { handoff: Handoff; phase3Path: string; cogentRoot: string } {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(taskId)) {
    throw new Error("taskId contains unsupported characters");
  }
  const phase3Path = resolve(workspaceDir, "skills", "cogentnexus", "scripts", "phase3.py");
  const cogentRoot = resolve(config.cogentRoot ?? join(workspaceDir, ".cogent"));
  if (!existsSync(phase3Path)) throw new Error(`CogentNexus phase3 runtime not found: ${phase3Path}`);
  const result = spawnSync(config.pythonCommand ?? "python", [
    phase3Path, "--root", cogentRoot, "context", "inspect", "--task-id", taskId,
  ], { encoding: "utf8", windowsHide: true, timeout: 30_000 });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error((result.stderr || result.stdout || "handoff validation failed").trim());
  const handoff = JSON.parse(result.stdout) as Handoff;
  if (handoff.taskId !== taskId) throw new Error("handoff task identity mismatch");
  if (handoff.status !== "prepared") throw new Error(`handoff is not prepared (status=${handoff.status})`);
  if (handoff.contextDecision?.action !== "ROTATE") {
    throw new Error(`rotation is not authorized by context policy (action=${handoff.contextDecision?.action ?? "unknown"})`);
  }
  return { handoff, phase3Path, cogentRoot };
}

export function rotationIdentity(taskId: string, generation: number) {
  const suffix = `${taskId.toLowerCase().replace(/[^a-z0-9-]/g, "-")}-${generation}`;
  return {
    runId: `cogent-rotate-${suffix}`,
    childSessionKey: `agent:main:cogent-rotate-${suffix}`,
  };
}

function workerPrompt(taskId: string, phase3Path: string, cogentRoot: string): string {
  return [
    "Resume a CogentNexus task from durable state; do not reconstruct prior private reasoning.",
    `Task ID: ${taskId}`,
    `Cogent root: ${cogentRoot}`,
    `Runtime: ${phase3Path}`,
    "First inspect and claim the prepared handoff using your trusted current session key.",
    "Verify existing artifacts, perform only the recorded next action within inherited authorization, checkpoint evidence, then release the lease.",
    "Never claim completion without deterministic verification.",
  ].join("\n");
}

function launchWorker(args: string[]): ChildProcess {
  return spawn("openclaw", args, {
    detached: false,
    stdio: "ignore",
    windowsHide: true,
  });
}

const configSchema = Type.Object({
  cogentRoot: Type.Optional(Type.String()),
  pythonCommand: Type.Optional(Type.String()),
  agentId: Type.Optional(Type.String()),
  model: Type.Optional(Type.String()),
  timeoutSeconds: Type.Optional(Type.Integer({ minimum: 60, maximum: 86400 })),
  autoResume: Type.Optional(Type.Boolean({ description: "Schedule one durable continuation turn after a resumable interruption." })),
  autoResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000 })),
}, { additionalProperties: false });

const entry = defineToolPlugin({
  id: "cogentnexus-rotation",
  name: "CogentNexus Rotation Controller",
  description: "Validate a durable CogentNexus ROTATE handoff and start one idempotently identified TaskFlow worker.",
  configSchema,
  tools: (tool) => [tool({
    name: "cogent_rotation",
    label: "CogentNexus Rotation",
    description: "Plan or start a safe session rotation. Defaults to dry-run; execute only after CogentNexus produced a verified ROTATE handoff.",
    parameters: Type.Object({
      taskId: Type.String({ description: "Durable CogentNexus task id." }),
      execute: Type.Optional(Type.Boolean({ description: "Start the detached worker. Defaults to false." })),
    }, { additionalProperties: false }),
    optional: true,
    factory: ({ api, config, toolContext }) => ({
      name: "cogent_rotation",
      label: "CogentNexus Rotation",
      description: "Plan or start a safe CogentNexus session rotation.",
      parameters: Type.Object({
        taskId: Type.String(),
        execute: Type.Optional(Type.Boolean()),
      }, { additionalProperties: false }),
      async execute(_toolCallId: string, params: { taskId: string; execute?: boolean }) {
        if (!toolContext.sessionKey) throw new Error("rotation requires a trusted OpenClaw session context");
        const workspaceDir = toolContext.workspaceDir ?? process.cwd();
        const checked = inspectHandoff(params.taskId, workspaceDir, config);
        const identity = rotationIdentity(checked.handoff.taskId, checked.handoff.generation);
        const plan = {
          taskId: checked.handoff.taskId,
          generation: checked.handoff.generation,
          ownerSessionKey: toolContext.sessionKey,
          childSessionKey: identity.childSessionKey,
          runId: identity.runId,
          contractHash: checked.handoff.contractHash,
          action: "ROTATE",
        };
        if (params.execute !== true) {
          return { content: [{ type: "text", text: JSON.stringify({ ...plan, status: "dry-run" }) }], details: plan };
        }

        const taskFlow = api.runtime.tasks.flow.fromToolContext(toolContext);
        const previous = taskFlow.list().find((flow) => {
          const state = flow.stateJson as Record<string, unknown> | null | undefined;
          return flow.controllerId === "cogentnexus/rotation" && state?.runId === identity.runId;
        });
        const flow = previous ?? taskFlow.createManaged({
          controllerId: "cogentnexus/rotation",
          goal: checked.handoff.goal ?? `Resume ${checked.handoff.taskId}`,
          currentStep: "starting_detached_worker",
          stateJson: plan,
        });
        const linked = taskFlow.runTask({
          flowId: flow.flowId,
          runtime: "subagent",
          childSessionKey: identity.childSessionKey,
          runId: identity.runId,
          label: `CogentNexus ${checked.handoff.taskId}`,
          task: checked.handoff.nextAction ?? "Resume from durable handoff",
          status: "running",
          startedAt: Date.now(),
          lastEventAt: Date.now(),
        });
        if (!linked.created && !linked.found) throw new Error(linked.reason);
        if (previous || !linked.created) {
          const details = { ...plan, status: "already-started", flowId: flow.flowId };
          return { content: [{ type: "text", text: JSON.stringify(details) }], details };
        }

        const cliArgs = ["agent", "--session-key", identity.childSessionKey, "--message", workerPrompt(params.taskId, checked.phase3Path, checked.cogentRoot), "--json", "--timeout", String(config.timeoutSeconds ?? 3600)];
        if (config.agentId) cliArgs.splice(1, 0, "--agent", config.agentId);
        if (config.model) cliArgs.push("--model", config.model);
        const child = launchWorker(cliArgs);
        child.once("error", () => {
          taskFlow.fail({ flowId: flow.flowId, expectedRevision: flow.revision, stateJson: { ...plan, launch: "failed" }, endedAt: Date.now() });
        });
        child.once("exit", (code) => {
          const current = taskFlow.get(flow.flowId);
          if (!current || current.syncMode !== "managed") return;
          const stateJson = { ...plan, exitCode: code };
          if (code === 0) taskFlow.finish({ flowId: flow.flowId, expectedRevision: current.revision, stateJson, endedAt: Date.now() });
          else taskFlow.fail({ flowId: flow.flowId, expectedRevision: current.revision, stateJson, endedAt: Date.now() });
        });
        const details = { ...plan, status: "started", flowId: flow.flowId };
        return { content: [{ type: "text", text: JSON.stringify(details) }], details };
      },
    }),
  })],
});

const registerTools = entry.register?.bind(entry);
entry.register = (api) => {
  registerTools?.(api);
  const config = (api.pluginConfig ?? {}) as RotationConfig;
  if (config.autoResume === false) return;
  const scheduledRuns = new Set<string>();
  api.on("agent_end", async (event, ctx) => {
    const runId = event.runId ?? ctx.runId;
    const sessionKey = ctx.sessionKey;
    await scheduleInterruptedResume({
      success: event.success,
      error: event.error,
      runId,
      sessionKey,
      delayMs: config.autoResumeDelayMs,
      workflow: api.session.workflow,
      scheduledRuns,
    });
  }, { priority: 50, timeoutMs: 10_000 });
};

export default entry;
