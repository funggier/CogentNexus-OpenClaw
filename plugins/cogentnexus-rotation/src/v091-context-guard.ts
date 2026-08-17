import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

export type ContextGuardConfig = {
  contextSafetyEnabled?: boolean;
  contextSoftRatio?: number;
  contextHardRatio?: number;
  contextMinimumHeadroomTokens?: number;
  contextMaintenancePollMs?: number;
  contextMaintenanceMaxAttempts?: number;
  contextCompactionTimeoutMs?: number;
  contextHardTrimMaxLines?: number;
  workspaceDir?: string;
  ticketDatabasePath?: string;
};

type SessionDescription = {
  key?:string;
  sessionId?:string;
  totalTokens?:number;
  totalTokensFresh?:boolean;
  contextTokens?:number;
  compactionCheckpointCount?:number;
};

type Maintenance = {
  session_key:string;
  owner_generation:number;
  ticket_id:string;
  state:string;
  hard_required:number;
  attempt_count:number;
  session_id:string|null;
  context_window:number|null;
  projected_tokens:number|null;
};

export type ContextPressure = {
  contextWindow:number;
  projectedTokens:number;
  softLimit:number;
  hardLimit:number;
  ratio:number;
  level:"normal"|"soft"|"hard";
  source:"fresh-session-counter"|"estimated-loaded-context";
};

const iso=()=>new Date().toISOString();

