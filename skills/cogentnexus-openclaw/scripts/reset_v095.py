#!/usr/bin/env python3
"""Provider-neutral destructive lifecycle boundary for CogentNexus-OpenClaw v0.9.5.

This boundary owns only OpenClaw bridge installation/state reconstruction. OpenClaw
remains the sole provider/model/auth/routing authority. The only route operation
here is restoring the native OpenClaw route as a safety boundary; this module
never selects, starts, stops, probes, or commits a provider route.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import lifecycle_v091 as base
import namespace_ownership
import openclaw_route_v092 as openclaw_route
import openclaw_runtime_boundary_v092 as runtime_boundary
import supervisor_quiescence

HERE = Path(__file__).resolve()
HOST = HERE.with_name("host_provider_v092.py")
BOOTSTRAP_RELATIVE = Path("scripts") / "bootstrap-ticket-db.mjs"
TICKET_STORE_RELATIVE = Path("dist") / "ticket-store.js"
PLUGIN_ID = base.PLUGIN_ID
PLUGIN_PACKAGE = "openclaw-plugin-cogentnexus-openclaw"
HOST_COMMAND_TIMEOUT_SECONDS = 300
HOST_ENABLE_TIMEOUT_SECONDS = 600


def _plugin_payload(root: Path) -> bool:
    bootstrap = root / BOOTSTRAP_RELATIVE
    ticket_store = root / TICKET_STORE_RELATIVE
    manifest_path = root / "openclaw.plugin.json"
    package_path = root / "package.json"
    if not (bootstrap.is_file() and ticket_store.is_file() and manifest_path.is_file() and package_path.is_file()):
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        isinstance(manifest, dict)
        and manifest.get("id") == PLUGIN_ID
        and isinstance(package, dict)
        and package.get("name") == PLUGIN_PACKAGE
    )


def _installed_plugin_roots(state_root: Path) -> list[Path]:
    roots: list[Path] = [state_root / "extensions" / PLUGIN_ID]
    managed_projects = state_root / "npm" / "projects"
    if managed_projects.is_dir():
        try:
            projects = [path for path in managed_projects.iterdir() if path.is_dir()]
        except OSError:
            projects = []
        for project in projects:
            roots.append(project)
            roots.append(project / "node_modules" / PLUGIN_PACKAGE)
    deduped: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = os.path.normcase(os.path.abspath(str(root)))
        if key not in seen:
            seen.add(key)
            deduped.append(root)
    return deduped


def resolve_installed_bootstrap(state_root: Path | None = None) -> Path:
    """Resolve one reviewed installed payload from the OpenClaw state boundary."""
    resolved_state = (state_root or base.STATE_ROOT).resolve()
    selected = namespace_ownership.resolve_installed_plugin(resolved_state)
    installed_root = Path(selected["root"])
    bootstrap = installed_root / BOOTSTRAP_RELATIVE
    if not _plugin_payload(installed_root):
        raise RuntimeError(f"installed CogentNexus-OpenClaw payload is incomplete: {installed_root}")
    return bootstrap


def bootstrap_ticket_database(state_root: Path | None = None) -> Path:
    bootstrap = resolve_installed_bootstrap(state_root)
    base.run(
        [base.node_executable(), str(bootstrap), "--workspace", str(base.WORKSPACE)],
        timeout=120,
        check=True,
    )
    return bootstrap


def _run_host(root: Path, command: str) -> Any:
    timeout = HOST_ENABLE_TIMEOUT_SECONDS if command == "enable" else HOST_COMMAND_TIMEOUT_SECONDS
    return base.run([sys.executable, str(HOST), "--root", str(root), command], timeout=timeout, check=False)


def reset(root: Path) -> int:
    try:
        ownership = namespace_ownership.verify_manifest(root, workspace=base.WORKSPACE)
        # Installed plugin payloads live under OpenClaw's state root, while the
        # CNX runtime controller lives under `root`. Keep those ownership domains
        # distinct during reset.
        resolve_installed_bootstrap()
    except Exception as error:
        print(json.dumps({"result": "error", "action": "reset", "error": str(error), "stateChanged": False}, ensure_ascii=False, indent=2))
        return 2

    if not base.confirm("reset"):
        return 0

    try:
        disabled = _run_host(root, "disable")
        if disabled.returncode != 0:
            raise RuntimeError("CogentNexus-OpenClaw could not enter its disabled safety boundary before reset")

        restored = openclaw_route.restore_native(root)
        if not restored.get("ok"):
            raise RuntimeError(f"native OpenClaw route restore failed before reset: {restored}")

        base.disable_startup(root)
        base.reset_plugin_configuration()
        if root.exists():
            shutil.rmtree(root)

        initialized = _run_host(root, "init")
        if initialized.returncode != 0:
            raise RuntimeError("fresh CogentNexus-OpenClaw state initialization failed")

        namespace_ownership.write_manifest(root, ownership)
        bootstrap_ticket_database()
        policy = base.run([sys.executable, str(HOST), "--root", str(root), "policy", "apply"], timeout=120, check=False)
        if policy.returncode != 0:
            raise RuntimeError("fresh CogentNexus-OpenClaw policy application failed")
        first_enable_detail = ""
        try:
            enabled = _run_host(root, "enable")
        except subprocess.TimeoutExpired as error:
            # A timed-out Host child may not finish its transactional rollback.
            # Re-establish the disabled/native boundary before the one permitted retry.
            cleanup = _run_host(root, "disable")
            if cleanup.returncode != 0:
                raise RuntimeError(
                    "CogentNexus-OpenClaw first reset enable timed out and "
                    "the disabled safety boundary could not be re-established"
                ) from error
            reclaimed = supervisor_quiescence.reclaim_dead_enable_owner(root)
            if not reclaimed.get("reclaimed") and reclaimed.get("reason") != "absent":
                raise RuntimeError(
                    "CogentNexus-OpenClaw first reset enable timed out but "
                    f"its quiescence lease could not be safely reclaimed: {reclaimed}"
                ) from error
            first_enable_detail = f"timed out after {error.timeout} seconds"
            enabled = None

        if enabled is None or enabled.returncode != 0:
            # OpenClaw 2026.9.x can transiently lose the Gateway control path
            # during the first plugin activation after fresh reset. Retry
            # exactly once only after the native Gateway is observably healthy.
            retry_gateway = base.gateway_health()
            if not retry_gateway.get("healthy"):
                detail = first_enable_detail
                if enabled is not None:
                    detail = (enabled.stderr or enabled.stdout or "").strip()
                raise RuntimeError(
                    "CogentNexus-OpenClaw enable failed after provider-neutral reset "
                    f"and native Gateway did not recover: {detail or retry_gateway}"
                )
            try:
                enabled = _run_host(root, "enable")
            except subprocess.TimeoutExpired as error:
                reclaimed = supervisor_quiescence.reclaim_dead_enable_owner(root)
                if not reclaimed.get("reclaimed") and reclaimed.get("reason") != "absent":
                    raise RuntimeError(
                        "CogentNexus-OpenClaw retry enable timed out but its "
                        f"quiescence lease could not be safely reclaimed: {reclaimed}"
                    ) from error
                cleanup = _run_host(root, "disable")
                if cleanup.returncode != 0:
                    raise RuntimeError(
                        "CogentNexus-OpenClaw retry enable timed out and the "
                        "disabled safety boundary could not be re-established"
                    ) from error
                raise RuntimeError(
                    "CogentNexus-OpenClaw enable timed out after the one bounded "
                    f"provider-neutral reset retry ({error.timeout} seconds)"
                ) from error
            if enabled.returncode != 0:
                detail = (enabled.stderr or enabled.stdout or "").strip()
                raise RuntimeError(
                    "CogentNexus-OpenClaw enable failed after one bounded "
                    f"provider-neutral reset retry: {detail or 'no child-process detail'}"
                )

        boundary = runtime_boundary.activate_current_config()
        if not boundary.get("ok"):
            raise RuntimeError(f"Gateway activation failed after provider-neutral reset: {boundary}")

        plugin = base.verify_plugin_loaded()
        gateway = base.gateway_health()
        if not gateway.get("healthy"):
            raise RuntimeError("OpenClaw Gateway failed health verification after CogentNexus-OpenClaw reset")

        print("")
        print("COGENTNEXUS-OPENCLAW RESET: PASS")
        print(f"Workspace : {base.WORKSPACE}")
        print(f"Plugin    : {plugin.get('status')}")
        print("Provider  : OpenClaw-owned / unchanged")
        print("Routing   : OpenClaw-owned / unchanged")
        print("State     : fresh-install active")
        return 0
    except Exception as error:
        try:
            if (root / "host" / "controller.json").exists():
                _run_host(root, "disable")
        except Exception:
            pass
        print(json.dumps({
            "result": "error",
            "action": "reset",
            "error": str(error),
            "safety": "CogentNexus-OpenClaw was left disabled when possible; no provider selection or inference recovery was attempted",
        }, ensure_ascii=False, indent=2))
        return 1
