import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { nextDirectRecoveryWakeMs } from "./v091-direct-recovery.js";

function seed(path:string) {
  const db=new DatabaseSync(path);
  db.exec(`
    CREATE TABLE tickets(
      ticket_id TEXT PRIMARY KEY,
      owner_session_key TEXT NOT NULL,
      status TEXT NOT NULL,
      workflow_eligible INTEGER NOT NULL,
      workflow_id TEXT
    );
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      next_attempt_at TEXT,
      updated_at TEXT NOT NULL,
      owner_generation INTEGER NOT NULL
    );
  `);
  db.prepare("INSERT INTO tickets VALUES (?,?,?,?,?)").run("CNXT-1","agent:main:test","accepted",0,null);
  db.prepare("INSERT INTO cnx_sessions VALUES (?,?,?)").run("agent:main:test","active",7);
  db.prepare("INSERT INTO cnx_direct_recovery VALUES (?,?,?,?,?)").run("CNXT-1","pending",null,new Date().toISOString(),7);
  return db;
}

describe("v0.9.1 Direct Recovery wake authority",()=>{
  it("arms an immediate wake only while the Ticket and exact session generation remain authoritative",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-v091-direct-wake-"));
    try {
      const path=join(root,"tickets.sqlite3");
      const db=seed(path);
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBe(25);

      db.prepare("UPDATE cnx_sessions SET generation=8").run();
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBeUndefined();

      db.prepare("UPDATE cnx_sessions SET generation=7").run();
      db.prepare("UPDATE tickets SET status='cancelled'").run();
      expect(nextDirectRecoveryWakeMs(path,{},new Date())).toBeUndefined();
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
});
