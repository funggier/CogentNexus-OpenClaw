import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { randomUUID } from "node:crypto";
import { existsSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";
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
  workspaceDir?: string;
  pythonCommand?: string;
  agentId?: string;
  model?: string;
  timeoutSeconds?: number;
  autoResume?: boolean;
  autoResumeDelayMs?: number;
  autoRotate?: boolean;
  autoWorkflowCompletion?: boolean;
  completionPollMs?: number;
};

type WorkflowCompletion = {
  schemaVersion: number;
  taskId: string;
  ownerSessionKey: string;
  workflowStatus: string;
  stateRevision?: number;
  createdAt: string;
  deliveryStatus: string;
  deliveredAt?: string;
};

function workflowRuntime(workspaceDir: string): string {
  const path = resolve(workspaceDir, "skills", "cogentnexus", "scripts", "workflow.py");
  if (!existsSync(path)) throw new Error(`CogentNexus workflow runtime not found: ${path}`);
  return path;
}

function workspacePath(workspaceDir: string, value: string): string {
  const workspace = resolve(workspaceDir);
  const path = resolve(workspace, value);
  const rel = relative(workspace, path);
  if (rel === "" || rel.startsWith("..") || rel.startsWith("/") || rel.startsWith("\\")) throw new Error("manifestPath must remain inside the workspace");
  return path;
}

function runWorkflowCli(python: string, runtime: string, args: string[]) {
  const result = spawnSync(python, [runtime, ...args], { encoding:"utf8", windowsHide:true, timeout:30_000 });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error((result.stderr || result.stdout || "workflow command failed").trim());
  return result.stdout.trim() ? JSON.parse(result.stdout) : {};
}

export function startBoundWorkflow(input: { workspaceDir:string; manifestPath:string; ownerSessionKey:string; pythonCommand?:string }) {
  const workspace = resolve(input.workspaceDir);
  const runtime = workflowRuntime(workspace);
  const manifest = workspacePath(workspace, input.manifestPath);
  if (!existsSync(manifest)) throw new Error(`workflow manifest not found: ${manifest}`);
  const python = input.pythonCommand ?? "python";
  const initialized = runWorkflowCli(python, runtime, ["--root",workspace,"init",manifest]);
  const taskId = initialized?.taskId;
  if (typeof taskId !== "string" || !taskId) throw new Error("workflow init returned no taskId");
  runWorkflowCli(python, runtime, ["--root",workspace,"bind-owner",taskId,"--session-key",input.ownerSessionKey]);
  const flowDir = resolve(workspace,".cogent","workflows",taskId);
  const stdout = join(flowDir,"controller.stdout.log"), stderr = join(flowDir,"controller.stderr.log");
  writeFileSync(stdout,"",{flag:"a"}); writeFileSync(stderr,"",{flag:"a"});
  const child = spawn(python,[runtime,"--root",workspace,"run",taskId],{
    detached:true,stdio:"ignore",windowsHide:true,
  });
  child.unref();
  return {taskId,status:"started",controllerPid:child.pid,ownerBound:true};
}

export function workflowCompletionTag(notice: WorkflowCompletion): string {
  const task = notice.taskId.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 80);
  return `cogent-workflow-result-${task}-${notice.stateRevision ?? 0}`;
}

export function completionMessage(notice: WorkflowCompletion): string {
  return [
    `CogentNexus workflow ${notice.taskId} reached terminal status ${notice.workflowStatus}.`,
    "Inspect the durable workflow state, ledger, validators, and artifact hashes now.",
    "If completed, consume the verified result and continue the recorded goal or report the compact outcome.",
    "If blocked or failed, classify the failure and resume safely only when authorized and materially useful.",
    "Do not wait for the user to notice process or CPU changes, and do not claim domain success from workflow completion alone.",
  ].join("\n");
}

export function pendingWorkflowCompletions(workspaceDir: string): Array<{ path: string; notice: WorkflowCompletion }> {
  const base = resolve(workspaceDir, ".cogent", "workflows");
  if (!existsSync(base)) return [];
  const found: Array<{ path: string; notice: WorkflowCompletion }> = [];
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory() || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(entry.name)) continue;
    const path = join(base, entry.name, "completion.json");
    if (!existsSync(path)) continue;
    try {
      const notice = JSON.parse(readFileSync(path, "utf8")) as WorkflowCompletion;
      if (notice.schemaVersion === 1 && notice.taskId === entry.name && notice.deliveryStatus === "pending" &&
          typeof notice.ownerSessionKey === "string" && notice.ownerSessionKey.length > 0) found.push({ path, notice });
    } catch { /* A partial or malformed outbox remains for operator inspection. */ }
  }
  return found;
}

function markCompletionDelivered(path: string, notice: WorkflowCompletion) {
  const next = { ...notice, deliveryStatus: "delivered", deliveredAt: new Date().toISOString() };
  const temporary = `${path}.${process.pid}.tmp`;
  writeFileSync(temporary, `${JSON.stringify(next, null, 2)}\n`, "utf8");
  renameSync(temporary, path);
}

