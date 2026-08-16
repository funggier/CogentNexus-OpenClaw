import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { createCnxRuntimeSafetyProxy, verifyCnxCompactionResult } from "./v090-runtime-safety.js";

function gatewayWithSession(session:any) {
  return {
    request:async(method:string)=>{
      if(method==="sessions.describe")return {session};
      throw new Error(`unexpected ${method}`);
    },
  };
}

describe("v0.9 runtime safety proxy",()=>{
  it("marks unmeasured semantic compaction unsafe instead of silently accepting it",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:false,totalTokens:1000}),
      params:{key:"agent:main:dashboard:A"},
      result:{ok:true,compacted:true,result:{}},
    });
    expect(result.ok).toBe(true);
    expect(result.result.tokensAfter).toBe(Number.MAX_SAFE_INTEGER);
    expect(result.cnxVerification.verified).toBe(false);
  });

  it("uses the conservative maximum of compaction tokensAfter and a fresh session counter",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:true,totalTokens:24000}),
      params:{key:"agent:main:dashboard:A"},
      result:{ok:true,compacted:true,result:{tokensBefore:30000,tokensAfter:18000}},
    });
    expect(result.result.tokensAfter).toBe(24000);
    expect(result.cnxVerification.verified).toBe(true);
  });

  it("fails closed when hard-trim occupancy cannot be freshly verified",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:false,totalTokens:8000}),
      params:{key:"agent:main:dashboard:A",maxLines:60},
      result:{ok:true,compacted:true},
    });
    expect(result.ok).toBe(false);
    expect(result.compacted).toBe(false);
    expect(result.error).toMatch(/could not verify fresh post-hard-trim/i);
  });

  it("rejects a hard trim that still occupies more than 88 percent of the active window",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:true,totalTokens:30000}),
      params:{key:"agent:main:dashboard:A",maxLines:60},
      result:{ok:true,compacted:true},
    });
    expect(result.ok).toBe(false);
    expect(result.error).toMatch(/remained above safe context target/i);
  });

  it("externalizes a huge CNX hidden-worker prompt while preserving exact bytes and SHA manifest",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-runtime-safety-"));
    try{
      let launched:any;
      const api={
        runtime:{
          gateway:{request:async()=>({})},
          subagent:{run:async(input:any)=>{launched=input;return {runId:"r1"};}},
        },
        logger:{info:()=>{}},
      };
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,syntheticPromptInlineChars:4000,syntheticPromptChunkChars:2000});
      const exact=`[CogentNexus Internal Direct Recovery]\n${"abcdefghijklmnopqrstuvwxyz".repeat(500)}`;
      await proxy.runtime.subagent.run({sessionKey:"agent:main:subagent:cnx-test-0123456789ab-g1-deadbeef",message:exact,deliver:false});
      expect(launched.message.length).toBeLessThan(exact.length);
      expect(launched.message).toContain("[CogentNexus Internal Payload Reference]");
      const manifestMatch=/Manifest: (\.cogent\/context\/synthetic-input\/[^\n]+\/manifest\.json)/u.exec(launched.message);
      expect(manifestMatch?.[1]).toBeTruthy();
      const manifest=JSON.parse(readFileSync(join(root,manifestMatch![1]),"utf8"));
      expect(manifest.totalChars).toBe(exact.length);
      expect(readFileSync(join(root,manifest.fullPath),"utf8")).toBe(exact);
      expect(manifest.chunks.length).toBeGreaterThan(1);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
