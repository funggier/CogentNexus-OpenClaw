import copy
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

BASE = Path(__file__).with_name("test_plugin_generation_rollover.py")
SPEC = importlib.util.spec_from_file_location("semantic_matrix_base", BASE)
assert SPEC and SPEC.loader
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)
ownership = base.ownership


def _fingerprint(paths):
    return ownership._plugin_payload(paths["new_plugin"])["fingerprint"]


def _classify(paths, *, inventory=None, expected=None):
    return ownership.classify_install(
        paths["workspace"],
        app_data=paths["app_data"],
        plugin_inventory=inventory if inventory is not None else paths["inventory"],
        expected_replacement_fingerprint=expected if expected is not None else _fingerprint(paths),
    )


def _tree_snapshot(root: Path):
    root = root.resolve(strict=False)
    if not root.exists():
        return ("missing",)
    entries = []
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append((rel, "symlink", str(path.readlink())))
        elif path.is_dir():
            entries.append((rel, "dir"))
        elif path.is_file():
            entries.append((rel, "file", hashlib.sha256(path.read_bytes()).hexdigest()))
        else:
            entries.append((rel, "other"))
    return tuple(entries)


def _snap(paths, *extra_roots):
    return (
        _tree_snapshot(paths["openclaw_state"]),
        *(_tree_snapshot(Path(root)) for root in extra_roots),
    )


def _reject_unchanged(paths, *, match, inventory=None, expected=None, extra_roots=()):
    before = _snap(paths, *extra_roots)
    inventory_before = copy.deepcopy(inventory if inventory is not None else paths["inventory"])
    with pytest.raises(RuntimeError, match=match):
        _classify(paths, inventory=inventory, expected=expected)
    assert _snap(paths, *extra_roots) == before
    assert (inventory if inventory is not None else paths["inventory"]) == inventory_before


def _assert_success(paths, result):
    assert result["mode"] == "upgrade"
    assert result["pendingRollover"] is False
    assert result["pluginAlreadyExact"] is True
    assert result["interruptedRolloverReentry"] is True
    assert Path(result["replacementPluginPath"]) == paths["new_plugin"].resolve()
    assert Path(result["manifestPluginPath"]) == paths["old_plugin"].resolve()


