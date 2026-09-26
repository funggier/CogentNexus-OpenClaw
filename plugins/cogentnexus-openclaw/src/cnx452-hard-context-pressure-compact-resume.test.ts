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
  const ticket=store.accept({runId,ownerSessionKey:sessionKey,prompt:"continue"});
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

function harness(input:{root:string;path:string;sessionKey:string;compactSucceeds:boolean}) {
  let hook:any;
  let compactCalls=0;
  let compacted=false;
  const registration={
    on:(name:string,fn:any)=>{if(name==="before_agent_run")hook=fn;},
    registerService:()=>{},
  };
  const api={
    runtime:{gateway:{request:async(method:string)=>{
      if(method==="sessions.describe")return {session:{
        key:input.sessionKey,
        sessionId:"physical-cnx452",
        contextTokens:24576,
        totalTokens:compacted?12000:23000,
        totalTokensFresh:true,
      }};
      if(method==="sessions.compact"){
        compactCalls+=1;
        if(input.compactSucceeds){
          compacted=true;
          return {ok:true,compacted:true,result:{tokensBefore:23000,tokensAfter:12000}};
        }
        return {ok:false,compacted:false};
      }
      if(method==="chat.history")return {messages:[]};
      throw new Error(`unexpected gateway method ${method}`);
    }}},
    logger:{info:()=>{},warn:()=>{}},
  };
  installContextGuard(api,registration,{
    workspaceDir:input.root,
    ticketDatabasePath:input.path,
    contextCompactionTimeoutMs:30000,
    contextHardTrimMaxLines:60,
  });
  return {hook,getCompactCalls:()=>compactCalls};
}

describe("CNX-452 hard context pressure compact/resume",()=>{
  it("compacts inline and resumes the same accepted owner turn when hard pressure becomes safe",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx452-inline-"));
    try{
      const sessionKey="agent:main:dashboard:cnx452-inline";
      const runId="cnx452-inline-run";
      const {path,ticket}=setup(root,runId,sessionKey);
      const {hook,getCompactCalls}=harness({root,path,sessionKey,compactSucceeds:true});

      const decision=await hook(
        {prompt:"continue",messages:[{role:"assistant",content:"x".repeat(60000)}],systemPrompt:"system"},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:24576},
      );

      expect(decision).toEqual({outcome:"pass"});
      expect(getCompactCalls()).toBe(1);

      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:null,failure_message:null});
      const recoveryExists=Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get());
      expect(recoveryExists ? db.prepare("SELECT count(*) AS n FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId) : {n:0})
        .toEqual({n:0});
      expect(db.prepare("SELECT state,hard_required,last_action,last_tokens_before,last_tokens_after FROM cnx_context_maintenance WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"done",hard_required:1,last_action:"semantic-compact",last_tokens_before:23000,last_tokens_after:12000});
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='context_pressure_hard_observed'").get(ticket.ticketId))
        .toEqual({n:1});
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='context_pressure_inline_resolved'").get(ticket.ticketId))
        .toEqual({n:1});
      db.close();
    }finally{
      rmSync(root,{recursive:true,force:true});
    }
  });
  it("fails closed without Direct recovery when bounded compaction cannot establish a safe context",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx452-unresolved-"));
    try{
      const sessionKey="agent:main:dashboard:cnx452-unresolved";
      const runId="cnx452-unresolved-run";
      const {path,ticket}=setup(root,runId,sessionKey);
      const {hook,getCompactCalls}=harness({root,path,sessionKey,compactSucceeds:false});

      const decision=await hook(
        {prompt:"continue",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:24576},
      );

      expect(decision).toMatchObject({
        outcome:"block",
        category:"cnxclaw_context_pressure_unresolved",
        metadata:{ticketId:ticket.ticketId,pressure:{level:"hard",contextWindow:24576}},
      });
      expect(getCompactCalls()).toBeGreaterThan(0);

      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:null,failure_message:null});
      const recoveryExists=Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get());
      expect(recoveryExists ? db.prepare("SELECT count(*) AS n FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId) : {n:0})
        .toEqual({n:0});
      expect(db.prepare("SELECT state,hard_required,last_action FROM cnx_context_maintenance WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"cancelled",hard_required:1,last_action:"inline-maintenance-error"});
      expect(db.prepare("SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='context_pressure_inline_unresolved'").get(ticket.ticketId))
        .toEqual({n:1});
      db.close();
    }finally{
      rmSync(root,{recursive:true,force:true});
    }
  });


});
