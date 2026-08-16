#!/usr/bin/env python3
import argparse, hashlib, json, os, platform, re, shlex, shutil, subprocess, sys, tempfile, time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from artifact_manifest import fingerprint, matches
from capability_registry import build_registry, check as check_capability, find as find_capabilities, get as get_capability
from recovery_controller import apply_to_state, classify as classify_recovery, make_plan, recovery_state

WORKSPACE=Path(__file__).resolve().parents[3]
DEFAULT_ROOT=WORKSPACE/".cogent"
TASK_ID_RE=re.compile(r"^[A-Za-z0-9._-]+$")
EVENTS={"INTENT","ACTION","OBSERVATION","DECISION","VERIFICATION","COMMIT","ROLLBACK","FAILURE","RECOVERY"}
MANUAL_EVENTS={"ACTION","OBSERVATION","DECISION","FAILURE"}
SECRET_RE=re.compile(r"(password|passwd|token|secret|authorization|api[-_]?key)",re.I)
OUTPUT_LIMIT=4000

def now(): return datetime.now(timezone.utc).isoformat()
def emit(value): print(json.dumps(value,ensure_ascii=False,indent=2))

def atomic_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as handle:
            json.dump(value,handle,ensure_ascii=False,indent=2); handle.write("\n"); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def task_base(args):
    if not TASK_ID_RE.fullmatch(args.task_id): raise SystemExit("invalid task id")
    return args.root.resolve()/"tasks"/args.task_id

def task_paths(args):
    base=task_base(args)
    return {"base":base,"state":base/"state.json","ledger":base/"ledger.jsonl","verification":base/"verification.json",
            "transaction":base/"transaction.json","lock":base/".lock","revisions":base/"revisions"}

