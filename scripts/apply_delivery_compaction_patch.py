#!/usr/bin/env python3
"""Temporary branch helper: apply v0.8 delivery/compaction continuity patch.

Delete this file after the patch is committed and normal validation passes.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing patch anchor: {label}")
    return text.replace(old, new, 1)


def patch_ticket_store() -> None:
    path = ROOT / "plugins/cogentnexus-rotation/src/ticket-store.ts"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "  deliveryAttempts: number;\n};",
        "  deliveryAttempts: number;\n  scheduledAt?: string | null;\n  deliveryRunId?: string | null;\n};",
        "TicketOutbox fields",
    )
    text = replace_once(
        text,
        "  result_json TEXT,\n  workflow_eligible INTEGER NOT NULL DEFAULT 0,",
        "  result_json TEXT,\n  response_ready_at TEXT,\n  delivery_confirmed_at TEXT,\n  delivery_last_error TEXT,\n  workflow_eligible INTEGER NOT NULL DEFAULT 0,",
        "ticket delivery columns",
    )
    text = replace_once(
        text,
        "  last_delivery_error TEXT,\n  created_at TEXT NOT NULL,",
        "  last_delivery_error TEXT,\n  scheduled_at TEXT,\n  delivery_run_id TEXT,\n  created_at TEXT NOT NULL,",
        "outbox receipt columns",
    )
    text = replace_once(
        text,
        '      this.ensureColumn(db,"tickets","result_json","TEXT");\n      this.ensureColumn(db,"tickets","workflow_eligible","INTEGER NOT NULL DEFAULT 0");',
        '      this.ensureColumn(db,"tickets","result_json","TEXT");\n      this.ensureColumn(db,"tickets","response_ready_at","TEXT");\n      this.ensureColumn(db,"tickets","delivery_confirmed_at","TEXT");\n      this.ensureColumn(db,"tickets","delivery_last_error","TEXT");\n      this.ensureColumn(db,"tickets","workflow_eligible","INTEGER NOT NULL DEFAULT 0");',
        "ticket migration columns",
    )
    text = replace_once(
        text,
        '      this.ensureColumn(db,"tickets","manifest_path","TEXT");\n      db.exec("CREATE INDEX IF NOT EXISTS idx_tickets_recovery ON tickets(status, lease_expires_at)");\n      const applied = new Date().toISOString();\n      for (const version of [1,2,3,4,5])',
        '      this.ensureColumn(db,"tickets","manifest_path","TEXT");\n      this.ensureColumn(db,"ticket_outbox","scheduled_at","TEXT");\n      this.ensureColumn(db,"ticket_outbox","delivery_run_id","TEXT");\n      db.exec("CREATE INDEX IF NOT EXISTS idx_tickets_recovery ON tickets(status, lease_expires_at)");\n      db.exec("CREATE INDEX IF NOT EXISTS idx_tickets_direct_delivery ON tickets(status, workflow_eligible, response_ready_at, delivery_confirmed_at)");\n      const applied = new Date().toISOString();\n      for (const version of [1,2,3,4,5,6])',
        "schema migration v6",
    )

    direct_methods = r'''  finalizeDirectRun(input:{runId:string;success:boolean;interrupted:boolean;message?:string;expectsDelivery?:boolean;now?:Date}): "completed"|"awaiting_delivery"|"waiting"|"failed"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      if (input.success) {
        const expectsDelivery=input.expectsDelivery !== false;
        const payload={runId:input.runId,direct:true,expectsDelivery};
        if (!expectsDelivery) {
          db.prepare("UPDATE tickets SET status='completed',result_json=?,response_ready_at=?,delivery_confirmed_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
            .run(JSON.stringify(payload),nowIso,nowIso,nowIso,nowIso,row.ticket_id);
          this.event(db,row.ticket_id,"response_ready",payload,nowIso);
          this.event(db,row.ticket_id,"delivery_confirmed",{runId:input.runId,required:false},nowIso);
          this.event(db,row.ticket_id,"completed",payload,nowIso);
          db.exec("COMMIT"); return "completed";
        }
        db.prepare("UPDATE tickets SET result_json=?,response_ready_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
          .run(JSON.stringify(payload),nowIso,nowIso,row.ticket_id);
        this.event(db,row.ticket_id,"response_ready",payload,nowIso);
        db.exec("COMMIT"); return "awaiting_delivery";
      }
      const status=input.interrupted?"waiting":"failed";
      const classification=input.interrupted?"interrupted":"permanent";
      const message=(input.message??(input.interrupted?"direct run interrupted":"direct run failed")).slice(0,2000);
      db.prepare("UPDATE tickets SET status=?,workflow_eligible=?,failure_class=?,failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(status,input.interrupted?1:0,classification,message,message,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,input.interrupted?"promoted_to_durable":"failed",{runId:input.runId,classification,message},nowIso);
      if (!input.interrupted) this.enqueueTerminal(db,row.ticket_id,"failed",{classification,message},nowIso);
      db.exec("COMMIT"); return status;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  confirmDirectDelivery(input:{runId:string;now?:Date}): "completed"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      db.prepare("UPDATE tickets SET status='completed',delivery_confirmed_at=?,delivery_last_error=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(nowIso,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,"delivery_confirmed",{runId:input.runId},nowIso);
      this.event(db,row.ticket_id,"completed",{runId:input.runId,direct:true,deliveryConfirmed:true},nowIso);
      db.exec("COMMIT"); return "completed";
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  failDirectDelivery(input:{runId:string;message?:string;now?:Date}): "waiting"|"unchanged" {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    const message=(input.message??"direct reply delivery failed").slice(0,2000);
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
      if (!row) { db.exec("COMMIT"); return "unchanged"; }
      db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'")
        .run(message,message,nowIso,row.ticket_id);
      this.event(db,row.ticket_id,"direct_delivery_failed",{runId:input.runId,message},nowIso);
      db.exec("COMMIT"); return "waiting";
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  pendingDirectRunForSession(sessionKey:string): string|undefined {
    const db=this.open();
    try {
      const row=db.prepare("SELECT run_id FROM tickets WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL ORDER BY response_ready_at DESC LIMIT 1").get(sessionKey) as any;
      return row?.run_id;
    } finally { db.close(); }
  }

  recoverUndeliveredDirect(input:{now?:Date;olderThanMs?:number;limit?:number}={}): Array<{ticketId:string;runId:string}> {
    const db=this.open();
    const now=input.now??new Date();
    const cutoff=new Date(now.getTime()-Math.max(1000,input.olderThanMs??120000)).toISOString();
    const nowIso=now.toISOString();
    const limit=Math.max(1,Math.min(input.limit??100,1000));
    try {
      db.exec("BEGIN IMMEDIATE");
      const rows=db.prepare("SELECT ticket_id,run_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL AND response_ready_at<=? ORDER BY response_ready_at,ticket_id LIMIT ?").all(cutoff,limit) as any[];
      const recovered:Array<{ticketId:string;runId:string}>=[];
      for (const row of rows) {
        const message="direct response was ready but final delivery was not confirmed before the receipt deadline";
        const changed=db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted' AND delivery_confirmed_at IS NULL")
          .run(message,message,nowIso,row.ticket_id);
        if (changed.changes!==1) continue;
        this.event(db,row.ticket_id,"direct_delivery_timeout",{runId:row.run_id,cutoff},nowIso);
        recovered.push({ticketId:row.ticket_id,runId:row.run_id});
      }
      db.exec("COMMIT"); return recovered;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  hasNonTerminalForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM tickets WHERE owner_session_key=? AND status NOT IN ('completed','failed','cancelled') LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }

  hasPendingOutboxForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM ticket_outbox WHERE owner_session_key=? AND delivery_status='pending' LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }
'''
    text, count = re.subn(
        r"  finalizeDirectRun\([\s\S]*?\n  get\(ticketId: string\): TicketRecord \| undefined \{",
        direct_methods + "\n  get(ticketId: string): TicketRecord | undefined {",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("failed to replace finalizeDirectRun block")

    outbox_methods = r'''  pendingOutbox(limit = 100, now = new Date(), retryAfterMs = 300_000): TicketOutbox[] {
    const db = this.open();
    const cutoff = new Date(now.getTime() - Math.max(1_000, retryAfterMs)).toISOString();
    try {
      return (db.prepare(`SELECT outbox_id,ticket_id,owner_session_key,terminal_status,payload_json,delivery_attempts,scheduled_at,delivery_run_id
        FROM ticket_outbox WHERE delivery_status='pending' AND (scheduled_at IS NULL OR scheduled_at<=?) ORDER BY outbox_id LIMIT ?`).all(cutoff,Math.max(1,Math.min(limit,1000))) as any[])
        .map((row) => ({outboxId:Number(row.outbox_id),ticketId:row.ticket_id,ownerSessionKey:row.owner_session_key,
          terminalStatus:row.terminal_status,payload:JSON.parse(row.payload_json),deliveryAttempts:Number(row.delivery_attempts),scheduledAt:row.scheduled_at,deliveryRunId:row.delivery_run_id}));
    } finally { db.close(); }
  }

  markOutboxScheduled(outboxId:number, runId?:string, now=new Date()): boolean {
    const db=this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET delivery_attempts=delivery_attempts+1,scheduled_at=?,delivery_run_id=?,last_delivery_error=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(now.toISOString(),runId??null,outboxId).changes===1;
    } finally { db.close(); }
  }

  bindOutboxRun(outboxId:number, runId:string): boolean {
    const db=this.open();
    try {
      return db.prepare("UPDATE ticket_outbox SET delivery_run_id=?,last_delivery_error=NULL WHERE outbox_id=? AND delivery_status='pending'")
        .run(runId,outboxId).changes===1;
    } finally { db.close(); }
  }

  markOutboxDelivered(outboxId: number, now = new Date()): boolean {
    const db = this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET delivery_status='delivered',delivered_at=?,last_delivery_error=NULL,scheduled_at=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(now.toISOString(),outboxId).changes === 1;
    } finally { db.close(); }
  }

  markOutboxFailed(outboxId: number, message: string): boolean {
    const db = this.open();
    try {
      return db.prepare(`UPDATE ticket_outbox SET last_delivery_error=?,scheduled_at=NULL,delivery_run_id=NULL
        WHERE outbox_id=? AND delivery_status='pending'`).run(message.slice(0,2000),outboxId).changes === 1;
    } finally { db.close(); }
  }
'''
    text, count = re.subn(
        r"  pendingOutbox\([\s\S]*?\n  snapshot\(now = new Date\(\)\) \{",
        outbox_methods + "\n  snapshot(now = new Date()) {",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("failed to replace outbox methods")

    text = replace_once(
        text,
        r'return !/\[(?:CogentNexus|Subagent) Context\]|cogent-workflow-result-|cogent-resume-|The previous run was interrupted\./iu.test(prompt);',
        r'return !/\[(?:CogentNexus|Subagent) Context\]|\[CogentNexus (?:Delivery|Continuation):|cogent-workflow-result-|cogent-resume-|The previous run was interrupted\./iu.test(prompt);',
        "internal continuation exclusion",
    )
    path.write_text(text, encoding="utf-8")


def patch_index() -> None:
    path = ROOT / "plugins/cogentnexus-rotation/src/index.ts"
    text = path.read_text(encoding="utf-8")

    anchor = 'import { ExternalResearchStore, type ClaimRelation, type SourceType } from "./external-research.js";\n'
    extra = 'import { bindDeliveryRun, hasPendingSessionWork, hasVisibleAssistantOutput, markWorkflowDeliveryScheduleFailed, markWorkflowDeliveryScheduled, parseDeliveryMarker, postCompactionResumeTag, settleDeliveryTarget, ticketDeliveryMarker, workflowDeliveryIsRetryable, workflowDeliveryMarker, type DeliveryTarget } from "./delivery-continuity.js";\n'
    text = replace_once(text, anchor, anchor + extra, "delivery import")

    text = replace_once(
        text,
        "  autoResumeDelayMs?: number;\n  autoRotate?: boolean;",
        "  autoResumeDelayMs?: number;\n  directDeliverySettleMs?: number;\n  directDeliveryTimeoutMs?: number;\n  outboxDeliveryTimeoutMs?: number;\n  postCompactionResumeDelayMs?: number;\n  autoRotate?: boolean;",
        "RotationConfig delivery fields",
    )
    text = replace_once(
        text,
        "  lastDeliveryError?: string;\n};",
        "  lastDeliveryError?: string;\n  scheduledAt?: string;\n  deliveryRunId?: string;\n};",
        "WorkflowCompletion delivery fields",
    )
    text = replace_once(
        text,
        "  return [\n    `CogentNexus workflow ${notice.taskId} reached terminal status ${notice.workflowStatus}.`,",
        "  return [\n    workflowDeliveryMarker(notice.taskId, notice.stateRevision ?? 0),\n    `CogentNexus workflow ${notice.taskId} reached terminal status ${notice.workflowStatus}.`,",
        "workflow delivery marker",
    )
    text = replace_once(
        text,
        "export function pendingWorkflowCompletions(workspaceDir: string): Array<{ path: string; notice: WorkflowCompletion }> {",
        "export function pendingWorkflowCompletions(workspaceDir: string, now = new Date(), retryAfterMs = 300_000): Array<{ path: string; notice: WorkflowCompletion }> {",
        "workflow retry signature",
    )
    text = replace_once(
        text,
        '      if (notice.schemaVersion === 1 && notice.taskId === entry.name && notice.deliveryStatus === "pending" &&\n          typeof notice.ownerSessionKey === "string" && notice.ownerSessionKey.length > 0) found.push({ path, notice });',
        '      if (notice.schemaVersion === 1 && notice.taskId === entry.name && workflowDeliveryIsRetryable(notice, now, retryAfterMs) &&\n          typeof notice.ownerSessionKey === "string" && notice.ownerSessionKey.length > 0) found.push({ path, notice });',
        "workflow retry filter",
    )

    delivery_block = r'''export async function deliverWorkflowCompletion(api: any, path: string, notice: WorkflowCompletion) {
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
'''
    text, count = re.subn(
        r"function markCompletionDelivered\([\s\S]*?\nexport function ticketOutboxTag",
        delivery_block + "\nexport function ticketOutboxTag",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("failed to replace workflow delivery block")

    ticket_delivery = r'''export async function deliverTicketOutbox(api: any, store: TicketStore, item: TicketOutbox) {
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
'''
    text, count = re.subn(
        r"export async function deliverTicketOutbox\([\s\S]*?\n}\n\nexport function enforcementDecision",
        ticket_delivery + "\nexport function enforcementDecision",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("failed to replace ticket outbox delivery block")

    post_compaction = r'''
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
'''
    text = replace_once(
        text,
        "export async function scheduleInterruptedResume(input: {",
        post_compaction + "\nexport async function scheduleInterruptedResume(input: {",
        "post-compaction helper",
    )

    text = replace_once(
        text,
        '  autoResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000 })),\n  autoRotate:',
        '  autoResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000 })),\n  directDeliverySettleMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 60000, description: "Quiet period after fallback message_sent receipts before a direct Ticket is considered delivered." })),\n  directDeliveryTimeoutMs: Type.Optional(Type.Integer({ minimum: 10000, maximum: 3600000, description: "Maximum time a response-ready direct Ticket may remain without confirmed final delivery before durable recovery." })),\n  outboxDeliveryTimeoutMs: Type.Optional(Type.Integer({ minimum: 10000, maximum: 3600000, description: "Retry age for a scheduled terminal delivery that never receives a delivery receipt." })),\n  postCompactionResumeDelayMs: Type.Optional(Type.Integer({ minimum: 1000, maximum: 120000, description: "Delayed fallback continuation scheduled after successful compaction while durable work remains." })),\n  autoRotate:',
        "config schema delivery fields",
    )

    registration = '''  const config = (api.pluginConfig ?? {}) as RotationConfig;\n  const scheduledRuns = new Set<string>();\n'''
    registration_new = r'''  const config = (api.pluginConfig ?? {}) as RotationConfig;
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
'''
    text = replace_once(text, registration, registration_new, "registration state")

    before_run = '  if (config.preInferenceAdmission !== false) api.on("before_agent_run", (event, ctx) => {\n'
    before_run_new = r'''  if (config.preInferenceAdmission !== false) api.on("before_agent_run", (event, ctx) => {
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
'''
    text = replace_once(text, before_run, before_run_new, "before_agent_run delivery binding")

    agent_end_anchor = '  if (config.autoResume !== false || config.autoRotate === true || config.ticketFirst === true) api.on("agent_end", async (event, ctx) => {\n'
    delivery_hooks = r'''  if (config.ticketFirst === true) api.on("reply_dispatch", (event, ctx) => {
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
'''
    text = replace_once(text, agent_end_anchor, delivery_hooks, "delivery/compaction hooks")

    old_end = '''    const runId = event.runId ?? ctx.runId;\n    const sessionKey = ctx.sessionKey;\n    await scheduleInterruptedResume({\n      success: event.success,\n      error: event.error,\n      runId,\n      sessionKey,\n      delayMs: config.autoResumeDelayMs,\n      workflow: api.session.workflow,\n      scheduledRuns,\n    });\n    if (config.ticketFirst === true && runId) {\n      try {\n        const workspaceDir=ctx.workspaceDir??process.cwd(),store=new TicketStore(config.ticketDatabasePath??defaultTicketDatabase(workspaceDir));\n        store.finalizeDirectRun({runId,success:event.success,interrupted:isResumableInterruption(event.success,event.error),message:event.error??\"\"});\n      } catch(error) { api.logger.warn(`CogentNexus direct Ticket finalization failed: ${error instanceof Error?error.message:String(error)}`); }\n    }\n'''
    new_end = r'''    const runId = event.runId ?? ctx.runId;
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
'''
    text = replace_once(text, old_end, new_end, "agent_end delivery gate")

    text = replace_once(
        text,
        "            for (const item of pendingWorkflowCompletions(workspaceDir)) {",
        "            for (const item of pendingWorkflowCompletions(workspaceDir,new Date(),config.outboxDeliveryTimeoutMs ?? 300000)) {",
        "workflow delivery retry interval",
    )
    text = replace_once(
        text,
        "            const recovered = store.recoverExpired();\n            for (const item of recovered)",
        "            const undelivered=store.recoverUndeliveredDirect({olderThanMs:config.directDeliveryTimeoutMs ?? 120000});\n            for (const item of undelivered) api.logger.warn(`CogentNexus promoted unconfirmed direct delivery ${item.ticketId} (${item.runId}) to durable recovery`);\n            const recovered = store.recoverExpired();\n            for (const item of recovered)",
        "undelivered direct recovery scan",
    )
    text = replace_once(
        text,
        "            for (const item of store.pendingOutbox()) {",
        "            for (const item of store.pendingOutbox(100,new Date(),config.outboxDeliveryTimeoutMs ?? 300000)) {",
        "ticket outbox retry interval",
    )
    path.write_text(text, encoding="utf-8")


def patch_host() -> None:
    path = ROOT / "skills/cogentnexus/scripts/host.py"
    text = path.read_text(encoding="utf-8")
    if "hooks.allowConversationAccess" in text:
        return
    anchor = '    for key, value in settings:\n        run(["openclaw", "config", "set", f"plugins.entries.{PLUGIN_ID}.config.{key}", value], timeout=60, check=True)\n'
    replacement = anchor + '    run(["openclaw", "config", "set", f"plugins.entries.{PLUGIN_ID}.hooks.allowConversationAccess", "true"], timeout=60, check=True)\n'
    text = replace_once(text, anchor, replacement, "conversation hook access")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_ticket_store()
    patch_index()
    patch_host()
    print("delivery/compaction patch applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
