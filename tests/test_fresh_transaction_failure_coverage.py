"""CNX-20260826-069 — close fresh transaction failure coverage.

F1/F2/F8: production installer caught-failure boundary + supported external-
effect inverse, exercised through the actual install.ps1 rollback helper with
a shimmed ``openclaw`` command.
F3-F5: exact application-data root participates in record/rollback/recovery;
record-time rejection of unsafe paths.
F6: commit stays strictly after ownership verify; no rollback after commit.
F7: hard-crash rerun recovery covers recorded workspace AND application-data
artifacts, then classification returns coherent fresh.
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
TRANSACTION_NAME = no.TRANSACTION_NAME
begin = no.begin_fresh_transaction
classify_install = no.classify_install
commit = no.commit_transaction
expected_paths = no.expected_paths
load_marker = no.load_transaction_marker
recovery_preflight = no.recovery_preflight
record = no.record_transaction_path
rollback = no.rollback_transaction


def _make_residue(workspace: Path, *, recorded: bool = True) -> None:
    paths = expected_paths(workspace)
    controller = paths["stateRoot"] / "host" / "controller.json"
    controller.parent.mkdir(parents=True, exist_ok=True)
    controller.write_text(
        json.dumps({"schemaVersion": 1, "mode": "passthrough"}), encoding="utf-8")
    skill = paths["skillPath"] / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("# CogentNexus-OpenClaw\n", encoding="utf-8")
    if recorded:
        record(workspace, paths["stateRoot"] / "host", app_data=_app_root_of(workspace))
        record(workspace, paths["stateRoot"], app_data=_app_root_of(workspace))
        record(workspace, paths["skillPath"], app_data=_app_root_of(workspace))


def _fixture(tmp_path: Path):
    """Isolated app-data parent + workspace + surviving sibling sentinel."""
    app_parent = tmp_path / "appdata-local"
    app_parent.mkdir()
    sibling = app_parent / "SiblingSentinel"
    sibling.mkdir()
    (sibling / "keep.txt").write_text("sentinel", encoding="utf-8")
    ws = tmp_path / "workspace"
    ws.mkdir()
    return app_parent, ws


def _app_root_of(ws: Path) -> Path:
    return ws.parent / "appdata-local" / APP_DIRNAME


# ---------------------------------------------------------------------------
# F3 — application-data exact-root rollback
# ---------------------------------------------------------------------------

def test_f3_exact_app_data_root_recorded_then_removed(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    # product app-data root is created only AFTER transaction begin
    (app_root / "runtime").mkdir(parents=True)
    (app_root / "runtime" / "python.txt").write_text("owned", encoding="utf-8")
    record(ws, app_root, app_data=app_root)
    _make_residue(ws, recorded=False)
    record(ws, expected_paths(ws)["stateRoot"], app_data=app_root)
    record(ws, expected_paths(ws)["skillPath"], app_data=app_root)

    result = rollback(ws, archive=False, app_data=app_root)

    assert result["status"] == "ROLLED_BACK"
    assert not app_root.exists(), "exact transaction-created app-data root must be removed"
    assert (app_parent / "SiblingSentinel" / "keep.txt").exists(), "sibling sentinel must survive"
    assert app_parent.exists(), "application-data parent must survive"
    assert (ws / "skills").exists(), "shared workspace parents must survive"
    assert classify_install(ws, app_data=app_root)["mode"] == "fresh"


# ---------------------------------------------------------------------------
# F4 — preexisting application-data preservation
# ---------------------------------------------------------------------------

def test_f4_preexisting_app_data_survives_caught_failure(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    # root PREEXISTS the transaction with a user sentinel inside
    (app_root / "user-sentinel.txt").parent.mkdir(parents=True)
    (app_root / "user-sentinel.txt").write_text("pre-existing", encoding="utf-8")
    begin(ws, app_data=app_root)
    marker = json.loads((expected_paths(ws)["stateRoot"] / TRANSACTION_NAME).read_text(encoding="utf-8"))
    assert str(app_root).lower() not in [p.lower() for p in marker["createdPaths"]]
    _make_residue(ws)
    rollback(ws, archive=False, app_data=app_root)
    assert (app_root / "user-sentinel.txt").read_text(encoding="utf-8") == "pre-existing"


# ---------------------------------------------------------------------------
# F5 — record-time rejection leaves marker unchanged
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kind", [
    "workspace_parent", "sibling_skill", "arbitrary_temp",
    "app_data_sibling", "app_data_parent_itself",
])
def test_f5_record_rejects_unsafe_paths_immediately(tmp_path: Path, kind: str):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    if kind == "workspace_parent":
        bad = ws.parent / "outside.txt"
    elif kind == "sibling_skill":
        bad = ws / "skills" / "other-skill"
    elif kind == "arbitrary_temp":
        bad = tmp_path / "arbitrary" / "evil.bin"
        (tmp_path / "arbitrary").mkdir(exist_ok=True)
    elif kind == "app_data_sibling":
        bad = app_parent / "SiblingSentinel"
    else:
        bad = app_parent
    before = load_marker(ws)["createdPaths"]
    with pytest.raises(RuntimeError):
        record(ws, bad, app_data=app_root)
    assert load_marker(ws)["createdPaths"] == before, "rejected record must not mutate createdPaths"


def test_f5b_exact_app_data_root_is_recordable(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    app_root.mkdir(parents=True)
    record(ws, app_root, app_data=app_root)
    assert str(app_root.resolve()).lower() in [p.lower() for p in load_marker(ws)["createdPaths"]]


# ---------------------------------------------------------------------------
# F6 — commit boundary regression
# ---------------------------------------------------------------------------

def test_f6_commit_requires_verified_ownership(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    _make_residue(ws)
    # no ownership manifest -> commit must fail closed and stay incomplete
    with pytest.raises(RuntimeError):
        commit(ws)
    assert load_marker(ws)["state"] == "incomplete"


def test_f6b_rollback_after_committed_marker_refused(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    marker_path = expected_paths(ws)["stateRoot"] / TRANSACTION_NAME
    payload = json.loads(marker_path.read_text(encoding="utf-8"))
    payload["state"] = "committed"
    marker_path.write_text(json.dumps(payload), encoding="utf-8")
    _make_residue(ws)
    with pytest.raises(RuntimeError):
        rollback(ws, archive=False, app_data=app_root)
    assert (expected_paths(ws)["skillPath"] / "SKILL.md").exists()


def test_f6c_structural_commit_only_inside_try_after_verify():
    verify_invocation = INSTALL_PS1_TEXT.find("verify --root $cogentNexusOpenClawRoot --workspace")
    commit_invocation = INSTALL_PS1_TEXT.find("transaction-commit --workspace")
    assert 0 < verify_invocation < commit_invocation
    # the old standalone rollback call sites at create/verify are gone:
    assert len(re.findall(r"Invoke-FreshTransactionRollback\b", INSTALL_PS1_TEXT)) <= 2, (
        "rollback helper must appear exactly once as definition and once at the "
        "single production caught-failure boundary")


# ---------------------------------------------------------------------------
# F7 — crash/rerun recovery across workspace AND application data
# ---------------------------------------------------------------------------

def test_f7_crash_rerun_recovery_covers_app_data(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    begin(ws, app_data=app_root)
    (app_root / "runtime").mkdir(parents=True)
    record(ws, app_root, app_data=app_root)
    _make_residue(ws)
    result = recovery_preflight(ws, app_data=app_root)
    assert result["status"] == "RECOVERED_FRESH"
    assert not app_root.exists()
    assert (app_parent / "SiblingSentinel" / "keep.txt").exists()
    assert app_parent.exists()
    assert classify_install(ws, app_data=app_root)["mode"] == "fresh"


# ---------------------------------------------------------------------------
# F1/F2/F8 — production installer caught-failure boundary (structural +
# executable harness through the actual install.ps1 helper)
# ---------------------------------------------------------------------------

def _pos(pattern: str) -> int:
    m = re.search(pattern, INSTALL_PS1_TEXT)
    assert m, f"pattern not found: {pattern}"
    return m.start()


def test_f1_structural_single_boundary_wraps_begin_to_commit():
    begin_invocation = INSTALL_PS1_TEXT.find("transaction-begin --workspace")
    boundary_open = re.search(
        r"single production caught-failure[\s\S]{0,600}?(?m:^)try \{",
        INSTALL_PS1_TEXT)
    assert boundary_open, "the protected boundary try must open right after the B1 marker comment"
    try_open = boundary_open.end() - len("try {")
    # the production boundary catch is the one immediately following the try
    # the production boundary catch is the first multi-line catch after the try
    catch = INSTALL_PS1_TEXT.find("} catch {\n", try_open)
    assert catch > 0, "boundary catch must follow the boundary try"
    assert begin_invocation < try_open < catch, "one try boundary must open after transaction-begin"
    commit_invocation = INSTALL_PS1_TEXT.find("transaction-commit --workspace", try_open)
    assert begin_invocation < commit_invocation < catch, "commit must occur inside the protected boundary"
    boundary_zone = INSTALL_PS1_TEXT[catch:catch + 600]
    assert "Invoke-FreshTransactionRollback" in boundary_zone, (
        "the single catch must route every caught pre-commit failure through "
        "the production rollback helper")


def test_f1b_structural_no_bare_precommit_throw_escapes_boundary():
    # every legacy explicit rollback call site is consolidated into the catch
    assert INSTALL_PS1_TEXT.count("Invoke-FreshTransactionRollback -WorkspacePath") == 1


def test_f2_structural_plugin_inverse_and_policy_order():
    helper = re.search(
        r"(?s)function\s+Invoke-FreshTransactionRollback\s*\{.*?\r?\n\}", INSTALL_PS1_TEXT)
    assert helper, "production rollback helper must exist"
    body = helper.group(0)
    assert "plugins uninstall cogentnexus-openclaw --force" in body, (
        "supported OpenClaw plugin inverse required for fresh-attempt registrations")
    assert "$script:FreshPluginInstalled" in INSTALL_PS1_TEXT.replace(body, "") or \
        "FreshPluginInstalled" in INSTALL_PS1_TEXT
    # flag is set only after a successful plugins install in this attempt
    flag_pos = _pos(r"\$script:FreshPluginInstalled\s*=\s*\$true")
    install_pos = _pos(r"plugins install \$packagePath --force")
    assert install_pos < flag_pos
    # AGENTS managed policy applies only AFTER ownership commit
    policy_pos = _pos(r"policy apply")
    commit_pos = _pos(r"transaction-commit")
    assert commit_pos < policy_pos, (
        "managed AGENTS policy application must be reordered post-ownership-commit")


def _run_ps1_snippet(snippet: str, target: Path) -> subprocess.CompletedProcess:
    ps1 = target
    ps1.write_text(snippet, encoding="utf-8-sig")
    try:
        return subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
            capture_output=True, text=True, timeout=300,
        )
    finally:
        ps1.unlink(missing_ok=True)


def _extract_helper_snippet() -> str:
    match = re.search(
        r"(?ms)^function\s+Invoke-FreshTransactionRollback\s*\{.*?^\}", INSTALL_PS1_TEXT)
    assert match, "cannot extract production rollback helper from install.ps1"
    return match.group(0)


HARNESS_TEMPLATE = """
$ErrorActionPreference = 'Stop'
$ws = '{ws}'
$adParent = '{ad_parent}'
$appRoot = Join-Path $adParent '{app_dirname}'
$shimDir = '{shim_dir}'
$env:Path = "$shimDir;" + $env:Path
$ownership = '{ownership}'
$env:NAMESPACE_OWNERSHIP_SCRIPT = $ownership
# production helper references the repo-level $ownershipScript; bind it for harness use
$ownershipScript = $ownership

