#!/usr/bin/env python3
"""Deterministic CogentNexus workflow runner (Phase 4 core)."""
import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

TERMINAL = {"completed", "blocked", "failed", "cancelled"}
STEP_TERMINAL = {"completed", "blocked", "failed", "cancelled"}
TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

def now(): return datetime.now(timezone.utc).isoformat()
def emit(value): print(json.dumps(value, ensure_ascii=False, indent=2))
def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
def digest(value): return hashlib.sha256(canonical(value)).hexdigest()

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n"); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)

@contextmanager
def lock(path, timeout=10):
    """Acquire a process-scoped lock that the OS releases after a crash/kill."""
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    handle = open(path, "a+b")
    if handle.seek(0, os.SEEK_END) == 0:
        handle.write(b"\0"); handle.flush()
    acquired = False
    try:
        while not acquired:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                if time.monotonic() >= deadline: raise TimeoutError("workflow lock timeout")
                time.sleep(.05)
        handle.seek(0); handle.truncate(); handle.write(f"{os.getpid()} {time.time()}".encode()); handle.flush()
        yield
    finally:
        if acquired:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()

def validate_manifest(value):
    if not isinstance(value, dict) or value.get("schemaVersion") != 1: raise ValueError("schemaVersion must be 1")
    if not isinstance(value.get("taskId"), str) or not TASK_ID.fullmatch(value["taskId"]): raise ValueError("taskId must be a safe portable identifier")
    steps = value.get("steps")
    if not isinstance(steps, list) or not steps: raise ValueError("non-empty steps required")
    ids = []
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("id"), str) or not step["id"].strip(): raise ValueError("step id required")
        step_id = step["id"]; ids.append(step_id)
        deps = step.get("dependsOn", [])
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps): raise ValueError(f"invalid dependsOn: {step_id}")
        executor = step.get("executor")
        if not isinstance(executor, dict) or executor.get("type") not in {"command", "ollama", "concat"}: raise ValueError(f"invalid executor: {step_id}")
        if executor["type"] == "command" and (not isinstance(executor.get("argv"), list) or not executor["argv"] or any(not isinstance(x, str) for x in executor["argv"])): raise ValueError(f"command argv required: {step_id}")
        if executor["type"] == "ollama":
            if not isinstance(executor.get("model"), str) or not executor.get("output"): raise ValueError(f"ollama model/output required: {step_id}")
            if not executor.get("prompt") and not executor.get("promptFile"): raise ValueError(f"ollama prompt required: {step_id}")
            include_files = executor.get("includeFiles", [])
            if not isinstance(include_files, list) or any(not isinstance(x, str) for x in include_files): raise ValueError(f"invalid ollama includeFiles: {step_id}")
        if executor["type"] == "concat":
            if not isinstance(executor.get("inputs"), list) or not executor["inputs"] or any(not isinstance(x, str) for x in executor["inputs"]): raise ValueError(f"concat inputs required: {step_id}")
            if not isinstance(executor.get("output"), str) or not executor["output"]: raise ValueError(f"concat output required: {step_id}")
        validator = step.get("validator")
        if validator is not None and (not isinstance(validator, dict) or not isinstance(validator.get("argv"), list) or not validator["argv"] or any(not isinstance(x, str) for x in validator["argv"])): raise ValueError(f"invalid validator: {step_id}")
        outputs = step.get("outputs", [])
        if not isinstance(outputs, list) or any(not isinstance(x, str) for x in outputs): raise ValueError(f"invalid outputs: {step_id}")
        maximum = step.get("maximumAttempts", 2)
        if type(maximum) is not int or maximum < 1 or maximum > 20: raise ValueError(f"invalid maximumAttempts: {step_id}")
    if len(ids) != len(set(ids)): raise ValueError("duplicate step id")
    known = set(ids)
    for step in steps:
        if any(dep not in known or dep == step["id"] for dep in step.get("dependsOn", [])): raise ValueError(f"invalid dependency: {step['id']}")
    visiting, visited = set(), set(); by_id = {x["id"]: x for x in steps}
    def visit(step_id):
        if step_id in visiting: raise ValueError("dependency cycle")
        if step_id in visited: return
        visiting.add(step_id)
        for dep in by_id[step_id].get("dependsOn", []): visit(dep)
        visiting.remove(step_id); visited.add(step_id)
    for step_id in ids: visit(step_id)
    return copy.deepcopy(value)

