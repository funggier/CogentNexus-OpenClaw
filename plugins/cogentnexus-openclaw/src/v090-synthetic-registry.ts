import { createHash } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { TicketStore } from "./ticket-store.js";

type SyntheticOwner = {
  sessionKey: string;
  generation: number;
};

export type StaleSyntheticRun = {
  runId: string;
  ownerSessionKey: string;
  ownerGeneration: number;
  childSessionKey: string;
  runtimeInstance: string;
};

function openDb(databasePath: string) {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_synthetic_runs(
      run_id TEXT PRIMARY KEY,
      owner_session_key TEXT NOT NULL,
      owner_generation INTEGER NOT NULL,
      child_session_key TEXT NOT NULL,
      runtime_instance TEXT NOT NULL,
      state TEXT NOT NULL DEFAULT 'running' CHECK(state IN ('running','done','cancelled')),
      outcome TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      ended_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_cnx_synthetic_active
      ON cnx_synthetic_runs(state,runtime_instance,owner_session_key,owner_generation);
    CREATE INDEX IF NOT EXISTS idx_cnx_synthetic_child
      ON cnx_synthetic_runs(child_session_key,state);
  `);
  return db;
}

function ownerHash(sessionKey: string) {
  return createHash("sha256").update(sessionKey).digest("hex").slice(0, 12);
}

export function syntheticIdentityFromChildKey(databasePath: string, childSessionKey: string): SyntheticOwner | undefined {
  if (!childSessionKey.includes(":subagent:cnx-")) return undefined;
  const match = /-([0-9a-f]{12})-g(\d+)-[0-9a-f]{8}$/iu.exec(childSessionKey);
  if (!match?.[1] || !match[2]) return undefined;
  const expectedHash = match[1].toLowerCase();
  const generation = Number(match[2]);
  if (!Number.isSafeInteger(generation) || generation < 0) return undefined;

  const db = openDb(databasePath);
  try {
    const sessionTable = db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_sessions'").get();
    if (!sessionTable) return undefined;
    const rows = db.prepare("SELECT session_key FROM cnx_sessions").all() as Array<{session_key:string}>;
    const owner = rows.find((row) => ownerHash(row.session_key) === expectedHash);
    return owner ? { sessionKey:owner.session_key, generation } : undefined;
  } finally { db.close(); }
}

export function recordSyntheticSpawn(databasePath: string, input: {
  runId: string;
  childSessionKey: string;
  runtimeInstance: string;
  now?: Date;
}) {
  const owner = syntheticIdentityFromChildKey(databasePath, input.childSessionKey);
  if (!owner) return false;
  const db = openDb(databasePath), stamp = (input.now ?? new Date()).toISOString();
  try {
    const current = db.prepare("SELECT state,generation FROM cnx_sessions WHERE session_key=?").get(owner.sessionKey) as
      {state:string;generation:number} | undefined;
    if (!current || current.state !== "active" || Number(current.generation) !== owner.generation) return false;
    db.prepare(`INSERT INTO cnx_synthetic_runs(
      run_id,owner_session_key,owner_generation,child_session_key,runtime_instance,state,outcome,created_at,updated_at,ended_at
    ) VALUES (?,?,?,?,?,'running',NULL,?,?,NULL)
    ON CONFLICT(run_id) DO UPDATE SET
      owner_session_key=excluded.owner_session_key,
      owner_generation=excluded.owner_generation,
      child_session_key=excluded.child_session_key,
      runtime_instance=excluded.runtime_instance,
      state='running',outcome=NULL,updated_at=excluded.updated_at,ended_at=NULL`)
      .run(input.runId, owner.sessionKey, owner.generation, input.childSessionKey, input.runtimeInstance, stamp, stamp);
    return true;
  } finally { db.close(); }
}

export function settleSyntheticRun(databasePath: string, input: {
  runId?: string;
  childSessionKey?: string;
  state?: "done" | "cancelled";
  outcome?: string;
  now?: Date;
}) {
  if (!input.runId && !input.childSessionKey) return 0;
  const db = openDb(databasePath), stamp = (input.now ?? new Date()).toISOString();
  try {
    if (input.runId) {
      return Number(db.prepare(`UPDATE cnx_synthetic_runs SET state=?,outcome=?,updated_at=?,ended_at=?
        WHERE run_id=? AND state='running'`).run(input.state ?? "done", input.outcome ?? null, stamp, stamp, input.runId).changes);
    }
    return Number(db.prepare(`UPDATE cnx_synthetic_runs SET state=?,outcome=?,updated_at=?,ended_at=?
      WHERE child_session_key=? AND state='running'`).run(input.state ?? "done", input.outcome ?? null, stamp, stamp, input.childSessionKey!).changes);
  } finally { db.close(); }
}

export function staleSyntheticRuns(databasePath: string, runtimeInstance: string): StaleSyntheticRun[] {
  const db = openDb(databasePath);
  try {
    return (db.prepare(`SELECT run_id,owner_session_key,owner_generation,child_session_key,runtime_instance
      FROM cnx_synthetic_runs WHERE state='running' AND runtime_instance<>?
      ORDER BY created_at,run_id`).all(runtimeInstance) as Array<{
        run_id:string;
        owner_session_key:string;
        owner_generation:number;
        child_session_key:string;
        runtime_instance:string;
      }>).map((row) => ({
        runId:row.run_id,
        ownerSessionKey:row.owner_session_key,
        ownerGeneration:Number(row.owner_generation),
        childSessionKey:row.child_session_key,
        runtimeInstance:row.runtime_instance,
      }));
  } finally { db.close(); }
}

export function cancelSyntheticForSession(databasePath: string, sessionKey: string, reason: string, now = new Date()) {
  const db = openDb(databasePath), stamp = now.toISOString();
  try {
    return Number(db.prepare(`UPDATE cnx_synthetic_runs SET state='cancelled',outcome=?,updated_at=?,ended_at=?
      WHERE owner_session_key=? AND state='running'`).run(reason.slice(0,2000), stamp, stamp, sessionKey).changes);
  } finally { db.close(); }
}
