import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { contextPressure } from "./v090-context-guard.js";
import { defaultTicketDatabase } from "./ticket-store.js";

export type CompactionBoundaryConfig={workspaceDir?:string;ticketDatabasePath?:string};

export function createCompactionBoundaryApi(api:any) {
  const proxy=Object.create(api);
  const originalOn=api.on?.bind(api);
  if(originalOn) {
    proxy.on=(name:string,handler:any,options?:any)=>{
      if(name==="after_compaction") {
        // v0.9 owns continuation through Ticket/Direct-Recovery state. The
        // legacy post-compaction hook scheduled a synthetic turn for every
        // compaction and cannot distinguish a user/manual Compact from an
        // overflow compaction. Suppress that wake path; a passive observer is
        // installed separately and may only settle an already-authorized hold.
        api.logger.info?.("CogentNexus v0.9 suppressed legacy after_compaction synthetic continuation registration");
        return undefined;
      }
      return originalOn(name,handler,options);
    };
  }
  return proxy;
}

function existingContextStore(databasePath:string) {
  if(!existsSync(databasePath))return false;
  let db:DatabaseSync|undefined;
  try {
    db=new DatabaseSync(databasePath,{readOnly:true});
    const names=new Set((db.prepare(`SELECT name FROM sqlite_master WHERE type='table' AND name IN
      ('cnx_context_maintenance','cnx_sessions','tickets','ticket_events')`).all() as Array<{name:string}>).map((row)=>row.name));
    return ["cnx_context_maintenance","cnx_sessions","tickets","ticket_events"].every((name)=>names.has(name));
  } catch {return false;} finally {db?.close();}
}

export function settleExistingContextHoldFromCompaction(input:{
  databasePath:string;
  sessionKey:string;
  tokenCount?:number;
  session?:{sessionId?:string;totalTokens?:number;totalTokensFresh?:boolean;contextTokens?:number}|null;
  now?:Date;
}) {
  // A user/manual Compact must be zero-mutation when CNX has no pre-existing
  // context runtime state. Do not bootstrap SQLite or create tables here.
  if(!existingContextStore(input.databasePath))return {found:false,settled:false,reason:"no-existing-context-store"};
  const db=new DatabaseSync(input.databasePath),stamp=(input.now??new Date()).toISOString();
  try {
    db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE");
    const row=db.prepare(`SELECT session_key,owner_generation,ticket_id,state FROM cnx_context_maintenance
      WHERE session_key=? AND state IN ('pending','running','degraded')`).get(input.sessionKey) as any;
    if(!row){db.exec("COMMIT");return {found:false,settled:false,reason:"no-active-context-hold"};}
    const authority=db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(input.sessionKey) as any;
    if(!authority||authority.state!=="active"||Number(authority.generation)!==Number(row.owner_generation)){
      db.exec("COMMIT");return {found:true,settled:false,reason:"authority-superseded"};
    }
    const session=input.session??{};
    const contextWindow=Number(session.contextTokens)>0?Number(session.contextTokens):undefined;
    const eventTokens=Number(input.tokenCount)>0?Number(input.tokenCount):undefined;
    const freshTokens=session.totalTokensFresh===true&&Number(session.totalTokens)>0?Number(session.totalTokens):undefined;
    const observed=eventTokens&&freshTokens?Math.max(eventTokens,freshTokens):(freshTokens??eventTokens);
    if(observed===undefined||contextWindow===undefined) {
      db.prepare(`UPDATE cnx_context_maintenance SET session_id=COALESCE(?,session_id),last_tokens_after=COALESCE(?,last_tokens_after),
        last_action='native-compact-observed-unmeasured',updated_at=? WHERE session_key=? AND owner_generation=?
        AND state IN ('pending','running','degraded')`)
        .run(session.sessionId??null,observed??null,stamp,input.sessionKey,row.owner_generation);
      db.exec("COMMIT");
      return {found:true,settled:false,reason:"unmeasured",observedTokens:observed,contextWindow};
    }
    const pressure=contextPressure({session:{...session,totalTokens:observed,totalTokensFresh:true,contextTokens:contextWindow},config:{}});
    if(pressure.level!=="normal"){
      db.prepare(`UPDATE cnx_context_maintenance SET session_id=COALESCE(?,session_id),context_window=?,projected_tokens=?,
        last_tokens_after=?,last_action='native-compact-observed-pressure-remains',updated_at=?
        WHERE session_key=? AND owner_generation=? AND state IN ('pending','running','degraded')`)
        .run(session.sessionId??null,contextWindow,observed,observed,stamp,input.sessionKey,row.owner_generation);
      db.exec("COMMIT");
      return {found:true,settled:false,reason:"pressure-remains",observedTokens:observed,contextWindow};
    }
    const changed=db.prepare(`UPDATE cnx_context_maintenance SET state='done',session_id=COALESCE(?,session_id),
      context_window=?,projected_tokens=?,last_tokens_after=?,last_action='native-compact-satisfied',
      last_error=NULL,next_attempt_at=NULL,updated_at=?,completed_at=?
      WHERE session_key=? AND owner_generation=? AND state IN ('pending','running','degraded')`)
      .run(session.sessionId??null,contextWindow,observed,observed,stamp,stamp,input.sessionKey,row.owner_generation);
    if(changed.changes===1) {
      db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
        .run(row.ticket_id,"context_compaction_satisfied",JSON.stringify({source:"openclaw-after-compaction",observedTokens:observed,contextWindow}),stamp);
    }
    db.exec("COMMIT");
    return {found:true,settled:changed.changes===1,reason:changed.changes===1?"safe-context":"concurrent-change",observedTokens:observed,contextWindow};
  } catch(error){try{db.exec("ROLLBACK");}catch{}throw error;} finally {db.close();}
}

export function installPassiveCompactionObserver(api:any,config:CompactionBoundaryConfig={}) {
  api.on?.("after_compaction",async(event:any,ctx:any)=>{
    const sessionKey=ctx?.sessionKey;
    if(!sessionKey||sessionKey.includes(":subagent:"))return;
    const workspaceDir=resolve(config.workspaceDir??ctx?.workspaceDir??process.cwd());
    const databasePath=resolve(config.ticketDatabasePath??defaultTicketDatabase(workspaceDir));
    if(!existsSync(databasePath))return;
    let session:any=null;
    try {
      const response=await api.runtime?.gateway?.request?.("sessions.describe",{key:sessionKey},{timeoutMs:5000});
      session=response?.session??null;
    } catch {}
    const result=settleExistingContextHoldFromCompaction({databasePath,sessionKey,tokenCount:event?.tokenCount,session});
    if(result.found)api.logger.info?.(`CogentNexus passive compaction observation ${sessionKey}: settled=${result.settled} reason=${result.reason} tokens=${result.observedTokens??"?"}/${result.contextWindow??"?"}`);
  },{priority:50,timeoutMs:7500});
}
