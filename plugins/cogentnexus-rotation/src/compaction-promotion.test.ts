import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { schedulePostCompactionResume } from "./index.js";
import { TicketStore } from "./ticket-store.js";

describe("post-compaction deterministic recovery", () => {
  it("promotes the original unfinished DIRECT Ticket when the delayed guard actually fires", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-post-compact-promote-"));
    try {
      const path=join(root,"tickets.sqlite3"),store=new TicketStore(path),sessionKey="agent:main:owner";
      const ticket=store.accept({runId:"original-run",ownerSessionKey:sessionKey,prompt:"finish this long direct task"});
      store.route(ticket.ticketId,false);
      expect(store.hasPendingDirectExecutionForSession(sessionKey)).toBe(true);
      expect(store.promotePendingDirectForSession({sessionKey,reason:"compaction guard fired",now:new Date("2026-08-15T00:00:10.000Z")}))
        .toEqual({ticketId:ticket.ticketId,runId:"original-run"});
      expect(store.hasPendingDirectExecutionForSession(sessionKey)).toBe(false);
      expect(store.ready().map(x=>x.ticketId)).toEqual([ticket.ticketId]);
      const db=new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT status,workflow_eligible,failure_class,failure_message FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({status:"waiting",workflow_eligible:1,failure_class:"interrupted",failure_message:"compaction guard fired"});
      expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type))
        .toEqual(["accepted","routed","post_compaction_promoted"]);
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("does not promote a response-ready Ticket that is waiting only for delivery receipt", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-post-compact-response-ready-"));
    try {
      const store=new TicketStore(join(root,"tickets.sqlite3")),sessionKey="agent:main:owner";
      const ticket=store.accept({runId:"response-ready",ownerSessionKey:sessionKey,prompt:"long answer"});
      store.route(ticket.ticketId,false);
      expect(store.finalizeDirectRun({runId:"response-ready",success:true,interrupted:false,expectsDelivery:true})).toBe("awaiting_delivery");
      expect(store.hasPendingDirectExecutionForSession(sessionKey)).toBe(false);
      expect(store.promotePendingDirectForSession({sessionKey})).toBeUndefined();
      expect(store.ready()).toEqual([]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("schedules the guard only for unfinished DIRECT execution, not for response-ready delivery", async () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-post-compact-scope-"));
    try {
      const store=new TicketStore(join(root,"tickets.sqlite3")),sessionKey="agent:main:owner";
      const scheduled:any[]=[];
      const workflow={
        async unscheduleSessionTurnsByTag(){},
        async scheduleSessionTurn(input:any){scheduled.push(input);},
      };
      const first=store.accept({runId:"unfinished",ownerSessionKey:sessionKey,prompt:"unfinished task"});store.route(first.ticketId,false);
      await expect(schedulePostCompactionResume({sessionKey,workspaceDir:root,store,workflow,delayMs:1000})).resolves.toBe(true);
      expect(scheduled).toHaveLength(1);
      store.promotePendingDirectForSession({sessionKey});
      await expect(schedulePostCompactionResume({sessionKey,workspaceDir:root,store,workflow,delayMs:1000})).resolves.toBe(false);

      const second=store.accept({runId:"ready",ownerSessionKey:sessionKey,prompt:"ready response"});store.route(second.ticketId,false);
      store.finalizeDirectRun({runId:"ready",success:true,interrupted:false,expectsDelivery:true});
      await expect(schedulePostCompactionResume({sessionKey,workspaceDir:root,store,workflow,delayMs:1000})).resolves.toBe(false);
      expect(scheduled).toHaveLength(1);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
});
