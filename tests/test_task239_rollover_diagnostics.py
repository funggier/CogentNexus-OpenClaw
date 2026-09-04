"""CNX-20260904-239 — bounded rollover-prepare diagnostics.

These tests intentionally describe the missing owning-boundary behavior before
production repair. They must fail on the accepted predecessor source because
the child stderr is not merged and the captured output is not bounded/preserved
on the fail-closed path.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).parents[1]
INSTALL_PS1 = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")
MAX_DIAGNOSTIC_CHARS = 4096


def _rollover_prepare_line() -> str:
    match = re.search(r"\$prepareOutput\s*=.*rollover-prepare.*", INSTALL_PS1)
    assert match, "rollover-prepare capture boundary is missing"
    return match.group(0)


def test_rollover_prepare_merges_child_stderr_and_stdout():
    """A Python traceback on stderr must enter the retained diagnostic."""
    line = _rollover_prepare_line()
    assert "2>&1" in line
    assert "Out-String" in line


def test_rollover_prepare_has_bounded_diagnostic_preservation_contract():
    """Nonzero child output must be bounded before fail-closed throw."""
    assert re.search(r"Get-Bounded.*Diagnostic|Bounded.*Diagnostic", INSTALL_PS1)
    assert str(MAX_DIAGNOSTIC_CHARS) in INSTALL_PS1
    failure = re.search(
        r"if\s*\(\$rolloverPrepareExit\s*-ne\s*0\).*?throw\s+([\"'][^\r\n]+[\"'])",
        INSTALL_PS1,
        flags=re.DOTALL,
    )
    assert failure, "rollover-prepare fail-closed branch is missing"
    failure_region = INSTALL_PS1[failure.start() : failure.end() + 1]
    assert "$prepareOutput" in failure_region


def test_rollover_prepare_keeps_nonzero_fail_closed_semantics():
    """Diagnostic preservation must not turn child failure into success."""
    assert "$rolloverPrepareExit = $LASTEXITCODE" in INSTALL_PS1
    assert re.search(
        r"if\s*\(\$rolloverPrepareExit\s*-ne\s*0\).*?throw",
        INSTALL_PS1,
        flags=re.DOTALL,
    )
