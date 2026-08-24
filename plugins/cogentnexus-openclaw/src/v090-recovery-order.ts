import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

export type RecoveryOrderConfig={workspaceDir?:string;ticketDatabasePath?:string};

function stamp(){return new Date().toISOString();}

function openDb(path:string){
  new TicketStore(path).snapshot();
  const db=new DatabaseSync(path);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000");
  return db;
}

function acceptedSequence(db:DatabaseSync,ticketId:string):number|undefined {
  const row=db.prepare("SELECT MIN(event_id) AS event_id FROM ticket_events WHERE ticket_id=? AND event_type='accepted'").get(ticketId) as any;
  const value=Number(row?.event_id);
  return Number.isSafeInteger(value)&&value>0?value:undefined;
}

export function predecessorRecovery(path:string,input:{ticketId:string;ownerSessionKey:string;ownerGeneration:number}) {
  const db=openDb(path);
  try {
    const sequence=acceptedSequence(db,input.ticketId);
    if(sequence===undefined)return undefined;
    return db.prepare(`SELECT older.ticket_id,MIN(accepted.event_id) AS accepted_sequence,recovery.state,recovery.next_attempt_at
      FROM tickets older
      JOIN ticket_events accepted ON accepted.ticket_id=older.ticket_id AND accepted.event_type='accepted'
      JOIN cnx_direct_recovery recovery ON recovery.ticket_id=older.ticket_id
      WHERE older.owner_session_key=? AND older.ticket_id<>? AND older.status='accepted'
        AND older.workflow_eligible=0 AND older.workflow_id IS NULL
        AND recovery.owner_generation=? AND recovery.state IN ('pending','running','awaiting_delivery')
      GROUP BY older.ticket_id,recovery.state,recovery.next_attempt_at
      HAVING MIN(accepted.event_id)<?
      ORDER BY accepted_sequence LIMIT 1`)
      .get(input.ownerSessionKey,input.ticketId,input.ownerGeneration,sequence) as any;
  } finally {db.close();}
}

export function directRecoveryIdentity(path:string,ticketId:string,ownerGeneration:number,expectedRunId?:string) {
  const db=openDb(path);
  try {
    const row=db.prepare(`SELECT t.ticket_id,t.owner_session_key,t.status,t.created_at,t.workflow_eligible,t.workflow_id,
      s.state AS session_state,s.generation,r.state AS recovery_state,r.active_run_id,
      (SELECT MIN(e.event_id) FROM ticket_events e WHERE e.ticket_id=t.ticket_id AND e.event_type='accepted') AS accepted_sequence
      FROM tickets t
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      LEFT JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id
      WHERE t.ticket_id=?`).get(ticketId) as any;
    if(!row)return {authorized:false,reason:"ticket-missing"};
    if(row.status!=="accepted"||Number(row.workflow_eligible)!==0||row.workflow_id)return {authorized:false,reason:`ticket-${row.status}`};
    if(row.session_state!=="active"||Number(row.generation)!==ownerGeneration)return {authorized:false,reason:"session-authority-superseded"};
    if(expectedRunId) {
      if(row.recovery_state!=="running"||row.active_run_id!==expectedRunId)return {authorized:false,reason:"recovery-claim-superseded"};
    } else if(!['pending','running','awaiting_delivery'].includes(String(row.recovery_state??""))) {
      return {authorized:false,reason:`recovery-${row.recovery_state??"missing"}`};
    }
    const acceptedSequence=Number(row.accepted_sequence);
    if(!Number.isSafeInteger(acceptedSequence)||acceptedSequence<=0)return {authorized:false,reason:"acceptance-sequence-missing"};
    return {authorized:true,ticketId:row.ticket_id,ownerSessionKey:row.owner_session_key,ownerGeneration,createdAt:row.created_at,
      acceptedSequence,recoveryState:row.recovery_state,activeRunId:row.active_run_id};
  } finally {db.close();}
}

