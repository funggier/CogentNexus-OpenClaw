#!/usr/bin/env python3
"""Exact ownership, plugin-resolution, and migration inventory boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRODUCT_ID = "cogentnexus-openclaw"
DISPLAY_NAME = "CogentNexus-OpenClaw"
INSTALLED_VERSION = "0.9.3"
SCHEMA_VERSION = 1
MANIFEST_NAME = "ownership.json"
PLUGIN_PACKAGE = "openclaw-plugin-cogentnexus-openclaw"
LEGACY_PLUGIN_ID = "cogentnexus-rotation"
LEGACY_MIGRATION_SOURCE = "legacy-cogentnexus-pre-v0.9.3"
TASK_SERVICE_IDENTITIES = (
    "CogentNexus-OpenClaw-Supervisor",
    "cogentnexus-openclaw-supervisor",
    "ai.cogentnexus.openclaw.supervisor",
)
MANIFEST_FIELDS = {
    "schemaVersion", "productId", "displayName", "installedVersion",
    "workspace", "stateRoot", "skillPath", "pluginId", "pluginPath",
    "launcherPath", "taskServiceIdentities", "installedAt", "migrationSource",
}


def _canonical(path: Path) -> str:
    return os.path.normcase(str(path.expanduser().resolve(strict=False)))


def _contained(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def expected_paths(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(strict=False)
    state = workspace.parent
    return {
        "workspace": workspace,
        "stateRoot": workspace / ".cogentnexus-openclaw",
        "skillPath": workspace / "skills" / PRODUCT_ID,
        "launchers": (workspace / "cnxclaw.cmd", workspace / "cnxclaw"),
        "openclawState": state,
        "applicationData": Path(os.environ.get("LOCALAPPDATA", state / ".local-data")) / DISPLAY_NAME,
    }


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_NAME


def _plugin_payload(root: Path, *, expected_version: str = INSTALLED_VERSION) -> dict[str, Any] | None:
    files = [root / "openclaw.plugin.json", root / "package.json",
             root / "scripts" / "bootstrap-ticket-db.mjs", root / "dist" / "ticket-store.js"]
    if not all(path.is_file() for path in files):
        return None
    try:
        manifest = json.loads(files[0].read_text(encoding="utf-8"))
        package = json.loads(files[1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if manifest.get("id") != PRODUCT_ID or manifest.get("version") != expected_version:
        return None
    if package.get("name") != PLUGIN_PACKAGE or package.get("version") != expected_version:
        return None
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {"root": root.resolve(strict=False), "fingerprint": digest.hexdigest(), "version": expected_version}


def plugin_candidate_roots(openclaw_state: Path) -> list[Path]:
    roots = [openclaw_state / "extensions" / PRODUCT_ID]
    projects = openclaw_state / "npm" / "projects"
    if projects.is_dir():
        for project in sorted((item for item in projects.iterdir() if item.is_dir()), key=lambda item: item.name):
            roots.extend((project, project / "node_modules" / PLUGIN_PACKAGE))
    result: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = _canonical(root)
        if key not in seen:
            seen.add(key)
            result.append(root)
    return result


def resolve_installed_plugin(openclaw_state: Path, *, expected_version: str = INSTALLED_VERSION) -> dict[str, Any]:
    candidates = [payload for root in plugin_candidate_roots(openclaw_state)
                  if (payload := _plugin_payload(root, expected_version=expected_version)) is not None]
    if not candidates:
        raise RuntimeError("no exact installed CogentNexus-OpenClaw plugin payload was found")
    if len(candidates) != 1:
        details = [{"root": str(item["root"]), "fingerprint": item["fingerprint"]} for item in candidates]
        raise RuntimeError(f"installed plugin path is ambiguous; refusing ownership: {json.dumps(details, sort_keys=True)}")
    return candidates[0]


def build_manifest(*, root: Path, workspace: Path, skill: Path, plugin_path: Path,
                   launcher: Path, version: str, task_services: list[str] | None = None,
                   migration_source: str | None = None) -> dict[str, Any]:
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
        "taskServiceIdentities": list(task_services or TASK_SERVICE_IDENTITIES),
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


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise RuntimeError("ownership manifest installedAt must be an ISO-8601 UTC string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise RuntimeError("ownership manifest installedAt is not parseable") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise RuntimeError("ownership manifest installedAt must use UTC")
    return parsed


def verify_manifest(root: Path, *, workspace: Path, require_artifacts: bool = True,
                    verify_plugin: bool = True) -> dict[str, Any]:
    target = manifest_path(root)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"ownership manifest is missing or unreadable: {target}: {error}") from error
    if not isinstance(payload, dict) or set(payload) != MANIFEST_FIELDS:
        raise RuntimeError("ownership manifest schema fields are not exact; refusing mutation")
    paths = expected_paths(workspace)
    launchers = {_canonical(item) for item in paths["launchers"]}
    expected = {
        "schemaVersion": SCHEMA_VERSION, "productId": PRODUCT_ID,
        "displayName": DISPLAY_NAME, "installedVersion": INSTALLED_VERSION,
        "workspace": _canonical(paths["workspace"]), "stateRoot": _canonical(paths["stateRoot"]),
        "skillPath": _canonical(paths["skillPath"]), "pluginId": PRODUCT_ID,
        "taskServiceIdentities": list(TASK_SERVICE_IDENTITIES),
    }
    mismatches = {key: {"expected": value, "actual": payload.get(key)}
                  for key, value in expected.items() if payload.get(key) != value}
    if _canonical(root) != _canonical(paths["stateRoot"]):
        mismatches["rootArgument"] = {"expected": _canonical(paths["stateRoot"]), "actual": _canonical(root)}
    if payload.get("launcherPath") not in launchers:
        mismatches["launcherPath"] = {"expected": sorted(launchers), "actual": payload.get("launcherPath")}
    plugin_text = payload.get("pluginPath")
    if not isinstance(plugin_text, str) or not _contained(Path(plugin_text), paths["openclawState"]):
        mismatches["pluginPath"] = {"expected": f"contained by {_canonical(paths['openclawState'])}", "actual": plugin_text}
    if payload.get("migrationSource") not in {None, LEGACY_MIGRATION_SOURCE}:
        mismatches["migrationSource"] = {"expected": [None, LEGACY_MIGRATION_SOURCE], "actual": payload.get("migrationSource")}
    _parse_utc(payload.get("installedAt"))
    if mismatches:
        raise RuntimeError(f"ownership manifest mismatch; refusing mutation: {json.dumps(mismatches, sort_keys=True)}")
    if verify_plugin:
        actual = resolve_installed_plugin(paths["openclawState"], expected_version=INSTALLED_VERSION)
        if _canonical(actual["root"]) != plugin_text:
            raise RuntimeError(f"ownership manifest pluginPath does not match verified installed payload: {actual['root']}")
    if require_artifacts:
        required = [paths["stateRoot"], paths["skillPath"] / "SKILL.md", Path(payload["launcherPath"]), Path(payload["pluginPath"])]
        missing = [str(item) for item in required if not item.exists()]
        if missing:
            raise RuntimeError(f"owned installation is incomplete; refusing mutation: {missing}")
    return payload


def current_inventory(workspace: Path, *, app_data: Path | None = None) -> dict[str, list[str]]:
    paths = expected_paths(workspace)
    app_root = app_data or paths["applicationData"]
    new_items: dict[str, Path] = {
        "launcherWindows": paths["launchers"][0], "launcherPosix": paths["launchers"][1],
        "skill": paths["skillPath"], "state": paths["stateRoot"], "applicationData": app_root,
        "directPlugin": paths["openclawState"] / "extensions" / PRODUCT_ID,
    }
    for index, candidate in enumerate(plugin_candidate_roots(paths["openclawState"])):
        new_items[f"pluginCandidate{index}"] = candidate
    legacy_items = {
        "launcherWindows": workspace / "cnx.cmd", "launcherPosix": workspace / "cnx",
        "skill": workspace / "skills" / "cogentnexus", "state": workspace / ".cogent",
        "plugin": paths["openclawState"] / "extensions" / LEGACY_PLUGIN_ID,
    }
    return {
        "new": [f"{name}={path}" for name, path in new_items.items() if path.exists()],
        "legacy": [f"{name}={path}" for name, path in legacy_items.items() if path.exists()],
    }


def classify_install(workspace: Path, *, app_data: Path | None = None) -> dict[str, Any]:
    inventory = current_inventory(workspace, app_data=app_data)
    paths = expected_paths(workspace)
    if inventory["legacy"] and inventory["new"]:
        raise RuntimeError(f"mixed legacy/new namespace is ambiguous; refusing mutation: {inventory}")
    if inventory["new"]:
        verify_manifest(paths["stateRoot"], workspace=workspace)
        return {"mode": "upgrade", **inventory}
    if inventory["legacy"]:
        return prove_legacy_ownership(workspace, inventory=inventory)
    return {"mode": "fresh", **inventory}


def prove_legacy_ownership(workspace: Path, *, inventory: dict[str, list[str]] | None = None) -> dict[str, Any]:
    inventory = inventory or current_inventory(workspace)
    evidence: list[str] = []
    skill = workspace / "skills" / "cogentnexus" / "SKILL.md"
    if skill.is_file() and "CogentNexus" in skill.read_text(encoding="utf-8", errors="replace"):
        evidence.append("legacy-skill-metadata")
    controller_path = workspace / ".cogent" / "host" / "controller.json"
    legacy_mode: str | None = None
    if controller_path.is_file():
        try:
            controller = json.loads(controller_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise RuntimeError(f"legacy controller is corrupted; refusing migration: {error}") from error
        legacy_mode = controller.get("mode") if isinstance(controller, dict) else None
        if legacy_mode not in {"passthrough", "managed", "maintenance"}:
            raise RuntimeError(f"legacy controller mode is ambiguous ({legacy_mode!r}); refusing migration")
        evidence.append("legacy-controller-structure")
    plugin = workspace.parent / "extensions" / LEGACY_PLUGIN_ID / "openclaw.plugin.json"
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
    verify.add_argument("--root", type=Path, required=True); verify.add_argument("--workspace", type=Path, required=True)
    inventory = sub.add_parser("classify-install")
    inventory.add_argument("--workspace", type=Path, required=True); inventory.add_argument("--app-data", type=Path)
    resolver = sub.add_parser("resolve-plugin")
    resolver.add_argument("--openclaw-state", type=Path, required=True); resolver.add_argument("--version", default=INSTALLED_VERSION)
    create = sub.add_parser("create")
    for name in ("root", "workspace", "skill", "plugin-path", "launcher"):
        create.add_argument(f"--{name}", type=Path, required=True)
    create.add_argument("--version", required=True); create.add_argument("--migration-source")
    args = parser.parse_args()
    if args.command == "verify":
        result = verify_manifest(args.root, workspace=args.workspace)
    elif args.command == "classify-install":
        result = classify_install(args.workspace, app_data=args.app_data)
    elif args.command == "resolve-plugin":
        payload = resolve_installed_plugin(args.openclaw_state, expected_version=args.version)
        result = {"root": str(payload["root"]), "version": payload["version"], "fingerprint": payload["fingerprint"]}
    else:
        result = build_manifest(root=args.root, workspace=args.workspace, skill=args.skill,
                                plugin_path=args.plugin_path, launcher=args.launcher,
                                version=args.version, migration_source=args.migration_source)
        write_manifest(args.root, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
