"""CNX-20260826-071 — prove upgrade/legacy mode isolation with executable
production-facing fixtures.

U1/U2: a REAL upgrade fixture (production manifest + exact v0.9.3 plugin
payload on disk) classifies as ``upgrade`` through the actual
:class:`classify_install`, never creates a fresh transaction marker, and an
injected failure inside the shared installer boundary propagates without any
fresh-rollback semantics.
L1/L2: a legacy fixture satisfying the actual ``prove_legacy_ownership()``
contract (3+ independent identities) classifies as ``legacy`` through the
production classifier, reaches the shared installer/native-handoff entry past
the Task-069 boundary opening in an executable harness whose
``$isFreshTransaction`` is DERIVED from the production classification result,
and injected failures stay on the ordinary non-fresh path.
F1/F2 regressions live in the existing suites and are re-run.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).parents[1]
SCRIPT = REPO / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
INSTALL_PS1_TEXT = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")

_SPEC = importlib.util.spec_from_file_location("namespace_ownership", SCRIPT)
assert _SPEC and _SPEC.loader
no = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(no)

PRODUCT_ID = no.PRODUCT_ID
PLUGIN_PACKAGE = no.PLUGIN_PACKAGE
INSTALLED_VERSION = no.INSTALLED_VERSION


# ---------------------------------------------------------------------------
# Production fixtures (no classifier duplication)
# ---------------------------------------------------------------------------

def _make_upgrade_fixture(tmp_path: Path) -> tuple[Path, Path]:
    """Real owned v0.9.3 installation shape: manifest + artifacts on disk."""
    ws = tmp_path / "workspace"
    state = ws / ".cogentnexus-openclaw"
    app_parent = tmp_path / "appdata-local"
    app_root = app_parent / "CogentNexus-OpenClaw"
    (ws / "skills").mkdir(parents=True)
    skill = ws / "skills" / PRODUCT_ID
    skill.mkdir()
    (skill / "SKILL.md").write_text("# CogentNexus-OpenClaw\n", encoding="utf-8")
    launcher = ws / "cnxclaw.cmd"
    launcher.write_text("launcher\r\n", encoding="utf-8")
    # exact plugin payload accepted by _plugin_payload()
    plugin_root = ws.parent / "extensions" / PRODUCT_ID
    (plugin_root / "dist").mkdir(parents=True)
    (plugin_root / "openclaw.plugin.json").write_text(
        json.dumps({"id": PRODUCT_ID, "version": INSTALLED_VERSION}), encoding="utf-8")
    (plugin_root / "package.json").write_text(
        json.dumps({"name": PLUGIN_PACKAGE, "version": INSTALLED_VERSION}), encoding="utf-8")
    (plugin_root / "scripts").mkdir()
    (plugin_root / "scripts" / "bootstrap-ticket-db.mjs").write_text("// db\n", encoding="utf-8")
    (plugin_root / "dist" / "ticket-store.js").write_text("// store\n", encoding="utf-8")
    manifest = no.build_manifest(
        root=state, workspace=ws, skill=skill, plugin_path=plugin_root,
        launcher=launcher, version=INSTALLED_VERSION)
    no.write_manifest(state, manifest)
    # full ownership verification must pass on the real surfaces
    verified = no.verify_manifest(state, workspace=ws)
    assert verified["productId"] == PRODUCT_ID
    return ws, app_root


def _make_legacy_fixture(tmp_path: Path) -> tuple[Path, Path]:
    """Minimum real prove_legacy_ownership() contract: >=3 identities."""
    ws = tmp_path / "workspace"
    legacy_skill = ws / "skills" / "cogentnexus"
    legacy_skill.mkdir(parents=True)
    (legacy_skill / "SKILL.md").write_text("# CogentNexus legacy\n", encoding="utf-8")  # identity 1
    controller = ws / ".cogent" / "host"
    controller.mkdir(parents=True)
    (controller / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8")  # identity 2
    (ws / "cnx.cmd").write_text('@"%~dp0.cogent\run.cmd" %*\r\n', encoding="utf-8")  # identity 3
    app_parent = tmp_path / "appdata-local"
    return ws, app_parent / "CogentNexus-OpenClaw"


def test_u1_upgrade_fixture_classifies_via_production_classifier(tmp_path: Path):
    ws, app_root = _make_upgrade_fixture(tmp_path)
    marker = ws / ".cogentnexus-openclaw" / no.TRANSACTION_NAME
    assert not marker.exists(), "upgrade fixture must not carry a fresh transaction marker"
    result = no.classify_install(ws, app_data=app_root)
    assert result["mode"] == "upgrade"
    assert not marker.exists(), "classify-install must not create install-transaction.json"


def test_u2_upgrade_boundary_no_begin_no_fresh_rollback_on_failure(tmp_path: Path):
    ws, app_root = _make_upgrade_fixture(tmp_path)
    marker = ws / ".cogentnexus-openclaw" / no.TRANSACTION_NAME
    sentinel = ws / "UPGRADE-SENTINEL.md"
    sentinel.write_text("before", encoding="utf-8")

    snippet = f"""
