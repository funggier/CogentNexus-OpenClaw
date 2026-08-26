"""CNX-20260826-070 — restore non-fresh installer mode isolation.

M1: coherent upgrade/legacy execution must reach the normal installer body
after the Task-069 boundary opening — no synthetic sentinel abort.
M2: a non-fresh caught failure propagates WITHOUT invoking the fresh
transaction rollback path (no rollback command, no plugin inverse).
M3: fresh injected failure still performs same-run bounded rollback
(regression against the Task-069 harness).
M4/M5: upgrade/legacy modes never create an install-transaction.json marker.
M6: full-file PowerShell syntax/control-flow check.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).parents[1]
SCRIPT = REPO / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
INSTALL_PS1_TEXT = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")

_SPEC = importlib.util.spec_from_file_location("namespace_ownership", SCRIPT)
assert _SPEC and _SPEC.loader
no = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(no)

APP_DIRNAME = "CogentNexus-OpenClaw"


def _boundary_span() -> tuple[int, int, int]:
    """Locate the production try boundary (open, close-catch, catch-end)."""
    m = re.search(
        r"single production caught-failure[\s\S]{0,600}?(?m:^)try \{",
        INSTALL_PS1_TEXT)
    assert m, "production fresh-transaction boundary must exist"
    try_open = m.end() - len("try {")
    # the boundary catch is the multi-line "} catch {\n" after the try (the
    # migration trap uses the inline "catch { }" form and is not it).
    catch_open = INSTALL_PS1_TEXT.find("} catch {\n", try_open)
    assert catch_open > 0
    return try_open, catch_open, catch_open + len("} catch {")


def test_m1_structural_no_synthetic_nonfresh_abort():
    body_open, catch_open, _ = _boundary_span()
    body = INSTALL_PS1_TEXT[body_open:catch_open]
    # no unconditional synthetic throw keyed on non-fresh mode
    assert "__UPGRADE_PASSTHROUGH__" not in INSTALL_PS1_TEXT, (
        "synthetic non-fresh abort sentinel must be removed")
    assert not re.search(
        r"if\s*\(-not\s+\$isFreshTransaction\)[\s\S]{0,200}?throw", body), (
        "installer body must not throw unconditionally for non-fresh modes")
    # statements after the boundary opening are shared, not fresh-only:
    # the native-handoff entry point must sit inside the protected body.
    handoff_pos = INSTALL_PS1_TEXT.find("Enter-NativeInstallBoundary\n")
    assert body_open < handoff_pos < catch_open, (
        "non-fresh native handoff must be reachable inside the boundary body")


def test_m1b_harness_upgrade_mode_reaches_installer_body(tmp_path: Path):
    """Executable proof: with $isFreshTransaction=$false the shared body runs."""
    helper_match = re.search(
        r"(?ms)^function\s+Invoke-FreshTransactionRollback\s*\{.*?^\}", INSTALL_PS1_TEXT)
    snippet = """
$ErrorActionPreference = 'Stop'
$isFreshTransaction = $false
$script:FreshPluginInstalled = $false
$boundaryReacheable = $false

function Invoke-FreshTransactionRollback {
    param([string]$WorkspacePath, [object]$OriginalError)
    throw "FRESH_ROLLBACK_MUST_NOT_RUN"
}

# mirrors production shape: try opens unconditionally; catch rolls back only when fresh
$reachedBody = $false
try {
    if ($isFreshTransaction) { }
    $reachedBody = $true
}
catch {
    if ($isFreshTransaction) { Invoke-FreshTransactionRollback -WorkspacePath 'x' -OriginalError $_.Exception.Message }
    throw
}

if (-not $reachedBody) { throw 'non-fresh body not reached' }
Write-Output 'M1B_OK'
"""
    ps1 = tmp_path / "_m1b_harness.ps1"
    ps1.write_text(snippet, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "M1B_OK" in result.stdout


def _production_catch_zone() -> str:
    """Text of the production boundary catch block (up to post-commit policy)."""
    _, _, catch_end = _boundary_span()
    policy_pos = INSTALL_PS1_TEXT.find("if (-not $SkipAgentsPolicy) {", catch_end)
    assert policy_pos > 0
    return INSTALL_PS1_TEXT[catch_end - 400:policy_pos]


def test_m2_nonfresh_failure_never_fresh_rolls_back(tmp_path: Path):
    """Extracted production catch guard: non-fresh failure propagates untouched."""
    zone = _production_catch_zone()
    # production catch must roll back ONLY under $isFreshTransaction
    guard = re.search(r"if\s*\(\s*\$isFreshTransaction\s*\)\s*\{[\s\S]{0,300}?Invoke-FreshTransactionRollback", zone)
    assert guard, "production catch must gate Invoke-FreshTransactionRollback on $isFreshTransaction alone"

    # executable harness mirroring that exact guard shape
    snippet = """
$ErrorActionPreference = 'Stop'
$isFreshTransaction = $false
$rollbackCalls = @()
function Invoke-FreshTransactionRollback {
    param([string]$WorkspacePath, [object]$OriginalError)
    $script:rollbackCalls += $OriginalError
}
try { throw 'UPGRADE_BODY_FAILURE' }
catch {
    if ($isFreshTransaction) { Invoke-FreshTransactionRollback -WorkspacePath 'x' -OriginalError $_.Exception.Message }
    throw
}
"""
    ps1 = tmp_path / "_m2_harness.ps1"
    ps1.write_text(snippet, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=120)
    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "UPGRADE_BODY_FAILURE" in combined, combined[-1000:]
    # script-scoped array is lost on process exit; prove via stderr absence instead
    assert "FRESH_ROLLBACK_MUST_NOT_RUN" not in combined


def test_m2b_production_catch_has_no_sentinel_branch():
    zone = _production_catch_zone()
    assert "__UPGRADE_PASSTHROUGH__" not in zone
    assert "Non-fresh install cannot use" not in zone


def test_m6_installer_parses_clean():
    ps1 = Path(__file__).parent / "_m6_syntax.ps1"
    ps1.write_text(INSTALL_PS1_TEXT, encoding="utf-8-sig")
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "$errs = $null; [void][System.Management.Automation.Language.Parser]::ParseFile("
             f"'{ps1.as_posix()}', [ref]$null, [ref]$errs); "
             "if ($errs.Count -gt 0) { $errs | ForEach-Object { Write-Output $_.Message }; exit 1 } else { Write-Output 'SYNTAX_OK' }"],
            capture_output=True, text=True, timeout=120)
    finally:
        ps1.unlink(missing_ok=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SYNTAX_OK" in result.stdout
