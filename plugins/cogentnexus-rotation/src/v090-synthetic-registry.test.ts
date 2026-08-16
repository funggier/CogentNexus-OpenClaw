import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  recordSyntheticSpawn,
  settleSyntheticRun,
  staleSyntheticRuns,
  syntheticIdentityFromChildKey,
} from "./v090-synthetic-registry.js";

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "cnx-v090-synth-reg-"));
  const path = join(root, "tickets.sqlite3");
  new TicketStore(path).snapshot();
  const db = new DatabaseSync(path);
  db.exec(`CREATE TABLE IF NOT EXISTS cnx_sessions(
    session_key TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    generation INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT,
    delete_reason TEXT
  )`);
  const stamp = new Date().toISOString();
  db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',3,?,?)")
    .run("agent:main:dashboard:A",stamp,stamp);
  db.close();
  const hash = createHash("sha256").update("agent:main:dashboard:A").digest("hex").slice(0,12);
  const child = `agent:main:subagent:cnx-recovery-test-${hash}-g3-deadbeef`;
  return {root,path,child};
}

describe("v0.9 durable synthetic execution registry", () => {
  it("resolves exact owner and generation from a CNX hidden child key", () => {
    const {root,path,child} = fixture();
    try {
      expect(syntheticIdentityFromChildKey(path,child)).toEqual({sessionKey:"agent:main:dashboard:A",generation:3});
      expect(syntheticIdentityFromChildKey(path,"agent:main:subagent:other")).toBeUndefined();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("persists a hidden run and exposes it only to a later runtime instance", () => {
    const {root,path,child} = fixture();
    try {
      expect(recordSyntheticSpawn(path,{runId:"cnx-hidden-1",childSessionKey:child,runtimeInstance:"runtime-old"})).toBe(true);
      expect(staleSyntheticRuns(path,"runtime-old")).toEqual([]);
      expect(staleSyntheticRuns(path,"runtime-new")).toMatchObject([{
        runId:"cnx-hidden-1",
        ownerSessionKey:"agent:main:dashboard:A",
        ownerGeneration:3,
        childSessionKey:child,
        runtimeInstance:"runtime-old",
      }]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("does not register a child whose captured generation no longer owns the session", () => {
    const {root,path,child} = fixture();
    try {
      const db = new DatabaseSync(path);
      db.prepare("UPDATE cnx_sessions SET generation=4 WHERE session_key='agent:main:dashboard:A'").run();
      db.close();
      expect(recordSyntheticSpawn(path,{runId:"stale",childSessionKey:child,runtimeInstance:"runtime-old"})).toBe(false);
      expect(staleSyntheticRuns(path,"runtime-new")).toEqual([]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("settles a completed run so restart fencing does not touch it", () => {
    const {root,path,child} = fixture();
    try {
      recordSyntheticSpawn(path,{runId:"done-run",childSessionKey:child,runtimeInstance:"runtime-old"});
      expect(settleSyntheticRun(path,{runId:"done-run",state:"done",outcome:"ok"})).toBe(1);
      expect(staleSyntheticRuns(path,"runtime-new")).toEqual([]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });
});
