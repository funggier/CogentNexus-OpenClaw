import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { directRecoveryIdentity, installRecoveryOrderAdmission, predecessorRecovery, queueBehindOlderRecovery } from "./v090-recovery-order.js";

function setup(root:string) {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
  store.snapshot();
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS cnx_sessions(
      session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
      deleted_at TEXT,delete_reason TEXT);
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      mode TEXT NOT NULL DEFAULT 'resume',state TEXT NOT NULL DEFAULT 'pending',attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,owner_generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,updated_at TEXT NOT NULL);`);
  db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',3,?,?)").run("agent:main:dashboard:A",stamp,stamp);
  db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',3,?,?)").run("agent:main:dashboard:B",stamp,stamp);
  db.close();
  return {path,store};
}

function addRecovery(path:string,ticketId:string,state="running",generation=3) {
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.prepare(`INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at)
    VALUES (?,'resume',?,1,?,NULL,NULL,?,?,?)`).run(ticketId,state,state==="running"?`run-${ticketId}`:null,generation,stamp,stamp);
  db.close();
}

describe("v0.9 same-session Direct Recovery ordering",()=>{
  it("uses monotonic accepted event_id instead of timestamp or UUID ordering",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-recovery-order-"));
    try{
      const {path,store}=setup(root),session="agent:main:dashboard:A";
      const first=store.accept({runId:"first",ownerSessionKey:session,prompt:"first intent"});store.route(first.ticketId,false);
      const second=store.accept({runId:"second",ownerSessionKey:session,prompt:"second intent"});store.route(second.ticketId,false);
      addRecovery(path,first.ticketId,"running");
      const predecessor=predecessorRecovery(path,{ticketId:second.ticketId,ownerSessionKey:session,ownerGeneration:3}) as any;
      expect(predecessor?.ticket_id).toBe(first.ticketId);
      const db=new DatabaseSync(path,{readOnly:true});
      const firstSeq=Number((db.prepare("SELECT event_id FROM ticket_events WHERE ticket_id=? AND event_type='accepted'").get(first.ticketId) as any).event_id);
      const secondSeq=Number((db.prepare("SELECT event_id FROM ticket_events WHERE ticket_id=? AND event_type='accepted'").get(second.ticketId) as any).event_id);db.close();
      expect(firstSeq).toBeLessThan(secondSeq);
      expect(Number(predecessor.accepted_sequence)).toBe(firstSeq);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("commits a newer same-session Ticket to pending recovery behind its predecessor",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-recovery-queue-"));
    try{
      const {path,store}=setup(root),session="agent:main:dashboard:A";
      const first=store.accept({runId:"first",ownerSessionKey:session,prompt:"first"});store.route(first.ticketId,false);addRecovery(path,first.ticketId,"awaiting_delivery");
      const second=store.accept({runId:"second",ownerSessionKey:session,prompt:"second"});store.route(second.ticketId,false);
      const queued=queueBehindOlderRecovery(path,{sessionKey:session,runId:"second"});
      expect(queued).toMatchObject({ticketId:second.ticketId,predecessorTicketId:first.ticketId,predecessorState:"awaiting_delivery"});
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT state,owner_generation FROM cnx_direct_recovery WHERE ticket_id=?").get(second.ticketId)).toEqual({state:"pending",owner_generation:3});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=? AND event_type='direct_recovery_serialized'").get(second.ticketId)).toEqual({count:1});db.close();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("does not serialize an independent session behind another session's recovery",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-recovery-isolation-"));
    try{
      const {path,store}=setup(root);
      const a=store.accept({runId:"a",ownerSessionKey:"agent:main:dashboard:A",prompt:"A"});store.route(a.ticketId,false);addRecovery(path,a.ticketId,"running");
      const b=store.accept({runId:"b",ownerSessionKey:"agent:main:dashboard:B",prompt:"B"});store.route(b.ticketId,false);
      expect(queueBehindOlderRecovery(path,{sessionKey:"agent:main:dashboard:B",runId:"b"})).toBeUndefined();
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("revokes an ordered recovery when the session generation advances",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-recovery-generation-"));
    try{
      const {path,store}=setup(root),session="agent:main:dashboard:A";
      const ticket=store.accept({runId:"x",ownerSessionKey:session,prompt:"X"});store.route(ticket.ticketId,false);addRecovery(path,ticket.ticketId,"running");
      expect(directRecoveryIdentity(path,ticket.ticketId,3)).toMatchObject({authorized:true,ownerGeneration:3});
      const db=new DatabaseSync(path);db.prepare("UPDATE cnx_sessions SET generation=4 WHERE session_key=?").run(session);db.close();
      expect(directRecoveryIdentity(path,ticket.ticketId,3)).toMatchObject({authorized:false,reason:"session-authority-superseded"});
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("registers after Ticket-first admission and blocks a newer owner run",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-recovery-hook-"));
    try{
      const {path,store}=setup(root),session="agent:main:dashboard:A";
      const first=store.accept({runId:"first",ownerSessionKey:session,prompt:"first"});store.route(first.ticketId,false);addRecovery(path,first.ticketId,"running");
      const second=store.accept({runId:"second",ownerSessionKey:session,prompt:"second"});store.route(second.ticketId,false);
      let handler:any,options:any;
      const api={on:(name:string,fn:any,opts:any)=>{if(name==="before_agent_run"){handler=fn;options=opts;}},logger:{info:()=>{}}};
      installRecoveryOrderAdmission(api,{workspaceDir:root,ticketDatabasePath:path});
      expect(options.priority).toBe(1600);
      const result=await handler({}, {sessionKey:session,runId:"second",workspaceDir:root});
      expect(result).toMatchObject({outcome:"block",category:"cogentnexus_recovery_order",metadata:{ticketId:second.ticketId,predecessorTicketId:first.ticketId}});
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
