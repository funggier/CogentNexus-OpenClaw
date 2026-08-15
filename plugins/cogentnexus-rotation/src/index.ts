import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { randomUUID } from "node:crypto";
import { existsSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { statfsSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { freemem } from "node:os";
import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";
import { classifyDurableRequest, compileDurableIntake, durableRequestFingerprint } from "./admission.js";
import { defaultTicketDatabase, TicketStore, ticketIntakeEligible, type TicketOutbox } from "./ticket-store.js";
import { TicketDispatcher } from "./ticket-dispatcher.js";
import { KnowledgeStore, type ApplicationOutcome, type ExperienceKind } from "./knowledge-store.js";
import { ExternalResearchStore, type ClaimRelation, type SourceType } from "./external-research.js";
import { bindDeliveryRun, hasPendingSessionWork, hasVisibleAssistantOutput, markWorkflowDeliveryScheduleFailed, markWorkflowDeliveryScheduled, parseDeliveryMarker, postCompactionResumeTag, settleDeliveryTarget, ticketDeliveryMarker, workflowDeliveryIsRetryable, workflowDeliveryMarker, type DeliveryTarget } from "./delivery-continuity.js";

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
  directDeliverySettleMs?: number;
  directDeliveryTimeoutMs?: number;
  outboxDeliveryTimeoutMs?: number;
  postCompactionResumeDelayMs?: number;
  autoRotate?: boolean;
  autoWorkflowCompletion?: boolean;
  completionPollMs?: number;
  enforcedMode?: boolean;
  preInferenceAdmission?: boolean;
  admissionMinimumScore?: number;
  durableWorkerModel?: string;
  ticketFirst?: boolean;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  ticketOutboxPollMs?: number;
  ticketDispatchPollMs?: number;
  ticketDispatchLimit?: number;
  ticketLeaseMs?: number;
  ticketMinimumFreeMemoryBytes?: number;
  ticketMinimumFreeDiskBytes?: number;
  ticketMaximumRunning?: number;
  ticketMaximumAttempts?: number;
  knowledgeEnabled?: boolean;
  externalResearchEnabled?: boolean;
};

export type TicketResourceSnapshot = {freeMemoryBytes:number;freeDiskBytes:number;running:number};

export function ticketResourceAdmission(snapshot: TicketResourceSnapshot, config: RotationConfig) {
  const minimumMemory = config.ticketMinimumFreeMemoryBytes ?? 512 * 1024 * 1024;
  const minimumDisk = config.ticketMinimumFreeDiskBytes ?? 512 * 1024 * 1024;
  const maximumRunning = config.ticketMaximumRunning ?? 1;
  const reasons:string[] = [];
  if (snapshot.freeMemoryBytes < minimumMemory) reasons.push("memory");
  if (snapshot.freeDiskBytes < minimumDisk) reasons.push("disk");
  if (snapshot.running >= maximumRunning) reasons.push("concurrency");
  return {admitted:reasons.length === 0,reasons,snapshot};
}

function ticketResourceSnapshot(workspaceDir:string, store:TicketStore):TicketResourceSnapshot {
  const disk = statfsSync(workspaceDir);
  return {freeMemoryBytes:freemem(),freeDiskBytes:Number(disk.bavail) * Number(disk.bsize),running:store.linkedRunning().length};
}

type WorkflowCompletion = {
  schemaVersion: number;
  taskId: string;
  ownerSessionKey: string;
  workflowStatus: string;
  stateRevision?: number;
  createdAt: string;
  deliveryStatus: string;
  deliveredAt?: string;
  deliveryAttempts?: number;
  lastDeliveryAttemptAt?: string;
  lastDeliveryError?: string;
  scheduledAt?: string;
  deliveryRunId?: string;
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
  const requested = JSON.parse(readFileSync(manifest,"utf8"));
  let initialized: any;
  let existing = false;
  try {
    initialized = runWorkflowCli(python, runtime, ["--root",workspace,"init",manifest,"--owner-session-key",input.ownerSessionKey]);
  } catch (error) {
    const taskId = requested?.taskId;
    const flowDir = typeof taskId === "string" ? resolve(workspace,".cogent","workflows",taskId) : "";
    const statePath = flowDir ? resolve(flowDir,"state.json") : "";
    const ownerPath = flowDir ? resolve(flowDir,"owner.json") : "";
    if (!statePath || !ownerPath || !existsSync(statePath) || !existsSync(ownerPath)) throw error;
    const state = JSON.parse(readFileSync(statePath,"utf8"));
    const owner = JSON.parse(readFileSync(ownerPath,"utf8"));
    if (state.taskId !== taskId || owner.ownerSessionKey !== input.ownerSessionKey) throw error;
    initialized = state;
    existing = true;
  }
  const taskId = initialized?.taskId;
  if (typeof taskId !== "string" || !taskId) throw new Error("workflow init returned no taskId");
  const flowDir = resolve(workspace,".cogent","workflows",taskId);
  if (existing && ["completed","blocked","failed","cancelled"].includes(initialized.status)) {
    return {taskId,status:initialized.status,controllerPid:initialized.controllerPid,ownerBound:true,idempotentReplay:true};
  }
  const stdout = join(flowDir,"controller.stdout.log"), stderr = join(flowDir,"controller.stderr.log");
  writeFileSync(stdout,"",{flag:"a"}); writeFileSync(stderr,"",{flag:"a"});
  const child = spawn(python,[runtime,"--root",workspace,"run",taskId],{
    detached:true,stdio:"ignore",windowsHide:true,
  });
  child.unref();
  return {taskId,status:"started",controllerPid:child.pid,ownerBound:true,idempotentReplay:existing};
}

export function dispatchTicketWorkflows(input:{workspaceDir:string;store:TicketStore;config:RotationConfig;now?:Date;snapshot?:TicketResourceSnapshot;
  compile?:typeof compileDurableIntake;start?:typeof startBoundWorkflow}) {
  const admission = ticketResourceAdmission(input.snapshot ?? ticketResourceSnapshot(input.workspaceDir,input.store),input.config);
  if (!admission.admitted) return {admission,leases:[]};
  const dispatcher = new TicketDispatcher(input.store);
  const leases = dispatcher.dispatch({
    limit:input.config.ticketDispatchLimit ?? 1,
    leaseMs:input.config.ticketLeaseMs ?? 60_000,
    now:input.now,
    admit:()=>ticketResourceAdmission(input.snapshot ?? ticketResourceSnapshot(input.workspaceDir,input.store),input.config).admitted,
    launch:(lease)=>{
      const ticket = input.store.get(lease.ticketId);
      if (!ticket || !ticket.workflowEligible) throw new Error("Ticket is not eligible for workflow dispatch");
      const classified = classifyDurableRequest(ticket.prompt,input.config.admissionMinimumScore ?? 5);
      const decision = classified.lane === "durable" ? classified : {...classified,lane:"durable" as const,score:Math.max(classified.score,input.config.admissionMinimumScore ?? 5),reasons:[...classified.reasons,"direct-interruption-recovery"]};
      const requestHash = durableRequestFingerprint(ticket.prompt);
      const duplicate = activeWorkflowForRequest(input.workspaceDir,requestHash);
      const intake = duplicate ? undefined : (input.compile ?? compileDurableIntake)({workspaceDir:input.workspaceDir,prompt:ticket.prompt,runId:ticket.runId,decision,model:input.config.durableWorkerModel ?? "qwen3.5:9b-32k"});
      const started = duplicate ?? (input.start ?? startBoundWorkflow)({workspaceDir:input.workspaceDir,manifestPath:intake!.manifestPath,ownerSessionKey:ticket.ownerSessionKey,pythonCommand:input.config.pythonCommand});
      const manifestPath = intake?.manifestPath ?? `.cogent/workflows/${started.taskId}/manifest.json`;
      input.store.linkWorkflow({...lease,workflowId:started.taskId,manifestPath,now:input.now});
    },
  });
  return {admission,leases};
}

export function reconcileTicketWorkflows(input:{workspaceDir:string;store:TicketStore;config:RotationConfig;now?:Date}) {
  const results:Array<{ticketId:string;action:string}> = [];
  for (const linked of input.store.linkedRunning()) {
    const statePath = resolve(input.workspaceDir,".cogent","workflows",linked.workflowId,"state.json");
    if (!existsSync(statePath)) continue;
    let state:any;
    try { state=JSON.parse(readFileSync(statePath,"utf8")); } catch { continue; }
    try {
      if (state.status === "completed") {
        input.store.complete({...linked,result:{workflowId:linked.workflowId,status:state.status,stateRevision:state.revision},now:input.now});
        results.push({ticketId:linked.ticketId,action:"completed"});
      } else if (["failed","cancelled"].includes(state.status)) {
        input.store.failAttempt({...linked,classification:"permanent",message:`workflow ${state.status}`,now:input.now});
        results.push({ticketId:linked.ticketId,action:"failed"});
      } else if (state.status === "blocked") {
        input.store.failAttempt({...linked,classification:"capability",message:"workflow blocked",now:input.now});
        results.push({ticketId:linked.ticketId,action:"waiting"});
      } else {
        input.store.heartbeat({...linked,leaseMs:input.config.ticketLeaseMs ?? 60_000,now:input.now});
        results.push({ticketId:linked.ticketId,action:"heartbeat"});
      }
    } catch { /* A concurrent recovery or newer fencing generation owns the Ticket. */ }
  }
  return results;
}

export function workflowCompletionTag(notice: WorkflowCompletion): string {
  const task = notice.taskId.replace(/[^A-Za-z0-9_-]/g, "-").slice(0, 80);
  return `cogent-workflow-result-${task}-${notice.stateRevision ?? 0}`;
}

export function completionMessage(notice: WorkflowCompletion): string {
  return [
    workflowDeliveryMarker(notice.taskId, notice.stateRevision ?? 0),
    `CogentNexus workflow ${notice.taskId} reached terminal status ${notice.workflowStatus}.`,
    "Inspect the durable workflow state, ledger, validators, and artifact hashes now.",
    "If completed, consume the verified result and continue the recorded goal or report the compact outcome.",
    "If blocked or failed, classify the failure and resume safely only when authorized and materially useful.",
    "Do not wait for the user to notice process or CPU changes, and do not claim domain success from workflow completion alone.",
  ].join("\n");
}

export function pendingWorkflowCompletions(workspaceDir: string, now = new Date(), retryAfterMs = 300_000): Array<{ path: string; notice: WorkflowCompletion }> {
  const base = resolve(workspaceDir, ".cogent", "workflows");
  if (!existsSync(base)) return [];
  const found: Array<{ path: string; notice: WorkflowCompletion }> = [];
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory() || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(entry.name)) continue;
    const path = join(base, entry.name, "completion.json");
    if (!existsSync(path)) continue;
    try {
      const notice = JSON.parse(readFileSync(path, "utf8")) as WorkflowCompletion;
      if (notice.schemaVersion === 1 && notice.taskId === entry.name && workflowDeliveryIsRetryable(notice, now, retryAfterMs) &&
          typeof notice.ownerSessionKey === "string" && notice.ownerSessionKey.length > 0) found.push({ path, notice });
    } catch { /* A partial or malformed outbox remains for operator inspection. */ }
  }
  return found;
}

