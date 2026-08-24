import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { nextDirectRecoveryWakeMs, resetStaleDirectRecovery } from "./v091-direct-recovery.js";

function seed(path:string) {
  const store=new TicketStore(path);
  const ticket=store.accept({runId:"run-1",ownerSessionKey:"agent:main:test",prompt:"test"});
  const db=new DatabaseSync(path);
  db.exec(`
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      next_attempt_at TEXT,
      active_run_id TEXT,
      last_error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      owner_generation INTEGER NOT NULL
    );
  `);
  db.prepare("INSERT INTO cnx_sessions VALUES (?,?,?)").run("agent:main:test","active",7);
  const stamp=new Date().toISOString();
  db.prepare("INSERT INTO cnx_direct_recovery VALUES (?,?,?,?,?,?,?,?)")
    .run(ticket.ticketId,"pending",null,null,null,stamp,stamp,7);
  return {db,ticketId:ticket.ticketId};
}

describe("v0.9.1 Direct Recovery wake authority",()=>{
  it("arms an immediate wake only while the Ticket and exact session generation remain authoritative",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-v091-direct-wake-"));
    try {
      const path=join(root,"tickets.sqlite3");
      const {db}=seed(path);
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBe(25);

      db.prepare("UPDATE cnx_sessions SET generation=8").run();
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBeUndefined();

      db.prepare("UPDATE cnx_sessions SET generation=7").run();
      db.prepare("UPDATE tickets SET status='cancelled'").run();
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBeUndefined();
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("opens the writable recovery database without passing undefined constructor options",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-v091-direct-write-"));
    try {
      const path=join(root,"tickets.sqlite3");
      const {db,ticketId}=seed(path);
      const now=new Date("2026-08-18T08:00:00.000Z");
      const stale=new Date(now.getTime()-2*60*60_000).toISOString();
      db.prepare("UPDATE cnx_direct_recovery SET state='running',active_run_id='run-stale',updated_at=? WHERE ticket_id=?")
        .run(stale,ticketId);
      db.close();

      expect(resetStaleDirectRecovery(path,{},now)).toBe(1);

      const check=new DatabaseSync(path,{readOnly:true});
      const row=check.prepare("SELECT state,active_run_id,last_error FROM cnx_direct_recovery WHERE ticket_id=?")
        .get(ticketId) as {state:string;active_run_id:string|null;last_error:string|null};
      expect(row.state).toBe("pending");
      expect(row.active_run_id).toBeNull();
      expect(row.last_error).toBe("stale Direct recovery reset");
      check.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
});
