#!/usr/bin/env python3
"""Exact ownership, plugin-resolution, and migration inventory boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
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
ROLLOVER_PLAN_SCHEMA_VERSION = 1
ROLLOVER_PLAN_FIELDS = {
    "schemaVersion", "operation", "productId", "installedVersion",
    "workspace", "stateRoot", "openclawState", "applicationData",
    "controllerMode", "retiredPluginPath", "replacementPluginPath",
    "retiredProjectRoot", "replacementProjectRoot", "backupPath",
    "retiredFingerprint", "replacementFingerprint",
    "retiredWrapperSha256", "replacementWrapperSha256",
    "retiredWrapperProofSha256", "replacementWrapperProofSha256",
    "retiredProjectTreeSha256", "replacementProjectTreeSha256",
    "inventorySha256", "activeRegistration", "activeRegistrationSha256",
    "manifestBeforeSha256", "manifestAfter", "createdAt",
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


def _json_sha256(value: Any) -> str:
    return _sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8"))


def _managed_wrapper_proof(project: Path) -> dict[str, Any]:
    """Prove the exact OpenClaw-managed npm project wrapper for this product."""
    project_name = project.name
    generation_prefix = f"{PLUGIN_PACKAGE}__openclaw-generation__"
    if project_name != PLUGIN_PACKAGE and not (
        project_name.startswith(generation_prefix)
        and re.fullmatch(r"g-[a-f0-9]{16}", project_name[len(generation_prefix):])
    ):
        raise RuntimeError(f"managed npm wrapper ownership has an invalid project name: {project}")
    package_path = project / "package.json"
    lock_path = project / "package-lock.json"
    if not package_path.is_file() or not lock_path.is_file():
        raise RuntimeError(f"managed npm wrapper ownership requires package.json and package-lock.json: {project}")
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"managed npm wrapper ownership JSON is unreadable: {project}") from error
    allowed_package_fields = {"private", "dependencies", "overrides", "openclaw"}
    if not isinstance(package, dict) or not set(package).issubset(allowed_package_fields):
        raise RuntimeError(f"managed npm wrapper ownership has foreign package.json fields: {project}")
    dependencies = package.get("dependencies")
    if package.get("private") is not True or not isinstance(dependencies, dict):
        raise RuntimeError(f"managed npm wrapper ownership lacks private dependencies: {project}")
    if not all(isinstance(key, str) and isinstance(value, str) and value
               for key, value in dependencies.items()):
        raise RuntimeError(f"managed npm wrapper ownership has invalid dependency entries: {project}")
    dependency_spec = dependencies.get(PLUGIN_PACKAGE)
    if not isinstance(dependency_spec, str) or not dependency_spec:
        raise RuntimeError(f"managed npm wrapper ownership does not bind {PLUGIN_PACKAGE}: {project}")
    metadata = package.get("openclaw", {})
    if not isinstance(metadata, dict) or not set(metadata).issubset(
        {"managedPeerDependencies", "managedOverrides"}
    ):
        raise RuntimeError(f"managed npm wrapper ownership has foreign OpenClaw metadata: {project}")
    managed_peers = metadata.get("managedPeerDependencies", [])
    managed_overrides = metadata.get("managedOverrides", [])
    if not (isinstance(managed_peers, list) and len(managed_peers) == len(set(managed_peers))
            and all(isinstance(item, str) and item for item in managed_peers)):
        raise RuntimeError(f"managed npm wrapper ownership has invalid managed peers: {project}")
    if not (isinstance(managed_overrides, list)
            and len(managed_overrides) == len(set(managed_overrides))
            and all(isinstance(item, str) and item for item in managed_overrides)):
        raise RuntimeError(f"managed npm wrapper ownership has invalid managed overrides: {project}")
    if set(dependencies) - {PLUGIN_PACKAGE} != set(managed_peers):
        raise RuntimeError(f"managed npm wrapper ownership includes undeclared dependencies: {project}")
    overrides = package.get("overrides", {})
    if not isinstance(overrides, dict) or set(overrides) != set(managed_overrides):
        raise RuntimeError(f"managed npm wrapper ownership overrides are not OpenClaw-declared: {project}")
    packages = lock.get("packages") if isinstance(lock, dict) else None
    lock_root = packages.get("") if isinstance(packages, dict) else None
    lock_dependencies = lock_root.get("dependencies") if isinstance(lock_root, dict) else None
    installed = packages.get(f"node_modules/{PLUGIN_PACKAGE}") if isinstance(packages, dict) else None
    if lock_dependencies != dependencies or not isinstance(installed, dict) \
            or installed.get("version") != INSTALLED_VERSION:
        raise RuntimeError(f"managed npm wrapper ownership lockfile does not bind the exact package/version: {project}")
    proof = {
        "projectName": project_name,
        "dependencySpec": dependency_spec,
        "managedPeerDependencies": sorted(managed_peers),
        "managedOverrides": sorted(managed_overrides),
        "packageJsonSha256": _sha256_file(package_path),
        "packageLockSha256": _sha256_file(lock_path),
    }
    return proof


def _wrapper_identifies_product(project: Path) -> bool:
    """Detect possible product evidence for inventory; never authorizes mutation."""
    package_path = project / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    dependencies = package.get("dependencies") if isinstance(package, dict) else None
    return isinstance(dependencies, dict) and PLUGIN_PACKAGE in dependencies


def _project_tree_sha256(root: Path) -> str:
    """Hash an exact tree without following symlinks or Windows junctions."""
    entries: list[dict[str, Any]] = []

    def visit(directory: Path) -> None:
        with os.scandir(directory) as iterator:
            children = sorted(iterator, key=lambda item: item.name)
        for child in children:
            child_path = Path(child.path)
            relative = child_path.relative_to(root).as_posix()
            is_junction = bool(getattr(os.path, "isjunction", lambda _path: False)(child.path))
            if child.is_symlink() or is_junction:
                entries.append({
                    "path": relative,
                    "type": "junction" if is_junction else "symlink",
                    "target": os.readlink(child.path),
                })
            elif child.is_dir(follow_symlinks=False):
                entries.append({"path": relative, "type": "directory"})
                visit(child_path)
            elif child.is_file(follow_symlinks=False):
                entries.append({
                    "path": relative,
                    "type": "file",
                    "size": child.stat(follow_symlinks=False).st_size,
                    "sha256": _sha256_file(child_path),
                })
            else:
                raise RuntimeError(f"managed npm project has an unsupported filesystem entry: {child_path}")

    visit(root)
    return _json_sha256(entries)


def product_plugin_inventory(openclaw_state: Path) -> dict[str, Path]:
    """Inventory product evidence without treating unrelated npm projects as ours."""
    items: dict[str, Path] = {}
    direct = openclaw_state / "extensions" / PRODUCT_ID
    if direct.exists():
        items["directPlugin"] = direct
    projects = openclaw_state / "npm" / "projects"
    if not projects.is_dir():
        return items
    for project in sorted((item for item in projects.iterdir() if item.is_dir()), key=lambda item: item.name):
        child = project / "node_modules" / PLUGIN_PACKAGE
        if child.exists():
            items[f"npmPackage:{project.name}"] = child
        if _wrapper_identifies_product(project):
            items[f"npmWrapper:{project.name}"] = project
    return items


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


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_bytes_atomic(target: Path, value: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_bytes(value)
    temporary.replace(target)


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


def _require_passthrough(root: Path) -> str:
    controller_path = root / "host" / "controller.json"
    try:
        controller = json.loads(controller_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"CogentNexus-OpenClaw controller is missing or unreadable: {controller_path}") from error
    mode = controller.get("mode") if isinstance(controller, dict) else None
    if mode != "passthrough":
        raise RuntimeError(f"plugin generation rollover requires PASSTHROUGH mode; observed {mode!r}")
    return mode


def _npm_project_for_plugin(plugin_path: Path, openclaw_state: Path) -> Path:
    projects = (openclaw_state / "npm" / "projects").resolve(strict=False)
    plugin_path = plugin_path.resolve(strict=False)
    try:
        relative = plugin_path.relative_to(projects)
    except ValueError as error:
        raise RuntimeError(f"plugin is not inside the managed npm projects boundary: {plugin_path}") from error
    parts = relative.parts
    if len(parts) != 3 or parts[1] != "node_modules" or parts[2] != PLUGIN_PACKAGE:
        raise RuntimeError(f"plugin is not an exact isolated managed npm payload: {plugin_path}")
    project = projects / parts[0]
    if not project.is_dir():
        raise RuntimeError(f"managed npm wrapper ownership is unproven: {project}")
    _managed_wrapper_proof(project)
    return project


def _active_registered_plugin(plugin_inventory: dict[str, Any], openclaw_state: Path) -> dict[str, Any]:
    if not isinstance(plugin_inventory, dict) or not isinstance(plugin_inventory.get("plugins"), list):
        raise RuntimeError("OpenClaw plugin inventory JSON has no plugins array")
    records = [item for item in plugin_inventory["plugins"]
               if isinstance(item, dict) and item.get("id") == PRODUCT_ID]
    if len(records) != 1:
        raise RuntimeError(f"OpenClaw active canonical registration is not unique ({len(records)})")
    record = records[0]
    version = record.get("version") or record.get("packageVersion")
    if record.get("packageName") != PLUGIN_PACKAGE or version != INSTALLED_VERSION:
        raise RuntimeError("OpenClaw active canonical registration package/version is unproven")
    root_text = record.get("rootDir")
    if not isinstance(root_text, str) or not root_text.strip():
        raise RuntimeError("OpenClaw active canonical registration has no rootDir")
    active_root = Path(root_text).resolve(strict=False)
    if not _contained(active_root, openclaw_state):
        raise RuntimeError(f"OpenClaw active canonical registration is outside its state boundary: {active_root}")
    payload = _plugin_payload(active_root)
    if payload is None:
        raise RuntimeError(f"OpenClaw active canonical registration payload is not exact: {active_root}")
    registration = {
        "id": record.get("id"),
        "packageName": record.get("packageName"),
        "version": version,
        "rootDir": _canonical(active_root),
        "source": record.get("source"),
        "enabled": record.get("enabled"),
        "status": record.get("status"),
    }
    return {
        "record": record,
        "registration": registration,
        "registrationSha256": _json_sha256(registration),
        **payload,
    }


def _exact_rollover_state(*, root: Path, workspace: Path,
                          plugin_inventory: dict[str, Any]) -> dict[str, Any]:
    paths = expected_paths(workspace)
    mode = _require_passthrough(root)
    manifest = verify_manifest(root, workspace=workspace, verify_plugin=False)
    retired_root = Path(manifest["pluginPath"]).resolve(strict=False)
    retired = _plugin_payload(retired_root)
    if retired is None:
        raise RuntimeError(f"manifest-owned prior plugin payload is not exact: {retired_root}")
    candidates = [payload for candidate in plugin_candidate_roots(paths["openclawState"])
                  if (payload := _plugin_payload(candidate)) is not None]
    if len(candidates) != 2:
        raise RuntimeError(f"rollover requires exactly two canonical payload candidates; observed {len(candidates)}")
    candidate_keys = {_canonical(item["root"]) for item in candidates}
    if _canonical(retired_root) not in candidate_keys:
        raise RuntimeError("manifest-owned prior plugin is not one of the two canonical candidates")
    replacement = _active_registered_plugin(plugin_inventory, paths["openclawState"])
    if _canonical(replacement["root"]) not in candidate_keys:
        raise RuntimeError("OpenClaw active replacement is not one of the two canonical candidates")
    if _canonical(replacement["root"]) == _canonical(retired_root):
        raise RuntimeError("OpenClaw still registers the manifest-owned prior generation as active")
    if replacement["fingerprint"] != retired["fingerprint"]:
        raise RuntimeError("replacement payload conflicts with the manifest-owned same-version payload")
    retired_project = _npm_project_for_plugin(retired_root, paths["openclawState"])
    replacement_project = _npm_project_for_plugin(replacement["root"], paths["openclawState"])
    if _canonical(retired_project) == _canonical(replacement_project):
        raise RuntimeError("retired and replacement payloads unexpectedly share one npm project")
    return {
        "paths": paths,
        "mode": mode,
        "manifest": manifest,
        "retired": retired,
        "replacement": replacement,
        "retiredProject": retired_project,
        "replacementProject": replacement_project,
        "retiredWrapperProof": _managed_wrapper_proof(retired_project),
        "replacementWrapperProof": _managed_wrapper_proof(replacement_project),
        "inventorySha256": _json_sha256(plugin_inventory),
    }


def build_plugin_rollover_plan(*, root: Path, workspace: Path, application_data: Path,
                               plugin_inventory: dict[str, Any],
                               backup_token: str | None = None) -> dict[str, Any]:
    root = root.resolve(strict=False)
    workspace = workspace.resolve(strict=False)
    application_data = application_data.resolve(strict=False)
    state = _exact_rollover_state(
        root=root, workspace=workspace, plugin_inventory=plugin_inventory,
    )
    if application_data.name.lower() != DISPLAY_NAME.lower() or _contained(
        application_data, state["paths"]["openclawState"]
    ):
        raise RuntimeError(
            "rollover application-data root must be the external CogentNexus-OpenClaw boundary"
        )
    token = backup_token or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if not token or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for character in token):
        raise RuntimeError("rollover backup token contains unsafe characters")
    backup_path = (application_data / "plugin-generation-rollover-backups" /
                   f"{state['retiredProject'].name}-{token}").resolve(strict=False)
    if backup_path.exists():
        raise RuntimeError(f"rollover backup destination already exists: {backup_path}")
    manifest_target = manifest_path(root)
    manifest_after = dict(state["manifest"])
    manifest_after["pluginPath"] = _canonical(state["replacement"]["root"])
    manifest_after["installedAt"] = datetime.now(timezone.utc).isoformat()
    return {
        "schemaVersion": ROLLOVER_PLAN_SCHEMA_VERSION,
        "operation": "cogentnexus-openclaw-plugin-generation-rollover",
        "productId": PRODUCT_ID,
        "installedVersion": INSTALLED_VERSION,
        "workspace": _canonical(workspace),
        "stateRoot": _canonical(root),
        "openclawState": _canonical(state["paths"]["openclawState"]),
        "applicationData": _canonical(application_data),
        "controllerMode": state["mode"],
        "retiredPluginPath": _canonical(state["retired"]["root"]),
        "replacementPluginPath": _canonical(state["replacement"]["root"]),
        "retiredProjectRoot": _canonical(state["retiredProject"]),
        "replacementProjectRoot": _canonical(state["replacementProject"]),
        "backupPath": _canonical(backup_path),
        "retiredFingerprint": state["retired"]["fingerprint"],
        "replacementFingerprint": state["replacement"]["fingerprint"],
        "retiredWrapperSha256": _sha256_file(state["retiredProject"] / "package.json"),
        "replacementWrapperSha256": _sha256_file(state["replacementProject"] / "package.json"),
        "retiredWrapperProofSha256": _json_sha256(state["retiredWrapperProof"]),
        "replacementWrapperProofSha256": _json_sha256(state["replacementWrapperProof"]),
        "retiredProjectTreeSha256": _project_tree_sha256(state["retiredProject"]),
        "replacementProjectTreeSha256": _project_tree_sha256(state["replacementProject"]),
        "inventorySha256": state["inventorySha256"],
        "activeRegistration": state["replacement"]["registration"],
        "activeRegistrationSha256": state["replacement"]["registrationSha256"],
        "manifestBeforeSha256": _sha256_file(manifest_target),
        "manifestAfter": manifest_after,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }


def write_plugin_rollover_plan(plan_path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or set(plan) != ROLLOVER_PLAN_FIELDS:
        raise RuntimeError("plugin rollover plan schema fields are not exact")
    content = json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    _write_bytes_atomic(plan_path, content)
    return {"planPath": str(plan_path.resolve(strict=False)), "planSha256": _sha256_bytes(content)}


def _validate_rollover_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict) or set(plan) != ROLLOVER_PLAN_FIELDS:
        raise RuntimeError("plugin rollover plan schema fields are not exact")
    expected = {
        "schemaVersion": ROLLOVER_PLAN_SCHEMA_VERSION,
        "operation": "cogentnexus-openclaw-plugin-generation-rollover",
        "productId": PRODUCT_ID,
        "installedVersion": INSTALLED_VERSION,
        "controllerMode": "passthrough",
    }
    mismatches = {key: {"expected": value, "actual": plan.get(key)}
                  for key, value in expected.items() if plan.get(key) != value}
    if mismatches:
        raise RuntimeError(f"plugin rollover plan identity mismatch: {json.dumps(mismatches, sort_keys=True)}")


def apply_plugin_rollover_plan(*, plan_path: Path, expected_plan_sha256: str,
                               plugin_inventory: dict[str, Any]) -> dict[str, Any]:
    plan_bytes = plan_path.read_bytes()
    actual_plan_sha256 = _sha256_bytes(plan_bytes)
    if not isinstance(expected_plan_sha256, str) or actual_plan_sha256.lower() != expected_plan_sha256.lower():
        raise RuntimeError(f"plugin rollover plan hash mismatch; expected {expected_plan_sha256}, actual {actual_plan_sha256}")
    try:
        plan = json.loads(plan_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("plugin rollover plan is not valid UTF-8 JSON") from error
    _validate_rollover_plan(plan)
    root = Path(plan["stateRoot"]).resolve(strict=False)
    workspace = Path(plan["workspace"]).resolve(strict=False)
    application_data = Path(plan["applicationData"]).resolve(strict=False)
    if _canonical(expected_paths(workspace)["openclawState"]) != plan["openclawState"]:
        raise RuntimeError("plugin rollover plan OpenClaw state binding is invalid")
    if application_data.name.lower() != DISPLAY_NAME.lower() or _contained(
        application_data, Path(plan["openclawState"])
    ):
        raise RuntimeError("plugin rollover plan application-data boundary is invalid")
    backup_path = Path(plan["backupPath"]).resolve(strict=False)
    backup_root = (application_data / "plugin-generation-rollover-backups").resolve(strict=False)
    if not _contained(backup_path, backup_root) or _canonical(backup_path) == _canonical(backup_root):
        raise RuntimeError("plugin rollover backup destination is outside the exact product backup boundary")
    if backup_path.exists():
        raise RuntimeError(f"plugin rollover backup destination already exists: {backup_path}")
    manifest_target = manifest_path(root)
    manifest_before = manifest_target.read_bytes()
    if _sha256_bytes(manifest_before) != plan["manifestBeforeSha256"]:
        raise RuntimeError("ownership manifest changed after rollover plan review")
    current_inventory_sha256 = _json_sha256(plugin_inventory)
    if current_inventory_sha256 != plan["inventorySha256"]:
        raise RuntimeError(
            "OpenClaw plugin inventory changed after rollover plan review; refusing retirement"
        )
    state = _exact_rollover_state(
        root=root, workspace=workspace, plugin_inventory=plugin_inventory,
    )
    exact_bindings = {
        "retiredPluginPath": _canonical(state["retired"]["root"]),
        "replacementPluginPath": _canonical(state["replacement"]["root"]),
        "retiredProjectRoot": _canonical(state["retiredProject"]),
        "replacementProjectRoot": _canonical(state["replacementProject"]),
        "retiredFingerprint": state["retired"]["fingerprint"],
        "replacementFingerprint": state["replacement"]["fingerprint"],
        "retiredWrapperSha256": _sha256_file(state["retiredProject"] / "package.json"),
        "replacementWrapperSha256": _sha256_file(state["replacementProject"] / "package.json"),
        "retiredWrapperProofSha256": _json_sha256(state["retiredWrapperProof"]),
        "replacementWrapperProofSha256": _json_sha256(state["replacementWrapperProof"]),
        "retiredProjectTreeSha256": _project_tree_sha256(state["retiredProject"]),
        "replacementProjectTreeSha256": _project_tree_sha256(state["replacementProject"]),
        "inventorySha256": state["inventorySha256"],
        "activeRegistration": state["replacement"]["registration"],
        "activeRegistrationSha256": state["replacement"]["registrationSha256"],
    }
    mismatches = {key: {"planned": plan.get(key), "actual": value}
                  for key, value in exact_bindings.items() if plan.get(key) != value}
    if mismatches:
        raise RuntimeError(f"plugin rollover state changed after plan review: {json.dumps(mismatches, sort_keys=True)}")
    if plan.get("manifestAfter", {}).get("pluginPath") != plan["replacementPluginPath"]:
        raise RuntimeError("plugin rollover replacement is not bound to the planned ownership manifest")
    retired_project = state["retiredProject"]
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if os.stat(retired_project).st_dev != os.stat(backup_path.parent).st_dev:
        raise RuntimeError(
            "plugin rollover requires a same-volume atomic rename; refusing cross-filesystem retirement"
        )
    try:
        os.replace(retired_project, backup_path)
    except Exception as error:
        raise RuntimeError(f"plugin rollover failed before retirement: {error}") from error
    try:
        if retired_project.exists() or not backup_path.is_dir():
            raise RuntimeError("atomic retirement did not produce the exact source/backup state")
        if _project_tree_sha256(backup_path) != plan["retiredProjectTreeSha256"]:
            raise RuntimeError("retired project backup tree does not match the reviewed plan")
        write_manifest(root, plan["manifestAfter"])
        verified = verify_manifest(root, workspace=workspace)
        if _canonical(Path(verified["pluginPath"])) != plan["replacementPluginPath"]:
            raise RuntimeError("final ownership manifest does not bind the replacement plugin")
        _require_passthrough(root)
    except Exception as error:
        rollback_errors: list[str] = []
        try:
            if retired_project.exists():
                raise RuntimeError(f"retired project path unexpectedly exists during rollback: {retired_project}")
            retired_project.parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup_path, retired_project)
            if _project_tree_sha256(retired_project) != plan["retiredProjectTreeSha256"]:
                raise RuntimeError("restored project tree does not match the reviewed plan")
        except Exception as rollback_error:
            rollback_errors.append(f"project restore failed: {rollback_error}")
        try:
            _write_bytes_atomic(manifest_target, manifest_before)
        except Exception as rollback_error:
            rollback_errors.append(f"manifest restore failed: {rollback_error}")
        if rollback_errors:
            raise RuntimeError(
                f"plugin rollover failed and rollback is incomplete: {error}; {'; '.join(rollback_errors)}"
            ) from error
        raise RuntimeError(f"plugin rollover failed; rollback complete: {error}") from error
    return {
        "status": "ROLLOVER_APPLIED_PASSTHROUGH",
        "planSha256": actual_plan_sha256,
        "backupPath": str(backup_path),
        "pluginPath": plan["replacementPluginPath"],
    }


def current_inventory(workspace: Path, *, app_data: Path | None = None) -> dict[str, list[str]]:
    paths = expected_paths(workspace)
    app_root = app_data or paths["applicationData"]
    new_items: dict[str, Path] = {
        "launcherWindows": paths["launchers"][0], "launcherPosix": paths["launchers"][1],
        "skill": paths["skillPath"], "state": paths["stateRoot"], "applicationData": app_root,
    }
    new_items.update(product_plugin_inventory(paths["openclawState"]))
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


def require_skip_plugin_safe(mode: str) -> dict[str, str]:
    if mode != "upgrade":
        raise RuntimeError("skip-plugin requires a coherent upgrade with an existing exact v0.9.3 plugin")
    return {"mode": mode, "skipPlugin": "allowed-existing-exact-plugin"}


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
    rollover_plan = sub.add_parser("rollover-plan")
    rollover_plan.add_argument("--root", type=Path, required=True)
    rollover_plan.add_argument("--workspace", type=Path, required=True)
    rollover_plan.add_argument("--app-data", type=Path, required=True)
    rollover_plan.add_argument("--inventory-json", type=Path, required=True)
    rollover_plan.add_argument("--plan", type=Path, required=True)
    rollover_apply = sub.add_parser("rollover-apply")
    rollover_apply.add_argument("--plan", type=Path, required=True)
    rollover_apply.add_argument("--plan-sha256", required=True)
    rollover_apply.add_argument("--inventory-json", type=Path, required=True)
    skip = sub.add_parser("preflight-skip-plugin")
    skip.add_argument("--mode", required=True)
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
    elif args.command == "rollover-plan":
        plugin_inventory = json.loads(args.inventory_json.read_text(encoding="utf-8"))
        plan = build_plugin_rollover_plan(
            root=args.root, workspace=args.workspace, application_data=args.app_data,
            plugin_inventory=plugin_inventory,
        )
        result = {**write_plugin_rollover_plan(args.plan, plan), "plan": plan}
    elif args.command == "rollover-apply":
        plugin_inventory = json.loads(args.inventory_json.read_text(encoding="utf-8"))
        result = apply_plugin_rollover_plan(
            plan_path=args.plan, expected_plan_sha256=args.plan_sha256,
            plugin_inventory=plugin_inventory,
        )
    elif args.command == "preflight-skip-plugin":
        result = require_skip_plugin_safe(args.mode)
    else:
        result = build_manifest(root=args.root, workspace=args.workspace, skill=args.skill,
                                plugin_path=args.plugin_path, launcher=args.launcher,
                                version=args.version, migration_source=args.migration_source)
        write_manifest(args.root, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
