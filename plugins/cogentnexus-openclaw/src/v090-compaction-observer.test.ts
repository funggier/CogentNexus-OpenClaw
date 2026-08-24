import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { installPassiveCompactionObserver } from "./v090-compaction-boundary.js";
import { TicketStore } from "./ticket-store.js";

function fixture(root:string) {
  const path=join(root,"tickets.sqlite3"),sessionKey="agent:main:dashboard:A",store=new TicketStore(path);
  const ticket=store.accept({runId:"run-compact",ownerSessionKey:sessionKey,prompt:"long task"});store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT);
    CREATE TABLE IF NOT EXISTS cnx_context_maintenance(
      session_key TEXT PRIMARY KEY,owner_generation INTEGER NOT NULL,ticket_id TEXT NOT NULL,state TEXT NOT NULL,
      hard_required INTEGER NOT NULL DEFAULT 0,attempt_count INTEGER NOT NULL DEFAULT 0,next_attempt_at TEXT,last_error TEXT,
      session_id TEXT,context_window INTEGER,projected_tokens INTEGER,last_tokens_before INTEGER,last_tokens_after INTEGER,
      last_action TEXT,capsule_path TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,completed_at TEXT);`);
  db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',9,?,?)").run(sessionKey,stamp,stamp);
  db.prepare(`INSERT INTO cnx_context_maintenance(session_key,owner_generation,ticket_id,state,hard_required,attempt_count,next_attempt_at,
    session_id,context_window,projected_tokens,created_at,updated_at) VALUES (?,?,?,'pending',1,0,?,'physical-old',32768,30000,?,?)`)
    .run(sessionKey,9,ticket.ticketId,stamp,stamp,stamp);
  db.close();
  return {path,sessionKey,ticketId:ticket.ticketId};
}

function observerApi() {
  let handler:any;let gatewayCalls=0;
  const api={
    on:(name:string,fn:any)=>{if(name==="after_compaction")handler=fn;},
    runtime:{gateway:{request:async()=>{gatewayCalls++;return {session:{contextTokens:32768,totalTokens:6000,totalTokensFresh:true,sessionId:"rpc-session"}};}}},
    logger:{info:()=>{}},
  };
  return {api,get handler(){return handler;},get gatewayCalls(){return gatewayCalls;}};
}

describe("v0.9 passive manual Compact observer",()=>{
  it("settles an existing hold from native tokenCount plus stored window without any Gateway RPC",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-compact-zero-rpc-"));
    try{
      const fx=fixture(root),capture=observerApi();
      installPassiveCompactionObserver(capture.api,{workspaceDir:root,ticketDatabasePath:fx.path});
      await capture.handler({tokenCount:6200},{sessionKey:fx.sessionKey,workspaceDir:root});
      expect(capture.gatewayCalls).toBe(0);
      const db=new DatabaseSync(fx.path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action,last_tokens_after,context_window FROM cnx_context_maintenance WHERE session_key=?").get(fx.sessionKey))
        .toEqual({state:"done",last_action:"native-compact-satisfied",last_tokens_after:6200,context_window:32768});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=? AND event_type='context_compaction_satisfied'").get(fx.ticketId))
        .toEqual({count:1});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("performs zero Gateway RPC when the session has no active context hold",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-compact-no-hold-"));
    try{
      const fx=fixture(root),db=new DatabaseSync(fx.path);db.prepare("UPDATE cnx_context_maintenance SET state='done',completed_at=? WHERE session_key=?").run(new Date().toISOString(),fx.sessionKey);db.close();
      const capture=observerApi();installPassiveCompactionObserver(capture.api,{workspaceDir:root,ticketDatabasePath:fx.path});
      await capture.handler({tokenCount:5000},{sessionKey:fx.sessionKey,workspaceDir:root});
      expect(capture.gatewayCalls).toBe(0);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("uses a single sessions.describe fallback only when an active hold lacks sufficient measurement",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-compact-rpc-fallback-"));
    try{
      const fx=fixture(root),db=new DatabaseSync(fx.path);db.prepare("UPDATE cnx_context_maintenance SET context_window=NULL WHERE session_key=?").run(fx.sessionKey);db.close();
      const capture=observerApi();installPassiveCompactionObserver(capture.api,{workspaceDir:root,ticketDatabasePath:fx.path});
      await capture.handler({}, {sessionKey:fx.sessionKey,workspaceDir:root});
      expect(capture.gatewayCalls).toBe(1);
      const verify=new DatabaseSync(fx.path,{readOnly:true});
      expect(verify.prepare("SELECT state,last_action,last_tokens_after FROM cnx_context_maintenance WHERE session_key=?").get(fx.sessionKey))
        .toEqual({state:"done",last_action:"native-compact-satisfied",last_tokens_after:6000});verify.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
