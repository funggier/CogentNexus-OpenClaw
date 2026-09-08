import importlib.util
import hashlib
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


def _quarantine_with_committed_marker(paths: dict[str, Path]) -> None:
    ownership.manifest_path(paths["root"]).unlink()
    marker = {
        "schemaVersion": ownership._TRANSACTION_SCHEMA_VERSION,
        "transactionId": f"{ownership.PRODUCT_ID}-test-recovery",
        "productId": ownership.PRODUCT_ID,
        "installedVersion": ownership.INSTALLED_VERSION,
        "workspace": ownership._canonical(paths["workspace"]),
        "stateRoot": ownership._canonical(paths["root"]),
        "skillPath": ownership._canonical(paths["workspace"] / "skills" / ownership.PRODUCT_ID),
        "applicationData": ownership._canonical(paths["app_data"]),
        "state": "committed",
        "createdAt": "2026-09-08T00:00:00+00:00",
        "createdPaths": [],
        "applicationDataPreexisting": False,
    }
    ownership.transaction_path(paths["root"]).write_text(json.dumps(marker), encoding="utf-8")


def _recover(paths: dict[str, Path], transaction: dict, inventory: dict | None = None):
    transaction_bytes = json.dumps(transaction).encode("utf-8")
    return ownership.recover_quarantined_plugin_rollover(
        transaction_bytes=transaction_bytes,
        plugin_inventory=inventory or _inventory(paths, paths["direct"]),
        workspace=paths["workspace"],
        application_data=paths["app_data"],
        expected_transaction_sha256=hashlib.sha256(transaction_bytes).hexdigest(),
        expected_replacement_fingerprint=transaction["expectedReplacementFingerprint"],
    )


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


