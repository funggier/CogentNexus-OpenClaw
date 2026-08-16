#!/usr/bin/env python3
"""CogentNexus Host control wrapper for OpenClaw compatibility policy.

OpenClaw 2026.7.1-2 can classify a diagnostic stalled-run abort as a generic
user abort after losing the original stuck_recovery reason. While CogentNexus
owns runtime lifecycle, keep that native watchdog outside the normal CNX run
horizon. The user's previous OpenClaw value is snapshotted and restored on
`cnx disable`; user changes made while managed are never overwritten.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
HOST = HERE.with_name("host.py")
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogent"
WATCHDOG_PATH = "diagnostics.stuckSessionAbortMs"
MANAGED_WATCHDOG_ABORT_MS = 24 * 60 * 60 * 1000


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
    )


def openclaw_executable() -> str:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


def root_from_argv(argv: list[str]) -> Path:
    for index, value in enumerate(argv):
        if value == "--root" and index + 1 < len(argv):
            return Path(argv[index + 1]).resolve()
    return DEFAULT_ROOT.resolve()


def command_from_argv(argv: list[str]) -> tuple[str | None, str | None]:
    skip = False
    positionals: list[str] = []
    for index, value in enumerate(argv):
        if skip:
            skip = False
            continue
        if value == "--root" and index + 1 < len(argv):
            skip = True
            continue
        if value.startswith("-"):
            continue
        positionals.append(value)
    return (positionals[0] if positionals else None, positionals[1] if len(positionals) > 1 else None)


def load_host_mode(root: Path) -> str:
    path = root / "host" / "controller.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        mode = value.get("mode")
        return mode if mode in {"managed", "maintenance", "passthrough"} else "managed"
    except FileNotFoundError:
        return "managed"
    except Exception:
        return "managed"


def snapshot_path(root: Path) -> Path:
    return root / "host" / "openclaw-watchdog-compat.json"


def audit_path(root: Path) -> Path:
    return root / "runtime" / "host-control-events.jsonl"


def append_audit(root: Path, action: str, payload: dict[str, Any]) -> None:
    path = audit_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"schemaVersion": 1, "timestamp": now_iso(), "action": action, **payload}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def config_get(path: str) -> tuple[bool, Any]:
    result = run([openclaw_executable(), "config", "get", path, "--json"], timeout=30)
    if result.returncode != 0:
        return False, None
    raw = result.stdout.strip()
    if not raw:
        return True, None
    try:
        return True, json.loads(raw)
    except json.JSONDecodeError:
        return True, raw


def config_set(path: str, value: Any) -> None:
    result = run(
        [openclaw_executable(), "config", "set", path, json.dumps(value, separators=(",", ":")), "--strict-json"],
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f"failed to set {path}").strip())


def config_unset(path: str) -> None:
    result = run([openclaw_executable(), "config", "unset", path], timeout=60)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f"failed to unset {path}").strip())


def write_snapshot(root: Path, value: dict[str, Any]) -> None:
    path = snapshot_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def apply_watchdog_compat(root: Path) -> dict[str, Any]:
    path = snapshot_path(root)
    existing = path.exists()
    if existing:
        try:
            snapshot = json.loads(path.read_text(encoding="utf-8"))
        except Exception as error:
            raise RuntimeError(f"invalid CogentNexus watchdog snapshot: {error}") from error
    else:
        present, original = config_get(WATCHDOG_PATH)
        snapshot = {
            "schemaVersion": 1,
            "path": WATCHDOG_PATH,
            "originalPresent": present,
            "originalValue": original,
            "managedValue": MANAGED_WATCHDOG_ABORT_MS,
            "capturedAt": now_iso(),
            "applied": False,
        }
        write_snapshot(root, snapshot)

    present, current = config_get(WATCHDOG_PATH)
    if existing and snapshot.get("applied") is True and (not present or current != MANAGED_WATCHDOG_ABORT_MS):
        # The value moved after CNX had applied it. Treat that as operator-owned
        # configuration, never overwrite it on a supervisor tick, and mark the
        # compatibility guarantee inactive so plugin abort handling fails safe.
        snapshot["applied"] = False
        snapshot["operatorOverrideDetectedAt"] = now_iso()
        snapshot["operatorValue"] = current if present else None
        write_snapshot(root, snapshot)
        append_audit(root, "watchdog-compat-operator-override", {"currentPresent": present, "current": current})
        raise RuntimeError(
            "OpenClaw diagnostics.stuckSessionAbortMs changed while CogentNexus was managed; "
            "operator value was preserved and managed start/recovery is blocked until policy is resolved"
        )

    changed = not present or current != MANAGED_WATCHDOG_ABORT_MS
    if changed:
        config_set(WATCHDOG_PATH, MANAGED_WATCHDOG_ABORT_MS)
    snapshot["applied"] = True
    snapshot.pop("operatorValue", None)
    snapshot.pop("operatorOverrideDetectedAt", None)
    snapshot["lastAppliedAt"] = now_iso()
    write_snapshot(root, snapshot)
    append_audit(root, "watchdog-compat-applied", {"changed": changed, "managedValue": MANAGED_WATCHDOG_ABORT_MS})
    return {"changed": changed, "managedValue": MANAGED_WATCHDOG_ABORT_MS}


def restore_watchdog_compat(root: Path) -> dict[str, Any]:
    path = snapshot_path(root)
    if not path.exists():
        return {"restored": False, "reason": "no-snapshot"}
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    present, current = config_get(WATCHDOG_PATH)
    managed_value = snapshot.get("managedValue", MANAGED_WATCHDOG_ABORT_MS)
    if not present or current != managed_value:
        result = {"restored": False, "reason": "user-config-changed", "current": current}
        append_audit(root, "watchdog-compat-preserved-user-change", result)
        path.unlink(missing_ok=True)
        return result

    if snapshot.get("originalPresent"):
        config_set(WATCHDOG_PATH, snapshot.get("originalValue"))
    else:
        config_unset(WATCHDOG_PATH)
    result = {"restored": True, "originalPresent": bool(snapshot.get("originalPresent"))}
    append_audit(root, "watchdog-compat-restored", result)
    path.unlink(missing_ok=True)
    return result


def should_apply(root: Path, command: str | None, action: str | None) -> bool:
    if command == "enable":
        return True
    if load_host_mode(root) == "passthrough":
        return False
    if command in {"start", "restart"}:
        return True
    if command == "gateway" and action in {"start", "restart"}:
        return True
    if command == "supervisor" and action == "tick":
        return True
    return False


def delegate(argv: list[str]) -> int:
    result = subprocess.run(
        [sys.executable, str(HOST), *argv],
        text=True,
        creationflags=creation_flags(),
    )
    return int(result.returncode)


def main() -> int:
    argv = sys.argv[1:]
    root = root_from_argv(argv)
    command, action = command_from_argv(argv)
    try:
        if command == "disable":
            restore_watchdog_compat(root)
        elif should_apply(root, command, action):
            apply_watchdog_compat(root)
    except Exception as error:
        print(json.dumps({"result": "error", "error": f"CogentNexus watchdog compatibility failed: {error}"}, ensure_ascii=False, indent=2))
        return 1
    return delegate(argv)


if __name__ == "__main__":
    raise SystemExit(main())