export async function deliverWorkflowCompletion(api: any, path: string, notice: WorkflowCompletion) {
  const tag = workflowCompletionTag(notice);
  const taskFlow = api.runtime.tasks.managedFlows.bindSession({ sessionKey: notice.ownerSessionKey });
  const previous = taskFlow.list().find((flow: any) => flow.controllerId === "cogentnexus/workflow" && flow.stateJson?.completionTag === tag);
  if (!previous) {
    const stateJson = { taskId:notice.taskId,workflowStatus:notice.workflowStatus,stateRevision:notice.stateRevision,completionTag:tag };
    const flow = taskFlow.createManaged({controllerId:"cogentnexus/workflow",goal:`Continue after ${notice.taskId}`,currentStep:"terminal_result",stateJson});
    const current = taskFlow.get(flow.flowId);
    if (current?.syncMode === "managed") {
      if (notice.workflowStatus === "completed") taskFlow.finish({flowId:flow.flowId,expectedRevision:current.revision,stateJson,endedAt:Date.now()});
      else taskFlow.fail({flowId:flow.flowId,expectedRevision:current.revision,stateJson,endedAt:Date.now()});
    }
  }
  await api.session.workflow.unscheduleSessionTurnsByTag({ sessionKey: notice.ownerSessionKey, tag });
  await api.session.workflow.scheduleSessionTurn({sessionKey:notice.ownerSessionKey,delayMs:1000,deleteAfterRun:true,deliveryMode:"announce",
    name:`CogentNexus workflow ${notice.taskId}`,tag,message:completionMessage(notice)});
  markCompletionDelivered(path, notice);
}

type RotationObservation = { taskId?: string; sessionKey?: string; status?: string; rotationRequired?: boolean };

export function rotationCandidates(output: string, sessionKey: string): string[] {
  const document = JSON.parse(output) as { observations?: RotationObservation[] };
  return (document.observations ?? [])
    .filter((item) => item.status === "observed" && item.sessionKey === sessionKey && item.rotationRequired === true && typeof item.taskId === "string")
    .map((item) => item.taskId as string);
}

export function monitorRotations(workspaceDir: string, config: RotationConfig, sessionKey: string): string[] {
  const phase3Path = resolve(workspaceDir, "skills", "cogentnexus", "scripts", "phase3.py");
  const cogentRoot = resolve(config.cogentRoot ?? join(workspaceDir, ".cogent"));
  const result = spawnSync(config.pythonCommand ?? "python", [phase3Path, "--root", cogentRoot, "context", "monitor", "--execute-safe"], {
    encoding: "utf8", windowsHide: true, timeout: 30_000,
  });
  if (result.error) throw result.error;
  if (!result.stdout.trim()) throw new Error((result.stderr || "context monitor failed").trim());
  return rotationCandidates(result.stdout, sessionKey);
}

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

async function startRotation(api: any, taskFlow: any, ownerSessionKey: string, workspaceDir: string, config: RotationConfig, taskId: string) {
  const checked = inspectHandoff(taskId, workspaceDir, config);
  const identity = rotationIdentity(checked.handoff.taskId, checked.handoff.generation);
  const plan = { taskId:checked.handoff.taskId,generation:checked.handoff.generation,ownerSessionKey,childSessionKey:identity.childSessionKey,runId:identity.runId,contractHash:checked.handoff.contractHash,action:"ROTATE" };
  const previous = taskFlow.list().find((flow: any) => flow.controllerId === "cogentnexus/rotation" && flow.stateJson?.runId === identity.runId);
  const flow = previous ?? taskFlow.createManaged({controllerId:"cogentnexus/rotation",goal:checked.handoff.goal ?? `Resume ${checked.handoff.taskId}`,currentStep:"starting_detached_worker",stateJson:plan});
  const linked = taskFlow.runTask({flowId:flow.flowId,runtime:"subagent",childSessionKey:identity.childSessionKey,runId:identity.runId,label:`CogentNexus ${checked.handoff.taskId}`,task:checked.handoff.nextAction ?? "Resume from durable handoff",status:"running",startedAt:Date.now(),lastEventAt:Date.now()});
  if (!linked.created && !linked.found) throw new Error(linked.reason);
  if (previous || !linked.created) return {...plan,status:"already-started",flowId:flow.flowId};
  const cliArgs = ["agent","--session-key",identity.childSessionKey,"--message",workerPrompt(taskId,checked.phase3Path,checked.cogentRoot),"--json","--timeout",String(config.timeoutSeconds ?? 3600)];
  if (config.agentId) cliArgs.splice(1,0,"--agent",config.agentId);
  if (config.model) cliArgs.push("--model",config.model);
  const child = launchWorker(cliArgs);
  child.once("error", () => { const current=taskFlow.get(flow.flowId); if(current?.syncMode==="managed") taskFlow.fail({flowId:flow.flowId,expectedRevision:current.revision,stateJson:{...plan,launch:"failed"},endedAt:Date.now()}); });
  child.once("exit", async (code) => {
    const current=taskFlow.get(flow.flowId); if(!current || current.syncMode!=="managed") return;
    const stateJson={...plan,exitCode:code};
    if(code===0) taskFlow.finish({flowId:flow.flowId,expectedRevision:current.revision,stateJson,endedAt:Date.now()});
    else taskFlow.fail({flowId:flow.flowId,expectedRevision:current.revision,stateJson,endedAt:Date.now()});
    const tag=`cogent-rotation-result-${identity.runId}`;
    await api.session.workflow.unscheduleSessionTurnsByTag({sessionKey:ownerSessionKey,tag});
    await api.session.workflow.scheduleSessionTurn({sessionKey:ownerSessionKey,delayMs:1000,deleteAfterRun:true,deliveryMode:"announce",name:`CogentNexus result ${taskId}`,tag,message:`Temporary CogentNexus worker ${identity.childSessionKey} finished with exit code ${code}. Inspect durable task ${taskId}, verify its handoff and artifacts, then report only the compact verified result.`});
  });
  return {...plan,status:"started",flowId:flow.flowId};
}

