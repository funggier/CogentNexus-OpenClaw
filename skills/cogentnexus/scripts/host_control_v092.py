#!/usr/bin/env python3
"""CogentNexus v0.9.2 Host control shim.

Preserves every v0.9.1 watchdog/plugin/lifecycle safety fence while changing the
delegated Host implementation to the provider-neutral v0.9.2 overlay.
"""
from __future__ import annotations

from pathlib import Path

import host_control_v091 as v091

HERE = Path(__file__).resolve()
v091.legacy.HOST = HERE.with_name("host_provider_v092.py")


if __name__ == "__main__":
    raise SystemExit(v091.main())
