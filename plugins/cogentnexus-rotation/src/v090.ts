import { createHash, randomUUID } from "node:crypto";
import { existsSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { classifyDurableRequest } from "./admission.js";
import { hasVisibleAssistantOutput, parseDeliveryMarker, settleDeliveryTarget } from "./delivery-continuity.js";
import baseEntry from "./index.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type Cfg={workspaceDir?:string;ticketDatabasePath?:string;ticketRecoveryPollMs?:number;timeoutSeconds?:number;admissionMinimumScore?:number};
type Recovery={ticket_id:string;owner_session_key:string;prompt:string;mode:string;attempt_count:number};
type Turn={sessionKey:string;delayMs:number;deleteAfterRun:boolean;deliveryMode:"announce";name:string;tag:string;message:string};
const PATCH=Symbol.for("cogentnexus.v090.ticket-patch"), WRAP=Symbol.for("cogentnexus.v090.entry-wrap");
const now=()=>new Date().toISOString();
const dbPath=(cfg:Cfg,workspace:string)=>resolve(cfg.ticketDatabasePath??defaultTicketDatabase(workspace));

function openDb(path:string){
  new TicketStore(path).snapshot();
  const db=new DatabaseSync(path); db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
    ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    mode TEXT NOT NULL DEFAULT 'resume',state TEXT NOT NULL DEFAULT 'pending',attempt_count INTEGER NOT NULL DEFAULT 0,
    active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
    CREATE UNIQUE INDEX IF NOT EXISTS idx_cnx_direct_recovery_run ON cnx_direct_recovery(active_run_id) WHERE active_run_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_cnx_direct_recovery_due ON cnx_direct_recovery(state,next_attempt_at,updated_at);`);
  return db;
}
function addEvent(db:DatabaseSync,id:string,type:string,payload:unknown,stamp:string){db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)").run(id,type,JSON.stringify(payload),stamp);}
function queueRecovery(db:DatabaseSync,id:string,mode:"resume"|"redeliver",message:string,stamp:string){
  db.prepare(`INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,created_at,updated_at)
    VALUES (?,?,'pending',0,NULL,?,?,?,?) ON CONFLICT(ticket_id) DO UPDATE SET mode=excluded.mode,state='pending',active_run_id=NULL,
    next_attempt_at=excluded.next_attempt_at,last_error=excluded.last_error,updated_at=excluded.updated_at`)
    .run(id,mode,stamp,message.slice(0,2000),stamp,stamp);
}

export function isExplicitUserCancellation(message?:string){
  if(!message)return false;
  return /(?:reply operation )?aborted by user|user (?:cancelled|canceled)|(?:cancelled|canceled) by user|explicit user (?:stop|abort|cancel)/iu.test(message);
}

export function cancelSessionTickets(path:string,input:{runId:string;message?:string;now?:Date}){
  const db=openDb(path),stamp=(input.now??new Date()).toISOString(),message=(input.message??"Cancelled by user").slice(0,2000);
  try{
    db.exec("BEGIN IMMEDIATE");
    const owner=db.prepare("SELECT owner_session_key FROM tickets WHERE run_id=? ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
    if(!owner?.owner_session_key){db.exec("COMMIT");return{ownerSessionKey:null,cancelled:[] as string[]};}
    const rows=db.prepare("SELECT ticket_id,status,run_id FROM tickets WHERE owner_session_key=? AND status IN ('accepted','planned','running','waiting') ORDER BY created_at,ticket_id").all(owner.owner_session_key) as any[];
    const cancelled:string[]=[];
    for(const row of rows){
      const changed=db.prepare(`UPDATE tickets SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,
        failure_class=NULL,failure_message=?,response_ready_at=NULL,delivery_last_error=NULL,updated_at=?
        WHERE ticket_id=? AND status IN ('accepted','planned','running','waiting')`).run(message,stamp,row.ticket_id);
      if(changed.changes!==1)continue;
      cancelled.push(row.ticket_id);
      db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(row.ticket_id);
      db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=? WHERE ticket_id=?")
        .run(message,stamp,row.ticket_id);
      addEvent(db,row.ticket_id,"cancelled_by_user",{source:"openclaw-ui-stop",runId:input.runId,previousStatus:row.status,previousRunId:row.run_id,message},stamp);
    }
    db.exec("COMMIT");
    return{ownerSessionKey:owner.owner_session_key as string,cancelled};
  }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
}

export function markDirectRecovery(path:string,input:{runId:string;mode:"resume"|"redeliver";message?:string;now?:Date}){
  if(isExplicitUserCancellation(input.message)){cancelSessionTickets(path,{runId:input.runId,message:input.message,now:input.now});return false;}
  const db=openDb(path),stamp=(input.now??new Date()).toISOString(),message=(input.message??"Direct run interrupted").slice(0,2000);
  try{db.exec("BEGIN IMMEDIATE");const row=db.prepare("SELECT ticket_id FROM tickets WHERE run_id=? AND status='accepted' AND workflow_eligible=0 ORDER BY created_at DESC LIMIT 1").get(input.runId) as any;
    if(!row){db.exec("COMMIT");return false;}
    db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=? WHERE ticket_id=?")
      .run(message,message,stamp,row.ticket_id); queueRecovery(db,row.ticket_id,input.mode,message,stamp);
    addEvent(db,row.ticket_id,input.mode==="redeliver"?"direct_redelivery_pending":"direct_retry_pending",{runId:input.runId,message},stamp);db.exec("COMMIT");return true;
  }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
}
function markSession(path:string,sessionKey:string,message:string){
  const db=openDb(path),stamp=now();try{db.exec("BEGIN IMMEDIATE");const row=db.prepare("SELECT ticket_id,run_id FROM tickets WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND response_ready_at IS NULL ORDER BY created_at DESC LIMIT 1").get(sessionKey) as any;
    if(!row){db.exec("COMMIT");return false;}db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=?").run(message,stamp,row.ticket_id);
    queueRecovery(db,row.ticket_id,"resume",message,stamp);addEvent(db,row.ticket_id,"direct_retry_pending",{runId:row.run_id,sessionKey,message},stamp);db.exec("COMMIT");return true;
  }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
}
export function patchTicketStore(){
  const p=TicketStore.prototype as any;if(p[PATCH])return;Object.defineProperty(p,PATCH,{value:true});
  const finalize=TicketStore.prototype.finalizeDirectRun, failDelivery=TicketStore.prototype.failDirectDelivery;
  TicketStore.prototype.finalizeDirectRun=function(input:Parameters<TicketStore["finalizeDirectRun"]>[0]){
    if(!input.success&&isExplicitUserCancellation(input.message)){cancelSessionTickets(this.databasePath,{runId:input.runId,message:input.message,now:input.now});return"unchanged";}
    if(!input.success&&input.interrupted)return markDirectRecovery(this.databasePath,{runId:input.runId,mode:"resume",message:input.message,now:input.now})?"waiting":"unchanged";
    return finalize.call(this,input);
  };
  TicketStore.prototype.failDirectDelivery=function(input:Parameters<TicketStore["failDirectDelivery"]>[0]){
    return markDirectRecovery(this.databasePath,{runId:input.runId,mode:"redeliver",message:input.message,now:input.now})?"waiting":failDelivery.call(this,input);
  };
  TicketStore.prototype.recoverUndeliveredDirect=function(input:Parameters<TicketStore["recoverUndeliveredDirect"]>[0]={}){
    const db=openDb(this.databasePath),n=input.now??new Date(),cutoff=new Date(n.getTime()-Math.max(1000,input.olderThanMs??120000)).toISOString(),stamp=n.toISOString();
    try{db.exec("BEGIN IMMEDIATE");const rows=db.prepare("SELECT ticket_id,run_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL AND response_ready_at<=? ORDER BY response_ready_at LIMIT ?").all(cutoff,Math.max(1,Math.min(input.limit??100,1000))) as any[];
      for(const r of rows){const m="Direct response delivery was not confirmed before deadline";db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,response_ready_at=NULL,updated_at=? WHERE ticket_id=?").run(m,m,stamp,r.ticket_id);queueRecovery(db,r.ticket_id,"redeliver",m,stamp);addEvent(db,r.ticket_id,"direct_redelivery_timeout",{runId:r.run_id,cutoff},stamp);}db.exec("COMMIT");return [];
    }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
  };
  TicketStore.prototype.promotePendingDirectForSession=function(input:Parameters<TicketStore["promotePendingDirectForSession"]>[0]){markSession(this.databasePath,input.sessionKey,input.reason??"Post-compaction continuation");return undefined;};
}
export const isDashboardSession=(key:string)=>/^agent:[^:]+:dashboard:/u.test(key);
export const directRecoveryBackoffMs=(attempt:number)=>[5,15,30,60,120,300][Math.max(0,Math.min(5,attempt-1))]*1000;
function fingerprint(messages:unknown[]){for(let i=messages.length-1;i>=0;i--){const m=messages[i] as any;if(m?.role==="assistant"&&hasVisibleAssistantOutput([m]))return createHash("sha256").update(JSON.stringify(m)).digest("hex");}return undefined;}
function resetCompletions(workspace:string){const root=resolve(workspace,".cogent","workflows");if(!existsSync(root))return 0;let count=0;for(const e of readdirSync(root,{withFileTypes:true})){if(!e.isDirectory())continue;const path=join(root,e.name,"completion.json");if(!existsSync(path))continue;try{const n=JSON.parse(readFileSync(path,"utf8"));if(n?.deliveryStatus!=="pending"||(!n.scheduledAt&&!n.deliveryRunId))continue;delete n.scheduledAt;delete n.deliveryRunId;const tmp=`${path}.${process.pid}.v090.tmp`;writeFileSync(tmp,`${JSON.stringify(n,null,2)}\n`);renameSync(tmp,path);count++;}catch{}}return count;}
export function prepareV090RecoveryState(workspace:string,cfg:Cfg={}){
  const path=dbPath(cfg,workspace),db=openDb(path),stamp=now();let reopened=0,outboxReset=0,cancelledLegacy=0;
  try{db.exec("BEGIN IMMEDIATE");const rows=db.prepare("SELECT ticket_id,prompt,status,workflow_eligible,failure_class,failure_message FROM tickets WHERE status IN ('waiting','failed') AND workflow_id IS NULL AND ((workflow_eligible=1 AND failure_class='interrupted') OR (status='failed' AND workflow_eligible=0 AND failure_class='permanent' AND failure_message='Reply operation aborted by user')) ORDER BY created_at").all() as any[];
    for(const r of rows){
      const legacyAbort=r.failure_class==="permanent"&&r.failure_message==="Reply operation aborted by user";
      if(legacyAbort){
        db.prepare("UPDATE tickets SET status='cancelled',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,failure_class=NULL,updated_at=? WHERE ticket_id=?").run(stamp,r.ticket_id);
        db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(r.ticket_id);
        db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error='legacy user abort migrated to cancelled',updated_at=? WHERE ticket_id=?").run(stamp,r.ticket_id);
        addEvent(db,r.ticket_id,"v090_user_abort_cancelled",{previousStatus:r.status},stamp);cancelledLegacy++;continue;
      }
      if(classifyDurableRequest(r.prompt,cfg.admissionMinimumScore??5).lane!=="direct")continue;
      db.prepare("DELETE FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").run(r.ticket_id);const c=db.prepare("UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,response_ready_at=NULL,delivery_confirmed_at=NULL,delivery_last_error=NULL,result_json=NULL,failure_class='interrupted',updated_at=? WHERE ticket_id=? AND workflow_id IS NULL").run(stamp,r.ticket_id);if(c.changes){const reason=`v0.9.0 reopened ${r.status} Direct Ticket`;queueRecovery(db,r.ticket_id,"resume",reason,stamp);addEvent(db,r.ticket_id,"v090_direct_recovery_reopened",{previousStatus:r.status},stamp);reopened++;}}
    outboxReset=Number(db.prepare("UPDATE ticket_outbox SET scheduled_at=NULL,delivery_run_id=NULL WHERE delivery_status='pending' AND (scheduled_at IS NOT NULL OR delivery_run_id IS NOT NULL)").run().changes);
    db.prepare("UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,updated_at=? WHERE state='running'").run(stamp,stamp);db.exec("COMMIT");
  }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
  return{databasePath:path,reopened,cancelledLegacy,outboxReset,workflowDeliveryReset:resetCompletions(workspace)};
}
function resetStale(path:string,cfg:Cfg){const db=openDb(path);try{const cutoff=new Date(Date.now()-Math.max(15*60000,Math.min((cfg.timeoutSeconds??3600)*1000+60000,4*60*60000))).toISOString();return Number(db.prepare("UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,last_error=COALESCE(last_error,'stale Direct recovery reset'),updated_at=? WHERE state='running' AND updated_at<=?").run(now(),now(),cutoff).changes);}finally{db.close();}}
function due(path:string){const db=openDb(path);try{return db.prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.state='pending' AND t.status='accepted' AND t.workflow_eligible=0 AND (r.next_attempt_at IS NULL OR r.next_attempt_at<=?) ORDER BY COALESCE(r.next_attempt_at,r.created_at) LIMIT 1`).get(now()) as Recovery|undefined;}finally{db.close();}}
function claim(path:string,id:string,runId:string){const db=openDb(path);try{return db.prepare("UPDATE cnx_direct_recovery SET state='running',attempt_count=attempt_count+1,active_run_id=?,next_attempt_at=NULL,last_error=NULL,updated_at=? WHERE ticket_id=? AND state='pending'").run(runId,now(),id).changes===1;}finally{db.close();}}
function bindRun(path:string,id:string,oldRun:string,newRun:string){if(oldRun===newRun)return;const db=openDb(path);try{db.prepare("UPDATE cnx_direct_recovery SET active_run_id=?,updated_at=? WHERE ticket_id=? AND state='running' AND active_run_id=?").run(newRun,now(),id,oldRun);}finally{db.close();}}
function success(path:string,id:string,runId:string,mode:"transcript"|"channel"){
  const db=openDb(path),stamp=now();try{db.exec("BEGIN IMMEDIATE");const row=db.prepare("SELECT t.status,t.workflow_eligible,r.state,r.active_run_id FROM tickets t JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id WHERE t.ticket_id=?").get(id) as any;if(!row||row.status!=="accepted"||Number(row.workflow_eligible)!==0||row.state!=="running"||row.active_run_id!==runId){db.exec("COMMIT");return;}
    const result={directRecovery:true,runId,deliveryMode:mode};db.prepare("UPDATE tickets SET status='completed',result_json=?,response_ready_at=?,delivery_confirmed_at=?,delivery_last_error=NULL,failure_class=NULL,failure_message=NULL,updated_at=? WHERE ticket_id=?").run(JSON.stringify(result),stamp,stamp,stamp,id);db.prepare("UPDATE cnx_direct_recovery SET state='done',active_run_id=NULL,next_attempt_at=NULL,last_error=NULL,updated_at=? WHERE ticket_id=?").run(stamp,id);addEvent(db,id,"direct_recovery_response_ready",{runId,deliveryMode:mode},stamp);addEvent(db,id,"delivery_confirmed",{runId,recovery:true,deliveryMode:mode},stamp);addEvent(db,id,"completed",result,stamp);db.exec("COMMIT");
  }catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}
}
function retry(path:string,id:string,runId:string,message:string){const db=openDb(path),stamp=new Date();try{db.exec("BEGIN IMMEDIATE");const r=db.prepare("SELECT attempt_count FROM cnx_direct_recovery WHERE ticket_id=? AND state='running' AND active_run_id=?").get(id,runId) as any;if(!r){db.exec("COMMIT");return;}const next=new Date(stamp.getTime()+directRecoveryBackoffMs(Number(r.attempt_count))).toISOString();db.prepare("UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,last_error=?,updated_at=? WHERE ticket_id=?").run(next,message.slice(0,2000),stamp.toISOString(),id);db.prepare("UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? WHERE ticket_id=? AND status='accepted'").run(message.slice(0,2000),message.slice(0,2000),stamp.toISOString(),id);addEvent(db,id,"direct_recovery_retry",{runId,message,nextAttemptAt:next,attempt:Number(r.attempt_count)},stamp.toISOString());db.exec("COMMIT");}catch(e){try{db.exec("ROLLBACK");}catch{}throw e;}finally{db.close();}}
function recoveryPrompt(r:Recovery){return["#cogent-direct",`[CogentNexus Continuation: direct-recovery:${r.ticket_id}]`,r.mode==="redeliver"?"The previous final response was not confirmed as delivered. Reconstruct only the compact final response; do not repeat external side effects.":"The previous run was interrupted. Resume automatically from committed state; do not repeat completed side effects.","Preserve the original user intent. Inspect durable state and existing artifacts first.","Original committed request:",r.prompt].join("\n");}
async function monitor(api:any,sessionKey:string,runId:string,before:string|undefined,timeoutMs:number){const waited=await api.runtime.subagent.waitForRun({runId,timeoutMs});const after=await api.runtime.subagent.getSessionMessages({sessionKey,limit:8});const f=fingerprint(after.messages??[]);return{waited,fresh:Boolean(f&&f!==before)};}
async function launchRecovery(api:any,path:string,r:Recovery,cfg:Cfg){const attempt=Number(r.attempt_count)+1,planned=`cnx-direct-${r.ticket_id.replace(/[^A-Za-z0-9_-]/g,"-").slice(0,48)}-${attempt}-${randomUUID().slice(0,8)}`;if(!claim(path,r.ticket_id,planned))return;let runId=planned;try{const before=await api.runtime.subagent.getSessionMessages({sessionKey:r.owner_session_key,limit:8});const deliver=!isDashboardSession(r.owner_session_key);const launched=await api.runtime.subagent.run({sessionKey:r.owner_session_key,message:recoveryPrompt(r),deliver,idempotencyKey:planned});runId=launched.runId;bindRun(path,r.ticket_id,planned,runId);const o=await monitor(api,r.owner_session_key,runId,fingerprint(before.messages??[]),Math.max(60000,Math.min((cfg.timeoutSeconds??3600)*1000,3600000)));if(o.waited.status==="ok"&&o.fresh){success(path,r.ticket_id,runId,deliver?"channel":"transcript");return;}if(o.waited.status!=="timeout")retry(path,r.ticket_id,runId,o.waited.error??"Recovery produced no new visible assistant output");}catch(e){retry(path,r.ticket_id,runId,e instanceof Error?e.message:String(e));}}
function recoveryService(api:any,cfg:Cfg){let timer:ReturnType<typeof setInterval>|undefined,active=false;return{id:"cogentnexus-direct-recovery-v090",start:async(ctx:any)=>{const workspace=resolve(cfg.workspaceDir??ctx.config?.agents?.defaults?.workspace??process.cwd()),path=dbPath(cfg,workspace);const tick=async()=>{if(active)return;active=true;try{resetStale(path,cfg);const r=due(path);if(r)void launchRecovery(api,path,r,cfg);}catch(e){api.logger.warn(`CogentNexus Direct recovery scan failed: ${e instanceof Error?e.message:String(e)}`);}finally{active=false;}};await tick();timer=setInterval(()=>void tick(),Math.max(1000,Math.min(cfg.ticketRecoveryPollMs??5000,30000)));timer.unref?.();},stop:async()=>{if(timer)clearInterval(timer);timer=undefined;}};}

