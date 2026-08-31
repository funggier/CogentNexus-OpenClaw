import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("clean_reinstall_handoff", ROOT / "scripts/clean_reinstall_handoff.py")
assert SPEC and SPEC.loader
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)
OWNERSHIP_SPEC = importlib.util.spec_from_file_location(
    "handoff_namespace_ownership", ROOT / "skills/cogentnexus-openclaw/scripts/namespace_ownership.py"
)
assert OWNERSHIP_SPEC and OWNERSHIP_SPEC.loader
ownership = importlib.util.module_from_spec(OWNERSHIP_SPEC)
OWNERSHIP_SPEC.loader.exec_module(ownership)


def test_external_backup_does_not_create_active_application_data_residue(tmp_path: Path):
    app_data = tmp_path / "local" / "CogentNexus-OpenClaw"
    backup = tmp_path / "local" / "CogentNexus-OpenClaw-Clean-Reinstall-Backups" / "run"
    result = handoff.validate_backup_boundary(app_data, backup)
    backup.mkdir(parents=True)
    (backup / "ownership.json").write_bytes(b"backup-sentinel")
    assert result["boundary"] == "external"
    assert not app_data.exists()
    assert (backup / "ownership.json").read_bytes() == b"backup-sentinel"
    workspace = tmp_path / ".openclaw/workspace"
    assert ownership.classify_install(workspace, app_data=app_data)["mode"] == "fresh"


def test_backup_inside_active_application_data_is_rejected(tmp_path: Path):
    app_data = tmp_path / "CogentNexus-OpenClaw"
    with pytest.raises(RuntimeError, match="outside active"):
        handoff.validate_backup_boundary(app_data, app_data / "clean-reinstall-backups")


def test_reinstall_failure_preserves_backup_and_records_recovery(tmp_path: Path):
    backup = tmp_path / "backups/run"
    sentinel = backup / "state/ownership.json"
    sentinel.parent.mkdir(parents=True)
    sentinel.write_bytes(b"owned-state")
    report = handoff.write_recovery(backup, tmp_path / "workspace", "installer exit 17")
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert sentinel.read_bytes() == b"owned-state"
    assert payload["status"] == "REINSTALL_FAILED_BACKUP_PRESERVED"
    assert payload["error"] == "installer exit 17"
    assert payload["humanDecisionRequired"] is True
