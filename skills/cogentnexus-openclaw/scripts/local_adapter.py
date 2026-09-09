#!/usr/bin/env python3
"""Explicit local-adapter lifecycle boundary for CogentNexus-OpenClaw.

This module owns only local inference-adapter process operations. It must never
select, mutate, or commit an OpenClaw provider/model/auth route.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import provider


SUPPORTED_LOCAL_ADAPTERS = ("ollama",)


def _normalize(name: str) -> str:
    value = (name or "").strip().lower()
    if value not in SUPPORTED_LOCAL_ADAPTERS:
        raise ValueError(
            f"unsupported local adapter: {name!r}; expected one of: {', '.join(SUPPORTED_LOCAL_ADAPTERS)}"
        )
    return value


def run(root: Path, adapter: str, action: str) -> tuple[int, dict[str, Any]]:
    del root  # The adapter boundary is intentionally independent of CNX Host state.
    name = _normalize(adapter)
    operation = (action or "").strip().lower()
    if operation not in {"start", "stop", "restart", "status", "check"}:
        return 2, {"result": "error", "error": "Usage: cnxclaw local ollama start|stop|restart|status|check"}

    if operation == "status":
        return 0, {"result": "ok", "adapter": name, "status": provider.probe(name)}
    if operation == "check":
        status = provider.probe(name)
        return (0 if status.get("healthy") else 1), {
            "result": "ok" if status.get("healthy") else "not-ready",
            "adapter": name,
            "status": status,
        }
    if operation == "start":
        result = provider.start(name)
        return (0 if result.get("ok") else 1), {"result": "ok" if result.get("ok") else "error", "adapter": name, "operation": operation, "details": result}
    if operation == "stop":
        result = provider.stop(name)
        return (0 if result.get("ok") else 1), {"result": "ok" if result.get("ok") else "error", "adapter": name, "operation": operation, "details": result}

    stop_result = provider.stop(name)
    if not stop_result.get("ok"):
        return 1, {"result": "error", "adapter": name, "operation": operation, "phase": "stop", "details": stop_result}
    start_result = provider.start(name)
    return (0 if start_result.get("ok") else 1), {
        "result": "ok" if start_result.get("ok") else "error",
        "adapter": name,
        "operation": operation,
        "stop": stop_result,
        "start": start_result,
    }