export async function executeCompatibilityWake(api:any,cfg:Cfg,input:Turn){const workspace=resolve(cfg.workspaceDir??process.cwd()),path=dbPath(cfg,workspace),target=parseDeliveryMarker(input.message),store=new TicketStore(path);try{const before=await api.runtime.subagent.getSessionMessages({sessionKey:input.sessionKey,limit:8});const deliver=!isDashboardSession(input.sessionKey);const run=await api.runtime.subagent.run({sessionKey:input.sessionKey,message:input.message,deliver,idempotencyKey:`cnx-scheduled-${createHash("sha256").update(`${input.sessionKey}\0${input.tag}`).digest("hex").slice(0,40)}-${randomUUID().slice(0,8)}`});const o=await monitor(api,input.sessionKey,run.runId,fingerprint(before.messages??[]),Math.max(60000,Math.min((cfg.timeoutSeconds??3600)*1000,3600000)));if(target&&o.waited.status==="ok"&&o.fresh)settleDeliveryTarget({workspaceDir:workspace,store,target,success:true});else if(target&&o.waited.status!=="timeout")settleDeliveryTarget({workspaceDir:workspace,store,target,success:false,error:o.waited.error??"Compatibility wake produced no new visible assistant output"});return o;}catch(e){if(target)settleDeliveryTarget({workspaceDir:workspace,store,target,success:false,error:e instanceof Error?e.message:String(e)});api.logger.warn(`CogentNexus compatibility wake failed for ${input.tag}: ${e instanceof Error?e.message:String(e)}`);throw e;}}
function compatWorkflow(api:any,cfg:Cfg){const timers=new Map<string,ReturnType<typeof setTimeout>>();const key=(s:string,t:string)=>`${s}\0${t}`;const unschedule=async(i:{sessionKey:string;tag:string})=>{const k=key(i.sessionKey,i.tag),x=timers.get(k);if(x){clearTimeout(x);timers.delete(k);}return{removed:x?1:0,failed:0};};const schedule=async(i:Turn)=>{await unschedule(i);const path=dbPath(cfg,resolve(cfg.workspaceDir??process.cwd()));if(i.tag.startsWith("cogent-resume-")||i.tag.startsWith("cogent-post-compact-")){markSession(path,i.sessionKey,i.tag.startsWith("cogent-post-compact-")?"Post-compaction continuation":"Interrupted Direct continuation");return{scheduled:true,compatibilityMode:"direct-recovery"};}const k=key(i.sessionKey,i.tag),t=setTimeout(()=>{timers.delete(k);void executeCompatibilityWake(api,cfg,i).catch(()=>{});},Math.max(0,i.delayMs??0));t.unref?.();timers.set(k,t);return{scheduled:true,compatibilityMode:"runtime-subagent"};};return{unscheduleSessionTurnsByTag:unschedule,scheduleSessionTurn:schedule};}

function wrap(){const entry=baseEntry as any;if(entry[WRAP])return;Object.defineProperty(entry,WRAP,{value:true});const register=baseEntry.register?.bind(baseEntry);baseEntry.register=(api:any)=>{patchTicketStore();const cfg=(api.pluginConfig??{}) as Cfg,reg=api.registerService?.bind(api),proxy=Object.create(api);proxy.session={...api.session,workflow:{...api.session?.workflow,...compatWorkflow(api,cfg)}};proxy.registerService=(service:any)=>{if(!reg)return;if(service?.id!=="cogentnexus-ticket-recovery"||typeof service.start!=="function")return reg(service);reg({...service,start:async(ctx:any)=>{const workspace=resolve(cfg.workspaceDir??ctx.config?.agents?.defaults?.workspace??process.cwd()),p=prepareV090RecoveryState(workspace,cfg);api.logger.info?.(`CogentNexus v0.9.0 recovery migration: reopened=${p.reopened} cancelledLegacy=${p.cancelledLegacy} outboxReset=${p.outboxReset} workflowDeliveryReset=${p.workflowDeliveryReset}`);return service.start(ctx);}});};register?.(proxy);reg?.(recoveryService(api,cfg));};}
wrap();
export default baseEntry;
