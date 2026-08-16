import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { directRecoveryIdentity, predecessorRecovery, touchDirectRecoveryClaim } from "./v090-recovery-order.js";
import { externalizeOversizedSyntheticPayload, type SyntheticPayloadConfig } from "./v090-synthetic-payload.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type RuntimeSafetyConfig = SyntheticPayloadConfig & {
  workspaceDir?:string;
  ticketDatabasePath?:string;
  contextRecoveryHoldPollMs?:number;
  contextRecoveryHoldMaxMs?:number;
  recoveryOrderPollMs?:number;
};

function positive(value:unknown):number|undefined {
  const number=Number(value);
  return Number.isFinite(number)&&number>0?number:undefined;
}

export async function verifyCnxCompactionResult(input:{originalGateway:any;params:any;result:any}):Promise<any> {
  const {originalGateway,params,result}=input;
  if(result?.ok!==true||result?.compacted!==true||typeof params?.key!=="string")return result;
  const rawAfter=positive(result?.result?.tokensAfter);
  let session:any=null;
  try { const description=await originalGateway.request("sessions.describe",{key:params.key},{timeoutMs:5000});session=description?.session??null; } catch {}
  const freshAfter=session?.totalTokensFresh===true?positive(session?.totalTokens):undefined;
  const window=positive(session?.contextTokens);
  const observedAfter=rawAfter&&freshAfter?Math.max(rawAfter,freshAfter):(freshAfter??rawAfter);
  const isHardTrim=params?.maxLines!==undefined;
  if(!isHardTrim) {
    const safeAfter=observedAfter??Number.MAX_SAFE_INTEGER;
    return {...result,result:{...(result.result??{}),tokensAfter:safeAfter},cnxVerification:{verified:observedAfter!==undefined,occupancyVerified:observedAfter!==undefined,
      observedAfter,contextWindow:window,source:freshAfter!==undefined?"fresh-session-counter":rawAfter!==undefined?"compaction-result":"unavailable"}};
  }
  const maxLines=Math.max(1,Math.floor(Number(params.maxLines)||0));
  const kept=positive(result?.kept??result?.result?.kept);
  const structuralVerified=kept!==undefined&&kept<=maxLines;
  if(freshAfter!==undefined&&window!==undefined) {
    const limit=Math.floor(window*0.88);
    if(freshAfter>limit)return {...result,ok:false,compacted:false,error:`CogentNexus hard-trim verification remained above safe context target (${freshAfter}/${window})`,
      cnxVerification:{verified:true,occupancyVerified:true,structuralVerified,observedAfter:freshAfter,contextWindow:window,limit,kept,maxLines,source:"fresh-session-counter"}};
    return {...result,cnxVerification:{verified:true,occupancyVerified:true,structuralVerified,observedAfter:freshAfter,contextWindow:window,limit,kept,maxLines,source:"fresh-session-counter"}};
  }
  if(structuralVerified)return {...result,cnxVerification:{verified:true,occupancyVerified:false,structuralVerified:true,observedAfter:undefined,contextWindow:window,kept,maxLines,source:"max-lines-result"}};
  return {...result,ok:false,compacted:false,error:"CogentNexus could not verify hard-trim occupancy or retained-line bound",
    cnxVerification:{verified:false,occupancyVerified:false,structuralVerified:false,observedAfter:freshAfter,contextWindow:window,kept,maxLines,source:"unavailable"}};
}

