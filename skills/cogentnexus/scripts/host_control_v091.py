#!/usr/bin/env python3
"""v0.9.0 Host control shim with symmetric enable rollback."""
from __future__ import annotations

import json
from pathlib import Path

import host_control as legacy

HERE = Path(__file__).resolve()
legacy.HOST = HERE.with_name("host_v091.py")


def main() -> int:
    argv = legacy.sys.argv[1:]
    root = legacy.root_from_argv(argv)
    command, _action = legacy.command_from_argv(argv)

    if command != "enable":
        return legacy.main()

    try:
        legacy.apply_watchdog_compat(root)
    except Exception as error:
        print(json.dumps({
            "result":"error",
            "error":f"CogentNexus watchdog compatibility failed before enable: {error}",
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
        "delegateExitCode":code,
        "rollbackError":rollback_error,
    })
    if rollback_error:
        print(json.dumps({
            "result":"error",
            "error":"CogentNexus enable failed and watchdog compatibility rollback also failed",
            "delegateExitCode":code,
            "rollbackError":rollback_error,
        }, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
