import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installContextGuard } from "./v091-context-guard.js";

function setup(root:string, runId:string, sessionKey:string) {
  const path=join(root,"tickets.sqlite3");
  const store=new TicketStore(path);
  const ticket=store.accept({runId,ownerSessionKey:sessionKey,prompt:"ขอแบบเจาะลึกลงรายละเอียดครับ"});
  store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path);
  const stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT)`);
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',0,?,?)")
    .run(sessionKey,stamp,stamp);
  db.close();
  return {path,ticket};
}

function hookHarness(input:{
  root:string;
  path:string;
  sessionKey:string;
  totalTokens:number;
  contextTokens:number;
}) {
  let hook:any;
  const registration={
    on:(name:string,fn:any)=>{if(name==="before_agent_run")hook=fn;},
    registerService:()=>{},
  };
  const api={
    runtime:{gateway:{request:async(method:string)=>{
      if(method==="sessions.describe")return {session:{
        key:input.sessionKey,
        sessionId:"physical-cnx451",
        contextTokens:input.contextTokens,
        totalTokens:input.totalTokens,
        totalTokensFresh:true,
      }};
      throw new Error(`unexpected ${method}`);
    }}},
    logger:{info:()=>{},warn:()=>{}},
  };
  installContextGuard(api,registration,{workspaceDir:input.root,ticketDatabasePath:input.path});
  return hook;
}

describe("CNX-451 soft context pressure",()=>{
  it("does not block the live 21093/24576 soft-pressure topology",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx451-soft-"));
    try{
      const sessionKey="agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8";
      const runId="7483411c-296b-4ee9-8ea2-7d7c434a4712";
      const {path,ticket}=setup(root,runId,sessionKey);
      const hook=hookHarness({root,path,sessionKey,totalTokens:21089,contextTokens:24576});
      const decision=await hook(
        {prompt:"ขอแบบเจาะลึกลงรายละเอียดครับ",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:24576},
      );

      expect(decision).toEqual({outcome:"pass"});

      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:null,failure_message:null});
      const recoveryExists=Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get());
      expect(recoveryExists ? db.prepare("SELECT count(*) AS n FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId) : {n:0})
        .toEqual({n:0});
      expect(db.prepare("SELECT count(*) AS n FROM cnx_context_maintenance WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({n:0});
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='context_pressure_soft_observed'").get(ticket.ticketId))
        .toEqual({n:1});
      db.close();
    } finally {
      rmSync(root,{recursive:true,force:true});
    }
  });

  it("preserves fail-closed hard-pressure safety when inline compaction cannot establish a safe context",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx451-hard-"));
    try{
      const sessionKey="agent:main:dashboard:cnx451-hard";
      const runId="cnx451-hard-run";
      const {path,ticket}=setup(root,runId,sessionKey);
      const hook=hookHarness({root,path,sessionKey,totalTokens:23000,contextTokens:24576});
      const decision=await hook(
        {prompt:"continue",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:24576},
      );

      expect(decision).toMatchObject({
        outcome:"block",
        category:"cnxclaw_context_pressure_unresolved",
        metadata:{ticketId:ticket.ticketId,pressure:{level:"hard",contextWindow:24576}},
      });

      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,hard_required,last_action FROM cnx_context_maintenance WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"cancelled",hard_required:1,last_action:"inline-maintenance-error"});
      const recoveryExists=Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type=\'table\' AND name=\'cnx_direct_recovery\'").get());
      expect(recoveryExists ? db.prepare("SELECT count(*) AS n FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId) : {n:0})
        .toEqual({n:0});
      expect(db.prepare("SELECT status,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:null,failure_message:null});
      db.close();
    } finally {
      rmSync(root,{recursive:true,force:true});
    }
  });
});
