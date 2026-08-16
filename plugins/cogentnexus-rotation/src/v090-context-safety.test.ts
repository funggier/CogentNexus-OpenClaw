import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { evaluateContextPressure, installContextSafety } from "./v090-context-safety.js";

function setupDb(root:string,sessionKey="agent:main:dashboard:A") {
  const path=join(root,"tickets.sqlite3");
  const store=new TicketStore(path);
  const ticket=store.accept({runId:"run-1",ownerSessionKey:sessionKey,prompt:"continue the long task"});
  store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path);
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    generation INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT,
    delete_reason TEXT
  )`);
  const stamp=new Date().toISOString();
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',4,?,?)")
    .run(sessionKey,stamp,stamp);
  db.close();
  return {path,store,ticket};
}

describe("v0.9 context safety",()=>{
  it("uses a more conservative soft boundary for a 32K local-model window",()=>{
    const pressure=evaluateContextPressure({
      messages:[{role:"user",content:"x".repeat(1000)}],
      prompt:"next",
      session:{contextTokens:32768,totalTokens:23000,totalTokensFresh:true},
    });
    expect(pressure.contextWindow).toBe(32768);
    expect(pressure.softLimit).toBeLessThan(24000);
    expect(pressure.level).toBe("soft");
  });

  it("keeps a low-pressure session on normal owner inference",()=>{
    const pressure=evaluateContextPressure({
      messages:[{role:"user",content:"hello"}],
      prompt:"next",
      session:{contextTokens:32768,totalTokens:8000,totalTokensFresh:true},
    });
    expect(pressure.level).toBe("normal");
  });

  it("commits context maintenance and Direct Recovery before a nearly-full owner run can call the model",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-v090-context-"));
    try {
      const sessionKey="agent:main:dashboard:A";
      const {path,ticket}=setupDb(root,sessionKey);
      let beforeAgentRun:any;
      let service:any;
      const registrationApi={
        on:(name:string,handler:any)=>{if(name==="before_agent_run")beforeAgentRun=handler;},
        registerService:(value:any)=>{service=value;},
      };
      const api={
        runtime:{gateway:{request:async(method:string)=>{
          if(method==="sessions.describe") return {session:{key:sessionKey,sessionId:"session-old",contextTokens:32768,totalTokens:30000,totalTokensFresh:true}};
          throw new Error(`unexpected ${method}`);
        }}},
        logger:{info:()=>{},warn:()=>{}},
      };
      installContextSafety(api,registrationApi,{workspaceDir:root,ticketDatabasePath:path});
      expect(typeof beforeAgentRun).toBe("function");
      expect(service?.id).toBe("cogentnexus-context-maintenance-v090");
      const decision=await beforeAgentRun({prompt:"continue",messages:[],systemPrompt:""},{sessionKey,runId:"run-1",workspaceDir:root});
      expect(decision.outcome).toBe("block");
      expect(decision.category).toBe("cogentnexus_context_pressure");
      expect(decision.metadata.ticketId).toBe(ticket.ticketId);
      expect(decision.metadata.pressure.level).toBe("hard");

      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,hard_required,owner_generation,ticket_id FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"pending",hard_required:1,owner_generation:4,ticket_id:ticket.ticketId});
      expect(db.prepare("SELECT state,owner_generation FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"pending",owner_generation:4});
      expect(db.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"accepted",failure_class:"interrupted"});
      db.close();
    } finally {rmSync(root,{recursive:true,force:true});}
  });

  it("does not apply the context gate to a non-ticketed/internal run",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-v090-context-internal-"));
    try {
      const path=join(root,"tickets.sqlite3");
      new TicketStore(path).snapshot();
      let handler:any;
      installContextSafety(
        {runtime:{gateway:{request:async()=>({session:{contextTokens:32768,totalTokens:32000,totalTokensFresh:true}})}},logger:{}},
        {on:(name:string,value:any)=>{if(name==="before_agent_run")handler=value;},registerService:()=>{}},
        {workspaceDir:root,ticketDatabasePath:path},
      );
      const decision=await handler({prompt:"internal",messages:[]},{sessionKey:"agent:main:dashboard:A",runId:"no-ticket",workspaceDir:root});
      expect(decision).toEqual({outcome:"pass"});
    } finally {rmSync(root,{recursive:true,force:true});}
  });
});