def read_json(path):
    if not path.is_file(): raise SystemExit(f"missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def ledger_records(path):
    if not path.exists(): return []
    records=[]
    for number,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if line.strip():
            try: records.append(json.loads(line))
            except json.JSONDecodeError as exc: raise SystemExit(f"invalid ledger line {number}: {exc}")
    return records

@contextmanager
def writer_lock(path,timeout=10):
    path.parent.mkdir(parents=True,exist_ok=True); deadline=time.monotonic()+timeout
    while True:
        try:
            fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
            os.write(fd,json.dumps({"pid":os.getpid(),"createdAt":now()}).encode()); os.close(fd); break
        except (FileExistsError,PermissionError) as exc:
            # Windows may report a sharing violation as PermissionError while another
            # process is creating/deleting the lock. Treat it as contention only when
            # the lock path actually exists; preserve genuine permission failures.
            if isinstance(exc,PermissionError) and not path.exists(): raise
            try:
                if time.time()-path.stat().st_mtime>30:
                    try: path.unlink()
                    except PermissionError: pass
                    else: continue
            except FileNotFoundError: continue
            if time.monotonic()>=deadline: raise SystemExit("task writer lock timeout")
            time.sleep(0.05)
    try: yield
    finally:
        try: path.unlink()
        except FileNotFoundError: pass

def append_raw(path,event):
    with path.open("a",encoding="utf-8",newline="\n") as handle:
        handle.write(json.dumps(event,ensure_ascii=False,separators=(",",":"))+"\n"); handle.flush(); os.fsync(handle.fileno())

def next_event(paths,args,kind,summary,data=None):
    records=ledger_records(paths["ledger"])
    return {"sequence":len(records)+1,"timestamp":now(),"taskId":args.task_id,"type":kind,"summary":summary,"data":data or {}}

def write_revision(paths,state):
    revision=paths["revisions"]/f"{int(state['revision']):06d}.json"
    if revision.exists():
        if read_json(revision)!=state: raise SystemExit(f"revision conflict: {state['revision']}")
    else: atomic_json(revision,state)
    current=read_json(paths["state"]) if paths["state"].exists() else None
    if current is None or int(current.get("revision",0))<=int(state["revision"]): atomic_json(paths["state"],state)

def recover_pending_locked(paths):
    if not paths["transaction"].exists(): return False
    txn=read_json(paths["transaction"]); event=txn["event"]; state=txn["state"]
    records=ledger_records(paths["ledger"]); seq=int(event["sequence"])
    if len(records)<seq: append_raw(paths["ledger"],event)
    elif records[seq-1]!=event: raise SystemExit("transaction conflicts with ledger")
    write_revision(paths,state); paths["transaction"].unlink(); return True

def transactional_state(paths,event,state):
    atomic_json(paths["transaction"],{"schemaVersion":1,"event":event,"state":state})
    append_raw(paths["ledger"],event); write_revision(paths,state); paths["transaction"].unlink()

def append_event(args,kind,summary,data=None):
    paths=task_paths(args)
    with writer_lock(paths["lock"]):
        recover_pending_locked(paths)
        if not paths["state"].exists(): raise SystemExit("task is not initialized")
        event=next_event(paths,args,kind,summary,data); append_raw(paths["ledger"],event)
    return event

def load_state(args):
    paths=task_paths(args)
    with writer_lock(paths["lock"]): recover_pending_locked(paths)
    return read_json(paths["state"])

def task_init(args):
    paths=task_paths(args)
    with writer_lock(paths["lock"]):
        recover_pending_locked(paths)
        if paths["state"].exists() or paths["ledger"].exists(): raise SystemExit("task already exists")
        state={"schemaVersion":2,"taskId":args.task_id,"goal":args.goal,"currentObjective":args.objective or args.goal,
          "status":"ready","revision":1,"completedSteps":[],"currentStep":None,"producedArtifacts":[],
          "importantDiscoveries":[],"pendingWork":[],"knownFailures":[],"recoveryHint":"Load committed state and select the smallest next step.",
          "verification":{"status":"NOT_RUN","report":None},"recovery":recovery_state({}),"updatedAt":now(),"ledgerSequence":1}
        event=next_event(paths,args,"INTENT","Task initialized",{"goal":args.goal}); transactional_state(paths,event,state)
    emit(state)

def state_show(args): emit(load_state(args))

def resolve_artifact(value):
    path=Path(value)
    return path.resolve() if path.is_absolute() else (WORKSPACE/path).resolve()

def sha256(path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()

def completion_evidence(paths,state,artifacts):
    report=read_json(paths["verification"])
    if report.get("status")!="PASS": raise SystemExit("completion rejected: latest verification is not PASS")
    if report.get("verifiedStateRevision")!=state.get("revision"): raise SystemExit("completion rejected: verification is stale for current state revision")
    evidence={item["target"]:item for item in report.get("checks",[]) if item.get("type")=="artifact" and item.get("pass")}
    for value in artifacts:
        target=str(resolve_artifact(value)); expected=evidence.get(target)
        if expected is None: raise SystemExit(f"completion rejected: artifact lacks integrity evidence: {value}")
        if not matches(expected): raise SystemExit(f"completion rejected: artifact changed after verification: {value}")
    return report
def state_commit(args):
    paths=task_paths(args)
    with writer_lock(paths["lock"]):
        recover_pending_locked(paths); state=read_json(paths["state"])
        artifacts=list(dict.fromkeys(list(state.get("producedArtifacts",[]))+args.artifact))
        report=completion_evidence(paths,state,artifacts) if args.status=="completed" else None
        new=dict(state); new["schemaVersion"]=2; new["revision"]=int(state["revision"])+1
        if args.objective is not None: new["currentObjective"]=args.objective
        if args.current_step is not None: new["currentStep"]=args.current_step
        if args.status is not None: new["status"]=args.status
        if args.recovery_hint is not None: new["recoveryHint"]=args.recovery_hint
        mapping={"completedSteps":args.completed,"producedArtifacts":args.artifact,"importantDiscoveries":args.discovery,
                 "pendingWork":args.pending,"knownFailures":args.failure}
        for key,values in mapping.items():
            if values: new[key]=list(dict.fromkeys(list(new.get(key,[]))+values))
        if paths["verification"].exists():
            current_report=read_json(paths["verification"])
            new["verification"]={"status":current_report["status"],"report":str(paths["verification"])}
        new["updatedAt"]=now()
        event=next_event(paths,args,"COMMIT",f"State revision {new['revision']} committed",
          {"revision":new["revision"],"status":new["status"],"currentStep":new["currentStep"],
           "verificationId":report.get("verificationId") if report else None})
        new["ledgerSequence"]=event["sequence"]; transactional_state(paths,event,new)
    emit(new)

def state_rollback(args):
    paths=task_paths(args)
    with writer_lock(paths["lock"]):
        recover_pending_locked(paths); old=read_json(paths["revisions"]/f"{args.revision:06d}.json"); current=read_json(paths["state"])
        restored=dict(old); restored["schemaVersion"]=2; restored["revision"]=int(current["revision"])+1; restored["updatedAt"]=now()
        event=next_event(paths,args,"ROLLBACK",f"Rolled back content to revision {args.revision}",
          {"sourceRevision":args.revision,"newRevision":restored["revision"]})
        restored["ledgerSequence"]=event["sequence"]; transactional_state(paths,event,restored)
    emit(restored)

def sanitize(value):
    if isinstance(value,dict): return {k:("***REDACTED***" if SECRET_RE.search(str(k)) else sanitize(v)) for k,v in value.items()}
    if isinstance(value,list): return [sanitize(v) for v in value]
    return value

def parse_data(values):
    data={}
    for item in values:
        if "=" not in item: raise SystemExit("--data requires key=value")
        key,value=item.split("=",1); data[key]="***REDACTED***" if SECRET_RE.search(key) else value
    return data

def ledger_append(args):
    event=append_event(args,args.type,args.summary,parse_data(args.data)); emit(event)

def sanitize_argv(argv):
    clean=[]; redact_next=False
    for item in argv:
        if redact_next: clean.append("***REDACTED***"); redact_next=False; continue
        if SECRET_RE.search(item):
            if "=" in item: clean.append(item.split("=",1)[0]+"=***REDACTED***")
            else: clean.append(item); redact_next=True
        else: clean.append(item)
    return clean

def classify_failure(returncode,error=""):
    text=error.lower()
    if "timed out" in text: return "timeout"
    if "permission" in text or "access is denied" in text: return "permission"
    if returncode is not None and returncode<0: return "process-killed"
    return "tool-failure"

def run_command(args):
    load_state(args); argv=shlex.split(args.command,posix=os.name!="nt")
    append_event(args,"ACTION",f"Execute step: {args.step}",{"step":args.step,"argv":sanitize_argv(argv),"timeoutSeconds":args.timeout})
    started=time.monotonic()
    try:
        proc=subprocess.run(argv,cwd=WORKSPACE,capture_output=True,text=True,timeout=args.timeout)
        data={"step":args.step,"durationMs":round((time.monotonic()-started)*1000),"exitCode":proc.returncode,
              "stdout":proc.stdout[-OUTPUT_LIMIT:],"stderr":proc.stderr[-OUTPUT_LIMIT:]}
        kind="OBSERVATION" if proc.returncode==0 else "FAILURE"
        if kind=="FAILURE": data["class"]=classify_failure(proc.returncode,proc.stderr)
        append_event(args,kind,f"Step {args.step} {'passed' if proc.returncode==0 else 'failed'}",sanitize(data)); emit(data)
        return proc.returncode
    except subprocess.TimeoutExpired as exc:
        data={"step":args.step,"durationMs":round((time.monotonic()-started)*1000),"class":"timeout",
              "stdout":str(exc.stdout or "")[-OUTPUT_LIMIT:],"stderr":str(exc.stderr or "")[-OUTPUT_LIMIT:]}
        append_event(args,"FAILURE",f"Step {args.step} timed out",sanitize(data)); emit(data); return 124
    except Exception as exc:
        data={"step":args.step,"durationMs":round((time.monotonic()-started)*1000),"class":classify_failure(None,str(exc)),"error":str(exc)}
        append_event(args,"FAILURE",f"Step {args.step} could not start",sanitize(data)); emit(data); return 1

def memory_info():
    result={"availableBytes":None,"totalBytes":None}
    try:
        import psutil
        vm=psutil.virtual_memory(); return {"availableBytes":vm.available,"totalBytes":vm.total}
    except Exception: pass
    if os.name=="nt":
        proc=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",
          "(Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json -Compress)"],
          capture_output=True,text=True,timeout=10)
        if proc.returncode==0:
            value=json.loads(proc.stdout); result={"availableBytes":int(value["FreePhysicalMemory"])*1024,
              "totalBytes":int(value["TotalVisibleMemorySize"])*1024}
    return result