function openDb(path:string) {
  new TicketStore(path).snapshot();
  const db=new DatabaseSync(path);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_context_maintenance(
    session_key TEXT PRIMARY KEY,
    owner_generation INTEGER NOT NULL,
    ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    state TEXT NOT NULL DEFAULT 'pending' CHECK(state IN ('pending','running','done','cancelled','degraded')),
    hard_required INTEGER NOT NULL DEFAULT 0,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    next_attempt_at TEXT,
    last_error TEXT,
    session_id TEXT,
    context_window INTEGER,
    projected_tokens INTEGER,
    last_tokens_before INTEGER,
    last_tokens_after INTEGER,
    last_action TEXT,
    capsule_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT
  );
  CREATE INDEX IF NOT EXISTS idx_cnx_context_due ON cnx_context_maintenance(state,next_attempt_at,updated_at);`);
  return db;
}

function authority(db:DatabaseSync,key:string) {
  const exists=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_sessions'").get();
  if(!exists) return undefined;
  const row=db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(key) as any;
  return row ? {state:String(row.state),generation:Number(row.generation)} : undefined;
}

function estimateTokens(value:unknown) {
  let text="";
  try{text=typeof value==="string"?value:JSON.stringify(value??"");}catch{text=String(value??"");}
  return Math.ceil(text.length/2.5);
}

function ratio(value:number|undefined,fallback:number) {
  return typeof value==="number"&&Number.isFinite(value)?Math.max(0.35,Math.min(0.97,value)):fallback;
}

function defaultSoft(window:number) {
  if(window<=32768)return 0.68;
  if(window<=65536)return 0.74;
  if(window<=131072)return 0.80;
  return 0.84;
}

export function contextPressure(input:{messages?:unknown[];prompt?:string;systemPrompt?:string;session?:SessionDescription|null;config?:ContextGuardConfig}):ContextPressure {
  const session=input.session??{};
  const window=Math.max(8192,Math.floor(Number(session.contextTokens)||32768));
  const estimated=estimateTokens(input.messages??[])+estimateTokens(input.systemPrompt??"")+estimateTokens(input.prompt??"");
  const fresh=session.totalTokensFresh===true&&Number(session.totalTokens)>0;
  const projected=Math.max(estimated,fresh?Number(session.totalTokens)+estimateTokens(input.prompt??""):0);
  const softRatio=ratio(input.config?.contextSoftRatio,defaultSoft(window));
  const hardRatio=Math.max(softRatio+0.04,ratio(input.config?.contextHardRatio,0.90));
  const configured=input.config?.contextMinimumHeadroomTokens;
  const headroom=typeof configured==="number"&&Number.isFinite(configured)
    ? Math.max(2048,Math.min(Math.floor(configured),Math.floor(window*0.45)))
    : Math.max(4096,Math.min(16384,Math.floor(window*0.18)));
  const softLimit=Math.max(4096,Math.min(Math.floor(window*softRatio),window-headroom));
  const hardLimit=Math.max(softLimit+1024,Math.min(Math.floor(window*hardRatio),window-2048));
  return {
    contextWindow:window,projectedTokens:projected,softLimit,hardLimit,ratio:projected/window,
    level:projected>=hardLimit?"hard":projected>=softLimit?"soft":"normal",
    source:fresh?"fresh-session-counter":"estimated-loaded-context",
  };
}

async function describe(api:any,key:string):Promise<SessionDescription|null> {
  const request=api.runtime?.gateway?.request;
  if(typeof request!=="function")return null;
  const response=await request("sessions.describe",{key},{timeoutMs:5000});
  return response?.session??null;
}

function currentDirectTicket(db:DatabaseSync,key:string,runId?:string) {
  if(runId) {
    const exact=db.prepare(`SELECT ticket_id,run_id,prompt FROM tickets WHERE owner_session_key=? AND run_id=?
      AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL ORDER BY created_at DESC LIMIT 1`).get(key,runId) as any;
    if(exact)return exact as {ticket_id:string;run_id:string;prompt:string};
  }
  return db.prepare(`SELECT ticket_id,run_id,prompt FROM tickets WHERE owner_session_key=?
    AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL ORDER BY created_at DESC LIMIT 1`).get(key) as any;
}

function event(db:DatabaseSync,ticketId:string,type:string,payload:unknown,stamp:string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId,type,JSON.stringify(payload),stamp);
}

function authorize(databasePath:string,input:{sessionKey:string;runId:string;session:SessionDescription|null;pressure:ContextPressure}) {
  const db=openDb(databasePath),stamp=iso();
  try {
    db.exec("BEGIN IMMEDIATE");
    const auth=authority(db,input.sessionKey),ticket=currentDirectTicket(db,input.sessionKey,input.runId);
    if(!auth||auth.state!=="active"||!ticket){db.exec("COMMIT");return undefined;}
    const recoveryTable=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get();
    if(!recoveryTable) db.exec(`CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
      mode TEXT NOT NULL DEFAULT 'resume',state TEXT NOT NULL DEFAULT 'pending',attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,owner_generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,updated_at TEXT NOT NULL)`);
    const reason=`context pressure ${Math.round(input.pressure.ratio*100)}% (${input.pressure.projectedTokens}/${input.pressure.contextWindow})`;
    db.prepare(`INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at)
      VALUES (?,'resume','pending',0,NULL,?,?,?, ?,?) ON CONFLICT(ticket_id) DO UPDATE SET
      mode='resume',state='pending',active_run_id=NULL,next_attempt_at=excluded.next_attempt_at,last_error=excluded.last_error,
      owner_generation=excluded.owner_generation,updated_at=excluded.updated_at`)
      .run(ticket.ticket_id,stamp,reason,auth.generation,stamp,stamp);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,response_ready_at=NULL,
      delivery_confirmed_at=NULL,updated_at=? WHERE ticket_id=? AND status='accepted'`).run(reason,reason,stamp,ticket.ticket_id);
    db.prepare(`INSERT INTO cnx_context_maintenance(session_key,owner_generation,ticket_id,state,hard_required,attempt_count,next_attempt_at,last_error,
      session_id,context_window,projected_tokens,created_at,updated_at) VALUES (?,?,?,'pending',?,0,?,NULL,?,?,?,?,?)
      ON CONFLICT(session_key) DO UPDATE SET owner_generation=excluded.owner_generation,ticket_id=excluded.ticket_id,state='pending',
      hard_required=excluded.hard_required,attempt_count=0,next_attempt_at=excluded.next_attempt_at,last_error=NULL,
      session_id=excluded.session_id,context_window=excluded.context_window,projected_tokens=excluded.projected_tokens,
      capsule_path=NULL,completed_at=NULL,updated_at=excluded.updated_at`)
      .run(input.sessionKey,auth.generation,ticket.ticket_id,input.pressure.level==="hard"?1:0,stamp,input.session?.sessionId??null,
        input.pressure.contextWindow,input.pressure.projectedTokens,stamp,stamp);
    event(db,ticket.ticket_id,"context_pressure_deferred",{sessionKey:input.sessionKey,generation:auth.generation,sessionId:input.session?.sessionId,
      pressure:input.pressure,reason},stamp);
    db.exec("COMMIT");
    return {ticketId:ticket.ticket_id,generation:auth.generation};
  } catch(error){try{db.exec("ROLLBACK");}catch{}throw error;}finally{db.close();}
}

