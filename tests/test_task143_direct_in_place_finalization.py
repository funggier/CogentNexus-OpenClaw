import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest


SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("task143_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def _write_plugin(root: Path, *, marker: str) -> Path:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(parents=True, exist_ok=True)
    (root / "openclaw.plugin.json").write_text(
        json.dumps({"id": ownership.PRODUCT_ID, "version": ownership.INSTALLED_VERSION}),
        encoding="utf-8",
    )
    (root / "package.json").write_text(
        json.dumps({
            "name": ownership.PLUGIN_PACKAGE,
            "version": ownership.INSTALLED_VERSION,
            "files": ["dist", "scripts/bootstrap-ticket-db.mjs", "openclaw.plugin.json", "README.md"],
        }),
        encoding="utf-8",
    )
    (root / "README.md").write_text("package readme", encoding="utf-8")
    (root / "scripts" / "bootstrap-ticket-db.mjs").write_text(marker, encoding="utf-8")
    (root / "dist" / "ticket-store.js").write_text(marker, encoding="utf-8")
    (root / "dist" / "index.js").write_text(marker, encoding="utf-8")
    return root


def _base_owned_layout(tmp_path: Path, plugin_path: Path) -> dict[str, Path]:
    openclaw_state = tmp_path / ".openclaw"
    workspace = openclaw_state / "workspace"
    root = workspace / ".cogentnexus-openclaw"
    skill = workspace / "skills" / ownership.PRODUCT_ID
    launcher = workspace / "cnxclaw.cmd"
    app_data = tmp_path / "local-app-data" / ownership.DISPLAY_NAME

    (root / "host").mkdir(parents=True)
    (root / "host" / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8"
    )
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("name: CogentNexus-OpenClaw", encoding="utf-8")
    launcher.write_text("cnxclaw", encoding="utf-8")

    manifest = ownership.build_manifest(
        root=root,
        workspace=workspace,
        skill=skill,
        plugin_path=plugin_path,
        launcher=launcher,
        version=ownership.INSTALLED_VERSION,
    )
    ownership.write_manifest(root, manifest)
    return {
        "openclaw_state": openclaw_state,
        "workspace": workspace,
        "root": root,
        "app_data": app_data,
        "plugin": plugin_path,
    }


def _task142_direct_layout(tmp_path: Path, *, marker: str = "retired-A") -> dict[str, Path]:
    direct = tmp_path / ".openclaw" / "extensions" / ownership.PRODUCT_ID
    _write_plugin(direct, marker=marker)
    paths = _base_owned_layout(tmp_path, direct)
    paths["direct"] = direct
    return paths


def _write_managed_wrapper(project: Path) -> Path:
    project.mkdir(parents=True, exist_ok=True)
    (project / "package.json").write_text(
        json.dumps({"private": True, "dependencies": {ownership.PLUGIN_PACKAGE: "file:plugin.tgz"}}),
        encoding="utf-8",
    )
    (project / "package-lock.json").write_text(
        json.dumps({
            "name": "openclaw-managed-plugin-root",
            "lockfileVersion": 3,
            "packages": {
                "": {"dependencies": {ownership.PLUGIN_PACKAGE: "file:plugin.tgz"}},
                f"node_modules/{ownership.PLUGIN_PACKAGE}": {"version": ownership.INSTALLED_VERSION},
            },
        }),
        encoding="utf-8",
    )
    return project


def _managed_layout(tmp_path: Path) -> dict[str, Path]:
    project = _write_managed_wrapper(
        tmp_path / ".openclaw" / "npm" / "projects" / ownership.PLUGIN_PACKAGE
    )
    plugin = _write_plugin(project / "node_modules" / ownership.PLUGIN_PACKAGE, marker="retired-managed-A")
    paths = _base_owned_layout(tmp_path, plugin)
    paths["project"] = project
    return paths


def _inventory(paths: dict[str, Path], root: Path | None = None) -> dict:
    plugin_root = root or paths["plugin"]
    return {
        "workspaceDir": str(paths["workspace"]),
        "registry": {"source": "persisted", "diagnostics": []},
        "plugins": [{
            "id": ownership.PRODUCT_ID,
            "packageName": ownership.PLUGIN_PACKAGE,
            "version": ownership.INSTALLED_VERSION,
            "rootDir": str(plugin_root),
            "source": str(plugin_root / "dist" / "index.js"),
            "enabled": False,
            "status": "disabled",
        }],
        "diagnostics": [],
    }


def _replace_payload(destination: Path, candidate: Path) -> None:
    shutil.rmtree(destination)
    shutil.copytree(candidate, destination)


def _prepare_direct_transition(tmp_path: Path) -> tuple[dict[str, Path], Path, dict, str, str]:
    paths = _task142_direct_layout(tmp_path)
    candidate = _write_plugin(tmp_path / "candidate-payload", marker="replacement-B")
    expected = ownership._plugin_payload(candidate)["fingerprint"]
    retired = ownership._plugin_payload(paths["direct"])["fingerprint"]
    assert expected != retired
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"],
        workspace=paths["workspace"],
        application_data=paths["app_data"],
        expected_replacement_fingerprint=expected,
        backup_token="task142-same-path",
    )
    assert transaction["retiredFingerprint"] == retired
    assert transaction["expectedReplacementFingerprint"] == expected
    assert Path(transaction["retiredPluginPath"]) == paths["direct"].resolve()
    assert Path(transaction["backupPath"]).is_dir()
    return paths, candidate, transaction, retired, expected


