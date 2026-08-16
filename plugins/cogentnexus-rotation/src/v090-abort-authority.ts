import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

export const RECOVERABLE_ABORT_MESSAGE = "CogentNexus recoverable interruption: OpenClaw abort provenance was not human-authoritative";

type StopMarker = {
  messageSid?: string;
  timestamp?: number;
};

type RunStopBaseline = {
  sessionKey: string;
  marker: StopMarker;
};

function record(value:unknown):value is Record<string,unknown> {
  return Boolean(value&&typeof value==="object"&&!Array.isArray(value));
}

export function isAbortLikeMessage(message?:string|null) {
  if(!message)return false;
  const value=message.trim();
  return value==="agent run aborted"
    || /^This operation was aborted(?:\s*\|\s*\d+)?$/u.test(value)
    || /(?:reply operation )?aborted by user|user (?:cancelled|canceled)|(?:cancelled|canceled) by user|explicit user (?:stop|abort|cancel)/iu.test(value);
}

function findStructuredAbort(value:unknown,runId?:string,seen=new Set<object>()):boolean {
  if(!value||typeof value!=="object")return false;
  if(seen.has(value as object))return false;
  seen.add(value as object);
  if(Array.isArray(value))return value.some((item)=>findStructuredAbort(item,runId,seen));
  const item=value as Record<string,unknown>;
  const marker=item.openclawAbort;
  if(record(marker)&&marker.aborted===true&&(marker.origin==="rpc"||marker.origin==="stop-command")) {
    if(!runId||typeof marker.runId!=="string"||marker.runId===runId)return true;
  }
  return Object.values(item).some((child)=>findStructuredAbort(child,runId,seen));
}

export function hasStructuredHumanAbort(messages:unknown,runId?:string) {
  return findStructuredAbort(messages,runId);
}

function readJson(path:string) {
  try{return JSON.parse(readFileSync(path,"utf8"));}catch{return undefined;}
}

function roots(cfg:any,ctx:any) {
  const workspace=resolve(ctx?.workspaceDir??cfg?.workspaceDir??process.cwd());
  const root=resolve(cfg?.cogentRoot??resolve(workspace,".cogent"));
  return {workspace,root};
}

export function hostMaintenanceActive(cfg:any,ctx:any) {
  const {root}=roots(cfg,ctx),path=resolve(root,"runtime","maintenance.json");
  if(!existsSync(path))return false;
  const value=readJson(path);
  return value?.active===true;
}

function runIdOf(event:any,ctx:any):string|undefined {
  const value=event?.runId??ctx?.runId;
  return typeof value==="string"&&value.trim()?value.trim():undefined;
}

function sessionKeyOf(event:any,ctx:any):string|undefined {
  const value=event?.sessionKey??ctx?.sessionKey;
  return typeof value==="string"&&value.trim()?value.trim():undefined;
}

function agentIdFromSessionKey(sessionKey:string) {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1];
}

function stopMarkerFromEntry(entry:any):StopMarker {
  return {
    ...(typeof entry?.abortCutoffMessageSid==="string"&&entry.abortCutoffMessageSid
      ? {messageSid:entry.abortCutoffMessageSid}
      : {}),
    ...(typeof entry?.abortCutoffTimestamp==="number"&&Number.isFinite(entry.abortCutoffTimestamp)
      ? {timestamp:entry.abortCutoffTimestamp}
      : {}),
  };
}

function readStopMarker(api:any,sessionKey:string):StopMarker|undefined {
  const getEntry=api.runtime?.agent?.session?.getSessionEntry;
  if(typeof getEntry!=="function")return undefined;
  const agentId=agentIdFromSessionKey(sessionKey);
  try {
    const entry=getEntry({sessionKey,...(agentId?{agentId}:{})});
    return stopMarkerFromEntry(entry);
  } catch {
    return undefined;
  }
}

export function stopMarkerAdvanced(before:StopMarker|undefined,after:StopMarker|undefined):boolean {
  if(!before||!after)return false;
  if(typeof after.timestamp==="number") {
    const previous=typeof before.timestamp==="number"?before.timestamp:Number.NEGATIVE_INFINITY;
    if(after.timestamp>previous)return true;
  }
  if(after.messageSid&&after.messageSid!==before.messageSid)return true;
  return false;
}

export function isAuthoritativeAbortLifecycle(event:any):boolean {
  if(event?.stream!=="lifecycle")return false;
  const data=event?.data;
  return Boolean(data&&typeof data==="object"
    && data.phase==="end"
    && data.status==="cancelled"
    && data.aborted===true
    && (data.stopReason==="rpc"||data.stopReason==="stop-command"));
}