export async function deliverWorkflowCompletion(api: any, path: string, notice: WorkflowCompletion) {
  const scheduled = markWorkflowDeliveryScheduled(path, notice);
  try {
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
    return scheduled;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    markWorkflowDeliveryScheduleFailed(path, scheduled, message);
    throw error;
  }
}

export function ticketOutboxTag(item: TicketOutbox) {
  return `cogent-ticket-result-${item.ticketId.replace(/[^A-Za-z0-9_-]/g,"-").slice(0,96)}`;
}

export async function deliverTicketOutbox(api: any, store: TicketStore, item: TicketOutbox) {
  const tag = ticketOutboxTag(item);
  store.markOutboxScheduled(item.outboxId);
  try {
    await api.session.workflow.unscheduleSessionTurnsByTag({sessionKey:item.ownerSessionKey,tag});
    await api.session.workflow.scheduleSessionTurn({
      sessionKey:item.ownerSessionKey,delayMs:1000,deleteAfterRun:true,deliveryMode:"announce",
      name:`CogentNexus Ticket ${item.ticketId}`,tag,
      message:[ticketDeliveryMarker(item.outboxId),`CogentNexus Ticket ${item.ticketId} reached terminal status ${item.terminalStatus}.`,
        "Inspect the committed Ticket, event history, result, and validators before reporting or continuing.",
        "Do not repeat external side effects and do not claim success from terminal state alone."].join("\n"),
    });
  } catch (error) {
    store.markOutboxFailed(item.outboxId,error instanceof Error ? error.message : String(error));
    throw error;
  }
}

