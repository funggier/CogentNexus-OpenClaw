import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { externalizeOversizedSyntheticPayload, type SyntheticPayloadConfig } from "./v090-synthetic-payload.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type RuntimeSafetyConfig = SyntheticPayloadConfig & {
  workspaceDir?:string;
  ticketDatabasePath?:string;
  contextRecoveryHoldPollMs?:number;
  contextRecoveryHoldMaxMs?:number;
};

function positive(value:unknown):number|undefined {
  const number=Number(value);
  return Number.isFinite(number)&&number>0?number:undefined;
}

export async function verifyCnxCompactionResult(input:{
  originalGateway:any;
  params:any;
  result:any;
}):Promise<any> {
  const {originalGateway,params,result}=input;
  if(result?.ok!==true||result?.compacted!==true||typeof params?.key!=="string")return result;

  const rawAfter=positive(result?.result?.tokensAfter);
  let session:any=null;
  try {
    const description=await originalGateway.request("sessions.describe",{key:params.key},{timeoutMs:5000});
    session=description?.session??null;
  } catch {}
  const freshAfter=session?.totalTokensFresh===true?positive(session?.totalTokens):undefined;
  const window=positive(session?.contextTokens);
  const observedAfter=rawAfter&&freshAfter?Math.max(rawAfter,freshAfter):(freshAfter??rawAfter);
  const isHardTrim=params?.maxLines!==undefined;

  if(!isHardTrim) {
    const safeAfter=observedAfter??Number.MAX_SAFE_INTEGER;
    return {
      ...result,
      result:{...(result.result??{}),tokensAfter:safeAfter},
      cnxVerification:{verified:observedAfter!==undefined,observedAfter,contextWindow:window,source:freshAfter!==undefined?"fresh-session-counter":rawAfter!==undefined?"compaction-result":"unavailable"},
    };
  }

  if(freshAfter===undefined||window===undefined) {
    return {
      ...result,
      ok:false,
      compacted:false,
      error:"CogentNexus could not verify fresh post-hard-trim context occupancy",
      cnxVerification:{verified:false,observedAfter:freshAfter,contextWindow:window,source:"unavailable"},
    };
  }
  const limit=Math.floor(window*0.88);
  if(freshAfter>limit) {
    return {
      ...result,
      ok:false,
      compacted:false,
      error:`CogentNexus hard-trim verification remained above safe context target (${freshAfter}/${window})`,
      cnxVerification:{verified:true,observedAfter:freshAfter,contextWindow:window,limit,source:"fresh-session-counter"},
    };
  }
  return {
    ...result,
    cnxVerification:{verified:true,observedAfter:freshAfter,contextWindow:window,limit,source:"fresh-session-counter"},
  };
}

