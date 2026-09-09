#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 operator CLI boundary.

Ownership rules:
- CNX lifecycle commands own CNX/Gateway lifecycle only.
- `local <adapter> ...` owns local adapter process lifecycle only.
- OpenClaw owns provider/model/auth/routing.
- Provider metadata exposed by status/check is diagnostic, never lifecycle authority.

The old provider-routing implementation is intentionally not retained here.
Legacy `--provider` input is rejected rather than silently reinterpreted.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import checks_v092 as checks
import local_adapter
import provider

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogentnexus-openclaw"
HOST_CONTROL = HERE.with_name("host_control_v092.py")


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def parse_globals(argv: list[str]) -> tuple[Path, list[str], bool]:
    root = DEFAULT_ROOT
    json_mode = False
    cleaned: list[str] = []
    index = 0
    while index < len(argv):
        value = argv[index]
        if value == "--root" and index + 1 < len(argv):
            root = Path(argv[index + 1]).expanduser().resolve()
            index += 2
            continue
        if value == "--json":
            json_mode = True
            index += 1
            continue
        cleaned.append(value)
        index += 1
    return root.resolve(), cleaned, json_mode


def option_value(args: list[str], name: str) -> str | None:
    for index, value in enumerate(args):
        if value == name and index + 1 < len(args):
            return args[index + 1]
        if value.startswith(name + "="):
            return value[len(name) + 1 :]
    return None


def has_option(args: list[str], name: str) -> bool:
    return option_value(args, name) is not None or name in args


def run_host(root: Path, args: list[str], timeout: int = 420) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(HOST_CONTROL), "--root", str(root), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
        env=os.environ.copy(),
    )
    raw = proc.stdout.strip()
    parsed: Any = None
    if raw:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
    return {
        "ok": proc.returncode == 0,
        "exitCode": proc.returncode,
        "output": parsed,
        "stdout": raw,
        "stderr": proc.stderr.strip(),
    }


def delegate(root: Path, args: list[str], interactive: bool = False) -> int:
    command = [sys.executable, str(HOST_CONTROL), "--root", str(root), *args]
    if interactive:
        return int(subprocess.run(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, creationflags=creation_flags()).returncode)
    proc = subprocess.run(command, capture_output=True, text=True, creationflags=creation_flags())
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return int(proc.returncode)


def provider_snapshot() -> dict[str, Any]:
    values: dict[str, Any] = {}
    for name in provider.SUPPORTED_PROVIDERS:
        values[name] = provider.probe(name)
    return {"providerMetadata": values, "authority": "openclaw"}


def do_check(root: Path, args: list[str]) -> tuple[int, dict[str, Any]]:
    if len(args) < 2:
        return 2, {"result": "error", "error": "Usage: cnxclaw check system|cogentnexus-openclaw|config|openclaw|gateway|provider|model|storage|recovery|delivery|resources"}
    component = args[1].lower()
    explicit = option_value(args[2:], "--provider")
    if component == "provider" and len(args) >= 3 and not args[2].startswith("-"):
        explicit = args[2]
    try:
        report = checks.system_check(root, explicit) if component == "system" else checks.component_check(root, component, explicit)
        return int(report["exitCode"]), report
    except Exception as error:
        return 3, {"check": component, "verdict": "INDETERMINATE", "exitCode": 3, "error": str(error), "readOnly": True, "stateChanged": False}


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def help_text() -> str:
    return """CogentNexus-OpenClaw v0.9.5

CNX lifecycle (no provider/model selection):
  cnxclaw.cmd start
  cnxclaw.cmd stop
  cnxclaw.cmd restart
  cnxclaw.cmd status
  cnxclaw.cmd enable
  cnxclaw.cmd disable
  cnxclaw.cmd reset
  cnxclaw.cmd uninstall

Local adapter lifecycle (does not mutate OpenClaw routing):
  cnxclaw.cmd local ollama start
  cnxclaw.cmd local ollama stop
  cnxclaw.cmd local ollama restart
  cnxclaw.cmd local ollama status
  cnxclaw.cmd local ollama check

Inspection (read-only):
  cnxclaw.cmd check system
  cnxclaw.cmd check provider
  cnxclaw.cmd provider list
  cnxclaw.cmd provider status

Provider/model/auth/routing selection is owned by OpenClaw.
"""


def main(argv: list[str] | None = None) -> int:
    root, args, json_mode = parse_globals(list(sys.argv[1:] if argv is None else argv))
    if not args or args[0] in {"-h", "--help", "help"}:
        print(help_text())
        return 0

    command = args[0].lower()

    if command == "local":
        if len(args) != 3:
            emit({"result": "error", "error": "Usage: cnxclaw local ollama start|stop|restart|status|check"})
            return 2
        try:
            code, result = local_adapter.run(root, args[1], args[2])
        except ValueError as error:
            emit({"result": "error", "error": str(error)})
            return 2
        emit(result)
        return code

    if command in {"start", "stop", "restart", "status", "enable", "disable", "reset", "uninstall"} and has_option(args[1:], "--provider"):
        emit({
            "result": "error",
            "error": "--provider is no longer a CNX lifecycle authority in v0.9.5; select provider/model in OpenClaw instead",
            "compatibility": "legacy input rejected and no route/lifecycle transition was attempted",
        })
        return 2

    if command == "check":
        code, report = do_check(root, args)
        print(json.dumps(report, ensure_ascii=False, indent=2) if json_mode else checks.render(report))
        return code

    if command == "provider":
        action = args[1].lower() if len(args) > 1 else "status"
        if action not in {"list", "status"} or len(args) > 2:
            emit({"result": "error", "error": "Usage: cnxclaw provider list|status"})
            return 2
        emit(provider_snapshot())
        return 0

    if command == "status":
        if len(args) != 1:
            emit({"result": "error", "error": "Usage: cnxclaw status"})
            return 2
        host = run_host(root, ["status"], timeout=120)
        emit({"host": host.get("output") if host.get("ok") else host, **provider_snapshot()})
        return 0 if host.get("ok") else 1

    if command in {"start", "stop", "restart", "enable", "disable"}:
        if len(args) != 1:
            emit({"result": "error", "error": f"Usage: cnxclaw {command}"})
            return 2
        return delegate(root, [command])

    if command == "reset":
        if len(args) != 1:
            emit({"result": "error", "error": "Usage: cnxclaw reset"})
            return 2
        return delegate(root, [command], interactive=True)

    if command == "uninstall":
        if len(args) != 1:
            emit({"result": "error", "error": "Usage: cnxclaw uninstall"})
            return 2
        return delegate(root, [command], interactive=True)

    if command == "cloud":
        emit({
            "result": "delegated-to-openclaw",
            "authority": "openclaw",
            "message": "Cloud provider/model selection is owned by OpenClaw; CogentNexus-OpenClaw does not implement a cloud routing transition.",
        })
        return 0

    return delegate(root, args)


if __name__ == "__main__":
    raise SystemExit(main())