export function enforcementDecision(toolName: string, params: Record<string, unknown>, sessionKey?: string, enabled = true) {
  if (!enabled || !sessionKey || toolName === "cogent_workflow_start") return { block:false };
  const executionTools = /(?:^|__)(?:shell_command|exec_command|powershell|bash|terminal|run_command)$/i;
  if (!executionTools.test(toolName)) return { block:false };
  let payload = "";
  try { payload = JSON.stringify(params); } catch { return { block:false }; }
  const invokesRuntime = /workflow\.py/i.test(payload);
  const bypassesOwner = /--operator-unbound|\bbind-owner\b/i.test(payload);
  const initializesDirectly = invokesRuntime && /(?:^|[\s\"'])init(?:[\s\"']|$)/i.test(payload);
  if (!bypassesOwner && !initializesDirectly) return { block:false };
  return {block:true,blockReason:"CogentNexus Enforced Mode: conversational durable workflows must start through cogent_workflow_start with the trusted current owner session."};
}

export function durableAdmissionEligible(input: { sessionKey?: string; senderIsOwner?: boolean }) {
  if (!input.sessionKey || input.sessionKey.includes(":subagent:")) return false;
  if (input.senderIsOwner !== false) return true;
  // Dashboard sessions are authenticated, direct control-UI conversations. In
  // current OpenClaw builds their before_agent_run event can carry
  // senderIsOwner=false because WebChat has no channel sender identity. The
  // canonical dashboard namespace is therefore the owner-bound fallback; do
  // not extend this exception to arbitrary CLI, channel, or agent sessions.
  return /^agent:[^:]+:dashboard:[^:]+$/u.test(input.sessionKey);
}

export function activeWorkflowForRequest(workspaceDir: string, requestHash: string) {
  const base = resolve(workspaceDir, ".cogent", "workflows");
  if (!existsSync(base)) return undefined;
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    try {
      const manifest = JSON.parse(readFileSync(join(base, entry.name, "manifest.json"), "utf8"));
      const state = JSON.parse(readFileSync(join(base, entry.name, "state.json"), "utf8"));
      if (manifest?.admission?.requestHash === requestHash && !["completed", "blocked", "failed", "cancelled"].includes(state?.status)) {
        return { taskId: entry.name, status: state.status, controllerPid: state.controllerPid };
      }
    } catch { /* malformed workflows remain operator-visible and are not deduplicated */ }
  }
  return undefined;
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


export async function schedulePostCompactionResume(input: {
  sessionKey: string;
  workspaceDir: string;
  store: TicketStore;
  delayMs?: number;
  workflow: ResumeWorkflow;
}): Promise<boolean> {
  if (!hasPendingSessionWork(input.workspaceDir,input.store,input.sessionKey)) return false;
  const tag=postCompactionResumeTag(input.sessionKey);
  await input.workflow.unscheduleSessionTurnsByTag({sessionKey:input.sessionKey,tag});
  await input.workflow.scheduleSessionTurn({
    sessionKey:input.sessionKey,
    delayMs:input.delayMs ?? 5000,
    deleteAfterRun:true,
    deliveryMode:"announce",
    name:"CogentNexus post-compaction continuation",
    tag,
    message:[
      "#cogent-direct",
      "[CogentNexus Continuation: post-compaction]",
      "Compaction completed while CogentNexus still has non-terminal work or unconfirmed delivery for this session.",
      "Resume from the latest committed Ticket/workflow/handoff state; do not reconstruct discarded reasoning.",
      "If the original run already continued or the work is now terminal, do not repeat the answer or any external side effect.",
    ].join("\n"),
  });
  return true;
}

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
  directDeliverySettleMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000, description: "Quiet period after fallback message_sent receipts before a direct Ticket is considered delivered." })),
  directDeliveryTimeoutMs: Type.Optional(Type.Integer({ minimum: 10000, maximum: 3600000, description: "Maximum time a response-ready direct Ticket may remain without confirmed final delivery before durable recovery." })),
  outboxDeliveryTimeoutMs: Type.Optional(Type.Integer({ minimum: 10000, maximum: 3600000, description: "Retry age for a scheduled terminal delivery that never receives a delivery receipt." })),
  postCompactionResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 120000, description: "Delayed fallback continuation scheduled after successful compaction while durable work remains." })),
  autoRotate: Type.Optional(Type.Boolean({ description: "Opt in to a clean TaskFlow/Codex worker for ROTATE handoffs. Disabled by default." })),
  workspaceDir: Type.Optional(Type.String({ description: "Workspace containing CogentNexus durable state and workflow completion outboxes." })),
  autoWorkflowCompletion: Type.Optional(Type.Boolean({ description: "Automatically wake the bound owner when a workflow reaches a terminal state." })),
  completionPollMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 300000 })),
  enforcedMode: Type.Optional(Type.Boolean({ description: "Enforce owner/session and managed workflow authority boundaries." })),
  preInferenceAdmission: Type.Optional(Type.Boolean({ description: "Route obvious durable owner requests before the selected conversational model receives the prompt." })),
  admissionMinimumScore: Type.Optional(Type.Integer({ minimum: 3, maximum: 20 })),
  durableWorkerModel: Type.Optional(Type.String({ description: "Ollama model used by automatically compiled bounded workflow components." })),
  ticketFirst: Type.Optional(Type.Boolean({ description: "Commit every eligible owner message to SQLite before inference. Host-managed installs enable this by default." })),
  ticketDatabasePath: Type.Optional(Type.String({ description: "Optional SQLite ticket database path. Defaults under workspace .cogent/runtime." })),
  ticketRecoveryPollMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 300000, description: "Deterministic expired-lease recovery scan interval." })),
  ticketOutboxPollMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 300000, description: "Terminal Ticket delivery interval." })),
  ticketDispatchPollMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 300000, description: "Bounded Ticket dispatch interval." })),
  ticketDispatchLimit: Type.Optional(Type.Integer({ minimum: 1, maximum: 32, description: "Maximum Tickets claimed per dispatch tick." })),
  ticketLeaseMs: Type.Optional(Type.Integer({ minimum: 5000, maximum: 3600000, description: "Ticket worker lease and heartbeat extension." })),
  ticketMinimumFreeMemoryBytes: Type.Optional(Type.Integer({ minimum: 0, description: "Minimum observed free memory before Ticket dispatch." })),
  ticketMinimumFreeDiskBytes: Type.Optional(Type.Integer({ minimum: 0, description: "Minimum observed free disk before Ticket dispatch." })),
  ticketMaximumRunning: Type.Optional(Type.Integer({ minimum: 1, maximum: 32, description: "Maximum linked running Ticket workflows." })),
  ticketMaximumAttempts: Type.Optional(Type.Integer({ minimum: 1, maximum: 20, description: "Maximum Ticket claim attempts before a retryable failure becomes terminal." })),
  knowledgeEnabled: Type.Optional(Type.Boolean({ description: "Enable the additive SQLite Experience/Lesson store. Retrieval remains optional and never controls durable execution." })),
  externalResearchEnabled: Type.Optional(Type.Boolean({ description: "Enable bounded external-research job storage and evidence ingestion. Network access still requires an explicit capability adapter." })),
}, { additionalProperties: false });

