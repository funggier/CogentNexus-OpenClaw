#!/usr/bin/env python3
"""CogentNexus v0.9.2 assistant-delivery transport entry.

Windows npm installs expose ``openclaw.cmd`` as a command shim. Python's
CreateProcess path is not a reliable execution boundary for that shim and can
fail with WinError 2 even while the same command works from PowerShell.

This entry keeps the v0.9.1 durable delivery/lease implementation unchanged,
but replaces its Gateway RPC transport with a direct ``node.exe openclaw.mjs``
invocation. That removes the command-shell hop and gives the Host ownership of
the actual Node process so timeout/process-tree handling remains deterministic.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

import host_delivery as base


def _openclaw_node_command() -> list[str]:
    node = shutil.which("node.exe" if os.name == "nt" else "node") or shutil.which("node")
    if not node:
        raise FileNotFoundError("Node executable not found on PATH")

    shim = base.openclaw_executable()
    shim_path = Path(shim).resolve()
    candidates = [
        shim_path.with_name("node_modules") / "openclaw" / "openclaw.mjs",
        Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "openclaw" / "openclaw.mjs",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return [node, str(candidate)]
    raise FileNotFoundError(
        "OpenClaw JavaScript CLI entry not found next to npm shim: "
        + ", ".join(str(path) for path in candidates)
    )


def gateway_rpc(method: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    command = [
        *_openclaw_node_command(),
        "gateway",
        "call",
        method,
        "--params",
        json.dumps(params or {}, ensure_ascii=False, separators=(",", ":")),
        "--json",
    ]
    result = base.run(command, timeout=timeout, check=True)
    return base._parse_json_stream(method, result)


# Functions such as inject_assistant resolve gateway_rpc through the base
# module's globals at execution time, so replacing this symbol redirects every
# delivery RPC without duplicating the durable delivery implementation.
base.gateway_rpc = gateway_rpc


if __name__ == "__main__":
    raise SystemExit(base.main())