class Workflow:
    def __init__(self, root, task_id):
        self.root = Path(root).resolve(); self.task_id = task_id
        self.base = self.root / ".cogent" / "workflows" / task_id
        self.state_path = self.base / "state.json"; self.manifest_path = self.base / "manifest.json"
        self.ledger_path = self.base / "ledger.jsonl"; self.lock_path = self.base / ".lock"
        self.owner_path = self.base / "owner.json"; self.completion_path = self.base / "completion.json"
        self.controller_out = self.base / "controller.stdout.log"; self.controller_err = self.base / "controller.stderr.log"
    def read(self, path): return json.loads(path.read_text(encoding="utf-8"))
    def state(self): return self.read(self.state_path)
    def manifest(self): return self.read(self.manifest_path)
    def event(self, kind, summary, data=None):
        records = []
        if self.ledger_path.exists(): records = [json.loads(x) for x in self.ledger_path.read_text(encoding="utf-8").splitlines() if x.strip()]
        record = {"sequence": len(records)+1, "timestamp": now(), "taskId": self.task_id, "type": kind, "summary": summary, "data": data or {}}
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8", newline="\n") as handle: handle.write(json.dumps(record, ensure_ascii=False) + "\n"); handle.flush(); os.fsync(handle.fileno())
        return record
    def save(self, state): state["updatedAt"] = now(); state["revision"] = int(state.get("revision", 0))+1; atomic_json(self.state_path, state)

def queue_terminal_completion(flow, state):
    if state.get("status") not in TERMINAL or not flow.owner_path.is_file() or flow.completion_path.exists(): return None
    owner = flow.read(flow.owner_path)
    session_key = owner.get("ownerSessionKey")
    if not isinstance(session_key, str) or not session_key.strip(): return None
    notice = {"schemaVersion":1,"taskId":flow.task_id,"ownerSessionKey":session_key,"workflowStatus":state["status"],
              "stateRevision":state.get("revision"),"createdAt":now(),"deliveryStatus":"pending"}
    atomic_json(flow.completion_path, notice)
    flow.event("WORKFLOW_COMPLETION_QUEUED", "Terminal workflow result queued for owner continuation",
               {"workflowStatus":state["status"],"stateRevision":state.get("revision")})
    return notice

def bind_owner(root, task_id, session_key):
    if not isinstance(session_key, str) or not session_key.strip() or len(session_key) > 512: raise ValueError("valid owner session key required")
    flow = Workflow(root, task_id)
    with lock(flow.lock_path):
        state = flow.state()
        if state.get("status") not in {"ready", "completed", "blocked", "failed", "cancelled"}:
            raise ValueError("owner binding cannot change while workflow execution is active")
        binding = {"schemaVersion":1,"taskId":task_id,"ownerSessionKey":session_key.strip(),"boundAt":now()}
        atomic_json(flow.owner_path, binding)
        state["ownerMode"] = "session"
        flow.save(state)
        flow.event("WORKFLOW_OWNER_BOUND", "Workflow bound to an owner session")
        notice = queue_terminal_completion(flow, state)
    return {"binding":binding,"completion":notice}

def initialize(root, manifest_file, owner_session_key=None, operator_unbound=False, operator_reason=None):
    if bool(owner_session_key) == bool(operator_unbound):
        raise ValueError("initialize requires exactly one of owner_session_key or operator_unbound")
    if operator_unbound and (not isinstance(operator_reason, str) or len(operator_reason.strip()) < 8):
        raise ValueError("operator-unbound workflows require an audit reason of at least 8 characters")
    if owner_session_key and (not isinstance(owner_session_key, str) or not owner_session_key.strip() or len(owner_session_key) > 512):
        raise ValueError("valid owner session key required")
    manifest = validate_manifest(json.loads(Path(manifest_file).read_text(encoding="utf-8")))
    flow = Workflow(root, manifest["taskId"])
    flow.base.mkdir(parents=True, exist_ok=True)
    with lock(flow.lock_path):
        if flow.state_path.exists(): raise ValueError("workflow already exists")
        atomic_json(flow.manifest_path, manifest)
        if owner_session_key:
            atomic_json(flow.owner_path, {"schemaVersion":1,"taskId":manifest["taskId"],"ownerSessionKey":owner_session_key.strip(),"boundAt":now()})
        steps = {s["id"]: {"status":"pending","attempts":0,"artifacts":{},"lastError":None,"startedAt":None,"completedAt":None} for s in manifest["steps"]}
        mode = "session" if owner_session_key else "operator-unbound"
        state = {"schemaVersion":1,"taskId":manifest["taskId"],"manifestHash":digest(manifest),"status":"ready","revision":1,"ownerMode":mode,"steps":steps,"createdAt":now(),"updatedAt":now()}
        atomic_json(flow.state_path, state)
        flow.event("WORKFLOW_CREATED", "Workflow initialized", {"manifestHash":state["manifestHash"],"ownerMode":mode,"operatorReason":operator_reason.strip() if operator_unbound else None})
    return flow.state()