function due(databasePath:string,maxAttempts:number):Maintenance[] {
  const db=openDb(databasePath),stamp=iso();
  try {
    db.prepare(`UPDATE cnx_context_maintenance SET state='cancelled',last_error='session authority superseded',next_attempt_at=NULL,
      updated_at=?,completed_at=? WHERE state IN ('pending','running','degraded') AND NOT EXISTS(
        SELECT 1 FROM cnx_sessions s WHERE s.session_key=cnx_context_maintenance.session_key AND s.state='active'
          AND s.generation=cnx_context_maintenance.owner_generation)`).run(stamp,stamp);
    db.prepare(`UPDATE cnx_context_maintenance SET state='cancelled',last_error=COALESCE(last_error,'context maintenance retry limit reached'),
      next_attempt_at=NULL,updated_at=?,completed_at=? WHERE state='degraded' AND attempt_count>=?`).run(stamp,stamp,maxAttempts);
    return db.prepare(`SELECT session_key,owner_generation,ticket_id,state,hard_required,attempt_count,session_id,context_window,projected_tokens
      FROM cnx_context_maintenance WHERE state IN ('pending','degraded') AND attempt_count<? AND (next_attempt_at IS NULL OR next_attempt_at<=?)
      ORDER BY hard_required DESC,updated_at,session_key LIMIT 4`).all(maxAttempts,stamp) as Maintenance[];
  } finally{db.close();}
}

function claim(databasePath:string,row:Maintenance) {
  const db=openDb(databasePath),stamp=iso();
  try{return Number(db.prepare(`UPDATE cnx_context_maintenance SET state='running',attempt_count=attempt_count+1,next_attempt_at=NULL,
    last_error=NULL,updated_at=? WHERE session_key=? AND owner_generation=? AND state IN ('pending','degraded') AND EXISTS(
      SELECT 1 FROM cnx_sessions s WHERE s.session_key=? AND s.state='active' AND s.generation=?)`)
    .run(stamp,row.session_key,row.owner_generation,row.session_key,row.owner_generation).changes)===1;}finally{db.close();}
}

function currentAuthority(databasePath:string,row:Maintenance) {
  const db=openDb(databasePath);
  try{const auth=authority(db,row.session_key);return Boolean(auth&&auth.state==="active"&&auth.generation===row.owner_generation);}finally{db.close();}
}

function finish(databasePath:string,row:Maintenance,input:{state:"done"|"degraded"|"cancelled";action:string;before?:number;after?:number;error?:string;retryMs?:number;capsule?:string}) {
  const db=openDb(databasePath),stamp=iso(),next=input.retryMs?new Date(Date.now()+input.retryMs).toISOString():null;
  try{db.prepare(`UPDATE cnx_context_maintenance SET state=?,last_action=?,last_tokens_before=?,last_tokens_after=?,last_error=?,
    next_attempt_at=?,capsule_path=COALESCE(?,capsule_path),updated_at=?,completed_at=? WHERE session_key=? AND owner_generation=?`)
    .run(input.state,input.action,input.before??null,input.after??null,input.error?.slice(0,2000)??null,next,input.capsule??null,stamp,
      input.state==="done"||input.state==="cancelled"?stamp:null,row.session_key,row.owner_generation);}finally{db.close();}
}