function directRecoveryTicketId(sessionKey:string) {
  const match=/(CNXT-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/iu.exec(sessionKey);
  return match?.[1];
}

function generationFromHiddenSession(sessionKey:string) {
  const match=/-g(\d+)-[0-9a-f]{8}$/iu.exec(sessionKey);
  const value=match?Number(match[1]):NaN;
  return Number.isSafeInteger(value)&&value>=0?value:undefined;
}

type HoldSnapshot = {hold:boolean;revoked:boolean;state?:string;action?:string;ownerSessionKey?:string};

export function contextRecoveryHoldSnapshot(databasePath:string,hiddenSessionKey:string):HoldSnapshot {
  const ticketId=directRecoveryTicketId(hiddenSessionKey);
  const generation=generationFromHiddenSession(hiddenSessionKey);
  if(!ticketId||generation===undefined)return {hold:false,revoked:false};
  new TicketStore(databasePath).snapshot();
  const db=new DatabaseSync(databasePath,{readOnly:true});
  try {
    const contextTable=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_context_maintenance'").get();
    if(!contextTable)return {hold:false,revoked:false};
    const ticket=db.prepare("SELECT status,owner_session_key FROM tickets WHERE ticket_id=?").get(ticketId) as any;
    if(!ticket||ticket.status!=="accepted")return {hold:false,revoked:true,state:String(ticket?.status??"missing")};
    const sessionTable=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_sessions'").get();
    if(sessionTable) {
      const owner=db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(ticket.owner_session_key) as any;
      if(!owner||owner.state!=="active"||Number(owner.generation)!==generation)return {hold:false,revoked:true,state:String(owner?.state??"missing"),ownerSessionKey:ticket.owner_session_key};
    }
    const row=db.prepare("SELECT state,owner_generation,last_action FROM cnx_context_maintenance WHERE ticket_id=?").get(ticketId) as any;
    if(!row)return {hold:false,revoked:false,ownerSessionKey:ticket.owner_session_key};
    if(Number(row.owner_generation)!==generation)return {hold:false,revoked:true,state:String(row.state),action:String(row.last_action??""),ownerSessionKey:ticket.owner_session_key};
    const state=String(row.state),action=String(row.last_action??"");
    if(["pending","running","degraded"].includes(state))return {hold:true,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
    if(state==="done")return {hold:false,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
    // Retry exhaustion means session cleanup could not be completed safely, but
    // the committed Ticket may still progress through its bounded hidden worker.
    if(state==="cancelled"&&action==="retry-limit")return {hold:false,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
    // Every other cancelled maintenance state represents a lifecycle/ownership
    // revocation or a physical-session race and must not release stale work.
    if(state==="cancelled")return {hold:false,revoked:true,state,action,ownerSessionKey:ticket.owner_session_key};
    return {hold:false,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
  } finally {db.close();}
}

async function waitForContextRelease(input:{databasePath:string;hiddenSessionKey:string;config:RuntimeSafetyConfig;logger:any}) {
  const ticketId=directRecoveryTicketId(input.hiddenSessionKey);
  if(!ticketId)return;
  const pollMs=Math.max(250,Math.min(Math.floor(input.config.contextRecoveryHoldPollMs??750),5000));
  const maxMs=Math.max(30_000,Math.min(Math.floor(input.config.contextRecoveryHoldMaxMs??1_800_000),3_600_000));
  const deadline=Date.now()+maxMs;
  let announced=false;
  while(true) {
    const snapshot=contextRecoveryHoldSnapshot(input.databasePath,input.hiddenSessionKey);
    if(snapshot.revoked)throw new Error(`CogentNexus Direct Recovery authority revoked while waiting for context maintenance (${snapshot.state??"unknown"}/${snapshot.action??""})`);
    if(!snapshot.hold)return;
    if(!announced) {
      announced=true;
      input.logger.info?.(`CogentNexus holding hidden Direct Recovery ${ticketId} until context maintenance leaves state=${snapshot.state}`);
    }
    if(Date.now()>=deadline)throw new Error(`CogentNexus context recovery hold timed out for ${ticketId}`);
    await new Promise((resolvePromise)=>setTimeout(resolvePromise,pollMs));
  }
}

export function createCnxRuntimeSafetyProxy(api:any,config:RuntimeSafetyConfig={}) {
  const proxy=Object.create(api);
  const runtime=Object.create(api.runtime??{});
  const workspaceDir=resolve(config.workspaceDir??process.cwd());
  const databasePath=resolve(config.ticketDatabasePath??defaultTicketDatabase(workspaceDir));

  const originalGateway=api.runtime?.gateway;
  if(originalGateway?.request) {
    const gateway=Object.create(originalGateway);
    gateway.request=async(method:string,params?:any,options?:any)=>{
      const result=await originalGateway.request(method,params,options);
      if(method!=="sessions.compact")return result;
      return verifyCnxCompactionResult({originalGateway,params,result});
    };
    runtime.gateway=gateway;
  }

  const originalSubagent=api.runtime?.subagent;
  if(originalSubagent?.run) {
    const subagent=Object.create(originalSubagent);
    subagent.run=async(input:any)=>{
      const sessionKey=String(input?.sessionKey??"");
      const message=typeof input?.message==="string"?input.message:"";
      if(!sessionKey.includes(":subagent:cnx-")||!/\[CogentNexus Internal/iu.test(message))return originalSubagent.run(input);
      if(/\[CogentNexus Internal Direct Recovery\]/iu.test(message)) {
        await waitForContextRelease({databasePath,hiddenSessionKey:sessionKey,config,logger:api.logger});
      }
      const bounded=externalizeOversizedSyntheticPayload({workspaceDir,sessionKey,message,config});
      if(bounded.externalized)api.logger.info?.(`CogentNexus externalized oversized hidden payload for ${sessionKey}: chunks=${bounded.chunkCount} sha256=${bounded.sha256?.slice(0,16)}`);
      return originalSubagent.run({...input,message:bounded.message});
    };
    runtime.subagent=subagent;
  }

  proxy.runtime=runtime;
  return proxy;
}