def run_argv(argv, cwd, timeout, on_started=None):
    start = time.perf_counter()
    try:
        proc = subprocess.Popen([str(x) for x in argv], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, shell=False)
        if on_started: on_started(proc.pid)
        stdout, stderr = proc.communicate(timeout=timeout)
        return {"ok":proc.returncode==0,"exitCode":proc.returncode,"stdout":stdout[-12000:],"stderr":stderr[-12000:],"seconds":round(time.perf_counter()-start,3),"pid":proc.pid}
    except subprocess.TimeoutExpired as exc:
        proc.kill(); stdout, stderr = proc.communicate()
        return {"ok":False,"exitCode":None,"stdout":str(stdout or exc.stdout or "")[-12000:],"stderr":str(stderr or "timeout")[-12000:],"seconds":round(time.perf_counter()-start,3),"pid":proc.pid}

def run_ollama(executor, cwd, timeout):
    prompt = executor.get("prompt")
    if executor.get("promptFile"): prompt = confined_path(cwd, executor["promptFile"]).read_text(encoding="utf-8")
    included = []
    for value in executor.get("includeFiles", []):
        included.append(f"\n\n--- Included file: {value} ---\n{confined_path(cwd, value).read_text(encoding='utf-8')}")
    prompt = str(prompt or "") + "".join(included)
    payload = json.dumps({"model":executor["model"],"prompt":prompt,"stream":False,"think":bool(executor.get("think",False)),"options":executor.get("options",{})}).encode()
    request = urllib.request.Request(executor.get("url","http://127.0.0.1:11434/api/generate"), data=payload, headers={"Content-Type":"application/json"})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response: data = json.load(response)
        output = confined_path(cwd, executor["output"]); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(data.get("response", ""), encoding="utf-8")
        return {"ok":True,"exitCode":0,"stdout":"","stderr":"","seconds":round(time.perf_counter()-start,3),"evalCount":data.get("eval_count")}
    except Exception as exc:
        return {"ok":False,"exitCode":None,"stdout":"","stderr":str(exc)[-12000:],"seconds":round(time.perf_counter()-start,3)}

def run_concat(executor, cwd):
    start = time.perf_counter()
    try:
        chunks = [confined_path(cwd, value).read_text(encoding="utf-8") for value in executor["inputs"]]
        output = confined_path(cwd, executor["output"]); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n\n".join(chunks), encoding="utf-8")
        return {"ok":True,"exitCode":0,"stdout":"","stderr":"","seconds":round(time.perf_counter()-start,3)}
    except Exception as exc:
        return {"ok":False,"exitCode":None,"stdout":"","stderr":str(exc)[-12000:],"seconds":round(time.perf_counter()-start,3)}

def confined_path(root, value):
    base = Path(root).resolve()
    path = (base / value).resolve()
    if path != base and base not in path.parents: raise ValueError(f"path escapes workflow root: {value}")
    return path

