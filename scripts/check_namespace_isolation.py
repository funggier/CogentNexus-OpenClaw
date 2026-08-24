#!/usr/bin/env python3
"""Reject current filenames/content that escape the OpenClaw variant namespace."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_PREFIXES = ("docs/operations/coordination/",)
MIGRATION_PATHS = {
    "scripts/install.ps1", "scripts/install.sh",
    "skills/cogentnexus-openclaw/scripts/namespace_ownership.py",
    "tests/test_namespace_ownership.py", "tests/test_namespace_install_contract.py",
    "tests/test_namespace_lint.py", "docs/releases/v0.9.3.md",
    "docs/V093_RECOVERY_REALITY_TESTS.md",
    "scripts/test-v093-gateway-convergence-windows.ps1",
    "scripts/test-v093-ollama-recovery-windows-v2.ps1",
    "scripts/test-v093-ollama-recovery-windows-v3.ps1",
    "scripts/test-v093-recovery-reality-windows.ps1",
}
FORBIDDEN = re.compile(
    r"cnx\.cmd|(?<![A-Za-z0-9_-])\.cogent(?:[/\\\"'\s]|$)|"
    r"skills[/\\]cogentnexus(?:[/\\\"'\s]|$)|"
    r"openclaw-plugin-cogentnexus-rotation|cogentnexus-rotation|"
    r"cogentnexus(?!(?:[-._]?openclaw|[-._]?hermesagent))(?=[-./_:]|\s|$)",
    re.IGNORECASE,
)
LEGACY_ENV = re.compile(r"(?<![A-Za-z0-9_])CNX_(?=[A-Z])")


def historical(relative: str) -> bool:
    return relative.startswith(HISTORICAL_PREFIXES) or (
        relative.startswith("docs/releases/") and relative != "docs/releases/v0.9.3.md"
    )


def migration_literal_allowed(relative: str, line: str) -> bool:
    if relative not in MIGRATION_PATHS:
        return False
    if relative.startswith("docs/") or relative.startswith("scripts/test-v093-") or relative.startswith("tests/test_namespace_"):
        return True
    lowered = line.lower()
    legacy_literals = (
        "cogentnexus-rotation", "openclaw-plugin-cogentnexus-rotation",
        "cogentnexus supervisor", "cogentnexus-supervisor",
        "ai.cogentnexus.supervisor", ".cogent", "skills/cogentnexus",
        'workspace / "skills" / "cogentnexus"', 'workspace / "cnx"', "workspace/cnx",
        "cnx.cmd",
    )
    return any(marker in lowered for marker in ("legacy", "migration", *legacy_literals))


def find_violations(relative: str, text: str) -> list[str]:
    normalized = relative.replace("\\", "/")
    if historical(normalized):
        return []
    failures: list[str] = []
    if (FORBIDDEN.search(normalized) or LEGACY_ENV.search(normalized)) and not migration_literal_allowed(normalized, normalized):
        failures.append(f"{normalized}: forbidden operational filename")
    for number, line in enumerate(text.splitlines(), 1):
        if normalized == "scripts/check_namespace_isolation.py":
            continue
        if (FORBIDDEN.search(line) or LEGACY_ENV.search(line)) and not migration_literal_allowed(normalized, line):
            failures.append(f"{normalized}:{number}: forbidden generic namespace: {line.strip()}")
    return failures


def main() -> int:
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    failures: list[str] = []
    for relative in listed.stdout.splitlines():
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        failures.extend(find_violations(relative, text))
    if failures:
        print("CogentNexus-OpenClaw namespace isolation: FAIL", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("CogentNexus-OpenClaw namespace isolation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
