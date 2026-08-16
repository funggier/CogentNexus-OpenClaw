import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
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
  settleDeliveryTarget,
  ticketDeliveryMarker,
  workflowDeliveryIsRetryable,
  workflowDeliveryMarker,
} from "./delivery-continuity.js";
import { TicketStore } from "./ticket-store.js";

describe("delivery continuity",()=>{
  it("detects whether agent_end contains visible assistant output",()=>{
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[{type:"text",text:"done"}]}])).toBe(true);
    expect(hasVisibleAssistantOutput([{role:"assistant",content:[{type:"toolCall",name:"x"}]}])).toBe(false);
    expect(hasVisibleAssistantOutput([{role:"user",content:"hello"}])).toBe(false);
  });

  it("round-trips deterministic Ticket and workflow delivery markers",()=>{
    const ticket=ticketDeliveryMarker(17);
    expect(parseDeliveryMarker(ticket)).toEqual({kind:"ticket",outboxId:17});
    const workflow=workflowDeliveryMarker("WF-1",9);
    expect(parseDeliveryMarker(workflow)).toEqual({kind:"workflow",taskId:"WF-1",stateRevision:9});
    expect(parseDeliveryMarker("normal text")).toBeUndefined();
  });

  it("keeps workflow completion pending after scheduling and commits only after delivery receipt",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-delivery-"));
    try {
      const taskId="WF-DELIVERY",dir=join(root,".cogent","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json"),notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:test",workflowStatus:"completed",stateRevision:4,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice));
      const scheduled=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      expect(scheduled.deliveryStatus).toBe("pending");
      expect(scheduled.scheduledAt).toBe("2026-08-15T00:00:01.000Z");
      const store=new TicketStore(join(root,"tickets.sqlite3"));
      const target={kind:"workflow" as const,taskId,stateRevision:4};
      expect(bindDeliveryRun({workspaceDir:root,store,target,runId:"delivery-run"})).toBe(true);
      let saved=JSON.parse(readFileSync(path,"utf8"));
      expect(saved).toMatchObject({deliveryStatus:"pending",deliveryRunId:"delivery-run"});
      expect(settleDeliveryTarget({workspaceDir:root,store,target,success:true})).toBe(true);
      saved=JSON.parse(readFileSync(path,"utf8"));
      expect(saved.deliveryStatus).toBe("delivered");
      expect(saved.deliveredAt).toBeTruthy();
      expect(saved.scheduledAt).toBeUndefined();
      expect(saved.deliveryRunId).toBeUndefined();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("returns a failed workflow delivery to pending retry state",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-retry-"));
    try {
      const taskId="WF-RETRY",dir=join(root,".cogent","workflows",taskId);mkdirSync(dir,{recursive:true});
      const path=join(dir,"completion.json"),notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:test",workflowStatus:"completed",stateRevision:1,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice));
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
