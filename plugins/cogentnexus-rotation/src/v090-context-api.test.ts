import { describe, expect, it, vi } from "vitest";
import { createContextMaintenanceApi } from "./v090-context-api.js";

describe("v0.9 context maintenance OpenClaw projection",()=>{
  it("reads session telemetry through the supported session accessor and hides physical sessionId",async()=>{
    const gatewayRequest=vi.fn();
    const getSessionEntry=vi.fn(()=>({
      sessionId:"physical-after-compact",
      contextTokens:32768,
      totalTokens:7000,
      totalTokensFresh:true,
      compactionCheckpointCount:3,
    }));
    const api={runtime:{
      gateway:{request:gatewayRequest},
      agent:{session:{getSessionEntry}},
      subagent:{getSessionMessages:vi.fn()},
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("sessions.describe",{key:"agent:main:dashboard:A"});
    expect(result.session).toEqual({contextTokens:32768,totalTokens:7000,totalTokensFresh:true,compactionCheckpointCount:3});
    expect(result.session.sessionId).toBeUndefined();
    expect(getSessionEntry).toHaveBeenCalledWith({sessionKey:"agent:main:dashboard:A",agentId:"main"});
    expect(gatewayRequest).not.toHaveBeenCalled();
  });

  it("removes a stale numeric totalTokens value after manual trim invalidates freshness",async()=>{
    const api={runtime:{
      gateway:{request:vi.fn()},
      agent:{session:{getSessionEntry:()=>({sessionId:"physical-revision",contextTokens:32768,totalTokens:30000,totalTokensFresh:false})}},
      subagent:{getSessionMessages:vi.fn()},
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("sessions.describe",{key:"agent:main:dashboard:A"});
    expect(result.session).toEqual({contextTokens:32768,totalTokensFresh:false});
    expect(result.session.totalTokens).toBeUndefined();
  });

  it("reads bounded owner history through the supported subagent accessor",async()=>{
    const gatewayRequest=vi.fn();
    const getSessionMessages=vi.fn(async()=>({messages:[{role:"user",content:"a"},{role:"assistant",content:"b"}]}));
    const api={runtime:{
      gateway:{request:gatewayRequest},
      agent:{session:{getSessionEntry:vi.fn()}},
      subagent:{getSessionMessages},
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("chat.history",{sessionKey:"agent:main:dashboard:A",limit:50,maxChars:50000});
    expect(result.messages).toHaveLength(2);
    expect(getSessionMessages).toHaveBeenCalledWith({sessionKey:"agent:main:dashboard:A",limit:50});
    expect(gatewayRequest).not.toHaveBeenCalled();
  });

  it("delegates hard trim to Host and accepts it only after a fresh safe token measurement",async()=>{
    const gatewayRequest=vi.fn();
    const runCommandWithTimeout=vi.fn(async()=>({
      code:0,stdout:JSON.stringify({ok:true,compacted:true,kept:120}),stderr:"",signal:null,killed:false,termination:"exit",
    }));
    const getSessionEntry=vi.fn(()=>({contextTokens:32768,totalTokens:7000,totalTokensFresh:true}));
    const api={runtime:{
      gateway:{request:gatewayRequest},
      agent:{session:{getSessionEntry}},
      subagent:{getSessionMessages:vi.fn()},
      system:{runCommandWithTimeout},
    }};
    const proxy=createContextMaintenanceApi(api,{workspaceDir:"C:/workspace",cogentRoot:"C:/workspace/.cogent",pythonCommand:"python"});
    const result=await proxy.runtime.gateway.request("sessions.compact",{key:"agent:main:dashboard:A",maxLines:120},{timeoutMs:90000});
    expect(result.ok).toBe(true);
    expect(result.cnxVerification).toMatchObject({source:"fresh-session-counter",tokens:7000,kept:120});
    const [argv,options]=runCommandWithTimeout.mock.calls[0];
    expect(argv[0]).toBe("python");
    expect(argv.some((value:string)=>value.replace(/\\/gu,"/").endsWith("/host_context.py"))).toBe(true);
    expect(argv).toContain("compact");
    expect(argv).toContain("agent:main:dashboard:A");
    expect(argv).toContain("120");
    expect(argv).not.toContain("chat.abort");
    expect(options.killProcessTree).toBe(true);
    expect(gatewayRequest).not.toHaveBeenCalled();
  });

  it("rejects a hard trim that still has an unsafe fresh token count",async()=>{
    const runCommandWithTimeout=vi.fn(async()=>({code:0,stdout:JSON.stringify({ok:true,compacted:true,kept:60}),stderr:""}));
    const api={runtime:{
      gateway:{request:vi.fn()},
      agent:{session:{getSessionEntry:()=>({contextTokens:32768,totalTokens:29000,totalTokensFresh:true})}},
      subagent:{getSessionMessages:vi.fn()},
      system:{runCommandWithTimeout},
    }};
    const proxy=createContextMaintenanceApi(api,{workspaceDir:"C:/workspace",pythonCommand:"python"});
    await expect(proxy.runtime.gateway.request("sessions.compact",{key:"agent:main:dashboard:A",maxLines:60},{timeoutMs:90000}))
      .rejects.toThrow(/still reports .*\(safe=/u);
  });

  it("verifies a stale post-trim token counter from bounded transcript evidence",async()=>{
    const runCommandWithTimeout=vi.fn(async()=>({code:0,stdout:JSON.stringify({ok:true,compacted:true,kept:60}),stderr:""}));
    const getSessionMessages=vi.fn(async()=>({messages:[{role:"user",content:"hello"},{role:"assistant",content:"world"}]}));
    const api={runtime:{
      gateway:{request:vi.fn()},
      agent:{session:{getSessionEntry:()=>({contextTokens:32768,totalTokens:30000,totalTokensFresh:false})}},
      subagent:{getSessionMessages},
      system:{runCommandWithTimeout},
    }};
    const proxy=createContextMaintenanceApi(api,{workspaceDir:"C:/workspace",pythonCommand:"python"});
    const result=await proxy.runtime.gateway.request("sessions.compact",{key:"agent:main:dashboard:A",maxLines:60},{timeoutMs:90000});
    expect(result.cnxVerification.source).toBe("bounded-post-trim-estimate");
    expect(result.cnxVerification.kept).toBe(60);
    expect(getSessionMessages).toHaveBeenCalledWith({sessionKey:"agent:main:dashboard:A",limit:200});
  });

  it("fails closed when post-trim transcript evidence saturates its verification bound",async()=>{
    const runCommandWithTimeout=vi.fn(async()=>({code:0,stdout:JSON.stringify({ok:true,compacted:true,kept:1000}),stderr:""}));
    const messages=Array.from({length:2020},(_,i)=>({role:"user",content:`m${i}`}));
    const api={runtime:{
      gateway:{request:vi.fn()},
      agent:{session:{getSessionEntry:()=>({contextTokens:32768,totalTokensFresh:false})}},
      subagent:{getSessionMessages:vi.fn(async()=>({messages}))},
      system:{runCommandWithTimeout},
    }};
    const proxy=createContextMaintenanceApi(api,{workspaceDir:"C:/workspace",pythonCommand:"python"});
    await expect(proxy.runtime.gateway.request("sessions.compact",{key:"agent:main:dashboard:A",maxLines:1000},{timeoutMs:90000}))
      .rejects.toThrow(/verification saturated/u);
  });

  it("does not modify unrelated Gateway methods",async()=>{
    const expected={ok:true,value:42};
    const request=vi.fn(async()=>expected);
    const api={runtime:{
      gateway:{request},
      agent:{session:{getSessionEntry:vi.fn()}},
      subagent:{getSessionMessages:vi.fn()},
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    await expect(proxy.runtime.gateway.request("health",{})).resolves.toBe(expected);
    expect(request).toHaveBeenCalledTimes(1);
  });
});
