"""CNX-20260825-067 D2 tests — fresh-install transaction/recovery contract.

Exercises the production surfaces in namespace_ownership.py:
- begin_fresh_transaction / load_transaction_marker / recovery_preflight /
  commit_transaction / rollback_transaction
- classify_install() integration with incomplete transaction markers.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
_SPEC = importlib.util.spec_from_file_location("namespace_ownership", SCRIPT)
assert _SPEC and _SPEC.loader
namespace_ownership = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(namespace_ownership)

TRANSACTION_NAME = namespace_ownership.TRANSACTION_NAME
begin_fresh_transaction = namespace_ownership.begin_fresh_transaction
classify_install = namespace_ownership.classify_install
commit_transaction = namespace_ownership.commit_transaction
expected_paths = namespace_ownership.expected_paths
load_transaction_marker = namespace_ownership.load_transaction_marker
recovery_preflight = namespace_ownership.recovery_preflight
rollback_transaction = namespace_ownership.rollback_transaction


def _make_residue(workspace: Path, *, recorded: bool = True, app_data: Path | None = None) -> None:
    """Recreate the exact Task-066 partial residue shape.

    Mirrors the production installer: each residue-capable creation is
    recorded in the active transaction marker via record_transaction_path.
    CNX-20260826-074 I2: the caller-supplied isolated application-data root
    flows through all production inventory/transaction surfaces so tests are
    independent of the live machine's installed product.
    """
    record_transaction_path = namespace_ownership.record_transaction_path
    paths = expected_paths(workspace)
    controller = paths["stateRoot"] / "host" / "controller.json"
    controller.parent.mkdir(parents=True, exist_ok=True)
    controller.write_text(json.dumps({"schemaVersion": 1, "mode": "passthrough"}), encoding="utf-8")
    skill = paths["skillPath"] / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("# CogentNexus-OpenClaw\n", encoding="utf-8")
    if recorded:
        kw = {"app_data": app_data} if app_data is not None else {}
        record_transaction_path(workspace, paths["stateRoot"] / "host", **kw)
        record_transaction_path(workspace, paths["stateRoot"], **kw)
        record_transaction_path(workspace, paths["skillPath"], **kw)


def _isolated_app_root(tmp_path: Path) -> Path:
    """Exact isolated application-data product root for a temp workspace."""
    return tmp_path / "appdata-local" / "CogentNexus-OpenClaw"


# R1 — fresh transaction begins before residue-capable mutation
def test_r1_transaction_begin_writes_marker(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    handle = begin_fresh_transaction(workspace)
    marker_path = workspace / ".cogentnexus-openclaw" / TRANSACTION_NAME
    assert marker_path.is_file(), "marker must exist inside CNX-owned state root before mutation"
    payload = json.loads(marker_path.read_text(encoding="utf-8"))
    assert payload["schemaVersion"] == 1
    assert payload["productId"] == "cogentnexus-openclaw"
    assert payload["state"] in {"incomplete", "committed"}
    assert payload["workspace"].lower() == str(workspace.resolve()).lower()
    assert isinstance(payload["createdPaths"], list)
    # marker is distinguishable from ownership.json and does not claim ownership
    assert not (workspace / ".cogentnexus-openclaw" / "ownership.json").exists()
    assert set(payload) >= {
        "schemaVersion", "transactionId", "productId", "workspace", "stateRoot",
        "skillPath", "applicationData", "state", "createdAt", "createdPaths",
    }


# R1b — marker exists BEFORE inventory becomes non-empty (ordering proof)
def test_r1b_marker_written_before_artifact_creation(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    app_data = _isolated_app_root(tmp_path)
    assert classify_install(workspace, app_data=app_data)["mode"] == "fresh"
    handle = begin_fresh_transaction(workspace, app_data=app_data)
    # simulate the first residue-capable mutation AFTER the marker exists
    _make_residue(workspace, app_data=app_data)
    ci = namespace_ownership.current_inventory
    assert ci(workspace, app_data=app_data)["new"], "residue shape must make new inventory non-empty"
    assert load_transaction_marker(workspace) is not None


# R2 — simulated failure after creation is recoverable via production preflight
def test_r2_incomplete_transaction_recovery_restores_fresh(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    app_data = _isolated_app_root(tmp_path)
    begin_fresh_transaction(workspace, app_data=app_data)
    _make_residue(workspace, app_data=app_data)
    # no ownership.json -> classify dead-ends on the manifest check
    with pytest.raises(RuntimeError):
        classify_install(workspace, app_data=app_data)
    result = recovery_preflight(workspace, app_data=app_data)
    assert result["status"] == "RECOVERED_FRESH"
    assert classify_install(workspace, app_data=app_data)["mode"] == "fresh"
    assert not (workspace / ".cogentnexus-openclaw" / "host" / "controller.json").exists()
    assert not (workspace / "skills" / "cogentnexus-openclaw").exists()


# R3 — normal caught failure rolls back created paths only
def test_r3_rollback_removes_only_created_paths(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    app_data = _isolated_app_root(tmp_path)
    unrelated = workspace / "USER.md"
    unrelated.write_text("unrelated", encoding="utf-8")
    begin_fresh_transaction(workspace, app_data=app_data)
    _make_residue(workspace, app_data=app_data)

    def inv():
        return namespace_ownership.current_inventory(workspace, app_data=app_data)

    result_rb = rollback_transaction(workspace, archive=False, app_data=app_data)
    assert inv()["new"] == [], f"inventory after rollback: {inv()} rb={result_rb}"
    assert classify_install(workspace, app_data=app_data)["mode"] == "fresh"
    assert unrelated.read_text(encoding="utf-8") == "unrelated"


# R4 — successful commit: marker no longer authorizes cleanup
def test_r4_committed_marker_does_not_authorize_cleanup(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    begin_fresh_transaction(workspace)
    _make_residue(workspace)
    # simulate the production end state: full ownership exists and the
    # installer retired the marker to "committed" after verify_manifest passed
    marker_path = workspace / ".cogentnexus-openclaw" / TRANSACTION_NAME
    payload = json.loads(marker_path.read_text(encoding="utf-8"))
    payload["state"] = "committed"
    payload["createdPaths"] = []
    marker_path.write_text(json.dumps(payload), encoding="utf-8")
    # without ownership.json a committed marker is ambiguous: fail-closed,
    # never rollback, never adopt
    with pytest.raises(RuntimeError):
        recovery_preflight(workspace)
    assert (workspace / "skills" / "cogentnexus-openclaw" / "SKILL.md").exists()


# R5 — malicious/out-of-bound markers rejected before any deletion
@pytest.mark.parametrize("escapee", ["parent", "sibling_skill", "userprofile"])
def test_r5_out_of_bound_marker_rejected(tmp_path: Path, escapee: str, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    begin_fresh_transaction(workspace)
    marker_path = workspace / ".cogentnexus-openclaw" / TRANSACTION_NAME
    payload = json.loads(marker_path.read_text(encoding="utf-8"))
    if escapee == "parent":
        bad = str((workspace.parent / "outside.txt").resolve())
    elif escapee == "sibling_skill":
        bad = str((workspace / "skills" / "other-skill").resolve())
    else:
        bad = str((tmp_path / "arbitrary" / "evil.txt").resolve())
    (tmp_path / "arbitrary").mkdir(exist_ok=True)
    sentinel_parent = workspace.parent / "outside.txt"
    if escapee == "parent":
        sentinel_parent.write_text("sentinel", encoding="utf-8")
    payload["createdPaths"] = [bad]
    marker_path.write_text(json.dumps(payload), encoding="utf-8")
    _make_residue(workspace)
    with pytest.raises(RuntimeError):
        recovery_preflight(workspace)
    if escapee == "parent":
        assert sentinel_parent.exists(), "out-of-bound path must never be deleted"
    # residue untouched after refusal
    assert (workspace / "skills" / "cogentnexus-openclaw" / "SKILL.md").exists()


# R5b — tampered marker (missing fields / unknown schema) rejected fail-closed
def test_r5b_invalid_marker_schema_rejected(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    begin_fresh_transaction(workspace)
    marker_path = workspace / ".cogentnexus-openclaw" / TRANSACTION_NAME
    payload = json.loads(marker_path.read_text(encoding="utf-8"))
    payload.pop("transactionId")
    marker_path.write_text(json.dumps(payload), encoding="utf-8")
    _make_residue(workspace)
    with pytest.raises(RuntimeError):
        recovery_preflight(workspace)


# R6 — unmarked partial state remains fail-closed
def test_r6_unmarked_residue_still_dead_ends(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _make_residue(workspace)
    with pytest.raises(RuntimeError, match="transaction marker"):
        recovery_preflight(workspace)
    with pytest.raises(RuntimeError):
        classify_install(workspace)
    # nothing was deleted by the refused recovery
    assert (workspace / "skills" / "cogentnexus-openclaw" / "SKILL.md").exists()
