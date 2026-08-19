import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { launchRecovery } from "./v090.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

export const DIRECT_RECOVERY_ID = "cogentnexus-direct-recovery-v090";
export const ASSISTANT_DELIVERY_RETRY_MS = 30_000;

type Config = {
  cogentRoot?:string;
  workspaceDir?:string;
  ticketDatabasePath?:string;
  timeoutSeconds?:number;
  pythonCommand?:string;
};

type Recovery = {
  ticket_id:string;
  owner_session_key:string;
  prompt:string;
  mode:"resume"|"redeliver";
  attempt_count:number;
  owner_generation:number;
};

type Hooks = {
  beforeStart?:(ctx:any)=>Promise<void>;
  subscribePulse:(listener:()=>void)=>()=>void;
};

function openDb(path:string,readOnly=false) {
  if(!readOnly)new TicketStore(path).snapshot();
  return readOnly ? new DatabaseSync(path,{readOnly:true}) : new DatabaseSync(path);
}

function tableExists(db:DatabaseSync,name:string) {
  return Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
}

function columnExists(db:DatabaseSync,table:string,column:string) {
  if(!tableExists(db,table))return false;
  return (db.prepare(`PRAGMA table_info(${table})`).all() as Array<{name?:string}>).some((row)=>row.name===column);
}

function modelCallRecoveryFence(db:DatabaseSync,alias="r") {
  if(!tableExists(db,"cnx_direct_model_call"))return "";
  return ` AND NOT EXISTS (SELECT 1 FROM cnx_direct_model_call m
    WHERE m.ticket_id=${alias}.ticket_id AND m.state IN ('active','recovering'))`;
}

function deliveryLeaseSupported(db:DatabaseSync) {
  return columnExists(db,"cnx_assistant_delivery","claim_token")&&columnExists(db,"cnx_assistant_delivery","claim_expires_at");
}

export function resetStaleDirectRecovery(path:string,cfg:Config,now=new Date()):number {
  if(!existsSync(path))return 0;
  const db=openDb(path),stamp=now.toISOString();
  try {
    if(!tableExists(db,"cnx_direct_recovery")||!tableExists(db,"tickets")||!tableExists(db,"cnx_sessions"))return 0;
    const staleMs=Math.max(15*60_000,Math.min((cfg.timeoutSeconds??3600)*1000+60_000,4*60*60_000));
    const cutoff=new Date(now.getTime()-staleMs).toISOString();
    return Number(db.prepare(`UPDATE cnx_direct_recovery SET state='pending',active_run_id=NULL,next_attempt_at=?,
      last_error=COALESCE(last_error,'stale Direct recovery reset'),updated_at=? WHERE state='running' AND updated_at<=?
      AND ticket_id IN (SELECT t.ticket_id FROM tickets t JOIN cnx_sessions s ON s.session_key=t.owner_session_key
        WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
          AND s.state='active' AND s.generation=cnx_direct_recovery.owner_generation)`).run(stamp,stamp,cutoff).changes);
  } finally {db.close();}
}

