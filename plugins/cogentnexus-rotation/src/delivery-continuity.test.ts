import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  bindDeliveryRun,
  hasPendingSessionWork,
  hasVisibleAssistantOutput,
  markWorkflowDeliveryScheduled,
  parseDeliveryMarker,
  postCompactionResumeTag,
  settleDeliveryTarget,
  ticketDeliveryMarker,
  workflowDeliveryIsRetryable,
  workflowDeliveryMarker,
} from "./delivery-continuity.js";
import { TicketStore } from "./ticket-store.js";

describe("delivery continuity", () => {
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
    expect(ticket).toBe("[CogentNexus Delivery: ticket:42]");
    expect(workflow).toBe("[CogentNexus Delivery: workflow:WF-ABC:7]");
    expect(parseDeliveryMarker(ticket)).toEqual({kind:"ticket",outboxId:42});
    expect(parseDeliveryMarker(workflow)).toEqual({kind:"workflow",taskId:"WF-ABC",stateRevision:7});
    expect(parseDeliveryMarker("ordinary user message")).toBeUndefined();
    expect(postCompactionResumeTag("agent:main:owner/1")).toMatch(/^cogent-post-compact-/);
  });

  it("keeps workflow completion pending after scheduling and commits only after delivery receipt", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-workflow-delivery-"));
    try {
      const taskId="WF-DELIVERY";
      const workflowDir=join(root,".cogent","workflows",taskId);
      mkdirSync(workflowDir,{recursive:true});
      const path=join(workflowDir,"completion.json");
      const notice={schemaVersion:1,taskId,ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:3,createdAt:"2026-08-15T00:00:00.000Z",deliveryStatus:"pending"};
      writeFileSync(path,JSON.stringify(notice),"utf8");
      const scheduled=markWorkflowDeliveryScheduled(path,notice,new Date("2026-08-15T00:00:01.000Z"));
      expect(scheduled).toMatchObject({deliveryStatus:"pending",deliveryAttempts:1,scheduledAt:"2026-08-15T00:00:01.000Z"});
      expect(workflowDeliveryIsRetryable(scheduled,new Date("2026-08-15T00:04:59.000Z"),300_000)).toBe(false);
      expect(workflowDeliveryIsRetryable(scheduled,new Date("2026-08-15T00:05:02.000Z"),300_000)).toBe(true);

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
      const taskId="WF-FAIL",workflowDir=join(root,".cogent","workflows",taskId);mkdirSync(workflowDir,{recursive:true});
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
  });
});