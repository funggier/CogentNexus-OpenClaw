#!/usr/bin/env python3
"""Read-only CogentNexus preflight/check engine.

Every check is observational: no process lifecycle action, state repair, database
mutation, provider selection, or configuration write is allowed from this module.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

import provider

VERDICT_EXIT = {"READY": 0, "READY_WITH_WARNINGS": 1, "NOT_READY": 2, "INDETERMINATE": 3}


def item(name: str, status: str, summary: str, **details: Any) -> dict[str, Any]:
    return {"name": name, "status": status, "summary": summary, "details": details}


def _run(cmd: list[str], timeout: int = 30) -> dict[str, Any]:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, creationflags=flags)
        return {"ok": proc.returncode == 0, "exitCode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _state_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def read_state(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = _state_path(root)
    if not path.exists():
        return None, "Host controller state does not exist"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"Host controller state is unreadable: {exc}"
    if value.get("mode") not in {"managed", "passthrough", "maintenance"}:
        return None, f"invalid Host mode: {value.get('mode')!r}"
    return value, None


def check_cogentnexus(root: Path) -> list[dict[str, Any]]:
    here = Path(__file__).resolve().parent
    required = ["host_control_v091.py", "host_v091.py", "lifecycle_v091.py", "provider.py", "checks.py", "cnx.py"]
    missing = [name for name in required if not (here / name).is_file()]
    results = [
        item("CogentNexus installation", "FAIL" if missing else "PASS", "Required CogentNexus files are missing" if missing else "Core/provider/check scripts are present", missing=missing)
    ]
    state, error = read_state(root)
    if error:
        results.append(item("Host controller state", "FAIL", error, path=str(_state_path(root))))
    else:
        results.append(item(
            "Host controller state", "PASS", f"Mode is {state.get('mode')}",
            mode=state.get("mode"), selectedProvider=state.get("selectedProvider"),
            desiredGateway=state.get("desiredGateway"), desiredProvider=state.get("desiredProvider"),
            providerTransition=state.get("providerTransition"),
        ))
        if state.get("providerTransition"):
            results.append(item("Provider transition", "WARN", "A provider transition marker is present; a previous switch may have been interrupted", transition=state.get("providerTransition")))
    return results


def check_config(root: Path) -> list[dict[str, Any]]:
    results = []
    runtime_config = root / "runtime" / "config.json"
    if not runtime_config.exists():
        results.append(item("Runtime config", "WARN", "Runtime config has not been initialized yet", path=str(runtime_config)))
    else:
        try:
            value = json.loads(runtime_config.read_text(encoding="utf-8"))
            results.append(item("Runtime config", "PASS", "Runtime configuration is valid JSON", schemaVersion=value.get("schemaVersion")))
        except Exception as exc:
            results.append(item("Runtime config", "FAIL", f"Runtime configuration is invalid: {exc}", path=str(runtime_config)))
    executable = provider.openclaw_executable()
    if not executable:
        results.append(item("OpenClaw config", "FAIL", "OpenClaw CLI is unavailable"))
    else:
        result = _run([executable, "config", "validate"], timeout=30)
        results.append(item("OpenClaw config", "PASS" if result.get("ok") else "FAIL", "OpenClaw configuration validates" if result.get("ok") else "OpenClaw configuration validation failed", evidence=result))
    return results


def check_openclaw() -> list[dict[str, Any]]:
    executable = provider.openclaw_executable()
    if not executable:
        return [item("OpenClaw installation", "FAIL", "OpenClaw CLI was not found")]
    result = _run([executable, "--version"], timeout=20)
    return [item("OpenClaw installation", "PASS" if result.get("ok") else "FAIL", "OpenClaw CLI is available" if result.get("ok") else "OpenClaw version check failed", executable=executable, version=result.get("stdout"), evidence=result)]


def check_gateway() -> list[dict[str, Any]]:
    executable = provider.openclaw_executable()
    if not executable:
        return [item("Gateway", "FAIL", "OpenClaw CLI unavailable; Gateway cannot be inspected")]
    result = _run([executable, "gateway", "status"], timeout=30)
    output = f"{result.get('stdout', '')}\n{result.get('stderr', '')}".lower()
    healthy = result.get("ok") and "runtime: running" in output and "connectivity probe: ok" in output
    if healthy:
        return [item("Gateway", "PASS", "OpenClaw Gateway is reachable", evidence=result)]
    if result.get("ok") or "stopped" in output or "econnrefused" in output:
        return [item("Gateway", "WARN", "Gateway is installed but is not currently ready", evidence=result)]
    return [item("Gateway", "INDETERMINATE", "Gateway status could not be determined", evidence=result)]


def resolve_provider(root: Path, override: str | None) -> tuple[str | None, list[dict[str, Any]]]:
    state, _ = read_state(root)
    selected = state.get("selectedProvider") if state else None
    if override:
        try:
            requested = provider.normalize_provider(override)
        except ValueError as exc:
            return None, [item("Provider selection", "FAIL", str(exc))]
        return requested, [item("Provider selection", "PASS", f"Preflight requested provider: {requested}", requested=requested, persisted=selected, mutatesState=False)]
    if selected:
        try:
            selected = provider.normalize_provider(selected)
        except ValueError:
            return None, [item("Provider selection", "FAIL", f"Persisted provider is unsupported: {selected!r}")]
        return selected, [item("Provider selection", "PASS", f"Using persisted provider: {selected}", selected=selected)]
    installed = provider.installed_providers()
    if len(installed) == 1:
        return installed[0], [item("Provider selection", "WARN", f"No provider is persisted; exactly one provider is installed ({installed[0]})", inferred=installed[0], mutatesState=False)]
    if not installed:
        return None, [item("Provider selection", "FAIL", "No supported local provider is installed", supported=list(provider.SUPPORTED_PROVIDERS))]
    return None, [item("Provider selection", "FAIL", "Multiple providers are installed but no provider has been selected", installed=installed, suggested=[f"cnx.cmd start --provider {name}" for name in installed])]


def check_provider(root: Path, override: str | None = None, include_inventory: bool = True) -> list[dict[str, Any]]:
    target, results = resolve_provider(root, override)
    inventory = provider.inventory(timeout=2.0) if include_inventory else {}
    if include_inventory:
        for name in provider.SUPPORTED_PROVIDERS:
            info = inventory[name]
            status = "PASS" if info["healthy"] else "WARN" if info["installed"] else "INFO"
            summary = f"{name} is installed and reachable" if info["healthy"] else f"{name} is installed but not currently reachable" if info["installed"] else f"{name} is not installed"
            results.append(item(f"Provider discovery: {name}", status, summary, installed=info["installed"], controllable=info["controllable"], reachable=info["reachable"], endpoint=info["endpoint"], modelCount=info["modelCount"]))
    if not target:
        return results
    info = inventory.get(target) or provider.probe(target, timeout=3.0)
    if not info["installed"]:
        results.append(item("Selected provider", "FAIL", f"Provider '{target}' is not installed", provider=target))
    elif info["healthy"]:
        results.append(item("Selected provider", "PASS", f"Provider '{target}' is ready", provider=target, endpoint=info["endpoint"]))
    elif info["controllable"]:
        results.append(item("Selected provider", "WARN", f"Provider '{target}' is installed and startable but not currently reachable", provider=target, endpoint=info["endpoint"]))
    else:
        results.append(item("Selected provider", "FAIL", f"Provider '{target}' is installed but its CLI adapter is unavailable", provider=target, endpoint=info["endpoint"]))
    return results


def check_model(root: Path, override: str | None = None) -> list[dict[str, Any]]:
    target, results = resolve_provider(root, override)
    status = provider.openclaw_model_status()
    if not status.get("ok"):
        results.append(item("OpenClaw model routing", "INDETERMINATE", "Could not read OpenClaw model status", evidence=status))
        return results
    model_ref = status.get("defaultModel")
    routed = provider.model_provider(model_ref)
    if not model_ref:
        results.append(item("OpenClaw model routing", "WARN", "OpenClaw default model could not be resolved from model status"))
    elif target and routed and routed != target:
        results.append(item("OpenClaw model routing", "FAIL", f"OpenClaw default model routes to '{routed}' while preflight provider is '{target}'", defaultModel=model_ref, provider=target))
    else:
        results.append(item("OpenClaw model routing", "PASS", f"OpenClaw default model: {model_ref}", defaultModel=model_ref, modelProvider=routed, provider=target))
    if target:
        p = provider.probe(target, timeout=3.0)
        if p["healthy"] and p["modelCount"] > 0:
            results.append(item("Provider model catalog", "PASS", f"{target} exposes {p['modelCount']} model(s)", models=p["models"][:20]))
        elif p["healthy"]:
            results.append(item("Provider model catalog", "WARN", f"{target} is reachable but currently exposes no models", provider=target))
        else:
            results.append(item("Provider model catalog", "WARN", f"{target} is not running, so model availability cannot be verified", provider=target))
    return results


def _ticket_db(root: Path) -> Path:
    return root / "runtime" / "cogentnexus.sqlite3"


def check_storage(root: Path) -> list[dict[str, Any]]:
    results = []
    db_path = _ticket_db(root)
    if not db_path.exists():
        results.append(item("Ticket store", "WARN", "Ticket database does not exist yet", path=str(db_path)))
    else:
        try:
            db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=5)
            try:
                integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
                tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                status = "PASS" if integrity == "ok" and "tickets" in tables else "FAIL"
                results.append(item("Ticket store", status, "Ticket database is readable and integrity_check is ok" if status == "PASS" else "Ticket database integrity/schema check failed", path=str(db_path), integrity=integrity, tables=sorted(tables)))
            finally:
                db.close()
        except Exception as exc:
            results.append(item("Ticket store", "FAIL", f"Ticket database could not be inspected read-only: {exc}", path=str(db_path)))
    try:
        usage = shutil.disk_usage(root.parent if root.parent.exists() else Path.cwd())
        results.append(item("Disk headroom", "PASS" if usage.free >= 512 * 1024 * 1024 else "FAIL", f"Free disk: {usage.free / 1024**3:.2f} GiB", freeBytes=usage.free))
    except Exception as exc:
        results.append(item("Disk headroom", "INDETERMINATE", f"Disk usage could not be read: {exc}"))
    return results


def check_recovery(root: Path) -> list[dict[str, Any]]:
    results = []
    maintenance = root / "runtime" / "maintenance.json"
    if maintenance.exists():
        try:
            value = json.loads(maintenance.read_text(encoding="utf-8"))
            results.append(item("Maintenance/recovery fence", "WARN", "Intentional maintenance/restart marker is present", marker=value))
        except Exception as exc:
            results.append(item("Maintenance/recovery fence", "FAIL", f"Maintenance marker is invalid: {exc}"))
    else:
        results.append(item("Maintenance/recovery fence", "PASS", "No maintenance marker is active"))
    health = root / "runtime" / "health.json"
    if health.exists():
        try:
            snapshot = json.loads(health.read_text(encoding="utf-8"))
            status = snapshot.get("status")
            results.append(item("Supervisor health snapshot", "PASS" if status == "healthy" else "WARN", f"Last supervisor status: {status}", timestamp=snapshot.get("timestamp"), status=status))
        except Exception as exc:
            results.append(item("Supervisor health snapshot", "FAIL", f"Supervisor health snapshot is invalid: {exc}"))
    else:
        results.append(item("Supervisor health snapshot", "WARN", "No supervisor health snapshot exists yet"))
    return results


def check_delivery(root: Path) -> list[dict[str, Any]]:
    path = _ticket_db(root)
    if not path.exists():
        return [item("Delivery/outbox", "WARN", "Ticket database does not exist yet")]
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
        try:
            table = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='ticket_outbox'").fetchone()
            if not table:
                return [item("Delivery/outbox", "WARN", "ticket_outbox table is not present")]
            pending = int(db.execute("SELECT count(*) FROM ticket_outbox WHERE delivery_status='pending'").fetchone()[0])
            return [item("Delivery/outbox", "PASS" if pending == 0 else "WARN", "No pending terminal deliveries" if pending == 0 else f"{pending} terminal delivery item(s) are pending", pending=pending)]
        finally:
            db.close()
    except Exception as exc:
        return [item("Delivery/outbox", "INDETERMINATE", f"Delivery state could not be inspected: {exc}")]


def _memory_info() -> dict[str, Any]:
    if os.name == "nt":
        exe = shutil.which("powershell.exe") or shutil.which("powershell")
        if exe:
            command = "(Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json -Compress)"
            result = _run([exe, "-NoProfile", "-NonInteractive", "-Command", command], timeout=10)
            if result.get("ok"):
                try:
                    value = json.loads(result["stdout"])
                    return {"availableBytes": int(value["FreePhysicalMemory"]) * 1024, "totalBytes": int(value["TotalVisibleMemorySize"]) * 1024}
                except Exception:
                    pass
    elif Path("/proc/meminfo").exists():
        values = {}
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            key, value = line.split(":", 1)
            values[key] = int(value.strip().split()[0]) * 1024
        return {"availableBytes": values.get("MemAvailable"), "totalBytes": values.get("MemTotal")}
    return {"availableBytes": None, "totalBytes": None}


def check_resources(root: Path) -> list[dict[str, Any]]:
    info = _memory_info()
    available = info.get("availableBytes")
    minimum = 2 * 1024**3
    config = root / "runtime" / "config.json"
    if config.exists():
        try:
            value = json.loads(config.read_text(encoding="utf-8"))
            minimum = float(value.get("concurrency", {}).get("minimumFreeMemoryGB", 2)) * 1024**3
        except Exception:
            pass
    if available is None:
        return [item("Memory headroom", "INDETERMINATE", "Available memory could not be determined", **info)]
    return [item("Memory headroom", "PASS" if available >= minimum else "WARN", f"Available memory: {available / 1024**3:.2f} GiB", availableBytes=available, minimumFreeBytes=int(minimum), totalBytes=info.get("totalBytes"))]


def aggregate(entries: list[dict[str, Any]]) -> str:
    statuses = [entry["status"] for entry in entries]
    if "FAIL" in statuses:
        return "NOT_READY"
    if "INDETERMINATE" in statuses:
        return "INDETERMINATE"
    if "WARN" in statuses:
        return "READY_WITH_WARNINGS"
    return "READY"


def system_check(root: Path, provider_override: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    entries.extend(check_cogentnexus(root))
    entries.extend(check_config(root))
    entries.extend(check_openclaw())
    entries.extend(check_provider(root, provider_override, include_inventory=True))
    entries.extend(check_model(root, provider_override))
    entries.extend(check_gateway())
    entries.extend(check_storage(root))
    entries.extend(check_recovery(root))
    entries.extend(check_delivery(root))
    entries.extend(check_resources(root))
    verdict = aggregate(entries)
    return {"check": "system", "providerOverride": provider_override, "verdict": verdict, "exitCode": VERDICT_EXIT[verdict], "checks": entries, "readOnly": True, "stateChanged": False}


def component_check(root: Path, component: str, provider_override: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    mapping = {
        "cogentnexus": lambda: check_cogentnexus(root), "config": lambda: check_config(root),
        "openclaw": check_openclaw, "gateway": check_gateway,
        "provider": lambda: check_provider(root, provider_override, include_inventory=True),
        "model": lambda: check_model(root, provider_override), "storage": lambda: check_storage(root),
        "recovery": lambda: check_recovery(root), "delivery": lambda: check_delivery(root),
        "resources": lambda: check_resources(root),
    }
    if component not in mapping:
        raise ValueError(f"unsupported check component: {component}")
    entries = mapping[component]()
    verdict = aggregate(entries)
    return {"check": component, "providerOverride": provider_override, "verdict": verdict, "exitCode": VERDICT_EXIT[verdict], "checks": entries, "readOnly": True, "stateChanged": False}


def preflight_start(root: Path, provider_name: str) -> dict[str, Any]:
    target = provider.normalize_provider(provider_name)
    entries: list[dict[str, Any]] = []
    entries.extend(check_cogentnexus(root))
    entries.extend(check_openclaw())
    entries.extend(check_config(root))
    info = provider.probe(target, timeout=2.0)
    if not info["installed"]:
        entries.append(item("Provider preflight", "FAIL", f"Provider '{target}' is not installed"))
    elif info["healthy"]:
        entries.append(item("Provider preflight", "PASS", f"Provider '{target}' is already ready", provider=target))
    elif info["controllable"]:
        entries.append(item("Provider preflight", "PASS", f"Provider '{target}' is installed and can be started", provider=target))
    else:
        entries.append(item("Provider preflight", "FAIL", f"Provider '{target}' has no controllable CLI adapter", provider=target))
    verdict = aggregate(entries)
    return {"check": "preflight-start", "provider": target, "verdict": verdict, "exitCode": VERDICT_EXIT[verdict], "checks": entries, "readOnly": True, "stateChanged": False}


def render(report: dict[str, Any]) -> str:
    lines = ["CogentNexus System Check", "=" * 58]
    for entry in report.get("checks", []):
        lines.append(f"[{entry.get('status', '?')}] {entry.get('name')}")
        lines.append(f"       {entry.get('summary')}")
    lines.extend(["-" * 58, f"SYSTEM READINESS: {report.get('verdict')}", "No state was changed."])
    return "\n".join(lines)
