import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

type ContextSafetyConfig = {
  contextSafetyEnabled?: boolean;
  contextSoftRatio?: number;
  contextHardRatio?: number;
  contextMinimumHeadroomTokens?: number;
  contextMaintenancePollMs?: number;
  contextMaintenanceMaxAttempts?: number;
  contextCompactionTimeoutMs?: number;
  contextHardTrimMaxLines?: number;
};

type SessionAuthority = { state:string; generation:number };
type SessionDescription = {
  key?: string;
  sessionId?: string;
  totalTokens?: number;
  totalTokensFresh?: boolean;
  contextTokens?: number;
  compactionCheckpointCount?: number;
};

type Pressure = {
  usedTokens:number;
  contextWindow:number;
  projectedTokens:number;
  softLimit:number;
  hardLimit:number;
  ratio:number;
  level:"normal"|"soft"|"hard";
  source:"fresh-session-counter"|"estimated-loaded-context";
};

type ContextMaintenanceRow = {
  session_key:string;
  owner_generation:number;
  ticket_id:string;
  state:string;
  hard_required:number;
  attempt_count:number;
  next_attempt_at:string|null;
  last_error:string|null;
  session_id:string|null;
  context_window:number|null;
  projected_tokens:number|null;
};

function nowIso() { return new Date().toISOString(); }

function ensureColumn(db:DatabaseSync, table:string, column:string, declaration:string) {
  const rows=db.prepare(`PRAGMA table_info(${table})`).all() as Array<{name:string}>;
  if(!rows.some((row)=>row.name===column)) db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${declaration}`);
}

function openDb(databasePath:string) {
  new TicketStore(databasePath).snapshot();
  const db=new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_context_maintenance(
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
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      completed_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_context_maintenance_due
      ON cnx_context_maintenance(state,next_attempt_at,updated_at);
  `);
  ensureColumn(db,"cnx_context_maintenance","owner_generation","INTEGER NOT NULL DEFAULT 0");
  return db;
}

function sessionAuthority(db:DatabaseSync, sessionKey:string):SessionAuthority|undefined {
  const table=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_sessions'").get();
  if(!table) return undefined;
  const row=db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(sessionKey) as any;
  return row ? {state:String(row.state),generation:Number(row.generation)} : undefined;
}

function currentDirectTicket(db:DatabaseSync, sessionKey:string, runId?:string) {
  if(runId) {
    const row=db.prepare(`SELECT ticket_id,run_id FROM tickets
      WHERE owner_session_key=? AND run_id=? AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL
      ORDER BY created_at DESC LIMIT 1`).get(sessionKey,runId) as any;
    if(row) return row as {ticket_id:string;run_id:string};
  }
  return db.prepare(`SELECT ticket_id,run_id FROM tickets
    WHERE owner_session_key=? AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL
    ORDER BY created_at DESC LIMIT 1`).get(sessionKey) as {ticket_id:string;run_id:string}|undefined;
}

function addEvent(db:DatabaseSync,ticketId:string,eventType:string,payload:unknown,stamp:string) {
  db.prepare("INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)")
    .run(ticketId,eventType,JSON.stringify(payload),stamp);
}

function estimateTokens(value:unknown) {
  let text="";
  try { text=typeof value==="string" ? value : JSON.stringify(value ?? ""); }
  catch { text=String(value ?? ""); }
  // Conservative for Thai/code/JSON. It is intentionally an over-estimate for
  // ordinary English because this guard must run before the provider rejects.
  return Math.max(0,Math.ceil(text.length/2.5));
}

function clampRatio(value:number|undefined,fallback:number) {
  return typeof value==="number" && Number.isFinite(value) ? Math.min(0.97,Math.max(0.35,value)) : fallback;
}

function defaultSoftRatio(window:number) {
  if(window<=32768) return 0.68;
  if(window<=65536) return 0.74;
  if(window<=131072) return 0.80;
  return 0.84;
}