def git_info():
    if not shutil.which("git"): return {"available":False}
    proc=subprocess.run(["git","status","--porcelain=v1","--branch"],cwd=WORKSPACE,capture_output=True,text=True,timeout=10)
    return {"available":True,"isRepository":proc.returncode==0,"status":proc.stdout.splitlines() if proc.returncode==0 else []}

def probe(args):
    disk=shutil.disk_usage(WORKSPACE)
    system={"timestamp":now(),"platform":platform.platform(),"python":sys.version.split()[0],"pid":os.getpid(),
      "cpuCount":os.cpu_count(),"memory":memory_info(),"disk":{"totalBytes":disk.total,"freeBytes":disk.free},"cwd":str(Path.cwd())}
    workspace={"timestamp":now(),"workspace":str(WORKSPACE),"writable":os.access(WORKSPACE,os.W_OK),"git":git_info(),
      "tools":{name:bool(shutil.which(name)) for name in ("git","python","node","openclaw","ollama")}}
    result=system if args.scope=="system" else workspace if args.scope=="workspace" else {"system":system,"workspace":workspace}
    if getattr(args,"task_id",None): append_event(args,"OBSERVATION",f"{args.scope} probe",result)
    emit(result)

def verify_run(args):
    state=load_state(args); checks=[]
    for value in args.exists:
        path=resolve_artifact(value); checks.append({"type":"exists","target":str(path),"pass":path.exists()})
    for value in args.hash:
        item=fingerprint(resolve_artifact(value))
        checks.append({"type":"artifact","target":item["target"],"pass":item["digest"] is not None,"kind":item["kind"],
          "digest":item["digest"],"fileCount":item["fileCount"],"totalBytes":item["totalBytes"]})
    for command in args.command:
        argv=shlex.split(command,posix=os.name!="nt"); started=time.monotonic()
        try:
            proc=subprocess.run(argv,cwd=WORKSPACE,capture_output=True,text=True,timeout=args.timeout)
            checks.append({"type":"command","command":sanitize_argv(argv),"pass":proc.returncode==0,"exitCode":proc.returncode,
              "durationMs":round((time.monotonic()-started)*1000),"stdout":proc.stdout[-OUTPUT_LIMIT:],"stderr":proc.stderr[-OUTPUT_LIMIT:]})
        except subprocess.TimeoutExpired as exc:
            checks.append({"type":"command","command":sanitize_argv(argv),"pass":False,"class":"timeout",
              "stdout":str(exc.stdout or "")[-OUTPUT_LIMIT:],"stderr":str(exc.stderr or "")[-OUTPUT_LIMIT:]})
    status="PASS" if checks and all(item.get("pass") for item in checks) else "FAIL"
    verification_id=hashlib.sha256(json.dumps({"taskId":args.task_id,"stateRevision":state["revision"],"checks":checks},sort_keys=True).encode()).hexdigest()[:16]
    report={"schemaVersion":2,"verificationId":verification_id,"taskId":args.task_id,"verifiedStateRevision":state["revision"],
      "status":status,"checkedAt":now(),"checks":checks}
    paths=task_paths(args)
    with writer_lock(paths["lock"]): atomic_json(paths["verification"],report)
    append_event(args,"VERIFICATION",f"Verification {status}",{"verificationId":verification_id,"verifiedStateRevision":state["revision"],"checks":len(checks)})
    emit(report); return 0 if status=="PASS" else 1

