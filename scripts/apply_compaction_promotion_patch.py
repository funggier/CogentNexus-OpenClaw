#!/usr/bin/env python3
from pathlib import Path

# Patch TicketStore with a deterministic promotion used only when the delayed
# post-compaction guard actually fires.
ticket = Path("plugins/cogentnexus-rotation/src/ticket-store.ts")
text = ticket.read_text(encoding="utf-8")
anchor = '''  hasNonTerminalForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM tickets WHERE owner_session_key=? AND status NOT IN ('completed','failed','cancelled') LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }
'''
insert = '''  hasPendingDirectExecutionForSession(sessionKey:string): boolean {
    const db=this.open();
    try { return Boolean(db.prepare("SELECT 1 FROM tickets WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NULL LIMIT 1").get(sessionKey)); }
    finally { db.close(); }
  }

  promotePendingDirectForSession(input:{sessionKey:string;reason?:string;now?:Date}): {ticketId:string;runId:string}|undefined {
    const db=this.open(),nowIso=(input.now??new Date()).toISOString();
    const reason=(input.reason??"post-compaction continuation guard fired before the original direct turn reached terminal state").slice(0,2000);
    try {
      db.exec("BEGIN IMMEDIATE");
      const row=db.prepare("SELECT ticket_id,run_id FROM tickets WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NULL ORDER BY created_at DESC LIMIT 1").get(input.sessionKey) as any;
      if(!row){db.exec("COMMIT");return undefined;}
      const changed=db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NULL")
        .run(reason,nowIso,row.ticket_id);
      if(changed.changes!==1){db.exec("COMMIT");return undefined;}
      this.event(db,row.ticket_id,"post_compaction_promoted",{runId:row.run_id,reason},nowIso);
      db.exec("COMMIT");
      return {ticketId:row.ticket_id,runId:row.run_id};
    } catch(error){try{db.exec("ROLLBACK");}catch{}throw error;} finally{db.close();}
  }

'''+anchor
if anchor not in text: raise SystemExit("TicketStore pending-session anchor missing")
text=text.replace(anchor,insert,1)
ticket.write_text(text,encoding="utf-8")

# Make the delayed guard only target unfinished DIRECT execution. Running durable
# workflows and terminal outboxes already have deterministic services of their own.
delivery = Path("plugins/cogentnexus-rotation/src/delivery-continuity.ts")
text=delivery.read_text(encoding="utf-8")
old='''export function hasPendingSessionWork(workspaceDir: string, store: TicketStore, sessionKey: string): boolean {
  return store.hasNonTerminalForSession(sessionKey) || store.hasPendingOutboxForSession(sessionKey) || hasPendingWorkflowDeliveryForSession(workspaceDir, sessionKey);
}
'''
new='''export function hasPendingSessionWork(workspaceDir: string, store: TicketStore, sessionKey: string): boolean {
  return store.hasNonTerminalForSession(sessionKey) || store.hasPendingOutboxForSession(sessionKey) || hasPendingWorkflowDeliveryForSession(workspaceDir, sessionKey);
}

export function hasPendingDirectExecutionForSession(store: TicketStore, sessionKey: string): boolean {
  return store.hasPendingDirectExecutionForSession(sessionKey);
}
'''
if old not in text: raise SystemExit("delivery pending-session anchor missing")
text=text.replace(old,new,1)
delivery.write_text(text,encoding="utf-8")

index=Path("plugins/cogentnexus-rotation/src/index.ts")
text=index.read_text(encoding="utf-8")
text=text.replace(
  'bindDeliveryRun, hasPendingSessionWork, hasVisibleAssistantOutput,',
  'bindDeliveryRun, hasPendingDirectExecutionForSession, hasPendingSessionWork, hasVisibleAssistantOutput,',
  1,
)
old_guard='''  if (!hasPendingSessionWork(input.workspaceDir,input.store,input.sessionKey)) return false;
'''
new_guard='''  if (!hasPendingDirectExecutionForSession(input.store,input.sessionKey)) return false;
'''
if old_guard not in text: raise SystemExit("schedulePostCompactionResume pending-work anchor missing")
text=text.replace(old_guard,new_guard,1)
old_before='''    const deliveryTarget=parseDeliveryMarker(event.prompt);
    if(deliveryTarget){
      if(currentRunId){
        const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(currentWorkspace));
        if(bindDeliveryRun({workspaceDir:currentWorkspace,store,target:deliveryTarget,runId:currentRunId})) deliveryTargets.set(currentRunId,deliveryTarget);
      }
      return {outcome:"pass"};
    }
'''
new_before='''    const deliveryTarget=parseDeliveryMarker(event.prompt);
    if(deliveryTarget){
      if(currentRunId){
        const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(currentWorkspace));
        if(bindDeliveryRun({workspaceDir:currentWorkspace,store,target:deliveryTarget,runId:currentRunId})) deliveryTargets.set(currentRunId,deliveryTarget);
      }
      return {outcome:"pass"};
    }
    if(event.prompt.includes("[CogentNexus Continuation: post-compaction]") && ctx.sessionKey){
      const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(currentWorkspace));
      const promoted=store.promotePendingDirectForSession({sessionKey:ctx.sessionKey});
      if(promoted) return {
        outcome:"block",
        reason:"post-compaction guard promoted the unfinished direct Ticket to durable recovery",
        category:"cogentnexus_post_compaction_recovery",
        metadata:{ticketId:promoted.ticketId,runId:promoted.runId},
        message:`CogentNexus resumed committed Ticket ${promoted.ticketId} after history compaction. Durable recovery is continuing automatically; the original request does not need to be sent again.`,
      };
      return {outcome:"pass"};
    }
'''
if old_before not in text: raise SystemExit("before_agent_run delivery anchor missing")
text=text.replace(old_before,new_before,1)
index.write_text(text,encoding="utf-8")
print("post-compaction deterministic promotion patch applied")
