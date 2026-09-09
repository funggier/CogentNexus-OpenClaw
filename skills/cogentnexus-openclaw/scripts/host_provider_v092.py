#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.2 Host façade.

The proven v0.9.4-era provider-event and recovery payload remains executable
unchanged for this TDD slice. Only the legacy lifecycle ``--provider`` bridge is
redefined here: in v0.9.5 OpenClaw owns provider/model/auth routing and provider
process lifecycle, so the flag is accepted solely as backward-compatible syntax
and is removed before delegating to the CNX Gateway/runtime lifecycle.
"""
from __future__ import annotations

from pathlib import Path


_WRAPPER_NAME = __name__
_LEGACY_PATH = Path(__file__).with_name("host_provider_v092_legacy_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_host_provider_v092_legacy_v094_embedded"
try:
    exec(compile(_LEGACY_PATH.read_text(encoding="utf-8"), str(_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME


def provider_aware_runtime(root: Path, *args: str, timeout: int = 180, check: bool = True):
    """Delegate lifecycle operations without taking provider lifecycle authority."""
    values = list(args)
    if len(values) >= 2 and values[0] == "lifecycle" and values[1] in {"start", "stop"}:
        values = [value for value in values if value != "--provider"]
    return ORIGINAL_RUNTIME(root, *values, timeout=timeout, check=check)


# Replace only the legacy provider-lifecycle translation surface. The event and
# recovery functions from the compatibility payload remain unchanged until their
# own RED/GREEN slice.
legacy.runtime = provider_aware_runtime


if __name__ == "__main__":
    raise SystemExit(legacy.main())
