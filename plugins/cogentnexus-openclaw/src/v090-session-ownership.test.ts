import { DatabaseSync } from "node:sqlite";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import * as v090 from "./v090.js";
import * as v090Entry from "./v090.js";

function sessionAuthority(path:string,key:string) {
  const db = new DatabaseSync(path);
  try {
    return db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(key) as any;
  } finally { db.close(); }
}

describe("v0.9 session ownership", () => {
  it("replaces stale lifecycle owner without allowing old work", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-session-owner-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:K";
      const store = new TicketStore(path);
      const old = store.accept({runId:"old",ownerSessionKey:key,prompt:"old work"});
      store.route(old.ticketId,true);
      const before = sessionAuthority(path,key);
      const result = v090.deleteSessionByKey(path,{sessionKey:key,message:"deleted",sessionId:"A"} as any);
      expect(result).toBeTruthy();
      const deleted = sessionAuthority(path,key);
      expect(deleted.state).toBe("deleted");
      const runs = store.runRecovery({limit:10});
      expect(runs).toBe(0);
      expect(result).toMatchObject({queued:false,suppressed:true,reason:"session generation superseded"});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("reactivates a genuinely new lifecycle on the same deleted session key while reusing the tombstoned generation", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-session-recreate-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:K";
      const store = new TicketStore(path);
      const old = store.accept({runId:"old",ownerSessionKey:key,prompt:"old work"});
      store.route(old.ticketId,true);
      const before = sessionAuthority(path,key);
      v090.deleteSessionByKey(path,{sessionKey:key,message:"deleted",sessionId:"A"} as any);
      v090.finalizeSessionDeletion(path,key,"deleted");
      const deleted = sessionAuthority(path,key);
      expect(deleted.state).toBe("deleted");

      const reactivate = (v090 as any).reactivateSessionForLifecycle;
      expect(reactivate).toBeTypeOf("function");
      expect(reactivate(path,{sessionKey:key,sessionId:"A"}))
        .toMatchObject({state:"deleted",accepted:false,lifecycleMatches:false});
      expect(reactivate(path,{sessionKey:key,sessionId:"B"})).toMatchObject({state:"active"});
      expect(sessionAuthority(path,key)).toEqual({state:"active",generation:deleted.generation+1});
      expect((v090 as any).reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"B"}))
        .toMatchObject({state:"active",generation:deleted.generation+1});
      expect((v090 as any).reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"A"}))
        .toMatchObject({state:"active",accepted:false,lifecycleMatches:false});
      expect((v090 as any).reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"C"}))
        .toMatchObject({state:"active",accepted:false,lifecycleMatches:false});
      expect((v090 as any).reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"B"}))
        .toMatchObject({state:"active",accepted:true,lifecycleMatches:true,generation:deleted.generation+1});
      const identity = new DatabaseSync(path,{readOnly:true});
      expect(identity.prepare("SELECT generation,session_id,state FROM cnx_sessions WHERE session_key=?").get(key))
        .toEqual({generation:deleted.generation+1,session_id:"B",state:"active"});
      identity.close();
      const verify = new DatabaseSync(path,{readOnly:true});
      expect(verify.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(old.ticketId)).toEqual({status:"cancelled"});
      verify.close();
      expect(() => store.accept({runId:"new",ownerSessionKey:key,prompt:"fresh work"})).not.toThrow();
      expect(before.generation).toBe(deleted.generation-1);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("binds a legacy active NULL lifecycle without generation churn", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-legacy-lifecycle-"));
    try {
      const path = join(root, "tickets.sqlite3"), key = "agent:main:dashboard:legacy";
      const initial = sessionAuthority(path, key);
      const db = new DatabaseSync(path);
      db.prepare("UPDATE cnx_sessions SET session_id=NULL WHERE session_key=?").run(key);
      db.close();
      const result = (v090 as any).reactivateSessionForLifecycle(path, {sessionKey:key,sessionId:"legacy-current"});
      expect(result).toMatchObject({state:"active",accepted:true,lifecycleMatches:true,generation:initial.generation});
      expect((v090 as any).isCurrentSessionLifecycle(path, {sessionKey:key,sessionId:"legacy-current"})).toBe(true);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("blocks before_agent_run when OpenClaw lifecycle identity is stale", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-hook-lifecycle-"));
    try {
      const path = join(root, "tickets.sqlite3"), key = "agent:main:dashboard:hook";
      (v090 as any).reactivateSessionForLifecycle(path, {sessionKey:key,sessionId:"current-B"});
      const hooks = new Map<string, any[]>();
      const api:any = {
        pluginConfig:{ticketFirst:false,preInferenceAdmission:false,ticketDatabasePath:path,workspaceDir:root},
        registerTool:()=>{}, registerService:()=>{},
        on:(name:string, handler:any)=>{ const list=hooks.get(name) ?? []; list.push(handler); hooks.set(name,list); },
        logger:{warn:()=>{},error:()=>{},info:()=>{}}, session:{workflow:{}}, runtime:{tasks:{managedFlows:{}}},
      };
      (v090Entry as any).register(api);
      const before = hooks.get("before_agent_run") ?? [];
      const stale = before.map((handler) => handler({prompt:"ordinary owner prompt"},{sessionKey:key,sessionId:"stale-A",workspaceDir:root}))
        .find((result:any) => result?.category === "cnxclaw_lifecycle_identity");
      expect(stale).toMatchObject({outcome:"block",category:"cnxclaw_lifecycle_identity"});
      const current = before.map((handler) => handler({prompt:"ordinary owner prompt"},{sessionKey:key,sessionId:"current-B",workspaceDir:root}))
        .find((result:any) => result?.category === "cnxclaw_lifecycle_identity");
      expect(current).toBeUndefined();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("admits the first owner turn before asynchronous session_start", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-first-turn-order-"));
    try {
      const path = join(root, "tickets.sqlite3"), key = "agent:main:discord:ordered";
      const store = new TicketStore(path);
      const old = store.accept({runId:"old",ownerSessionKey:key,prompt:"old work"});
      store.route(old.ticketId,true);
      v090.deleteSessionByKey(path,{sessionKey:key,message:"deleted",sessionId:"A"} as any);
      v090.finalizeSessionDeletion(path,key,"deleted");
      const deleted = sessionAuthority(path,key);
      const hooks = new Map<string, any[]>();
      const api:any = {
        pluginConfig:{ticketFirst:false,preInferenceAdmission:false,ticketDatabasePath:path,workspaceDir:root},
        registerTool:()=>{}, registerService:()=>{},
        on:(name:string, handler:any)=>{ const list=hooks.get(name) ?? []; list.push(handler); hooks.set(name,list); },
        logger:{warn:()=>{},error:()=>{},info:()=>{}}, session:{workflow:{}}, runtime:{tasks:{managedFlows:{}}},
      };
      (v090Entry as any).register(api);
      const before = hooks.get("before_agent_run") ?? [];
      const invoke = (sessionId:string) => before.map((handler) => handler({prompt:"ordinary owner prompt"},{sessionKey:key,sessionId,workspaceDir:root}));
      expect(invoke("B").some((result:any) => result?.category === "cnxclaw_lifecycle_identity")).toBe(false);
      const verify = new DatabaseSync(path,{readOnly:true});
      expect(verify.prepare("SELECT state,session_id,generation FROM cnx_sessions WHERE session_key=?").get(key))
        .toEqual({state:"active",session_id:"B",generation:deleted.generation+1});
      verify.close();
      expect(invoke("A").some((result:any) => result?.category === "cnxclaw_lifecycle_identity")).toBe(true);
      expect(invoke("C").some((result:any) => result?.category === "cnxclaw_lifecycle_identity")).toBe(true);
      for (const handler of hooks.get("session_start") ?? []) handler({sessionKey:key,sessionId:"B"},{sessionKey:key,sessionId:"B",workspaceDir:root});
      expect(sessionAuthority(path,key)).toEqual({state:"active",generation:deleted.generation+1});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("cross-session context is read-only and internal synthetic turns are excluded", () => {
    const context = (v090 as any).boundedOwnerContext([
      {role:"user",content:"real message from another session"},
      {role:"assistant",content:"useful prior result"},
      {role:"user",content:"#cogent-direct\n[CogentNexus-OpenClaw Continuation: internal]"},
      {role:"user",content:"[CogentNexus-OpenClaw Delivery: ticket:9]\ninternal"},
    ]);
    expect(context.some((item:any)=>String(item.content).includes("real message"))).toBe(true);
    expect(context.some((item:any)=>String(item.content).includes("CogentNexus-OpenClaw Continuation"))).toBe(false);
    expect(context.some((item:any)=>String(item.content).includes("CogentNexus-OpenClaw Delivery"))).toBe(false);
  });
});
