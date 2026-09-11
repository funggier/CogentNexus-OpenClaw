#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.1 Host façade.

The proven v0.9.4-era v0.9.1 hardening payload remains executable unchanged.
This façade removes only the legacy global provider-lifecycle request from the
transactional enable path. OpenClaw owns provider/model/auth routing in v0.9.5.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable


_WRAPPER_NAME = __name__
_LEGACY_PATH = Path(__file__).with_name("host_v091_legacy_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_host_v091_legacy_v094_embedded"
try:
    exec(compile(_LEGACY_PATH.read_text(encoding="utf-8"), str(_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME

_LEGACY_ENABLE = enable


def _provider_neutral_runtime(original: Callable[..., Any]) -> Callable[..., Any]:
    """Drop only the obsolete global provider-start request from enable."""
    def invoke(root: Path, *args: str, **kwargs: Any):
        values = list(args)
        if len(values) >= 2 and values[0] == "lifecycle" and values[1] == "start":
            values = [value for value in values if value != "--provider"]
        return original(root, *values, **kwargs)

    return invoke


def enable(root: Path) -> dict[str, Any]:
    """Run the proven transactional enable path without provider ownership."""
    original_runtime = legacy.runtime
    legacy.runtime = _provider_neutral_runtime(original_runtime)
    try:
        return _LEGACY_ENABLE(root)
    finally:
        legacy.runtime = original_runtime


legacy.enable = enable


if __name__ == "__main__":
    raise SystemExit(legacy.main())