async function snapshotCapsule(api:any,workspaceDir:string,databasePath:string,row:Maintenance,session:SessionDescription|null,reason:string) {
  const db=openDb(databasePath);let tickets:any[]=[];
  try{tickets=db.prepare(`SELECT ticket_id,status,run_id,workflow_id,failure_class,failure_message,prompt,created_at,updated_at
    FROM tickets WHERE owner_session_key=? ORDER BY created_at DESC LIMIT 32`).all(row.session_key) as any[];}finally{db.close();}
  for(const ticket of tickets) if(typeof ticket.prompt==="string"&&ticket.prompt.length>20000)ticket.prompt=`${ticket.prompt.slice(0,20000)}\n...[truncated in context capsule]`;
  let recent:any=null;
  try{recent=await api.runtime?.gateway?.request?.("chat.history",{sessionKey:row.session_key,limit:50,maxChars:50000},{timeoutMs:5000});}catch{}
  const hash=createHash("sha256").update(row.session_key).digest("hex").slice(0,16),dir=resolve(workspaceDir,".cogent","context",hash);
  mkdirSync(dir,{recursive:true});
  const path=resolve(dir,`g${row.owner_generation}-${iso().replace(/[:.]/g,"-")}.json`);
  writeFileSync(path,`${JSON.stringify({schemaVersion:1,createdAt:iso(),reason,ownerSessionKey:row.session_key,ownerGeneration:row.owner_generation,
    ticketId:row.ticket_id,sessionId:session?.sessionId??row.session_id,contextWindow:session?.contextTokens??row.context_window,
    projectedTokens:row.projected_tokens,totalTokens:session?.totalTokens,totalTokensFresh:session?.totalTokensFresh,
    compactionCheckpointCount:session?.compactionCheckpointCount,tickets,recentHistory:recent,
    note:"OpenClaw keeps/archives the full transcript. This bounded capsule preserves CNX authority, active intent and recent context before deterministic hard trimming."},null,2)}\n`);
  return path;
}

