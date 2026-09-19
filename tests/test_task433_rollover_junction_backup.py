from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
SPEC = importlib.util.spec_from_file_location("task433_ownership", SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def _make_windows_junction(link: Path, target: Path) -> None:
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"junction creation unavailable: {result.stdout} {result.stderr}")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows junction regression")
def test_task433_project_snapshot_detects_junction_without_following_target(tmp_path: Path):
    root = tmp_path / "project"
    target = tmp_path / "external-openclaw"
    root.mkdir()
    target.mkdir()
    (target / "external-only.txt").write_text("must-not-be-owned", encoding="utf-8")
    junction = root / "openclaw"
    _make_windows_junction(junction, target)

    snapshot = ownership._project_tree_snapshot(root)

    assert snapshot["entries"] == [{
        "path": "openclaw",
        "type": "junction",
        "target": os.readlink(junction),
    }]


@pytest.mark.skipif(sys.platform != "win32", reason="Windows junction regression")
def test_task433_rollover_copy_preserves_junction_and_exact_snapshot(tmp_path: Path):
    source = tmp_path / "source"
    backup = tmp_path / "backup"
    target = tmp_path / "external-openclaw"
    source.mkdir()
    target.mkdir()
    (source / "owned.txt").write_text("owned", encoding="utf-8")
    (target / "external-only.txt").write_text("peer", encoding="utf-8")
    junction = source / "node_modules" / "openclaw"
    junction.parent.mkdir()
    _make_windows_junction(junction, target)

    ownership._copy_project_tree_preserving_reparse_points(source, backup)

    backup_junction = backup / "node_modules" / "openclaw"
    assert ownership._is_reparse_point(backup_junction)
    assert os.readlink(backup_junction) == os.readlink(junction)
    assert ownership._project_tree_snapshot(source) == ownership._project_tree_snapshot(backup)
    assert not any(
        entry["path"].startswith("node_modules/openclaw/")
        for entry in ownership._project_tree_snapshot(backup)["entries"]
    )
