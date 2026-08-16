import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

export const RECOVERABLE_ABORT_MESSAGE = "CogentNexus recoverable interruption: OpenClaw abort provenance was not human-authoritative";
const MANAGED_WATCHDOG_ABORT_MS = 24 * 60 * 60 * 1000;

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

export function managedWatchdogProtectionActive(cfg:any,ctx:any) {
  const {root}=roots(cfg,ctx),path=resolve(root,"host","openclaw-watchdog-compat.json");
  if(!existsSync(path))return false;
  const value=readJson(path);
  return value?.applied===true
    && Number(value?.managedValue)>=MANAGED_WATCHDOG_ABORT_MS;
}

export type AbortAuthority = "not-abort"|"structured-human"|"managed-human-compat"|"recoverable-maintenance"|"recoverable-ambiguous";

export function classifyAbortAuthority(event:any,ctx:any,cfg:any):AbortAuthority {
  if(event?.success||!isAbortLikeMessage(event?.error))return "not-abort";
  const runId=event?.runId??ctx?.runId;
  if(hasStructuredHumanAbort(event?.messages,runId))return "structured-human";
  if(hostMaintenanceActive(cfg,ctx))return "recoverable-maintenance";
  // OpenClaw 2026.7.1-2 loses the diagnostic stuck_recovery reason before
  // agent_end. CNX neutralizes that known ambiguous source to a 24h horizon in
  // managed mode. Only while that protection is durably recorded may the
  // remaining legacy abort text act as the UI-Stop compatibility fallback.
  if(managedWatchdogProtectionActive(cfg,ctx))return "managed-human-compat";
  return "recoverable-ambiguous";
}

export function createAbortAuthorityApi(api:any,cfg:any={}) {
  const proxy=Object.create(api),originalOn=api.on?.bind(api);
  if(typeof originalOn!=="function")return proxy;
  proxy.on=(name:string,handler:any,options?:any)=>{
    if(name!=="agent_end")return originalOn(name,handler,options);
    return originalOn(name,(event:any,ctx:any)=>{
      const authority=classifyAbortAuthority(event,ctx,cfg);
      if(authority==="recoverable-maintenance"||authority==="recoverable-ambiguous") {
        api.logger?.info?.(`CogentNexus abort authority: ${authority}; preserving run as recoverable interruption`);
        return handler({...event,error:RECOVERABLE_ABORT_MESSAGE},ctx);
      }
      return handler(event,ctx);
    },options);
  };
  return proxy;
}
