import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import shutil

import pytest


SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("rollover_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def write_plugin(root: Path, *, marker: str = "same", version: str = "0.9.3") -> Path:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(parents=True, exist_ok=True)
    (root / "openclaw.plugin.json").write_text(
        json.dumps({"id": ownership.PRODUCT_ID, "version": version}), encoding="utf-8"
    )
    (root / "package.json").write_text(
        json.dumps({
            "name": ownership.PLUGIN_PACKAGE,
            "version": version,
            "files": ["dist", "scripts/bootstrap-ticket-db.mjs", "openclaw.plugin.json", "README.md"],
        }), encoding="utf-8"
    )
    (root / "README.md").write_text("package readme", encoding="utf-8")
    (root / "scripts/bootstrap-ticket-db.mjs").write_text(marker, encoding="utf-8")
    (root / "dist/ticket-store.js").write_text(marker, encoding="utf-8")
    return root


def test_installable_runtime_change_changes_fingerprint(tmp_path: Path):
    plugin = write_plugin(tmp_path / "plugin")
    baseline = ownership.plugin_fingerprint(plugin)["fingerprint"]
    (plugin / "dist" / "v091-dashboard-verified-delivery.js").write_text("runtime-v1", encoding="utf-8")
    changed = ownership.plugin_fingerprint(plugin)["fingerprint"]
    assert changed != baseline


def test_installable_runtime_path_change_changes_fingerprint(tmp_path: Path):
    plugin = write_plugin(tmp_path / "plugin")
    (plugin / "dist" / "v091-dashboard-verified-delivery.js").write_text("runtime", encoding="utf-8")
    baseline = ownership.plugin_fingerprint(plugin)["fingerprint"]
    (plugin / "dist" / "v091-dashboard-verified-delivery.js").rename(plugin / "dist" / "renamed-runtime.js")
    changed = ownership.plugin_fingerprint(plugin)["fingerprint"]
    assert changed != baseline


def write_generation(openclaw_state: Path, name: str, *, marker: str = "same") -> tuple[Path, Path]:
    project = openclaw_state / "npm" / "projects" / name
    project.mkdir(parents=True)
    (project / "package.json").write_text(
        json.dumps({
            "private": True,
            "dependencies": {ownership.PLUGIN_PACKAGE: "file:plugin.tgz"},
        }),
        encoding="utf-8",
    )
    plugin = project / "node_modules" / ownership.PLUGIN_PACKAGE
    write_plugin(plugin, marker=marker)
    (project / "package-lock.json").write_text(
        json.dumps({
            "name": "openclaw-managed-plugin-root",
            "lockfileVersion": 3,
            "packages": {
                "": {
                    "dependencies": {ownership.PLUGIN_PACKAGE: "file:plugin.tgz"},
                },
                f"node_modules/{ownership.PLUGIN_PACKAGE}": {
                    "version": ownership.INSTALLED_VERSION,
                },
            },
        }),
        encoding="utf-8",
    )
    return project, plugin


def rollover_layout(tmp_path: Path) -> dict[str, Path | dict]:
    openclaw_state = tmp_path / ".openclaw"
    workspace = openclaw_state / "workspace"
    root = workspace / ".cogentnexus-openclaw"
    skill = workspace / "skills" / ownership.PRODUCT_ID
    launcher = workspace / "cnxclaw.cmd"
    app_data = tmp_path / "local-app-data" / ownership.DISPLAY_NAME
    root.mkdir(parents=True)
    (root / "host").mkdir()
    (root / "host" / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8"
    )
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("name: CogentNexus-OpenClaw", encoding="utf-8")
    launcher.write_text("cnxclaw", encoding="utf-8")
    old_project, old_plugin = write_generation(openclaw_state, ownership.PLUGIN_PACKAGE)
    new_project, new_plugin = write_generation(
        openclaw_state,
        f"{ownership.PLUGIN_PACKAGE}__openclaw-generation__g-0123456789abcdef",
    )
    manifest = ownership.build_manifest(
        root=root,
        workspace=workspace,
        skill=skill,
        plugin_path=old_plugin,
        launcher=launcher,
        version=ownership.INSTALLED_VERSION,
    )
    ownership.write_manifest(root, manifest)
    inventory = {
        "workspaceDir": str(workspace),
        "registry": {"source": "persisted", "diagnostics": []},
        "plugins": [{
            "id": ownership.PRODUCT_ID,
            "packageName": ownership.PLUGIN_PACKAGE,
            "version": ownership.INSTALLED_VERSION,
            "rootDir": str(new_plugin),
            "source": str(new_plugin / "dist" / "index.js"),
            "enabled": False,
            "status": "disabled",
        }],
        "diagnostics": [],
    }
    return {
        "openclaw_state": openclaw_state,
        "workspace": workspace,
        "root": root,
        "app_data": app_data,
        "old_project": old_project,
        "old_plugin": old_plugin,
        "new_project": new_project,
        "new_plugin": new_plugin,
        "inventory": inventory,
    }


def build_plan(paths: dict[str, Path | dict], *, token: str = "reviewed-test") -> dict:
    return ownership.build_plugin_rollover_plan(
        root=paths["root"],
        workspace=paths["workspace"],
        application_data=paths["app_data"],
        plugin_inventory=paths["inventory"],
        backup_token=token,
    )


def test_task054_two_roots_are_ambiguous_but_plan_binds_old_and_active_new(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    with pytest.raises(RuntimeError, match="ambiguous"):
        ownership.resolve_installed_plugin(paths["openclaw_state"])

    plan = build_plan(paths)

    assert Path(plan["retiredPluginPath"]) == paths["old_plugin"].resolve()
    assert Path(plan["replacementPluginPath"]) == paths["new_plugin"].resolve()
    assert Path(plan["retiredProjectRoot"]) == paths["old_project"].resolve()
    assert Path(plan["replacementProjectRoot"]) == paths["new_project"].resolve()
    assert plan["retiredFingerprint"] == plan["replacementFingerprint"]
    assert plan["controllerMode"] == "passthrough"
    assert len(plan["inventorySha256"]) == 64
    assert len(plan["activeRegistrationSha256"]) == 64
    assert len(plan["retiredProjectTreeSha256"]) == 64
    assert len(plan["replacementProjectTreeSha256"]) == 64
    assert plan["activeRegistration"]["rootDir"] == ownership._canonical(paths["new_plugin"])
    assert plan["activeRegistration"]["packageName"] == ownership.PLUGIN_PACKAGE
    assert plan["activeRegistration"]["packageNameEvidence"] == "inventory"


def test_plan_accepts_live_openclaw_record_without_optional_package_name_when_payload_proves_it(
    tmp_path: Path,
):
    paths = rollover_layout(tmp_path)
    record = paths["inventory"]["plugins"][0]
    record.pop("packageName")
    record.update({
        "name": "CogentNexus-OpenClaw Bridge",
        "origin": "global",
    })

    plan = build_plan(paths)

    assert plan["activeRegistration"] == {
        "id": "cogentnexus-openclaw",
        "packageName": "openclaw-plugin-cogentnexus-openclaw",
        "packageNameEvidence": "payload-package-json",
        "version": "0.9.3",
        "rootDir": ownership._canonical(paths["new_plugin"]),
        "source": str(paths["new_plugin"] / "dist" / "index.js"),
        "enabled": False,
        "status": "disabled",
    }


def test_plan_rejects_foreign_or_shared_wrapper_even_when_it_depends_on_product(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    wrapper_path = paths["old_project"] / "package.json"
    wrapper = json.loads(wrapper_path.read_text(encoding="utf-8"))
    wrapper["dependencies"]["unrelated-user-package"] = "1.0.0"
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")
    sentinel = paths["old_project"] / "unrelated-user-data.txt"
    sentinel.write_text("must survive", encoding="utf-8")

    with pytest.raises(RuntimeError, match="wrapper ownership"):
        build_plan(paths)

    assert sentinel.read_text(encoding="utf-8") == "must survive"
    assert paths["old_project"].is_dir()


def test_plan_accepts_only_openclaw_declared_managed_peer_dependencies(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    for key in ("old_project", "new_project"):
        wrapper_path = paths[key] / "package.json"
        wrapper = json.loads(wrapper_path.read_text(encoding="utf-8"))
        wrapper["dependencies"]["openclaw"] = "2026.8.0"
        wrapper["openclaw"] = {"managedPeerDependencies": ["openclaw"]}
        wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")
        lock_path = paths[key] / "package-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["packages"][""]["dependencies"]["openclaw"] = "2026.8.0"
        lock["packages"]["node_modules/openclaw"] = {"version": "2026.8.0"}
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

    plan = build_plan(paths)
    assert plan["retiredProjectTreeSha256"] != ""


@pytest.mark.parametrize("field,value", [
    ("id", "foreign"),
    ("packageName", "foreign-package"),
    ("packageName", None),
    ("version", "0.9.2"),
    ("rootDir", "foreign-root"),
])
def test_plan_rejects_unproven_active_registration_without_retiring_anything(
    tmp_path: Path, field: str, value: str
):
    paths = rollover_layout(tmp_path)
    inventory = json.loads(json.dumps(paths["inventory"]))
    inventory["plugins"][0][field] = value
    paths["inventory"] = inventory
    old_before = (paths["old_project"] / "package.json").read_bytes()

    with pytest.raises(RuntimeError):
        build_plan(paths)

    assert paths["old_project"].is_dir()
    assert (paths["old_project"] / "package.json").read_bytes() == old_before
    assert paths["new_project"].is_dir()


def test_apply_requires_exact_plan_hash_and_preserves_unrelated_projects(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    unrelated = paths["openclaw_state"] / "npm" / "projects" / "similarly-named-unrelated"
    unrelated.mkdir()
    (unrelated / "sentinel.bin").write_bytes(b"must-not-change")
    plan_path = tmp_path / "rollover-plan.json"
    written = ownership.write_plugin_rollover_plan(plan_path, build_plan(paths))

    with pytest.raises(RuntimeError, match="hash"):
        ownership.apply_plugin_rollover_plan(
            plan_path=plan_path,
            expected_plan_sha256="0" * 64,
            plugin_inventory=paths["inventory"],
        )
    assert paths["old_project"].is_dir()

    result = ownership.apply_plugin_rollover_plan(
        plan_path=plan_path,
        expected_plan_sha256=written["planSha256"],
        plugin_inventory=paths["inventory"],
    )

    assert result["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"
    assert not paths["old_project"].exists()
    assert Path(result["backupPath"]).is_dir()
    assert paths["new_project"].is_dir()
    assert (unrelated / "sentinel.bin").read_bytes() == b"must-not-change"
    assert ownership.resolve_installed_plugin(paths["openclaw_state"])["root"] == paths["new_plugin"].resolve()
    manifest = ownership.verify_manifest(paths["root"], workspace=paths["workspace"])
    assert Path(manifest["pluginPath"]) == paths["new_plugin"].resolve()


def test_apply_rejects_changed_fresh_inventory_before_any_mutation(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    plan_path = tmp_path / "rollover-plan.json"
    written = ownership.write_plugin_rollover_plan(plan_path, build_plan(paths))
    fresh_inventory = json.loads(json.dumps(paths["inventory"]))
    fresh_inventory["plugins"][0]["status"] = "loaded"

    with pytest.raises(RuntimeError, match="inventory changed"):
        ownership.apply_plugin_rollover_plan(
            plan_path=plan_path,
            expected_plan_sha256=written["planSha256"],
            plugin_inventory=fresh_inventory,
        )

    assert paths["old_project"].is_dir()
    assert paths["new_project"].is_dir()


def test_apply_atomic_rename_failure_preserves_source_manifest_and_replacement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    paths = rollover_layout(tmp_path)
    manifest_before = (paths["root"] / ownership.MANIFEST_NAME).read_bytes()
    plan_path = tmp_path / "rollover-plan.json"
    written = ownership.write_plugin_rollover_plan(plan_path, build_plan(paths))

    def fail_replace(source, destination):
        raise OSError("injected atomic rename failure")

    monkeypatch.setattr(ownership.os, "replace", fail_replace)
    with pytest.raises(RuntimeError, match="before retirement"):
        ownership.apply_plugin_rollover_plan(
            plan_path=plan_path,
            expected_plan_sha256=written["planSha256"],
            plugin_inventory=paths["inventory"],
        )

    assert paths["old_project"].is_dir()
    assert paths["new_project"].is_dir()
    assert (paths["root"] / ownership.MANIFEST_NAME).read_bytes() == manifest_before


def test_apply_rolls_back_project_and_manifest_when_final_verification_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    paths = rollover_layout(tmp_path)
    manifest_before = (paths["root"] / ownership.MANIFEST_NAME).read_bytes()
    plan_path = tmp_path / "rollover-plan.json"
    plan = build_plan(paths)
    backup_path = Path(plan["backupPath"])
    written = ownership.write_plugin_rollover_plan(plan_path, plan)
    real_verify = ownership.verify_manifest

    def fail_only_after_retirement(root: Path, *, workspace: Path, **kwargs):
        if not paths["old_project"].exists():
            raise RuntimeError("injected final verification failure")
        return real_verify(root, workspace=workspace, **kwargs)

    monkeypatch.setattr(ownership, "verify_manifest", fail_only_after_retirement)
    with pytest.raises(RuntimeError, match="rollback complete"):
        ownership.apply_plugin_rollover_plan(
            plan_path=plan_path,
            expected_plan_sha256=written["planSha256"],
            plugin_inventory=paths["inventory"],
        )

    assert paths["old_project"].is_dir()
    assert paths["new_project"].is_dir()
    assert (paths["root"] / ownership.MANIFEST_NAME).read_bytes() == manifest_before
    assert not backup_path.exists()


def test_plan_rejects_conflicting_same_version_replacement_payload(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("conflict", encoding="utf-8")
    with pytest.raises(RuntimeError, match="conflicts"):
        build_plan(paths)
    assert paths["old_project"].is_dir()
    assert paths["new_project"].is_dir()


def test_plan_requires_external_variant_scoped_application_data(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    paths["app_data"] = tmp_path / "foreign-backups"
    with pytest.raises(RuntimeError, match="application-data"):
        build_plan(paths)


def test_plan_rejects_non_passthrough_and_linked_or_non_npm_candidates(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["root"] / "host" / "controller.json").write_text(
        json.dumps({"mode": "managed"}), encoding="utf-8"
    )
    with pytest.raises(RuntimeError, match="PASSTHROUGH"):
        build_plan(paths)

    (paths["root"] / "host" / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8"
    )
    paths["inventory"]["plugins"][0]["rootDir"] = str(tmp_path / "linked-source")
    with pytest.raises(RuntimeError, match="active"):
        build_plan(paths)


def test_plan_apply_cli_round_trip_requires_and_returns_review_hash(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    inventory_path = tmp_path / "plugin-inventory.json"
    plan_path = tmp_path / "plugin-rollover-plan.json"
    inventory_path.write_text(json.dumps(paths["inventory"]), encoding="utf-8")
    planned = subprocess.run(
        [
            sys.executable, str(SCRIPT), "rollover-plan",
            "--root", str(paths["root"]),
            "--workspace", str(paths["workspace"]),
            "--app-data", str(paths["app_data"]),
            "--inventory-json", str(inventory_path),
            "--plan", str(plan_path),
        ],
        text=True, capture_output=True, check=False,
    )
    assert planned.returncode == 0, planned.stderr
    plan_result = json.loads(planned.stdout)
    assert plan_result["planPath"] == str(plan_path.resolve())
    assert len(plan_result["planSha256"]) == 64

    applied = subprocess.run(
        [
            sys.executable, str(SCRIPT), "rollover-apply",
            "--plan", str(plan_path),
            "--plan-sha256", plan_result["planSha256"],
            "--inventory-json", str(inventory_path),
        ],
        text=True, capture_output=True, check=False,
    )
    assert applied.returncode == 0, applied.stderr
    assert json.loads(applied.stdout)["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"


def test_task085_single_manifest_owned_changed_source_is_normal_upgrade(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    shutil.rmtree(paths["new_project"])
    expected = ownership._plugin_payload(paths["old_plugin"])["fingerprint"]
    (paths["old_plugin"] / "dist" / "ticket-store.js").write_text("old", encoding="utf-8")
    expected_source = expected
    inventory = json.loads(json.dumps(paths["inventory"]))
    inventory["plugins"][0]["rootDir"] = str(paths["old_plugin"])
    result = ownership.classify_install(
        paths["workspace"], app_data=paths["app_data"],
        plugin_inventory=inventory,
        expected_replacement_fingerprint=expected_source,
    )
    assert result["pendingRollover"] is False
    assert result["pluginAlreadyExact"] is False


def test_task085_equivalent_pending_payload_still_requires_source_equality(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    with pytest.raises(RuntimeError, match="source"):
        ownership.classify_install(
            paths["workspace"], app_data=paths["app_data"],
            plugin_inventory=paths["inventory"],
            expected_replacement_fingerprint="0" * 64,
        )


def test_task085_production_action_truth_table_exists_and_pending_is_rollover_only():
    helper = Path(__file__).parents[1] / "scripts" / "resolve-plugin-lifecycle-actions.ps1"
    assert helper.is_file()
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
         "-Mode", "upgrade", "-PendingRollover"],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    actions = json.loads(result.stdout)
    assert actions["installPlugin"] is False
    assert actions["rolloverPlugin"] is True


def test_task085_production_action_truth_table_all_supported_states():
    helper = Path(__file__).parents[1] / "scripts" / "resolve-plugin-lifecycle-actions.ps1"
    cases = [
        (("fresh",), {"installPlugin": True, "rolloverPlugin": False}),
        (("legacy",), {"installPlugin": True, "rolloverPlugin": False}),
        (("upgrade",), {"installPlugin": True, "rolloverPlugin": True}),
        (("upgrade", "-PendingRollover"), {"installPlugin": False, "rolloverPlugin": True}),
        (("upgrade", "-PluginAlreadyExact"), {"installPlugin": False, "rolloverPlugin": False}),
        (("upgrade", "-PendingRollover", "-SkipPlugin"), {"installPlugin": False, "rolloverPlugin": False}),
    ]
    for args, expected in cases:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
             "-Mode", args[0], *args[1:]], text=True, capture_output=True, check=False,
        )
        assert result.returncode == 0, result.stderr
        actions = json.loads(result.stdout)
        assert {key: actions[key] for key in expected} == expected

    impossible = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
         "-Mode", "upgrade", "-PendingRollover", "-PluginAlreadyExact"],
        text=True, capture_output=True, check=False,
    )
    assert impossible.returncode != 0


def test_source_attested_changed_payload_is_authorized_and_bound_into_plan(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    expected = ownership._plugin_payload(paths["new_plugin"])["fingerprint"]
    plan = ownership.build_plugin_rollover_plan(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"], plugin_inventory=paths["inventory"],
        expected_replacement_fingerprint=expected, backup_token="attested-test",
    )
    assert plan["replacementFingerprint"] == expected
    assert plan["expectedReplacementFingerprint"] == expected
    assert plan["replacementAuthorization"] == "candidate-source-fingerprint"


def test_wrong_source_attestation_rejects_without_retirement(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    before = (paths["old_project"] / "package.json").read_bytes()
    with pytest.raises(RuntimeError, match="attestation"):
        ownership.build_plugin_rollover_plan(
            root=paths["root"], workspace=paths["workspace"],
            application_data=paths["app_data"], plugin_inventory=paths["inventory"],
            expected_replacement_fingerprint="0" * 64, backup_token="wrong-test",
        )
    assert paths["old_project"].is_dir()
    assert (paths["old_project"] / "package.json").read_bytes() == before


def test_attested_pending_rollover_classification_accepts_exact_two_generation_topology(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    expected = ownership._plugin_payload(paths["new_plugin"])["fingerprint"]
    result = ownership.classify_install(
        paths["workspace"], app_data=paths["app_data"],
        plugin_inventory=paths["inventory"],
        expected_replacement_fingerprint=expected,
    )
    assert result["mode"] == "upgrade"
    assert result["pendingRollover"] is True
    assert result["pluginAlreadyExact"] is False
    assert Path(result["manifestPluginPath"]) == paths["old_plugin"].resolve()
    assert Path(result["replacementPluginPath"]) == paths["new_plugin"].resolve()
    assert result["expectedReplacementFingerprint"] == expected


def test_unattested_pending_rollover_classification_remains_ambiguous(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    with pytest.raises(RuntimeError, match="ambiguous"):
        ownership.classify_install(
            paths["workspace"], app_data=paths["app_data"],
            plugin_inventory=paths["inventory"],
        )


def test_rollover_plan_cli_requires_source_attestation_for_changed_payload(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    inventory_path = tmp_path / "inventory.json"
    plan_path = tmp_path / "plan.json"
    inventory_path.write_text(json.dumps(paths["inventory"]), encoding="utf-8")
    result = subprocess.run([
        sys.executable, str(SCRIPT), "rollover-plan",
        "--root", str(paths["root"]), "--workspace", str(paths["workspace"]),
        "--app-data", str(paths["app_data"]), "--inventory-json", str(inventory_path),
        "--plan", str(plan_path), "--expected-replacement-fingerprint", "0" * 64,
    ], text=True, capture_output=True, check=False)
    assert result.returncode != 0
    assert "attestation" in (result.stderr + result.stdout).lower()


def test_attested_changed_payload_applies_and_binds_source_fingerprint(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    expected = ownership._plugin_payload(paths["new_plugin"])["fingerprint"]
    plan_path = tmp_path / "attested-plan.json"
    written = ownership.write_plugin_rollover_plan(
        plan_path,
        ownership.build_plugin_rollover_plan(
            root=paths["root"], workspace=paths["workspace"],
            application_data=paths["app_data"], plugin_inventory=paths["inventory"],
            expected_replacement_fingerprint=expected, backup_token="attested-apply",
        ),
    )
    result = ownership.apply_plugin_rollover_plan(
        plan_path=plan_path, expected_plan_sha256=written["planSha256"],
        plugin_inventory=paths["inventory"],
    )
    assert result["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"
    assert paths["old_project"].exists() is False
    assert Path(result["pluginPath"]) == paths["new_plugin"].resolve()


def test_rollover_transaction_survives_external_replacement_of_old_generation(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    expected = ownership._plugin_payload(paths["new_plugin"])["fingerprint"]
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"], expected_replacement_fingerprint=expected,
        backup_token="transaction-boundary",
    )

    shutil.rmtree(paths["old_project"])
    result = ownership.finalize_plugin_rollover_transaction(
        transaction=transaction, plugin_inventory=paths["inventory"],
    )

    assert result["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"
    assert Path(result["pluginPath"]) == paths["new_plugin"].resolve()
    assert Path(result["backupPath"]).is_dir()
    manifest = ownership.verify_manifest(paths["root"], workspace=paths["workspace"])
    assert Path(manifest["pluginPath"]) == paths["new_plugin"].resolve()


def test_rollover_transaction_rejects_unexpected_replacement_without_commit(tmp_path: Path):
    paths = rollover_layout(tmp_path)
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"],
        expected_replacement_fingerprint="0" * 64,
        backup_token="transaction-mismatch",
    )
    manifest_before = (paths["root"] / ownership.MANIFEST_NAME).read_bytes()
    shutil.rmtree(paths["old_project"])

    with pytest.raises(RuntimeError, match="replacement|attestation"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction, plugin_inventory=paths["inventory"],
        )

    assert (paths["root"] / ownership.MANIFEST_NAME).read_bytes() == manifest_before


def test_rollover_final_verification_failure_does_not_restore_missing_retired_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    paths = rollover_layout(tmp_path)
    (paths["new_plugin"] / "dist" / "ticket-store.js").write_text("new", encoding="utf-8")
    expected = ownership._plugin_payload(paths["new_plugin"])["fingerprint"]
    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["root"], workspace=paths["workspace"],
        application_data=paths["app_data"], expected_replacement_fingerprint=expected,
        backup_token="final-verification-failure",
    )
    shutil.rmtree(paths["old_project"])
    real_verify = ownership.verify_manifest

    def fail_after_replacement_commit(root: Path, *, workspace: Path, **kwargs):
        manifest = json.loads((root / ownership.MANIFEST_NAME).read_text(encoding="utf-8"))
        if manifest["pluginPath"] == ownership._canonical(paths["new_plugin"]):
            raise RuntimeError("injected final verification failure")
        return real_verify(root, workspace=workspace, **kwargs)

    monkeypatch.setattr(ownership, "verify_manifest", fail_after_replacement_commit)
    with pytest.raises(RuntimeError, match="injected final verification failure"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction, plugin_inventory=paths["inventory"],
        )

    manifest_path = paths["root"] / ownership.MANIFEST_NAME
    assert not manifest_path.exists()
    assert not paths["old_project"].exists()
    assert Path(transaction["backupPath"]).is_dir()
