#!/usr/bin/env python3
"""Verified OpenClaw Gateway process boundary for v0.9.2 config transactions."""
from __future__ import annotations

import os
import shutil
import subprocess
from typing import Any


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def openclaw_executable() -> str | None:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        value = shutil.which(name)
        if value:
            return value
    return None


def _run(argv: list[str], timeout: int) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=creation_flags(),
        )
        return {
            "ok": proc.returncode == 0,
            "exitCode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "command": argv,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc), "command": argv}


def _healthy_status(result: dict[str, Any]) -> bool:
    if not result.get("ok"):
        return False
    evidence = f"{result.get('stdout', '')}\n{result.get('stderr', '')}".lower()
    negative = (
        "connectivity probe: failed",
        "runtime: stopped",
        "service is loaded but not running",
        "econnrefused",
    )
    if any(marker in evidence for marker in negative):
        return False
    return "runtime: running" in evidence and "connectivity probe: ok" in evidence


def activate_current_config() -> dict[str, Any]:
    """Force Gateway to reload the config currently durable on disk, then verify.

    A successful `openclaw config validate` proves only the file. Provider/model
    route changes are not considered active until a Gateway process boundary has
    completed and the post-boundary status probe is healthy.
    """
    executable = openclaw_executable()
    if not executable:
        return {"ok": False, "error": "OpenClaw CLI unavailable"}

    restart = _run([executable, "gateway", "restart"], 180)
    fallback = None
    if not restart.get("ok"):
        fallback = _run([executable, "gateway", "start"], 180)
        if not fallback.get("ok"):
            return {
                "ok": False,
                "phase": "gateway-boundary",
                "restart": restart,
                "fallbackStart": fallback,
            }

    status = _run([executable, "gateway", "status"], 60)
    healthy = _healthy_status(status)
    return {
        "ok": healthy,
        "phase": "verified" if healthy else "gateway-verification",
        "restart": restart,
        "fallbackStart": fallback,
        "status": status,
    }