def verify_show(args):
    paths=task_paths(args); report=read_json(paths["verification"]); state=read_json(paths["state"])
    report=dict(report); report["currentStateRevision"]=state["revision"]; report["stale"]=report.get("verifiedStateRevision")!=state["revision"]; emit(report)

def capability_path(args): return args.root.resolve()/"capabilities"/"registry.json"
def capability_availability(args):
    path=capability_path(args); return check_capability(path) if path.exists() else {"ok":False,"missingRequired":[]}
def capability_cmd(args):
    path=capability_path(args)
    if args.command_name=="sync": emit(build_registry(WORKSPACE,path)); return
    if not path.exists(): build_registry(WORKSPACE,path)
    if args.command_name=="list": emit(json.loads(path.read_text(encoding="utf-8"))); return
    if args.command_name=="find": emit(find_capabilities(path,args.query)); return
    if args.command_name=="inspect": emit(get_capability(path,args.name)); return
    if args.command_name=="check": emit(check_capability(path,args.name)); return

def recover_cmd(args):
    state=load_state(args); records=ledger_records(task_paths(args)["ledger"]); classification=classify_recovery(records)
    if args.command_name=="classify": emit(classification); return
    if args.command_name=="plan": emit(make_plan(state,classification,capability_availability(args))); return
    if args.command_name=="inspect": emit({"taskId":args.task_id,"recovery":state.get("recovery",recovery_state({})),"classification":classification}); return
    execute=args.execute_safe; plan=make_plan(state,classification,capability_availability(args))
    if not execute: emit({"dryRun":True,"taskId":args.task_id,"plan":plan}); return
    paths=task_paths(args)
    with writer_lock(paths["lock"]):
        recover_pending_locked(paths); current=read_json(paths["state"]); decision=apply_to_state(current,plan,now())
        if not decision["allowed"]:
            event=next_event(paths,args,"FAILURE",f"Recovery blocked: {decision['reason']}",{"plan":plan}); append_raw(paths["ledger"],event)
            raise SystemExit(decision["reason"])
        new=decision["state"]; event=next_event(paths,args,"RECOVERY",f"Recovery attempt {new['recovery']['attempts']}: {plan['strategy']}",{"plan":plan})
        new["ledgerSequence"]=event["sequence"]; transactional_state(paths,event,new)
    emit({"taskId":args.task_id,"applied":True,"plan":plan,"stateRevision":new["revision"],"recovery":new["recovery"]})

