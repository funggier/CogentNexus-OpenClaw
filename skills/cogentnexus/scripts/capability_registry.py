#!/usr/bin/env python3
import os,platform,re,shutil
from datetime import datetime,timezone
from pathlib import Path
EXECUTABLES={"python.runtime":("python","Run Python programs"),"git.cli":("git","Operate Git repositories"),"github.cli":("gh","Operate GitHub repositories and workflows"),"ollama.local":("ollama","Run local models"),"openclaw.cli":("openclaw","Operate OpenClaw"),"node.runtime":("node","Run Node.js"),"gitleaks.scan":("gitleaks","Scan for secrets")}
BUILTINS=[
("runtime.state","Durable revisioned task state",True,True),("runtime.ledger","Append-only execution ledger",True,False),
("runtime.verify","Artifact integrity verification",True,True),("runtime.recover","Bounded recovery policies",True,True),
("process.execute","Execute a bounded local process",True,False)]
def now(): return datetime.now(timezone.utc).isoformat()
def locate(exe):
 location=shutil.which(exe)
 if location:return location
 if os.name=="nt":
  candidates=[]
  if exe=="gh":candidates.append(Path(os.environ.get("ProgramFiles","C:/Program Files"))/"GitHub CLI"/"gh.exe")
  if exe=="gitleaks":
   base=Path(os.environ.get("LOCALAPPDATA",""))/"Microsoft"/"WinGet"/"Packages"
   if base.is_dir():candidates.extend(base.glob("Gitleaks.Gitleaks_*/gitleaks.exe"))
  for candidate in candidates:
   if candidate.is_file():return str(candidate)
 return None
def entry(name,description,available,write,reversible,source,evidence,authorization=False):
 return {"name":name,"description":description,"available":available,"canRead":True,"canWrite":write,"destructive":False,
 "requiresAuthorization":authorization,"memoryCost":"low","reversible":reversible,"source":source,"platform":platform.system().lower(),"observedAt":now(),"evidence":evidence}
def build_registry(workspace):
 workspace=Path(workspace).resolve(); values=[entry(n,d,True,w,r,"cogent-runtime","built-in") for n,d,w,r in BUILTINS]
 for name,(exe,description) in EXECUTABLES.items():
  location=locate(exe); values.append(entry(name,description,bool(location),name in {"git.cli","github.cli","openclaw.cli"},name!="github.cli","environment",location or f"{exe} not found",name=="github.cli"))
 skills=workspace/"skills"
 if skills.is_dir():
  for folder in sorted(p for p in skills.iterdir() if p.is_dir() and (p/"SKILL.md").is_file()):
   values.append(entry(f"skill.{folder.name}",f"OpenClaw skill: {folder.name}",True,False,True,"openclaw-skill",str(folder/"SKILL.md")))
 return {"schemaVersion":1,"generatedAt":now(),"workspace":str(workspace),"capabilities":values}
def find(registry,query):
 words=set(re.findall(r"[a-z0-9]+",query.lower())); ranked=[]
 for item in registry.get("capabilities",[]):
  name=item.get("name","").lower(); hay=name+" "+item.get("description","").lower()
  score=sum(3 if w in name else 1 for w in words if w in hay)
  if score: ranked.append((score,item))
 return [item for _,item in sorted(ranked,key=lambda x:(-x[0],x[1]["name"]))]
def get(registry,name): return next((x for x in registry.get("capabilities",[]) if x.get("name")==name),None)
def check(item):
 if item is None: return {"available":False,"reason":"capability not registered"}
 result=dict(item)
 if item["name"] in EXECUTABLES:
  location=locate(EXECUTABLES[item["name"]][0]); result.update({"available":bool(location),"evidence":location or "executable not found","observedAt":now()})
 elif item["name"].startswith("skill."): result.update({"available":Path(item.get("evidence","")).is_file(),"observedAt":now()})
 return result
