import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { createCnxRuntimeSafetyProxy } from "./v090-runtime-safety.js";

function sha(path:string){return createHash("sha256").update(readFileSync(path)).digest("hex");}

function gatewayCapture(){
  const calls:Array<{method:string;params:any;options:any}>=[];
  const gateway={
    request:async(method:string,params?:any,options?:any)=>{
      calls.push({method,params,options});
      if(method==="sessions.patch")return {ok:true,resolved:{model:params?.model,modelProvider:"ollama"}};
      throw new Error(`unexpected ${method}`);
    },
  };
  return {gateway,calls};
}

describe("v0.9 user model-selection boundary",()=>{
  it("passes sessions.patch model selection through without creating CNXCLAW SQLite state",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-model-no-db-"));
    try{
      const databasePath=join(root,"never-created.sqlite3"),capture=gatewayCapture();
      const api={runtime:{gateway:capture.gateway},logger:{info:()=>{}}};
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,ticketDatabasePath:databasePath});
      const result=await proxy.runtime.gateway.request("sessions.patch",{key:"agent:main:dashboard:A",model:"ollama/qwen3.8:27b"});
      expect(result).toMatchObject({ok:true,resolved:{model:"ollama/qwen3.8:27b"}});
      expect(capture.calls).toEqual([{method:"sessions.patch",params:{key:"agent:main:dashboard:A",model:"ollama/qwen3.8:27b"},options:undefined}]);
      expect(existsSync(databasePath)).toBe(false);
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("leaves an existing CogentNexus-OpenClaw database byte-identical when the user changes model",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-model-existing-db-"));
    try{
      const databasePath=join(root,"tickets.sqlite3"),store=new TicketStore(databasePath);
      const ticket=store.accept({runId:"run-existing",ownerSessionKey:"agent:main:dashboard:A",prompt:"existing committed intent"});
      store.route(ticket.ticketId,false);
      const before=sha(databasePath),beforeBytes=readFileSync(databasePath);
      const capture=gatewayCapture(),api={runtime:{gateway:capture.gateway},logger:{info:()=>{}}};
      const proxy=createCnxRuntimeSafetyProxy(api,{workspaceDir:root,ticketDatabasePath:databasePath});
      await proxy.runtime.gateway.request("sessions.patch",{key:"agent:main:dashboard:A",model:"ollama/gpt-oss:20b"});
      const after=sha(databasePath),afterBytes=readFileSync(databasePath);
      expect(after).toBe(before);
      expect(Buffer.compare(afterBytes,beforeBytes)).toBe(0);
      expect(store.get(ticket.ticketId)).toMatchObject({ticketId:ticket.ticketId});
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("does not treat model changes as Reset, Compact, Stop, or a human Ticket event",async()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-model-semantic-"));
    try{
      const databasePath=join(root,"tickets.sqlite3"),store=new TicketStore(databasePath);
      store.snapshot();
      const before=sha(databasePath),capture=gatewayCapture();
      const proxy=createCnxRuntimeSafetyProxy({runtime:{gateway:capture.gateway},logger:{info:()=>{}}},{workspaceDir:root,ticketDatabasePath:databasePath});
      await proxy.runtime.gateway.request("sessions.patch",{key:"agent:main:dashboard:A",model:"ollama/qwen3.8:27b"});
      await proxy.runtime.gateway.request("sessions.patch",{key:"agent:main:dashboard:A",model:"ollama/gpt-oss:20b"});
      expect(sha(databasePath)).toBe(before);
      const db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT count(*) AS count FROM tickets").get()).toEqual({count:0});
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events").get()).toEqual({count:0});
      db.close();
      expect(capture.calls.map((call)=>call.method)).toEqual(["sessions.patch","sessions.patch"]);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