export function dueDirectRecovery(path:string,now=new Date()):Recovery|undefined {
  if(!existsSync(path))return undefined;
  const db=openDb(path,true);
  try {
    if(!tableExists(db,"cnx_direct_recovery")||!tableExists(db,"tickets")||!tableExists(db,"cnx_sessions"))return undefined;
    const modelFence=modelCallRecoveryFence(db,"r");
    return db.prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count,r.owner_generation
      FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id
      JOIN cnx_sessions s ON s.session_key=t.owner_session_key
      WHERE r.state='pending' AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
        AND s.state='active' AND s.generation=r.owner_generation
        AND (r.next_attempt_at IS NULL OR r.next_attempt_at<=?)${modelFence}
      ORDER BY COALESCE(r.next_attempt_at,r.created_at) LIMIT 1`).get(now.toISOString()) as Recovery|undefined;
  } finally {db.close();}
}

function staleDelayMs(updatedAt:string,cfg:Config,nowMs:number) {
  const staleMs=Math.max(15*60_000,Math.min((cfg.timeoutSeconds??3600)*1000+60_000,4*60*60_000));
  const updated=Date.parse(updatedAt);
  return Number.isFinite(updated)?Math.max(0,updated+staleMs-nowMs):staleMs;
}

function nextAssistantDeliveryWakeMs(db:DatabaseSync,now=new Date()):number|undefined {
  if(!tableExists(db,"cnx_assistant_delivery"))return undefined;
  const nowMs=now.getTime();
  const retryCutoffMs=nowMs-ASSISTANT_DELIVERY_RETRY_MS;
  if(!deliveryLeaseSupported(db)) {
    const row=db.prepare("SELECT attempt_count,updated_at FROM cnx_assistant_delivery WHERE status='pending' ORDER BY updated_at LIMIT 1")
      .get() as {attempt_count?:number;updated_at?:string}|undefined;
    if(!row?.updated_at)return undefined;
    if(Number(row.attempt_count??0)===0)return 25;
    const updated=Date.parse(row.updated_at);
    return Number.isFinite(updated)?Math.max(25,updated+ASSISTANT_DELIVERY_RETRY_MS-nowMs):25;
  }
  const rows=db.prepare(`SELECT attempt_count,updated_at,claim_token,claim_expires_at
    FROM cnx_assistant_delivery WHERE status='pending' ORDER BY owner_session_key,delivery_id LIMIT 32`).all() as Array<{
      attempt_count?:number;updated_at?:string;claim_token?:string|null;claim_expires_at?:string|null;
    }>;
  let best:number|undefined;
  for(const row of rows) {
    let dueMs=nowMs;
    if(row.claim_token&&row.claim_expires_at) {
      const expiry=Date.parse(row.claim_expires_at);
      dueMs=Number.isFinite(expiry)?expiry:nowMs;
    } else if(Number(row.attempt_count??0)>0&&row.updated_at) {
      const updated=Date.parse(row.updated_at);
      dueMs=Number.isFinite(updated)?Math.max(updated+ASSISTANT_DELIVERY_RETRY_MS,retryCutoffMs+ASSISTANT_DELIVERY_RETRY_MS):nowMs;
    }
    const delay=Math.max(25,dueMs-nowMs);
    best=best===undefined?delay:Math.min(best,delay);
  }
  return best;
}

export function nextDirectRecoveryWakeMs(path:string,cfg:Config,now=new Date()):number|undefined {
  if(!existsSync(path))return undefined;
  const db=openDb(path,true),nowMs=now.getTime();
  try {
    const delays:number[]=[];
    const hasRecoveryTables=tableExists(db,"cnx_direct_recovery")&&tableExists(db,"tickets")&&tableExists(db,"cnx_sessions");
    if(hasRecoveryTables) {
      const modelFence=modelCallRecoveryFence(db,"r");
      const pending=db.prepare(`SELECT r.next_attempt_at FROM cnx_direct_recovery r
        JOIN tickets t ON t.ticket_id=r.ticket_id JOIN cnx_sessions s ON s.session_key=t.owner_session_key
        WHERE r.state='pending' AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
          AND s.state='active' AND s.generation=r.owner_generation${modelFence}
        ORDER BY CASE WHEN r.next_attempt_at IS NULL THEN 0 ELSE 1 END,r.next_attempt_at LIMIT 1`).get() as {next_attempt_at?:string|null}|undefined;
      if(pending) {
        if(!pending.next_attempt_at)delays.push(0);
        else {
          const at=Date.parse(pending.next_attempt_at);
          delays.push(Number.isFinite(at)?Math.max(0,at-nowMs):0);
        }
      }
      const running=db.prepare(`SELECT r.updated_at FROM cnx_direct_recovery r
        JOIN tickets t ON t.ticket_id=r.ticket_id JOIN cnx_sessions s ON s.session_key=t.owner_session_key
        WHERE r.state='running' AND t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL
          AND s.state='active' AND s.generation=r.owner_generation
        ORDER BY r.updated_at LIMIT 1`).get() as {updated_at?:string}|undefined;
      if(running?.updated_at)delays.push(staleDelayMs(running.updated_at,cfg,nowMs));
    }
    const deliveryDelay=nextAssistantDeliveryWakeMs(db,now);
    if(deliveryDelay!==undefined)delays.push(deliveryDelay);
    if(delays.length===0)return undefined;
    return Math.max(25,Math.min(...delays));
  } finally {db.close();}
}

export function assistantDeliveryDue(path:string,now=new Date()):boolean {
  if(!existsSync(path))return false;
  const db=openDb(path,true);
  try {
    if(!tableExists(db,"cnx_assistant_delivery"))return false;
    const stamp=now.toISOString();
    const cutoff=new Date(now.getTime()-ASSISTANT_DELIVERY_RETRY_MS).toISOString();
    if(!deliveryLeaseSupported(db)) {
      return Boolean(db.prepare(`SELECT 1 FROM cnx_assistant_delivery
        WHERE status='pending' AND (attempt_count=0 OR updated_at<=?) LIMIT 1`).get(cutoff));
    }
    return Boolean(db.prepare(`SELECT 1 FROM cnx_assistant_delivery
      WHERE status='pending'
        AND (claim_token IS NULL OR claim_expires_at IS NULL OR claim_expires_at<=?)
        AND (attempt_count=0 OR updated_at<=?) LIMIT 1`).get(stamp,cutoff));
  } finally {db.close();}
}

function kickHostDelivery(workspace:string,cfg:Config) {
  const script=resolve(workspace,"skills","cogentnexus","scripts","host_delivery.py");
  if(!existsSync(script))return false;
  const root=resolve(cfg.cogentRoot??join(workspace,".cogent"));
  try {
    const child=spawn(cfg.pythonCommand??"python",[script,"--root",root,"flush"],{
      detached:true,stdio:"ignore",windowsHide:true,
    });
    child.unref();
    return true;
  } catch {return false;}
}

export function createEventDrivenDirectRecoveryService(api:any,cfg:Config,hooks:Hooks) {
  let wake:ReturnType<typeof setTimeout>|undefined;
  let removePulse:(()=>void)|undefined;
  let active=false,rerun=false,stopped=false;
  const service:any={
    id:DIRECT_RECOVERY_ID,
    start:async(ctx:any)=>{
      await hooks.beforeStart?.(ctx);
      const workspace=resolve(cfg.workspaceDir??ctx.config?.agents?.defaults?.workspace??process.cwd());
      const path=resolve(cfg.ticketDatabasePath??defaultTicketDatabase(workspace));
      const arm=()=>{
        if(wake)clearTimeout(wake);wake=undefined;
        if(stopped)return;
        const delay=nextDirectRecoveryWakeMs(path,cfg);
        if(delay===undefined)return;
        wake=setTimeout(()=>{wake=undefined;pulse();},delay);wake.unref?.();
      };
      const run=async()=>{
        if(stopped)return;
        if(active){rerun=true;return;}
        active=true;
        try {
          do {
            rerun=false;
            const reset=resetStaleDirectRecovery(path,cfg);
            if(reset>0)api.logger.warn?.(`CogentNexus reset ${reset} stale Direct recovery claim(s)`);
            if(assistantDeliveryDue(path))kickHostDelivery(workspace,cfg);
            const recovery=dueDirectRecovery(path);
            if(recovery) {
              void launchRecovery(api,path,workspace,recovery,cfg as any)
                .catch((error)=>api.logger.warn?.(`CogentNexus Direct recovery launch failed: ${error instanceof Error?error.message:String(error)}`))
                .finally(()=>queueMicrotask(pulse));
            }
          } while(rerun&&!stopped);
        } catch(error) {
          api.logger.warn?.(`CogentNexus Direct recovery event worker failed: ${error instanceof Error?error.message:String(error)}`);
        } finally {
          active=false;
          arm();
        }
      };
      const pulse=()=>{void run();};
      removePulse=hooks.subscribePulse(pulse);
      await run();
    },
    stop:async()=>{
      stopped=true;removePulse?.();removePulse=undefined;
      if(wake)clearTimeout(wake);wake=undefined;
    },
  };
  return service;
}
