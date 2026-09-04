"""CNX-20260904-239 — bounded rollover-prepare diagnostics.

These tests intentionally describe the missing owning-boundary behavior before
production repair. They must fail on the accepted predecessor source because
the child stderr is not merged and the captured output is not bounded/preserved
on the fail-closed path.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).parents[1]
INSTALL_PS1 = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")
MAX_DIAGNOSTIC_CHARS = 4096


def _rollover_prepare_line() -> str:
    match = re.search(r"Invoke-NativeInstallerDiagnostic[\s\S]{0,900}?rollover-prepare", INSTALL_PS1)
    assert match, "rollover-prepare capture boundary is missing"
    return match.group(0)


def test_rollover_prepare_merges_child_stderr_and_stdout():
    """A Python traceback on stderr must enter the retained diagnostic."""
    line = _rollover_prepare_line()
    assert "2>&1" in INSTALL_PS1
    assert "Out-String" in INSTALL_PS1
    assert "Invoke-NativeInstallerDiagnostic" in line


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


def _powershell_executable() -> str | None:
    candidates = ("powershell.exe", "pwsh") if os.name == "nt" else ("pwsh", "powershell")
    return next((shutil.which(candidate) for candidate in candidates if shutil.which(candidate)), None)


def test_bounded_diagnostic_helper_behavior_is_real_and_deterministic():
    """Execute the owning PowerShell helper against empty/short/long output."""
    import pytest

    powershell = _powershell_executable()
    if powershell is None:
        pytest.skip("no PowerShell runtime available for helper execution")
    match = re.search(
        r"function Get-BoundedInstallerDiagnostic\s*\{.*?\n\}",
        INSTALL_PS1,
        flags=re.DOTALL,
    )
    assert match, "bounded diagnostic helper is missing"
    script = """$ErrorActionPreference = 'Stop'
%s
$long = ('H' * 3000) + ('T' * 1000) + 'PYTHON-TRACEBACK-MARKER' + ('T' * 2000)
@(
  [ordered]@{name='empty'; value=(Get-BoundedInstallerDiagnostic -Output '')},
  [ordered]@{name='short'; value=(Get-BoundedInstallerDiagnostic -Output '  child stderr marker  ')},
  [ordered]@{name='long'; value=(Get-BoundedInstallerDiagnostic -Output $long)}
) | ConvertTo-Json -Compress
""" % match.group(0)
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", encoding="utf-8", delete=False) as handle:
        handle.write(script)
        script_path = handle.name
    try:
        result = subprocess.run(
            [powershell, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        Path(script_path).unlink(missing_ok=True)
    rows = result.stdout.strip()
    import json
    values = {row["name"]: row["value"] for row in json.loads(rows)}
    assert values["empty"] == "[no child diagnostic output captured]"
    assert values["short"] == "child stderr marker"
    assert len(values["long"]) == MAX_DIAGNOSTIC_CHARS
    assert values["long"].startswith("H")
    assert values["long"].endswith("T")
    assert "PYTHON-TRACEBACK-MARKER" in values["long"]
    assert "[child diagnostic truncated]" in values["long"]


def test_rollover_prepare_keeps_nonzero_fail_closed_semantics():
    """Diagnostic preservation must not turn child failure into success."""
    assert "$rolloverPrepareExit = [int]$prepareCapture.ExitCode" in INSTALL_PS1
    assert re.search(
        r"if\s*\(\$rolloverPrepareExit\s*-ne\s*0\).*?throw",
        INSTALL_PS1,
        flags=re.DOTALL,
    )
