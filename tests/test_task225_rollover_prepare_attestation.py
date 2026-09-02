import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("task225_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def _write_direct_plugin(root: Path, *, marker: str) -> Path:
    (root / "dist").mkdir(parents=True, exist_ok=True)
    (root / "openclaw.plugin.json").write_text(
        json.dumps({"id": ownership.PRODUCT_ID, "version": ownership.INSTALLED_VERSION}),
        encoding="utf-8",
    )
    (root / "package.json").write_text(
        json.dumps({
            "name": ownership.PLUGIN_PACKAGE,
            "version": ownership.INSTALLED_VERSION,
            "files": ["dist", "openclaw.plugin.json"],
        }),
        encoding="utf-8",
    )
    (root / "dist" / "index.js").write_text(marker, encoding="utf-8")
    return root


def _owned_direct_layout(tmp_path: Path) -> dict[str, Path]:
    openclaw_state = tmp_path / ".openclaw"
    workspace = openclaw_state / "workspace"
    state_root = workspace / ".cogentnexus-openclaw"
    direct = openclaw_state / "extensions" / ownership.PRODUCT_ID
    skill = workspace / "skills" / ownership.PRODUCT_ID
    launcher = workspace / "cnxclaw.cmd"
    app_data = tmp_path / "local-app-data" / ownership.DISPLAY_NAME

    _write_direct_plugin(direct, marker="retired-A")
    (state_root / "host").mkdir(parents=True)
    (state_root / "host" / "controller.json").write_text(
        json.dumps({"mode": "passthrough"}), encoding="utf-8"
    )
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("name: CogentNexus-OpenClaw", encoding="utf-8")
    launcher.write_text("cnxclaw", encoding="utf-8")

    manifest = ownership.build_manifest(
        root=state_root,
        workspace=workspace,
        skill=skill,
        plugin_path=direct,
        launcher=launcher,
        version=ownership.INSTALLED_VERSION,
    )
    ownership.write_manifest(state_root, manifest)
    return {
        "openclaw_state": openclaw_state,
        "workspace": workspace,
        "state_root": state_root,
        "direct": direct,
        "app_data": app_data,
    }


def test_prepare_never_returns_internally_inconsistent_tree_attestations_when_nonpayload_source_changes_after_copy(
    tmp_path: Path, monkeypatch
):
    paths = _owned_direct_layout(tmp_path)
    candidate = _write_direct_plugin(tmp_path / "candidate", marker="replacement-B")
    expected = ownership._plugin_payload(candidate)["fingerprint"]

    # This file is intentionally outside package.json.files. It is accepted by
    # the current payload validator but participates in full project-tree proof.
    mutable_nonpayload = paths["direct"] / "runtime-state.txt"
    mutable_nonpayload.write_text("before-copy", encoding="utf-8")

    original_copytree = ownership.shutil.copytree

    def copy_then_change_source(source, destination, *args, **kwargs):
        result = original_copytree(source, destination, *args, **kwargs)
        Path(source, "runtime-state.txt").write_text("after-copy", encoding="utf-8")
        return result

    monkeypatch.setattr(ownership.shutil, "copytree", copy_then_change_source)

    transaction = ownership.prepare_plugin_rollover_transaction(
        root=paths["state_root"],
        workspace=paths["workspace"],
        application_data=paths["app_data"],
        expected_replacement_fingerprint=expected,
        backup_token="task225-attestation-race",
    )

    backup = Path(transaction["backupPath"])
    source_payload = ownership._plugin_payload(paths["direct"])
    backup_payload = ownership._plugin_payload(backup)
    assert source_payload is not None and backup_payload is not None
    assert source_payload["fingerprint"] == backup_payload["fingerprint"]

    # A successful prepare transaction must be self-consistent with the
    # finalizer contract; otherwise prepare has authorized an unfinalizable
    # transaction before the installer performs any replacement mutation.
    assert transaction["retiredProjectTreeSha256"] == transaction["backupProjectTreeSha256"]
