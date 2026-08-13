import { createHash, randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";

export type ResearchStatus = "queued" | "running" | "completed" | "blocked" | "failed" | "cancelled";
export type SourceType = "official" | "primary" | "standard" | "research" | "maintainer" | "secondary";
export type ClaimRelation = "supports" | "contradicts" | "mentions";

export type ResearchPolicy = {
  maximumQueries: number;
  maximumSources: number;
  maximumBytesPerSource: number;
  timeoutMs: number;
  freshnessSeconds: number;
  minimumIndependentSources: number;
};

export type SearchResult = { url: string; title?: string; publisher?: string; sourceType?: SourceType; publishedAt?: string };
export type SearchFetchAdapter = {
  search(query: string, limit: number, signal: AbortSignal): Promise<SearchResult[]>;
  fetch(url: string, maximumBytes: number, signal: AbortSignal): Promise<{ body: string; contentType?: string; publishedAt?: string }>;
};

const RESEARCH_SCHEMA = `
CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS research_jobs (
  job_id TEXT PRIMARY KEY, ticket_id TEXT, status TEXT NOT NULL CHECK(status IN ('queued','running','completed','blocked','failed','cancelled')),
  question TEXT NOT NULL, reason TEXT NOT NULL, scope_json TEXT NOT NULL, policy_json TEXT NOT NULL,
  query_count INTEGER NOT NULL DEFAULT 0, source_count INTEGER NOT NULL DEFAULT 0,
  last_error TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, completed_at TEXT
);
CREATE TABLE IF NOT EXISTS research_queries (
  query_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES research_jobs(job_id) ON DELETE CASCADE,
  query_text TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS research_sources (
  source_id TEXT PRIMARY KEY, canonical_url TEXT NOT NULL UNIQUE, publisher TEXT, source_type TEXT NOT NULL,
  origin_key TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source_snapshots (
  snapshot_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES research_sources(source_id) ON DELETE CASCADE,
  content_hash TEXT NOT NULL, excerpt TEXT NOT NULL, content_type TEXT, published_at TEXT, accessed_at TEXT NOT NULL,
  expires_at TEXT NOT NULL, UNIQUE(source_id,content_hash)
);
CREATE INDEX IF NOT EXISTS idx_source_snapshots_cache ON source_snapshots(source_id,expires_at);
CREATE TABLE IF NOT EXISTS external_observations (
  observation_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES research_jobs(job_id) ON DELETE CASCADE,
  snapshot_id TEXT NOT NULL REFERENCES source_snapshots(snapshot_id), query_id TEXT REFERENCES research_queries(query_id),
  created_at TEXT NOT NULL, UNIQUE(job_id,snapshot_id)
);
CREATE TABLE IF NOT EXISTS research_claims (
  claim_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES research_jobs(job_id) ON DELETE CASCADE,
  claim_text TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('observed','corroborated','contradicted')),
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS claim_evidence (
  claim_id TEXT NOT NULL REFERENCES research_claims(claim_id) ON DELETE CASCADE,
  observation_id TEXT NOT NULL REFERENCES external_observations(observation_id) ON DELETE CASCADE,
  relation TEXT NOT NULL CHECK(relation IN ('supports','contradicts','mentions')),
  PRIMARY KEY(claim_id,observation_id)
);
`;

const DEFAULT_POLICY: ResearchPolicy = { maximumQueries: 3, maximumSources: 6, maximumBytesPerSource: 512_000, timeoutMs: 30_000, freshnessSeconds: 86_400, minimumIndependentSources: 2 };
const SECRET_PATTERN = /(?:api[_-]?key|authorization|bearer|password|passwd|secret|token|cookie|session[_-]?key)\s*[:=]\s*\S+/iu;
const INJECTION_PATTERN = /(?:ignore\s+(?:all\s+)?previous|system\s+prompt|developer\s+message|tool\s+call|execute\s+(?:this|the)|override\s+(?:policy|instructions))/iu;

function text(value: string, name: string, maximum = 4000) {
  const clean = value.normalize("NFKC").trim();
  if (!clean) throw new Error(`${name} is required`);
  if (SECRET_PATTERN.test(clean)) throw new Error(`${name} appears to contain a secret`);
  return clean.slice(0, maximum);
}
function boundedInteger(value: number, name: string, minimum: number, maximum: number) {
  if (!Number.isInteger(value) || value < minimum || value > maximum) throw new Error(`${name} must be between ${minimum} and ${maximum}`);
  return value;
}
function policy(input: Partial<ResearchPolicy> = {}): ResearchPolicy {
  return {
    maximumQueries: boundedInteger(input.maximumQueries ?? DEFAULT_POLICY.maximumQueries,"maximumQueries",1,10),
    maximumSources: boundedInteger(input.maximumSources ?? DEFAULT_POLICY.maximumSources,"maximumSources",1,25),
    maximumBytesPerSource: boundedInteger(input.maximumBytesPerSource ?? DEFAULT_POLICY.maximumBytesPerSource,"maximumBytesPerSource",1024,2_000_000),
    timeoutMs: boundedInteger(input.timeoutMs ?? DEFAULT_POLICY.timeoutMs,"timeoutMs",1000,120_000),
    freshnessSeconds: boundedInteger(input.freshnessSeconds ?? DEFAULT_POLICY.freshnessSeconds,"freshnessSeconds",60,31_536_000),
    minimumIndependentSources: boundedInteger(input.minimumIndependentSources ?? DEFAULT_POLICY.minimumIndependentSources,"minimumIndependentSources",1,5),
  };
}
function canonicalUrl(value: string) {
  const url = new URL(value);
  if (url.protocol !== "https:") throw new Error("research sources must use https");
  if (url.username || url.password) throw new Error("research URL must not contain credentials");
  for (const [key,value] of url.searchParams) if (/(?:api[_-]?key|access[_-]?token|secret|password|authorization)/i.test(key) || SECRET_PATTERN.test(`${key}=${value}`)) throw new Error("research URL appears to contain a secret");
  const host = url.hostname.toLowerCase().replace(/^\[|\]$/g,"");
  if (host === "localhost" || host.endsWith(".local") || /^(?:127\.|10\.|192\.168\.|169\.254\.|0\.)/.test(host) || /^172\.(?:1[6-9]|2\d|3[01])\./.test(host) || host === "::1" || /^(?:fc|fd|fe[89ab])/i.test(host)) throw new Error("private or local research URL is not allowed");
  url.hash = "";
  for (const key of [...url.searchParams.keys()]) if (/^(?:utm_|fbclid|gclid)/i.test(key)) url.searchParams.delete(key);
  url.hostname = host;
  return url.toString();
}
function safeExcerpt(body: string) {
  const clean = body.replace(/\0/g,"").replace(/\s+/g," ").trim().slice(0,12_000);
  return { excerpt: clean, injectionSuspected: INJECTION_PATTERN.test(clean) };
}
function hash(value: string) { return createHash("sha256").update(value,"utf8").digest("hex"); }
function originKey(url: string, publisher?: string) { return (publisher?.trim().toLowerCase() || new URL(url).hostname.toLowerCase()).slice(0,300); }

export class ExternalResearchStore {
  readonly databasePath: string;
  constructor(databasePath: string) { this.databasePath = resolve(databasePath); }
  private open() {
    mkdirSync(dirname(this.databasePath),{recursive:true});
    const db = new DatabaseSync(this.databasePath);
    try {
      db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
      db.exec(RESEARCH_SCHEMA);
      const now = new Date().toISOString();
      for (const version of [7,8,9]) db.prepare("INSERT OR IGNORE INTO schema_migrations(version,applied_at) VALUES (?,?)").run(version,now);
      return db;
    } catch(error) { db.close(); throw error; }
  }
  createJob(input: { ticketId?: string; question: string; reason: string; scope?: string[]; policy?: Partial<ResearchPolicy>; internalCoverage: number; internalConfidence: number; freshnessSensitive?: boolean; networkAllowed?: boolean; now?: Date }) {
    if (input.networkAllowed === false) throw new Error("external research is disabled for this request");
    if (input.internalCoverage >= .7 && input.internalConfidence >= .7 && !input.freshnessSensitive) throw new Error("external research is not justified when internal coverage and confidence are sufficient");
    const jobId=`CNXR-${randomUUID()}`, now=(input.now ?? new Date()).toISOString(), configured=policy(input.policy);
    const scope=(input.scope ?? []).map(x=>text(x,"scope",300)).slice(0,20);
    const db=this.open();
    try {
      db.prepare("INSERT INTO research_jobs(job_id,ticket_id,status,question,reason,scope_json,policy_json,created_at,updated_at) VALUES (?,?, 'queued',?,?,?,?,?,?)")
        .run(jobId,input.ticketId ?? null,text(input.question,"question"),text(input.reason,"reason",1000),JSON.stringify(scope),JSON.stringify(configured),now,now);
      return this.getJob(jobId,db);
    } finally { db.close(); }
  }
  start(jobId: string, now = new Date()) { return this.transition(jobId,"running",["queued"],undefined,now); }
  finish(jobId: string, now = new Date()) { return this.transition(jobId,"completed",["running"],undefined,now); }
  fail(jobId: string, error: string, now = new Date()) { return this.transition(jobId,"failed",["queued","running"],text(error,"error",1000),now); }
  cancel(jobId: string, reason: string, now = new Date()) { return this.transition(jobId,"cancelled",["queued","running"],text(reason,"reason",1000),now); }
  block(jobId: string, reason: string, now = new Date()) { return this.transition(jobId,"blocked",["queued","running"],text(reason,"reason",1000),now); }
  addQuery(jobId: string, query: string, now = new Date()) {
    const db=this.open(), createdAt=now.toISOString(), queryId=`CNXQ-${randomUUID()}`;
    try {
      db.exec("BEGIN IMMEDIATE"); const job=this.requireRunning(db,jobId); const configured=JSON.parse(job.policy_json) as ResearchPolicy;
      if(Number(job.query_count) >= configured.maximumQueries) throw new Error("research query budget exhausted");
      db.prepare("INSERT INTO research_queries(query_id,job_id,query_text,created_at) VALUES (?,?,?,?)").run(queryId,jobId,text(query,"query",1000),createdAt);
      db.prepare("UPDATE research_jobs SET query_count=query_count+1,updated_at=? WHERE job_id=?").run(createdAt,jobId); db.exec("COMMIT"); return {queryId,createdAt};
    } catch(error) { try{db.exec("ROLLBACK");}catch{} throw error; } finally { db.close(); }
  }
  addObservation(input: { jobId: string; queryId?: string; url: string; publisher?: string; sourceType?: SourceType; body: string; contentType?: string; publishedAt?: string; now?: Date }) {
    const db=this.open(), now=input.now ?? new Date(), accessedAt=now.toISOString();
    try {
      db.exec("BEGIN IMMEDIATE"); const job=this.requireRunning(db,input.jobId); const configured=JSON.parse(job.policy_json) as ResearchPolicy;
      if(Number(job.source_count) >= configured.maximumSources) throw new Error("research source budget exhausted");
      if(Buffer.byteLength(input.body,"utf8") > configured.maximumBytesPerSource) throw new Error("research source exceeds byte budget");
      if(input.queryId) { const query=db.prepare("SELECT 1 ok FROM research_queries WHERE query_id=? AND job_id=?").get(input.queryId,input.jobId) as any; if(!query) throw new Error("query does not belong to research job"); }
      const url=canonicalUrl(input.url), publisher=input.publisher ? text(input.publisher,"publisher",300) : undefined;
      const sourceType=input.sourceType ?? "secondary", sourceId=`CNXS-${randomUUID()}`, snapshotId=`CNXSS-${randomUUID()}`, observationId=`CNXO-${randomUUID()}`;
      const sanitized=safeExcerpt(input.body); if(sanitized.injectionSuspected) throw new Error("source contains suspected prompt injection");
      if(!sanitized.excerpt) throw new Error("source body is empty");
      const existing=db.prepare("SELECT source_id FROM research_sources WHERE canonical_url=?").get(url) as any;
      const actualSourceId=existing?.source_id ?? sourceId;
      if(!existing) db.prepare("INSERT INTO research_sources(source_id,canonical_url,publisher,source_type,origin_key,created_at) VALUES (?,?,?,?,?,?)").run(sourceId,url,publisher ?? null,sourceType,originKey(url,publisher),accessedAt);
      const contentHash=hash(sanitized.excerpt), cached=db.prepare("SELECT snapshot_id FROM source_snapshots WHERE source_id=? AND content_hash=?").get(actualSourceId,contentHash) as any;
      const actualSnapshotId=cached?.snapshot_id ?? snapshotId, expiresAt=new Date(now.getTime()+configured.freshnessSeconds*1000).toISOString();
      if(!cached) db.prepare("INSERT INTO source_snapshots(snapshot_id,source_id,content_hash,excerpt,content_type,published_at,accessed_at,expires_at) VALUES (?,?,?,?,?,?,?,?)").run(snapshotId,actualSourceId,contentHash,sanitized.excerpt,input.contentType?.slice(0,200) ?? null,input.publishedAt ?? null,accessedAt,expiresAt);
      db.prepare("INSERT OR IGNORE INTO external_observations(observation_id,job_id,snapshot_id,query_id,created_at) VALUES (?,?,?,?,?)").run(observationId,input.jobId,actualSnapshotId,input.queryId ?? null,accessedAt);
      const inserted=Number((db.prepare("SELECT changes() changes").get() as any).changes);
      if(inserted) db.prepare("UPDATE research_jobs SET source_count=source_count+1,updated_at=? WHERE job_id=?").run(accessedAt,input.jobId);
      db.exec("COMMIT"); return {observationId:inserted ? observationId : undefined,snapshotId:actualSnapshotId,contentHash,cached:Boolean(cached),expiresAt};
    } catch(error) { try{db.exec("ROLLBACK");}catch{} throw error; } finally { db.close(); }
  }
  useFreshCache(input:{jobId:string;queryId?:string;url:string;now?:Date}) {
    const db=this.open(), now=(input.now ?? new Date()).toISOString();
    try {
      db.exec("BEGIN IMMEDIATE"); const job=this.requireRunning(db,input.jobId); const configured=JSON.parse(job.policy_json) as ResearchPolicy;
      if(Number(job.source_count) >= configured.maximumSources) throw new Error("research source budget exhausted");
      if(input.queryId) { const query=db.prepare("SELECT 1 ok FROM research_queries WHERE query_id=? AND job_id=?").get(input.queryId,input.jobId) as any; if(!query) throw new Error("query does not belong to research job"); }
      const cached=db.prepare("SELECT ss.snapshot_id FROM research_sources s JOIN source_snapshots ss ON ss.source_id=s.source_id WHERE s.canonical_url=? AND ss.expires_at>? ORDER BY ss.accessed_at DESC LIMIT 1").get(canonicalUrl(input.url),now) as any;
      if(!cached) { db.exec("COMMIT"); return undefined; }
      const observationId=`CNXO-${randomUUID()}`;
      db.prepare("INSERT OR IGNORE INTO external_observations(observation_id,job_id,snapshot_id,query_id,created_at) VALUES (?,?,?,?,?)").run(observationId,input.jobId,cached.snapshot_id,input.queryId ?? null,now);
      const inserted=Number((db.prepare("SELECT changes() changes").get() as any).changes);
      if(inserted) db.prepare("UPDATE research_jobs SET source_count=source_count+1,updated_at=? WHERE job_id=?").run(now,input.jobId);
      db.exec("COMMIT"); return {observationId:inserted?observationId:undefined,snapshotId:cached.snapshot_id,cached:true};
    } catch(error) { try{db.exec("ROLLBACK");}catch{} throw error; } finally { db.close(); }
  }
  addClaim(input:{jobId:string;claim:string;evidence:Array<{observationId:string;relation:ClaimRelation}>;now?:Date}) {
    if(!input.evidence.length) throw new Error("claim requires evidence");
    const db=this.open(), now=(input.now ?? new Date()).toISOString(), claimId=`CNXC-${randomUUID()}`;
    try {
      db.exec("BEGIN IMMEDIATE"); this.requireRunning(db,input.jobId);
      const origins=new Set<string>(), relations=new Set<string>();
      for(const item of input.evidence) {
        const row=db.prepare("SELECT s.origin_key FROM external_observations o JOIN source_snapshots ss ON ss.snapshot_id=o.snapshot_id JOIN research_sources s ON s.source_id=ss.source_id WHERE o.observation_id=? AND o.job_id=?").get(item.observationId,input.jobId) as any;
        if(!row) throw new Error("claim evidence does not belong to research job"); origins.add(row.origin_key); relations.add(item.relation);
      }
      const configured=JSON.parse((db.prepare("SELECT policy_json FROM research_jobs WHERE job_id=?").get(input.jobId) as any).policy_json) as ResearchPolicy;
      const status=relations.has("contradicts") ? "contradicted" : origins.size >= configured.minimumIndependentSources && [...input.evidence].filter(x=>x.relation==="supports").length >= configured.minimumIndependentSources ? "corroborated" : "observed";
      db.prepare("INSERT INTO research_claims(claim_id,job_id,claim_text,status,created_at,updated_at) VALUES (?,?,?,?,?,?)").run(claimId,input.jobId,text(input.claim,"claim"),status,now,now);
      for(const item of input.evidence) db.prepare("INSERT INTO claim_evidence(claim_id,observation_id,relation) VALUES (?,?,?)").run(claimId,item.observationId,item.relation);
      db.exec("COMMIT"); return {claimId,status,independentOrigins:origins.size};
    } catch(error) { try{db.exec("ROLLBACK");}catch{} throw error; } finally { db.close(); }
  }
  snapshot() {
    const db=this.open(); try {
      const jobs=db.prepare("SELECT status,count(*) count FROM research_jobs GROUP BY status").all() as any[];
      return {jobs:Object.fromEntries(jobs.map(x=>[x.status,Number(x.count)])),observations:Number((db.prepare("SELECT count(*) count FROM external_observations").get() as any).count),claims:Number((db.prepare("SELECT count(*) count FROM research_claims").get() as any).count)};
    } finally { db.close(); }
  }
  get(jobId:string) { const db=this.open(); try{return this.getJob(jobId,db);}finally{db.close();} }
  private transition(jobId:string,target:ResearchStatus,allowed:ResearchStatus[],error:string|undefined,now:Date) {
    const db=this.open(), timestamp=now.toISOString(); try {
      const current=db.prepare("SELECT status FROM research_jobs WHERE job_id=?").get(jobId) as any; if(!current) throw new Error("research job not found");
      if(!allowed.includes(current.status)) throw new Error(`illegal research transition ${current.status} -> ${target}`);
      db.prepare("UPDATE research_jobs SET status=?,last_error=?,updated_at=?,completed_at=? WHERE job_id=?").run(target,error ?? null,timestamp,["completed","blocked","failed","cancelled"].includes(target)?timestamp:null,jobId);
      return this.getJob(jobId,db);
    } finally { db.close(); }
  }
  private requireRunning(db:DatabaseSync,jobId:string) { const job=db.prepare("SELECT status,policy_json,query_count,source_count FROM research_jobs WHERE job_id=?").get(jobId) as any; if(!job) throw new Error("research job not found"); if(job.status!=="running") throw new Error("research job must be running"); return job; }
  private getJob(jobId:string,db:DatabaseSync) { const row=db.prepare("SELECT * FROM research_jobs WHERE job_id=?").get(jobId) as any; if(!row) throw new Error("research job not found"); return {jobId:row.job_id,ticketId:row.ticket_id,status:row.status,question:row.question,reason:row.reason,scope:JSON.parse(row.scope_json),policy:JSON.parse(row.policy_json),queryCount:Number(row.query_count),sourceCount:Number(row.source_count),lastError:row.last_error,createdAt:row.created_at,updatedAt:row.updated_at,completedAt:row.completed_at}; }
}

export async function runBoundedResearch(input:{store:ExternalResearchStore;jobId:string;queries:string[];adapter:SearchFetchAdapter}) {
  const job=input.store.start(input.jobId), controller=new AbortController(), timer=setTimeout(()=>controller.abort(),job.policy.timeoutMs);
  try {
    for(const query of input.queries.slice(0,job.policy.maximumQueries)) {
      const saved=input.store.addQuery(input.jobId,query), results=await input.adapter.search(query,job.policy.maximumSources-job.sourceCount,controller.signal);
      for(const result of results.slice(0,job.policy.maximumSources)) {
        if(input.store.get(input.jobId).sourceCount>=job.policy.maximumSources) break;
        const cached=input.store.useFreshCache({jobId:input.jobId,queryId:saved.queryId,url:result.url});
        if(cached) continue;
        const fetched=await input.adapter.fetch(canonicalUrl(result.url),job.policy.maximumBytesPerSource,controller.signal);
        input.store.addObservation({jobId:input.jobId,queryId:saved.queryId,url:result.url,publisher:result.publisher,sourceType:result.sourceType,body:fetched.body,contentType:fetched.contentType,publishedAt:fetched.publishedAt ?? result.publishedAt});
      }
    }
    return input.store.finish(input.jobId);
  } catch(error) { input.store.fail(input.jobId,error instanceof Error ? error.message : String(error)); throw error; }
  finally { clearTimeout(timer); }
}