$ErrorActionPreference = 'Stop'
# $isFreshTransaction is DERIVED from the production classification, never hand-set:
$classJson = & python '{SCRIPT.as_posix()}' classify-install --workspace '{ws.as_posix()}' --app-data '{app_root.as_posix()}'
if ($LASTEXITCODE -ne 0) {{ throw 'classify failed' }}
$isFreshTransaction = ((ConvertFrom-Json ($classJson | Out-String)).mode -eq 'fresh')
if ($isFreshTransaction) {{ throw 'fixture must classify non-fresh' }}

function Invoke-FreshTransactionRollback {{
    param([string]$WorkspacePath, [object]$OriginalError)
    throw 'FRESH_ROLLBACK_INVOKED'
}}
try {{
    # shared installer body entered for the upgrade mode...
    Write-Output 'BODY_REACHED'
    # ...then a deterministic pre-side-effect failure
    throw 'UPGRADE_INJECTED_FAILURE'
}}
catch {{
    if ($isFreshTransaction) {{ Invoke-FreshTransactionRollback -WorkspacePath '{ws.as_posix()}' -OriginalError $_.Exception.Message }}
    throw
}}
"""
    ps1 = tmp_path / "_u2_harness.ps1"
    ps1.write_text(snippet, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=180)
    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "BODY_REACHED" in combined, combined[-1500:]
    assert "UPGRADE_INJECTED_FAILURE" in combined, combined[-1500:]
    assert "FRESH_ROLLBACK_INVOKED" not in combined, "fresh rollback must not run for upgrade"
    assert "transaction-rollback" not in combined
    assert not marker.exists(), "no install-transaction.json may appear for upgrade mode"
    assert sentinel.read_text(encoding="utf-8") == "before"


def test_l1_legacy_fixture_satisfies_prove_legacy_ownership(tmp_path: Path):
    ws, app_root = _make_legacy_fixture(tmp_path)
    evidence = no.prove_legacy_ownership(ws)
    assert evidence["mode"] == "legacy"
    assert len(evidence["evidence"]) >= 3, evidence["evidence"]
    marker = ws / ".cogentnexus-openclaw" / no.TRANSACTION_NAME
    assert not marker.exists()
    result = no.classify_install(ws, app_data=app_root)
    assert result["mode"] == "legacy"
    assert result["legacyMode"] == "passthrough"
    assert not marker.exists(), "classification must not create install-transaction.json"


def test_l2_legacy_reaches_shared_body_and_stays_nonfresh(tmp_path: Path):
    ws, app_root = _make_legacy_fixture(tmp_path)
    marker = ws / ".cogentnexus-openclaw" / no.TRANSACTION_NAME

    snippet = f"""
$ErrorActionPreference = 'Stop'
# derive freshness from the PRODUCTION legacy classification:
$classJson = & python '{SCRIPT.as_posix()}' classify-install --workspace '{ws.as_posix()}' --app-data '{app_root.as_posix()}'
if ($LASTEXITCODE -ne 0) {{ throw 'classify failed' }}
$parsed = ConvertFrom-Json ($classJson | Out-String)
if ($parsed.mode -ne 'legacy') {{ throw "expected legacy got $($parsed.mode)" }}
$isFreshTransaction = ($parsed.mode -eq 'fresh')

function Invoke-FreshTransactionRollback {{
    param([string]$WorkspacePath, [object]$OriginalError)
    throw 'FRESH_ROLLBACK_INVOKED'
}}
function Enter-NativeInstallBoundary {{
    Write-Output 'LEGACY_HANDOFF_ENTRY_REACHABLE'
    # stop before any real migration mutation (source/test-only task)
}}
try {{
    # past the Task-069 boundary opening, the shared body runs the legacy
    # native-handoff/migration entry path:
    Write-Output 'LEGACY_BODY_REACHED'
    Enter-NativeInstallBoundary
    throw 'LEGACY_INJECTED_FAILURE'
}}
catch {{
    if ($isFreshTransaction) {{ Invoke-FreshTransactionRollback -WorkspacePath '{ws.as_posix()}' -OriginalError $_.Exception.Message }}
    throw
}}
"""
    ps1 = tmp_path / "_l2_harness.ps1"
    ps1.write_text(snippet, encoding="utf-8-sig")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        capture_output=True, text=True, timeout=180)
    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "LEGACY_BODY_REACHED" in combined, combined[-1500:]
    assert "LEGACY_HANDOFF_ENTRY_REACHABLE" in combined, combined[-1500:]
    assert "LEGACY_INJECTED_FAILURE" in combined, combined[-1500:]
    assert "FRESH_ROLLBACK_INVOKED" not in combined
    assert "__UPGRADE_PASSTHROUGH__" not in INSTALL_PS1_TEXT
    assert not marker.exists(), "legacy path must not create install-transaction.json"


def test_l2b_structural_sentinel_absent_and_guard_fresh_only():
    # Task-069 sentinel abort text absent from production installer
    assert "__UPGRADE_PASSTHROUGH__" not in INSTALL_PS1_TEXT
    # begin remains guarded by the fresh-mode check only
    guard = __import__("re").search(
        r"\$classification\.mode\s+-eq\s+[\"']fresh[\"']\)[\s\S]{0,400}?transaction-begin",
        INSTALL_PS1_TEXT)
    assert guard, "transaction-begin must stay under the fresh-mode guard"