export function evaluateContextPressure(input:{
  messages?:unknown[];
  prompt?:string;
  systemPrompt?:string;
  session?:SessionDescription|null;
  config?:ContextSafetyConfig;
}):Pressure {
  const session=input.session ?? {};
  const window=Math.max(8192,Math.floor(Number(session.contextTokens)||32768));
  const estimated=Math.max(0,
    estimateTokens(input.messages ?? []) +
    estimateTokens(input.systemPrompt ?? "") +
    estimateTokens(input.prompt ?? ""));
  const fresh=Boolean(session.totalTokensFresh) && Number.isFinite(Number(session.totalTokens)) && Number(session.totalTokens)>0;
  // Previous-run totalTokens already contains the recurring system/context
  // envelope; add only the new prompt estimate to avoid double-counting it.
  const fromCounter=fresh ? Number(session.totalTokens)+estimateTokens(input.prompt ?? "") : 0;
  const projected=Math.max(estimated,fromCounter);
  const softRatio=clampRatio(input.config?.contextSoftRatio,defaultSoftRatio(window));
  const hardRatio=Math.max(softRatio+0.05,clampRatio(input.config?.contextHardRatio,0.90));
  const requestedHeadroom=input.config?.contextMinimumHeadroomTokens;
  const headroom=typeof requestedHeadroom==="number" && Number.isFinite(requestedHeadroom)
    ? Math.max(2048,Math.min(Math.floor(requestedHeadroom),Math.floor(window*0.45)))
    : Math.max(4096,Math.min(16384,Math.floor(window*0.18)));
  const softLimit=Math.max(4096,Math.min(Math.floor(window*softRatio),window-headroom));
  const hardLimit=Math.max(softLimit+1024,Math.min(Math.floor(window*hardRatio),window-2048));
  const level:Pressure["level"]=projected>=hardLimit?"hard":projected>=softLimit?"soft":"normal";
  return {
    usedTokens:fresh?Number(session.totalTokens):estimated,
    contextWindow:window,
    projectedTokens:projected,
    softLimit,
    hardLimit,
    ratio:projected/window,
    level,
    source:fresh?"fresh-session-counter":"estimated-loaded-context",
  };
}

async function describeSession(api:any,sessionKey:string):Promise<SessionDescription|null> {
  const request=api.runtime?.gateway?.request;
  if(typeof request!=="function") return null;
  const response=await request("sessions.describe",{key:sessionKey},{timeoutMs:5000});
  return response?.session ?? null;
}

