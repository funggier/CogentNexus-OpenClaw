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
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("sessions.describe",{key:"agent:main:dashboard:A"});
    expect(result.session).toEqual({contextTokens:32768,totalTokensFresh:false});
    expect(result.session.totalTokens).toBeUndefined();
  });

  it("delegates sessions.compact to the fixed Host adapter instead of privileged Gateway RPC",async()=>{
    const gatewayRequest=vi.fn();
    const runCommandWithTimeout=vi.fn(async(argv:string[])=>({
      code:0,stdout:JSON.stringify({ok:true,tokensAfter:7000}),stderr:"",signal:null,killed:false,termination:"exit",
      argv,
    }));
    const api={runtime:{
      gateway:{request:gatewayRequest},
      agent:{session:{getSessionEntry:vi.fn()}},
      system:{runCommandWithTimeout},
    }};
    const proxy=createContextMaintenanceApi(api,{workspaceDir:"C:/workspace",cogentRoot:"C:/workspace/.cogent",pythonCommand:"python"});
    await expect(proxy.runtime.gateway.request("sessions.compact",{key:"agent:main:dashboard:A",maxLines:120},{timeoutMs:90000}))
      .resolves.toEqual({ok:true,tokensAfter:7000});
    const [argv,options]=runCommandWithTimeout.mock.calls[0];
    expect(argv[0]).toBe("python");
    expect(argv).toContain("host_context.py");
    expect(argv).toContain("compact");
    expect(argv).toContain("agent:main:dashboard:A");
    expect(argv).toContain("120");
    expect(argv).not.toContain("chat.abort");
    expect(options.killProcessTree).toBe(true);
    expect(gatewayRequest).not.toHaveBeenCalled();
  });

  it("does not modify unrelated Gateway methods",async()=>{
    const expected={ok:true,value:42};
    const request=vi.fn(async()=>expected);
    const api={runtime:{
      gateway:{request},
      agent:{session:{getSessionEntry:vi.fn()}},
      system:{runCommandWithTimeout:vi.fn()},
    }};
    const proxy=createContextMaintenanceApi(api);
    await expect(proxy.runtime.gateway.request("chat.history",{})).resolves.toBe(expected);
    expect(request).toHaveBeenCalledTimes(1);
  });
});
