import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import {
  RECOVERABLE_ABORT_MESSAGE,
  classifyAbortAuthority,
  createAbortAuthorityApi,
  hasStructuredHumanAbort,
  stopMarkerAdvanced,
} from "./v090-abort-authority.js";

function writeJson(path:string,value:unknown){mkdirSync(dirname(path),{recursive:true});writeFileSync(path,JSON.stringify(value));}

describe("v0.9 abort authority",()=>{
  it("recognizes structured OpenClaw rpc/stop-command abort evidence",()=>{
    const messages=[{role:"assistant",openclawAbort:{aborted:true,origin:"rpc",runId:"run-a"}}];
    expect(hasStructuredHumanAbort(messages,"run-a")).toBe(true);
    expect(hasStructuredHumanAbort(messages,"run-b")).toBe(false);
  });

  it("treats an ambiguous abort as recoverable even when managed mode is active",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-auth-"));
    try{
      expect(classifyAbortAuthority(
        {success:false,error:"Reply operation aborted by user",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:join(root,".cogent")},
      )).toBe("recoverable-ambiguous");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("requires a durable Stop cutoff to advance during the run",()=>{
    expect(stopMarkerAdvanced(
      {messageSid:"old",timestamp:1000},
      {messageSid:"old",timestamp:1000},
    )).toBe(false);
    expect(stopMarkerAdvanced(
      {messageSid:"old",timestamp:1000},
      {messageSid:"new",timestamp:2000},
    )).toBe(true);
    expect(stopMarkerAdvanced(
      {},
      {messageSid:"first",timestamp:2000},
    )).toBe(true);
    expect(stopMarkerAdvanced(undefined,{messageSid:"new",timestamp:2000})).toBe(false);
  });

  it("classifies durable cutoff evidence as authoritative human Stop",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-durable-"));
    try{
      expect(classifyAbortAuthority(
        {success:false,error:"agent run aborted",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:join(root,".cogent")},
        true,
      )).toBe("durable-human-stop");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("never treats Gateway maintenance aborts as human Stop without durable evidence",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-maint-")),cogent=join(root,".cogent");
    try{
      writeJson(join(cogent,"runtime","maintenance.json"),{active:true,reason:"operator lifecycle stop"});
      expect(classifyAbortAuthority(
        {success:false,error:"agent run aborted",runId:"run-a",messages:[]},
        {runId:"run-a",workspaceDir:root},
        {workspaceDir:root,cogentRoot:cogent},
      )).toBe("recoverable-maintenance");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("snapshots the pre-run cutoff and only forwards a later advanced cutoff as user Stop",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-proxy-"));
    try{
      const handlers=new Map<string,any[]>();
      let entry:any={sessionId:"physical-a",abortCutoffMessageSid:"old",abortCutoffTimestamp:1000};
      const api={
        runtime:{agent:{session:{getSessionEntry:vi.fn(()=>entry)}}},
        on:vi.fn((name:string,handler:any)=>{const list=handlers.get(name)??[];list.push(handler);handlers.set(name,list);}),
        logger:{info:vi.fn()},
      };
      const proxy=createAbortAuthorityApi(api,{workspaceDir:root,cogentRoot:join(root,".cogent")});
      const seen:any[]=[];
      proxy.on("before_agent_run",()=>undefined);
      proxy.on("agent_end",(event:any)=>seen.push(event));
      const ctx={runId:"run-a",sessionKey:"agent:main:dashboard:A",workspaceDir:root};
      await handlers.get("before_agent_run")?.[0]({runId:"run-a"},ctx);
      entry={...entry,abortCutoffMessageSid:"new",abortCutoffTimestamp:2000};
      await handlers.get("agent_end")?.[0]({success:false,error:"Reply operation aborted by user",runId:"run-a",messages:[]},ctx);
      expect(seen[0].error).toBe("Reply operation aborted by user");
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("sanitizes an abort when only an old cutoff exists",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-abort-stale-"));
    try{
      const handlers=new Map<string,any[]>();
      const entry={sessionId:"physical-a",abortCutoffMessageSid:"old",abortCutoffTimestamp:1000};
      const api={
        runtime:{agent:{session:{getSessionEntry:vi.fn(()=>entry)}}},
        on:vi.fn((name:string,handler:any)=>{const list=handlers.get(name)??[];list.push(handler);handlers.set(name,list);}),
        logger:{info:vi.fn()},
      };
      const proxy=createAbortAuthorityApi(api,{workspaceDir:root,cogentRoot:join(root,".cogent")});
      const seen:any[]=[];
      proxy.on("before_agent_run",()=>undefined);
      proxy.on("agent_end",(event:any)=>seen.push(event));
      const ctx={runId:"run-b",sessionKey:"agent:main:dashboard:A",workspaceDir:root};
      await handlers.get("before_agent_run")?.[0]({runId:"run-b"},ctx);
      await handlers.get("agent_end")?.[0]({success:false,error:"Reply operation aborted by user",runId:"run-b",messages:[]},ctx);
      expect(seen[0].error).toBe(RECOVERABLE_ABORT_MESSAGE);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
