import { mkdtempSync,rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join,resolve } from "node:path";
import { runPhase6Evaluation,writePhase6Report } from "../dist/evaluation.js";

const root=mkdtempSync(join(tmpdir(),"cogentnexus-phase6-"));
try {
  const report=runPhase6Evaluation(join(root,"evaluation.sqlite3"));
  if(process.argv[2]) writePhase6Report(report,resolve(process.argv[2]));
  process.stdout.write(`${JSON.stringify(report,null,2)}\n`);
  if(!report.passed) process.exitCode=1;
} finally { rmSync(root,{recursive:true,force:true}); }
