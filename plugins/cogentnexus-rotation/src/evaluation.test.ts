import { mkdtempSync,rmSync,readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach,describe,expect,it } from "vitest";
import { runPhase6Evaluation,writePhase6Report } from "./evaluation.js";

const roots:string[]=[]; afterEach(()=>{while(roots.length)rmSync(roots.pop()!,{recursive:true,force:true});});
describe("Phase 6 evaluation",()=>{
  it("passes interruption, retry, duplication, retrieval, and evidence gates",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-phase6-"));roots.push(root); const report=runPhase6Evaluation(join(root,"evaluation.sqlite3"),new Date("2026-08-13T00:00:00Z"));
    expect(report.passed).toBe(true); expect(Object.values(report.gates).every(Boolean)).toBe(true);
    expect(report.interruption).toEqual({recovered:true,generationAdvanced:true,completedOnce:true});
    expect(report.retry).toEqual({bounded:true,attempts:2,completed:true}); expect(report.duplication).toEqual({duplicateDetected:true,ticketCount:1,sideEffectCount:1});
    expect(report.retrieval).toMatchObject({cases:12,recallAt3:1,provenanceCoverage:1});
    expect(report.decisions.semanticRetrieval.enable).toBe(false);
    expect(report.decisions.postgresAdapter.enable).toBe(
      report.database.ticketCount>report.decisions.postgresAdapter.thresholds.maximumTicketCount ||
      report.database.writeP95LatencyMs>report.decisions.postgresAdapter.thresholds.maximumWriteP95LatencyMs,
    );
    expect(report.evidenceSha256).toMatch(/^[a-f0-9]{64}$/);
    const path=writePhase6Report(report,join(root,"report.json")); expect(JSON.parse(readFileSync(path,"utf8"))).toEqual(report);
  });
});