def test_quarantined_direct_rollover_recovers_only_from_transaction_proof(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    ownership.manifest_path(paths["root"]).unlink()
    marker = {
        "schemaVersion": ownership._TRANSACTION_SCHEMA_VERSION,
        "transactionId": f"{ownership.PRODUCT_ID}-test-recovery",
        "productId": ownership.PRODUCT_ID,
        "installedVersion": ownership.INSTALLED_VERSION,
        "workspace": ownership._canonical(paths["workspace"]),
        "stateRoot": ownership._canonical(paths["root"]),
        "skillPath": ownership._canonical(paths["workspace"] / "skills" / ownership.PRODUCT_ID),
        "applicationData": ownership._canonical(paths["app_data"]),
        "state": "committed",
        "createdAt": "2026-09-08T00:00:00+00:00",
        "createdPaths": [],
        "applicationDataPreexisting": False,
    }
    ownership.transaction_path(paths["root"]).write_text(json.dumps(marker), encoding="utf-8")

    transaction_bytes = json.dumps(transaction).encode("utf-8")
    result = ownership.recover_quarantined_plugin_rollover(
        transaction_bytes=transaction_bytes,
        plugin_inventory=_inventory(paths, paths["direct"]),
        workspace=paths["workspace"],
        application_data=paths["app_data"],
        expected_transaction_sha256=hashlib.sha256(transaction_bytes).hexdigest(),
        expected_replacement_fingerprint=transaction["expectedReplacementFingerprint"],
    )

    assert result["status"] == "ROLLOVER_RECOVERED_PASSTHROUGH"
    manifest = ownership.verify_manifest(paths["root"], workspace=paths["workspace"])
    assert manifest["installedVersion"] == ownership.INSTALLED_VERSION
    assert Path(manifest["pluginPath"]) == paths["direct"].resolve()


def test_quarantined_rollover_recovery_rejects_tampered_backup_without_adoption(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    ownership.manifest_path(paths["root"]).unlink()
    marker = {
        "schemaVersion": ownership._TRANSACTION_SCHEMA_VERSION,
        "transactionId": f"{ownership.PRODUCT_ID}-tamper-test",
        "productId": ownership.PRODUCT_ID,
        "installedVersion": ownership.INSTALLED_VERSION,
        "workspace": ownership._canonical(paths["workspace"]),
        "stateRoot": ownership._canonical(paths["root"]),
        "skillPath": ownership._canonical(paths["workspace"] / "skills" / ownership.PRODUCT_ID),
        "applicationData": ownership._canonical(paths["app_data"]),
        "state": "committed",
        "createdAt": "2026-09-08T00:00:00+00:00",
        "createdPaths": [],
        "applicationDataPreexisting": False,
    }
    ownership.transaction_path(paths["root"]).write_text(json.dumps(marker), encoding="utf-8")
    (Path(transaction["backupPath"]) / "dist" / "ticket-store.js").write_text("tampered", encoding="utf-8")

    with pytest.raises(RuntimeError, match="backup"):
        transaction_bytes = json.dumps(transaction).encode("utf-8")
        ownership.recover_quarantined_plugin_rollover(
            transaction_bytes=transaction_bytes,
            plugin_inventory=_inventory(paths, paths["direct"]),
            workspace=paths["workspace"],
            application_data=paths["app_data"],
            expected_transaction_sha256=hashlib.sha256(transaction_bytes).hexdigest(),
            expected_replacement_fingerprint=transaction["expectedReplacementFingerprint"],
        )

    assert not ownership.manifest_path(paths["root"]).exists()


def test_quarantined_rollover_cli_recovers_from_exact_transaction(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    ownership.manifest_path(paths["root"]).unlink()
    marker = {
        "schemaVersion": ownership._TRANSACTION_SCHEMA_VERSION,
        "transactionId": f"{ownership.PRODUCT_ID}-cli-test",
        "productId": ownership.PRODUCT_ID,
        "installedVersion": ownership.INSTALLED_VERSION,
        "workspace": ownership._canonical(paths["workspace"]),
        "stateRoot": ownership._canonical(paths["root"]),
        "skillPath": ownership._canonical(paths["workspace"] / "skills" / ownership.PRODUCT_ID),
        "applicationData": ownership._canonical(paths["app_data"]),
        "state": "committed",
        "createdAt": "2026-09-08T00:00:00+00:00",
        "createdPaths": [],
        "applicationDataPreexisting": False,
    }
    ownership.transaction_path(paths["root"]).write_text(json.dumps(marker), encoding="utf-8")
    transaction_path = tmp_path / "rollover.json"
    inventory_path = tmp_path / "inventory.json"
    transaction_path.write_text(json.dumps(transaction), encoding="utf-8")
    inventory_path.write_text(json.dumps(_inventory(paths, paths["direct"])), encoding="utf-8")
    transaction_sha256 = ownership._sha256_file(transaction_path)

    result = subprocess.run([
        "python", str(SCRIPT), "rollover-recover",
        "--transaction", str(transaction_path), "--inventory-json", str(inventory_path),
        "--workspace", str(paths["workspace"]), "--app-data", str(paths["app_data"]),
        "--expected-transaction-sha256", transaction_sha256,
        "--expected-replacement-fingerprint", transaction["expectedReplacementFingerprint"],
    ], text=True, capture_output=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "ROLLOVER_RECOVERED_PASSTHROUGH"


@pytest.mark.parametrize("field", [
    "workspace", "stateRoot", "openclawState", "applicationData",
    "backupPath", "retiredPluginPath", "retiredProjectRoot",
])
def test_quarantined_recovery_rejects_attacker_controlled_path_fields(tmp_path: Path, field: str):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)
    outside = tmp_path / "attacker" / field
    outside.mkdir(parents=True)
    transaction[field] = ownership._canonical(outside)

    with pytest.raises(RuntimeError, match="workspace|state|application|backup|retired|boundary|binding"):
        _recover(paths, transaction)

    assert not ownership.manifest_path(paths["root"]).exists()


@pytest.mark.parametrize("mode", ["managed", "maintenance"])
def test_quarantined_recovery_requires_live_passthrough_controller(tmp_path: Path, mode: str):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)
    (paths["root"] / "host" / "controller.json").write_text(json.dumps({"mode": mode}), encoding="utf-8")

    with pytest.raises(RuntimeError, match="PASSTHROUGH|controller"):
        _recover(paths, transaction)

    assert not ownership.manifest_path(paths["root"]).exists()


@pytest.mark.parametrize("controller", [None, "not-json"])
def test_quarantined_recovery_rejects_missing_or_unreadable_live_controller(tmp_path: Path, controller: str | None):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)
    controller_path = paths["root"] / "host" / "controller.json"
    if controller is None:
        controller_path.unlink()
    else:
        controller_path.write_text(controller, encoding="utf-8")

    with pytest.raises(RuntimeError, match="controller.*missing|unreadable"):
        _recover(paths, transaction)

    assert not ownership.manifest_path(paths["root"]).exists()


def test_quarantined_recovery_rechecks_live_controller_after_finalization(tmp_path: Path, monkeypatch):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)
    real_require = ownership._require_passthrough
    calls = 0

    def changing_controller(root: Path) -> str:
        nonlocal calls
        calls += 1
        if calls == 2:
            (root / "host" / "controller.json").write_text(
                json.dumps({"mode": "managed"}), encoding="utf-8"
            )
        return real_require(root)

    monkeypatch.setattr(ownership, "_require_passthrough", changing_controller)
    with pytest.raises(RuntimeError, match="PASSTHROUGH"):
        _recover(paths, transaction)

    assert calls == 2
    assert not ownership.manifest_path(paths["root"]).exists()


