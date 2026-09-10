#!/usr/bin/env python3
"""Canonical local-adapter boundary for CogentNexus-OpenClaw v0.9.5.

This module owns local inference-adapter process operations only. It never
selects or mutates OpenClaw provider/model/auth routing and never changes CNX
Host generation or lifecycle mode.
"""
from __future__ import annotations

from typing import Any

import provider


def local_ollama_status() -> dict[str, Any]:
    return {"result": "ok", "adapter": "ollama", "status": provider.probe("ollama")}


def local_ollama_check() -> tuple[int, dict[str, Any]]:
    status = provider.probe("ollama")
    healthy = bool(status.get("healthy"))
    return (0 if healthy else 1), {
        "result": "ok" if healthy else "not-ready",
        "adapter": "ollama",
        "status": status,
    }


def local_ollama_start() -> tuple[int, dict[str, Any]]:
    result = provider.start("ollama")
    ok = bool(result.get("ok"))
    return (0 if ok else 1), {
        "result": "ok" if ok else "error",
        "adapter": "ollama",
        "action": "start",
        "details": result,
    }


def local_ollama_stop() -> tuple[int, dict[str, Any]]:
    result = provider.stop("ollama")
    ok = bool(result.get("ok"))
    return (0 if ok else 1), {
        "result": "ok" if ok else "error",
        "adapter": "ollama",
        "action": "stop",
        "details": result,
    }


def local_ollama_restart() -> tuple[int, dict[str, Any]]:
    stop_code, stop = local_ollama_stop()
    if stop_code != 0:
        return stop_code, {
            "result": "error",
            "adapter": "ollama",
            "action": "restart",
            "phase": "stop",
            "stop": stop,
        }
    start_code, start = local_ollama_start()
    return start_code, {
        "result": "ok" if start_code == 0 else "error",
        "adapter": "ollama",
        "action": "restart",
        "stop": stop,
        "start": start,
    }


def run(root: Any, adapter: str, action: str) -> tuple[int, dict[str, Any]]:
    """Compatibility dispatcher used by older CLI callers.

    `root` is intentionally ignored: local adapter lifecycle has no CNX Host
    state authority. Only Ollama is exposed by the v0.9.5 command contract.
    """
    del root
    name = (adapter or "").strip().lower()
    operation = (action or "").strip().lower()
    if name != "ollama":
        return 2, {"result": "error", "error": "unsupported local adapter: expected ollama"}
    if operation == "status":
        return 0, local_ollama_status()
    if operation == "check":
        return local_ollama_check()
    if operation == "start":
        return local_ollama_start()
    if operation == "stop":
        return local_ollama_stop()
    if operation == "restart":
        return local_ollama_restart()
    return 2, {"result": "error", "error": "Usage: cnxclaw local ollama start|stop|restart|status|check"}
