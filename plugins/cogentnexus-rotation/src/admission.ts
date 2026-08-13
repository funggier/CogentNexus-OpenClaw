import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, resolve } from "node:path";

export type WorkDomain="software"|"trading"|"files"|"analysis"|"fiction"|"design"|"translation"|"general";
export type AdmissionDecision={lane:"direct"|"durable";score:number;reasons:string[];sections:Array<{id:string;title:string;body:string}>;domain:WorkDomain};

const durableTerms=[
  /(?:until|จน)(?:\s|\S){0,24}(?:complete|finish|เสร็จ)/iu,
  /(?:ห้ามข้าม|ห้ามลด)(?:\s|\S){0,40}(?:phase|ขั้น|ขอบเขต|จำนวน)/iu,
  /(?:dependency|validator|checkpoint|resume|disaster recovery|capacity planning|ตรวจสอบ|ความสอดคล้อง|ทดสอบ)/iu,
  /(?:อย่างน้อย|at least)\s*\d+/iu,
];
const domains:Array<[WorkDomain,RegExp]>=[
  ["trading",/(?:\bEA\b|expert advisor|MetaTrader|MQL[45]?|trading bot|backtest|กลยุทธ์เทรด|ระบบเทรด|เทรดเดอร์)/iu],
  ["translation",/(?:แปลภาษา|งานแปล|แปล(?:จาก|เป็น|เอกสาร|บทความ|นิยาย)|translation|translate|locali[sz]ation|subtitle|คำบรรยาย)/iu],
  ["software",/(?:program|software|system|application|website|API|database|code|โปรแกรม|ซอฟต์แวร์|ทำระบบ|เว็บไซต์|แอป|ฐานข้อมูล|เขียนโค้ด)/iu],
  ["files",/(?:จัดการไฟล์|ย้ายไฟล์|เปลี่ยนชื่อไฟล์|จัดระเบียบไฟล์|convert files?|rename files?|organize files?|file management)/iu],
  ["analysis",/(?:วิเคราะห์|analysis|dataset|ข้อมูล|สถิติ|รายงาน|research|compare|เปรียบเทียบ)/iu],
  ["fiction",/(?:นิยาย|เรื่องสั้น|บท|ตัวละคร|พล็อต|novel|fiction|short story|screenplay)/iu],
  ["design",/(?:ออกแบบ|design|UI|UX|wireframe|mockup|logo|ภาพ|illustration|architecture diagram)/iu],
];
const artifactPattern=/(?:^|[\s`"'(])([\w./\\-]+\.(?:md|csv|json|ya?ml|txt|py|js|mjs|cjs|ts|tsx|jsx|html|css|sql|mq[45]|mqh|xml|toml|ini|svg))(?![\w.])/giu;

function explicitSections(prompt:string){
  const matches=[...prompt.matchAll(/^\s*(PHASE\s+\d+|ขั้น(?:ตอน)?ที่\s*\d+|STEP\s+\d+)\b[^\r\n]*/gimu)];
  return matches.map((match,index)=>({id:`component-${String(index+1).padStart(2,"0")}`,title:match[0].trim(),body:prompt.slice(match.index??0,matches[index+1]?.index??prompt.length).trim()}));
}
function detectDomain(prompt:string):WorkDomain{return domains.find(([,pattern])=>pattern.test(prompt))?.[0]??"general";}
function namedArtifacts(prompt:string){
  const found=[...prompt.matchAll(artifactPattern)].map(match=>match[1].replace(/\\/g,"/"));
  return [...new Set(found)].filter(path=>!path.startsWith("/")&&!/^[A-Za-z]:/.test(path)&&!path.split("/").includes(".."));
}

export function classifyDurableRequest(prompt:string,minimumScore=5):AdmissionDecision{
  const domain=detectDomain(prompt);
  if (/\[(?:CogentNexus|Subagent) Context\]|cogent-workflow-result-|#cogent-direct\b/iu.test(prompt)) return {lane:"direct",score:0,reasons:["internal-or-explicit-direct"],sections:[],domain};
  const sections=explicitSections(prompt);let score=0;const reasons:string[]=[];
  if(sections.length>=3){score+=6;reasons.push(`explicit-components:${sections.length}`);}
  if(prompt.length>=1800){score+=2;reasons.push("large-request");}
  const matchedTerms=durableTerms.filter(pattern=>pattern.test(prompt)).length;
  if(matchedTerms>=2){score+=3;reasons.push(`durable-contract-signals:${matchedTerms}`);}
  const numericObligations=[...prompt.matchAll(/(?:อย่างน้อย|at least)\s*\d+|\b\d+\s+(?:services?|tables?|endpoints?|phases?|regions?|files?|chapters?|screens?)/giu)].length;
  if(numericObligations>=3){score+=3;reasons.push(`numeric-obligations:${numericObligations}`);}
  const artifacts=namedArtifacts(prompt);
  if(artifacts.length>=2){score+=4;reasons.push(`named-artifacts:${artifacts.length}`);}
  if(artifacts.length>=3&&/(?:งบ|budget|ยอดรวม|total)/iu.test(prompt)){score+=2;reasons.push("cross-artifact-budget-validation");}
  if(["software","trading"].includes(domain)&&/(?:สร้าง|พัฒนา|implement|build|create|แก้ไข|refactor)/iu.test(prompt)&&/(?:ทดสอบ|test|backtest|compile|build|ตรวจสอบ)/iu.test(prompt)){score+=5;reasons.push(`verified-${domain}-delivery`);}
  if(["files","analysis","fiction","design","translation"].includes(domain)&&/(?:หลายไฟล์|หลายขั้น|ทั้งระบบ|ครบถ้วน|complete|multiple files|end.to.end|ทั้งเล่ม|ทั้งชุด)/iu.test(prompt)){score+=5;reasons.push(`multi-step-${domain}`);}
  return {lane:score>=minimumScore?"durable":"direct",score,reasons,sections,domain};
}

function safeId(value:string){return value.replace(/[^A-Za-z0-9_-]/g,"-").replace(/-+/g,"-").slice(0,72);}
export function durableRequestFingerprint(prompt:string){return createHash("sha256").update(prompt.trim(),"utf8").digest("hex");}

const domainComponents:Record<WorkDomain,Array<[string,string]>>={
  software:[["specify","Inspect constraints and produce acceptance criteria, architecture, dependencies, and a test strategy."],["implement","Implement the requested software or system deliverables. Preserve existing project conventions and integrate all components."],["verify","Run or define build, lint, tests, and integration checks; repair defects and record exact evidence."]],
  trading:[["specify","Specify platform, symbols, timeframes, entries, exits, sizing, risk limits, and backtest acceptance criteria. Do not invent profit guarantees."],["implement","Implement the EA or trading-system deliverables with deterministic risk controls, logging, and configurable parameters."],["verify","Compile and validate strategy logic, risk constraints, look-ahead bias protections, and backtest/reproducibility evidence."]],
  files:[["inventory","Inventory relevant files, constraints, collisions, metadata requirements, and a reversible operation map."],["transform","Perform or specify the bounded file operations while preserving unrelated data and recording source-to-target mappings."],["verify","Verify counts, hashes or metadata, naming rules, collisions, and rollback evidence."]],
  analysis:[["define","Define the question, inputs, assumptions, schema, method, and acceptance checks."],["analyze","Perform the analysis with reproducible calculations and traceable source-to-result mappings."],["verify","Cross-check calculations, missing data, uncertainty, contradictions, and claims against evidence."]],
  fiction:[["story-bible","Create a story bible covering premise, characters, world rules, voice, continuity, and arc constraints."],["draft","Write the requested fiction deliverable while following the story bible and requested style."],["continuity","Check plot, character motivation, timeline, viewpoint, tone, and unresolved continuity defects; repair where appropriate."]],
  design:[["brief","Translate the request into audience, use cases, constraints, visual direction, states, accessibility, and acceptance criteria."],["produce","Produce the requested design artifacts and document key decisions and reusable tokens or specifications."],["review","Review hierarchy, consistency, responsiveness, accessibility, edge states, and handoff completeness."]],
  translation:[["translation-brief","Identify source and target languages, audience, register, terminology, protected names, formatting, and localization constraints."],["translate","Translate the complete requested content faithfully while preserving structure, numbers, names, links, placeholders, and the agreed terminology."],["bilingual-qa","Compare source and translation for omissions, additions, mistranslations, terminology drift, tone, grammar, formatting, numbers, names, and placeholders; repair defects and record only verifiable QA evidence."]],
  general:[["specify","Produce concrete acceptance criteria, dependencies, artifacts, constraints, and a verification plan."],["execute","Produce the requested deliverables from the verified specification."],["verify","Check every stated obligation, repair failures, and record evidence."]],
};

export function compileDurableIntake(input:{workspaceDir:string;prompt:string;runId:string;decision:AdmissionDecision;model:string}){
  const requestHash=durableRequestFingerprint(input.prompt),taskId=`CNX-AUTO-${safeId(input.runId)}`,relativeBase=`.cogent/intake/${taskId}`,base=resolve(input.workspaceDir,relativeBase);
  mkdirSync(base,{recursive:true});writeFileSync(resolve(base,"request.txt"),input.prompt,"utf8");
  const artifacts=namedArtifacts(input.prompt);
  if(artifacts.length) return compileNamedArtifacts({...input,requestHash,taskId,relativeBase,base,artifacts});
  const sections=input.decision.sections.length?input.decision.sections:domainComponents[input.decision.domain].map(([id,body])=>({id,title:id,body}));
  const steps:any[]=[],outputs:string[]=[];mkdirSync(resolve(base,"prompts"),{recursive:true});
  sections.forEach((section,index)=>{const output=`${relativeBase}/artifacts/${section.id}.md`,instruction=`${relativeBase}/prompts/${section.id}.txt`;
    writeFileSync(resolve(input.workspaceDir,instruction),["Act as one bounded CogentNexus worker.",`Work domain: ${input.decision.domain}.`,"Complete only the component below. Treat request.txt and prior verified components as authoritative context.","State assumptions and concrete evidence; never claim unperformed tests or external actions.",`Component: ${section.title}`,section.body].join("\n\n"),"utf8");
    steps.push({id:section.id,dependsOn:index===0?[]:[sections[index-1].id],executor:{type:"ollama",model:input.model,promptFile:instruction,includeFiles:[`${relativeBase}/request.txt`,...outputs],output,timeoutSeconds:1800,inactivityTimeoutSeconds:180,options:{num_predict:4096}},outputs:[output],outputMinimumBytes:80,maximumAttempts:2,idempotent:true});outputs.push(output);});
  const assembled=`${relativeBase}/artifacts/assembled.md`;steps.push({id:"assemble",dependsOn:sections.map(section=>section.id),executor:{type:"concat",inputs:outputs,output:assembled},outputs:[assembled],outputMinimumBytes:200,maximumAttempts:1,idempotent:true});
  return writeManifest({input,taskId,relativeBase,requestHash,steps,componentCount:sections.length,assembledOutput:assembled,goal:`Complete a verified durable ${input.decision.domain} request`});
}

function compileNamedArtifacts(input:{workspaceDir:string;prompt:string;runId:string;decision:AdmissionDecision;model:string;requestHash:string;taskId:string;relativeBase:string;base:string;artifacts:string[]}){
  mkdirSync(resolve(input.base,"prompts"),{recursive:true});const steps:any[]=[];
  input.artifacts.forEach((output,index)=>{const id=`artifact-${String(index+1).padStart(2,"0")}`,promptFile=`${input.relativeBase}/prompts/${id}.txt`;
    writeFileSync(resolve(input.workspaceDir,promptFile),["Create exactly one requested artifact.",`Work domain: ${input.decision.domain}.`,`Artifact path: ${output}`,"Use request.txt and prior artifacts as context. Return only the complete file content, without Markdown fences.","For source code, produce compilable, integrated code; for prose/design specifications, make it substantive and internally consistent. Never fabricate test results."].join("\n\n"),"utf8");
    steps.push({id,dependsOn:index?[`artifact-${String(index).padStart(2,"0")}`]:[],executor:{type:"ollama",model:input.model,promptFile,includeFiles:[`${input.relativeBase}/request.txt`,...input.artifacts.slice(0,index)],output,timeoutSeconds:1800,inactivityTimeoutSeconds:180,options:{num_predict:8192}},outputs:[output],outputMinimumBytes:20,maximumAttempts:2,idempotent:true});});
  const validatorPath=`${input.relativeBase}/validate_artifacts.py`;writeFileSync(resolve(input.workspaceDir,validatorPath),GENERIC_ARTIFACT_VALIDATOR,"utf8");
  steps.push({id:"validate-artifacts",dependsOn:steps.map(step=>step.id),executor:{type:"command",argv:["python",validatorPath,...input.artifacts]},validator:{argv:["python",validatorPath,...input.artifacts]},outputs:input.artifacts,maximumAttempts:1,idempotent:true});
  return writeManifest({input,taskId:input.taskId,relativeBase:input.relativeBase,requestHash:input.requestHash,steps,componentCount:input.artifacts.length,assembledOutput:input.artifacts.find(path=>/^readme\.md$/iu.test(basename(path)))??input.artifacts.at(-1)!,goal:`Create and externally validate ${input.artifacts.length} named ${input.decision.domain} artifacts`});
}

function writeManifest(args:{input:{workspaceDir:string;decision:AdmissionDecision};taskId:string;relativeBase:string;requestHash:string;steps:any[];componentCount:number;assembledOutput:string;goal:string}){
  const manifest={schemaVersion:1,taskId:args.taskId,goal:args.goal,domain:args.input.decision.domain,admission:{score:args.input.decision.score,reasons:args.input.decision.reasons,requestHash:args.requestHash},steps:args.steps};
  const manifestPath=`${args.relativeBase}/manifest.json`;writeFileSync(resolve(args.input.workspaceDir,manifestPath),`${JSON.stringify(manifest,null,2)}\n`,"utf8");
  return {taskId:args.taskId,manifestPath,componentCount:args.componentCount,assembledOutput:args.assembledOutput,requestHash:args.requestHash};
}

const GENERIC_ARTIFACT_VALIDATOR=`import ast,csv,json,sys\nfrom pathlib import Path\npaths=[Path(value) for value in sys.argv[1:]]\nassert paths,"no artifacts"\nfor path in paths:\n assert path.is_file(),f"missing artifact: {path}"\n data=path.read_bytes()\n assert len(data)>=20,f"artifact too small: {path}"\n assert b"\\x00" not in data,f"binary artifact unsupported: {path}"\n text=data.decode("utf-8-sig")\n suffix=path.suffix.lower()\n if suffix==".json": json.loads(text)\n elif suffix==".py": ast.parse(text,filename=str(path))\n elif suffix==".csv":\n  rows=list(csv.reader(text.splitlines()));assert rows and rows[0] and len(rows)>1,f"empty CSV: {path}"\n elif suffix==".svg":\n  assert "<svg" in text.lower() and "</svg>" in text.lower(),f"invalid SVG: {path}"\n elif suffix in {".js",".mjs",".cjs",".ts",".tsx",".jsx",".mq4",".mq5",".mqh",".sql",".html",".css"}:\n  assert text.strip(),f"empty source: {path}"\nprint("validated artifacts="+str(len(paths))+" paths="+",".join(map(str,paths)))\n`;
