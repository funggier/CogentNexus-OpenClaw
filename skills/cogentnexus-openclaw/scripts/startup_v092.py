#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.2 startup adapter wiring."""
from __future__ import annotations

from pathlib import Path

import startup as legacy

HERE = Path(__file__).resolve()


def host_control_path() -> Path:
    return HERE.with_name("host_control_v092.py")


legacy.host_control_path = host_control_path


if __name__ == "__main__":
    raise SystemExit(legacy.main())