async function maintain(api:any,row:Maintenance,config:ContextGuardConfig,workspaceDir:string,databasePath:string) {
  const request=api.runtime?.gateway?.request;if(typeof request!=="function")throw new Error("runtime.gateway.request unavailable");
  if(!currentAuthority(databasePath,row)){finish(databasePath,row,{state:"cancelled",action:"authority-revoked"});return {action:"authority-revoked"};}
  let current=await describe(api,row.session_key);
  if(!current){finish(databasePath,row,{state:"cancelled",action:"owner-missing",error:"OpenClaw session missing"});return {action:"owner-missing"};}
  if(row.session_id&&current.sessionId&&row.session_id!==current.sessionId){finish(databasePath,row,{state:"cancelled",action:"physical-session-changed"});return {action:"physical-session-changed"};}
  const window=Math.max(8192,Number(current.contextTokens??row.context_window??32768));
  const agentId=/^agent:([^:]+):/u.exec(row.session_key)?.[1];
  const timeoutMs=Math.max(30000,Math.min(config.contextCompactionTimeoutMs??600000,1800000));
  const hardTarget=Math.floor(window*0.86);
  let semantic:any,semanticError:string|undefined;
  try{semantic=await request("sessions.compact",{key:row.session_key,...(agentId?{agentId}:{})},{timeoutMs});}
  catch(error){semanticError=error instanceof Error?error.message:String(error);}
  if(!currentAuthority(databasePath,row)){finish(databasePath,row,{state:"cancelled",action:"authority-revoked-after-compact"});return {action:"authority-revoked-after-compact"};}
  const before=Number(semantic?.result?.tokensBefore??current.totalTokens??row.projected_tokens??0)||undefined;
  const after=Number(semantic?.result?.tokensAfter??0)||undefined;
  if(semantic?.ok===true&&semantic?.compacted===true&&(!after||after<=hardTarget)){
    finish(databasePath,row,{state:"done",action:"semantic-compact",before,after});return {action:"semantic-compact",before,after};
  }
  if(!row.hard_required&&!after){
    const error=semanticError??"semantic compaction did not provide a safe result";
    finish(databasePath,row,{state:"degraded",action:"semantic-deferred",before,after,error,retryMs:15000});return {action:"semantic-deferred",before,after,error};
  }
  const afterSemantic=await describe(api,row.session_key);
  if(!currentAuthority(databasePath,row)){finish(databasePath,row,{state:"cancelled",action:"authority-revoked-before-hard-trim"});return {action:"authority-revoked-before-hard-trim"};}
  if(!afterSemantic){finish(databasePath,row,{state:"cancelled",action:"owner-missing-before-hard-trim"});return {action:"owner-missing-before-hard-trim"};}
  const semanticSucceeded=semantic?.ok===true&&semantic?.compacted===true;
  if(row.session_id&&afterSemantic.sessionId&&row.session_id!==afterSemantic.sessionId&&!semanticSucceeded){
    finish(databasePath,row,{state:"cancelled",action:"physical-session-changed-before-hard-trim"});return {action:"physical-session-changed-before-hard-trim"};
  }
  let expectedSessionId=afterSemantic.sessionId??row.session_id;
  const capsule=await snapshotCapsule(api,workspaceDir,databasePath,row,afterSemantic,semanticError??"hard context pressure");
  const first=Math.max(20,Math.min(1000,Math.floor(config.contextHardTrimMaxLines??200)));
  const candidates=[first,Math.min(first,120),60].filter((value,index,array)=>array.indexOf(value)===index);
  let lastError=semanticError;
  for(const maxLines of candidates){
    if(!currentAuthority(databasePath,row)){finish(databasePath,row,{state:"cancelled",action:"authority-revoked-during-hard-trim",capsule});return {action:"authority-revoked-during-hard-trim",capsule};}
    const beforeHard=await describe(api,row.session_key);
    if(!beforeHard||expectedSessionId&&beforeHard.sessionId&&beforeHard.sessionId!==expectedSessionId){
      finish(databasePath,row,{state:"cancelled",action:"physical-session-changed-during-hard-trim",capsule});return {action:"physical-session-changed-during-hard-trim",capsule};
    }
    try{
      const result=await request("sessions.compact",{key:row.session_key,...(agentId?{agentId}:{}),maxLines},{timeoutMs:120000});
      if(result?.ok!==true||result?.compacted!==true){lastError=`hard trim ${maxLines} did not confirm compaction`;continue;}
      if(!currentAuthority(databasePath,row)){finish(databasePath,row,{state:"cancelled",action:"authority-revoked-after-hard-trim",capsule});return {action:"authority-revoked-after-hard-trim",capsule};}
      const post=await describe(api,row.session_key);expectedSessionId=post?.sessionId??expectedSessionId;
      const tokens=Number(post?.totalTokens??0)||undefined;
      if(!tokens||tokens<=Math.floor(window*0.88)||maxLines===candidates.at(-1)){
        finish(databasePath,row,{state:"done",action:`hard-trim-${maxLines}`,before,after:tokens,capsule});return {action:`hard-trim-${maxLines}`,before,after:tokens,capsule};
      }
      lastError=`hard trim ${maxLines} still reports ${tokens}/${window}`;
    }catch(error){lastError=error instanceof Error?error.message:String(error);}
  }
  throw new Error(`context maintenance exhausted semantic and hard-trim paths; capsule=${capsule}; ${lastError??"unknown"}`);
}

function nextDueDelay(databasePath:string,maxAttempts:number):number|undefined {
  const db=openDb(databasePath);
  try {
    const row=db.prepare(`SELECT next_attempt_at FROM cnx_context_maintenance
      WHERE state IN ('pending','degraded') AND attempt_count<? AND next_attempt_at IS NOT NULL
      ORDER BY next_attempt_at LIMIT 1`).get(maxAttempts) as {next_attempt_at?:string}|undefined;
    if(!row?.next_attempt_at)return undefined;
    const at=Date.parse(row.next_attempt_at);
    return Number.isFinite(at)?Math.max(0,at-Date.now()):undefined;
  } finally {db.close();}
}

