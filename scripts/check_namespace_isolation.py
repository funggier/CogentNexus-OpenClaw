#!/usr/bin/env python3
"""Reject current operational surfaces that escape the OpenClaw namespace."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_PREFIXES = ("docs/operations/coordination/",)
MIGRATION_ALLOWLIST = {
    "scripts/install.ps1", "scripts/install.sh",
    "skills/cogentnexus-openclaw/scripts/namespace_ownership.py",
    "tests/test_namespace_ownership.py", "tests/test_namespace_install_contract.py",
    "docs/releases/v0.9.3.md",
}
LEGACY = re.compile(
    r"cnx\.cmd|(?<![A-Za-z0-9_-])\.cogent(?:[/\\\"'\s]|$)|"
    r"skills[/\\]cogentnexus(?:[/\\\"'\s]|$)|cogentnexus-rotation|"
    r"openclaw-plugin-cogentnexus-rotation|(?<![A-Za-z0-9_])CNX_(?=[A-Z])"
)
BARE_DISPLAY = re.compile(r"CogentNexus(?!-OpenClaw|-HermesAgent)")


def main() -> int:
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    failures: list[str] = []
    for relative in listed.stdout.splitlines():
        normalized = relative.replace("\\", "/")
        if normalized.startswith(HISTORICAL_PREFIXES) or (normalized.startswith("docs/releases/") and normalized != "docs/releases/v0.9.3.md"):
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if normalized == "scripts/check_namespace_isolation.py" and (line.lstrip().startswith('r"') or line.startswith("BARE_DISPLAY")):
                continue
            if LEGACY.search(line) and normalized not in MIGRATION_ALLOWLIST:
                failures.append(f"{normalized}:{number}: forbidden legacy namespace: {line.strip()}")
            if BARE_DISPLAY.search(line) and normalized not in MIGRATION_ALLOWLIST:
                failures.append(f"{normalized}:{number}: bare product display name: {line.strip()}")
    if failures:
        print("CogentNexus-OpenClaw namespace isolation: FAIL", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("CogentNexus-OpenClaw namespace isolation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