function queueDirectRecoveryForContext(databasePath:string,input:{
  sessionKey:string;
  runId?:string;
  reason:string;
  hardRequired:boolean;
  session?:SessionDescription|null;
  pressure:Pressure;
}) {
  const db=openDb(databasePath),stamp=nowIso();
  try {
    db.exec("BEGIN IMMEDIATE");
    const authority=sessionAuthority(db,input.sessionKey);
    const ticket=currentDirectTicket(db,input.sessionKey,input.runId);
    if(!authority || authority.state!=="active" || !ticket) { db.exec("COMMIT"); return undefined; }
    const recoveryTable=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_recovery'").get();
    if(!recoveryTable) {
      db.exec(`CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
        ticket_id TEXT PRIMARY KEY REFERENCES tickets(ticket_id) ON DELETE CASCADE,
        mode TEXT NOT NULL DEFAULT 'resume', state TEXT NOT NULL DEFAULT 'pending', attempt_count INTEGER NOT NULL DEFAULT 0,
        active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,owner_generation INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,updated_at TEXT NOT NULL)`);
    }
    db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at
    ) VALUES (?,'resume','pending',0,NULL,?,?,?, ?,?)
    ON CONFLICT(ticket_id) DO UPDATE SET mode='resume',state='pending',active_run_id=NULL,
      next_attempt_at=excluded.next_attempt_at,last_error=excluded.last_error,
      owner_generation=excluded.owner_generation,updated_at=excluded.updated_at`)
      .run(ticket.ticket_id,stamp,input.reason.slice(0,2000),authority.generation,stamp,stamp);
    db.prepare(`UPDATE tickets SET failure_class='interrupted',failure_message=?,delivery_last_error=?,
      response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=?
      WHERE ticket_id=? AND status='accepted'`).run(input.reason.slice(0,2000),input.reason.slice(0,2000),stamp,ticket.ticket_id);
    db.prepare(`INSERT INTO cnx_context_maintenance(
      session_key,owner_generation,ticket_id,state,hard_required,attempt_count,next_attempt_at,last_error,
      session_id,context_window,projected_tokens,created_at,updated_at
    ) VALUES (?,?,?,'pending',?,0,?,NULL,?,?,?,?,?)
    ON CONFLICT(session_key) DO UPDATE SET owner_generation=excluded.owner_generation,ticket_id=excluded.ticket_id,
      state='pending',hard_required=MAX(cnx_context_maintenance.hard_required,excluded.hard_required),
      next_attempt_at=excluded.next_attempt_at,last_error=NULL,session_id=excluded.session_id,
      context_window=excluded.context_window,projected_tokens=excluded.projected_tokens,updated_at=excluded.updated_at`)
      .run(input.sessionKey,authority.generation,ticket.ticket_id,input.hardRequired?1:0,stamp,
        input.session?.sessionId ?? null,input.pressure.contextWindow,input.pressure.projectedTokens,stamp,stamp);
    addEvent(db,ticket.ticket_id,"context_pressure_deferred",{
      ownerSessionKey:input.sessionKey,ownerGeneration:authority.generation,hardRequired:input.hardRequired,
      sessionId:input.session?.sessionId,pressure:input.pressure,reason:input.reason,
    },stamp);
    db.exec("COMMIT");
    return {ticketId:ticket.ticket_id,generation:authority.generation};
  } catch(error) {
    try { db.exec("ROLLBACK"); } catch {}
    throw error;
  } finally { db.close(); }
}

function maintenanceDue(databasePath:string,limit=4):ContextMaintenanceRow[] {
  const db=openDb(databasePath),stamp=nowIso();
  try {
    // Generation/state mismatch is a hard cancellation boundary.
    db.prepare(`UPDATE cnx_context_maintenance SET state='cancelled',last_error='session authority superseded',updated_at=?,completed_at=?
      WHERE state IN ('pending','running','degraded') AND NOT EXISTS (
        SELECT 1 FROM cnx_sessions s WHERE s.session_key=cnx_context_maintenance.session_key
          AND s.state='active' AND s.generation=cnx_context_maintenance.owner_generation)`)
      .run(stamp,stamp);
    return db.prepare(`SELECT session_key,owner_generation,ticket_id,state,hard_required,attempt_count,next_attempt_at,last_error,
      session_id,context_window,projected_tokens FROM cnx_context_maintenance
      WHERE state IN ('pending','degraded') AND (next_attempt_at IS NULL OR next_attempt_at<=?)
      ORDER BY hard_required DESC,updated_at,session_key LIMIT ?`).all(stamp,Math.max(1,Math.min(limit,16))) as ContextMaintenanceRow[];
  } finally { db.close(); }
}

function claimMaintenance(databasePath:string,row:ContextMaintenanceRow) {
  const db=openDb(databasePath),stamp=nowIso();
  try {
    return Number(db.prepare(`UPDATE cnx_context_maintenance SET state='running',attempt_count=attempt_count+1,
      next_attempt_at=NULL,last_error=NULL,updated_at=? WHERE session_key=? AND owner_generation=? AND state IN ('pending','degraded')
      AND EXISTS (SELECT 1 FROM cnx_sessions s WHERE s.session_key=? AND s.state='active' AND s.generation=?)`)
      .run(stamp,row.session_key,row.owner_generation,row.session_key,row.owner_generation).changes)===1;
  } finally { db.close(); }
}

function recordMaintenance(databasePath:string,row:ContextMaintenanceRow,input:{
  state:"done"|"degraded"|"cancelled";
  action:string;
  tokensBefore?:number;
  tokensAfter?:number;
  error?:string;
  retryMs?:number;
}) {
  const db=openDb(databasePath),stamp=nowIso();
  try {
    const next=input.retryMs ? new Date(Date.now()+input.retryMs).toISOString() : null;
    db.prepare(`UPDATE cnx_context_maintenance SET state=?,last_action=?,last_tokens_before=?,last_tokens_after=?,
      last_error=?,next_attempt_at=?,updated_at=?,completed_at=? WHERE session_key=? AND owner_generation=?`)
      .run(input.state,input.action,input.tokensBefore ?? null,input.tokensAfter ?? null,input.error?.slice(0,2000) ?? null,
        next,stamp,input.state==="done"||input.state==="cancelled"?stamp:null,row.session_key,row.owner_generation);
  } finally { db.close(); }
}

function contextCapsule(workspaceDir:string,databasePath:string,row:ContextMaintenanceRow,session:SessionDescription|null,reason:string) {
  const db=openDb(databasePath);
  let tickets:any[]=[];
  try {
    tickets=db.prepare(`SELECT ticket_id,status,run_id,workflow_id,failure_class,failure_message,created_at,updated_at
      FROM tickets WHERE owner_session_key=? ORDER BY created_at DESC LIMIT 32`).all(row.session_key) as any[];
  } finally { db.close(); }
  const hash=createHash("sha256").update(row.session_key).digest("hex").slice(0,16);
  const dir=resolve(workspaceDir,".cogent","context",hash);
  mkdirSync(dir,{recursive:true});
  const stamp=nowIso().replace(/[:.]/g,"-");
  const path=resolve(dir,`g${row.owner_generation}-${stamp}.json`);
  writeFileSync(path,`${JSON.stringify({
    schemaVersion:1,createdAt:nowIso(),reason,ownerSessionKey:row.session_key,ownerGeneration:row.owner_generation,
    ticketId:row.ticket_id,sessionId:session?.sessionId ?? row.session_id,contextWindow:session?.contextTokens ?? row.context_window,
    projectedTokens:row.projected_tokens,totalTokens:session?.totalTokens,totalTokensFresh:session?.totalTokensFresh,
    compactionCheckpointCount:session?.compactionCheckpointCount,tickets,
    note:"Full OpenClaw transcript remains authoritative/archived; this capsule preserves CogentNexus ownership and recovery provenance before hard trimming.",
  },null,2)}\n`);
  return path;
}

async function compact(api:any,row:ContextMaintenanceRow,config:ContextSafetyConfig,workspaceDir:string,databasePath:string) {
  const request=api.runtime?.gateway?.request;
  if(typeof request!=="function") throw new Error("OpenClaw runtime.gateway.request is unavailable");
  const before=await describeSession(api,row.session_key);
  const window=Math.max(8192,Number(before?.contextTokens ?? row.context_window ?? 32768));
  const hardRatio=clampRatio(config.contextHardRatio,0.90);
  const hardTarget=Math.floor(window*Math.min(0.86,hardRatio-0.03));
  const agentId=/^agent:([^:]+):/u.exec(row.session_key)?.[1];
  const timeoutMs=Math.max(30_000,Math.min(config.contextCompactionTimeoutMs ?? 600_000,1_800_000));
  let semantic:any;
  let semanticError:string|undefined;
  try {
    semantic=await request("sessions.compact",{key:row.session_key,...(agentId?{agentId}:{})},{timeoutMs});
  } catch(error) {
    semanticError=error instanceof Error?error.message:String(error);
  }
  const tokensBefore=Number(semantic?.result?.tokensBefore ?? before?.totalTokens ?? row.projected_tokens ?? 0) || undefined;
  const tokensAfter=Number(semantic?.result?.tokensAfter ?? 0) || undefined;
  if(semantic?.ok===true && semantic?.compacted===true && (!tokensAfter || tokensAfter<=hardTarget)) {
    recordMaintenance(databasePath,row,{state:"done",action:"semantic-compact",tokensBefore,tokensAfter});
    return {action:"semantic-compact",tokensBefore,tokensAfter};
  }

  const mustHardTrim=Boolean(row.hard_required) || Boolean(tokensAfter && tokensAfter>hardTarget);
  if(!mustHardTrim) {
    const error=semanticError ?? `semantic compaction remained above target (${tokensAfter ?? "unknown"}/${hardTarget})`;
    recordMaintenance(databasePath,row,{state:"degraded",action:"semantic-deferred",tokensBefore,tokensAfter,error,retryMs:30_000});
    return {action:"semantic-deferred",tokensBefore,tokensAfter,error};
  }

  const capsule=contextCapsule(workspaceDir,databasePath,row,before,semanticError ?? "hard context pressure");
  const configured=Math.floor(config.contextHardTrimMaxLines ?? 200);
  const candidates=[configured,Math.min(configured,120),60].filter((value,index,array)=>value>=20 && array.indexOf(value)===index);
  let lastError=semanticError;
  for(const maxLines of candidates) {
    try {
      const result=await request("sessions.compact",{key:row.session_key,...(agentId?{agentId}:{}),maxLines},{timeoutMs:120_000});
      if(result?.ok!==true || result?.compacted!==true) {
        lastError=`hard trim ${maxLines} lines did not confirm compaction`;
        continue;
      }
      const after=await describeSession(api,row.session_key).catch(()=>null);
      const afterTokens=Number(after?.totalTokens ?? 0)||undefined;
      if(!afterTokens || afterTokens<=Math.floor(window*0.88) || maxLines===candidates.at(-1)) {
        recordMaintenance(databasePath,row,{state:"done",action:`hard-trim-${maxLines}`,tokensBefore,tokensAfter:afterTokens});
        return {action:`hard-trim-${maxLines}`,tokensBefore,tokensAfter:afterTokens,capsule};
      }
      lastError=`hard trim ${maxLines} lines still reports ${afterTokens}/${window} tokens`;
    } catch(error) { lastError=error instanceof Error?error.message:String(error); }
  }
  throw new Error(`context maintenance failed after semantic + hard trim; capsule=${capsule}; ${lastError ?? "unknown error"}`);
}

export function installContextSafety(api:any,registrationApi:any,config:ContextSafetyConfig & {workspaceDir?:string;ticketDatabasePath?:string}) {
  if(config.contextSafetyEnabled===false) return;
  const paths=(ctx:any)=>{
    const workspaceDir=resolve(config.workspaceDir ?? ctx?.workspaceDir ?? ctx?.config?.agents?.defaults?.workspace ?? process.cwd());
    const databasePath=resolve(config.ticketDatabasePath ?? resolve(workspaceDir,".cogent","runtime","cogentnexus.sqlite3"));
    return {workspaceDir,databasePath};
  };

  registrationApi.on?.("before_agent_run",async(event:any,ctx:any)=>{
    const sessionKey=ctx.sessionKey;
    if(!sessionKey || sessionKey.includes(":subagent:") || !ctx.runId) return {outcome:"pass"};
    const {databasePath}=paths(ctx);
    const db=openDb(databasePath);
    let ticket:ReturnType<typeof currentDirectTicket>;
    try { ticket=currentDirectTicket(db,sessionKey,ctx.runId); }
    finally { db.close(); }
    // The Ticket-first hook (priority 2000) has already committed/routed human
    // intent. No matching Direct Ticket means this is durable/internal/non-human
    // work and this guard must not change its ownership semantics.
    if(!ticket) return {outcome:"pass"};
    let session:SessionDescription|null=null;
    try { session=await describeSession(api,sessionKey); }
    catch(error) { api.logger.warn?.(`CogentNexus context describe failed for ${sessionKey}: ${error instanceof Error?error.message:String(error)}`); }
    const pressure=evaluateContextPressure({messages:event.messages,prompt:event.prompt,systemPrompt:event.systemPrompt,session,config});
    if(pressure.level==="normal") return {outcome:"pass"};
    const reason=`CogentNexus context safety deferred owner inference at ${Math.round(pressure.ratio*100)}% projected pressure (${pressure.projectedTokens}/${pressure.contextWindow})`;
    const queued=queueDirectRecoveryForContext(databasePath,{
      sessionKey,runId:ctx.runId,reason,hardRequired:pressure.level==="hard",session,pressure,
    });
    if(!queued) return {outcome:"pass"};
    api.logger.info?.(`CogentNexus context barrier ${sessionKey}: level=${pressure.level} projected=${pressure.projectedTokens}/${pressure.contextWindow} ticket=${queued.ticketId} generation=${queued.generation}`);
    return {
      outcome:"block",
      reason:"CogentNexus committed the request and moved it to bounded recovery before owner-session context overflow",
      category:"cogentnexus_context_pressure",
      metadata:{ticketId:queued.ticketId,ownerGeneration:queued.generation,pressure},
    };
  },{priority:1500,timeoutMs:10_000});

  let interval:ReturnType<typeof setInterval>|undefined;
  let active=false;
  registrationApi.registerService?.({
    id:"cogentnexus-context-maintenance-v090",
    start:async(ctx:any)=>{
      const {workspaceDir,databasePath}=paths(ctx);
      const tick=async()=>{
        if(active) return;
        active=true;
        try {
          for(const row of maintenanceDue(databasePath,4)) {
            if(!claimMaintenance(databasePath,row)) continue;
            try {
              const result=await compact(api,row,config,workspaceDir,databasePath);
              api.logger.info?.(`CogentNexus context maintenance ${row.session_key}: ${result.action} before=${result.tokensBefore ?? "?"} after=${result.tokensAfter ?? "?"}`);
            } catch(error) {
              const attempts=Number(row.attempt_count)+1;
              const maximum=Math.max(1,Math.min(config.contextMaintenanceMaxAttempts ?? 3,10));
              const message=error instanceof Error?error.message:String(error);
              recordMaintenance(databasePath,row,{
                state:attempts>=maximum?"degraded":"degraded",
                action:"maintenance-error",
                error:message,
                retryMs:attempts>=maximum?300_000:Math.min(300_000,15_000*Math.max(1,attempts)),
              });
              api.logger.warn?.(`CogentNexus context maintenance failed for ${row.session_key}: ${message}`);
            }
          }
        } finally { active=false; }
      };
      await tick();
      interval=setInterval(()=>{void tick();},Math.max(1000,Math.min(config.contextMaintenancePollMs ?? 3000,30_000)));
      interval.unref?.();
    },
    stop:async()=>{if(interval)clearInterval(interval);interval=undefined;},
  });
}
