#!/usr/bin/env python3
from pathlib import Path

path=Path("plugins/cogentnexus-rotation/src/index.test.ts")
text=path.read_text(encoding="utf-8")
old_import='import entry, { activeWorkflowForRequest, autoResumeTag, completionMessage, deliverTicketOutbox, deliverWorkflowCompletion, dispatchTicketWorkflows, durableAdmissionEligible, enforcementDecision, isResumableInterruption, pendingWorkflowCompletions, reconcileTicketWorkflows, rotationCandidates, rotationIdentity, scheduleInterruptedResume, ticketOutboxTag, ticketResourceAdmission, workflowCompletionTag } from "./index.js";'
new_import='import entry, { activeWorkflowForRequest, autoResumeTag, completionMessage, deliverTicketOutbox, deliverWorkflowCompletion, dispatchTicketWorkflows, durableAdmissionEligible, enforcementDecision, isResumableInterruption, pendingWorkflowCompletions, reconcileTicketWorkflows, rotationCandidates, rotationIdentity, scheduleInterruptedResume, schedulePostCompactionResume, ticketOutboxTag, ticketResourceAdmission, workflowCompletionTag } from "./index.js";'
if old_import not in text: raise SystemExit("index import anchor missing")
text=text.replace(old_import,new_import,1)
old='''  it("finishes TaskFlow, schedules the owner once by tag, and commits delivery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-delivery-"));
    try {
      const path = join(root,"completion.json");
      const notice = {schemaVersion:1,taskId:"WF-2",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:9,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(path, JSON.stringify(notice));
      const scheduled: any[] = [], finished: any[] = [];
      const flow = {flowId:"flow-1",syncMode:"managed",revision:1};
      const taskFlow = {list:()=>[],createManaged:()=>flow,get:()=>flow,finish:(value:any)=>finished.push(value),fail:()=>{ throw new Error("unexpected fail"); }};
      const api = {runtime:{tasks:{managedFlows:{bindSession:()=>taskFlow}}},session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async(value:any)=>scheduled.push(value)}}};
      await deliverWorkflowCompletion(api,path,notice);
      expect(finished).toHaveLength(1);
      expect(scheduled[0]).toMatchObject({sessionKey:"agent:main:owner",tag:"cogent-workflow-result-WF-2-9",deliveryMode:"announce"});
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryStatus).toBe("delivered");
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryAttempts).toBe(1);
    } finally { rmSync(root, { recursive:true, force:true }); }
  });'''
new='''  it("finishes TaskFlow and schedules the owner while delivery remains pending until receipt", async () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-delivery-"));
    try {
      const path = join(root,"completion.json");
      const notice = {schemaVersion:1,taskId:"WF-2",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:9,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(path, JSON.stringify(notice));
      const scheduled: any[] = [], finished: any[] = [];
      const flow = {flowId:"flow-1",syncMode:"managed",revision:1};
      const taskFlow = {list:()=>[],createManaged:()=>flow,get:()=>flow,finish:(value:any)=>finished.push(value),fail:()=>{ throw new Error("unexpected fail"); }};
      const api = {runtime:{tasks:{managedFlows:{bindSession:()=>taskFlow}}},session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async(value:any)=>scheduled.push(value)}}};
      await deliverWorkflowCompletion(api,path,notice);
      expect(finished).toHaveLength(1);
      expect(scheduled[0]).toMatchObject({sessionKey:"agent:main:owner",tag:"cogent-workflow-result-WF-2-9",deliveryMode:"announce"});
      expect(String(scheduled[0].message)).toContain("[CogentNexus Delivery: workflow:WF-2:9]");
      const saved=JSON.parse(readFileSync(path,"utf8"));
      expect(saved.deliveryStatus).toBe("pending");
      expect(saved.deliveryAttempts).toBe(1);
      expect(saved.scheduledAt).toEqual(expect.any(String));
    } finally { rmSync(root, { recursive:true, force:true }); }
  });'''
if old not in text: raise SystemExit("workflow delivery test anchor missing")
text=text.replace(old,new,1)
anchor='''  it("discovers only pending terminal workflow outboxes", () => {'''
insert='''  it("schedules a post-compaction continuation only while durable session work remains", async () => {
    const root=mkdtempSync(join(tmpdir(),"cogent-post-compact-"));
    try {
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const sessionKey="agent:main:owner";
      const ticket=store.accept({runId:"compaction-run",ownerSessionKey:sessionKey,prompt:"long task"});
      store.route(ticket.ticketId,false);
      const scheduled:any[]=[],unscheduled:any[]=[];
      const workflow={
        async unscheduleSessionTurnsByTag(input:any){unscheduled.push(input);},
        async scheduleSessionTurn(input:any){scheduled.push(input);},
      };
      await expect(schedulePostCompactionResume({sessionKey,workspaceDir:root,store,workflow,delayMs:2500})).resolves.toBe(true);
      expect(unscheduled).toHaveLength(1);
      expect(scheduled).toHaveLength(1);
      expect(scheduled[0]).toMatchObject({sessionKey,delayMs:2500,deliveryMode:"announce",deleteAfterRun:true});
      expect(String(scheduled[0].tag)).toMatch(/^cogent-post-compact-/);
      expect(String(scheduled[0].message)).toContain("[CogentNexus Continuation: post-compaction]");
      store.finalizeDirectRun({runId:"compaction-run",success:true,interrupted:false,expectsDelivery:false});
      await expect(schedulePostCompactionResume({sessionKey,workspaceDir:root,store,workflow,delayMs:2500})).resolves.toBe(false);
      expect(scheduled).toHaveLength(1);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

'''+anchor
if anchor not in text: raise SystemExit("post-compaction insertion anchor missing")
text=text.replace(anchor,insert,1)
path.write_text(text,encoding="utf-8")
print("index delivery/compaction regression tests updated")
