import { describe, expect, it } from "vitest";
import { createContextMaintenanceApi } from "./v090-context-api.js";

describe("v0.9 context maintenance OpenClaw projection",()=>{
  it("hides physical sessionId so manual Compact is not treated as an ownership reset",async()=>{
    const api={runtime:{gateway:{request:async()=>({session:{sessionId:"physical-after-compact",contextTokens:32768,totalTokens:7000,totalTokensFresh:true}})}}};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("sessions.describe",{key:"agent:main:dashboard:A"});
    expect(result.session).toEqual({contextTokens:32768,totalTokens:7000,totalTokensFresh:true});
    expect(result.session.sessionId).toBeUndefined();
  });

  it("removes a stale numeric totalTokens value after manual maxLines trim invalidates freshness",async()=>{
    const api={runtime:{gateway:{request:async()=>({session:{sessionId:"physical-revision",contextTokens:32768,totalTokens:30000,totalTokensFresh:false}})}}};
    const proxy=createContextMaintenanceApi(api);
    const result=await proxy.runtime.gateway.request("sessions.describe",{key:"agent:main:dashboard:A"});
    expect(result.session).toEqual({contextTokens:32768,totalTokensFresh:false});
    expect(result.session.totalTokens).toBeUndefined();
  });

  it("does not modify unrelated Gateway methods",async()=>{
    const expected={ok:true,value:42};
    const api={runtime:{gateway:{request:async()=>expected}}};
    const proxy=createContextMaintenanceApi(api);
    await expect(proxy.runtime.gateway.request("chat.history",{})).resolves.toBe(expected);
  });
});
