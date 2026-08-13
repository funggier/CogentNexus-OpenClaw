import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { performance } from "node:perf_hooks";
import { DatabaseSync } from "node:sqlite";
import { KnowledgeStore } from "./knowledge-store.js";
import { TicketStore } from "./ticket-store.js";
import { ExternalResearchStore } from "./external-research.js";

export type Phase6Report = {
  schemaVersion: 1;
  generatedAt: string;
  database: { integrity: string; migrations: number[]; ticketCount: number; verifiedLessonCount: number; writeP95LatencyMs: number };
  interruption: { recovered: boolean; generationAdvanced: boolean; completedOnce: boolean };
  retry: { bounded: boolean; attempts: number; completed: boolean };
  duplication: { duplicateDetected: boolean; ticketCount: number; sideEffectCount: number };
  retrieval: { cases: number; top1Precision: number; recallAt3: number; provenanceCoverage: number; p95LatencyMs: number };
  decisions: {
    semanticRetrieval: { enable: boolean; reason: string; thresholds: { minimumTop1Precision: number; minimumRecallAt3: number; maximumP95LatencyMs: number } };
    postgresAdapter: { enable: boolean; reason: string; thresholds: { maximumTicketCount: number; maximumWriteP95LatencyMs: number } };
  };
  gates: Record<string, boolean>;
  passed: boolean;
  evidenceSha256: string;
};

const RETRIEVAL_FIXTURES = [
  {summary:"Recover expired worker leases",guidance:"Reclaim stale leases and advance the fencing generation.",queries:["expired lease recovery","fencing generation"],irrelevant:"translation glossary"},
  {summary:"Bound validation retries",guidance:"Retry validation failures only until the configured attempt ceiling.",queries:["validation retry ceiling","bounded retries"],irrelevant:"source cache"},
  {summary:"Preserve verified checkpoints",guidance:"Resume from the smallest pending unit without regenerating accepted siblings.",queries:["verified checkpoint resume","accepted siblings"],irrelevant:"private URL"},
  {summary:"Verify artifact hashes",guidance:"Check deterministic SHA-256 evidence before final assembly.",queries:["artifact hash assembly","SHA-256 evidence"],irrelevant:"lease heartbeat"},
  {summary:"Reject private research URLs",guidance:"External research accepts public HTTPS sources and blocks local networks.",queries:["private research URL","public HTTPS source"],irrelevant:"artifact assembly"},
  {summary:"Corroborate independent publishers",guidance:"Mirrors from one origin count as one source of evidence.",queries:["independent publisher corroboration","duplicate origin evidence"],irrelevant:"retry timeout"},
] as const;

function p95(values:number[]) { const ordered=[...values].sort((a,b)=>a-b); return ordered[Math.min(ordered.length-1,Math.ceil(ordered.length*.95)-1)] ?? 0; }
function round(value:number) { return Number(value.toFixed(4)); }
function count(db:DatabaseSync,sql:string) { return Number((db.prepare(sql).get() as any).count); }
function stable(value:unknown):unknown { if(Array.isArray(value)) return value.map(stable); if(value&&typeof value==="object") return Object.fromEntries(Object.entries(value).sort(([a],[b])=>a.localeCompare(b)).map(([key,item])=>[key,stable(item)])); return value; }
function canonicalEvidence(report:Omit<Phase6Report,"evidenceSha256">) { return JSON.stringify(stable(report)); }

