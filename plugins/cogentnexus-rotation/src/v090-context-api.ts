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

function sessionEntry(api:any,sessionKey:string) {
  const getEntry=api.runtime?.agent?.session?.getSessionEntry;
  if(typeof getEntry!=="function")return undefined;
  const agentId=agentIdFromSessionKey(sessionKey);
  return getEntry({sessionKey,...(agentId?{agentId}:{})});
}

function estimateTokens(value:unknown) {
  let text="";
  try{text=JSON.stringify(value??"");}catch{text=String(value??"");}
  // Deliberately conservative for mixed English/Thai/JSON/tool payloads.
  return Math.ceil(text.length/2.2);
}

async function verifyHardTrim(api:any,sessionKey:string,maxLines:number,result:any) {
  if(result?.ok!==true||result?.compacted!==true)throw new Error(`hard trim ${maxLines} did not confirm compaction`);
  const kept=Number(result?.kept);
  if(!Number.isInteger(kept)||kept<0||kept>maxLines)throw new Error(`hard trim ${maxLines} returned invalid kept=${String(result?.kept)}`);

  const entry=sessionEntry(api,sessionKey);
  const contextWindow=Math.max(8192,Math.floor(Number(entry?.contextTokens)||32768));
  const headroom=Math.max(4096,Math.min(16384,Math.floor(contextWindow*0.18)));
  const safeLimit=Math.max(4096,Math.min(Math.floor(contextWindow*0.88),contextWindow-headroom));
  if(entry?.totalTokensFresh===true&&Number.isFinite(Number(entry?.totalTokens))&&Number(entry.totalTokens)>0) {
    const tokens=Number(entry.totalTokens);
    if(tokens>safeLimit)throw new Error(`hard trim ${maxLines} still reports ${tokens}/${contextWindow} tokens (safe=${safeLimit})`);
    return {...result,cnxVerification:{source:"fresh-session-counter",tokens,safeLimit,contextWindow,kept}};
  }

  const getMessages=api.runtime?.subagent?.getSessionMessages;
  if(typeof getMessages!=="function")throw new Error(`hard trim ${maxLines} invalidated token freshness and no supported transcript accessor is available`);
  const limit=Math.max(200,Math.min(2500,maxLines*2+20));
  const history=await getMessages({sessionKey,limit});
  const messages=Array.isArray(history?.messages)?history.messages:undefined;
  if(!messages)throw new Error(`hard trim ${maxLines} could not verify the post-trim transcript`);
  // maxLines is transcript-line bounded; request substantially more logical
  // messages than retained lines. If the accessor still saturates, evidence is
  // incomplete and must fail closed rather than undercounting the transcript.
  if(messages.length>=limit)throw new Error(`hard trim ${maxLines} post-trim transcript verification saturated at ${limit} messages`);
  const estimated=estimateTokens(messages);
  if(estimated>safeLimit)throw new Error(`hard trim ${maxLines} estimated ${estimated}/${contextWindow} tokens after trim (safe=${safeLimit})`);
  return {...result,cnxVerification:{source:"bounded-post-trim-estimate",tokens:estimated,safeLimit,contextWindow,kept,messageCount:messages.length}};
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
  const maxLines=Number.isInteger(params?.maxLines)&&params.maxLines>0?Number(params.maxLines):undefined;
  if(maxLines!==undefined)argv.push("--max-lines",String(maxLines));
  const commandResult=await run(argv,{timeoutMs:timeoutMs+20_000,killProcessTree:true,maxOutputBytes:1_000_000});
  if(commandResult?.code!==0)throw new Error(String(commandResult?.stderr||commandResult?.stdout||`Host context adapter failed (${commandResult?.code??"unknown"})`).trim());
  const result=parseJsonOutput(String(commandResult?.stdout??""));
  return maxLines===undefined?result:verifyHardTrim(api,sessionKey,maxLines,result);
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
      const entry=sessionEntry(api,sessionKey);
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
