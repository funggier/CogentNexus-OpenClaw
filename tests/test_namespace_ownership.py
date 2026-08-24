import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("namespace_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def layout(tmp_path: Path):
    workspace = tmp_path / ".openclaw" / "workspace"
    root = workspace / ".cogentnexus-openclaw"
    skill = workspace / "skills" / ownership.PRODUCT_ID
    launcher = workspace / "cnxclaw.cmd"
    plugin = workspace.parent / "extensions" / ownership.PRODUCT_ID
    return workspace, root, skill, launcher, plugin


def write_plugin(root: Path, *, marker="same", version="0.9.3") -> Path:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(parents=True, exist_ok=True)
    (root / "openclaw.plugin.json").write_text(json.dumps({"id": ownership.PRODUCT_ID, "version": version}), encoding="utf-8")
    (root / "package.json").write_text(json.dumps({"name": ownership.PLUGIN_PACKAGE, "version": version}), encoding="utf-8")
    (root / "scripts/bootstrap-ticket-db.mjs").write_text(marker, encoding="utf-8")
    (root / "dist/ticket-store.js").write_text(marker, encoding="utf-8")
    return root


def complete_install(tmp_path: Path, migration_source=None):
    workspace, root, skill, launcher, plugin = layout(tmp_path)
    root.mkdir(parents=True); skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("name: CogentNexus-OpenClaw", encoding="utf-8")
    launcher.write_text("cnxclaw", encoding="utf-8")
    write_plugin(plugin)
    payload = ownership.build_manifest(root=root, workspace=workspace, skill=skill, plugin_path=plugin,
                                       launcher=launcher, version="0.9.3", migration_source=migration_source)
    ownership.write_manifest(root, payload)
    return workspace, root, payload


def test_manifest_round_trip_exact_owned_artifacts(tmp_path: Path):
    workspace, root, _ = complete_install(tmp_path)
    verified = ownership.verify_manifest(root, workspace=workspace)
    assert verified["productId"] == ownership.PRODUCT_ID


@pytest.mark.parametrize("field,bad", [
    ("schemaVersion", 2), ("productId", "cogentnexus-hermesagent"),
    ("displayName", "CogentNexus"), ("installedVersion", "0.9.2"),
    ("workspace", "C:/foreign"), ("stateRoot", "C:/foreign"),
    ("skillPath", "C:/foreign"), ("pluginId", "foreign"),
    ("pluginPath", "C:/foreign"), ("launcherPath", "C:/foreign"),
    ("taskServiceIdentities", ["CogentNexus-OpenClaw-Supervisor"]),
    ("installedAt", "not-a-date"), ("migrationSource", "unknown"),
])
def test_every_manifest_field_tamper_fails_closed(tmp_path: Path, field: str, bad):
    workspace, root, payload = complete_install(tmp_path)
    payload[field] = bad
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError):
        ownership.verify_manifest(root, workspace=workspace)


def test_manifest_missing_or_extra_field_and_non_utc_timestamp_fail(tmp_path: Path):
    workspace, root, payload = complete_install(tmp_path)
    del payload["skillPath"]
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError, match="schema fields"):
        ownership.verify_manifest(root, workspace=workspace)
    workspace, root, payload = complete_install(tmp_path / "extra")
    payload["foreign"] = True
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError, match="schema fields"):
        ownership.verify_manifest(root, workspace=workspace)
    del payload["foreign"]; payload["installedAt"] = "2026-08-24T07:00:00+07:00"
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError, match="UTC"):
        ownership.verify_manifest(root, workspace=workspace)


def test_manifest_path_traversal_and_missing_owned_artifact_fail(tmp_path: Path):
    workspace, root, payload = complete_install(tmp_path)
    payload["pluginPath"] = str((workspace.parent / "extensions" / ".." / "foreign").resolve())
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError):
        ownership.verify_manifest(root, workspace=workspace)
    workspace, root, payload = complete_install(tmp_path / "missing")
    Path(payload["launcherPath"]).unlink()
    with pytest.raises(RuntimeError, match="incomplete"):
        ownership.verify_manifest(root, workspace=workspace)