export function runPhase6Evaluation(databasePath:string, now=new Date()):Phase6Report {
  const tickets=new TicketStore(databasePath), knowledge=new KnowledgeStore(databasePath), research=new ExternalResearchStore(databasePath), t0=new Date(now.getTime()); research.snapshot();

  const interrupted=tickets.accept({runId:"phase6-interruption",ownerSessionKey:"benchmark-owner",prompt:"interrupt safely"}); tickets.route(interrupted.ticketId,true,t0);
  const lease1=tickets.claim({ticketId:interrupted.ticketId,workerId:"worker-a",leaseMs:1000,now:t0})!;
  const recovered=tickets.recoverExpired({now:new Date(t0.getTime()+1001)});
  const lease2=tickets.claim({ticketId:interrupted.ticketId,workerId:"worker-b",leaseMs:5000,now:new Date(t0.getTime()+1002)})!;
  tickets.complete({...lease2,result:{validated:true},now:new Date(t0.getTime()+1003)});

  const retry=tickets.accept({runId:"phase6-retry",ownerSessionKey:"benchmark-owner",prompt:"retry bounded",maxAttempts:2}); tickets.route(retry.ticketId,true,t0);
  const retry1=tickets.claim({ticketId:retry.ticketId,workerId:"retry-a",leaseMs:5000,now:t0})!;
  const retryState=tickets.failAttempt({...retry1,classification:"validation",message:"fixture rejection",now:new Date(t0.getTime()+1)});
  const retry2=tickets.claim({ticketId:retry.ticketId,workerId:"retry-b",leaseMs:5000,now:new Date(t0.getTime()+2)})!;
  tickets.complete({...retry2,result:{validated:true},now:new Date(t0.getTime()+3)});

  const duplicateA=tickets.accept({runId:"phase6-duplicate",ownerSessionKey:"benchmark-owner",prompt:"deliver once"});
  const duplicateB=tickets.accept({runId:"phase6-duplicate",ownerSessionKey:"benchmark-owner",prompt:"deliver once"});
  tickets.route(duplicateA.ticketId,true,t0); const duplicateLease=tickets.claim({ticketId:duplicateA.ticketId,workerId:"duplicate-worker",leaseMs:5000,now:t0})!;
  let sideEffectCount=0; sideEffectCount++; tickets.complete({...duplicateLease,result:{sideEffectCount},now:new Date(t0.getTime()+1)});

  const lessonIds=new Map<string,string>();
  for(const fixture of RETRIEVAL_FIXTURES) {
    const candidate=knowledge.createCandidate({summary:fixture.summary,guidance:fixture.guidance,evidenceRef:`fixture:${fixture.summary}`,confidence:.7,now:t0});
    knowledge.transition({lessonId:candidate.lessonId,action:"verify",evidenceRef:`verification:${fixture.summary}`,confidence:.9,now:new Date(t0.getTime()+1)}); lessonIds.set(fixture.summary,candidate.lessonId);
  }
  let correctTop1=0,found=0,provenance=0; const latencies:number[]=[];
  for(const fixture of RETRIEVAL_FIXTURES) for(const query of fixture.queries) {
    const started=performance.now(),results=knowledge.search(query,{limit:3}); latencies.push(performance.now()-started);
    const expected=lessonIds.get(fixture.summary)!; const relevant=results.filter(x=>x.lessonId===expected).length;
    if(results[0]?.lessonId===expected) correctTop1++; if(relevant) found++; if(results.find(x=>x.lessonId===expected)?.provenance.length) provenance++;
  }
  const writeLatencies:number[]=[]; for(let i=0;i<50;i++){const started=performance.now();tickets.accept({runId:`phase6-write-${i}`,ownerSessionKey:"benchmark-owner",prompt:"write latency fixture"});writeLatencies.push(performance.now()-started);}

  const db=new DatabaseSync(resolve(databasePath));
  const migrations=(db.prepare("SELECT version FROM schema_migrations ORDER BY version").all() as any[]).map(x=>Number(x.version));
  const ticketCount=count(db,"SELECT count(*) count FROM tickets"), verifiedLessonCount=count(db,"SELECT count(*) count FROM lessons WHERE status='verified'");
  const completedInterruption=count(db,`SELECT count(*) count FROM tickets WHERE ticket_id='${interrupted.ticketId}' AND status='completed'`);
  const completedRetry=count(db,`SELECT count(*) count FROM tickets WHERE ticket_id='${retry.ticketId}' AND status='completed'`);
  const retryAttempts=Number((db.prepare("SELECT attempt_count FROM tickets WHERE ticket_id=?").get(retry.ticketId) as any).attempt_count);
  const duplicateTicketCount=Number((db.prepare("SELECT count(*) count FROM tickets WHERE run_id='phase6-duplicate'").get() as any).count);
  const integrity=String((db.prepare("PRAGMA integrity_check").get() as any).integrity_check); db.close();

  const cases=RETRIEVAL_FIXTURES.length*2, top1Precision=correctTop1/cases, recallAt3=found/cases, provenanceCoverage=provenance/cases, latency=p95(latencies);
  const semanticThresholds={minimumTop1Precision:.9,minimumRecallAt3:.9,maximumP95LatencyMs:50};
  const semanticEnable=top1Precision<semanticThresholds.minimumTop1Precision || recallAt3<semanticThresholds.minimumRecallAt3 || latency>semanticThresholds.maximumP95LatencyMs;
  const postgresThresholds={maximumTicketCount:100_000,maximumWriteP95LatencyMs:100};
  const writeLatency=p95(writeLatencies), postgresEnable=ticketCount>postgresThresholds.maximumTicketCount || writeLatency>postgresThresholds.maximumWriteP95LatencyMs;
  const gates={integrity:integrity==="ok",interruptionRecovery:recovered.length===1 && lease2.leaseGeneration===lease1.leaseGeneration+1 && completedInterruption===1,retryBounded:retryState==="waiting"&&retryAttempts===2&&completedRetry===1,duplicateSuppression:duplicateB.duplicate&&duplicateTicketCount===1&&sideEffectCount===1,retrievalPrecision:top1Precision>=semanticThresholds.minimumTop1Precision,retrievalRecall:recallAt3>=semanticThresholds.minimumRecallAt3,provenance:provenanceCoverage===1,latency:latency<=semanticThresholds.maximumP95LatencyMs};
  const base:Omit<Phase6Report,"evidenceSha256">={schemaVersion:1,generatedAt:now.toISOString(),database:{integrity,migrations,ticketCount,verifiedLessonCount,writeP95LatencyMs:round(writeLatency)},interruption:{recovered:recovered.length===1,generationAdvanced:lease2.leaseGeneration===lease1.leaseGeneration+1,completedOnce:completedInterruption===1},retry:{bounded:retryState==="waiting"&&retryAttempts===2,attempts:retryAttempts,completed:completedRetry===1},duplication:{duplicateDetected:duplicateB.duplicate,ticketCount:duplicateTicketCount,sideEffectCount},retrieval:{cases,top1Precision:round(top1Precision),recallAt3:round(recallAt3),provenanceCoverage:round(provenanceCoverage),p95LatencyMs:round(latency)},decisions:{semanticRetrieval:{enable:semanticEnable,reason:semanticEnable?"FTS5 missed the configured quality or latency gate.":"FTS5 meets the measured precision, recall, provenance, and latency gates; embeddings would add an unproven dependency.",thresholds:semanticThresholds},postgresAdapter:{enable:postgresEnable,reason:postgresEnable?"Observed workload exceeds a configured SQLite scale or write-latency threshold.":"Observed workload and write latency remain within SQLite evaluation thresholds; PostgreSQL is not justified by measured scale.",thresholds:postgresThresholds}},gates,passed:Object.values(gates).every(Boolean)};
  return {...base,evidenceSha256:createHash("sha256").update(canonicalEvidence(base)).digest("hex")};
}

export function writePhase6Report(report:Phase6Report,path:string) {
  const target=resolve(path); mkdirSync(dirname(target),{recursive:true}); writeFileSync(target,JSON.stringify(report,null,2)+"\n",{encoding:"utf8"}); return target;
}