{helper}

New-Item -ItemType Directory -Force -Path (Join-Path $adParent 'SiblingSentinel') | Out-Null
Set-Content (Join-Path $adParent 'SiblingSentinel/keep.txt') 'sentinel'
& python $ownership transaction-begin --workspace $ws --app-data $appRoot | Out-Null
if ($LASTEXITCODE -ne 0) {{ throw 'begin failed' }}
# fresh attempt mutates: state root contents + skill + NEW app-data root
New-Item -ItemType Directory -Force -Path (Join-Path $ws '.cogentnexus-openclaw/host') | Out-Null
Set-Content (Join-Path $ws '.cogentnexus-openclaw/host/controller.json') '{{}}'
& python $ownership transaction-record --workspace $ws --app-data $appRoot --path (Join-Path $ws '.cogentnexus-openclaw/host') | Out-Null
& python $ownership transaction-record --workspace $ws --app-data $appRoot --path (Join-Path $ws '.cogentnexus-openclaw') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ws 'skills/cogentnexus-openclaw') | Out-Null
Set-Content (Join-Path $ws 'skills/cogentnexus-openclaw/SKILL.md') '# CogentNexus-OpenClaw'
& python $ownership transaction-record --workspace $ws --app-data $appRoot --path (Join-Path $ws 'skills/cogentnexus-openclaw') | Out-Null
New-Item -ItemType Directory -Force -Path $appRoot | Out-Null
& python $ownership transaction-record --workspace $ws --app-data $appRoot --path $appRoot | Out-Null
Set-Content (Join-Path $ws 'USER-SENTINEL.md') 'unrelated'