const configSchema = Type.Object({
  cogentRoot: Type.Optional(Type.String()),
  pythonCommand: Type.Optional(Type.String()),
  agentId: Type.Optional(Type.String()),
  model: Type.Optional(Type.String()),
  timeoutSeconds: Type.Optional(Type.Integer({ minimum: 60, maximum: 86400 })),
  autoResume: Type.Optional(Type.Boolean({ description: "Schedule one durable continuation turn after a resumable interruption." })),
  autoResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000 })),
  autoRotate: Type.Optional(Type.Boolean({ description: "Automatically start a clean TaskFlow worker for a verified ROTATE handoff." })),
  workspaceDir: Type.Optional(Type.String({ description: "Workspace containing .cogent/workflows completion outboxes." })),
  autoWorkflowCompletion: Type.Optional(Type.Boolean({ description: "Automatically wake the bound owner when a workflow reaches a terminal state." })),
  completionPollMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 300000 })),
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
        const details = await startRotation(api, api.runtime.tasks.managedFlows.fromToolContext(toolContext), toolContext.sessionKey, workspaceDir, config, params.taskId);
        return { content: [{ type: "text", text: JSON.stringify(details) }], details };
      },
    }),
  }), tool({
      name:"cogent_workflow_start",
      label:"Start CogentNexus Workflow",
      description:"Initialize, bind to the trusted current session, and launch a durable workflow so terminal results automatically continue in the owner session.",
      parameters:Type.Object({manifestPath:Type.String({description:"Workflow-relative path to a schemaVersion 1 manifest."})},{additionalProperties:false}),
      optional:true,
      factory:({config,toolContext})=>({
        name:"cogent_workflow_start",label:"Start CogentNexus Workflow",description:"Start an owner-bound durable workflow.",
        parameters:Type.Object({manifestPath:Type.String()},{additionalProperties:false}),
        async execute(_id:string,params:{manifestPath:string}) {
          if(!toolContext.sessionKey) throw new Error("workflow start requires a trusted OpenClaw session context");
          const details=startBoundWorkflow({workspaceDir:toolContext.workspaceDir ?? process.cwd(),manifestPath:params.manifestPath,ownerSessionKey:toolContext.sessionKey,pythonCommand:config.pythonCommand});
          return {content:[{type:"text",text:JSON.stringify(details)}],details};
        },
      }),
    }),
  ],
});

const registerTools = entry.register?.bind(entry);
entry.register = (api) => {
  registerTools?.(api);
  const config = (api.pluginConfig ?? {}) as RotationConfig;
  const scheduledRuns = new Set<string>();
  if (config.autoResume !== false || config.autoRotate !== false) api.on("agent_end", async (event, ctx) => {
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
    if (event.success && config.autoRotate !== false && sessionKey) {
      try {
        const workspaceDir = ctx.workspaceDir ?? process.cwd();
        const taskIds = monitorRotations(workspaceDir, config, sessionKey);
        const taskFlow = api.runtime.tasks.managedFlows.bindSession({ sessionKey });
        for (const taskId of taskIds) await startRotation(api, taskFlow, sessionKey, workspaceDir, config, taskId);
      } catch (error) {
        api.logger.warn(`CogentNexus automatic rotation skipped: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
  }, { priority: 50, timeoutMs: 10_000 });
  if (config.autoWorkflowCompletion !== false) {
    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    api.registerService({
      id: "cogentnexus-workflow-completion",
      start: async (ctx: any) => {
        const workspaceDir = resolve(config.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const tick = async () => {
          if (active) return;
          active = true;
          try {
            for (const item of pendingWorkflowCompletions(workspaceDir)) {
              try { await deliverWorkflowCompletion(api, item.path, item.notice); }
              catch (error) { api.logger.warn(`CogentNexus workflow completion delivery failed for ${item.notice.taskId}: ${error instanceof Error ? error.message : String(error)}`); }
            }
          } finally { active = false; }
        };
        await tick();
        interval = setInterval(() => { void tick(); }, config.completionPollMs ?? 5000);
        interval.unref?.();
      },
      stop: async () => { if (interval) clearInterval(interval); interval = undefined; },
    });
  }
};

export default entry;