def test_task142_direct_same_path_replacement_finalizes_from_backup_and_fingerprint_transition(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)

    result = ownership.finalize_plugin_rollover_transaction(
        transaction=transaction,
        plugin_inventory=_inventory(paths, paths["direct"]),
    )

    assert result["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"
    assert Path(result["pluginPath"]) == paths["direct"].resolve()
    manifest = ownership.verify_manifest(paths["root"], workspace=paths["workspace"])
    assert Path(manifest["pluginPath"]) == paths["direct"].resolve()


def test_direct_same_path_rejects_no_fingerprint_transition(tmp_path: Path):
    paths = _task142_direct_layout(tmp_path)
    retired = ownership._plugin_payload(paths["direct"])["fingerprint"]
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"], expected_replacement_fingerprint=retired,
        backup_token="no-transition",
    )
    with pytest.raises(RuntimeError, match="transition|retired fingerprint|retired generation"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths, paths["direct"]),
        )


def test_managed_same_path_remains_rejected(tmp_path: Path):
    paths = _managed_layout(tmp_path)
    candidate = _write_plugin(tmp_path / "candidate-managed", marker="replacement-managed-B")
    expected = ownership._plugin_payload(candidate)["fingerprint"]
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"], expected_replacement_fingerprint=expected,
        backup_token="managed-same-path",
    )
    _replace_payload(paths["plugin"], candidate)
    with pytest.raises(RuntimeError, match="retired generation|managed"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths),
        )


def test_direct_same_path_rejects_tampered_backup(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    (Path(transaction["backupPath"]) / "dist" / "ticket-store.js").write_text("tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="backup proof|backup"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths, paths["direct"]),
        )


def test_direct_same_path_rejects_manifest_drift(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    manifest_path = paths["root"] / ownership.MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["installedAt"] = "2026-08-29T00:00:00+00:00"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(RuntimeError, match="manifest changed|manifest"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths, paths["direct"]),
        )


def test_direct_same_path_rejects_conflicting_product_storage_evidence(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    conflicting = paths["openclaw_state"] / "npm" / "projects" / "conflicting-product-wrapper"
    conflicting.mkdir(parents=True)
    (conflicting / "package.json").write_text(
        json.dumps({"private": True, "dependencies": {ownership.PLUGIN_PACKAGE: "file:foreign.tgz"}}),
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="conflicting|storage evidence|ownership"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths, paths["direct"]),
        )


def test_direct_transaction_rejects_root_indirection_added_after_prepare(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    redirected = paths["openclaw_state"] / "extensions" / "redirected-candidate"
    shutil.copytree(candidate, redirected)
    shutil.rmtree(paths["direct"])
    try:
        os.symlink(redirected, paths["direct"], target_is_directory=True)
    except OSError as symlink_error:
        result = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(paths["direct"]), str(redirected)],
            text=True, capture_output=True, check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"unable to create symlink or Windows junction: {symlink_error}; {result.stdout}{result.stderr}"
            ) from symlink_error
    with pytest.raises(RuntimeError, match="reparse|real directory|direct|indirection"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=_inventory(paths, paths["direct"]),
        )


def test_task142_partial_state_classifies_candidate_as_already_exact(tmp_path: Path):
    paths = _task142_direct_layout(tmp_path, marker="replacement-B")
    expected = ownership._plugin_payload(paths["direct"])["fingerprint"]
    result = ownership.classify_install(
        paths["workspace"], app_data=paths["app_data"],
        plugin_inventory=_inventory(paths, paths["direct"]),
        expected_replacement_fingerprint=expected,
    )
    assert result["mode"] == "upgrade"
    assert result["pendingRollover"] is False
    assert result["pluginAlreadyExact"] is True
    assert Path(result["replacementPluginPath"]) == paths["direct"].resolve()
