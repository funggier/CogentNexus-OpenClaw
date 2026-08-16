#!/usr/bin/env python3
"""Bounded CogentNexus Host adapter for privileged OpenClaw context maintenance.

This adapter intentionally exposes only the exact sessions.compact operation.
It never accepts an arbitrary Gateway method name from plugin/runtime callers.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogent"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def openclaw_executable() -> str:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


def validate_session_key(value: str) -> str:
    key = value.strip()
    if not key or len(key) > 2048 or "\x00" in key:
        raise ValueError("invalid OpenClaw session key")
    return key


def append_audit(root: Path, payload: dict[str, Any]) -> None:
    path = root / "runtime" / "context-host-events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def compact(root: Path, session_key: str, max_lines: int | None, timeout_ms: int) -> Any:
    key = validate_session_key(session_key)
    bounded_timeout = max(5_000, min(int(timeout_ms), 600_000))
    params: dict[str, Any] = {"key": key}
    if max_lines is not None:
        lines = int(max_lines)
        if lines < 1 or lines > 20_000:
            raise ValueError("max-lines must be between 1 and 20000")
        params["maxLines"] = lines

    command = [
        openclaw_executable(),
        "gateway",
        "call",
        "sessions.compact",
        "--params",
        json.dumps(params, ensure_ascii=False, separators=(",", ":")),
        "--json",
        "--timeout",
        str(bounded_timeout),
    ]
    started = now_iso()
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=bounded_timeout / 1000 + 15,
        creationflags=creation_flags(),
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "OpenClaw sessions.compact failed").strip()
        append_audit(root, {
            "schemaVersion": 1,
            "timestamp": now_iso(),
            "action": "sessions.compact",
            "sessionKey": key,
            "startedAt": started,
            "ok": False,
            "exitCode": result.returncode,
            "error": message[:2000],
        })
        raise RuntimeError(message)

    raw = result.stdout.strip()
    value: Any = None
    if raw:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"OpenClaw sessions.compact returned invalid JSON: {raw[:500]}") from error
    append_audit(root, {
        "schemaVersion": 1,
        "timestamp": now_iso(),
        "action": "sessions.compact",
        "sessionKey": key,
        "startedAt": started,
        "ok": True,
        "maxLines": max_lines,
    })
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    compact_cmd = sub.add_parser("compact")
    compact_cmd.add_argument("--session-key", required=True)
    compact_cmd.add_argument("--max-lines", type=int)
    compact_cmd.add_argument("--timeout-ms", type=int, default=120_000)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command != "compact":
            raise RuntimeError("unsupported Host context command")
        value = compact(args.root.resolve(), args.session_key, args.max_lines, args.timeout_ms)
        print(json.dumps(value, ensure_ascii=False))
        return 0
    except Exception as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
