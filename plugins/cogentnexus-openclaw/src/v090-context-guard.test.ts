import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { contextPressure, installContextGuard } from "./v090-context-guard.js";

function setup(root:string,sessionKey="agent:main:dashboard:A") {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
  const ticket=store.accept({runId:"run-1",ownerSessionKey:sessionKey,prompt:"continue long task"});
  store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT)`);
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',4,?,?)")
    .run(sessionKey,stamp,stamp);
  db.close();
  return {path,ticket};
}

afterEach(()=>vi.useRealTimers());

describe("v0.9 reload-safe context guard",()=>{
  it("marks a nearly-full 32K session as hard pressure before inference",()=>{
    const value=contextPressure({prompt:"next",messages:[],session:{contextTokens:32768,totalTokens:30000,totalTokensFresh:true}});
    expect(value.level).toBe("hard");
    expect(value.softLimit).toBeLessThan(value.hardLimit);
    expect(value.hardLimit).toBeLessThan(32768);
  });

  it("commits Direct Recovery and context maintenance before owner inference",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-context-guard-"));
    try{
      const sessionKey="agent:main:dashboard:A",{path,ticket}=setup(root,sessionKey);
      let hook:any;
      const registration={on:(name:string,fn:any)=>{if(name==="before_agent_run")hook=fn;},registerService:()=>{}};
      const api={runtime:{gateway:{request:async(method:string)=>{
        if(method==="sessions.describe")return {session:{key:sessionKey,sessionId:"physical-old",contextTokens:32768,totalTokens:30000,totalTokensFresh:true}};
        throw new Error(`unexpected ${method}`);
      }}},logger:{info:()=>{},warn:()=>{}}};
      installContextGuard(api,registration,{workspaceDir:root,ticketDatabasePath:path});
      const decision=await hook({prompt:"continue",messages:[],systemPrompt:""},{sessionKey,runId:"run-1",workspaceDir:root});
      expect(decision).toMatchObject({outcome:"block",category:"cnxclaw_context_pressure",metadata:{ticketId:ticket.ticketId}});
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,hard_required,owner_generation,session_id FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"pending",hard_required:1,owner_generation:4,session_id:"physical-old"});
      expect(db.prepare("SELECT state,owner_generation FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({state:"pending",owner_generation:4});
      db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never hard-trims a replacement physical session when Reset wins during compaction",async()=>{
    vi.useFakeTimers();
    const root=mkdtempSync(join(tmpdir(),"cnx-context-reset-race-"));
    try{
      const sessionKey="agent:main:dashboard:A",{path}=setup(root,sessionKey);
      let hook:any,service:any;
      const calls:Array<{method:string;params:any}>=[];
      let describeCount=0;
      const api={
        runtime:{gateway:{request:async(method:string,params:any)=>{
          calls.push({method,params});
          if(method==="sessions.describe"){
            describeCount++;
            return {session:{key:sessionKey,sessionId:"physical-old",contextTokens:32768,totalTokens:31000,totalTokensFresh:true}};
          }
          if(method==="sessions.compact"){
            const db=new DatabaseSync(path);db.prepare("UPDATE cnx_sessions SET generation=5,updated_at=? WHERE session_key=?")
              .run(new Date().toISOString(),sessionKey);db.close();
            return {ok:false,compacted:false};
          }
          throw new Error(`unexpected ${method}`);
        }}},
        logger:{info:()=>{},warn:()=>{}},
      };
      const registration={
        on:(name:string,fn:any)=>{if(name==="before_agent_run")hook=fn;},
        registerService:(value:any)=>{service=value;},
      };
      installContextGuard(api,registration,{workspaceDir:root,ticketDatabasePath:path,contextMaintenancePollMs:1000});
      await hook({prompt:"continue",messages:[],systemPrompt:""},{sessionKey,runId:"run-1",workspaceDir:root});
      await service.start({workspaceDir:root});
      await vi.advanceTimersByTimeAsync(1100);
      await Promise.resolve();
      await service.stop();
      expect(describeCount).toBeGreaterThanOrEqual(2);
      expect(calls.filter((item)=>item.method==="sessions.compact"&&item.params?.maxLines!==undefined)).toHaveLength(0);
      const db=new DatabaseSync(path,{readOnly:true});
      const row=db.prepare("SELECT state,last_action FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey);
      db.close();
      expect(row).toEqual({state:"cancelled",last_action:"authority-revoked-after-compact"});
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
