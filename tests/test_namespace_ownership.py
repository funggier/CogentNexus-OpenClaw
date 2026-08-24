import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("namespace_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def canonical_layout(tmp_path: Path):
    workspace = tmp_path / "workspace"
    root = workspace / ".cogentnexus-openclaw"
    return workspace, root


def test_manifest_round_trip_and_foreign_manifest_fail_closed(tmp_path: Path):
    workspace, root = canonical_layout(tmp_path)
    payload = ownership.build_manifest(
        root=root, workspace=workspace,
        skill=workspace / "skills" / ownership.PRODUCT_ID,
        plugin_path=tmp_path / "extensions" / ownership.PRODUCT_ID,
        launcher=workspace / "cnxclaw.cmd", version="0.9.3",
        task_services=["CogentNexus-OpenClaw-Supervisor"],
    )
    ownership.write_manifest(root, payload)
    assert ownership.verify_manifest(root, workspace=workspace)["productId"] == ownership.PRODUCT_ID
    payload["productId"] = "cogentnexus-hermesagent"
    ownership.write_manifest(root, payload)
    with pytest.raises(RuntimeError, match="refusing mutation"):
        ownership.verify_manifest(root, workspace=workspace)


@pytest.mark.parametrize("mode", ["passthrough", "managed", "maintenance"])
def test_legacy_requires_multiple_identities_and_rejects_mixed_layout(tmp_path: Path, mode: str):
    workspace, root = canonical_layout(tmp_path)
    skill = workspace / "skills" / "cogentnexus"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# CogentNexus\n", encoding="utf-8")
    state = workspace / ".cogent" / "host"
    state.mkdir(parents=True)
    (state / "controller.json").write_text(json.dumps({"mode": mode}), encoding="utf-8")
    (workspace / "cnx.cmd").write_text("python old.py --root .cogent", encoding="utf-8")
    proof = ownership.prove_legacy_ownership(workspace)
    assert proof["mode"] == "legacy"
    assert proof["legacyMode"] == mode
    assert len(proof["evidence"]) >= 3
    root.mkdir(parents=True)
    with pytest.raises(RuntimeError, match="mixed legacy/new"):
        ownership.prove_legacy_ownership(workspace)


def test_corrupted_or_unknown_legacy_controller_fails_closed(tmp_path: Path):
    workspace, _ = canonical_layout(tmp_path)
    skill = workspace / "skills" / "cogentnexus"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# CogentNexus\n", encoding="utf-8")
    controller = workspace / ".cogent" / "host" / "controller.json"
    controller.parent.mkdir(parents=True)
    (workspace / "cnx.cmd").write_text("python old.py --root .cogent", encoding="utf-8")
    controller.write_text("not-json", encoding="utf-8")
    with pytest.raises(RuntimeError, match="corrupted"):
        ownership.prove_legacy_ownership(workspace)
    controller.write_text(json.dumps({"mode": "foreign"}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="ambiguous"):
        ownership.prove_legacy_ownership(workspace)


def test_hermes_sentinels_are_outside_owned_manifest(tmp_path: Path):
    workspace, root = canonical_layout(tmp_path)
    sentinels = {
        workspace / "cnxhermes.cmd": b"hermes-launcher",
        workspace / ".cogentnexus-hermesagent" / "state.json": b"hermes-state",
        workspace / "skills" / "cogentnexus-hermesagent" / "SKILL.md": b"hermes-skill",
    }
    for path, content in sentinels.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    before = {path: path.read_bytes() for path in sentinels}
    payload = ownership.build_manifest(
        root=root, workspace=workspace, skill=workspace / "skills" / ownership.PRODUCT_ID,
        plugin_path=tmp_path / "extensions" / ownership.PRODUCT_ID,
        launcher=workspace / "cnxclaw.cmd", version="0.9.3")
    ownership.write_manifest(root, payload)
    assert all("hermesagent" not in value.lower() for key, value in payload.items() if isinstance(value, str))
    assert {path: path.read_bytes() for path in sentinels} == before
