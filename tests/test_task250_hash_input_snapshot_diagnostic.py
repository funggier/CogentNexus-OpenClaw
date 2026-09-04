import json
from pathlib import Path

import pytest

from test_task225_rollover_prepare_attestation import _owned_direct_layout, _write_direct_plugin, ownership


def test_task250_mismatch_reports_exact_same_scan_snapshot_delta(tmp_path: Path, monkeypatch):
    paths = _owned_direct_layout(tmp_path)
    candidate = _write_direct_plugin(tmp_path / "candidate", marker="replacement-B")
    expected = ownership._plugin_payload(candidate)["fingerprint"]
    mutable = paths["direct"] / "runtime-state.txt"
    mutable.write_text("before-copy", encoding="utf-8")

    original_copytree = ownership.shutil.copytree
    original_snapshot = getattr(ownership, "_project_tree_snapshot", None)
    calls = []
    mutated = False

    def copy_then_change_source(source, destination, *args, **kwargs):
        nonlocal mutated
        result = original_copytree(source, destination, *args, **kwargs)
        if not mutated and Path(source).resolve() == paths["direct"].resolve():
            mutable.write_text("after-copy", encoding="utf-8")
            mutated = True
        return result

    def snapshot(root):
        calls.append(Path(root).resolve())
        return original_snapshot(root)

    monkeypatch.setattr(ownership.shutil, "copytree", copy_then_change_source)
    if original_snapshot is not None:
        monkeypatch.setattr(ownership, "_project_tree_snapshot", snapshot)

    with pytest.raises(RuntimeError, match="pre-install backup project-tree attestation mismatch") as caught:
        ownership.prepare_plugin_rollover_transaction(
            root=paths["state_root"], workspace=paths["workspace"],
            application_data=paths["app_data"],
            expected_replacement_fingerprint=expected,
            backup_token="task250-snapshot-delta",
        )

    message = str(caught.value)
    assert "runtime-state.txt" in message
    assert "source" in message and "backup" in message
    assert "sha256" in message
    assert len(calls) == 2
    assert "after-copy" not in message
    parsed = json.loads(message.split("diagnostic=", 1)[1])
    assert parsed["changedPaths"] == ["runtime-state.txt"]
    assert parsed["sourceTreeSha256"] != parsed["backupTreeSha256"]
    assert parsed["differences"][0]["source"]["sha256"] != parsed["differences"][0]["backup"]["sha256"]
