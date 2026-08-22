#!/usr/bin/env python3
"""Read-only process liveness helpers for CogentNexus v0.9.2 provider events.

Python's ``os.kill(pid, 0)`` is a non-destructive existence probe on POSIX, but
on Windows ``os.kill`` maps non-console signals to ``TerminateProcess``.  The
provider event adapter must therefore never use that idiom on Windows.
"""
from __future__ import annotations

import ctypes
import os
from typing import Any

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
STILL_ACTIVE = 259


def _pid_alive_windows(pid: int, kernel32: Any | None = None) -> bool:
    if pid <= 0:
        return False
    kernel = kernel32 or ctypes.windll.kernel32
    handle = kernel.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not handle:
        return False
    try:
        exit_code = ctypes.c_ulong(0)
        if not kernel.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
            return False
        return int(exit_code.value) == STILL_ACTIVE
    finally:
        kernel.CloseHandle(handle)


def safe_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            return _pid_alive_windows(pid)
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def patch_provider_events(module: Any) -> None:
    """Replace the adapter's private liveness probe with the safe implementation."""
    module._pid_alive = safe_pid_alive
