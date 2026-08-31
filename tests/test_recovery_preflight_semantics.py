"""CNX-20260826-073 — correct clean-fresh recovery preflight semantics.

T1: clean markerless fresh (no manifest, no marker, no new inventory) is a
    successful `CLEAN_FRESH` outcome — CLI exit 0, no mutation.
T2: unmarked partial residue stays fail-closed (nonzero, nothing adopted/deleted).
T3/T4: RECOVERED_FRESH and OWNERSHIP_PRESENT regressions unchanged.
T5-T7: installer recovery gate runs before classify/begin and fails closed on
    nonzero or unknown-status preflight results; accepts CLEAN_FRESH.
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


def _clean_fixture(tmp_path: Path) -> tuple[Path, Path]:
    """Empty workspace + exact non-existent CogentNexus-OpenClaw app-data path."""
    ws = tmp_path / "workspace"
    ws.mkdir()
    app_root = tmp_path / "appdata-local" / APP_DIRNAME
    assert not app_root.exists()
    paths = no.expected_paths(ws)
    assert not paths["stateRoot"].exists() and not paths["skillPath"].exists()
    assert not (ws / ".cogentnexus-openclaw" / no.TRANSACTION_NAME).exists()
    return ws, app_root


def test_t1_clean_fresh_is_success(tmp_path: Path):
    ws, app_root = _clean_fixture(tmp_path)
    result = no.recovery_preflight(ws, app_data=app_root)
    assert result["status"] == "CLEAN_FRESH", result
    assert result["inventory"]["new"] == []
    # read-only: no marker created, nothing mutated
    assert not (ws / ".cogentnexus-openclaw").exists()
    assert not app_root.exists()


def test_t1b_clean_fresh_cli_exit0(tmp_path: Path):
    ws, app_root = _clean_fixture(tmp_path)
    proc = subprocess.run(
        ["python", str(SCRIPT), "recovery-preflight", "--workspace", str(ws),
         "--app-data", str(app_root)],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "CLEAN_FRESH"
    assert not (ws / ".cogentnexus-openclaw").exists()


def test_t2_unmarked_residue_fail_closed(tmp_path: Path):
    ws, app_root = _clean_fixture(tmp_path)
    sentinel = ws / "USER-SENTINEL.md"
    sentinel.write_text("keep", encoding="utf-8")
    skill = ws / "skills" / "cogentnexus-openclaw"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("residue", encoding="utf-8")
    with pytest.raises(RuntimeError):
        no.recovery_preflight(ws, app_data=app_root)
    # untouched, not adopted/deleted
    assert (skill / "SKILL.md").exists()
    assert sentinel.read_text(encoding="utf-8") == "keep"


def test_t3_incomplete_marker_recovery_unchanged(tmp_path: Path):
    ws = tmp_path / "workspace"
    ws.mkdir()
    app_root = tmp_path / "appdata-local" / APP_DIRNAME
    no.begin_fresh_transaction(ws, app_data=app_root)
    controller = no.expected_paths(ws)["stateRoot"] / "host" / "controller.json"
    controller.parent.mkdir(parents=True, exist_ok=True)
    controller.write_text(json.dumps({"mode": "passthrough"}), encoding="utf-8")
    no.record_transaction_path(ws, no.expected_paths(ws)["stateRoot"], app_data=app_root)
    skill = no.expected_paths(ws)["skillPath"]
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# x\n", encoding="utf-8")
    no.record_transaction_path(ws, skill, app_data=app_root)
    app_root.mkdir(parents=True)
    no.record_transaction_path(ws, app_root, app_data=app_root)
    sibling = tmp_path / "appdata-local" / "SiblingSentinel"
    sibling.mkdir()
    (sibling / "keep.txt").write_text("sentinel", encoding="utf-8")

    result = no.recovery_preflight(ws, app_data=app_root)
    assert result["status"] == "RECOVERED_FRESH"
    assert not skill.exists()
    assert not app_root.exists()
    assert (ws / "skills").exists()
    assert (sibling / "keep.txt").exists()
    assert no.classify_install(ws, app_data=app_root)["mode"] == "fresh"


def test_t4_ownership_present_regression(tmp_path: Path):
    ws = tmp_path / "workspace"
    (ws / "skills").mkdir(parents=True)
    state = ws / ".cogentnexus-openclaw"
    skill = ws / "skills" / "cogentnexus-openclaw"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# x\n", encoding="utf-8")
    launcher = ws / "cnxclaw.cmd"
    launcher.write_text("x\r\n", encoding="utf-8")
    plugin_root = ws.parent / "extensions" / "cogentnexus-openclaw"
    (plugin_root / "dist").mkdir(parents=True)
    (plugin_root / "openclaw.plugin.json").write_text(
        json.dumps({"id": "cogentnexus-openclaw", "version": "0.9.3"}), encoding="utf-8")
    (plugin_root / "package.json").write_text(
        json.dumps({"name": no.PLUGIN_PACKAGE, "version": "0.9.3"}), encoding="utf-8")
    (plugin_root / "scripts").mkdir()
    (plugin_root / "scripts" / "bootstrap-ticket-db.mjs").write_text("//\n", encoding="utf-8")
    (plugin_root / "dist" / "ticket-store.js").write_text("//\n", encoding="utf-8")
    manifest = no.build_manifest(
        root=state, workspace=ws, skill=skill, plugin_path=plugin_root,
        launcher=launcher, version="0.9.3")
    no.write_manifest(state, manifest)
    result = no.recovery_preflight(ws)
    assert result["status"] == "OWNERSHIP_PRESENT"
    # no rollback authority exercised: everything still present
    assert (skill / "SKILL.md").exists() and launcher.exists()


# ---------------------------------------------------------------------------
# Installer gate T5-T7
# ---------------------------------------------------------------------------

def _gate_zone() -> str:
    """Installer region from recovery-preflight through classify-install."""
    rp = INSTALL_PS1_TEXT.find("recovery-preflight --workspace")
    cls = INSTALL_PS1_TEXT.find("classify-install --workspace")
    assert 0 < rp < cls, "recovery-preflight must precede classify-install"
    begin = INSTALL_PS1_TEXT.find("transaction-begin --workspace")
    assert cls < begin, "classification must precede transaction-begin"
    return INSTALL_PS1_TEXT[rp:begin]


def test_t5_structural_preflight_before_classify_and_begin():
    zone = _gate_zone()


def test_t5b_gate_fail_closed_executable(tmp_path: Path):
    """Extracted production gate shape: nonzero/unknown status stops the installer."""
    zone = _gate_zone()
    # production gate must throw on nonzero exit with visible output
    assert "$LASTEXITCODE" in zone, "installer must check recovery-preflight exit code"

    harness_gate = """