def policy_next(args):
    state=load_state(args); records=ledger_records(task_paths(args)["ledger"])
    if any(x.get("type")=="FAILURE" for x in records):
        emit({"transition":"recover","taskId":args.task_id,"plan":make_plan(state,classify_recovery(records),capability_availability(args))}); return
    transition="commit" if state.get("verification",{}).get("status")=="PASS" else "execute-or-verify"
    emit({"transition":transition,"taskId":args.task_id,"stateRevision":state.get("revision"),"capabilitiesRegistry":str(capability_path(args))})

def ledger_cmd(args):
    paths=task_paths(args)
    with writer_lock(paths["lock"]): recover_pending_locked(paths)
    records=ledger_records(paths["ledger"])
    if args.command_name=="validate":
        for index,item in enumerate(records,1):
            if item.get("sequence")!=index or item.get("taskId")!=args.task_id or item.get("type") not in EVENTS:
                raise SystemExit(f"invalid ledger record: {index}")
        if paths["transaction"].exists(): raise SystemExit("pending transaction remains")
        emit({"status":"PASS","records":len(records)}); return
    if args.command_name=="tail": records=records[-args.lines:]
    emit(records)

def call(script,root,*parts):
    return subprocess.run([sys.executable,str(script),"--root",str(root),*parts],capture_output=True,text=True)

