#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_ROOT = WORKSPACE / ".cogent"
OUTPUT_LIMIT = 3000

DEFAULT_CONFIG = {
    "schemaVersion": 1,
    "supervisor": {
        "intervalSeconds": 300,
        "commandTimeoutSeconds": 30,
        "confirmDelaySeconds": 1,
        "verifyDelaySeconds": 3,
        "cooldownSeconds": 300,
        "maximumRecoveriesPerHour": 3,
        "ollamaMode": "auto",
        "allowOllamaStart": False
    },
    "concurrency": {
        "mode": "fixed",
        "inferenceLanes": 1,
        "maxInferenceLanes": 1,
        "executionLanes": 2,
        "verificationLanes": 2,
        "supervisorLanes": 1,
        "minimumFreeMemoryGB": 2,
        "leaseSeconds": 1800
    },
    "contextContinuity": {
        "softLimit": 0.25,
        "handoffLimit": 0.35,
        "criticalLimit": 0.45,
        "reserveTokens": 16384,
        "leaseSeconds": 1800,
        "autoMonitor": True
    },
    "workflowAutomation": {
        "enabled": True,
        "maximumLaunchesPerTick": 2
    }
}

def now():
    return datetime.now(timezone.utc).isoformat()

def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def read_json(path, default=None):
    if not path.exists():
        if default is not None:
            return default
        raise SystemExit(f"missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def deep_merge(base, override):
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def runtime_dir(root):
    return root.resolve() / "runtime"

def config_path(root):
    return runtime_dir(root) / "config.json"

def load_config(root):
    path = config_path(root)
    if not path.exists():
        atomic_json(path, DEFAULT_CONFIG)
    return deep_merge(DEFAULT_CONFIG, read_json(path))

@contextmanager
def file_lock(path, timeout=5, stale=120):
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, json.dumps({"pid": os.getpid(), "createdAt": now()}).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - path.stat().st_mtime > stale:
                    path.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError(f"lock timeout: {path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass

def append_runtime_event(root, event_type, summary, data=None):
    base = runtime_dir(root)
    ledger = base / "ledger.jsonl"
    with file_lock(base / ".ledger.lock"):
        records = ledger.read_text(encoding="utf-8").splitlines() if ledger.exists() else []
        event = {
            "sequence": len([line for line in records if line.strip()]) + 1,
            "timestamp": now(),
            "type": event_type,
            "summary": summary,
            "data": data or {}
        }
        with ledger.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    return event

def background_options():
    return (
        {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}
        if os.name == "nt"
        else {"start_new_session": True}
    )

def run_command(argv, timeout=30):
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            **background_options(),
        )
        return {
            "ok": proc.returncode == 0,
            "exitCode": proc.returncode,
            "durationMs": round((time.monotonic() - started) * 1000),
            "stdout": proc.stdout[-OUTPUT_LIMIT:],
            "stderr": proc.stderr[-OUTPUT_LIMIT:]
        }
    except Exception as exc:
        return {"ok": False, "durationMs": round((time.monotonic() - started) * 1000), "error": str(exc)}

def memory_info():
    result = {"availableBytes": None, "totalBytes": None}
    if os.name == "nt":
        command = "(Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json -Compress)"
        proc = run_command(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command], 10)
        if proc["ok"]:
            value = json.loads(proc["stdout"])
            return {"availableBytes": int(value["FreePhysicalMemory"]) * 1024, "totalBytes": int(value["TotalVisibleMemorySize"]) * 1024}
    elif Path("/proc/meminfo").exists():
        values = {}
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            key, value = line.split(":", 1)
            values[key] = int(value.strip().split()[0]) * 1024
        return {"availableBytes": values.get("MemAvailable"), "totalBytes": values.get("MemTotal")}
    elif sys.platform == "darwin":
        total = run_command(["sysctl", "-n", "hw.memsize"], 5)
        if total["ok"]:
            result["totalBytes"] = int(total["stdout"].strip())
    return result

def openclaw_executable():
    for name in ("openclaw", "openclaw.cmd"):
        found = shutil.which(name)
        if found:
            return found
    return None

def gateway_status_healthy(result):
    """Interpret OpenClaw status output, whose exit code may be zero while stopped."""
    if not result.get("ok"):
        return False
    output = f'{result.get("stdout", "")}\n{result.get("stderr", "")}'.lower()
    negative_markers = (
        "connectivity probe: failed",
        "runtime: stopped",
        "service is loaded but not running",
        "econnrefused",
    )
    if any(marker in output for marker in negative_markers):
        return False
    return "connectivity probe: ok" in output

def gateway_probe(timeout, fixture=None):
    if fixture in ("gateway-fail", "all-fail"):
        return {"name": "gateway", "enabled": True, "healthy": False, "evidence": "fixture"}
    if fixture is not None:
        return {"name": "gateway", "enabled": True, "healthy": True, "evidence": "fixture"}
    executable = openclaw_executable()
    if not executable:
        return {"name": "gateway", "enabled": True, "healthy": False, "evidence": "openclaw CLI unavailable"}
    result = run_command([executable, "gateway", "status"], timeout)
    return {"name": "gateway", "enabled": True, "healthy": gateway_status_healthy(result), "evidence": result}

def ollama_probe(config, fixture=None):
    if config["supervisor"].get("ollamaMode") == "disabled":
        return {"name": "ollama", "enabled": False, "healthy": True, "evidence": "disabled"}
    executable = shutil.which("ollama")
    if config["supervisor"].get("ollamaMode") == "auto" and not executable:
        return {"name": "ollama", "enabled": False, "healthy": True, "evidence": "not installed"}
    if fixture in ("ollama-fail", "all-fail"):
        return {"name": "ollama", "enabled": True, "healthy": False, "evidence": "fixture"}
    if fixture is not None:
        return {"name": "ollama", "enabled": True, "healthy": True, "evidence": "fixture"}
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10) as response:
            healthy = response.status == 200
        return {"name": "ollama", "enabled": True, "healthy": healthy, "evidence": "http://127.0.0.1:11434/api/tags"}
    except Exception as exc:
        return {"name": "ollama", "enabled": True, "healthy": False, "evidence": str(exc)}

def resource_probe(root):
    disk = shutil.disk_usage(WORKSPACE)
    return {
        "name": "resources",
        "enabled": True,
        "healthy": disk.free > 512 * 1024 * 1024,
        "memory": memory_info(),
        "diskFreeBytes": disk.free
    }

