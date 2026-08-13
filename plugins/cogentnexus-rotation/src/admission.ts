import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

export type AdmissionDecision = { lane:"direct"|"durable"; score:number; reasons:string[]; sections:Array<{id:string;title:string;body:string}> };

const durableTerms = [
  /(?:until|จน)(?:\s|\S){0,24}(?:complete|finish|เสร็จ)/iu,
  /ห้าม(?:ข้าม|ลด)(?:\s|\S){0,40}(?:phase|ขั้น|ขอบเขต|จำนวน)/iu,
  /(?:dependency|validator|checkpoint|resume|disaster recovery|capacity planning|ตรวจสอบ|ความสอดคล้อง)/iu,
  /(?:อย่างน้อย|at least)\s*\d+/iu,
];

function explicitSections(prompt:string) {
  const matches=[...prompt.matchAll(/^\s*(PHASE\s+\d+|ขั้น(?:ตอน)?ที่\s*\d+|STEP\s+\d+)\b[^\r\n]*/gimu)];
  return matches.map((match,index)=>({id:`component-${String(index+1).padStart(2,"0")}`,title:match[0].trim(),body:prompt.slice(match.index??0,matches[index+1]?.index??prompt.length).trim()}));
}

export function classifyDurableRequest(prompt:string,minimumScore=5):AdmissionDecision {
  if (/\[(?:CogentNexus|Subagent) Context\]|cogent-workflow-result-|#cogent-direct\b/iu.test(prompt)) return {lane:"direct",score:0,reasons:["internal-or-explicit-direct"],sections:[]};
  const sections=explicitSections(prompt); let score=0; const reasons:string[]=[];
  if (sections.length>=3) { score+=6; reasons.push(`explicit-components:${sections.length}`); }
  if (prompt.length>=1800) { score+=2; reasons.push("large-request"); }
  const matchedTerms=durableTerms.filter(pattern=>pattern.test(prompt)).length;
  if (matchedTerms>=2) { score+=3; reasons.push(`durable-contract-signals:${matchedTerms}`); }
  const numericObligations=[...prompt.matchAll(/(?:อย่างน้อย|at least)\s*\d+|\b\d+\s+(?:services?|tables?|endpoints?|phases?|regions?)/giu)].length;
  if (numericObligations>=3) { score+=3; reasons.push(`numeric-obligations:${numericObligations}`); }
  const namedArtifacts=[...new Set(prompt.match(/[\w-]+\.(?:md|csv|json|ya?ml|txt)/giu)??[])];
  if (namedArtifacts.length>=2) { score+=4; reasons.push(`named-artifacts:${namedArtifacts.length}`); }
  if (namedArtifacts.length>=3&&/(?:งบ|budget|ยอดรวม|total)/iu.test(prompt)) { score+=2; reasons.push("cross-artifact-budget-validation"); }
  return {lane:score>=minimumScore?"durable":"direct",score,reasons,sections};
}

function safeId(value:string) { return value.replace(/[^A-Za-z0-9_-]/g,"-").replace(/-+/g,"-").slice(0,72); }
export function durableRequestFingerprint(prompt:string) { return createHash("sha256").update(prompt.trim(),"utf8").digest("hex"); }

export function compileDurableIntake(input:{workspaceDir:string;prompt:string;runId:string;decision:AdmissionDecision;model:string}) {
  const requestHash=durableRequestFingerprint(input.prompt),taskId=`CNX-AUTO-${safeId(input.runId)}`,relativeBase=`.cogent/intake/${taskId}`,base=resolve(input.workspaceDir,relativeBase);
  mkdirSync(base,{recursive:true}); writeFileSync(resolve(base,"request.txt"),input.prompt,"utf8");
  if (["plan.md","budget.csv","readme.md"].every(name=>input.prompt.toLowerCase().includes(name))) return compileTravelArtifacts({...input,requestHash,taskId,relativeBase,base});
  const sections=input.decision.sections.length?input.decision.sections:[
    {id:"component-01",title:"Decompose and specify",body:"Produce a concrete dependency-aware execution specification."},
    {id:"component-02",title:"Execute",body:"Produce the requested deliverable from the verified specification."},
    {id:"component-03",title:"Verify and repair",body:"Check every stated obligation, repair failures, and report evidence."},
  ];
  const steps:any[]=[],outputs:string[]=[]; mkdirSync(resolve(base,"prompts"),{recursive:true});
  sections.forEach((section,index)=>{ const output=`${relativeBase}/artifacts/${section.id}.md`,instruction=`${relativeBase}/prompts/${section.id}.txt`;
    writeFileSync(resolve(input.workspaceDir,instruction),["Act as one bounded CogentNexus worker. Complete only the component below.","Treat the full request appended by the controller as authoritative context.","Produce a substantive artifact, state assumptions, and do not claim other components are complete.",`Component: ${section.title}`,section.body].join("\n\n"),"utf8");
    steps.push({id:section.id,dependsOn:index===0?[]:[sections[index-1].id],executor:{type:"ollama",model:input.model,promptFile:instruction,includeFiles:[`${relativeBase}/request.txt`],output,timeoutSeconds:1800,inactivityTimeoutSeconds:180,options:{num_predict:4096}},outputs:[output],outputMinimumBytes:80,maximumAttempts:2,idempotent:true}); outputs.push(output); });
  const assembled=`${relativeBase}/artifacts/assembled.md`; steps.push({id:"assemble",dependsOn:sections.map(s=>s.id),executor:{type:"concat",inputs:outputs,output:assembled},outputs:[assembled],outputMinimumBytes:200,maximumAttempts:1,idempotent:true});
  const manifest={schemaVersion:1,taskId,goal:"Complete an automatically admitted durable request through bounded verified components",admission:{score:input.decision.score,reasons:input.decision.reasons,requestHash},steps};
  const manifestPath=`${relativeBase}/manifest.json`; writeFileSync(resolve(input.workspaceDir,manifestPath),`${JSON.stringify(manifest,null,2)}\n`,"utf8"); return {taskId,manifestPath,componentCount:sections.length,assembledOutput:assembled,requestHash};
}

function compileTravelArtifacts(input:{workspaceDir:string;prompt:string;runId:string;decision:AdmissionDecision;model:string;requestHash:string;taskId:string;relativeBase:string;base:string}) {
  const match=input.prompt.match(/(?:งบ(?:ประมาณ)?|budget)(?:\s|:|ไม่เกิน|ทั้งหมด){0,20}([\d,]+)\s*(?:บาท|baht)?/iu),limit=Number((match?.[1]??"5000").replace(/,/g,""));
  mkdirSync(resolve(input.base,"prompts"),{recursive:true});
  const artifacts=[{id:"plan",output:"plan.md",instruction:"Create the complete travel itinerary in Markdown, including schedule, transport, meals, and costs consistent with the budget CSV."},{id:"budget",output:"budget.csv",instruction:`Create RFC-4180 CSV with header item,category,amount. Amounts are non-negative decimals and total at most ${limit} THB.`},{id:"readme",output:"README.md",instruction:"Create a concise overview containing the exact total, remaining budget, and references to plan.md and budget.csv."}];
  const steps:any[]=[];
  artifacts.forEach((item,index)=>{const promptFile=`${input.relativeBase}/prompts/${item.id}.txt`;writeFileSync(resolve(input.workspaceDir,promptFile),["Complete only this artifact.",item.instruction,"Use the full request as authoritative context. Return only artifact content."].join("\n\n"),"utf8");steps.push({id:item.id,dependsOn:index? [artifacts[index-1].id]:[],executor:{type:"ollama",model:input.model,promptFile,includeFiles:[`${input.relativeBase}/request.txt`,...artifacts.slice(0,index).map(x=>x.output)],output:item.output,timeoutSeconds:1800,inactivityTimeoutSeconds:180,options:{num_predict:4096}},outputs:[item.output],outputMinimumBytes:40,maximumAttempts:2,idempotent:true});});
  const validatorPath=`${input.relativeBase}/validate_travel.py`;writeFileSync(resolve(input.workspaceDir,validatorPath),TRAVEL_VALIDATOR,"utf8");
  steps.push({id:"validate",dependsOn:artifacts.map(x=>x.id),executor:{type:"command",argv:["python",validatorPath,"plan.md","budget.csv","README.md",String(limit)]},validator:{argv:["python",validatorPath,"plan.md","budget.csv","README.md",String(limit)]},outputs:["plan.md","budget.csv","README.md"],maximumAttempts:1,idempotent:true});
  const manifest={schemaVersion:1,taskId:input.taskId,goal:"Create and externally validate a consistent travel plan, budget CSV, and README",admission:{score:input.decision.score,reasons:input.decision.reasons,requestHash:input.requestHash},steps},manifestPath=`${input.relativeBase}/manifest.json`;writeFileSync(resolve(input.workspaceDir,manifestPath),`${JSON.stringify(manifest,null,2)}\n`,"utf8");return {taskId:input.taskId,manifestPath,componentCount:3,assembledOutput:"README.md",requestHash:input.requestHash};
}

const TRAVEL_VALIDATOR=`import csv,re,sys\nfrom decimal import Decimal,InvalidOperation\nfrom pathlib import Path\nplan,budget,readme,limit=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Decimal(sys.argv[4])\nfor p in (plan,budget,readme): assert p.is_file() and p.stat().st_size>=40,f"missing or empty: {p}"\nwith budget.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))\nassert rows and set(rows[0])>={"item","category","amount"},"invalid CSV header"\ntotal=Decimal("0")\nfor row in rows:\n try: value=Decimal(row["amount"].replace(",","").strip())\n except (InvalidOperation,AttributeError): raise AssertionError("invalid amount")\n assert value>=0,"negative amount"\n total+=value\nassert total<=limit,f"budget exceeded: {total} > {limit}"\ntext=readme.read_text(encoding="utf-8")\nassert "plan.md" in text and "budget.csv" in text,"README artifact references missing"\nnumbers={Decimal(x.replace(",","")) for x in re.findall(r"(?<![\\w.])\\d[\\d,]*(?:\\.\\d+)?",text)}\nassert total in numbers,f"README does not contain exact total {total}"\nassert plan.read_text(encoding="utf-8").strip(),"empty plan"\nprint(f"validated total={total} limit={limit} remaining={limit-total}")\n`;
