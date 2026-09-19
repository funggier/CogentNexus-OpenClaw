import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { settleExistingContextHoldFromCompaction } from "./v090-compaction-boundary.js";
import { installContextGuard } from "./v091-context-guard.js";

function setup(root:string,runId:string,sessionKey="agent:main:dashboard:model-switch") {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
  const ticket=store.accept({runId,ownerSessionKey:sessionKey,prompt:"model switch probe"});
  store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT)`);
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',7,?,?)")
    .run(sessionKey,stamp,stamp);
  db.close();
  return {path,ticket,sessionKey};
}

function harness(input:{
  root:string;
  path:string;
  sessionKey:string;
  describedContextTokens:number;
  totalTokens:number;
  totalTokensFresh?:boolean;
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
        sessionId:"physical-model-switch",
        contextTokens:input.describedContextTokens,
        totalTokens:input.totalTokens,
        totalTokensFresh:input.totalTokensFresh??true,
      }};
      throw new Error(`unexpected ${method}`);
    }}},
    logger:{info:()=>{},warn:()=>{}},
  };
  installContextGuard(api,registration,{workspaceDir:input.root,ticketDatabasePath:input.path});
  return hook;
}

afterEach(()=>vi.useRealTimers());

describe("CNX-426 model-switch-aware context budget",()=>{
  it("does not false-block a turn that switched from a stale 32K session window to a 262K effective turn budget",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx426-upswitch-"));
    try{
      const runId="run-upswitch",{path,sessionKey}=setup(root,runId);
      const hook=harness({root,path,sessionKey,describedContextTokens:32768,totalTokens:28425});
      const decision=await hook(
        {prompt:"ตอบแค่ CNXOK",messages:[],systemPrompt:""},
        {
          sessionKey,
          runId,
          workspaceDir:root,
          modelProviderId:"ollama",
          modelId:"qwen3.8:27b",
          contextTokenBudget:262144,
          contextWindowSource:"modelsConfig",
          contextWindowReferenceTokens:262144,
        },
      );
      expect(decision).toEqual({outcome:"pass"});
      const db=new DatabaseSync(path,{readOnly:true});
      const maintenance=db.prepare("SELECT * FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey);
      const events=db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=(SELECT ticket_id FROM tickets WHERE run_id=?) ORDER BY event_id").all(runId);
      db.close();
      expect(maintenance).toBeUndefined();
      expect(events).not.toContainEqual({event_type:"context_pressure_deferred"});
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("uses the smaller effective turn budget after a model switch instead of trusting a stale large session window",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx426-downswitch-"));
    try{
      const runId="run-downswitch",{path,ticket,sessionKey}=setup(root,runId);
      const hook=harness({root,path,sessionKey,describedContextTokens:262144,totalTokens:38000});
      const decision=await hook(
        {prompt:"continue",messages:[],systemPrompt:""},
        {
          sessionKey,
          runId,
          workspaceDir:root,
          modelProviderId:"ollama",
          modelId:"qwen3:1.7b",
          contextTokenBudget:40960,
          contextWindowSource:"modelsConfig",
          contextWindowReferenceTokens:40960,
        },
      );
      expect(decision).toMatchObject({
        outcome:"block",
        category:"cnxclaw_context_pressure",
        metadata:{ticketId:ticket.ticketId,pressure:{contextWindow:40960}},
      });
      const db=new DatabaseSync(path,{readOnly:true});
      const row=db.prepare("SELECT context_window,projected_tokens FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey);
      db.close();
      expect(row).toEqual({context_window:40960,projected_tokens:38004});
    }finally{rmSync(root,{recursive:true,force:true});}
  });


  it("keeps the stored turn budget authoritative when passive compaction observes a stale larger session window",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx426-passive-compact-"));
    try{
      const runId="run-passive-compact",{path,sessionKey}=setup(root,runId);
      const hook=harness({root,path,sessionKey,describedContextTokens:262144,totalTokens:38000});
      expect(await hook(
        {prompt:"continue",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:40960},
      )).toMatchObject({outcome:"block",metadata:{pressure:{contextWindow:40960}}});
      const result=settleExistingContextHoldFromCompaction({
        databasePath:path,
        sessionKey,
        tokenCount:38000,
        session:{contextTokens:262144,totalTokens:38000,totalTokensFresh:true,sessionId:"physical-model-switch"},
      });
      expect(result).toMatchObject({
        found:true,
        settled:false,
        reason:"pressure-remains",
        observedTokens:38000,
        contextWindow:40960,
      });
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action,context_window FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"pending",last_action:"native-compact-observed-pressure-remains",context_window:40960});
      db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("uses the stored turn budget during maintenance instead of accepting compaction against a stale larger session window",async()=>{
    vi.useFakeTimers();
    const root=mkdtempSync(join(tmpdir(),"cnx426-maintenance-"));
    try{
      const runId="run-maintenance",{path,sessionKey}=setup(root,runId);
      let hook:any,service:any,hardTrimmed=false;
      const compactCalls:any[]=[];
      const registration={
        on:(name:string,fn:any)=>{if(name==="before_agent_run")hook=fn;},
        registerService:(value:any)=>{service=value;},
      };
      const api={
        runtime:{gateway:{request:async(method:string,params:any)=>{
          if(method==="sessions.describe")return {session:{
            key:sessionKey,
            sessionId:"physical-model-switch",
            contextTokens:262144,
            totalTokens:hardTrimmed?12000:38000,
            totalTokensFresh:true,
          }};
          if(method==="sessions.compact"){
            compactCalls.push(params);
            if(params?.maxLines!==undefined)hardTrimmed=true;
            return {ok:true,compacted:true,result:{
              tokensBefore:38000,
              tokensAfter:hardTrimmed?12000:38000,
            }};
          }
          throw new Error(`unexpected ${method}`);
        }}},
        logger:{info:()=>{},warn:()=>{}},
      };
      installContextGuard(api,registration,{workspaceDir:root,ticketDatabasePath:path});
      expect(await hook(
        {prompt:"continue",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:40960},
      )).toMatchObject({outcome:"block",metadata:{pressure:{contextWindow:40960}}});
      await service.start({workspaceDir:root});
      await vi.advanceTimersByTimeAsync(1100);
      await Promise.resolve();
      await service.stop();
      expect(compactCalls.some((params)=>params?.maxLines!==undefined)).toBe(true);
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action,context_window FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toMatchObject({state:"done",context_window:40960});
      db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("preserves the legacy session-window fallback when OpenClaw does not provide a valid turn budget",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx426-fallback-"));
    try{
      const runId="run-fallback",{path,ticket,sessionKey}=setup(root,runId);
      const hook=harness({root,path,sessionKey,describedContextTokens:32768,totalTokens:30000});
      const decision=await hook(
        {prompt:"next",messages:[],systemPrompt:""},
        {sessionKey,runId,workspaceDir:root,contextTokenBudget:0},
      );
      expect(decision).toMatchObject({
        outcome:"block",
        category:"cnxclaw_context_pressure",
        metadata:{ticketId:ticket.ticketId,pressure:{contextWindow:32768}},
      });
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});