def test_rollover_recovery_cli_rejects_wrong_out_of_band_transaction_digest(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    ownership.manifest_path(paths["root"]).unlink()
    marker = {
        "schemaVersion": ownership._TRANSACTION_SCHEMA_VERSION,
        "transactionId": f"{ownership.PRODUCT_ID}-digest-test",
        "productId": ownership.PRODUCT_ID,
        "installedVersion": ownership.INSTALLED_VERSION,
        "workspace": ownership._canonical(paths["workspace"]),
        "stateRoot": ownership._canonical(paths["root"]),
        "skillPath": ownership._canonical(paths["workspace"] / "skills" / ownership.PRODUCT_ID),
        "applicationData": ownership._canonical(paths["app_data"]),
        "state": "committed",
        "createdAt": "2026-09-08T00:00:00+00:00",
        "createdPaths": [],
        "applicationDataPreexisting": False,
    }
    ownership.transaction_path(paths["root"]).write_text(json.dumps(marker), encoding="utf-8")
    transaction_path = tmp_path / "rollover.json"
    inventory_path = tmp_path / "inventory.json"
    transaction_path.write_text(json.dumps(transaction), encoding="utf-8")
    inventory_path.write_text(json.dumps(_inventory(paths, paths["direct"])), encoding="utf-8")

    result = subprocess.run([
        "python", str(SCRIPT), "rollover-recover",
        "--transaction", str(transaction_path), "--inventory-json", str(inventory_path),
        "--workspace", str(paths["workspace"]), "--app-data", str(paths["app_data"]),
        "--expected-transaction-sha256", "0" * 64,
        "--expected-replacement-fingerprint", transaction["expectedReplacementFingerprint"],
    ], text=True, capture_output=True, check=False)

    assert result.returncode != 0
    assert "transaction digest" in (result.stdout + result.stderr)
    assert not ownership.manifest_path(paths["root"]).exists()


def test_recovery_binds_digest_to_the_exact_bytes_it_parses(tmp_path: Path):
    paths, candidate, transaction, _, _ = _prepare_direct_transition(tmp_path)
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)
    transaction_bytes = json.dumps(transaction).encode("utf-8")
    different_bytes = json.dumps({**transaction, "createdAt": "forged-after-authorization"}).encode("utf-8")
    expected_digest = hashlib.sha256(different_bytes).hexdigest()

    with pytest.raises(RuntimeError, match="transaction digest"):
        ownership.recover_quarantined_plugin_rollover(
            transaction_bytes=transaction_bytes,
            plugin_inventory=_inventory(paths, paths["direct"]),
            workspace=paths["workspace"],
            application_data=paths["app_data"],
            expected_transaction_sha256=expected_digest,
            expected_replacement_fingerprint=transaction["expectedReplacementFingerprint"],
        )

    assert not ownership.manifest_path(paths["root"]).exists()


def test_quarantined_recovery_accepts_semantic_manifest_with_unreproducible_historical_bytes(tmp_path: Path):
    paths = _task142_direct_layout(tmp_path)
    manifest_file = ownership.manifest_path(paths["root"])
    semantic_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest_file.write_bytes(json.dumps(semantic_manifest, separators=(",", ":")).encode("utf-8"))
    candidate = _write_plugin(tmp_path / "candidate-payload", marker="replacement-B")
    expected = ownership._plugin_payload(candidate)["fingerprint"]
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"], application_data=paths["app_data"],
        expected_replacement_fingerprint=expected, backup_token="semantic-bytes",
    )
    _replace_payload(paths["direct"], candidate)
    _quarantine_with_committed_marker(paths)

    result = _recover(paths, transaction)

    assert result["status"] == "ROLLOVER_RECOVERED_PASSTHROUGH"
    assert ownership.manifest_path(paths["root"]).exists()


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