def self_test(args):
    root=Path(tempfile.mkdtemp(prefix="cogent-self-test-")); script=Path(__file__).resolve(); artifact=root/"artifact"
    try:
        if call(script,root,"task","init","--task-id","TEST-1","--goal","test").returncode: raise SystemExit("init failed")
        workers=[subprocess.Popen([sys.executable,str(script),"--root",str(root),"ledger","append","--task-id","TEST-1","--type","ACTION","--summary",f"parallel-{i}"],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True) for i in range(8)]
        for worker in workers:
            _,err=worker.communicate()
            if worker.returncode: raise SystemExit(err)
        if call(script,root,"run","--task-id","TEST-1","--step","health","--command",f"{sys.executable} --version").returncode: raise SystemExit("run failed")
        artifact.mkdir(); nested=artifact/"nested.txt"; nested.write_text("verified",encoding="utf-8")
        passed=call(script,root,"verify","run","--task-id","TEST-1","--exists",str(artifact),"--hash",str(artifact))
        if passed.returncode: raise SystemExit(passed.stderr or passed.stdout)
        nested.write_text("tampered",encoding="utf-8")
        rejected=call(script,root,"state","commit","--task-id","TEST-1","--status","completed","--artifact",str(artifact))
        if rejected.returncode==0 or "changed after verification" not in (rejected.stderr+rejected.stdout): raise SystemExit("directory tamper gate failed")
        nested.write_text("verified",encoding="utf-8")
        if call(script,root,"verify","run","--task-id","TEST-1","--exists",str(artifact),"--hash",str(artifact)).returncode: raise SystemExit("reverify failed")
        if call(script,root,"state","commit","--task-id","TEST-1","--status","completed","--artifact",str(artifact)).returncode: raise SystemExit("completion failed")
        if call(script,root,"ledger","validate","--task-id","TEST-1").returncode: raise SystemExit("ledger validation failed")
        if call(script,root,"capability","sync").returncode: raise SystemExit("capability sync failed")
        found=call(script,root,"capability","find","python")
        if found.returncode or "python.runtime" not in found.stdout: raise SystemExit("capability find failed")
        if call(script,root,"task","init","--task-id","TEST-2","--goal","recover").returncode: raise SystemExit("recovery init failed")
        if call(script,root,"ledger","append","--task-id","TEST-2","--type","FAILURE","--summary","memory exhausted","--data","class=oom").returncode: raise SystemExit("failure append failed")
        dry=call(script,root,"recover","apply","--task-id","TEST-2")
        if dry.returncode or '"dryRun": true' not in dry.stdout: raise SystemExit("dry-run failed")
        before=json.loads(call(script,root,"state","inspect","--task-id","TEST-2").stdout)["revision"]
        applied=call(script,root,"recover","apply","--task-id","TEST-2","--execute-safe")
        after=json.loads(call(script,root,"state","inspect","--task-id","TEST-2").stdout)["revision"]
        if applied.returncode or after!=before+1: raise SystemExit("safe apply failed")
        call(script,root,"recover","apply","--task-id","TEST-2","--execute-safe")
        blocked=call(script,root,"recover","apply","--task-id","TEST-2","--execute-safe")
        if blocked.returncode==0 or "circuit breaker" not in (blocked.stderr+blocked.stdout): raise SystemExit("circuit breaker failed")
        records=json.loads(call(script,root,"ledger","show","--task-id","TEST-1").stdout)
        if not any(x["type"]=="ACTION" for x in records) or not any(x["type"]=="OBSERVATION" for x in records): raise SystemExit("run events missing")
        if (root/"tasks"/"TEST-1"/"transaction.json").exists(): raise SystemExit("transaction remained")
        print("Cogent runtime Phase 2 self-test: PASS")
    finally: shutil.rmtree(root,ignore_errors=True)
def add_task_id(parser,required=True): parser.add_argument("--task-id",required=required)