function directRecoveryTicketId(sessionKey:string) {
  const match=/(CNXT-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/iu.exec(sessionKey);
  return match?.[1];
}
function generationFromHiddenSession(sessionKey:string) {
  const match=/-g(\d+)-[0-9a-f]{8}$/iu.exec(sessionKey),value=match?Number(match[1]):NaN;
  return Number.isSafeInteger(value)&&value>=0?value:undefined;
}

type HoldSnapshot = {hold:boolean;revoked:boolean;state?:string;action?:string;ownerSessionKey?:string};
export function contextRecoveryHoldSnapshot(databasePath:string,hiddenSessionKey:string):HoldSnapshot {
  const ticketId=directRecoveryTicketId(hiddenSessionKey),generation=generationFromHiddenSession(hiddenSessionKey);
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
    if(state==="cancelled"&&action==="retry-limit")return {hold:false,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
    if(state==="cancelled")return {hold:false,revoked:true,state,action,ownerSessionKey:ticket.owner_session_key};
    return {hold:false,revoked:false,state,action,ownerSessionKey:ticket.owner_session_key};
  } finally {db.close();}
}

function requireClaim(databasePath:string,ticketId:string,generation:number,runId:string) {
  const identity=directRecoveryIdentity(databasePath,ticketId,generation,runId) as any;
  if(!identity.authorized)throw new Error(`CogentNexus Direct Recovery claim revoked (${identity.reason??"unknown"})`);
  return identity;
}

async function waitForContextRelease(input:{databasePath:string;hiddenSessionKey:string;expectedRunId:string;config:RuntimeSafetyConfig;logger:any}) {
  const ticketId=directRecoveryTicketId(input.hiddenSessionKey),generation=generationFromHiddenSession(input.hiddenSessionKey);
  if(!ticketId||generation===undefined)return;
  const pollMs=Math.max(250,Math.min(Math.floor(input.config.contextRecoveryHoldPollMs??750),5000));
  const maxMs=Math.max(30_000,Math.min(Math.floor(input.config.contextRecoveryHoldMaxMs??1_800_000),3_600_000));
  const deadline=Date.now()+maxMs;let announced=false,lastHeartbeat=0;
  while(true) {
    const identity=requireClaim(input.databasePath,ticketId,generation,input.expectedRunId);
    if(Date.now()-lastHeartbeat>=5000){if(!touchDirectRecoveryClaim(input.databasePath,{ticketId,ownerSessionKey:identity.ownerSessionKey,ownerGeneration:generation,runId:input.expectedRunId}))throw new Error("CogentNexus Direct Recovery claim superseded during context hold");lastHeartbeat=Date.now();}
    const snapshot=contextRecoveryHoldSnapshot(input.databasePath,input.hiddenSessionKey);
    if(snapshot.revoked)throw new Error(`CogentNexus Direct Recovery authority revoked while waiting for context maintenance (${snapshot.state??"unknown"}/${snapshot.action??""})`);
    if(!snapshot.hold)return;
    if(!announced){announced=true;input.logger.info?.(`CogentNexus holding hidden Direct Recovery ${ticketId} until context maintenance leaves state=${snapshot.state}`);}
    if(Date.now()>=deadline)throw new Error(`CogentNexus context recovery hold timed out for ${ticketId}`);
    await new Promise((resolvePromise)=>setTimeout(resolvePromise,pollMs));
  }
}

async function waitForRecoveryOrder(input:{databasePath:string;hiddenSessionKey:string;expectedRunId:string;config:RuntimeSafetyConfig;logger:any}) {
  const ticketId=directRecoveryTicketId(input.hiddenSessionKey),generation=generationFromHiddenSession(input.hiddenSessionKey);
  if(!ticketId||generation===undefined)return;
  const pollMs=Math.max(100,Math.min(Math.floor(input.config.recoveryOrderPollMs??500),5000));
  let announcedPredecessor:string|undefined,lastHeartbeat=0;
  while(true) {
    const identity=requireClaim(input.databasePath,ticketId,generation,input.expectedRunId);
    if(Date.now()-lastHeartbeat>=5000){if(!touchDirectRecoveryClaim(input.databasePath,{ticketId,ownerSessionKey:identity.ownerSessionKey,ownerGeneration:generation,runId:input.expectedRunId}))throw new Error("CogentNexus Direct Recovery claim superseded during ordered wait");lastHeartbeat=Date.now();}
    const predecessor=predecessorRecovery(input.databasePath,{ticketId,ownerSessionKey:identity.ownerSessionKey,ownerGeneration:generation}) as any;
    if(!predecessor)return;
    if(announcedPredecessor!==String(predecessor.ticket_id)){announcedPredecessor=String(predecessor.ticket_id);input.logger.info?.(`CogentNexus holding Direct Recovery ${ticketId} behind ${announcedPredecessor} (${String(predecessor.state)}) in ${identity.ownerSessionKey}`);}
    await new Promise((resolvePromise)=>setTimeout(resolvePromise,pollMs));
  }
}

export function createCnxRuntimeSafetyProxy(api:any,config:RuntimeSafetyConfig={}) {
  const proxy=Object.create(api),runtime=Object.create(api.runtime??{});
  const workspaceDir=resolve(config.workspaceDir??process.cwd()),databasePath=resolve(config.ticketDatabasePath??defaultTicketDatabase(workspaceDir));
  const originalGateway=api.runtime?.gateway;
  if(originalGateway?.request) {
    const gateway=Object.create(originalGateway);
    gateway.request=async(method:string,params?:any,options?:any)=>{const result=await originalGateway.request(method,params,options);return method==="sessions.compact"?verifyCnxCompactionResult({originalGateway,params,result}):result;};
    runtime.gateway=gateway;
  }
  const originalSubagent=api.runtime?.subagent;
  if(originalSubagent?.run) {
    const subagent=Object.create(originalSubagent);
    subagent.run=async(input:any)=>{
      const sessionKey=String(input?.sessionKey??""),message=typeof input?.message==="string"?input.message:"";
      if(!sessionKey.includes(":subagent:cnx-")||!/\[CogentNexus Internal/iu.test(message))return originalSubagent.run(input);
      if(/\[CogentNexus Internal Direct Recovery\]/iu.test(message)) {
        const ticketId=directRecoveryTicketId(sessionKey);
        if(ticketId) {
          const expectedRunId=typeof input?.idempotencyKey==="string"&&input.idempotencyKey?input.idempotencyKey:"";
          if(!expectedRunId)throw new Error(`CogentNexus Direct Recovery ${ticketId} is missing its claim fencing token`);
          await waitForRecoveryOrder({databasePath,hiddenSessionKey:sessionKey,expectedRunId,config,logger:api.logger});
          await waitForContextRelease({databasePath,hiddenSessionKey:sessionKey,expectedRunId,config,logger:api.logger});
          const generation=generationFromHiddenSession(sessionKey);
          if(generation===undefined)throw new Error(`CogentNexus Direct Recovery ${ticketId} has no generation fence`);
          requireClaim(databasePath,ticketId,generation,expectedRunId);
        }
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