export type AbortAuthority = "not-abort"|"structured-human"|"lifecycle-human-stop"|"durable-human-stop"|"recoverable-maintenance"|"recoverable-ambiguous";

export function classifyAbortAuthority(event:any,ctx:any,cfg:any,humanAuthority:"none"|"lifecycle"|"durable"="none"):AbortAuthority {
  if(event?.success||!isAbortLikeMessage(event?.error))return "not-abort";
  const runId=event?.runId??ctx?.runId;
  if(hasStructuredHumanAbort(event?.messages,runId))return "structured-human";
  if(humanAuthority==="lifecycle")return "lifecycle-human-stop";
  if(humanAuthority==="durable")return "durable-human-stop";
  if(hostMaintenanceActive(cfg,ctx))return "recoverable-maintenance";
  // OpenClaw 2026.7.1-2 can lose non-human abort provenance (notably
  // diagnostic stuck_recovery) and emit the same legacy strings as UI Stop.
  // Error text is therefore interruption evidence only, never cancellation
  // authority. Human Stop is proven by the chat.abort/stop-command lifecycle
  // stopReason, transcript abort metadata, or a durable /stop cutoff advanced
  // during this exact run.
  return "recoverable-ambiguous";
}

/**
 * Preserve exact human-stop authority across the OpenClaw 2026.7.1-2 plugin
 * seam. The Gateway's chat.abort path emits a sanitized lifecycle event with
 * stopReason=rpc even when no assistant token has been produced yet, while the
 * later agent_end hook omits stopReason. Capture that run-scoped provenance and
 * consume it exactly once when the matching agent_end arrives.
 */
export function createAbortAuthorityApi(api:any,cfg:any={}) {
  const proxy=Object.create(api),originalOn=api.on?.bind(api);
  if(typeof originalOn!=="function")return proxy;
  const baselines=new Map<string,RunStopBaseline>();
  const humanLifecycleRuns=new Set<string>();

  const registerEvents=api.agent?.events?.registerAgentEventSubscription?.bind(api.agent.events)
    ?? api.registerAgentEventSubscription?.bind(api);
  if(typeof registerEvents==="function") {
    registerEvents({
      id:"cogentnexus-v090-abort-authority",
      description:"Preserve authoritative UI Stop provenance across agent_end",
      streams:["lifecycle"],
      handle:(event:any)=>{
        const runId=runIdOf(event,undefined);
        if(runId&&isAuthoritativeAbortLifecycle(event))humanLifecycleRuns.add(runId);
      },
    });
  }

  proxy.on=(name:string,handler:any,options?:any)=>{
    if(name==="before_agent_run") {
      return originalOn(name,(event:any,ctx:any)=>{
        const runId=runIdOf(event,ctx),sessionKey=sessionKeyOf(event,ctx);
        if(runId&&sessionKey&&!baselines.has(runId)) {
          baselines.set(runId,{sessionKey,marker:readStopMarker(api,sessionKey)??{}});
        }
        return handler(event,ctx);
      },options);
    }
    if(name!=="agent_end")return originalOn(name,handler,options);
    return originalOn(name,(event:any,ctx:any)=>{
      const runId=runIdOf(event,ctx);
      const baseline=runId?baselines.get(runId):undefined;
      const sessionKey=sessionKeyOf(event,ctx)??baseline?.sessionKey;
      const current=sessionKey?readStopMarker(api,sessionKey):undefined;
      const durableHumanStop=Boolean(baseline&&stopMarkerAdvanced(baseline.marker,current));
      const lifecycleHumanStop=Boolean(runId&&humanLifecycleRuns.has(runId));
      const authority=classifyAbortAuthority(event,ctx,cfg,lifecycleHumanStop?"lifecycle":durableHumanStop?"durable":"none");
      const forwarded=(authority==="recoverable-maintenance"||authority==="recoverable-ambiguous")
        ? {...event,error:RECOVERABLE_ABORT_MESSAGE}
        : event;
      if(forwarded!==event)api.logger?.info?.(`CogentNexus abort authority: ${authority}; preserving run as recoverable interruption`);
      const cleanup=()=>{if(runId){baselines.delete(runId);humanLifecycleRuns.delete(runId);}};
      try {
        const result=handler(forwarded,ctx);
        if(result&&typeof result.then==="function")return result.finally(cleanup);
        cleanup();
        return result;
      } catch(error) {
        cleanup();
        throw error;
      }
    },options);
  };
  return proxy;
}