export function touchDirectRecoveryClaim(path:string,input:{ticketId:string;ownerSessionKey:string;ownerGeneration:number;runId:string}) {
  const db=openDb(path),now=stamp();
  try {
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET updated_at=?
      WHERE ticket_id=? AND state='running' AND active_run_id=? AND owner_generation=?
        AND EXISTS(SELECT 1 FROM cnx_sessions WHERE session_key=? AND state='active' AND generation=?)`)
      .run(now,input.ticketId,input.runId,input.ownerGeneration,input.ownerSessionKey,input.ownerGeneration).changes)===1;
  } finally {db.close();}
}

export function queueBehindOlderRecovery(path:string,input:{sessionKey:string;runId:string;reason?:string}) {
  const db=openDb(path),now=stamp();
  try {
    db.exec("BEGIN IMMEDIATE");
    const current=db.prepare(`SELECT t.ticket_id,t.status,t.workflow_eligible,t.workflow_id,s.state AS session_state,s.generation,
      (SELECT MIN(e.event_id) FROM ticket_events e WHERE e.ticket_id=t.ticket_id AND e.event_type='accepted') AS accepted_sequence
      FROM tickets t JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      WHERE t.owner_session_key=? AND t.run_id=? ORDER BY t.created_at DESC LIMIT 1`).get(input.sessionKey,input.runId) as any;
    const sequence=Number(current?.accepted_sequence);
    if(!current||current.status!=="accepted"||Number(current.workflow_eligible)!==0||current.workflow_id||current.session_state!=="active"
      ||!Number.isSafeInteger(sequence)||sequence<=0){db.exec("COMMIT");return undefined;}
    const predecessor=db.prepare(`SELECT older.ticket_id,MIN(accepted.event_id) AS accepted_sequence,recovery.state,recovery.next_attempt_at
      FROM tickets older
      JOIN ticket_events accepted ON accepted.ticket_id=older.ticket_id AND accepted.event_type='accepted'
      JOIN cnx_direct_recovery recovery ON recovery.ticket_id=older.ticket_id
      WHERE older.owner_session_key=? AND older.ticket_id<>? AND older.status='accepted'
        AND older.workflow_eligible=0 AND older.workflow_id IS NULL
        AND recovery.owner_generation=? AND recovery.state IN ('pending','running','awaiting_delivery')
      GROUP BY older.ticket_id,recovery.state,recovery.next_attempt_at
      HAVING MIN(accepted.event_id)<?
      ORDER BY accepted_sequence LIMIT 1`).get(input.sessionKey,current.ticket_id,current.generation,sequence) as any;
    if(!predecessor){db.exec("COMMIT");return undefined;}
    const reason=(input.reason??`Queued behind older Direct Recovery ${predecessor.ticket_id}`).slice(0,2000);
    db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at
    ) VALUES (?,'resume','pending',0,NULL,?,?,?, ?,?)
    ON CONFLICT(ticket_id) DO UPDATE SET
      mode='resume',state=CASE WHEN cnx_direct_recovery.state IN ('running','awaiting_delivery') THEN cnx_direct_recovery.state ELSE 'pending' END,
      active_run_id=CASE WHEN cnx_direct_recovery.state='running' THEN cnx_direct_recovery.active_run_id ELSE NULL END,
      next_attempt_at=CASE WHEN cnx_direct_recovery.state IN ('running','awaiting_delivery') THEN cnx_direct_recovery.next_attempt_at ELSE excluded.next_attempt_at END,
      last_error=excluded.last_error,owner_generation=excluded.owner_generation,updated_at=excluded.updated_at`)
      .run(current.ticket_id,now,reason,current.generation,now,now);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,
      response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`)
      .run(reason,reason,now,current.ticket_id);
    db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
      .run(current.ticket_id,"direct_recovery_serialized",JSON.stringify({ownerSessionKey:input.sessionKey,ownerGeneration:Number(current.generation),acceptedSequence:sequence,
        predecessorTicketId:predecessor.ticket_id,predecessorAcceptedSequence:Number(predecessor.accepted_sequence),predecessorState:predecessor.state,reason}),now);
    db.exec("COMMIT");
    return {ticketId:String(current.ticket_id),ownerGeneration:Number(current.generation),acceptedSequence:sequence,
      predecessorTicketId:String(predecessor.ticket_id),predecessorAcceptedSequence:Number(predecessor.accepted_sequence),predecessorState:String(predecessor.state)};
  } catch(error){try{db.exec("ROLLBACK");}catch{}throw error;} finally {db.close();}
}

export function installRecoveryOrderAdmission(api:any,config:RecoveryOrderConfig={}) {
  api.on?.("before_agent_run",async(_event:any,ctx:any)=>{
    const sessionKey=ctx?.sessionKey,runId=ctx?.runId;
    if(!sessionKey||!runId||sessionKey.includes(":subagent:"))return {outcome:"pass"};
    const workspace=resolve(config.workspaceDir??ctx?.workspaceDir??ctx?.config?.agents?.defaults?.workspace??process.cwd());
    const path=resolve(config.ticketDatabasePath??defaultTicketDatabase(workspace));
    const queued=queueBehindOlderRecovery(path,{sessionKey,runId});
    if(!queued)return {outcome:"pass"};
    api.logger.info?.(`CogentNexus-OpenClaw serialized Ticket ${queued.ticketId} behind ${queued.predecessorTicketId} (${queued.predecessorState}) in ${sessionKey}`);
    return {outcome:"block",reason:"CogentNexus-OpenClaw committed this request and queued it behind older Direct Recovery in the same session",
      category:"cogentnexus_recovery_order",metadata:queued};
  },{priority:1600,timeoutMs:5000});
}