def test_direct_and_npm_managed_plugin_resolution(tmp_path: Path):
    workspace, _, _, _, direct = layout(tmp_path)
    write_plugin(direct)
    assert ownership.resolve_installed_plugin(workspace.parent)["root"] == direct.resolve()
    for child in sorted(direct.rglob("*"), reverse=True):
        if child.is_file(): child.unlink()
        elif child.is_dir(): child.rmdir()
    direct.rmdir()
    managed = workspace.parent / "npm/projects/generation/node_modules" / ownership.PLUGIN_PACKAGE
    write_plugin(managed)
    assert ownership.resolve_installed_plugin(workspace.parent)["root"] == managed.resolve()


def test_equal_version_candidates_are_ambiguous_even_when_bytes_match(tmp_path: Path):
    workspace, _, _, _, direct = layout(tmp_path)
    managed = workspace.parent / "npm/projects/generation/node_modules" / ownership.PLUGIN_PACKAGE
    write_plugin(direct); write_plugin(managed)
    with pytest.raises(RuntimeError, match="ambiguous"):
        ownership.resolve_installed_plugin(workspace.parent)
    (managed / "dist/ticket-store.js").write_text("conflict", encoding="utf-8")
    with pytest.raises(RuntimeError, match="ambiguous"):
        ownership.resolve_installed_plugin(workspace.parent)


@pytest.mark.parametrize("artifact", ["launcherWindows", "launcherPosix", "skill", "state", "applicationData", "directPlugin"])
def test_each_partial_new_artifact_blocks_fresh_install(tmp_path: Path, artifact: str):
    workspace, root, skill, launcher, plugin = layout(tmp_path)
    app_data = tmp_path / "appdata" / ownership.DISPLAY_NAME
    paths = {"launcherWindows": launcher, "launcherPosix": workspace / "cnxclaw", "skill": skill,
             "state": root, "applicationData": app_data, "directPlugin": plugin}
    target = paths[artifact]
    if artifact in {"launcherWindows", "launcherPosix"}:
        target.parent.mkdir(parents=True, exist_ok=True); target.write_text("partial", encoding="utf-8")
    else:
        target.mkdir(parents=True, exist_ok=True)
    with pytest.raises(RuntimeError):
        ownership.classify_install(workspace, app_data=app_data)


def test_partial_new_combinations_and_valid_upgrade(tmp_path: Path):
    workspace, root, skill, launcher, _ = layout(tmp_path)
    skill.mkdir(parents=True); launcher.write_text("partial", encoding="utf-8")
    with pytest.raises(RuntimeError):
        ownership.classify_install(workspace, app_data=tmp_path / "absent")
    workspace, root, _ = complete_install(tmp_path / "complete")
    assert ownership.classify_install(workspace, app_data=tmp_path / "absent")["mode"] == "upgrade"


@pytest.mark.parametrize("mode", ["passthrough", "managed", "maintenance"])
def test_install_over_legacy_modes_requires_three_identities(tmp_path: Path, mode: str):
    workspace, *_ = layout(tmp_path)
    skill = workspace / "skills/cogentnexus"; skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# CogentNexus", encoding="utf-8")
    controller = workspace / ".cogent/host/controller.json"; controller.parent.mkdir(parents=True)
    controller.write_text(json.dumps({"mode": mode}), encoding="utf-8")
    launcher = workspace / "cnx.cmd"; launcher.write_text("--root .cogent", encoding="utf-8")
    result = ownership.classify_install(workspace, app_data=tmp_path / "absent")
    assert result["mode"] == "legacy" and result["legacyMode"] == mode


def test_hermes_openclaw_and_ollama_sentinels_remain_byte_identical(tmp_path: Path):
    workspace, root, _ = complete_install(tmp_path)
    sentinels = {
        workspace / "cnxhermes.cmd": b"hermes-launcher",
        workspace / ".cogentnexus-hermesagent/state.json": b"hermes-state",
        workspace.parent / "openclaw.json": b"openclaw",
        tmp_path / "ollama/models/model": b"ollama",
    }
    for path, value in sentinels.items(): path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(value)
    before = {path: path.read_bytes() for path in sentinels}
    ownership.verify_manifest(root, workspace=workspace)
    assert {path: path.read_bytes() for path in sentinels} == before