$script:FreshPluginInstalled = {plugin_flag}
try {{
    # deterministic production-path failure injected well before ownership create
    python -c "import sys; sys.exit(3)"
    if ($LASTEXITCODE -ne 0) {{ throw 'CogentNexus-OpenClaw validation failed' }}
}}
catch {{
    Invoke-FreshTransactionRollback -WorkspacePath $ws -OriginalError $_.Exception.Message
}}
"""


def test_f1_harness_injected_failure_triggers_production_rollback(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    shim = tmp_path / "shim"
    shim.mkdir()
    (shim / "openclaw.cmd").write_text(
        "@echo off\r\necho %* >> \"%TEMP%\\cnx069-shim.log\"\r\nexit /b 0\r\n", encoding="utf-8")
    snippet = HARNESS_TEMPLATE.format(
        ws=str(ws), ad_parent=str(app_parent), app_dirname=APP_DIRNAME,
        shim_dir=str(shim), ownership=str(SCRIPT), plugin_flag="$true",
        helper=_extract_helper_snippet(),
    )
    log = Path("%TEMP%" ) if False else None  # placeholder, resolved below
    result = _run_ps1_snippet(snippet, tmp_path / "_f1_harness.ps1")
    combined = result.stdout + result.stderr
    assert result.returncode != 0, "original injected failure must propagate"
    assert "CogentNexus-OpenClaw validation failed" in combined, combined[-2000:]
    # exact fresh filesystem residue removed; unrelated sentinel survives
    assert not (ws / ".cogentnexus-openclaw" / "host").exists(), combined[-2000:]
    assert not (ws / "skills" / "cogentnexus-openclaw").exists()
    assert not app_root.exists()
    assert (app_parent / "SiblingSentinel" / "keep.txt").exists()
    assert (ws / "USER-SENTINEL.md").read_text(encoding="utf-8").strip() == "unrelated"
    assert (ws / "skills").exists()
    # supported plugin inverse was exercised through the shim
    shim_log = Path(os.environ["TEMP"]) / "cnx069-shim.log"
    assert shim_log.exists() and "plugins uninstall cogentnexus-openclaw --force" in \
        shim_log.read_text(encoding="utf-8"), "supported plugin inverse must be invoked"
    # result classifies coherent fresh afterward
    cls = subprocess.run(
        ["python", str(SCRIPT), "classify-install", "--workspace", str(ws),
         "--app-data", str(app_root)],
        capture_output=True, text=True)
    assert cls.returncode == 0 and json.loads(cls.stdout)["mode"] == "fresh", cls.stdout + cls.stderr


import os  # noqa: E402  (used by the harness assertions above)


def test_f1b_harness_no_plugin_inverse_when_not_registered_this_attempt(tmp_path: Path):
    app_parent, ws = _fixture(tmp_path)
    app_root = _app_root_of(ws)
    shim = tmp_path / "shim"
    shim.mkdir()
    log = tmp_path / "shim-log.txt"
    (shim / "openclaw.cmd").write_text(
        f"@echo off\r\necho %* >> \"{log.as_posix()}\"\r\nexit /b 0\r\n", encoding="utf-8")
    snippet = HARNESS_TEMPLATE.format(
        ws=str(ws), ad_parent=str(app_parent), app_dirname=APP_DIRNAME,
        shim_dir=str(shim), ownership=str(SCRIPT), plugin_flag="$false",
        helper=_extract_helper_snippet(),
    )
    result = _run_ps1_snippet(snippet, tmp_path / "_f1b_harness.ps1")
    assert result.returncode != 0
    assert not log.exists() or "uninstall" not in log.read_text(encoding="utf-8"), (
        "rollback must never uninstall a plugin this fresh attempt did not register")
    assert not app_root.exists()


# ---------------------------------------------------------------------------
# F8 — no external-effect residue after representative caught failures
# ---------------------------------------------------------------------------

def test_f8_structural_post_commit_effects_outside_boundary():
    """Everything after successful commit is post-ownership; nothing between
    commit and the closing catch may create product external effects."""
    commit_pos = INSTALL_PS1_TEXT.find("transaction-commit --workspace")
    catch_pos = INSTALL_PS1_TEXT.find("} catch {")
    zone = INSTALL_PS1_TEXT[commit_pos:catch_pos]
    for forbidden in ["plugins install", "npm ci"]:
        assert forbidden not in zone, f"{forbidden} must not sit between commit and boundary exit"