export function installContextGuard(api:any,registrationApi:any,config:ContextGuardConfig) {
  if(config.contextSafetyEnabled===false)return;
  const paths=(ctx:any)=>{const workspaceDir=resolve(config.workspaceDir??ctx?.workspaceDir??ctx?.config?.agents?.defaults?.workspace??process.cwd());
    return {workspaceDir,databasePath:resolve(config.ticketDatabasePath??resolve(workspaceDir,".cogent","runtime","cogentnexus.sqlite3"))};};

  let pulse:(()=>void)|undefined;
  registrationApi.on?.("before_agent_run",async(event:any,ctx:any)=>{
    if(!ctx.sessionKey||ctx.sessionKey.includes(":subagent:")||!ctx.runId)return {outcome:"pass"};
    const {databasePath}=paths(ctx),db=openDb(databasePath);let ticket:any;
    try{ticket=currentDirectTicket(db,ctx.sessionKey,ctx.runId);}finally{db.close();}
    if(!ticket)return {outcome:"pass"};
    let session:SessionDescription|null=null;
    try{session=await describe(api,ctx.sessionKey);}catch(error){api.logger.warn?.(`CogentNexus context describe failed: ${error instanceof Error?error.message:String(error)}`);}
    const pressure=contextPressure({messages:event.messages,prompt:event.prompt,systemPrompt:event.systemPrompt,session,config});
    if(pressure.level==="normal")return {outcome:"pass"};
    const queued=authorize(databasePath,{sessionKey:ctx.sessionKey,runId:ctx.runId,session,pressure});
    if(!queued)return {outcome:"pass"};
    api.logger.info?.(`CogentNexus context barrier ${ctx.sessionKey}: ${pressure.level} ${pressure.projectedTokens}/${pressure.contextWindow} ticket=${queued.ticketId}`);
    queueMicrotask(()=>pulse?.());
    return {outcome:"block",reason:"CogentNexus committed this request and deferred owner inference before context overflow",
      category:"cogentnexus_context_pressure",metadata:{ticketId:queued.ticketId,ownerGeneration:queued.generation,pressure}};
  },{priority:1500,timeoutMs:10000});

  let initial:ReturnType<typeof setTimeout>|undefined,retry:ReturnType<typeof setTimeout>|undefined,active=false,rerun=false,stopped=false;
  registrationApi.registerService?.({id:"cogentnexus-context-maintenance-v091",start:async(ctx:any)=>{
    const {workspaceDir,databasePath}=paths(ctx),maxAttempts=Math.max(1,Math.min(config.contextMaintenanceMaxAttempts??3,10));
    const scheduleRetry=()=>{
      if(stopped)return;
      if(retry)clearTimeout(retry);
      const delay=nextDueDelay(databasePath,maxAttempts);
      if(delay===undefined){retry=undefined;return;}
      retry=setTimeout(()=>{retry=undefined;pulse?.();},Math.max(25,delay));retry.unref?.();
    };
    const run=async()=>{
      if(stopped)return;
      if(active){rerun=true;return;}
      active=true;
      try {
        do {
          rerun=false;
          for(const row of due(databasePath,maxAttempts)){
            if(!claim(databasePath,row))continue;
            const attempt=row.attempt_count+1;
            try{
              const result=await maintain(api,row,config,workspaceDir,databasePath);
              api.logger.info?.(`CogentNexus context maintenance ${row.session_key}: ${result.action}`);
            } catch(error) {
              const message=error instanceof Error?error.message:String(error),exhausted=attempt>=maxAttempts;
              finish(databasePath,row,{state:exhausted?"cancelled":"degraded",action:exhausted?"retry-limit":"maintenance-error",error:message,retryMs:exhausted?undefined:Math.min(120000,15000*attempt)});
              api.logger.warn?.(`CogentNexus context maintenance failed for ${row.session_key} attempt ${attempt}/${maxAttempts}: ${message}`);
            }
          }
        } while(rerun&&!stopped);
      } finally {
        active=false;
        scheduleRetry();
      }
    };
    pulse=()=>{void run();};
    // Startup is a one-shot recovery event, not a polling loop. It gives v0.9
    // owner/native startup fences one second to settle before resuming a row that
    // was already human-authorized before the previous process stopped.
    initial=setTimeout(()=>pulse?.(),1000);initial.unref?.();
  },stop:async()=>{
    stopped=true;pulse=undefined;
    if(initial)clearTimeout(initial);if(retry)clearTimeout(retry);
    initial=undefined;retry=undefined;
  }});
}
