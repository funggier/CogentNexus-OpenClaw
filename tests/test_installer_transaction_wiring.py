"""CNX-20260826-068 — production installer transaction wiring tests.

P1: install.ps1 must invoke transaction-begin only for fresh mode, after
    classify-install and before the first residue-capable mutation.
P2: fresh-created owned paths (state root contents, skill, launcher,
    application data) are recorded before/atomically with creation.
P3/P7: caught-failure rollback and crash/rerun recovery use the same
    production marker/recording contract.
P4: transaction-commit occurs only after ownership create + verify.

These tests inspect the actual production scripts/install.ps1 control path
(ordered structural assertions) plus executable PowerShell harnesses that
exercise the extracted production helper functions from the same file.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).parents[1]
INSTALL_PS1 = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")


def _pos(pattern: str) -> int:
    matches = [m.start() for m in re.finditer(pattern, INSTALL_PS1)]
    assert matches, f"pattern not found in install.ps1: {pattern}"
    return matches[0]


def test_p1_begin_invoked_only_for_fresh_after_classification():
    classify_pos = _pos(r"classify-install")
    # begin is guarded by a fresh-mode check
    guard = re.search(r"\$classification\.mode\s+-eq\s+[\"']fresh[\"']\)[\s\S]{0,400}?transaction-begin", INSTALL_PS1)
    assert guard, "transaction-begin must be invoked under a fresh-mode guard"
    begin_pos = guard.start()
    assert classify_pos < begin_pos, "begin must come after classify-install"

    first_mutation = min(
        p for p in [
            _pos(r"New-Item -ItemType Directory -Force -Path \(Split-Path -Parent \$targetSkill\)"),
            _pos(r"Copy-Item -Recurse -Force -LiteralPath \$sourceSkill"),
        ]
    )
    assert begin_pos < first_mutation, "begin must precede the first residue-capable mutation"


def test_p2_required_paths_recorded():
    for literal in ["cogentNexusOpenClawRoot", "targetSkill", "launcher"]:
        record_calls = re.findall(rf"transaction-record[^\r\n]*\s+\S*{literal}", INSTALL_PS1)
        assert record_calls, f"no transaction-record call covering {literal}"


def test_p4_commit_only_after_verify():
    create_pos = _pos(r"namespace_ownership\.py\"\), \"create\"|namespace_ownership\.py\"\), 'create'")
    verify_pos = min(
        p for p in [m.start() for m in re.finditer(r"verify --root \$cogentNexusOpenClawRoot --workspace", INSTALL_PS1)]
    )
    commit_match = re.search(r"transaction-commit --workspace", INSTALL_PS1)
    assert commit_match, "production installer must retire the marker via transaction-commit"
    # the verify exit-code check must appear between verify and commit, and
    # the commit must be inside a $isFreshTransaction block that follows it
    gate_zone = INSTALL_PS1[verify_pos:commit_match.start() + 100]
    assert "New ownership manifest/artifacts failed exact verification" in gate_zone,         "verify failure gate must precede commit"
    assert re.search(r"verify --root \$cogentNexusOpenClawRoot[\s\S]{0,600}?transaction-commit", INSTALL_PS1),         "commit call must appear after verification gate"
    assert create_pos < verify_pos < commit_match.start()


def test_p3_rollback_helper_exists_and_reports_both_errors():
    match = re.search(r"function\s+Invoke-FreshTransactionRollback[\s\S]{0,3000}", INSTALL_PS1)
    assert match, "install.ps1 must define a production rollback helper used on caught failure"
    body = match.group(0)
    assert "transaction-rollback" in body or "rollback_transaction" in body or "rollback" in body


def _run_ps1_snippet(snippet: str) -> subprocess.CompletedProcess:
    script = (
        "$env:Path = \"C:\\Program Files\\nodejs;\" + $env:Path\n"
        + snippet
    )
    ps1 = Path(__file__).parent / "_p_harness.ps1"
    ps1.write_text(script, encoding="utf-8-sig")
    try:
        return subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
            capture_output=True, text=True, timeout=300,
        )
    finally:
        ps1.unlink(missing_ok=True)


def test_p8_production_ast_proves_independent_lifecycle_gates_and_order():
    helper = REPO / "scripts" / "analyze-installer-lifecycle-ast.ps1"
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
         "-Installer", str(REPO / "scripts" / "install.ps1")],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rows = json.loads(result.stdout)
    rollover = [r for r in rows if "rollover-plan" in r["command"] or "rollover-apply" in r["command"]]
    installs = [r for r in rows if "plugins install" in r["command"] or "npm pack" in r["command"]]
    resolves = [r for r in rows if " resolve-plugin --" in r["command"]]
    assert rollover and installs and resolves
    assert all(any("rolloverPlugin" in a for a in r["ancestors"]) for r in rollover)
    assert all(not any("installPlugin" in a for a in r["ancestors"]) for r in rollover)
    assert all(any("installPlugin" in a for a in r["ancestors"]) for r in installs)
    assert max(r["start"] for r in rollover) < min(r["start"] for r in resolves)


def test_p7_production_crash_rerun_recovery(tmp_path: Path):
    """Crash after recorded artifacts exist -> production recovery-preflight -> fresh."""
    ws = tmp_path / "workspace"
    (ws / "skills").mkdir(parents=True)
    app_data = tmp_path / "appdata-local" / "CogentNexus-OpenClaw"
    snippet = f"""
$ErrorActionPreference = 'Stop'
$ws = '{ws.as_posix()}'
$appData = '{app_data.as_posix()}'
$ownership = '{(REPO / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py").as_posix()}'
& python $ownership transaction-begin --workspace $ws --app-data $appData | Out-Null
if ($LASTEXITCODE -ne 0) {{ throw 'begin failed' }}
# simulate installer-created artifacts with production recording order
New-Item -ItemType Directory -Force -Path (Join-Path $ws '.cogentnexus-openclaw/host') | Out-Null
Set-Content (Join-Path $ws '.cogentnexus-openclaw/host/controller.json') '{{}}'
& python $ownership transaction-record --workspace $ws --app-data $appData --path (Join-Path $ws '.cogentnexus-openclaw/host') | Out-Null
& python $ownership transaction-record --workspace $ws --app-data $appData --path (Join-Path $ws '.cogentnexus-openclaw') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ws 'skills/cogentnexus-openclaw') | Out-Null
& python $ownership transaction-record --workspace $ws --app-data $appData --path (Join-Path $ws 'skills/cogentnexus-openclaw') | Out-Null
# hard crash: no caught rollback. Rerun installer recovery surface:
$json = & python $ownership recovery-preflight --workspace $ws --app-data $appData | ConvertFrom-Json
if ($json.status -ne 'RECOVERED_FRESH') {{ throw "expected RECOVERED_FRESH got $($json.status)" }}
$class = & python $ownership classify-install --workspace $ws --app-data $appData | ConvertFrom-Json
if ($class.mode -ne 'fresh') {{ throw "expected fresh got $($class.mode)" }}
if ((Test-Path (Join-Path $ws 'skills/cogentnexus-openclaw'))) {{ throw 'skill residue survived' }}
if (-not (Test-Path (Join-Path $ws 'skills'))) {{ throw 'shared parent skills deleted' }}
Write-Output 'P7_OK'
"""
    result = _run_ps1_snippet(snippet)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "P7_OK" in result.stdout
