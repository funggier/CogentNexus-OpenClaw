#!/usr/bin/env python3
"""Fail-closed ownership and legacy-migration primitives for CogentNexus-OpenClaw."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRODUCT_ID = "cogentnexus-openclaw"
DISPLAY_NAME = "CogentNexus-OpenClaw"
SCHEMA_VERSION = 1
MANIFEST_NAME = "ownership.json"
LEGACY_PLUGIN_ID = "cogentnexus-rotation"


def _canonical(path: Path) -> str:
    return os.path.normcase(str(path.expanduser().resolve()))


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_NAME


def build_manifest(
    *, root: Path, workspace: Path, skill: Path, plugin_path: Path,
    launcher: Path, version: str, task_services: list[str] | None = None,
    migration_source: str | None = None,
) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "productId": PRODUCT_ID,
        "displayName": DISPLAY_NAME,
        "installedVersion": version,
        "workspace": _canonical(workspace),
        "stateRoot": _canonical(root),
        "skillPath": _canonical(skill),
        "pluginId": PRODUCT_ID,
        "pluginPath": _canonical(plugin_path),
        "launcherPath": _canonical(launcher),
        "taskServiceIdentities": list(task_services or [
            "CogentNexus-OpenClaw-Supervisor",
            "cogentnexus-openclaw-supervisor",
            "ai.cogentnexus.openclaw.supervisor",
        ]),
        "installedAt": datetime.now(timezone.utc).isoformat(),
        "migrationSource": migration_source,
    }


def write_manifest(root: Path, payload: dict[str, Any]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    target = manifest_path(root)
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    return target


def verify_manifest(root: Path, *, workspace: Path | None = None) -> dict[str, Any]:
    target = manifest_path(root)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"ownership manifest is missing or unreadable: {target}: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("ownership manifest must be a JSON object")
    expected = {
        "schemaVersion": SCHEMA_VERSION,
        "productId": PRODUCT_ID,
        "displayName": DISPLAY_NAME,
        "pluginId": PRODUCT_ID,
        "stateRoot": _canonical(root),
    }
    if workspace is not None:
        expected["workspace"] = _canonical(workspace)
    mismatches = {key: {"expected": value, "actual": payload.get(key)} for key, value in expected.items() if payload.get(key) != value}
    if mismatches:
        raise RuntimeError(f"ownership manifest mismatch; refusing mutation: {json.dumps(mismatches, sort_keys=True)}")
    for field in ("installedVersion", "skillPath", "pluginPath", "launcherPath", "installedAt"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise RuntimeError(f"ownership manifest lacks required field: {field}")
    return payload


def legacy_inventory(workspace: Path, openclaw_state: Path | None = None) -> dict[str, Any]:
    state = openclaw_state or workspace.parent
    paths = {
        "launcherWindows": workspace / "cnx.cmd",
        "launcherPosix": workspace / "cnx",
        "skill": workspace / "skills" / "cogentnexus",
        "state": workspace / ".cogent",
        "plugin": state / "extensions" / LEGACY_PLUGIN_ID,
    }
    new_paths = [workspace / "cnxclaw.cmd", workspace / "cnxclaw", workspace / "skills" / PRODUCT_ID, workspace / ".cogentnexus-openclaw"]
    return {
        "legacy": {name: str(path) for name, path in paths.items() if path.exists()},
        "new": [str(path) for path in new_paths if path.exists()],
    }


def prove_legacy_ownership(workspace: Path, openclaw_state: Path | None = None) -> dict[str, Any]:
    inventory = legacy_inventory(workspace, openclaw_state)
    if inventory["new"] and inventory["legacy"]:
        raise RuntimeError("mixed legacy/new namespace is ambiguous; refusing migration")
    if not inventory["legacy"]:
        return {"mode": "fresh", "evidence": [], **inventory}
    evidence: list[str] = []
    skill = workspace / "skills" / "cogentnexus" / "SKILL.md"
    if skill.is_file() and "CogentNexus" in skill.read_text(encoding="utf-8", errors="replace"):
        evidence.append("legacy-skill-metadata")
    state = workspace / ".cogent"
    legacy_mode: str | None = None
    if (state / "host" / "controller.json").is_file():
        try:
            controller = json.loads((state / "host" / "controller.json").read_text(encoding="utf-8"))
            legacy_mode = controller.get("mode") if isinstance(controller, dict) else None
        except json.JSONDecodeError as error:
            raise RuntimeError(f"legacy controller is corrupted; refusing migration: {error}") from error
        if legacy_mode not in {"passthrough", "managed", "maintenance"}:
            raise RuntimeError(f"legacy controller mode is ambiguous ({legacy_mode!r}); refusing migration")
        evidence.append("legacy-controller-structure")
    plugin = (openclaw_state or workspace.parent) / "extensions" / LEGACY_PLUGIN_ID / "openclaw.plugin.json"
    if plugin.is_file():
        try:
            if json.loads(plugin.read_text(encoding="utf-8")).get("id") == LEGACY_PLUGIN_ID:
                evidence.append("legacy-plugin-id")
        except json.JSONDecodeError:
            pass
    launchers = [workspace / "cnx.cmd", workspace / "cnx"]
    if any(path.is_file() and ".cogent" in path.read_text(encoding="utf-8", errors="replace") for path in launchers):
        evidence.append("legacy-launcher-content")
    if len(evidence) < 3:
        raise RuntimeError(f"legacy ownership is unproven ({len(evidence)}/3 identities); refusing migration")
    return {"mode": "legacy", "legacyMode": legacy_mode, "evidence": evidence, **inventory}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--root", type=Path, required=True)
    verify.add_argument("--workspace", type=Path, required=True)
    inventory = sub.add_parser("inventory-legacy")
    inventory.add_argument("--workspace", type=Path, required=True)
    create = sub.add_parser("create")
    for name in ("root", "workspace", "skill", "plugin-path", "launcher"):
        create.add_argument(f"--{name}", type=Path, required=True)
    create.add_argument("--version", required=True)
    create.add_argument("--migration-source")
    args = parser.parse_args()
    if args.command == "verify":
        result = verify_manifest(args.root, workspace=args.workspace)
    elif args.command == "inventory-legacy":
        result = prove_legacy_ownership(args.workspace)
    else:
        result = build_manifest(root=args.root, workspace=args.workspace, skill=args.skill,
                                plugin_path=args.plugin_path, launcher=args.launcher,
                                version=args.version, migration_source=args.migration_source)
        write_manifest(args.root, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
