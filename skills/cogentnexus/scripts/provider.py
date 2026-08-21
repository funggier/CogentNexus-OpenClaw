#!/usr/bin/env python3
"""Provider-neutral local inference adapters for CogentNexus."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

SUPPORTED_PROVIDERS = ("ollama", "lmstudio")
DEFAULT_ENDPOINTS = {"ollama": "http://127.0.0.1:11434", "lmstudio": "http://127.0.0.1:1234"}


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def run(cmd: list[str], timeout: int = 30) -> dict[str, Any]:
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, creationflags=creation_flags())
        return {"ok": proc.returncode == 0, "exitCode": proc.returncode, "durationMs": round((time.monotonic() - started) * 1000), "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(), "command": cmd}
    except Exception as exc:
        return {"ok": False, "durationMs": round((time.monotonic() - started) * 1000), "error": str(exc), "command": cmd}


def _existing(candidates: list[str | None]) -> str | None:
    for value in candidates:
        if value and Path(value).expanduser().is_file():
            return str(Path(value).expanduser())
    return None


def find_ollama_cli() -> str | None:
    local = os.environ.get("LOCALAPPDATA", "")
    return _existing([shutil.which("ollama"), str(Path(local) / "Programs" / "Ollama" / "ollama.exe") if local else None])


def find_lms_cli() -> str | None:
    home = Path.home()
    local = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        shutil.which("lms"), shutil.which("lms.exe"), shutil.which("lms.cmd"),
        str(home / ".lmstudio" / "bin" / "lms"), str(home / ".lmstudio" / "bin" / "lms.exe"), str(home / ".lmstudio" / "bin" / "lms.cmd"),
    ]
    if local:
        candidates.extend([str(Path(local) / "Programs" / "LM Studio" / "bin" / "lms.exe"), str(Path(local) / "Programs" / "LM Studio" / "bin" / "lms.cmd")])
    return _existing(candidates)


def find_lmstudio_gui() -> str | None:
    local = os.environ.get("LOCALAPPDATA", "")
    program_files = os.environ.get("ProgramFiles", "")
    candidates: list[str | None] = []
    if local:
        candidates.extend([str(Path(local) / "Programs" / "LM Studio" / "LM Studio.exe"), str(Path(local) / "LM Studio" / "LM Studio.exe")])
    if program_files:
        candidates.append(str(Path(program_files) / "LM Studio" / "LM Studio.exe"))
    if sys.platform == "darwin":
        candidates.append("/Applications/LM Studio.app/Contents/MacOS/LM Studio")
    return _existing(candidates)


def normalize_provider(name: str) -> str:
    value = (name or "").strip().lower().replace("-", "")
    aliases = {"ollama": "ollama", "lmstudio": "lmstudio", "lm": "lmstudio"}
    if value not in aliases:
        raise ValueError(f"unsupported provider: {name!r}; expected one of: {', '.join(SUPPORTED_PROVIDERS)}")
    return aliases[value]


def detect(name: str) -> dict[str, Any]:
    provider_name = normalize_provider(name)
    if provider_name == "ollama":
        cli = find_ollama_cli()
        return {"name": provider_name, "installed": bool(cli), "controllable": bool(cli), "cli": cli, "application": None, "endpoint": DEFAULT_ENDPOINTS[provider_name]}
    cli = find_lms_cli()
    gui = find_lmstudio_gui()
    return {"name": provider_name, "installed": bool(cli or gui), "controllable": bool(cli), "cli": cli, "application": gui, "endpoint": DEFAULT_ENDPOINTS[provider_name]}


def _http_json(url: str, timeout: float = 5.0, provider_name: str | None = None) -> tuple[bool, Any]:
    headers = {"Accept": "application/json"}
    if provider_name == "lmstudio":
        token = os.environ.get("LM_API_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                parsed: Any = json.loads(body) if body else None
            except json.JSONDecodeError:
                parsed = body[:1000]
            return response.status == 200, {"status": response.status, "url": url, "body": parsed}
    except Exception as exc:
        return False, {"url": url, "error": str(exc)}


def _extract_model_ids(provider_name: str, body: Any) -> list[str]:
    if not isinstance(body, dict):
        return []
    values: list[str] = []
    rows = body.get("models") if provider_name == "ollama" else body.get("data") if isinstance(body.get("data"), list) else body.get("models")
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                value = row.get("name") or row.get("model") if provider_name == "ollama" else row.get("key") or row.get("id") or row.get("name") or row.get("model")
                if isinstance(value, str) and value:
                    values.append(value)
    return values


def probe(name: str, timeout: float = 5.0) -> dict[str, Any]:
    provider_name = normalize_provider(name)
    info = detect(provider_name)
    if provider_name == "ollama":
        ok, evidence = _http_json(f"{info['endpoint']}/api/tags", timeout, provider_name)
    else:
        ok, evidence = _http_json(f"{info['endpoint']}/api/v1/models", timeout, provider_name)
        if not ok:
            fallback_ok, fallback = _http_json(f"{info['endpoint']}/v1/models", timeout, provider_name)
            if fallback_ok:
                ok, evidence = fallback_ok, fallback
            else:
                evidence = {"primary": evidence, "fallback": fallback}
    body = evidence.get("body") if isinstance(evidence, dict) else None
    models = _extract_model_ids(provider_name, body)
    return {**info, "reachable": bool(ok), "healthy": bool(ok), "ready": bool(ok), "models": models, "modelCount": len(models), "evidence": evidence}


def inventory(timeout: float = 2.0) -> dict[str, dict[str, Any]]:
    return {name: probe(name, timeout=timeout) for name in SUPPORTED_PROVIDERS}


def installed_providers() -> list[str]:
    return [name for name in SUPPORTED_PROVIDERS if detect(name)["installed"]]


def _start_ollama() -> dict[str, Any]:
    cli = find_ollama_cli()
    if not cli:
        return {"ok": False, "error": "Ollama is not installed or its CLI could not be found"}
    try:
        kwargs: dict[str, Any] = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if os.name == "nt": kwargs["creationflags"] = creation_flags()
        else: kwargs["start_new_session"] = True
        subprocess.Popen([cli, "serve"], **kwargs)
        return {"ok": True, "command": [cli, "serve"]}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _start_lmstudio() -> dict[str, Any]:
    cli = find_lms_cli()
    if not cli:
        return {"ok": False, "error": "LM Studio is installed but the 'lms' CLI is unavailable; enable/install the LM Studio CLI first"}
    return run([cli, "server", "start", "--port", "1234"], timeout=60)


def start(name: str, timeout: float = 30.0) -> dict[str, Any]:
    provider_name = normalize_provider(name)
    before = probe(provider_name, timeout=min(timeout, 5.0))
    if before["healthy"]:
        return {"ok": True, "skipped": True, "reason": "already healthy", "before": before, "after": before}
    if not before["installed"]:
        return {"ok": False, "error": f"provider '{provider_name}' is not installed", "before": before}
    action = _start_ollama() if provider_name == "ollama" else _start_lmstudio()
    if not action.get("ok"):
        return {"ok": False, "action": action, "before": before}
    deadline = time.monotonic() + max(1.0, timeout)
    after = probe(provider_name, timeout=3.0)
    while not after["healthy"] and time.monotonic() < deadline:
        time.sleep(1.0)
        after = probe(provider_name, timeout=3.0)
    return {"ok": bool(after["healthy"]), "action": action, "before": before, "after": after}


def _stop_ollama() -> dict[str, Any]:
    if os.name == "nt":
        taskkill = shutil.which("taskkill")
        if not taskkill: return {"ok": False, "error": "taskkill unavailable"}
        attempts = [run([taskkill, "/IM", image, "/T", "/F"], timeout=30) for image in ("ollama app.exe", "ollama.exe")]
        return {"ok": any(item.get("ok") for item in attempts), "attempts": attempts}
    if shutil.which("systemctl"):
        return run(["systemctl", "--user", "stop", "ollama"], timeout=60)
    return {"ok": False, "error": "no supported Ollama stop adapter"}


def _stop_lmstudio() -> dict[str, Any]:
    cli = find_lms_cli()
    if not cli: return {"ok": False, "error": "LM Studio 'lms' CLI unavailable"}
    return run([cli, "server", "stop"], timeout=60)


def stop(name: str, timeout: float = 30.0) -> dict[str, Any]:
    provider_name = normalize_provider(name)
    before = probe(provider_name, timeout=3.0)
    if not before["healthy"]:
        return {"ok": True, "skipped": True, "reason": "already stopped or unreachable", "before": before, "after": before}
    action = _stop_ollama() if provider_name == "ollama" else _stop_lmstudio()
    deadline = time.monotonic() + max(1.0, timeout)
    after = probe(provider_name, timeout=2.0)
    while after["healthy"] and time.monotonic() < deadline:
        time.sleep(1.0)
        after = probe(provider_name, timeout=2.0)
    return {"ok": not after["healthy"], "action": action, "before": before, "after": after}


def openclaw_executable() -> str | None:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found: return found
    return None


def openclaw_model_status() -> dict[str, Any]:
    executable = openclaw_executable()
    if not executable: return {"ok": False, "error": "OpenClaw CLI unavailable", "defaultModel": None}
    result = run([executable, "models", "status", "--json"], timeout=30)
    if not result.get("ok"):
        return {"ok": False, "error": result.get("stderr") or result.get("error"), "defaultModel": None, "raw": result}
    try:
        document = json.loads(result.get("stdout") or "{}")
    except json.JSONDecodeError as exc:
        return {"ok": False, "error": f"invalid OpenClaw models status JSON: {exc}", "defaultModel": None}

    def find_default(value: Any) -> str | None:
        if isinstance(value, dict):
            for key in ("defaultModel", "default", "primary", "model"):
                found = value.get(key)
                if isinstance(found, str) and "/" in found: return found
                if isinstance(found, dict):
                    nested = found.get("primary") or found.get("default")
                    if isinstance(nested, str) and "/" in nested: return nested
            for nested_value in value.values():
                result_value = find_default(nested_value)
                if result_value: return result_value
        elif isinstance(value, list):
            for nested_value in value:
                result_value = find_default(nested_value)
                if result_value: return result_value
        return None

    return {"ok": True, "defaultModel": find_default(document), "document": document}


def model_provider(model_ref: str | None) -> str | None:
    if not isinstance(model_ref, str) or "/" not in model_ref: return None
    prefix = model_ref.split("/", 1)[0].strip().lower()
    return prefix if prefix in SUPPORTED_PROVIDERS else None
