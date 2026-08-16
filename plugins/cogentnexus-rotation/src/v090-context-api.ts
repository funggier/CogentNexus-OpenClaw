import { resolve } from "node:path";

function agentIdFromSessionKey(sessionKey:string) {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1];
}

function projectSessionEntry(entry:any) {
  if (!entry) return null;
  const contextTokens = typeof entry.contextTokens === "number" ? entry.contextTokens : undefined;
  const totalTokensFresh = entry.totalTokensFresh === true;
  const totalTokens = totalTokensFresh && typeof entry.totalTokens === "number" ? entry.totalTokens : undefined;
  const compactionCheckpointCount = typeof entry.compactionCheckpointCount === "number"
    ? entry.compactionCheckpointCount
    : undefined;
  return {
    ...(contextTokens !== undefined ? { contextTokens } : {}),
    ...(totalTokens !== undefined ? { totalTokens } : {}),
    totalTokensFresh,
    ...(compactionCheckpointCount !== undefined ? { compactionCheckpointCount } : {}),
  };
}

function parseJsonOutput(stdout:string) {
  const value=stdout.trim();
  if(!value)return null;
  try{return JSON.parse(value);}catch{throw new Error(`CogentNexus Host context adapter returned invalid JSON: ${value.slice(0,500)}`);}
}

async function runHostCompact(api:any,cfg:any,params:any,options:any) {
  const run=api.runtime?.system?.runCommandWithTimeout;
  if(typeof run!=="function")throw new Error("OpenClaw supported command runtime is unavailable for context maintenance");
  const sessionKey=String(params?.key??"").trim();
  if(!sessionKey)throw new Error("sessions.compact requires an exact session key");
  const workspace=resolve(cfg?.workspaceDir ?? process.cwd());
  const root=resolve(cfg?.cogentRoot ?? resolve(workspace,".cogent"));
  const script=resolve(workspace,"skills","cogentnexus","scripts","host_context.py");
  const timeoutMs=Math.max(5_000,Math.min(Number(options?.timeoutMs??120_000)||120_000,600_000));
  const argv=[
    cfg?.pythonCommand ?? "python",
    script,
    "--root",root,
    "compact",
    "--session-key",sessionKey,
    "--timeout-ms",String(timeoutMs),
  ];
  if(Number.isInteger(params?.maxLines) && params.maxLines>0)argv.push("--max-lines",String(params.maxLines));
  const result=await run(argv,{timeoutMs:timeoutMs+20_000,killProcessTree:true,maxOutputBytes:1_000_000});
  if(result?.code!==0)throw new Error(String(result?.stderr||result?.stdout||`Host context adapter failed (${result?.code??"unknown"})`).trim());
  return parseJsonOutput(String(result?.stdout??""));
}

async function readSupportedHistory(api:any,params:any) {
  const getMessages=api.runtime?.subagent?.getSessionMessages;
  if(typeof getMessages!=="function")throw new Error("OpenClaw supported session-message accessor is unavailable");
  const sessionKey=String(params?.sessionKey??params?.key??"").trim();
  if(!sessionKey)throw new Error("chat.history requires an exact session key");
  const limit=Math.max(1,Math.min(Number(params?.limit??50)||50,200));
  const result=await getMessages({sessionKey,limit});
  let messages=Array.isArray(result?.messages)?result.messages:[];
  const maxChars=Math.max(1000,Math.min(Number(params?.maxChars??50000)||50000,200000));
  // Keep the newest bounded history without mutating the source messages.
  let used=0;
  const kept:any[]=[];
  for(let index=messages.length-1;index>=0;index--){
    const item=messages[index];
    let size=0;try{size=JSON.stringify(item).length;}catch{size=String(item??"").length;}
    if(kept.length>0&&used+size>maxChars)break;
    kept.push(item);used+=size;
    if(used>=maxChars)break;
  }
  messages=kept.reverse();
  return {messages};
}

/**
 * Context maintenance facade for CogentNexus v0.9.
 *
 * OpenClaw 2026.7.1-2 intentionally denies runtime.gateway.request to normal
 * third-party plugins. Read-only session telemetry/history therefore use the
 * public runtime.agent.session and runtime.subagent accessors. The one
 * privileged mutation we need, sessions.compact, is delegated to the bounded
 * external Host adapter through OpenClaw's argv-based command runtime. No
 * arbitrary Gateway method can cross this adapter.
 */
export function createContextMaintenanceApi(api:any,cfg:any={}) {
  const proxy=Object.create(api);
  const runtime=Object.create(api.runtime??{});
  const gateway=Object.create(api.runtime?.gateway??{});
  const originalRequest=api.runtime?.gateway?.request?.bind(api.runtime.gateway);

  gateway.request=async(method:string,params:any,options:any)=>{
    if(method==="sessions.describe") {
      const sessionKey=String(params?.key??"").trim();
      if(!sessionKey)return {session:null};
      const getEntry=api.runtime?.agent?.session?.getSessionEntry;
      if(typeof getEntry!=="function")throw new Error("OpenClaw supported session accessor is unavailable");
      const agentId=agentIdFromSessionKey(sessionKey);
      const entry=getEntry({sessionKey,...(agentId?{agentId}:{})});
      return {session:projectSessionEntry(entry)};
    }
    if(method==="chat.history")return readSupportedHistory(api,params);
    if(method==="sessions.compact")return runHostCompact(api,cfg,params,options);
    if(typeof originalRequest!=="function")throw new Error(`Gateway method unavailable: ${method}`);
    return originalRequest(method,params,options);
  };

  runtime.gateway=gateway;
  proxy.runtime=runtime;
  return proxy;
}
