#!/usr/bin/env python3
"""CogentNexus v0.9.1 Host control shim with symmetric enable rollback.

Periodic supervisor ticks deliberately bypass the legacy watchdog re-apply path:
the watchdog fence is installed on enable/start/restart and does not need an
OpenClaw CLI process every minute merely to confirm an unchanged value.
"""
from __future__ import annotations

import json
from pathlib import Path

import host_control as legacy

HERE = Path(__file__).resolve()
legacy.HOST = HERE.with_name("host_v091.py")


def main() -> int:
    argv = legacy.sys.argv[1:]
    root = legacy.root_from_argv(argv)
    command, action = legacy.command_from_argv(argv)

    # Before first initialization there is no authority to assume MANAGED. Route
    # non-enable commands directly to host_v091, which seeds PASSTHROUGH. This
    # prevents a portable `cnx gateway start` or `cnx status` from applying the
    # managed watchdog merely because controller.json does not exist yet.
    if command != "enable" and not (root / "host" / "controller.json").exists():
        return legacy.delegate(argv)

    # The scheduled supervisor must remain file/socket-only while healthy.
    # Calling legacy.main() here would run apply_watchdog_compat(), which invokes
    # `openclaw config get` and spins up Node once per schedule even when idle.
    if command == "supervisor" and action == "tick":
        return legacy.delegate(argv)

    if command != "enable":
        return legacy.main()

    try:
        legacy.apply_watchdog_compat(root)
    except Exception as error:
        print(json.dumps({
            "result": "error",
            "error": f"CogentNexus watchdog compatibility failed before enable: {error}",
        }, ensure_ascii=False, indent=2))
        return 1

    code = legacy.delegate(argv)
    if code == 0:
        return 0

    rollback_error = None
    try:
        legacy.restore_watchdog_compat(root)
    except Exception as error:
        rollback_error = str(error)

    legacy.append_audit(root, "watchdog-compat-enable-rollback", {
        "delegateExitCode": code,
        "rollbackError": rollback_error,
    })
    if rollback_error:
        print(json.dumps({
            "result": "error",
            "error": "CogentNexus enable failed and watchdog compatibility rollback also failed",
            "delegateExitCode": code,
            "rollbackError": rollback_error,
        }, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