def main():
    parser=argparse.ArgumentParser(prog="cogent"); parser.add_argument("--root",type=Path,default=DEFAULT_ROOT)
    subs=parser.add_subparsers(dest="area",required=True)
    task=subs.add_parser("task").add_subparsers(dest="command_name",required=True)
    init=task.add_parser("init"); add_task_id(init); init.add_argument("--goal",required=True); init.add_argument("--objective"); init.set_defaults(func=task_init)
    state=subs.add_parser("state").add_subparsers(dest="command_name",required=True)
    for name in ("load","inspect"):
        p=state.add_parser(name); add_task_id(p); p.set_defaults(func=state_show)
    commit=state.add_parser("commit"); add_task_id(commit); commit.add_argument("--objective"); commit.add_argument("--current-step")
    commit.add_argument("--status",choices=["ready","executing","verifying","completed","failed","abandoned"])
    for flag in ("completed","artifact","discovery","pending","failure"): commit.add_argument("--"+flag,action="append",default=[])
    commit.add_argument("--recovery-hint"); commit.set_defaults(func=state_commit)
    rollback=state.add_parser("rollback"); add_task_id(rollback); rollback.add_argument("--revision",type=int,required=True); rollback.set_defaults(func=state_rollback)
    run=subs.add_parser("run"); add_task_id(run); run.add_argument("--step",required=True); run.add_argument("--command",required=True); run.add_argument("--timeout",type=int,default=120); run.set_defaults(func=run_command)
    probes=subs.add_parser("probe").add_subparsers(dest="scope",required=True)
    for name in ("system","workspace","all"):
        p=probes.add_parser(name); add_task_id(p,False); p.set_defaults(func=probe)
    verify=subs.add_parser("verify").add_subparsers(dest="command_name",required=True)
    vr=verify.add_parser("run"); add_task_id(vr); vr.add_argument("--exists",action="append",default=[]); vr.add_argument("--hash",action="append",default=[])
    vr.add_argument("--command",action="append",default=[]); vr.add_argument("--timeout",type=int,default=120); vr.set_defaults(func=verify_run)
    for name in ("inspect","status"):
        p=verify.add_parser(name); add_task_id(p); p.set_defaults(func=verify_show)
    recover=subs.add_parser("recover").add_subparsers(dest="command_name",required=True)
    for name in ("classify","plan","inspect"):
        p=recover.add_parser(name); add_task_id(p); p.set_defaults(func=recover_cmd)
    ra=recover.add_parser("apply"); add_task_id(ra); ra.add_argument("--execute-safe",action="store_true"); ra.set_defaults(func=recover_cmd)
    capability=subs.add_parser("capability").add_subparsers(dest="command_name",required=True)
    for name in ("sync","list"):
        p=capability.add_parser(name); p.set_defaults(func=capability_cmd)
    cf=capability.add_parser("find"); cf.add_argument("query"); cf.set_defaults(func=capability_cmd)
    for name in ("inspect","check"):
        p=capability.add_parser(name); p.add_argument("name"); p.set_defaults(func=capability_cmd)
    policy=subs.add_parser("policy").add_subparsers(dest="command_name",required=True)
    pn=policy.add_parser("next"); add_task_id(pn); pn.set_defaults(func=policy_next)
    ledger=subs.add_parser("ledger").add_subparsers(dest="command_name",required=True)
    la=ledger.add_parser("append"); add_task_id(la); la.add_argument("--type",choices=sorted(MANUAL_EVENTS),required=True); la.add_argument("--summary",required=True)
    la.add_argument("--data",action="append",default=[]); la.set_defaults(func=ledger_append)
    for name in ("show","tail","validate"):
        p=ledger.add_parser(name); add_task_id(p); p.add_argument("--lines",type=int,default=20); p.set_defaults(func=ledger_cmd)
    test=subs.add_parser("self-test"); test.set_defaults(func=self_test)
    args=parser.parse_args(); return args.func(args) or 0

if __name__=="__main__": raise SystemExit(main())