def test_task115_positive_managed_contract(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    _assert_success(paths, _classify(paths))


def test_task115_positive_direct_contract(tmp_path: Path):
    paths = base._direct_reentry_layout(tmp_path)
    _assert_success(paths, _classify(paths))


@pytest.mark.parametrize("kind", ["cnx_cmd", "cnx_posix", "legacy_skill", "legacy_state", "legacy_plugin"])
def test_task115_real_legacy_residue_rejected_without_mutation(tmp_path: Path, kind: str):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    if kind == "cnx_cmd":
        legacy = paths["workspace"] / "cnx.cmd"; legacy.write_text("legacy")
    elif kind == "cnx_posix":
        legacy = paths["workspace"] / "cnx"; legacy.write_text("legacy")
    elif kind == "legacy_skill":
        legacy = paths["workspace"] / "skills" / "cogentnexus"; legacy.mkdir(parents=True); (legacy / "sentinel").write_text("legacy")
    elif kind == "legacy_state":
        legacy = paths["workspace"] / ".cogent"; legacy.mkdir(); (legacy / "sentinel").write_text("legacy")
    else:
        legacy = paths["openclaw_state"] / "extensions" / ownership.LEGACY_PLUGIN_ID; legacy.mkdir(parents=True); (legacy / "sentinel").write_text("legacy")
    observed = ownership.current_inventory(paths["workspace"], app_data=paths["app_data"])
    assert observed["legacy"]
    assert any(str(legacy) in item for item in observed["legacy"])
    _reject_unchanged(paths, match="mixed legacy state")


def test_task115_exact_payload_outside_state_rejected_for_containment(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    external = tmp_path / "outside-openclaw" / ownership.PLUGIN_PACKAGE
    shutil.copytree(paths["new_plugin"], external)
    shutil.rmtree(paths["new_project"])
    payload = ownership._plugin_payload(external)
    assert payload is not None
    inv = copy.deepcopy(paths["inventory"])
    inv["plugins"][0]["rootDir"] = str(external)
    _reject_unchanged(paths, match="outside its state boundary", inventory=inv, expected=payload["fingerprint"], extra_roots=(external,))


def test_task115_exact_payload_noncanonical_contained_rejected(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    noncanonical = paths["openclaw_state"] / "other" / ownership.PRODUCT_ID
    shutil.copytree(paths["new_plugin"], noncanonical)
    shutil.rmtree(paths["new_project"])
    payload = ownership._plugin_payload(noncanonical)
    assert payload is not None
    inv = copy.deepcopy(paths["inventory"])
    inv["plugins"][0]["rootDir"] = str(noncanonical)
    _reject_unchanged(paths, match="exactly one canonical active replacement", inventory=inv, expected=payload["fingerprint"])


def test_task115_active_foreign_wrapper_rejected_without_mutation(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    package_path = paths["new_project"] / "package.json"
    package = json.loads(package_path.read_text())
    package["dependencies"]["foreign-user-package"] = "file:foreign.tgz"
    package_path.write_text(json.dumps(package))
    sentinel = paths["new_project"] / "foreign-user-data.txt"; sentinel.write_text("preserve")
    _reject_unchanged(paths, match="storage ownership is unproven|wrapper ownership")
    assert sentinel.read_text() == "preserve"


@pytest.mark.parametrize("shape", ["managed", "direct"])
def test_task115_separate_conflicting_wrapper_rejected_without_mutation(tmp_path: Path, shape: str):
    paths = base.rollover_layout(tmp_path) if shape == "managed" else base._direct_reentry_layout(tmp_path)
    if shape == "managed":
        paths["old_project"].rename(tmp_path / "retired-generation-removed")
    base._add_conflicting_product_wrapper(paths)
    wrapper = paths["openclaw_state"] / "npm" / "projects" / "user-shared-wrapper"
    sentinel = wrapper / "foreign-user-data.txt"; sentinel.write_text("preserve")
    _reject_unchanged(paths, match="conflicting product storage evidence")
    assert sentinel.read_text() == "preserve"


def test_task115_duplicate_exact_payload_rejected_as_canonical_ambiguity(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    direct = paths["openclaw_state"] / "extensions" / ownership.PRODUCT_ID
    shutil.copytree(paths["new_plugin"], direct)
    assert ownership._plugin_payload(paths["new_plugin"]) is not None
    assert ownership._plugin_payload(direct) is not None
    _reject_unchanged(paths, match="exactly one canonical active replacement")


def test_task115_duplicate_registration_rejected_as_registration_ambiguity(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    inv = copy.deepcopy(paths["inventory"]); inv["plugins"].append(copy.deepcopy(inv["plugins"][0]))
    _reject_unchanged(paths, match="active canonical registration is not unique", inventory=inv)


@pytest.mark.parametrize(("field", "value", "match"), [
    ("id", "wrong", "active canonical registration is not unique"),
    ("packageName", "wrong", "registration package/version is unproven"),
    ("version", "0.9.2", "registration package/version is unproven"),
])
def test_task115_registration_identity_failures_are_semantic(tmp_path: Path, field: str, value: str, match: str):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    inv = copy.deepcopy(paths["inventory"]); inv["plugins"][0][field] = value
    _reject_unchanged(paths, match=match, inventory=inv)


def test_task115_candidate_fingerprint_mismatch_is_attestation_failure(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    _reject_unchanged(paths, match="fingerprint does not match the candidate attestation", expected="0" * 64)


def test_task115_controller_mode_failure_is_passthrough_boundary(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    (paths["root"] / "host" / "controller.json").write_text(json.dumps({"mode": "managed"}))
    _reject_unchanged(paths, match="requires PASSTHROUGH mode")


def test_task115_manifest_failure_is_schema_boundary(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    (paths["root"] / ownership.MANIFEST_NAME).write_text("{}")
    _reject_unchanged(paths, match="manifest schema fields are not exact")


@pytest.mark.parametrize(("kind", "match"), [("skill", "incomplete owned artifacts"), ("launcher", "incomplete owned artifacts")])
def test_task115_missing_owned_artifact_is_semantic(tmp_path: Path, kind: str, match: str):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    if kind == "skill":
        (paths["workspace"] / "skills" / ownership.PRODUCT_ID / "SKILL.md").unlink()
    else:
        (paths["workspace"] / "cnxclaw.cmd").unlink()
    _reject_unchanged(paths, match=match)


def test_task115_altered_retired_path_stays_off_reentry_shortcut(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    (paths["old_plugin"] / "dist" / "ticket-store.js").unlink()
    result = _classify(paths)
    assert result["pendingRollover"] is True
    assert result.get("interruptedRolloverReentry", False) is False


def test_task115_unrelated_npm_project_is_not_product_conflict(tmp_path: Path):
    paths = base.rollover_layout(tmp_path)
    paths["old_project"].rename(tmp_path / "retired-generation-removed")
    unrelated = paths["openclaw_state"] / "npm" / "projects" / "unrelated"
    unrelated.mkdir(parents=True)
    (unrelated / "package.json").write_text(json.dumps({"name": "unrelated"}))
    evidence = ownership.product_plugin_inventory(paths["openclaw_state"])
    assert all("unrelated" not in key for key in evidence)
    _assert_success(paths, _classify(paths))
