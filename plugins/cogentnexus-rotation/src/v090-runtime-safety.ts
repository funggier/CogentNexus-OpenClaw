import { resolve } from "node:path";
import { externalizeOversizedSyntheticPayload, type SyntheticPayloadConfig } from "./v090-synthetic-payload.js";

type RuntimeSafetyConfig = SyntheticPayloadConfig & { workspaceDir?:string };

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
    // Semantic compaction normally reports tokensAfter. If neither the RPC nor
    // a fresh session counter can verify it, force the caller down its bounded
    // fallback path instead of treating an unmeasured compaction as safe.
    const safeAfter=observedAfter??Number.MAX_SAFE_INTEGER;
    return {
      ...result,
      result:{...(result.result??{}),tokensAfter:safeAfter},
      cnxVerification:{verified:observedAfter!==undefined,observedAfter,contextWindow:window,source:freshAfter!==undefined?"fresh-session-counter":rawAfter!==undefined?"compaction-result":"unavailable"},
    };
  }

  // Hard trim is destructive to the active transcript (OpenClaw archives the
  // predecessor), so fail closed unless the post-trim session counter is fresh.
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

export function createCnxRuntimeSafetyProxy(api:any,config:RuntimeSafetyConfig={}) {
  const proxy=Object.create(api);
  const runtime=Object.create(api.runtime??{});
  const workspaceDir=resolve(config.workspaceDir??process.cwd());

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
      const bounded=externalizeOversizedSyntheticPayload({workspaceDir,sessionKey,message,config});
      if(bounded.externalized)api.logger.info?.(`CogentNexus externalized oversized hidden payload for ${sessionKey}: chunks=${bounded.chunkCount} sha256=${bounded.sha256?.slice(0,16)}`);
      return originalSubagent.run({...input,message:bounded.message});
    };
    runtime.subagent=subagent;
  }

  proxy.runtime=runtime;
  return proxy;
}
