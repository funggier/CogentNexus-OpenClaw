#!/usr/bin/env python3
"""Compatibility facade for the canonical v0.9.5 local adapter boundary.

New code should import `local_adapters_v095`. This module remains as a narrow
compatibility shim for existing callers and intentionally owns no provider
routing authority.
"""
from __future__ import annotations

from typing import Any

from local_adapters_v095 import (
    local_ollama_check,
    local_ollama_restart,
    local_ollama_start,
    local_ollama_status,
    local_ollama_stop,
)

SUPPORTED_LOCAL_ADAPTERS = ("ollama",)


def run(root: Any, adapter: str, action: str) -> tuple[int, dict[str, Any]]:
    del root
    name = (adapter or "").strip().lower()
    operation = (action or "").strip().lower()
    if name != "ollama":
        return 2, {"result": "error", "error": "unsupported local adapter: expected ollama"}
    functions = {
        "status": lambda: (0, local_ollama_status()),
        "check": local_ollama_check,
        "start": local_ollama_start,
        "stop": local_ollama_stop,
        "restart": local_ollama_restart,
    }
    function = functions.get(operation)
    if function is None:
        return 2, {"result": "error", "error": "Usage: cnxclaw local ollama start|stop|restart|status|check"}
    return function()
