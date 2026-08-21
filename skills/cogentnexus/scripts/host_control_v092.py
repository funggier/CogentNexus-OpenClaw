#!/usr/bin/env python3
"""CogentNexus v0.9.2 Host control shim.

Preserves every v0.9.1 watchdog/plugin safety fence while routing normal Host
work through the provider-neutral v0.9.2 overlay and destructive lifecycle
through the provider-aware v0.9.2 wrapper.
"""
from __future__ import annotations

from pathlib import Path

import host_control_v091 as v091
import lifecycle_v092 as lifecycle

HERE = Path(__file__).resolve()
v091.legacy.HOST = HERE.with_name("host_provider_v092.py")


def option_value(argv: list[str], name: str) -> str | None:
    for index, value in enumerate(argv):
        if value == name and index + 1 < len(argv):
            return argv[index + 1]
        prefix = name + "="
        if value.startswith(prefix):
            return value[len(prefix):]
    return None


def main() -> int:
    argv = v091.legacy.sys.argv[1:]
    root = v091.legacy.root_from_argv(argv)
    command, _ = v091.legacy.command_from_argv(argv)
    if command in {"reset", "uninstall"}:
        return lifecycle.main(command, root, option_value(argv, "--provider"))
    return v091.main()


if __name__ == "__main__":
    raise SystemExit(main())