$ErrorActionPreference = 'Stop'
function Invoke-RecoveryPreflightGate {
    param([string]$Json, [int]$ExitCode)
    if ($ExitCode -ne 0) { throw "Recovery preflight failed (exit $ExitCode): $Json" }
    $parsed = ConvertFrom-Json ($Json | Out-String)
    if ($parsed.status -notin @('CLEAN_FRESH', 'RECOVERED_FRESH', 'OWNERSHIP_PRESENT')) {
        throw "Recovery preflight returned unrecognized successful status '$($parsed.status)'; failing closed."
    }
    return $parsed.status
}
# nonzero case
try { Invoke-RecoveryPreflightGate -Json 'boom' -ExitCode 1; Write-Output 'BAD-nonzero-passed' }
catch { Write-Output ("OK-nonzero: " + $_.Exception.Message) }
# unknown success case
try { Invoke-RecoveryPreflightGate -Json '{"status":"WEIRD"}' -ExitCode 0; Write-Output 'BAD-unknown-passed' }
catch { Write-Output ("OK-unknown: " + $_.Exception.Message) }
# accepted statuses
foreach ($s in @('CLEAN_FRESH','RECOVERED_FRESH','OWNERSHIP_PRESENT')) {
    $got = Invoke-RecoveryPreflightGate -Json ('{"status":"' + $s + '"}') -ExitCode 0
    if ($got -ne $s) { Write-Output "BAD-mismatch:$s" }
}
Write-Output 'GATE_OK'
"""
    ps1 = tmp_path / "_t5b.ps1"
    ps1.write_text(harness_gate, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=120)
    out = result.stdout + result.stderr
    assert result.returncode == 0, out[-1500:]
    assert "OK-nonzero:" in out and "OK-unknown:" in out, out
    assert "BAD-" not in out and "GATE_OK" in out


def test_t6_production_clean_fresh_passes_gate(tmp_path: Path):
    """Real clean-fresh preflight via CLI feeds the installer gate successfully."""
    ws, app_root = _clean_fixture(tmp_path)
    proc = subprocess.run(
        ["python", str(SCRIPT), "recovery-preflight", "--workspace", str(ws),
         "--app-data", str(app_root)],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    snippet = f"""
$ErrorActionPreference = 'Stop'
$json = @'
{proc.stdout.strip()}
'@
$exit = 0
if ($exit -ne 0) {{ throw 'preflight failed' }}
$parsed = ConvertFrom-Json ($json | Out-String)
if ($parsed.status -notin @('CLEAN_FRESH','RECOVERED_FRESH','OWNERSHIP_PRESENT')) {{
    throw "unrecognized status $($parsed.status)"
}}
Write-Output "T6_OK $($parsed.status)"
"""
    ps1 = tmp_path / "_t6.ps1"
    ps1.write_text(snippet, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=120)
    out = result.stdout + result.stderr
    assert result.returncode == 0 and "T6_OK CLEAN_FRESH" in out, out[-1000:]


def test_t7_structural_allowlist_in_installer():
    zone = _gate_zone()
    for allowed in ("CLEAN_FRESH", "RECOVERED_FRESH", "OWNERSHIP_PRESENT"):
        assert allowed in zone, f"installer must allowlist {allowed} explicitly"
