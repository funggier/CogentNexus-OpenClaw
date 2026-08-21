import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { createCompactionBoundaryApi, settleExistingContextHoldFromCompaction } from "./v090-compaction-boundary.js";
import { installContextGuard } from "./v090-context-guard.js";

function fixture(root:string) {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path),sessionKey="agent:main:dashboard:A";
  const ticket=store.accept({runId:"run-1",ownerSessionKey:sessionKey,prompt:"continue a long direct task"});
  store.route(ticket.ticketId,false);
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT);
    CREATE TABLE IF NOT EXISTS cnx_context_maintenance(
      session_key TEXT PRIMARY KEY,owner_generation INTEGER NOT NULL,ticket_id TEXT NOT NULL,state TEXT NOT NULL,
      hard_required INTEGER NOT NULL DEFAULT 0,attempt_count INTEGER NOT NULL DEFAULT 0,next_attempt_at TEXT,last_error TEXT,
      session_id TEXT,context_window INTEGER,projected_tokens INTEGER,last_tokens_before INTEGER,last_tokens_after INTEGER,
      last_action TEXT,capsule_path TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,completed_at TEXT);`);
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',4,?,?)")
    .run(sessionKey,stamp,stamp);
  db.prepare(`INSERT INTO cnx_context_maintenance(session_key,owner_generation,ticket_id,state,hard_required,attempt_count,next_attempt_at,
    session_id,context_window,projected_tokens,created_at,updated_at) VALUES (?,?,?,'pending',1,0,?, 'physical-old',32768,30000,?,?)`)
    .run(sessionKey,4,ticket.ticketId,stamp,stamp,stamp);
  db.close();
  return {path,store,sessionKey,ticketId:ticket.ticketId};
}

describe("v0.9 manual Compact boundary",()=>{
  it("suppresses the legacy after_compaction synthetic continuation registration but preserves other hooks",()=>{
    const names:string[]=[];
    const api={on:(name:string)=>{names.push(name);},logger:{info:()=>{}}};
    const proxy=createCompactionBoundaryApi(api);
    proxy.on("after_compaction",()=>{});
    proxy.on("agent_end",()=>{});
    expect(names).toEqual(["agent_end"]);
  });

  it("does not create SQLite state when a user compacts a session with no existing CNX context store",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-empty-"));
    try{
      const path=join(root,"missing.sqlite3");
      const result=settleExistingContextHoldFromCompaction({databasePath:path,sessionKey:"agent:main:dashboard:A",tokenCount:5000,
        session:{contextTokens:32768,totalTokens:5000,totalTokensFresh:true,sessionId:"physical-new"}});
      expect(result).toMatchObject({found:false,settled:false,reason:"no-existing-context-store"});
      expect(existsSync(path)).toBe(false);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("releases only an already-authorized context hold when manual Compact makes the same generation safe",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-safe-"));
    try{
      const {path,sessionKey,ticketId}=fixture(root);
      const result=settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:7000,
        session:{contextTokens:32768,totalTokens:30000,totalTokensFresh:true,sessionId:"physical-before-store-persist"},now:new Date("2026-08-16T13:00:00Z")});
      expect(result).toMatchObject({found:true,settled:true,reason:"safe-context",observedTokens:7000});
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action,session_id,last_tokens_after FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"done",last_action:"native-compact-satisfied",session_id:"physical-before-store-persist",last_tokens_after:7000});
      expect(db.prepare("SELECT status,workflow_eligible FROM tickets WHERE ticket_id=?").get(ticketId)).toEqual({status:"accepted",workflow_eligible:0});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_outbox").get()).toEqual({count:0});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never changes Direct Recovery state when a manual Compact only satisfies context maintenance",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-recovery-"));
    try{
      const {path,sessionKey,ticketId}=fixture(root),stamp=new Date().toISOString();
      let db=new DatabaseSync(path);
      db.exec(`CREATE TABLE cnx_direct_recovery(
        ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,mode TEXT NOT NULL,state TEXT NOT NULL,
        attempt_count INTEGER NOT NULL,active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,owner_generation INTEGER NOT NULL,
        created_at TEXT NOT NULL,updated_at TEXT NOT NULL);`);
      db.prepare(`INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at)
        VALUES (?,'resume','pending',2,NULL,?,'waiting for context',4,?,?)`).run(ticketId,stamp,stamp,stamp);db.close();
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:6000,
        session:{contextTokens:32768,totalTokens:30000,totalTokensFresh:true,sessionId:"physical-after-user-compact"}})).toMatchObject({settled:true});
      db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation FROM cnx_direct_recovery WHERE ticket_id=?").get(ticketId))
        .toEqual({state:"pending",attempt_count:2,active_run_id:null,next_attempt_at:stamp,last_error:"waiting for context",owner_generation:4});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("admits a fresh human Ticket normally after manual Compact without changing session generation",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-next-turn-"));
    try{
      const {path,store,sessionKey}=fixture(root);
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:6500,
        session:{contextTokens:32768,totalTokens:29000,totalTokensFresh:true,sessionId:"physical-before-persist"}})).toMatchObject({settled:true,observedTokens:6500});
      const next=store.accept({runId:"run-2",ownerSessionKey:sessionKey,prompt:"new human message after compact"});store.route(next.ticketId,false);
      let hook:any;
      installContextGuard({runtime:{gateway:{request:async(method:string)=>method==="sessions.describe"
        ? {session:{contextTokens:32768,totalTokens:7000,totalTokensFresh:true,sessionId:"physical-after-persist"}}:{}}},logger:{info:()=>{},warn:()=>{}}},
        {on:(name:string,handler:any)=>{if(name==="before_agent_run")hook=handler;},registerService:()=>{}},{workspaceDir:root,ticketDatabasePath:path});
      expect(await hook({prompt:"new human message after compact",messages:[],systemPrompt:""},{sessionKey,runId:"run-2",workspaceDir:root})).toEqual({outcome:"pass"});
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT generation,state FROM cnx_sessions WHERE session_key=?").get(sessionKey)).toEqual({generation:4,state:"active"});
      expect(db.prepare("SELECT status,workflow_eligible FROM tickets WHERE ticket_id=?").get(next.ticketId)).toEqual({status:"accepted",workflow_eligible:0});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE ticket_id=?").get(next.ticketId)).toEqual({count:0});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("uses a fresh session counter only when the after_compaction event did not provide tokenCount",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-session-fallback-"));
    try{
      const {path,sessionKey}=fixture(root);
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,
        session:{contextTokens:32768,totalTokens:6500,totalTokensFresh:true,sessionId:"physical-after-persist"}}))
        .toMatchObject({found:true,settled:true,reason:"safe-context",observedTokens:6500});
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("keeps the hold when manual Compact leaves context above the safe admission boundary",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-high-"));
    try{
      const {path,sessionKey}=fixture(root);
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:29500,
        session:{contextTokens:32768,totalTokens:30000,totalTokensFresh:true,sessionId:"physical-after-compact"}}))
        .toMatchObject({found:true,settled:false,reason:"pressure-remains",observedTokens:29500});
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"pending",last_action:"native-compact-observed-pressure-remains"});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never settles a context row already claimed by the maintenance worker",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-running-"));
    try{
      const {path,sessionKey}=fixture(root);let db=new DatabaseSync(path);
      db.prepare("UPDATE cnx_context_maintenance SET state='running',attempt_count=1 WHERE session_key=?").run(sessionKey);db.close();
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:4000,
        session:{contextTokens:32768,totalTokens:4000,totalTokensFresh:true,sessionId:"physical-after-user-compact"}}))
        .toMatchObject({found:true,settled:false,reason:"maintenance-running"});
      db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,last_action,session_id FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey))
        .toEqual({state:"running",last_action:null,session_id:"physical-old"});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never releases an old hold after Reset advanced the CNX generation",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-manual-compact-reset-"));
    try{
      const {path,sessionKey}=fixture(root);const db=new DatabaseSync(path);db.prepare("UPDATE cnx_sessions SET generation=5 WHERE session_key=?").run(sessionKey);db.close();
      expect(settleExistingContextHoldFromCompaction({databasePath:path,sessionKey,tokenCount:4000,
        session:{contextTokens:32768,totalTokens:4000,totalTokensFresh:true,sessionId:"replacement-session"}}))
        .toMatchObject({found:true,settled:false,reason:"authority-superseded"});
      const verify=new DatabaseSync(path,{readOnly:true});
      expect(verify.prepare("SELECT state,last_action FROM cnx_context_maintenance WHERE session_key=?").get(sessionKey)).toEqual({state:"pending",last_action:null});verify.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
