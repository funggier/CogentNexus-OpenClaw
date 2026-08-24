import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";

function setup(root:string) {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);store.snapshot();
  const db=new DatabaseSync(path),stamp=new Date().toISOString(),session="agent:main:dashboard:A";
  db.exec(`PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS cnx_sessions(
      session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
      deleted_at TEXT,delete_reason TEXT);
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      mode TEXT NOT NULL DEFAULT 'resume',state TEXT NOT NULL DEFAULT 'pending',attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,owner_generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,updated_at TEXT NOT NULL);`);
  db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',7,?,?)").run(session,stamp,stamp);db.close();
  const first=store.accept({runId:"first",ownerSessionKey:session,prompt:"first"});store.route(first.ticketId,false);
  const second=store.accept({runId:"second",ownerSessionKey:session,prompt:"second"});store.route(second.ticketId,false);
  const db2=new DatabaseSync(path),now=new Date().toISOString();
  for(const ticket of [first,second])db2.prepare(`INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at)
    VALUES (?,'resume','running',1,?,NULL,NULL,7,?,?)`).run(ticket.ticketId,`run-${ticket.ticketId}`,now,now);
  db2.close();
  return {path,store,session,first:first.ticketId,second:second.ticketId};
}

function hidden(ticketId:string){return `agent:main:subagent:cnx-recovery-${ticketId}-0123456789ab-g7-deadbeef`;}
function claim(ticketId:string){return `run-${ticketId}`;}
const internal="[CogentNexus-OpenClaw Internal Direct Recovery]\nresume committed work";
const sleep=(ms:number)=>new Promise(resolve=>setTimeout(resolve,ms));

describe("v0.9 hidden Direct Recovery ordered lane",()=>{
  it("does not invoke the model until the older same-session recovery is terminal",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-hidden-order-"));
    try{
      const fx=setup(root);let launches=0;
      const api={runtime:{subagent:{run:async(input:any)=>{launches++;return {runId:`launched-${input.sessionKey}`};}}},logger:{info:()=>{}}};
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,ticketDatabasePath:fx.path,recoveryOrderPollMs:100});
      const pending=proxy.runtime.subagent.run({sessionKey:hidden(fx.second),message:internal,idempotencyKey:claim(fx.second),deliver:false});
      await sleep(60);expect(launches).toBe(0);
      const db=new DatabaseSync(fx.path);db.prepare("UPDATE tickets SET status='completed' WHERE ticket_id=?").run(fx.first);db.prepare("UPDATE cnx_direct_recovery SET state='cancelled' WHERE ticket_id=?").run(fx.first);db.close();
      await pending;expect(launches).toBe(1);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("revokes a waiting hidden worker on generation change without any model call",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-hidden-revoke-"));
    try{
      const fx=setup(root);let launches=0;
      const api={runtime:{subagent:{run:async()=>{launches++;return {runId:"should-not-run"};}}},logger:{info:()=>{}}};
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,ticketDatabasePath:fx.path,recoveryOrderPollMs:100});
      const pending=proxy.runtime.subagent.run({sessionKey:hidden(fx.second),message:internal,idempotencyKey:claim(fx.second),deliver:false});
      await sleep(60);expect(launches).toBe(0);
      const db=new DatabaseSync(fx.path);db.prepare("UPDATE cnx_sessions SET generation=8 WHERE session_key=?").run(fx.session);db.close();
      await expect(pending).rejects.toThrow(/claim revoked/i);expect(launches).toBe(0);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("rejects a stale waiter whose active_run_id was superseded before predecessor release",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-hidden-claim-"));
    try{
      const fx=setup(root);let launches=0;
      const api={runtime:{subagent:{run:async()=>{launches++;return {runId:"should-not-run"};}}},logger:{info:()=>{}}};
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,ticketDatabasePath:fx.path,recoveryOrderPollMs:100});
      const pending=proxy.runtime.subagent.run({sessionKey:hidden(fx.second),message:internal,idempotencyKey:claim(fx.second),deliver:false});
      await sleep(60);expect(launches).toBe(0);
      const db=new DatabaseSync(fx.path);db.prepare("UPDATE cnx_direct_recovery SET active_run_id='replacement-claim',updated_at=? WHERE ticket_id=?").run(new Date().toISOString(),fx.second);db.close();
      await expect(pending).rejects.toThrow(/claim revoked.*superseded/i);expect(launches).toBe(0);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
