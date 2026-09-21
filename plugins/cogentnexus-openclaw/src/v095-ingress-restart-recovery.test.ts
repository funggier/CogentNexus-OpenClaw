import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { dueDirectRecovery, nextDirectRecoveryWakeMs } from "./v091-direct-recovery.js";
import { recoverStrandedIngressAfterRestart } from "./v095-ingress-restart-recovery.js";

function setup(path:string,generation=5,now=new Date("2026-09-21T05:50:00.000Z")) {
  const store=new TicketStore(path);
  store.snapshot();
  const db=new DatabaseSync(path);
  db.exec(`
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      deleted_at TEXT,
      delete_reason TEXT,
      session_id TEXT
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT NOT NULL,
      state TEXT NOT NULL,
      attempt_count INTEGER NOT NULL,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      owner_generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
  `);
  const sessionKey="agent:main:discord:channel:restart-fifo";
  db.prepare("INSERT INTO cnx_sessions VALUES (?,'active',?,?,?,?,?,?)")
    .run(sessionKey,generation,now.toISOString(),now.toISOString(),null,null,"physical-restart-fifo");
  db.close();
  return{store,sessionKey};
}

describe("CNX-442 pre-dispatch restart recovery",()=>{
  it("recovers only held unbound ingress and keeps it FIFO-blocked behind the bound predecessor",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx442-ingress-restart-"));
    try {
      const path=join(root,"tickets.sqlite3");
      const now=new Date("2026-09-21T05:50:00.000Z");
      const {store,sessionKey}=setup(path,5,now);

      const first=store.acceptIngress({
        sourceKey:"discord:first",
        sourceChannel:"discord",
        sourceMessageId:"msg-first",
        ownerSessionKey:sessionKey,
        prompt:"@Ce first",
      });
      expect(store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,
        ownerSessionId:"physical-restart-fifo",
        runId:"run-first",
        prompt:"@Ce first",
        sourceChannel:"discord",
      })).toMatchObject({state:"bound",ticketId:first.ticketId});
      store.route(first.ticketId,false);

      const second=store.acceptIngress({
        sourceKey:"discord:second",
        sourceChannel:"discord",
        sourceMessageId:"msg-second",
        ownerSessionKey:sessionKey,
        prompt:"@Ce second",
      });

      const recovered=recoverStrandedIngressAfterRestart(path,now);
      expect(recovered).toEqual({queued:1,existing:0,skippedSuperseded:0});

      let db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT ticket_id,state,owner_generation FROM cnx_direct_recovery ORDER BY created_at,ticket_id").all())
        .toEqual([{ticket_id:second.ticketId,state:"pending",owner_generation:5}]);
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE event_type='ingress_restart_recovery_pending'").get())
        .toEqual({n:1});
      db.close();

      expect(recoverStrandedIngressAfterRestart(path,now)).toEqual({queued:0,existing:1,skippedSuperseded:0});

      expect(dueDirectRecovery(path,now)).toBeUndefined();
      expect(nextDirectRecoveryWakeMs(path,{},now)).toBeUndefined();

      db=new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='completed',delivery_confirmed_at=?,updated_at=? WHERE ticket_id=?")
        .run(now.toISOString(),now.toISOString(),first.ticketId);
      db.close();

      expect(dueDirectRecovery(path,now)).toMatchObject({ticket_id:second.ticketId});
    } finally {
      rmSync(root,{recursive:true,force:true});
    }
  });

  it("does not revive ingress from a superseded owner generation",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx442-ingress-restart-generation-"));
    try {
      const path=join(root,"tickets.sqlite3");
      const now=new Date("2026-09-21T05:50:00.000Z");
      const {store,sessionKey}=setup(path,8,now);
      const ticket=store.acceptIngress({
        sourceKey:"discord:superseded",
        sourceChannel:"discord",
        sourceMessageId:"msg-superseded",
        ownerSessionKey:sessionKey,
        prompt:"@Ce old generation",
      });
      const db=new DatabaseSync(path);
      db.prepare("UPDATE cnx_sessions SET generation=9,updated_at=? WHERE session_key=?")
        .run(now.toISOString(),sessionKey);
      db.close();

      expect(recoverStrandedIngressAfterRestart(path,now))
        .toEqual({queued:0,existing:0,skippedSuperseded:1});

      const check=new DatabaseSync(path,{readOnly:true});
      expect(check.prepare("SELECT COUNT(*) AS n FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({n:0});
      check.close();
    } finally {
      rmSync(root,{recursive:true,force:true});
    }
  });
});
