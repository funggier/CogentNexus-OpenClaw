"""CNX-20260826-068 P5 — exact-root deletion boundary.

Rollback/recovery must never walk upward past the exact CogentNexus-OpenClaw-owned
roots. A preexisting shared `<workspace>\\skills` directory must survive.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
_SPEC = importlib.util.spec_from_file_location("namespace_ownership_p5", SCRIPT)
assert _SPEC and _SPEC.loader
namespace_ownership = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(namespace_ownership)


def _residue(workspace: Path) -> None:
    paths = namespace_ownership.expected_paths(workspace)
    controller = paths["stateRoot"] / "host" / "controller.json"
    controller.parent.mkdir(parents=True, exist_ok=True)
    controller.write_text(json.dumps({"schemaVersion": 1, "mode": "passthrough"}), encoding="utf-8")
    skill = paths["skillPath"] / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("# CogentNexus-OpenClaw\n", encoding="utf-8")
    for path in (paths["stateRoot"] / "host", paths["stateRoot"], paths["skillPath"]):
        namespace_ownership.record_transaction_path(workspace, path)


def test_p5_shared_skills_parent_survives_rollback(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    skills_parent = workspace / "skills"
    skills_parent.mkdir()
    sibling = skills_parent / "unrelated-skill"
    sibling.mkdir()
    (sibling / "keep.txt").write_text("keep", encoding="utf-8")
    marker = workspace / ".cogentnexus-openclaw" / namespace_ownership.TRANSACTION_NAME
    marker.parent.mkdir(parents=True, exist_ok=True)
    namespace_ownership.begin_fresh_transaction(workspace)
    _residue(workspace)
    result = namespace_ownership.rollback_transaction(workspace, archive=False)
    assert result["errors"] == []
    assert not (workspace / "skills" / "cogentnexus-openclaw").exists(), "owned skill root must be removed"
    assert skills_parent.is_dir(), "shared parent <workspace>\\skills must survive rollback"
    assert (sibling / "keep.txt").read_text(encoding="utf-8") == "keep", "unrelated siblings untouched"


def test_p5b_recovery_preflight_preserves_shared_parent(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    skills_parent = workspace / "skills"
    skills_parent.mkdir()
    namespace_ownership.begin_fresh_transaction(workspace)
    _residue(workspace)
    result = namespace_ownership.recovery_preflight(workspace)
    assert result["status"] == "RECOVERED_FRESH"
    assert skills_parent.is_dir(), "shared parent <workspace>\\skills must survive recovery"
