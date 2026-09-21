import { existsSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

export type IngressRestartRecoveryResult = {
  queued:number;
  existing:number;
  skippedSuperseded:number;
};

function tableExists(db:DatabaseSync,name:string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

export function recoverStrandedIngressAfterRestart(path:string,now=new Date()):IngressRestartRecoveryResult {
  if(!existsSync(path))return{queued:0,existing:0,skippedSuperseded:0};
  new TicketStore(path).snapshot();
  const db=new DatabaseSync(path);
  const stamp=now.toISOString();
  let queued=0,existing=0,skippedSuperseded=0;
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000");
    if(!tableExists(db,"ticket_ingress_claims")||!tableExists(db,"tickets")||
       !tableExists(db,"cnx_sessions")||!tableExists(db,"cnx_direct_recovery")) {
      return{queued,existing,skippedSuperseded};
    }
    db.exec("BEGIN IMMEDIATE");
    const rows=db.prepare(`
      SELECT c.rowid AS ingress_order,c.ticket_id,c.owner_session_key,c.owner_generation,
             c.source_message_id,c.bound_run_id,c.created_at,
             t.status,t.workflow_eligible,t.workflow_id,t.response_ready_at,
             s.state AS session_state,s.generation AS session_generation
      FROM ticket_ingress_claims c
      JOIN tickets t ON t.ticket_id=c.ticket_id
      JOIN cnx_sessions s ON s.session_key=c.owner_session_key
      WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND t.response_ready_at IS NULL AND c.bound_run_id IS NULL
      ORDER BY c.owner_session_key,c.owner_generation,c.rowid
    `).all() as any[];

    for(const row of rows) {
      if(row.session_state!=="active"||Number(row.session_generation)!==Number(row.owner_generation)) {
        skippedSuperseded++;
        continue;
      }
      const prior=db.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(row.ticket_id) as any;
      if(prior) {
        existing++;
        continue;
      }
      const reason="Gateway restarted before the accepted ingress reached terminal delivery";
      db.prepare(`
        INSERT INTO cnx_direct_recovery(
          ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
          owner_generation,created_at,updated_at
        ) VALUES (?,'resume','pending',0,NULL,?,?,?, ?,?)
      `).run(
        row.ticket_id,
        stamp,
        reason,
        Number(row.owner_generation),
        String(row.created_at??stamp),
        stamp,
      );
      db.prepare(`
        UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=?
        WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NULL
      `).run(reason,reason,stamp,row.ticket_id);
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
        .run(row.ticket_id,"ingress_restart_recovery_pending",JSON.stringify({
          ownerSessionKey:row.owner_session_key,
          ownerGeneration:Number(row.owner_generation),
          sourceMessageId:row.source_message_id,
          boundRunId:row.bound_run_id??null,
          ingressOrder:Number(row.ingress_order),
          reason,
        }),stamp);
      queued++;
    }
    db.exec("COMMIT");
    return{queued,existing,skippedSuperseded};
  } catch(error) {
    try{db.exec("ROLLBACK");}catch{}
    throw error;
  } finally {
    db.close();
  }
}