def artifact_hashes(root, outputs):
    found = {}
    for value in outputs:
        path = confined_path(root, value)
        if not path.is_file(): raise ValueError(f"missing output: {value}")
        found[value] = {"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size}
    return found

def inspect_workflow(root, task_id):
    flow = Workflow(root, task_id)
    state, manifest = flow.state(), flow.manifest()
    manifest_ok = digest(manifest) == state.get("manifestHash")
    controller_pid = state.get("controllerPid")
    controller_alive = process_alive(controller_pid)
    steps = []
    artifacts_ok = True
    any_runner_alive = False
    manifest_steps = {step["id"]: step for step in manifest.get("steps", [])}
    for step_id, current in state.get("steps", {}).items():
        configured = manifest_steps.get(step_id, {})
        runner_pid = current.get("runnerPid")
        runner_alive = process_alive(runner_pid)
        any_runner_alive = any_runner_alive or runner_alive
        checks = []
        for output in configured.get("outputs", []):
            expected = current.get("artifacts", {}).get(output)
            path = confined_path(flow.root, output)
            actual = None
            if path.is_file():
                actual = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
            matches = expected is not None and actual == expected
            if current.get("status") == "completed" and not matches: artifacts_ok = False
            checks.append({"path": output, "exists": path.is_file(), "matchesRecordedHash": matches,
                           "expected": expected, "actual": actual})
        steps.append({"id": step_id, "status": current.get("status"), "attempts": current.get("attempts", 0),
                      "maximumAttempts": configured.get("maximumAttempts", 2), "runnerPid": runner_pid,
                      "runnerAlive": runner_alive, "startedAt": current.get("startedAt"),
                      "completedAt": current.get("completedAt"), "lastError": current.get("lastError"),
                      "artifacts": checks})
    ledger = []
    if flow.ledger_path.exists():
        ledger = [json.loads(line) for line in flow.ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    status = state.get("status")
    completed_verified = status == "completed" and manifest_ok and artifacts_ok and all(x["status"] == "completed" for x in steps)
    if completed_verified: condition, normal = "completed_verified", True
    elif status == "running" and (controller_alive or any_runner_alive): condition, normal = "running_active", True
    elif status in {"ready", "pending"}: condition, normal = "queued", True
    elif status == "running": condition, normal = "stale_worker", False
    elif status == "blocked": condition, normal = "blocked", False
    elif status == "failed": condition, normal = "failed", False
    elif status == "completed": condition, normal = "completed_unverified", False
    else: condition, normal = str(status or "unknown"), False
    return {"schemaVersion": 1, "taskId": task_id, "condition": condition, "normal": normal,
            "workflowStatus": status, "completionVerified": completed_verified,
            "stateRevision": state.get("revision"), "updatedAt": state.get("updatedAt"),
            "manifestIntegrity": manifest_ok, "artifactIntegrity": artifacts_ok,
            "controller": {"pid": controller_pid, "alive": controller_alive},
            "runnerAlive": any_runner_alive, "steps": steps,
            "lastEvent": ledger[-1] if ledger else None,
            "evidence": {"state": str(flow.state_path), "manifest": str(flow.manifest_path),
                         "ledger": str(flow.ledger_path), "controllerStdout": str(flow.controller_out),
                         "controllerStderr": str(flow.controller_err)}}

def choose_step(manifest, state):
    for step in manifest["steps"]:
        current = state["steps"][step["id"]]
        if current["status"] != "pending": continue
        deps = [state["steps"][x]["status"] for x in step.get("dependsOn", [])]
        if all(x == "completed" for x in deps): return step
    return None

def process_alive(pid):
    if not isinstance(pid, int) or pid <= 0: return False
    if os.name == "nt":
        import ctypes
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if not handle: return False
        exit_code = ctypes.c_ulong()
        queried = ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(handle)
        return bool(queried) and exit_code.value == 259  # STILL_ACTIVE
    stat = Path(f"/proc/{pid}/stat")
    if stat.exists():
        try:
            # A finished child can remain waitable as a Unix zombie; it owns no work.
            if stat.read_text(encoding="utf-8").split(") ",1)[1].split(" ",1)[0] == "Z": return False
        except (OSError, IndexError): pass
    try: os.kill(pid, 0); return True
    except PermissionError: return True
    except (OSError, ProcessLookupError): return False

def reconcile_interrupted(flow, manifest, state):
    changed = False
    for step in manifest["steps"]:
        current = state["steps"][step["id"]]
        if current["status"] != "running": continue
        if process_alive(current.get("runnerPid")):
            return state, True
        validator = step.get("validator")
        if validator:
            result = run_argv(validator["argv"], flow.root, int(validator.get("timeoutSeconds",60)))
            if result["ok"]:
                try: current["artifacts"] = artifact_hashes(flow.root, step.get("outputs",[])); current["status"]="completed"; current["completedAt"]=now(); changed=True; flow.event("STEP_RECOVERED", f"Recovered completed step {step['id']}", {"validator":result}); continue
                except ValueError: pass
        if step.get("idempotent", False): current["status"]="pending"; current["lastError"]="interrupted; safe retry"; changed=True; flow.event("STEP_REQUEUED", f"Requeued interrupted step {step['id']}")
        else: current["status"]="blocked"; current["lastError"]="interrupted non-idempotent step requires review"; state["status"]="blocked"; changed=True; flow.event("STEP_BLOCKED", f"Interrupted non-idempotent step {step['id']}")
    if changed: flow.save(state)
    return state, False

def tick(root, task_id):
    flow = Workflow(root, task_id)
    with lock(flow.lock_path):
        manifest, state = flow.manifest(), flow.state()
        if digest(manifest) != state["manifestHash"]: raise ValueError("manifest integrity mismatch")
        state, worker_active = reconcile_interrupted(flow, manifest, state)
        if worker_active: return {"transition":"busy","state":state}
        if state["status"] in TERMINAL: return {"transition":"terminal","state":state}
        step = choose_step(manifest, state)
        if not step:
            statuses = [x["status"] for x in state["steps"].values()]
            if all(x == "completed" for x in statuses): state["status"]="completed"; flow.event("WORKFLOW_COMPLETED","All steps verified")
            elif any(x == "blocked" for x in statuses): state["status"]="blocked"
            else: state["status"]="failed"; flow.event("WORKFLOW_FAILED","No runnable step")
            flow.save(state); queue_terminal_completion(flow,state); return {"transition":"terminal","state":state}
        current = state["steps"][step["id"]]; current["status"]="running"; current["attempts"]+=1; current["startedAt"]=now(); current["runnerPid"]=None; current["controllerPid"]=os.getpid(); state["status"]="running"; flow.save(state); flow.event("STEP_STARTED",f"Started {step['id']}",{"attempt":current["attempts"],"controllerPid":os.getpid()})
    executor = step["executor"]; timeout = int(executor.get("timeoutSeconds",1800))
    def record_runner(pid):
        with lock(flow.lock_path):
            live = flow.state(); running = live["steps"][step["id"]]
            if running.get("status") != "running": raise RuntimeError("step execution ownership changed before child start")
            running["runnerPid"] = pid; flow.save(live)
            flow.event("STEP_PROCESS_STARTED", f"Child process started for {step['id']}", {"runnerPid":pid,"controllerPid":os.getpid()})
    if executor["type"] == "command": result = run_argv(executor["argv"], flow.root, timeout, record_runner)
    elif executor["type"] == "ollama": result = run_ollama(executor, flow.root, timeout)
    else: result = run_concat(executor, flow.root)
    validator_result = None
    if result["ok"] and step.get("validator"): validator_result = run_argv(step["validator"]["argv"], flow.root, int(step["validator"].get("timeoutSeconds",60))); result["ok"] = validator_result["ok"]
    with lock(flow.lock_path):
        state = flow.state(); current = state["steps"][step["id"]]
        current["runnerPid"] = None
        if result["ok"]:
            try: current["artifacts"] = artifact_hashes(flow.root, step.get("outputs",[]))
            except ValueError as exc: result["ok"]=False; result["stderr"]=str(exc)
        if result["ok"]:
            current.update(status="completed",completedAt=now(),lastError=None); flow.event("STEP_COMPLETED",f"Verified {step['id']}",{"execution":result,"validator":validator_result,"artifacts":current["artifacts"]})
        else:
            current["lastError"] = (validator_result or result).get("stderr") or (validator_result or result).get("stdout") or "execution failed"
            maximum = int(step.get("maximumAttempts",2))
            current["status"] = "pending" if current["attempts"] < maximum else "blocked"
            flow.event("STEP_FAILED",f"Step {step['id']} failed",{"attempt":current["attempts"],"maximum":maximum,"execution":result,"validator":validator_result})
            if current["status"] == "blocked": state["status"]="blocked"
        flow.save(state)
        if state["status"] in TERMINAL: queue_terminal_completion(flow,state)
    return {"transition":"continue" if state["status"] not in TERMINAL else "terminal","step":step["id"],"state":state}

def claim_controller(flow):
    with lock(flow.lock_path):
        state = flow.state(); owner = state.get("controllerPid")
        mode = state.get("ownerMode")
        if mode == "session" and not flow.owner_path.is_file(): raise ValueError("session-owned workflow is missing owner binding")
        if mode not in {"session", "operator-unbound"}: raise ValueError("workflow lacks enforced ownership mode")
        if process_alive(owner) and owner != os.getpid(): return False, state
        state["controllerPid"] = os.getpid(); state["controllerStartedAt"] = now(); flow.save(state)
        flow.event("CONTROLLER_CLAIMED", "Workflow controller claimed", {"pid":os.getpid()})
        return True, state

def release_controller(flow):
    with lock(flow.lock_path):
        state = flow.state()
        if state.get("controllerPid") == os.getpid():
            state["controllerPid"] = None; state["controllerFinishedAt"] = now(); flow.save(state); queue_terminal_completion(flow,state)
            flow.event("CONTROLLER_RELEASED", "Workflow controller released", {"pid":os.getpid(),"status":state.get("status")})

def run_workflow(root, task_id, maximum_ticks=100):
    flow = Workflow(root, task_id); claimed, state = claim_controller(flow)
    if not claimed: return {"status":"busy","history":[],"state":state}
    history = []
    try:
        for _ in range(maximum_ticks):
            result = tick(root, task_id); history.append({"transition":result["transition"],"step":result.get("step")})
            if result["state"]["status"] in TERMINAL: return {"status":result["state"]["status"],"history":history,"state":result["state"]}
            if result["transition"] == "busy": return {"status":"busy","history":history,"state":result["state"]}
        raise RuntimeError("maximum workflow ticks exceeded")
    finally: release_controller(flow)

def discover_workflows(root):
    base = Path(root).resolve() / ".cogent" / "workflows"; found = []
    if not base.is_dir(): return found
    for directory in sorted(path for path in base.iterdir() if path.is_dir()):
        try:
            flow = Workflow(root, directory.name); state = flow.state(); manifest = flow.manifest()
            if digest(manifest) != state.get("manifestHash"): raise ValueError("manifest integrity mismatch")
            controller = state.get("controllerPid"); status = state.get("status")
            runner_alive = any(process_alive(step.get("runnerPid")) for step in state.get("steps",{}).values() if step.get("status") == "running")
            found.append({"taskId":directory.name,"status":status,"controllerPid":controller,"controllerAlive":process_alive(controller),"runnerAlive":runner_alive,"resumable":status not in TERMINAL})
        except Exception as exc: found.append({"taskId":directory.name,"status":"invalid","resumable":False,"error":str(exc)})
    return found

def launch_controller(root, task_id):
    flow = Workflow(root, task_id); command = [sys.executable,str(Path(__file__).resolve()),"--root",str(Path(root).resolve()),"run",task_id]
    flags = 0; kwargs = {}
    if os.name == "nt": flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    else: kwargs["start_new_session"] = True
    stdout = flow.controller_out.open("a",encoding="utf-8"); stderr = flow.controller_err.open("a",encoding="utf-8")
    try: child = subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,close_fds=True,creationflags=flags,**kwargs)
    finally: stdout.close(); stderr.close()
    with lock(flow.lock_path): flow.event("CONTROLLER_LAUNCHED", "Detached workflow controller launched", {"pid":child.pid})
    return {"taskId":task_id,"pid":child.pid}

def supervise_workflows(root, execute=False, maximum=4):
    workflows = discover_workflows(root); actions = []
    for item in workflows:
        if len(actions) >= maximum: break
        if not item.get("resumable") or item.get("controllerAlive") or item.get("runnerAlive"): continue
        actions.append(launch_controller(root,item["taskId"]) if execute else {"taskId":item["taskId"],"action":"would-launch"})
    return {"status":"launched" if execute and actions else "observed","workflowCount":len(workflows),"actions":actions,"workflows":workflows}

def self_test():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); manifest = root / "manifest.json"
        py = sys.executable
        value = {"schemaVersion":1,"taskId":"WF-TEST","goal":"autonomous chain","steps":[
            {"id":"one","executor":{"type":"command","argv":[py,"-c","from pathlib import Path;Path('one.txt').write_text('one')"]},"outputs":["one.txt"],"validator":{"argv":[py,"-c","from pathlib import Path;assert Path('one.txt').read_text()=='one'"]},"idempotent":True},
            {"id":"two","dependsOn":["one"],"executor":{"type":"command","argv":[py,"-c","from pathlib import Path;Path('two.txt').write_text(Path('one.txt').read_text()+' two')"]},"outputs":["two.txt"],"validator":{"argv":[py,"-c","from pathlib import Path;assert Path('two.txt').read_text()=='one two'"]},"idempotent":True}
        ]}
        manifest.write_text(json.dumps(value),encoding="utf-8")
        try: initialize(root,manifest)
        except ValueError as exc: assert "exactly one" in str(exc)
        else: raise AssertionError("unenforced initialization unexpectedly succeeded")
        initialize(root,manifest,operator_unbound=True,operator_reason="self-test operator workflow"); result=run_workflow(root,"WF-TEST")
        assert result["status"]=="completed" and (root/"two.txt").read_text()=="one two"
        inspection=inspect_workflow(root,"WF-TEST"); assert inspection["normal"] and inspection["completionVerified"] and inspection["artifactIntegrity"]
        (root/"two.txt").write_text("tampered")
        inspection=inspect_workflow(root,"WF-TEST"); assert not inspection["normal"] and inspection["condition"]=="completed_unverified"
        # Simulate owner interruption after a child produced valid output.
        flow=Workflow(root,"WF-TEST-RECOVER"); value["taskId"]="WF-TEST-RECOVER"; value["steps"]=value["steps"][:1]; manifest.write_text(json.dumps(value),encoding="utf-8"); initialize(root,manifest,operator_unbound=True,operator_reason="self-test recovery")
        state=flow.state(); state["steps"]["one"]["status"]="running"; state["steps"]["one"]["runnerPid"]=99999999; (root/"one.txt").write_text("one"); flow.save(state)
        recovered=tick(root,"WF-TEST-RECOVER"); assert recovered["state"]["status"]=="completed"
        # A live worker is fenced: another tick observes it but never executes it twice.
        value["taskId"]="WF-TEST-BUSY"; manifest.write_text(json.dumps(value),encoding="utf-8"); initialize(root,manifest,operator_unbound=True,operator_reason="self-test busy fencing")
        busy_flow=Workflow(root,"WF-TEST-BUSY"); state=busy_flow.state(); state["steps"]["one"]["status"]="running"; state["steps"]["one"]["runnerPid"]=os.getpid(); busy_flow.save(state)
        busy=tick(root,"WF-TEST-BUSY"); assert busy["transition"]=="busy" and busy["state"]["steps"]["one"]["attempts"]==0
        # A failed validation is retried only up to the declared ceiling.
        value["taskId"]="WF-TEST-RETRY"; value["steps"][0]["validator"]={"argv":[py,"-c","raise SystemExit(1)"]}; value["steps"][0]["maximumAttempts"]=2
        manifest.write_text(json.dumps(value),encoding="utf-8"); initialize(root,manifest,operator_unbound=True,operator_reason="self-test retry ceiling"); failed=run_workflow(root,"WF-TEST-RETRY")
        assert failed["status"]=="blocked" and failed["state"]["steps"]["one"]["attempts"]==2
        # Deterministic discovery launches a detached controller that survives the caller.
        value["taskId"]="WF-TEST-SUPERVISE"; value["steps"][0]["validator"]={"argv":[py,"-c","from pathlib import Path;assert Path('one.txt').read_text()=='one'"]}; value["steps"][0]["maximumAttempts"]=2
        (root/"one.txt").unlink(missing_ok=True); manifest.write_text(json.dumps(value),encoding="utf-8"); initialize(root,manifest,owner_session_key="agent:main:test-owner")
        observed=supervise_workflows(root); assert any(x.get("taskId")=="WF-TEST-SUPERVISE" for x in observed["actions"])
        launched=supervise_workflows(root,execute=True,maximum=1); child_pid=launched["actions"][0]["pid"]; deadline=time.monotonic()+10
        while time.monotonic()<deadline and Workflow(root,"WF-TEST-SUPERVISE").state()["status"]!="completed": time.sleep(.05)
        if os.name != "nt":
            try: os.waitpid(child_pid,0)
            except ChildProcessError: pass
        else:
            while time.monotonic()<deadline and process_alive(child_pid): time.sleep(.05)
        assert Workflow(root,"WF-TEST-SUPERVISE").state()["status"]=="completed" and not process_alive(child_pid)
        notice=Workflow(root,"WF-TEST-SUPERVISE").read(Workflow(root,"WF-TEST-SUPERVISE").completion_path)
        assert notice["deliveryStatus"]=="pending" and Workflow(root,"WF-TEST-SUPERVISE").owner_path.is_file()
        # Killing the controller must not cause a still-live command child to run twice.
        value["taskId"]="WF-TEST-KILLED-CONTROLLER"
        value["steps"][0]["executor"]={"type":"command","argv":[py,"-c","import time;from pathlib import Path;time.sleep(1);Path('killed.txt').write_text('survived')"]}
        value["steps"][0]["outputs"]=["killed.txt"]
        value["steps"][0]["validator"]={"argv":[py,"-c","from pathlib import Path;assert Path('killed.txt').read_text()=='survived'"]}
        manifest.write_text(json.dumps(value),encoding="utf-8")
        initialize(root,manifest,operator_unbound=True,operator_reason="self-test killed controller")
        controller=subprocess.Popen([py,str(Path(__file__).resolve()),"--root",str(root),"run",value["taskId"]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        killed_flow=Workflow(root,value["taskId"]); deadline=time.monotonic()+5; runner_pid=None
        while time.monotonic()<deadline:
            runner_pid=killed_flow.state()["steps"]["one"].get("runnerPid")
            if runner_pid and runner_pid != controller.pid: break
            time.sleep(.05)
        assert runner_pid and runner_pid != controller.pid and process_alive(runner_pid)
        controller.terminate(); controller.wait(timeout=5)
        fenced=supervise_workflows(root,execute=True,maximum=1)
        observed=next(x for x in fenced["workflows"] if x.get("taskId")==value["taskId"])
        assert observed["runnerAlive"] and not any(x.get("taskId")==value["taskId"] for x in fenced["actions"])
        deadline=time.monotonic()+5
        while time.monotonic()<deadline and process_alive(runner_pid): time.sleep(.05)
        recovered=run_workflow(root,value["taskId"])
        final_killed=killed_flow.state()
        assert recovered["status"]=="completed" and final_killed["steps"]["one"]["attempts"]==1, {"recovered":recovered,"final":final_killed,"artifactExists":(root/"killed.txt").exists()}
        # Admission assembly uses the portable concat executor.
        value={"schemaVersion":1,"taskId":"WF-TEST-CONCAT","goal":"assemble validated components","steps":[
            {"id":"left","executor":{"type":"command","argv":[py,"-c","from pathlib import Path;Path('left.txt').write_text('left')"]},"outputs":["left.txt"],"idempotent":True},
            {"id":"right","executor":{"type":"command","argv":[py,"-c","from pathlib import Path;Path('right.txt').write_text('right')"]},"outputs":["right.txt"],"idempotent":True},
            {"id":"assemble","dependsOn":["left","right"],"executor":{"type":"concat","inputs":["left.txt","right.txt"],"output":"assembled.txt"},"outputs":["assembled.txt"],"idempotent":True}
        ]}
        manifest.write_text(json.dumps(value),encoding="utf-8")
        initialize(root,manifest,operator_unbound=True,operator_reason="self-test concat workflow")
        assembled=run_workflow(root,value["taskId"])
        assert assembled["status"]=="completed" and (root/"assembled.txt").read_text()=="left\n\nright"
    print("Cogent workflow self-test: PASS")

def parser():
    p=argparse.ArgumentParser(description="CogentNexus deterministic workflow engine"); p.add_argument("--root",type=Path,default=Path.cwd()); sub=p.add_subparsers(dest="command",required=True)
    v=sub.add_parser("validate"); v.add_argument("manifest",type=Path)
    i=sub.add_parser("init"); i.add_argument("manifest",type=Path); i.add_argument("--owner-session-key"); i.add_argument("--operator-unbound",action="store_true"); i.add_argument("--operator-reason")
    for name in ("tick","run","status","inspect"):
        x=sub.add_parser(name); x.add_argument("task_id")
    b=sub.add_parser("bind-owner"); b.add_argument("task_id"); b.add_argument("--session-key",required=True)
    s=sub.add_parser("supervise"); s.add_argument("--execute",action="store_true"); s.add_argument("--maximum",type=int,default=4)
    sub.add_parser("self-test"); return p

def main():
    args=parser().parse_args()
    conversational = bool(os.environ.get("CODEX_THREAD_ID"))
    if conversational and ((args.command == "init" and args.operator_unbound) or args.command == "bind-owner"):
        raise SystemExit("CogentNexus Enforced Mode: conversational workflows must use cogent_workflow_start with trusted owner binding")
    if args.command=="validate": emit({"valid":True,"manifest":validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))}); return
    if args.command=="init": emit(initialize(args.root,args.manifest,args.owner_session_key,args.operator_unbound,args.operator_reason)); return
    if args.command=="tick": emit(tick(args.root,args.task_id)); return
    if args.command=="run": emit(run_workflow(args.root,args.task_id)); return
    if args.command=="status": emit(Workflow(args.root,args.task_id).state()); return
    if args.command=="inspect": emit(inspect_workflow(args.root,args.task_id)); return
    if args.command=="bind-owner": emit(bind_owner(args.root,args.task_id,args.session_key)); return
    if args.command=="supervise": emit(supervise_workflows(args.root,args.execute,args.maximum)); return
    if args.command=="self-test": self_test(); return

if __name__=="__main__": main()

