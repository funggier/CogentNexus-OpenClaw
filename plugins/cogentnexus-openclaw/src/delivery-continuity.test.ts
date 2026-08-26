import { existsSync, mkdtempSync, mkdirSync, readFileSync, rmSync, unlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  bindDeliveryRun,
  hasPendingSessionWork,
  hasVisibleAssistantOutput,
  markWorkflowDeliveryScheduleFailed,
  markWorkflowDeliveryScheduled,
  parseDeliveryMarker,
  postCompactionResumeTag,
  publishCompletionLock,
  settleDeliveryTarget,
  ticketDeliveryMarker,
  withCompletionLock,
  workflowDeliveryIsRetryable,
  workflowDeliveryMarker,
} from "./delivery-continuity.js";
import { TicketStore } from "./ticket-store.js";

describe("delivery continuity", () => {
  it("does not expose a canonical lock when owner publication is interrupted", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-lock-publication-crash-"));
    try {
      const dir=join(root,".cogentnexus-openclaw","workflows","WF-LOCK-CRASH");mkdirSync(dir,{recursive:true});
      const lockPath=join(dir,"completion.json.lock"),record={pid:process.pid,token:"publication-test-token",acquiredAt:"2026-08-15T00:00:00.000Z"};
      const interrupt=(..._args:any[]) => { const error=new Error("synthetic publication interruption") as NodeJS.ErrnoException; error.code="EINTR"; throw error; };
      expect(() => publishCompletionLock(lockPath,record,interrupt)).toThrow(/publication interruption/);
      expect(existsSync(lockPath)).toBe(false);
      expect(existsSync(`${lockPath}.${process.pid}.${record.token}.tmp`)).toBe(false);
      publishCompletionLock(lockPath,record);
      expect(JSON.parse(readFileSync(lockPath,"utf8"))).toEqual(record);
      rmSync(lockPath,{force:true});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("publishes complete lock metadata before critical-section visibility", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-lock-visible-record-"));
    try {
      const path=join(root,"completion.json");
      expect(withCompletionLock(path,() => {
        const lock=JSON.parse(readFileSync(`${path}.lock`,"utf8"));
        expect(lock).toEqual(expect.objectContaining({pid:process.pid,token:expect.any(String),acquiredAt:expect.any(String)}));
        return true;
      })).toBe(true);
      expect(existsSync(`${path}.lock`)).toBe(false);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("does not release a replacement lock owned by another token", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-lock-replacement-"));
    try {
      const path=join(root,"completion.json"),lockPath=`${path}.lock`,replacement={pid:process.pid,token:"replacement-token",acquiredAt:"2026-08-15T00:00:00.000Z"};
      expect(withCompletionLock(path,() => {
        unlinkSync(lockPath);
        publishCompletionLock(lockPath,replacement);
        return true;
      })).toBe(true);
      expect(JSON.parse(readFileSync(lockPath,"utf8"))).toEqual(replacement);
      unlinkSync(lockPath);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("detects whether agent_end contains visible assistant output", () => {
    expect(hasVisibleAssistantOutput([])).toBe(false);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[]}])).toBe(false);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[{type:"text",text:""}]}])).toBe(false);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[{type:"text",text:"hello"}]}])).toBe(true);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:"hello"}])).toBe(true);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[{type:"image"}]}])).toBe(true);
  });

  it("round-trips deterministic Ticket and workflow delivery markers", () => {
    const ticket=ticketDeliveryMarker(42);
    const workflow=workflowDeliveryMarker("WF-ABC",7);
    expect(ticket).toBe("[CogentNexus-OpenClaw Delivery: ticket:42]");
    expect(workflow).toBe("[CogentNexus-OpenClaw Delivery: workflow:WF-ABC:7]");
    expect(parseDeliveryMarker(ticket)).toEqual({kind:"ticket",outboxId:42});
    expect(parseDeliveryMarker(workflow)).toEqual({kind:"workflow",taskId:"WF-ABC",stateRevision:7});
    expect(parseDeliveryMarker("ordinary user message")).toBeUndefined();
    expect(postCompactionResumeTag("agent:main:owner/1")).toMatch(/^cogent-post-compact-/);
  });

  it("keeps workflow completion pending after scheduling and commits only after delivery receipt", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-delivery-"));
    try {
      const taskId="WF-DELIVERY";
      const workflowDir=join(root,".cogentnexus-openclaw","workflows",taskId);
      mkdirSync(workflowDir,{recursive:true});
      const path=join(workflowDir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:3,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const scheduled=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      expect(scheduled).toMatchObject({deliveryStatus:"pending",deliveryAttempts:1,scheduledAt:"2026-08-15T00:00:01.000Z"});
      expect(scheduled).toBeDefined();
      expect(workflowDeliveryIsRetryable(scheduled!,new Date("2026-08-15T00:04:59.000Z"),300_000)).toBe(false);
      expect(workflowDeliveryIsRetryable(scheduled!,new Date("2026-08-15T00:05:02.000Z"),300_000)).toBe(true);

      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:3};
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"delivery-run",now:new Date("2026-08-15T00:00:02.000Z")})).toBe(true);
      expect(JSON.parse(readFileSync(path,"utf8"))).toMatchObject({deliveryStatus:"pending",deliveryRunId:"delivery-run"});
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,now:new Date("2026-08-15T00:00:03.000Z")})).toBe(true);
      expect(JSON.parse(readFileSync(path,"utf8"))).toMatchObject({deliveryStatus:"delivered",deliveredAt:"2026-08-15T00:00:03.000Z"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("returns a failed workflow delivery to pending retry state", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-delivery-fail-"));
    try {
      const taskId="WF-FAIL",workflowDir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(workflowDir,{recursive:true});
      const path=join(workflowDir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:1,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:1};
      bindDeliveryRun({workspaceDir:root,store,target,runId:"delivery-run"});
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:false,error:"channel interrupted"})).toBe(true);
      const saved=JSON.parse(readFileSync(path,"utf8"));
      expect(saved).toMatchObject({deliveryStatus:"pending",lastDeliveryError:"channel interrupted"});
      expect(saved.scheduledAt).toBeUndefined();
      expect(saved.deliveryRunId).toBeUndefined();
      expect(workflowDeliveryIsRetryable(saved)).toBe(true);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("rejects a Ticket delivery marker from the wrong owner session", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-ticket-marker-owner-")),path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
    try {
      const ticket=store.accept({runId:"marker-owner",ownerSessionKey:"agent:main:dashboard:owner-a",prompt:"failed work"});
      store.route(ticket.ticketId,true);
      const lease=store.claim({ticketId:ticket.ticketId,workerId:"marker-worker",leaseMs:10_000})!;
      store.complete({...lease,result:{ok:true}});
      const outbox=store.pendingOutbox()[0];
      expect(outbox).toBeTruthy();
      expect((bindDeliveryRun as any)({workspaceDir:root,store,target:{kind:"ticket",outboxId:outbox.outboxId},runId:"owner-b-run",sessionKey:"agent:main:dashboard:owner-b"})).toBe(false);
      expect(store.pendingOutbox()[0].deliveryRunId).toBeNull();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("does not reschedule a workflow completion after it is delivered", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-delivery-stale-"));
    try {
      const taskId="WF-STALE",workflowDir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(workflowDir,{recursive:true});
      const path=join(workflowDir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:2,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const first=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:2};
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,now:new Date("2026-08-15T00:00:02.000Z")})).toBe(true);
      expect((markWorkflowDeliveryScheduled as any)(path,first,new Date("2026-08-15T00:00:03.000Z"))).toBeUndefined();
      expect(JSON.parse(readFileSync(path,"utf8"))).toMatchObject({deliveryStatus:"delivered",deliveredAt:"2026-08-15T00:00:02.000Z"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("rejects an unbound workflow run from terminal settlement", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-unbound-run-"));
    try {
      const taskId="WF-UNBOUND",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:6,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:6};
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,runId:"unbound-run",sessionKey:"agent:main:owner"})).toBe(false);
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:false,runId:"unbound-run",sessionKey:"agent:main:owner",error:"must remain pending"})).toBe(false);
      expect(JSON.parse(readFileSync(path,"utf8"))).toMatchObject({deliveryStatus:"pending"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("does not let stale schedule failure overwrite delivered state", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-stale-failure-"));
    try {
      const taskId="WF-STALE-FAIL",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:4,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const scheduled=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"))!;
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:4};
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"run-new",sessionKey:"agent:main:owner",now:new Date("2026-08-15T00:00:01.500Z")})).toBe(true);
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,runId:"run-new",now:new Date("2026-08-15T00:00:02.000Z")})).toBe(true);
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"run-stale",now:new Date("2026-08-15T00:00:03.000Z")})).toBe(false);
      expect((markWorkflowDeliveryScheduleFailed as any)(path,scheduled,"synthetic schedule error")).toBeUndefined();
      expect(JSON.parse(readFileSync(path,"utf8"))).toMatchObject({deliveryStatus:"delivered",deliveredAt:"2026-08-15T00:00:02.000Z"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("serializes workflow binding behind a live completion lock", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-bind-lock-"));
    try {
      const taskId="WF-BIND-LOCK",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:1,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      writeFileSync(`${path}.lock`,JSON.stringify({pid:process.pid,token:"live-test-owner",acquiredAt:new Date().toISOString()}),"utf8");
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      expect(bindDeliveryRun({workspaceDir:root,store,target:{kind:"workflow",taskId,stateRevision:1},runId:"run-bind"})).toBe(false);
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryRunId).toBeUndefined();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("recovers a deterministically abandoned completion lock", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-abandoned-lock-"));
    try {
      const taskId="WF-ABANDONED",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:1,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      writeFileSync(`${path}.lock`,JSON.stringify({pid:999999,token:"dead-owner",acquiredAt:"2020-01-01T00:00:00.000Z"}),"utf8");
      expect(markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"))).toMatchObject({deliveryAttempts:1});
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryStatus).toBe("pending");
      expect(() => readFileSync(`${path}.lock`)).toThrow();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("rejects a different workflow delivery run after the first bind", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-run-fence-"));
    try {
      const taskId="WF-RUN-FENCE",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:1,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:1};
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"run-a"})).toBe(true);
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"run-a"})).toBe(true);
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"run-b"})).toBe(false);
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,runId:"run-b"})).toBe(false);
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true,runId:"run-a"})).toBe(true);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("converges repeated scheduling and permits one retry after rollback", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-retry-convergence-"));
    try {
      const taskId="WF-RETRY",dir=join(root,".cogentnexus-openclaw","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:5,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const first=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      expect(first).toMatchObject({deliveryAttempts:1});
      expect(markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:02.000Z"))).toBeUndefined();
      const retry=markWorkflowDeliveryScheduleFailed(path,first!,"temporary scheduling failure");
      expect(retry).toMatchObject({deliveryStatus:"pending",deliveryAttempts:1});
      const second=markWorkflowDeliveryScheduled(path,retry!,new Date("2026-08-15T00:00:03.000Z"));
      expect(second).toMatchObject({deliveryAttempts:2});
      expect(markWorkflowDeliveryScheduled(path,retry!,new Date("2026-08-15T00:00:04.000Z"))).toBeUndefined();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
  it("reports pending session work after a Ticket is durably accepted", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-pending-session-"));
    try {
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const session="agent:main:owner";
      expect(hasPendingSessionWork(root,store,session)).toBe(false);
      const ticket=store.accept({runId:"run",ownerSessionKey:session,prompt:"do work"});
      expect(hasPendingSessionWork(root,store,session)).toBe(true);
      store.route(ticket.ticketId,false);
      store.finalizeDirectRun({runId:"run",success:true,interrupted:false,expectsDelivery:false});
      expect(hasPendingSessionWork(root,store,session)).toBe(false);
    } finally { rmSync(root,{recursive:true,force:true}); }
  }, 15_000);
});
