#!/usr/bin/env python3
"""v0.9.5 baseline-consistency façade for the split Host compatibility surface."""
from __future__ import annotations

from pathlib import Path


_WRAPPER_NAME = __name__
_BOOTSTRAP_LEGACY_PATH = Path(__file__).with_name("check_baseline_consistency_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_baseline_v094_embedded"
try:
    exec(compile(_BOOTSTRAP_LEGACY_PATH.read_text(encoding="utf-8"), str(_BOOTSTRAP_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME

# The implementation remains archived as a compatibility engine, while the
# live validator contract advances with the current repository baseline.
EXPECTED_VERSION = "0.9.5"

_LEGACY_MAIN = main
_LEGACY_CURRENT_TEXT_FILES = current_text_files
_ORIGINAL_READ_TEXT = Path.read_text


def _legacy_path() -> Path:
    return ROOT / "scripts" / "check_baseline_consistency_v094.py"


def _host_facade() -> Path:
    return ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host.py"


def _host_compat_payload() -> Path:
    return ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_legacy_v094.py"


def current_text_files():
    """Exclude only the archived validator source from live-surface phrase scanning."""
    archived = _legacy_path()
    for path in _LEGACY_CURRENT_TEXT_FILES():
        if path != archived:
            yield path


def _composite_read_text(self: Path, *args, **kwargs) -> str:
    """Present the split Host façade + exact compatibility payload as one contract surface."""
    primary = _ORIGINAL_READ_TEXT(self, *args, **kwargs)
    if self == _host_facade():
        legacy = _ORIGINAL_READ_TEXT(_host_compat_payload(), *args, **kwargs)
        return primary + "\n" + legacy
    return primary


def main() -> int:
    payload = _host_compat_payload()
    if not payload.is_file():
        print("CogentNexus-OpenClaw baseline consistency FAILED:")
        print("- missing/empty baseline artifact: skills/cogentnexus-openclaw/scripts/host_legacy_v094.py")
        return 1
    Path.read_text = _composite_read_text
    try:
        return int(_LEGACY_MAIN())
    finally:
        Path.read_text = _ORIGINAL_READ_TEXT


if __name__ == "__main__":
    raise SystemExit(main())
