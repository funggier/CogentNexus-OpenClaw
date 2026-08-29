import importlib.util
import json
from pathlib import Path
import shutil


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


def _task142_direct_layout(tmp_path: Path) -> dict[str, Path]:
    openclaw_state = tmp_path / ".openclaw"
    workspace = openclaw_state / "workspace"
    root = workspace / ".cogentnexus-openclaw"
    skill = workspace / "skills" / ownership.PRODUCT_ID
    launcher = workspace / "cnxclaw.cmd"
    app_data = tmp_path / "local-app-data" / ownership.DISPLAY_NAME
    direct = openclaw_state / "extensions" / ownership.PRODUCT_ID

    (root / "host").mkdir(parents=True)
    (root / "host" / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8"
    )
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("name: CogentNexus-OpenClaw", encoding="utf-8")
    launcher.write_text("cnxclaw", encoding="utf-8")
    _write_plugin(direct, marker="retired-A")

    manifest = ownership.build_manifest(
        root=root,
        workspace=workspace,
        skill=skill,
        plugin_path=direct,
        launcher=launcher,
        version=ownership.INSTALLED_VERSION,
    )
    ownership.write_manifest(root, manifest)

    return {
        "openclaw_state": openclaw_state,
        "workspace": workspace,
        "root": root,
        "app_data": app_data,
        "direct": direct,
    }


def test_task142_direct_same_path_replacement_finalizes_from_backup_and_fingerprint_transition(tmp_path: Path):
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

    shutil.rmtree(paths["direct"])
    shutil.copytree(candidate, paths["direct"])

    inventory = {
        "workspaceDir": str(paths["workspace"]),
        "registry": {"source": "persisted", "diagnostics": []},
        "plugins": [{
            "id": ownership.PRODUCT_ID,
            "packageName": ownership.PLUGIN_PACKAGE,
            "version": ownership.INSTALLED_VERSION,
            "rootDir": str(paths["direct"]),
            "source": str(paths["direct"] / "dist" / "index.js"),
            "enabled": False,
            "status": "disabled",
        }],
        "diagnostics": [],
    }

    result = ownership.finalize_plugin_rollover_transaction(
        transaction=transaction,
        plugin_inventory=inventory,
    )

    assert result["status"] == "ROLLOVER_APPLIED_PASSTHROUGH"
    assert Path(result["pluginPath"]) == paths["direct"].resolve()
    manifest = ownership.verify_manifest(paths["root"], workspace=paths["workspace"])
    assert Path(manifest["pluginPath"]) == paths["direct"].resolve()
