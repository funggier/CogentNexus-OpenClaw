import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { contextRecoveryHoldSnapshot, createCnxRuntimeSafetyProxy, verifyCnxCompactionResult } from "./v090-runtime-safety.js";

function gatewayWithSession(session:any) {
  return {
    request:async(method:string)=>{
      if(method==="sessions.describe")return {session};
      throw new Error(`unexpected ${method}`);
    },
  };
}

function holdFixture(root:string) {
  const path=join(root,"tickets.sqlite3"),store=new TicketStore(path);
  const owner="agent:main:dashboard:A";
  const receipt=store.accept({runId:"run-hold",ownerSessionKey:owner,prompt:"long context task"});
  const ticketId=receipt.ticketId;
  store.route(ticketId,false);
  const db=new DatabaseSync(path),stamp=new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,state TEXT NOT NULL,generation INTEGER NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
    deleted_at TEXT,delete_reason TEXT);
    CREATE TABLE IF NOT EXISTS cnx_context_maintenance(
      session_key TEXT PRIMARY KEY,owner_generation INTEGER NOT NULL,ticket_id TEXT NOT NULL,state TEXT NOT NULL,
      last_action TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);`);
  db.prepare("INSERT OR REPLACE INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',4,?,?)").run(owner,stamp,stamp);
  db.prepare("INSERT INTO cnx_context_maintenance(session_key,owner_generation,ticket_id,state,last_action,created_at,updated_at) VALUES (?,?,?,'pending',NULL,?,?)")
    .run(owner,4,ticketId,stamp,stamp);
  db.close();
  const hidden=`agent:main:subagent:cnx-recovery-${ticketId}-0123456789ab-g4-deadbeef`;
  return {path,ticketId,owner,hidden};
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
    expect(result.cnxVerification).toMatchObject({verified:false,occupancyVerified:false,source:"unavailable"});
  });

  it("uses the conservative maximum of compaction tokensAfter and a fresh session counter",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:true,totalTokens:24000}),
      params:{key:"agent:main:dashboard:A"},
      result:{ok:true,compacted:true,result:{tokensBefore:30000,tokensAfter:18000}},
    });
    expect(result.result.tokensAfter).toBe(24000);
    expect(result.cnxVerification).toMatchObject({verified:true,occupancyVerified:true,observedAfter:24000});
  });

  it("fails closed when hard trim has neither fresh occupancy nor a retained-line proof",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:false,totalTokens:8000}),
      params:{key:"agent:main:dashboard:A",maxLines:60},
      result:{ok:true,compacted:true},
    });
    expect(result.ok).toBe(false);
    expect(result.compacted).toBe(false);
    expect(result.error).toMatch(/could not verify hard-trim occupancy or retained-line bound/i);
    expect(result.cnxVerification).toMatchObject({verified:false,occupancyVerified:false,structuralVerified:false});
  });

  it("accepts structural maxLines proof when manual trim invalidated token metadata",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:false,totalTokens:30000}),
      params:{key:"agent:main:dashboard:A",maxLines:60},
      result:{ok:true,compacted:true,kept:60,archived:"archive.jsonl"},
    });
    expect(result.ok).toBe(true);
    expect(result.compacted).toBe(true);
    expect(result.cnxVerification).toMatchObject({
      verified:true,
      occupancyVerified:false,
      structuralVerified:true,
      kept:60,
      maxLines:60,
      source:"max-lines-result",
    });
  });

  it("rejects a hard trim that still occupies more than 88 percent of the active window",async()=>{
    const result=await verifyCnxCompactionResult({
      originalGateway:gatewayWithSession({contextTokens:32768,totalTokensFresh:true,totalTokens:30000}),
      params:{key:"agent:main:dashboard:A",maxLines:60},
      result:{ok:true,compacted:true,kept:60},
    });
    expect(result.ok).toBe(false);
    expect(result.error).toMatch(/remained above safe context target/i);
    expect(result.cnxVerification).toMatchObject({verified:true,occupancyVerified:true,structuralVerified:true});
  });

  it("holds a Direct Recovery while context maintenance is active, then releases only safe terminal maintenance",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-context-hold-"));
    try{
      const {path,hidden}=holdFixture(root);
      expect(contextRecoveryHoldSnapshot(path,hidden)).toMatchObject({hold:true,revoked:false,state:"pending"});
      let db=new DatabaseSync(path);
      db.prepare("UPDATE cnx_context_maintenance SET state='done',last_action='semantic-compact' WHERE ticket_id=(SELECT ticket_id FROM cnx_context_maintenance LIMIT 1)").run();
      db.close();
      expect(contextRecoveryHoldSnapshot(path,hidden)).toMatchObject({hold:false,revoked:false,state:"done",action:"semantic-compact"});

      db=new DatabaseSync(path);
      db.prepare("UPDATE cnx_context_maintenance SET state='cancelled',last_action='authority-revoked' WHERE ticket_id=(SELECT ticket_id FROM cnx_context_maintenance LIMIT 1)").run();
      db.close();
      expect(contextRecoveryHoldSnapshot(path,hidden)).toMatchObject({hold:false,revoked:true,state:"cancelled",action:"authority-revoked"});

      db=new DatabaseSync(path);
      db.prepare("UPDATE cnx_context_maintenance SET state='cancelled',last_action='retry-limit' WHERE ticket_id=(SELECT ticket_id FROM cnx_context_maintenance LIMIT 1)").run();
      db.close();
      expect(contextRecoveryHoldSnapshot(path,hidden)).toMatchObject({hold:false,revoked:false,state:"cancelled",action:"retry-limit"});
    }finally{rmSync(root,{recursive:true,force:true});}
  });

  it("externalizes a huge CNXCLAW hidden-worker prompt while preserving exact bytes and SHA manifest",async()=>{
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
      const exact=`[CogentNexus-OpenClaw Internal Direct Recovery]\n${"abcdefghijklmnopqrstuvwxyz".repeat(500)}`;
      await proxy.runtime.subagent.run({sessionKey:"agent:main:subagent:cnx-test-0123456789ab-g1-deadbeef",message:exact,deliver:false});
      expect(launched.message.length).toBeLessThan(exact.length);
      expect(launched.message).toContain("[CogentNexus-OpenClaw Internal Payload Reference]");
      const manifestMatch=/Manifest: (\.cogentnexus-openclaw\/context\/synthetic-input\/[^\n]+\/manifest\.json)/u.exec(launched.message);
      expect(manifestMatch?.[1]).toBeTruthy();
      const manifest=JSON.parse(readFileSync(join(root,manifestMatch![1]),"utf8"));
      expect(manifest.totalChars).toBe(exact.length);
      expect(readFileSync(join(root,manifest.fullPath),"utf8")).toBe(exact);
      expect(manifest.chunks.length).toBeGreaterThan(1);
    }finally{rmSync(root,{recursive:true,force:true});}
  });
});