def provider_probe(name, config, fixture=None):
    timeout = int(config["supervisor"]["commandTimeoutSeconds"])
    if name == "gateway":
        return gateway_probe(timeout, fixture)
    if name == "ollama":
        return ollama_probe(config, fixture)
    if fixture is not None:
        return {"name": "resources", "enabled": True, "healthy": fixture != "all-fail", "evidence": "fixture"}
    return resource_probe(DEFAULT_ROOT)

def recovery_allowed(component_state, config):
    current = datetime.now(timezone.utc)
    one_hour_ago = current - timedelta(hours=1)
    attempts = [value for value in component_state.get("attempts", []) if datetime.fromisoformat(value) >= one_hour_ago]
    last = component_state.get("lastRecoveryAt")
    cooldown = int(config["supervisor"]["cooldownSeconds"])
    cooled = not last or (current - datetime.fromisoformat(last)).total_seconds() >= cooldown
    maximum = int(config["supervisor"]["maximumRecoveriesPerHour"])
    return len(attempts) < maximum and cooled, attempts

def start_ollama_windows():
    # Prefer the server command directly: it is deterministic, headless, and is
    # the supported standalone/service entry point on Windows. Fall back to the
    # desktop application only when the CLI binary cannot be resolved.
    cli_candidates = [
        shutil.which("ollama"),
        str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"),
    ]
    for value in cli_candidates:
        if not value:
            continue
        candidate = Path(value)
        if candidate.is_file():
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            command = [str(candidate), "serve"]
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
            return {"ok": True, "command": command}
    app = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama app.exe"
    if app.is_file():
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen([str(app)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        return {"ok": True, "command": [str(app)]}
    return {"ok": False, "error": "Ollama application not found"}

def recover_component(name, config, explicit_authority=False):
    timeout = int(config["supervisor"]["commandTimeoutSeconds"])
    if name == "gateway":
        executable = openclaw_executable()
        return run_command([executable, "gateway", "start"], max(timeout, 60)) if executable else {"ok": False, "error": "openclaw CLI unavailable"}
    if name == "ollama" and (explicit_authority or config["supervisor"].get("allowOllamaStart")):
        if os.name == "nt":
            return start_ollama_windows()
        if shutil.which("systemctl"):
            return run_command(["systemctl", "--user", "start", "ollama"], max(timeout, 60))
        return {"ok": False, "error": "no supported Ollama start adapter"}
    return {"ok": False, "error": "no authorized recovery adapter"}

def maintenance_path(root):
    return runtime_dir(root) / "maintenance.json"

def maintenance_status(root):
    path = maintenance_path(root)
    return read_json(path) if path.exists() else None

def set_maintenance(root, reason, owner="operator", recovery_policy="manual"):
    if recovery_policy not in {"manual", "healthy-runtime"}:
        raise ValueError("maintenance recovery policy must be manual or healthy-runtime")
    marker = {"schemaVersion": 1, "active": True, "createdAt": now(), "reason": reason, "owner": owner,
              "recoveryPolicy": recovery_policy}
    atomic_json(maintenance_path(root), marker)
    append_runtime_event(root, "DECISION", "Intentional maintenance mode enabled", marker)
    return marker

def clear_maintenance(root):
    path = maintenance_path(root)
    previous = read_json(path) if path.exists() else None
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    append_runtime_event(root, "COMMIT", "Intentional maintenance mode cleared", {"previous": previous})
    return previous

def stop_ollama(config):
    timeout = int(config["supervisor"]["commandTimeoutSeconds"])
    if os.name == "nt":
        executable = shutil.which("taskkill")
        return run_command([executable, "/IM", "ollama.exe", "/T"], timeout) if executable else {"ok": False, "error": "taskkill unavailable"}
    if shutil.which("systemctl"):
        return run_command(["systemctl", "--user", "stop", "ollama"], max(timeout, 60))
    return {"ok": False, "error": "no managed Ollama stop adapter"}

def wait_for_runtime_health(config, timeout_seconds=30, require_ollama=True):
    """Poll bounded readiness for exactly the components requested by the caller."""
    deadline = time.monotonic() + max(0.0, float(timeout_seconds))
    attempts = 0
    verified = None
    while True:
        attempts += 1
        verified = {
            "gateway": gateway_probe(int(config["supervisor"]["commandTimeoutSeconds"])),
            "ollama": ollama_probe(config),
        }
        if verified["gateway"]["healthy"] and (not require_ollama or verified["ollama"]["healthy"]):
            return verified, attempts, True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return verified, attempts, False
        time.sleep(min(2.0, remaining))

def lifecycle_cmd(args):
    root = args.root.resolve()
    config = load_config(root)
    marker = maintenance_status(root)
    if args.command_name == "status":
        emit({"maintenance": marker, "gateway": gateway_probe(int(config["supervisor"]["commandTimeoutSeconds"])), "ollama": ollama_probe(config), "startupHint": "After login, native OpenClaw startup plus the CogentNexus supervisor normally restores runtime; use lifecycle start for an immediate verified start."})
        return 0
    if args.command_name == "prepare":
        emit({"maintenance": set_maintenance(root, args.reason, args.owner, args.recovery_policy), "safeToPowerOff": True})
        return 0
    if args.command_name == "cancel":
        emit({"cancelled": bool(clear_maintenance(root)), "maintenance": None})
        return 0
    if args.command_name == "stop":
        marker = marker or set_maintenance(root, args.reason, args.owner)
        executable = openclaw_executable()
        results = {"gateway": run_command([executable, "gateway", "stop"], 60) if executable else {"ok": False, "error": "openclaw CLI unavailable"}}
        if args.provider:
            results["ollama"] = stop_ollama(config)
        append_runtime_event(root, "ACTION", "Runtime stopped for intentional shutdown", {"providerRequested": bool(args.provider), "results": results})
        emit({"maintenance": marker, "results": results, "safeToPowerOff": bool(results["gateway"].get("ok"))})
        return 0 if results["gateway"].get("ok") else 2
    if args.command_name == "restart":
        marker = set_maintenance(root, args.reason, args.owner, "healthy-runtime")
        executable = openclaw_executable()
        result = run_command([executable, "gateway", "restart"], 60) if executable else {"ok": False, "error": "openclaw CLI unavailable"}
        append_runtime_event(root, "ACTION", "Recoverable Gateway restart requested", {"result": result})
        emit({"restartRequested": bool(result.get("ok")), "maintenance": marker, "result": result,
              "recovery": "The native supervisor will start and verify Gateway if this caller is interrupted."})
        return 0 if result.get("ok") else 2
    if args.command_name == "start":
        results = {}
        initial = {"gateway": gateway_probe(int(config["supervisor"]["commandTimeoutSeconds"])), "ollama": ollama_probe(config)}
        if args.provider and not initial["ollama"]["healthy"]:
            # --provider is an explicit operator/Host request. It authorizes this
            # bounded provider start without weakening autonomous supervisor fences.
            results["ollama"] = recover_component("ollama", config, explicit_authority=True)
        else:
            results["ollama"] = {"ok": True, "skipped": True, "reason": "already healthy"}
        if initial["gateway"]["healthy"]:
            results["gateway"] = {"ok": True, "skipped": True, "reason": "already healthy"}
        else:
            executable = openclaw_executable()
            results["gateway"] = run_command([executable, "gateway", "start"], 60) if executable else {"ok": False, "error": "openclaw CLI unavailable"}
        initial_delay = max(0.0, float(config["supervisor"]["verifyDelaySeconds"]))
        if initial_delay:
            time.sleep(initial_delay)
        verified, verification_attempts, healthy = wait_for_runtime_health(
            config, timeout_seconds=30, require_ollama=bool(args.provider)
        )
        if healthy:
            clear_maintenance(root)
        verification = {"attempts": verification_attempts, "timeoutSeconds": 30, "initialDelaySeconds": initial_delay}
        append_runtime_event(root, "VERIFICATION", "Runtime startup verified" if healthy else "Runtime startup incomplete", {"results": results, "verified": verified, "verification": verification})
        emit({"started": healthy, "maintenance": maintenance_status(root), "results": results, "verified": verified, "verification": verification})
        return 0 if healthy else 2
    raise SystemExit("unknown lifecycle command")

def monitor_workflows(root, config, execute=False):
    workspace = root.parent if root.name == ".cogent" else root
    script = Path(__file__).resolve().with_name("workflow.py")
    maximum = max(1, int(config.get("workflowAutomation", {}).get("maximumLaunchesPerTick", 2)))
    command = [sys.executable, str(script), "--root", str(workspace), "supervise", "--maximum", str(maximum)]
    if execute: command.append("--execute")
    result = run_command(command, int(config["supervisor"]["commandTimeoutSeconds"]))
    if not result.get("ok"):
        return {"status":"error","workflowCount":0,"actions":[],"error":result.get("stderr") or result.get("error") or "workflow supervisor failed"}
    try: return json.loads(result.get("stdout") or "{}")
    except json.JSONDecodeError as exc: return {"status":"error","workflowCount":0,"actions":[],"error":f"invalid workflow supervisor output: {exc}"}

def supervisor_tick(args):
    root = args.root.resolve()
    config = load_config(root)
    base = runtime_dir(root)
    try:
        with file_lock(base / ".supervisor.lock", timeout=1, stale=max(120, int(config["supervisor"]["intervalSeconds"]))):
            marker = maintenance_status(root)
            if marker and marker.get("active"):
                if marker.get("recoveryPolicy") == "healthy-runtime":
                    gateway = provider_probe("gateway", config, args.fixture)
                    provider = provider_probe("ollama", config, args.fixture)
                    if gateway.get("healthy") and provider.get("healthy"):
                        previous = clear_maintenance(root)
                        append_runtime_event(root, "RECOVERY", "Stale restart maintenance cleared after runtime health verification", {"previous":previous})
                        marker = None
                if marker and marker.get("active") and marker.get("recoveryPolicy") != "healthy-runtime":
                    snapshot = {"schemaVersion": 1, "timestamp": now(), "status": "maintenance", "maintenance": marker, "probes": {}, "recoveries": [], "contextMonitor": {"status": "paused", "reason": "intentional maintenance"}, "workflowMonitor": {"status": "paused", "reason": "intentional maintenance"}, "executeSafe": bool(args.execute_safe)}
                    atomic_json(base / "health.json", snapshot)
                    append_runtime_event(root, "OBSERVATION", "Supervisor tick skipped during intentional maintenance", {"reason": marker.get("reason")})
                    emit(snapshot)
                    return 0
            state = read_json(base / "supervisor-state.json", {"schemaVersion": 1, "components": {}, "updatedAt": None})
            probes = {}
            for name in ("gateway", "ollama", "resources"):
                first = provider_probe(name, config, args.fixture)
                if first.get("enabled") and not first["healthy"]:
                    time.sleep(float(config["supervisor"]["confirmDelaySeconds"]))
                    first["confirmation"] = provider_probe(name, config, args.fixture)
                    first["healthy"] = bool(first["confirmation"]["healthy"])
                probes[name] = first
            recoveries = []
            circuit_open = False
            for name, probe in probes.items():
                component = state["components"].setdefault(name, {"consecutiveFailures": 0, "attempts": [], "circuitOpen": False})
                if not probe.get("enabled") or probe["healthy"]:
                    component["consecutiveFailures"] = 0
                    component["circuitOpen"] = False
                    continue
                component["consecutiveFailures"] += 1
                if name == "resources":
                    component["circuitOpen"] = False
                    continue
                allowed, attempts = recovery_allowed(component, config)
                component["attempts"] = attempts
                if not allowed:
                    component["circuitOpen"] = len(attempts) >= int(config["supervisor"]["maximumRecoveriesPerHour"])
                    circuit_open = circuit_open or component["circuitOpen"]
                    continue
                if args.execute_safe:
                    if args.fixture is not None:
                        action = {"ok": False, "simulated": True}
                        verified = provider_probe(name, config, args.fixture)
                    else:
                        action = recover_component(name, config)
                        time.sleep(float(config["supervisor"]["verifyDelaySeconds"]))
                        verified = provider_probe(name, config)
                    component["attempts"].append(now())
                    component["lastRecoveryAt"] = now()
                    recoveries.append({"component": name, "action": action, "verification": verified})
                    probe["healthy"] = bool(verified["healthy"])
                    append_runtime_event(root, "RECOVERY", f"Recovery attempted for {name}", recoveries[-1])
            unhealthy = [name for name, value in probes.items() if value.get("enabled") and not value["healthy"]]
            state["updatedAt"] = now()
            state["components"] = state["components"]
            status = "healthy" if not unhealthy else "circuit-open" if circuit_open else "degraded"
            if status == "healthy" and marker and marker.get("recoveryPolicy") == "healthy-runtime":
                previous = clear_maintenance(root)
                append_runtime_event(root, "RECOVERY", "Recoverable restart completed after supervised health verification", {"previous": previous, "recoveries": recoveries})
                marker = None
            context_monitor = {"status": "disabled", "bindingCount": 0, "observations": []}
            if args.fixture is None and config["contextContinuity"].get("autoMonitor", True):
                try:
                    context_monitor = monitor_context_bindings(root, execute_safe=bool(args.execute_safe))
                except Exception as exc:
                    context_monitor = {"status": "error", "error": str(exc), "bindingCount": 0, "observations": []}
            workflow_monitor = {"status": "disabled", "workflowCount": 0, "actions": []}
            if args.fixture is None and config.get("workflowAutomation", {}).get("enabled", True):
                workflow_monitor = monitor_workflows(root, config, execute=bool(args.execute_safe))
            snapshot = {"schemaVersion": 1, "timestamp": now(), "status": status, "maintenance": marker, "probes": probes, "recoveries": recoveries, "contextMonitor": context_monitor, "workflowMonitor": workflow_monitor, "executeSafe": bool(args.execute_safe)}
            atomic_json(base / "health.json", snapshot)
            atomic_json(base / "supervisor-state.json", state)
            append_runtime_event(root, "OBSERVATION", f"Supervisor tick: {status}", {"unhealthy": unhealthy, "recoveryCount": len(recoveries)})
            emit(snapshot)
            return 0 if status == "healthy" else 3 if status == "circuit-open" else 2
    except TimeoutError:
        emit({"status": "skipped", "reason": "supervisor already running"})
        return 0

def supervisor_status(args):
    base = runtime_dir(args.root)
    emit({
        "health": read_json(base / "health.json", None) if (base / "health.json").exists() else None,
        "state": read_json(base / "supervisor-state.json", None) if (base / "supervisor-state.json").exists() else None,
        "config": load_config(args.root)
    })

def supervisor_history(args):
    path = runtime_dir(args.root) / "ledger.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []
    emit(records[-args.lines:])

def supervisor_doctor(args):
    emit({
        "platform": platform.system().lower(),
        "schedulerBackend": detect_scheduler(),
        "openclaw": openclaw_executable(),
        "ollama": shutil.which("ollama"),
        "workspace": str(WORKSPACE),
        "runtimeRoot": str(args.root.resolve()),
        "config": load_config(args.root)
    })

def lane_limit(kind, config):
    policy = config["concurrency"]
    mapping = {
        "inference": int(policy["inferenceLanes"]),
        "execution": int(policy["executionLanes"]),
        "verification": int(policy["verificationLanes"]),
        "supervisor": int(policy["supervisorLanes"])
    }
    limit = mapping[kind]
    if kind == "inference" and policy["mode"] == "adaptive":
        limit = int(policy["maxInferenceLanes"])
        available = memory_info().get("availableBytes")
        minimum = float(policy["minimumFreeMemoryGB"]) * 1024 ** 3
        if available is not None and available < minimum:
            limit = 1
    return max(1, limit)

def clean_leases(state):
    current = datetime.now(timezone.utc)
    state["leases"] = [item for item in state.get("leases", []) if datetime.fromisoformat(item["expiresAt"]) > current]
    return state

def concurrency_status(args):
    config = load_config(args.root)
    path = runtime_dir(args.root) / "concurrency.json"
    with file_lock(runtime_dir(args.root) / ".concurrency.lock"):
        state = clean_leases(read_json(path, {"schemaVersion": 1, "leases": []}))
        atomic_json(path, state)
    counts = {kind: len([item for item in state["leases"] if item["kind"] == kind]) for kind in ("inference", "execution", "verification", "supervisor")}
    emit({"policy": config["concurrency"], "counts": counts, "limits": {kind: lane_limit(kind, config) for kind in counts}, "leases": state["leases"]})

def concurrency_acquire(args):
    config = load_config(args.root)
    base = runtime_dir(args.root)
    path = base / "concurrency.json"
    with file_lock(base / ".concurrency.lock"):
        state = clean_leases(read_json(path, {"schemaVersion": 1, "leases": []}))
        if any(item["owner"] == args.owner and item["kind"] == args.kind for item in state["leases"]):
            raise SystemExit("owner already holds this lane")
        active = len([item for item in state["leases"] if item["kind"] == args.kind])
        limit = lane_limit(args.kind, config)
        if active >= limit:
            emit({"admitted": False, "decision": "QUEUE", "kind": args.kind, "active": active, "limit": limit})
            return 2
        seconds = int(config["concurrency"]["leaseSeconds"])
        lease = {"leaseId": uuid.uuid4().hex, "owner": args.owner, "kind": args.kind, "createdAt": now(), "expiresAt": (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()}
        state["leases"].append(lease)
        atomic_json(path, state)
    emit({"admitted": True, "decision": "ADMIT", "lease": lease, "limit": limit})
    return 0

def concurrency_release(args):
    base = runtime_dir(args.root)
    path = base / "concurrency.json"
    with file_lock(base / ".concurrency.lock"):
        state = clean_leases(read_json(path, {"schemaVersion": 1, "leases": []}))
        before = len(state["leases"])
        state["leases"] = [item for item in state["leases"] if not (item["leaseId"] == args.lease_id and item["owner"] == args.owner)]
        if len(state["leases"]) == before:
            raise SystemExit("matching lease not found")
        atomic_json(path, state)
    emit({"released": True, "leaseId": args.lease_id})

def context_decision(used, maximum, config):
    if maximum <= 0 or used < 0:
        raise SystemExit("invalid token counts")
    ratio = used / maximum
    policy = config["contextContinuity"]
    if ratio >= float(policy["criticalLimit"]):
        action = "ROTATE"
    elif ratio >= float(policy["handoffLimit"]):
        action = "HANDOFF"
    elif ratio >= float(policy["softLimit"]):
        action = "CHECKPOINT"
    else:
        action = "CONTINUE"
    return {"usedTokens": used, "maximumTokens": maximum, "ratio": round(ratio, 6), "action": action, "reserveTokens": int(policy["reserveTokens"])}

def context_status(args):
    emit(context_decision(args.used_tokens, args.maximum_tokens, load_config(args.root)))

def handoff_contract(value):
    keys = (
        "schemaVersion", "taskId", "generation", "ownerSession", "goal", "currentObjective",
        "stateRevision", "completedSteps", "producedArtifacts", "importantDiscoveries",
        "knownFailures", "recoveryHint", "nextAction", "contextDecision", "authorization"
    )
    immutable = {key: value.get(key) for key in keys}
    return hashlib.sha256(json.dumps(immutable, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def validate_handoff(value):
    if value.get("contractHash") != handoff_contract(value):
        raise SystemExit("handoff integrity check failed")

def task_state_path(root, task_id):
    return root.resolve() / "tasks" / task_id / "state.json"

def handoff_path(root, task_id):
    return root.resolve() / "tasks" / task_id / "handoff.json"

def prepare_handoff(root, task_id, owner_session, next_action, used_tokens, maximum_tokens):
    root = root.resolve()
    state = read_json(task_state_path(root, task_id))
    path = handoff_path(root, task_id)
    previous = read_json(path, {"generation": 0})
    decision = context_decision(used_tokens, maximum_tokens, load_config(root))
    payload = {
        "schemaVersion": 1,
        "taskId": task_id,
        "generation": int(previous.get("generation", 0)) + 1,
        "status": "prepared",
        "createdAt": now(),
        "ownerSession": owner_session,
        "workerSession": None,
        "leaseId": None,
        "leaseExpiresAt": None,
        "goal": state.get("goal"),
        "currentObjective": state.get("currentObjective"),
        "stateRevision": state.get("revision"),
        "completedSteps": state.get("completedSteps", []),
        "producedArtifacts": state.get("producedArtifacts", []),
        "importantDiscoveries": state.get("importantDiscoveries", []),
        "knownFailures": state.get("knownFailures", []),
        "recoveryHint": state.get("recoveryHint"),
        "nextAction": next_action,
        "contextDecision": decision,
        "authorization": {"inheritTaskScope": True, "externalActionsRequireExistingAuthority": True}
    }
    payload["contractHash"] = handoff_contract(payload)
    with file_lock(path.parent / ".handoff.lock"):
        atomic_json(path, payload)
    append_runtime_event(root, "COMMIT", f"Handoff prepared for {task_id}", {"generation": payload["generation"], "stateRevision": payload["stateRevision"], "action": decision["action"]})
    return payload

def context_checkpoint(args):
    payload = prepare_handoff(args.root, args.task_id, args.owner_session, args.next_action, args.used_tokens, args.maximum_tokens)
    emit(payload)

def bindings_path(root):
    return runtime_dir(root) / "context-bindings.json"

def context_bind(args):
    root = args.root.resolve()
    read_json(task_state_path(root, args.task_id))
    path = bindings_path(root)
    with file_lock(path.parent / ".context-bindings.lock"):
        registry = read_json(path, {"schemaVersion": 1, "bindings": []})
        registry["bindings"] = [item for item in registry["bindings"] if item["taskId"] != args.task_id]
        binding = {
            "taskId": args.task_id,
            "sessionKey": args.session_key,
            "ownerSession": args.owner_session or args.session_key,
            "nextAction": args.next_action,
            "enabled": True,
            "boundAt": now(),
            "lastAction": None,
            "lastStateRevision": None,
            "lastObservedAt": None,
        }
        registry["bindings"].append(binding)
        atomic_json(path, registry)
    append_runtime_event(root, "COMMIT", f"Context session bound for {args.task_id}", {"sessionKey": args.session_key})
    emit(binding)

def context_unbind(args):
    path = bindings_path(args.root)
    with file_lock(path.parent / ".context-bindings.lock"):
        registry = read_json(path, {"schemaVersion": 1, "bindings": []})
        before = len(registry["bindings"])
        registry["bindings"] = [item for item in registry["bindings"] if item["taskId"] != args.task_id]
        if len(registry["bindings"]) == before:
            raise SystemExit("context binding not found")
        atomic_json(path, registry)
    append_runtime_event(args.root, "COMMIT", f"Context session unbound for {args.task_id}")
    emit({"unbound": True, "taskId": args.task_id})

def load_openclaw_sessions(sessions_json=None):
    if sessions_json:
        document = read_json(Path(sessions_json))
    else:
        executable = openclaw_executable()
        if not executable:
            raise RuntimeError("openclaw CLI unavailable")
        proc = subprocess.run(
            [executable, "sessions", "--json", "--limit", "all"],
            capture_output=True,
            text=True,
            timeout=30,
            **background_options(),
        )
        if proc.returncode:
            raise RuntimeError(proc.stderr.strip() or "openclaw sessions failed")
        document = json.loads(proc.stdout)
    sessions = document.get("sessions")
    if not isinstance(sessions, list):
        raise RuntimeError("invalid OpenClaw sessions document")
    return {item.get("key"): item for item in sessions if isinstance(item, dict) and item.get("key")}

def monitor_context_bindings(root, sessions_json=None, execute_safe=False, only_task=None):
    root = root.resolve()
    path = bindings_path(root)
    registry = read_json(path, {"schemaVersion": 1, "bindings": []})
    selected = [item for item in registry["bindings"] if item.get("enabled") and (not only_task or item["taskId"] == only_task)]
    if not selected:
        return {"status": "idle", "bindingCount": 0, "observations": []}
    sessions = load_openclaw_sessions(sessions_json)
    observations = []
    changed = False
    for binding in selected:
        item = sessions.get(binding["sessionKey"])
        if not item:
            observations.append({"taskId": binding["taskId"], "sessionKey": binding["sessionKey"], "status": "missing"})
            continue
        used, maximum = item.get("totalTokens"), item.get("contextTokens")
        fresh = item.get("totalTokensFresh") is True
        if isinstance(used, bool) or not isinstance(used, int) or isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            observations.append({"taskId": binding["taskId"], "sessionKey": binding["sessionKey"], "status": "invalid-usage"})
            continue
        decision = context_decision(used, maximum, load_config(root))
        state = read_json(task_state_path(root, binding["taskId"]))
        checkpointed = False
        should_checkpoint = (
            execute_safe and fresh and decision["action"] != "CONTINUE"
            and (binding.get("lastAction") != decision["action"] or binding.get("lastStateRevision") != state.get("revision"))
        )
        if should_checkpoint:
            prepare_handoff(root, binding["taskId"], binding["ownerSession"], binding["nextAction"], used, maximum)
            checkpointed = True
            binding["lastAction"] = decision["action"]
            binding["lastStateRevision"] = state.get("revision")
            changed = True
        binding["lastObservedAt"] = now()
        changed = True
        observations.append({
            "taskId": binding["taskId"], "sessionKey": binding["sessionKey"], "status": "observed",
            "fresh": fresh, "decision": decision, "checkpointed": checkpointed,
            "rotationRequired": decision["action"] == "ROTATE",
        })
    if changed:
        with file_lock(path.parent / ".context-bindings.lock"):
            current = read_json(path, {"schemaVersion": 1, "bindings": []})
            updates = {item["taskId"]: item for item in registry["bindings"]}
            current["bindings"] = [updates.get(item["taskId"], item) for item in current["bindings"]]
            atomic_json(path, current)
    result = {"status": "observed", "bindingCount": len(selected), "observations": observations}
    append_runtime_event(root, "OBSERVATION", "Context bindings monitored", {"bindingCount": len(selected), "checkpointCount": len([item for item in observations if item.get("checkpointed")])})
    return result

def context_monitor(args):
    result = monitor_context_bindings(args.root, args.sessions_json, args.execute_safe, args.task_id)
    emit(result)
    return 0 if all(item.get("status") == "observed" for item in result["observations"]) else 2

def context_rotations(args):
    root = args.root.resolve()
    registry = read_json(bindings_path(root), {"schemaVersion": 1, "bindings": []})
    items = []
    for binding in registry["bindings"]:
        if args.task_id and binding["taskId"] != args.task_id:
            continue
        path = handoff_path(root, binding["taskId"])
        item = {"taskId": binding["taskId"], "boundSessionKey": binding["sessionKey"], "ownerSession": binding["ownerSession"], "handoff": None}
        if path.exists():
            try:
                handoff = read_json(path); validate_handoff(handoff)
                item["handoff"] = {key: handoff.get(key) for key in ("generation", "status", "workerSession", "leaseId", "leaseExpiresAt", "claimedAt", "releasedAt", "resultSummary", "contextDecision")}
            except Exception as exc:
                item["handoff"] = {"status": "invalid", "error": str(exc)}
        items.append(item)
    emit({"schemaVersion": 1, "count": len(items), "rotations": items})
    return 0

def handoff_inspect(args):
    handoff = read_json(handoff_path(args.root, args.task_id))
    validate_handoff(handoff)
    emit(handoff)

def lease_expired(value):
    return not value or datetime.fromisoformat(value) <= datetime.now(timezone.utc)

def handoff_claim(args):
    path = handoff_path(args.root, args.task_id)
    config = load_config(args.root)
    with file_lock(path.parent / ".handoff.lock"):
        handoff = read_json(path)
        validate_handoff(handoff)
        if handoff["status"] == "claimed" and not lease_expired(handoff.get("leaseExpiresAt")) and handoff.get("workerSession") != args.worker_session:
            raise SystemExit("handoff already claimed by a live worker")
        seconds = int(config["contextContinuity"]["leaseSeconds"])
        handoff["status"] = "claimed"
        handoff["workerSession"] = args.worker_session
        handoff["leaseId"] = uuid.uuid4().hex
        handoff["leaseExpiresAt"] = (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()
        handoff["claimedAt"] = now()
        atomic_json(path, handoff)
    append_runtime_event(args.root, "ACTION", f"Handoff claimed for {args.task_id}", {"generation": handoff["generation"], "workerSession": args.worker_session})
    emit(handoff)

def handoff_release(args):
    path = handoff_path(args.root, args.task_id)
    with file_lock(path.parent / ".handoff.lock"):
        handoff = read_json(path)
        validate_handoff(handoff)
        if handoff.get("workerSession") != args.worker_session or handoff.get("leaseId") != args.lease_id:
            raise SystemExit("handoff lease mismatch")
        handoff["status"] = args.result
        handoff["resultSummary"] = args.summary
        handoff["releasedAt"] = now()
        handoff["workerSession"] = None
        handoff["leaseId"] = None
        handoff["leaseExpiresAt"] = None
        atomic_json(path, handoff)
    append_runtime_event(args.root, "COMMIT", f"Handoff released for {args.task_id}", {"generation": handoff["generation"], "result": args.result})
    emit(handoff)

def detect_scheduler():
    if os.name == "nt":
        return "windows"
    if sys.platform == "darwin":
        return "launchd"
    if shutil.which("systemctl"):
        return "systemd"
    if shutil.which("crontab"):
        return "cron"
    return "none"

def template_root():
    return Path(__file__).resolve().parents[1] / "templates" / "supervisor"

def render_template(backend, root):
    names = {"windows": "windows-task.xml", "systemd": "cogentnexus-supervisor.service", "systemd-timer": "cogentnexus-supervisor.timer", "launchd": "ai.cogentnexus.supervisor.plist", "cron": "cron.txt", "docker": "docker-compose.yml", "kubernetes": "kubernetes-probes.yaml"}
    selected = ["systemd", "systemd-timer"] if backend == "systemd" else [backend]
    rendered = {}
    for item in selected:
        path = template_root() / names[item]
        text = path.read_text(encoding="utf-8")
        replacements = {"{{PYTHON}}": sys.executable, "{{RUNTIME}}": str(Path(__file__).resolve()), "{{ROOT}}": str(root.resolve())}
        for key, value in replacements.items():
            text = text.replace(key, value)
        rendered[names[item]] = text
    return rendered

def scheduler_cmd(args):
    backend = detect_scheduler() if getattr(args, "backend", "auto") == "auto" else args.backend
    if args.command_name == "detect":
        emit({"backend": detect_scheduler(), "platform": platform.system().lower()})
        return
    if args.command_name == "status":
        emit({"backend": backend, "templates": sorted(render_template(backend, args.root)), "installed": None, "note": "Use the native service manager to inspect installation."})
        return
    emit({"backend": backend, "files": render_template(backend, args.root)})

def config_cmd(args):
    path = config_path(args.root)
    if args.command_name == "init":
        if path.exists() and not args.force:
            raise SystemExit("config already exists")
        atomic_json(path, DEFAULT_CONFIG)
    emit(load_config(args.root))

def call(script, root, *parts):
    return subprocess.run([sys.executable, str(script), "--root", str(root), *parts], capture_output=True, text=True)

def self_test(args):
    root = Path(tempfile.mkdtemp(prefix="cogent-runtime-test-"))
    script = Path(__file__).resolve()
    try:
        if call(script, root, "config", "init").returncode:
            raise SystemExit("config init failed")
        stopped_status = {"ok": True, "stdout": "Runtime: stopped", "stderr": "Connectivity probe: failed\nconnect ECONNREFUSED"}
        running_status = {"ok": True, "stdout": "Runtime: running\nConnectivity probe: ok", "stderr": ""}
        if gateway_status_healthy(stopped_status) or not gateway_status_healthy(running_status):
            raise SystemExit("gateway status interpretation failed")
        readiness_sequence = iter([False, True])
        original_gateway_probe = globals()["gateway_probe"]
        original_ollama_probe = globals()["ollama_probe"]
        try:
            globals()["gateway_probe"] = lambda timeout: {"name": "gateway", "enabled": True, "healthy": next(readiness_sequence)}
            globals()["ollama_probe"] = lambda config: {"name": "ollama", "enabled": True, "healthy": True}
            _, readiness_attempts, readiness_healthy = wait_for_runtime_health(load_config(root), timeout_seconds=1)
        finally:
            globals()["gateway_probe"] = original_gateway_probe
            globals()["ollama_probe"] = original_ollama_probe
        if not readiness_healthy or readiness_attempts != 2:
            raise SystemExit("runtime readiness polling failed")
        low = json.loads(call(script, root, "context", "status", "--used-tokens", "10", "--maximum-tokens", "100").stdout)
        high = json.loads(call(script, root, "context", "status", "--used-tokens", "83", "--maximum-tokens", "100").stdout)
        if low["action"] != "CONTINUE" or high["action"] != "ROTATE":
            raise SystemExit("context thresholds failed")
        task = root / "tasks" / "T1"
        atomic_json(task / "state.json", {"taskId": "T1", "goal": "test", "currentObjective": "resume", "revision": 4, "completedSteps": ["a"], "producedArtifacts": [], "importantDiscoveries": [], "knownFailures": [], "recoveryHint": "next"})
        checkpoint = call(script, root, "context", "checkpoint", "--task-id", "T1", "--owner-session", "main", "--next-action", "continue", "--used-tokens", "75", "--maximum-tokens", "100")
        if checkpoint.returncode:
            raise SystemExit(checkpoint.stderr)
        claimed = call(script, root, "context", "claim", "--task-id", "T1", "--worker-session", "worker-1")
        if claimed.returncode:
            raise SystemExit(claimed.stderr)
        lease = json.loads(claimed.stdout)
        collision = call(script, root, "context", "claim", "--task-id", "T1", "--worker-session", "worker-2")
        if collision.returncode == 0:
            raise SystemExit("handoff fencing failed")
        released = call(script, root, "context", "release", "--task-id", "T1", "--worker-session", "worker-1", "--lease-id", lease["leaseId"], "--result", "rotated", "--summary", "checkpoint")
        if released.returncode:
            raise SystemExit(released.stderr)
        sessions_fixture = root / "sessions.json"
        atomic_json(sessions_fixture, {"sessions": [{"key": "session-main", "totalTokens": 75, "contextTokens": 100, "totalTokensFresh": True}]})
        bound = call(script, root, "context", "bind", "--task-id", "T1", "--session-key", "session-main", "--owner-session", "main", "--next-action", "continue after rotation")
        monitored = call(script, root, "context", "monitor", "--task-id", "T1", "--sessions-json", str(sessions_fixture), "--execute-safe")
        repeated = call(script, root, "context", "monitor", "--task-id", "T1", "--sessions-json", str(sessions_fixture), "--execute-safe")
        if bound.returncode or monitored.returncode or repeated.returncode:
            raise SystemExit("automatic context monitoring failed")
        first_observation = json.loads(monitored.stdout)["observations"][0]
        second_observation = json.loads(repeated.stdout)["observations"][0]
        if not first_observation["checkpointed"] or second_observation["checkpointed"]:
            raise SystemExit("automatic checkpoint deduplication failed")
        rotations = call(script, root, "context", "rotations", "--task-id", "T1")
        if rotations.returncode or json.loads(rotations.stdout)["rotations"][0]["handoff"]["status"] != "prepared":
            raise SystemExit(f"rotation management status failed rc={rotations.returncode}: stdout={rotations.stdout} stderr={rotations.stderr}")
        tampered_path = handoff_path(root, "T1")
        tampered = read_json(tampered_path)
        tampered["nextAction"] = "tampered"
        atomic_json(tampered_path, tampered)
        if call(script, root, "context", "claim", "--task-id", "T1", "--worker-session", "worker-2").returncode == 0:
            raise SystemExit("handoff integrity gate failed")
        first = call(script, root, "concurrency", "acquire", "--kind", "inference", "--owner", "one")
        second = call(script, root, "concurrency", "acquire", "--kind", "inference", "--owner", "two")
        if first.returncode or second.returncode != 2:
            raise SystemExit("single-lane admission failed")
        lease_id = json.loads(first.stdout)["lease"]["leaseId"]
        if call(script, root, "concurrency", "release", "--owner", "one", "--lease-id", lease_id).returncode:
            raise SystemExit("lease release failed")
        config = load_config(root)
        workflow_observation = monitor_workflows(root, config, execute=False)
        if workflow_observation.get("status") != "observed" or workflow_observation.get("workflowCount") != 0:
            raise SystemExit("workflow supervisor integration failed")
        config["supervisor"]["cooldownSeconds"] = 0
        config["supervisor"]["confirmDelaySeconds"] = 0
        config["supervisor"]["verifyDelaySeconds"] = 0
        atomic_json(config_path(root), config)
        prepared = call(script, root, "lifecycle", "prepare", "--reason", "self-test")
        paused = call(script, root, "supervisor", "tick", "--fixture", "gateway-fail", "--execute-safe")
        cancelled = call(script, root, "lifecycle", "cancel")
        if prepared.returncode or paused.returncode or cancelled.returncode or json.loads(paused.stdout)["status"] != "maintenance":
            raise SystemExit("intentional maintenance fencing failed")
        auto_prepared = call(script, root, "lifecycle", "prepare", "--reason", "self-test restart", "--recovery-policy", "healthy-runtime")
        auto_recovering = call(script, root, "supervisor", "tick", "--fixture", "gateway-fail", "--execute-safe")
        auto_resumed = call(script, root, "supervisor", "tick", "--fixture", "healthy")
        recovering_snapshot = json.loads(auto_recovering.stdout)
        if (auto_prepared.returncode or auto_recovering.returncode != 2 or recovering_snapshot.get("status") != "degraded"
                or not recovering_snapshot.get("recoveries") or maintenance_status(root) is not None
                or auto_resumed.returncode or json.loads(auto_resumed.stdout).get("status") == "maintenance"):
            raise SystemExit("restart maintenance auto-resumption failed")
        (runtime_dir(root) / "supervisor-state.json").unlink(missing_ok=True)
        healthy = call(script, root, "supervisor", "tick", "--fixture", "healthy")
        failures = [call(script, root, "supervisor", "tick", "--fixture", "gateway-fail", "--execute-safe") for _ in range(3)]
        blocked = call(script, root, "supervisor", "tick", "--fixture", "gateway-fail", "--execute-safe")
        if healthy.returncode or any(item.returncode != 2 for item in failures) or blocked.returncode != 3:
            raise SystemExit("supervisor circuit breaker failed")
        config = load_config(root)
        config["concurrency"]["mode"] = "adaptive"
        config["concurrency"]["maxInferenceLanes"] = 2
        config["concurrency"]["minimumFreeMemoryGB"] = 0
        atomic_json(config_path(root), config)
        one = call(script, root, "concurrency", "acquire", "--kind", "inference", "--owner", "adaptive-one")
        two = call(script, root, "concurrency", "acquire", "--kind", "inference", "--owner", "adaptive-two")
        three = call(script, root, "concurrency", "acquire", "--kind", "inference", "--owner", "adaptive-three")
        if one.returncode or two.returncode or three.returncode != 2:
            raise SystemExit("adaptive ceiling failed")
        for backend in ("windows", "systemd", "launchd", "cron", "docker", "kubernetes"):
            if call(script, root, "scheduler", "render", "--backend", backend).returncode:
                raise SystemExit(f"scheduler render failed: {backend}")
        print("Cogent runtime self-test: PASS")
    finally:
        shutil.rmtree(root, ignore_errors=True)

def add_root(parser):
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)

def main():
    parser = argparse.ArgumentParser(prog="cogent-runtime")
    add_root(parser)
    areas = parser.add_subparsers(dest="area", required=True)

    lifecycle = areas.add_parser("lifecycle").add_subparsers(dest="command_name", required=True)
    ls = lifecycle.add_parser("status"); ls.set_defaults(func=lifecycle_cmd)
    lp = lifecycle.add_parser("prepare"); lp.add_argument("--reason", default="planned shutdown"); lp.add_argument("--owner", default="operator"); lp.add_argument("--recovery-policy", choices=["manual","healthy-runtime"], default="manual"); lp.set_defaults(func=lifecycle_cmd)
    lc = lifecycle.add_parser("cancel"); lc.set_defaults(func=lifecycle_cmd)
    lst = lifecycle.add_parser("stop"); lst.add_argument("--provider", action="store_true"); lst.add_argument("--reason", default="planned shutdown"); lst.add_argument("--owner", default="operator"); lst.set_defaults(func=lifecycle_cmd)
    lr = lifecycle.add_parser("restart"); lr.add_argument("--reason", default="planned gateway restart"); lr.add_argument("--owner", default="operator"); lr.set_defaults(func=lifecycle_cmd)
    lstart = lifecycle.add_parser("start"); lstart.add_argument("--provider", action="store_true"); lstart.set_defaults(func=lifecycle_cmd)

    supervisor = areas.add_parser("supervisor").add_subparsers(dest="command_name", required=True)
    tick = supervisor.add_parser("tick")
    tick.add_argument("--execute-safe", action="store_true")
    tick.add_argument("--fixture", choices=["healthy", "gateway-fail", "ollama-fail", "all-fail"])
    tick.set_defaults(func=supervisor_tick)
    status = supervisor.add_parser("status"); status.set_defaults(func=supervisor_status)
    history = supervisor.add_parser("history"); history.add_argument("--lines", type=int, default=20); history.set_defaults(func=supervisor_history)
    doctor = supervisor.add_parser("doctor"); doctor.set_defaults(func=supervisor_doctor)

    concurrency = areas.add_parser("concurrency").add_subparsers(dest="command_name", required=True)
    cs = concurrency.add_parser("status"); cs.set_defaults(func=concurrency_status)
    ca = concurrency.add_parser("acquire"); ca.add_argument("--kind", choices=["inference", "execution", "verification", "supervisor"], required=True); ca.add_argument("--owner", required=True); ca.set_defaults(func=concurrency_acquire)
    cr = concurrency.add_parser("release"); cr.add_argument("--owner", required=True); cr.add_argument("--lease-id", required=True); cr.set_defaults(func=concurrency_release)

    context = areas.add_parser("context").add_subparsers(dest="command_name", required=True)
    cx = context.add_parser("status"); cx.add_argument("--used-tokens", type=int, required=True); cx.add_argument("--maximum-tokens", type=int, required=True); cx.set_defaults(func=context_status)
    cp = context.add_parser("checkpoint"); cp.add_argument("--task-id", required=True); cp.add_argument("--owner-session", required=True); cp.add_argument("--next-action", required=True); cp.add_argument("--used-tokens", type=int, required=True); cp.add_argument("--maximum-tokens", type=int, required=True); cp.set_defaults(func=context_checkpoint)
    ci = context.add_parser("inspect"); ci.add_argument("--task-id", required=True); ci.set_defaults(func=handoff_inspect)
    cc = context.add_parser("claim"); cc.add_argument("--task-id", required=True); cc.add_argument("--worker-session", required=True); cc.set_defaults(func=handoff_claim)
    cl = context.add_parser("release"); cl.add_argument("--task-id", required=True); cl.add_argument("--worker-session", required=True); cl.add_argument("--lease-id", required=True); cl.add_argument("--result", choices=["completed", "failed", "rotated"], required=True); cl.add_argument("--summary", required=True); cl.set_defaults(func=handoff_release)
    cb = context.add_parser("bind"); cb.add_argument("--task-id", required=True); cb.add_argument("--session-key", required=True); cb.add_argument("--owner-session"); cb.add_argument("--next-action", required=True); cb.set_defaults(func=context_bind)
    cu = context.add_parser("unbind"); cu.add_argument("--task-id", required=True); cu.set_defaults(func=context_unbind)
    cm = context.add_parser("monitor"); cm.add_argument("--task-id"); cm.add_argument("--sessions-json"); cm.add_argument("--execute-safe", action="store_true"); cm.set_defaults(func=context_monitor)
    cr = context.add_parser("rotations"); cr.add_argument("--task-id"); cr.set_defaults(func=context_rotations)

    scheduler = areas.add_parser("scheduler").add_subparsers(dest="command_name", required=True)
    sd = scheduler.add_parser("detect"); sd.set_defaults(func=scheduler_cmd)
    for name in ("render", "status"):
        item = scheduler.add_parser(name)
        item.add_argument("--backend", choices=["auto", "windows", "systemd", "launchd", "cron", "docker", "kubernetes"], default="auto")
        item.set_defaults(func=scheduler_cmd)

    config = areas.add_parser("config").add_subparsers(dest="command_name", required=True)
    cinit = config.add_parser("init"); cinit.add_argument("--force", action="store_true"); cinit.set_defaults(func=config_cmd)
    cshow = config.add_parser("show"); cshow.set_defaults(func=config_cmd)

    test = areas.add_parser("self-test"); test.set_defaults(func=self_test)
    args = parser.parse_args()
    return args.func(args) or 0

if __name__ == "__main__":
    raise SystemExit(main())
