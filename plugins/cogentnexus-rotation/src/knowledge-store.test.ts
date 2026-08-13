import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";
import { KnowledgeStore } from "./knowledge-store.js";

const roots:string[] = [];
function fixture() {
  const root = mkdtempSync(join(tmpdir(),"cnx-knowledge-")); roots.push(root);
  return {root,path:join(root,"cogentnexus.sqlite3"),store:new KnowledgeStore(join(root,"cogentnexus.sqlite3"))};
}
afterEach(() => { while (roots.length) rmSync(roots.pop()!,{recursive:true,force:true}); });

describe("KnowledgeStore", () => {
  it("records evidence-backed execution experience", () => {
    const {store,path}=fixture();
    const saved=store.recordExperience({ticketId:"T-1",kind:"failure",summary:"validator rejected an invalid artifact",evidenceRef:"ticket:T-1/event:7",outcome:{classification:"validation"}});
    expect(saved.experienceId).toMatch(/^CNXE-/);
    expect(store.snapshot()).toMatchObject({experiences:{failure:1},lessons:{},applications:{}});
    const db=new DatabaseSync(path,{readOnly:true});
    expect(db.prepare("SELECT ticket_id,kind,evidence_ref FROM experiences").get()).toEqual({ticket_id:"T-1",kind:"failure",evidence_ref:"ticket:T-1/event:7"}); db.close();
  });

  it("keeps candidates out of normal retrieval until independently verified", () => {
    const {store}=fixture();
    const lesson=store.createCandidate({summary:"Validate hashes before assembly",guidance:"Run the deterministic hash gate before integration.",evidenceRef:"ticket:T-1/event:9",confidence:0.6});
    expect(lesson).toMatchObject({status:"hypothesis",confidence:0.6});
    expect(store.search("hash assembly")).toEqual([]);
    expect(()=>store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"ticket:T-1/event:9"})).toThrow("new independent evidence");
    expect(store.search("hash assembly")).toEqual([]);
    const verified=store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"benchmark:tamper-test"});
    expect(verified.status).toBe("verified");
    expect(verified.confidence).toBeGreaterThanOrEqual(0.75);
    expect(store.search("hash assembly")[0]).toMatchObject({lessonId:lesson.lessonId,status:"verified"});
    expect(store.search("hash assembly")[0].provenance).toHaveLength(2);
  });

  it("contradicts and retires lessons without returning unsafe stale guidance", () => {
    const {store}=fixture();
    const lesson=store.createCandidate({summary:"Retry every failure",guidance:"Always retry.",evidenceRef:"ticket:T-1/event:1"});
    store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"test:initial"});
    expect(store.search("retry failure")).toHaveLength(1);
    const contradicted=store.transition({lessonId:lesson.lessonId,action:"contradict",evidenceRef:"test:authorization-is-terminal"});
    expect(contradicted).toMatchObject({status:"contradicted",confidence:0.25});
    expect(store.search("retry failure")).toEqual([]);
    const retired=store.transition({lessonId:lesson.lessonId,action:"retire",evidenceRef:"review:obsolete"});
    expect(retired).toMatchObject({status:"retired",confidence:0});
    expect(()=>store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"invalid"})).toThrow("retired lesson is terminal");
  });

  it("records applications only for verified lessons", () => {
    const {store}=fixture();
    const lesson=store.createCandidate({summary:"Bound retries",guidance:"Stop after the configured ceiling.",evidenceRef:"ticket:T-2/event:3"});
    expect(()=>store.recordApplication({lessonId:lesson.lessonId,ticketId:"T-3",outcome:"success",evidenceRef:"ticket:T-3/event:8"})).toThrow("only verified lessons");
    store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"test:retry-ceiling"});
    expect(store.recordApplication({lessonId:lesson.lessonId,ticketId:"T-3",outcome:"success",evidenceRef:"ticket:T-3/event:8"}).applicationId).toMatch(/^CNXA-/);
    expect(store.snapshot().applications).toEqual({success:1});
  });

  it("reopens the same database idempotently and preserves FTS retrieval", () => {
    const {store,path}=fixture();
    const lesson=store.createCandidate({summary:"Preserve verified checkpoints",guidance:"Resume from the smallest pending step.",evidenceRef:"workflow:WF-1/revision:4"});
    store.transition({lessonId:lesson.lessonId,action:"verify",evidenceRef:"test:restart"});
    const reopened=new KnowledgeStore(path);
    expect(reopened.search("verified checkpoints")[0].lessonId).toBe(lesson.lessonId);
    const db=new DatabaseSync(path,{readOnly:true});
    expect((db.prepare("SELECT version FROM schema_migrations ORDER BY version").all() as any[]).map(x=>x.version)).toEqual([5,6]);
    db.close();
  });
});