const entry = defineToolPlugin({
  id: "cogentnexus-rotation",
  name: "CogentNexus OpenClaw Bridge",
  description: "Ticket-first OpenClaw bridge for CogentNexus Host-managed continuity, durable execution, recovery, context handoff, and verified delivery.",
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
    }), tool({
      name:"cogent_ticket_status",
      label:"CogentNexus Ticket Status",
      description:"Read deterministic Ticket queue and outbox health without inference.",
      parameters:Type.Object({},{additionalProperties:false}),
      optional:true,
      factory:({config,toolContext})=>({
        name:"cogent_ticket_status",
        label:"CogentNexus Ticket Status",
        description:"Read Ticket runtime status.",
        parameters:Type.Object({},{additionalProperties:false}),
        async execute() {
          const workspaceDir=toolContext.workspaceDir ?? process.cwd();
          const databasePath=config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir);
          const details={...new TicketStore(databasePath).snapshot(),knowledge:config.knowledgeEnabled === false ? {enabled:false} : {enabled:true,...new KnowledgeStore(databasePath).snapshot()},research:config.externalResearchEnabled === false ? {enabled:false} : {enabled:true,...new ExternalResearchStore(databasePath).snapshot()}};
          return {content:[{type:"text",text:JSON.stringify(details)}],details};
        },
      }),
    }), tool({
      name:"cogent_knowledge",
      label:"CogentNexus Knowledge",
      description:"Record evidence-backed experience, manage verified lessons, retrieve FTS matches with provenance, and record application outcomes.",
      parameters:Type.Object({
        action:Type.Union([Type.Literal("experience"),Type.Literal("candidate"),Type.Literal("verify"),Type.Literal("contradict"),Type.Literal("retire"),Type.Literal("search"),Type.Literal("apply"),Type.Literal("status")]),
        lessonId:Type.Optional(Type.String()), ticketId:Type.Optional(Type.String()), kind:Type.Optional(Type.String()), summary:Type.Optional(Type.String()), guidance:Type.Optional(Type.String()),
        evidenceRef:Type.Optional(Type.String()), query:Type.Optional(Type.String()), outcome:Type.Optional(Type.String()), confidence:Type.Optional(Type.Number({minimum:0,maximum:1})), limit:Type.Optional(Type.Integer({minimum:1,maximum:50})),
      },{additionalProperties:false}),
      optional:true,
      factory:({config,toolContext})=>({
        name:"cogent_knowledge",label:"CogentNexus Knowledge",description:"Use the durable evidence-backed knowledge store.",
        parameters:Type.Object({action:Type.String(),lessonId:Type.Optional(Type.String()),ticketId:Type.Optional(Type.String()),kind:Type.Optional(Type.String()),summary:Type.Optional(Type.String()),guidance:Type.Optional(Type.String()),evidenceRef:Type.Optional(Type.String()),query:Type.Optional(Type.String()),outcome:Type.Optional(Type.String()),confidence:Type.Optional(Type.Number()),limit:Type.Optional(Type.Integer())},{additionalProperties:false}),
        async execute(_id:string,params:any) {
          if(config.knowledgeEnabled === false) throw new Error("CogentNexus knowledge capability is disabled");
          if(!["search","status"].includes(params.action) && !toolContext.sessionKey) throw new Error("knowledge mutations require a trusted OpenClaw session context");
          const workspaceDir=toolContext.workspaceDir ?? process.cwd(),databasePath=config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir),store=new KnowledgeStore(databasePath);
          let details:unknown;
          if(params.action === "status") details=store.snapshot();
          else if(params.action === "search") details=store.search(params.query ?? "",{limit:params.limit});
          else if(params.action === "experience") details=store.recordExperience({ticketId:params.ticketId,kind:params.kind as ExperienceKind,summary:params.summary ?? "",evidenceRef:params.evidenceRef ?? ""});
          else if(params.action === "candidate") details=store.createCandidate({summary:params.summary ?? "",guidance:params.guidance ?? "",evidenceRef:params.evidenceRef ?? "",confidence:params.confidence});
          else if(["verify","contradict","retire"].includes(params.action)) details=store.transition({lessonId:params.lessonId ?? "",action:params.action,evidenceRef:params.evidenceRef ?? "",confidence:params.confidence});
          else if(params.action === "apply") details=store.recordApplication({lessonId:params.lessonId ?? "",ticketId:params.ticketId,outcome:params.outcome as ApplicationOutcome,evidenceRef:params.evidenceRef ?? ""});
          else throw new Error("unsupported knowledge action");
          return {content:[{type:"text",text:JSON.stringify(details)}],details};
        },
      }),
    }), tool({
      name:"cogent_research",
      label:"CogentNexus External Research",
      description:"Manage bounded external-research jobs and ingest untrusted source evidence as external observations. This tool does not promote lessons.",
      parameters:Type.Object({
        action:Type.Union([Type.Literal("create"),Type.Literal("start"),Type.Literal("query"),Type.Literal("observe"),Type.Literal("claim"),Type.Literal("finish"),Type.Literal("block"),Type.Literal("fail"),Type.Literal("cancel"),Type.Literal("get"),Type.Literal("status")]),
        jobId:Type.Optional(Type.String()),ticketId:Type.Optional(Type.String()),question:Type.Optional(Type.String()),reason:Type.Optional(Type.String()),query:Type.Optional(Type.String()),queryId:Type.Optional(Type.String()),
        internalCoverage:Type.Optional(Type.Number({minimum:0,maximum:1})),internalConfidence:Type.Optional(Type.Number({minimum:0,maximum:1})),freshnessSensitive:Type.Optional(Type.Boolean()),networkAllowed:Type.Optional(Type.Boolean()),
        url:Type.Optional(Type.String()),publisher:Type.Optional(Type.String()),sourceType:Type.Optional(Type.String()),body:Type.Optional(Type.String()),contentType:Type.Optional(Type.String()),publishedAt:Type.Optional(Type.String()),
        claim:Type.Optional(Type.String()),evidence:Type.Optional(Type.Array(Type.Object({observationId:Type.String(),relation:Type.String()}))),
      },{additionalProperties:false}),
      optional:true,
      factory:({config,toolContext})=>({
        name:"cogent_research",label:"CogentNexus External Research",description:"Use the bounded external-research evidence store.",
        parameters:Type.Object({action:Type.String(),jobId:Type.Optional(Type.String()),ticketId:Type.Optional(Type.String()),question:Type.Optional(Type.String()),reason:Type.Optional(Type.String()),query:Type.Optional(Type.String()),queryId:Type.Optional(Type.String()),internalCoverage:Type.Optional(Type.Number()),internalConfidence:Type.Optional(Type.Number()),freshnessSensitive:Type.Optional(Type.Boolean()),networkAllowed:Type.Optional(Type.Boolean()),url:Type.Optional(Type.String()),publisher:Type.Optional(Type.String()),sourceType:Type.Optional(Type.String()),body:Type.Optional(Type.String()),contentType:Type.Optional(Type.String()),publishedAt:Type.Optional(Type.String()),claim:Type.Optional(Type.String()),evidence:Type.Optional(Type.Array(Type.Any()))},{additionalProperties:false}),
        async execute(_id:string,params:any){
          if(config.externalResearchEnabled === false) throw new Error("CogentNexus external research capability is disabled");
          if(!["get","status"].includes(params.action) && !toolContext.sessionKey) throw new Error("research mutations require a trusted OpenClaw session context");
          const workspaceDir=toolContext.workspaceDir ?? process.cwd(),databasePath=config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir),store=new ExternalResearchStore(databasePath); let details:unknown;
          if(params.action==="status") details=store.snapshot();
          else if(params.action==="get") details=store.get(params.jobId ?? "");
          else if(params.action==="create") details=store.createJob({ticketId:params.ticketId,question:params.question ?? "",reason:params.reason ?? "",internalCoverage:params.internalCoverage ?? 0,internalConfidence:params.internalConfidence ?? 0,freshnessSensitive:params.freshnessSensitive,networkAllowed:params.networkAllowed});
          else if(params.action==="start") details=store.start(params.jobId ?? "");
          else if(params.action==="query") details=store.addQuery(params.jobId ?? "",params.query ?? "");
          else if(params.action==="observe") details=store.addObservation({jobId:params.jobId ?? "",queryId:params.queryId,url:params.url ?? "",publisher:params.publisher,sourceType:params.sourceType as SourceType,body:params.body ?? "",contentType:params.contentType,publishedAt:params.publishedAt});
          else if(params.action==="claim") details=store.addClaim({jobId:params.jobId ?? "",claim:params.claim ?? "",evidence:(params.evidence ?? []) as Array<{observationId:string;relation:ClaimRelation}>});
          else if(params.action==="finish") details=store.finish(params.jobId ?? "");
          else if(params.action==="block") details=store.block(params.jobId ?? "",params.reason ?? "");
          else if(params.action==="fail") details=store.fail(params.jobId ?? "",params.reason ?? "");
          else if(params.action==="cancel") details=store.cancel(params.jobId ?? "",params.reason ?? "");
          else throw new Error("unsupported research action");
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
  const deliveryTargets = new Map<string,DeliveryTarget>();
  const runWorkspaces = new Map<string,string>();
  const runSessions = new Map<string,string>();
  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const settleRunDelivery = (runId:string,success:boolean,error?:string) => {
    const timer=deliveryTimers.get(runId); if(timer){clearTimeout(timer);deliveryTimers.delete(runId);}
    const workspaceDir=resolve(runWorkspaces.get(runId) ?? config.workspaceDir ?? process.cwd());
    const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
    if(success) store.confirmDirectDelivery({runId}); else store.failDirectDelivery({runId,message:error});
    const target=deliveryTargets.get(runId);
    if(target) settleDeliveryTarget({workspaceDir,store,target,success,error});
    deliveryTargets.delete(runId); runWorkspaces.delete(runId); runSessions.delete(runId); dispatcherObservedRuns.delete(runId);
  };
  api.on("before_tool_call", (event, ctx) => enforcementDecision(event.toolName, event.params, ctx.sessionKey, config.enforcedMode !== false), { priority: 1000 });
  if (config.preInferenceAdmission !== false) api.on("before_agent_run", (event, ctx) => {
    const currentRunId=ctx.runId;
    const currentWorkspace=resolve(ctx.workspaceDir ?? config.workspaceDir ?? process.cwd());
    if(currentRunId){runWorkspaces.set(currentRunId,currentWorkspace);if(ctx.sessionKey)runSessions.set(currentRunId,ctx.sessionKey);}
    const deliveryTarget=parseDeliveryMarker(event.prompt);
    if(deliveryTarget){
      if(currentRunId){
        const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(currentWorkspace));
        if(bindDeliveryRun({workspaceDir:currentWorkspace,store,target:deliveryTarget,runId:currentRunId})) deliveryTargets.set(currentRunId,deliveryTarget);
      }
      return {outcome:"pass"};
    }
    // Trigger names vary by channel/dispatch path (for example WebChat and
    // sessions_send do not consistently report "user"). Trust the resolved
    // owner bit and canonical session shape instead; classifier exclusions
    // fence internal completion and continuation messages.
    if (!durableAdmissionEligible({sessionKey:ctx.sessionKey,senderIsOwner:event.senderIsOwner})) return { outcome:"pass" };
    const ownerSessionKey = ctx.sessionKey!;
    let acceptedTicket:ReturnType<TicketStore["accept"]> | undefined;
    let ticketStore:TicketStore | undefined;
    if (config.ticketFirst === true && ticketIntakeEligible(event.prompt)) {
      const workspaceDir = ctx.workspaceDir ?? process.cwd();
      const databasePath = config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir);
      ticketStore = new TicketStore(databasePath);
      acceptedTicket = ticketStore.accept({
        runId:ctx.runId ?? randomUUID(),
        ownerSessionKey,
        prompt:event.prompt,
        maxAttempts:config.ticketMaximumAttempts,
      });
    }
    const decision = classifyDurableRequest(event.prompt, config.admissionMinimumScore ?? 5);
    if (acceptedTicket && ticketStore) ticketStore.route(acceptedTicket.ticketId,decision.lane === "durable");
    if (decision.lane !== "durable") return { outcome:"pass" };
    if (acceptedTicket) return {
      outcome:"block",reason:"durable request committed and queued before conversational inference",category:"cogentnexus_ticket_admission",
      metadata:{ticketId:acceptedTicket.ticketId,score:decision.score,componentCount:decision.sections.length,deduplicated:acceptedTicket.duplicate},
      message:`CogentNexus committed Ticket ${acceptedTicket.ticketId} before inference. The resource-admitted dispatcher will start and link its verified workflow; terminal evidence will return automatically.`,
    };
    const workspaceDir = ctx.workspaceDir ?? process.cwd();
    const requestHash = durableRequestFingerprint(event.prompt);
    const duplicate = activeWorkflowForRequest(workspaceDir, requestHash);
    const intake = duplicate ? undefined : compileDurableIntake({
      workspaceDir,
      prompt:event.prompt,
      runId:ctx.runId ?? randomUUID(),
      decision,
      model:config.durableWorkerModel ?? "qwen3.5:9b-32k",
    });
    const started = duplicate ?? startBoundWorkflow({workspaceDir,manifestPath:intake!.manifestPath,ownerSessionKey:ownerSessionKey,pythonCommand:config.pythonCommand});
    const componentCount = intake?.componentCount ?? decision.sections.length;
    return {
      outcome:"block",
      reason:"durable request admitted before conversational inference",
      category:"cogentnexus_durable_admission",
      metadata:{taskId:started.taskId,score:decision.score,componentCount,deduplicated:Boolean(duplicate)},
      message:`CogentNexus ${duplicate ? "reused" : "admitted"} durable workflow ${started.taskId} before model inference. ${componentCount} bounded components run through the deterministic controller and Ollama without a temporary Codex worker; verified completion will return automatically.`,
    };
  }, { priority: 2000, timeoutMs: 30_000 });
  if (config.ticketFirst === true) api.on("reply_dispatch", (event, ctx) => {
    const runId=event.runId;
    if(!runId || !ctx.dispatcher.appendBeforeDeliver) return;
    let started=false;
    ctx.dispatcher.appendBeforeDeliver((payload,info)=>{
      if(info.kind==="final" && !started){
        started=true; dispatcherObservedRuns.add(runId);
        queueMicrotask(()=>{void (async()=>{
          try {
            await ctx.dispatcher.waitForIdle();
            const failed=ctx.dispatcher.getFailedCounts().final;
            const cancelled=ctx.dispatcher.getCancelledCounts?.().final ?? 0;
            settleRunDelivery(runId,failed===0 && cancelled===0,failed>0?`final delivery failed count=${failed}`:cancelled>0?`final delivery cancelled count=${cancelled}`:undefined);
          } catch(error) { settleRunDelivery(runId,false,error instanceof Error?error.message:String(error)); }
        })();});
      }
      return payload;
    });
  }, { priority: 500 });

  if (config.ticketFirst === true) api.on("message_sent", (event, ctx) => {
    const sessionKey=event.sessionKey ?? ctx.sessionKey;
    let runId=event.runId;
    if(!runId && sessionKey){
      const candidates=[...runSessions.entries()].filter(([,key])=>key===sessionKey);
      runId=candidates.at(-1)?.[0];
    }
    if(!runId || dispatcherObservedRuns.has(runId)) return;
    const previous=deliveryTimers.get(runId); if(previous) clearTimeout(previous);
    if(!event.success){settleRunDelivery(runId,false,event.error ?? "message_sent reported failure");return;}
    const timer=setTimeout(()=>settleRunDelivery(runId!,true),config.directDeliverySettleMs ?? 15000);
    timer.unref?.(); deliveryTimers.set(runId,timer);
  }, { priority: 50 });

  if (config.autoResume !== false && config.ticketFirst === true) api.on("after_compaction", async (_event, ctx) => {
    if(!ctx.sessionKey) return;
    const workspaceDir=resolve(ctx.workspaceDir ?? config.workspaceDir ?? process.cwd());
    const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
    try {
      await schedulePostCompactionResume({sessionKey:ctx.sessionKey,workspaceDir,store,delayMs:config.postCompactionResumeDelayMs,workflow:api.session.workflow});
    } catch(error) { api.logger.warn(`CogentNexus post-compaction continuation scheduling failed: ${error instanceof Error?error.message:String(error)}`); }
  }, { priority: 100, timeoutMs: 10_000 });

  if (config.autoResume !== false || config.autoRotate === true || config.ticketFirst === true) api.on("agent_end", async (event, ctx) => {
    const runId = event.runId ?? ctx.runId;
    const sessionKey = ctx.sessionKey;
    if(sessionKey) {
      try { await api.session.workflow.unscheduleSessionTurnsByTag({sessionKey,tag:postCompactionResumeTag(sessionKey)}); }
      catch(error) { api.logger.warn(`CogentNexus post-compaction guard cleanup failed: ${error instanceof Error?error.message:String(error)}`); }
    }
    const internalDelivery=Boolean(runId && deliveryTargets.has(runId));
    if(!internalDelivery) await scheduleInterruptedResume({
      success: event.success,
      error: event.error,
      runId,
      sessionKey,
      delayMs: config.autoResumeDelayMs,
      workflow: api.session.workflow,
      scheduledRuns,
    });
    if (config.ticketFirst === true && runId) {
      try {
        const workspaceDir=resolve(ctx.workspaceDir ?? config.workspaceDir ?? process.cwd());
        const store=new TicketStore(config.ticketDatabasePath??defaultTicketDatabase(workspaceDir));
        runWorkspaces.set(runId,workspaceDir); if(sessionKey)runSessions.set(runId,sessionKey);
        const visible=hasVisibleAssistantOutput(event.messages);
        store.finalizeDirectRun({runId,success:event.success,interrupted:isResumableInterruption(event.success,event.error),message:event.error??"",expectsDelivery:visible});
        if(!event.success){
          const timer=deliveryTimers.get(runId);if(timer)clearTimeout(timer);deliveryTimers.delete(runId);
          if(internalDelivery)settleRunDelivery(runId,false,event.error??"delivery run interrupted");
        } else if(internalDelivery && !visible) settleRunDelivery(runId,false,"delivery continuation produced no visible assistant output");
        else if(!visible){runWorkspaces.delete(runId);runSessions.delete(runId);}
      } catch(error) { api.logger.warn(`CogentNexus direct Ticket finalization failed: ${error instanceof Error?error.message:String(error)}`); }
    }
    if (event.success && config.autoRotate === true && sessionKey) {
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
            for (const item of pendingWorkflowCompletions(workspaceDir,new Date(),config.outboxDeliveryTimeoutMs ?? 300000)) {
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
  if (config.ticketFirst === true) {
    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    api.registerService({
      id: "cogentnexus-ticket-recovery",
      start: async (ctx: any) => {
        const workspaceDir = resolve(config.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const store = new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
        const tick = async () => {
          if (active) return;
          active = true;
          try {
            const undelivered=store.recoverUndeliveredDirect({olderThanMs:config.directDeliveryTimeoutMs ?? 120000});
            for (const item of undelivered) api.logger.warn(`CogentNexus promoted unconfirmed direct delivery ${item.ticketId} (${item.runId}) to durable recovery`);
            const recovered = store.recoverExpired();
            for (const item of recovered) api.logger.warn(`CogentNexus recovered expired Ticket ${item.ticketId} from worker ${item.previousWorkerId ?? "unknown"} generation ${item.previousLeaseGeneration}`);
            for (const item of reconcileTicketWorkflows({workspaceDir,store,config})) api.logger.info?.(`CogentNexus Ticket ${item.ticketId} workflow action ${item.action}`);
            const dispatched = dispatchTicketWorkflows({workspaceDir,store,config});
            if (!dispatched.admission.admitted) api.logger.info?.(`CogentNexus Ticket dispatch deferred: ${dispatched.admission.reasons.join(",")}`);
            for (const item of store.pendingOutbox(100,new Date(),config.outboxDeliveryTimeoutMs ?? 300000)) {
              try { await deliverTicketOutbox(api,store,item); }
              catch (error) { api.logger.warn(`CogentNexus Ticket completion delivery failed for ${item.ticketId}: ${error instanceof Error ? error.message : String(error)}`); }
            }
          } catch (error) {
            api.logger.error(`CogentNexus Ticket recovery scan failed: ${error instanceof Error ? error.message : String(error)}`);
          } finally { active = false; }
        };
        await tick();
        interval = setInterval(() => { void tick(); }, Math.min(config.ticketRecoveryPollMs ?? 15_000,config.ticketOutboxPollMs ?? 5000,config.ticketDispatchPollMs ?? 5000));
        interval.unref?.();
      },
      stop: async () => { if (interval) clearInterval(interval); interval = undefined; },
    });
  }
};

export default entry;
