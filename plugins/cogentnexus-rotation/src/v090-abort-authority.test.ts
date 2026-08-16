import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import {
  RECOVERABLE_ABORT_MESSAGE,
  classifyAbortAuthority,
  createAbortAuthorityApi,
  hasStructuredHumanAbort,
} from "./v090-abort-authority.js";

function writeJson(path:string,value:unknown){mkdirSync(join(path,".."),{recursive:true});writeFileSync(path,JSON.stringify(value));}

describe("v0.9 abort authority",()=>{
  it("recognizes structured OpenClaw rpc/stop-command abort evidence",()=>{
    const messages=[{role:"assistant",openclawAbort:{aborted:true,origin:"rpc",runId:"run-a"}}];
    expect(hasStructuredHumanAbort(messages,"run-a")).toBe(true);
    expect(hasStructuredHumanAbort(messages,"run-b")).toBe(false);
  });

  it("treats an ambiguous abort as recoverable without managed watchdog protection",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-auth-"));
    try{
      expect(classifyAbortAuthority(
        {success:false,error:"Reply operation aborted by user",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:join(root,".cogent")},
      )).toBe("recoverable-ambiguous");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("lets managed compatibility preserve UI Stop semantics after the watchdog ambiguity is neutralized",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-managed-")),cogent=join(root,".cogent");
    try{
      writeJson(join(cogent,"host","openclaw-watchdog-compat.json"),{applied:true,managedValue:86400000});
      expect(classifyAbortAuthority(
        {success:false,error:"Reply operation aborted by user",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:cogent},
      )).toBe("managed-human-compat");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never treats Gateway maintenance aborts as human Stop",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-maint-")),cogent=join(root,".cogent");
    try{
      writeJson(join(cogent,"host","openclaw-watchdog-compat.json"),{applied:true,managedValue:86400000});
      writeJson(join(cogent,"runtime","maintenance.json"),{active:true,reason:"operator lifecycle stop"});
      expect(classifyAbortAuthority(
        {success:false,error:"agent run aborted",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:cogent},
      )).toBe("recoverable-maintenance");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("sanitizes ambiguous agent_end before legacy cancellation/finalization handlers see it",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-proxy-"));
    try{
      let registered:any;
      const api={
        on:vi.fn((name:string,handler:any)=>{if(name==="agent_end")registered=handler;}),
        logger:{info:vi.fn()},
      };
      const proxy=createAbortAuthorityApi(api,{workspaceDir:root,cogentRoot:join(root,".cogent")});
      const seen:any[]=[];
      proxy.on("agent_end",(event:any)=>seen.push(event));
      await registered({success:false,error:"Reply operation aborted by user",runId:"run-a",messages:[]},{runId:"run-a",workspaceDir:root});
      expect(seen[0].error).toBe(RECOVERABLE_ABORT_MESSAGE);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
