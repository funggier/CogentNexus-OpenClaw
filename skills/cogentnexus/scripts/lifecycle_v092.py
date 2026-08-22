#!/usr/bin/env python3
"""CogentNexus v0.9.2 destructive lifecycle wrapper.

Uninstall and reset preserve the accepted v0.9.1 explicit-y and PASSTHROUGH-first
safety boundaries while also restoring the narrow OpenClaw route/timeout/compat
fields owned by v0.9.2 before CNX state is removed.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import lifecycle_v091 as base
import openclaw_route_v092 as openclaw_route
import openclaw_runtime_boundary_v092 as runtime_boundary
import provider

HERE = Path(__file__).resolve()
HOST = HERE.with_name("host_provider_v092.py")
HOST_CONTROL = HERE.with_name("host_control_v092.py")
STARTUP = HERE.with_name("startup_v092.py")
PLUGIN_ID = base.PLUGIN_ID
PLUGIN_PACKAGE = "openclaw-plugin-cogentnexus-rotation"
BOOTSTRAP_RELATIVE = Path("scripts") / "bootstrap-ticket-db.mjs"
TICKET_STORE_RELATIVE = Path("dist") / "ticket-store.js"

base.HOST = HOST
base.HOST_CONTROL = HOST_CONTROL
base.STARTUP = STARTUP


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _semver_key(value: object) -> tuple[int, int, int, str]:
    text = str(value or "")
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", text)
    if not match:
        return (-1, -1, -1, text)
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4))


def _plugin_payload(root: Path) -> dict[str, Any] | None:
    bootstrap = root / BOOTSTRAP_RELATIVE
    ticket_store = root / TICKET_STORE_RELATIVE
    manifest_path = root / "openclaw.plugin.json"
    package_path = root / "package.json"
    if not (bootstrap.is_file() and ticket_store.is_file() and manifest_path.is_file() and package_path.is_file()):
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(manifest, dict) or manifest.get("id") != PLUGIN_ID:
        return None
    if not isinstance(package, dict) or package.get("name") != PLUGIN_PACKAGE:
        return None
    fingerprint = hashlib.sha256()
    fingerprint.update(bootstrap.read_bytes())
    fingerprint.update(b"\0")
    fingerprint.update(ticket_store.read_bytes())
    try:
        installed_mtime_ns = root.stat().st_mtime_ns
    except OSError:
        installed_mtime_ns = 0
    return {
        "root": root,
        "bootstrap": bootstrap,
        "version": str(package.get("version") or ""),
        "versionKey": _semver_key(package.get("version")),
        "fingerprint": fingerprint.hexdigest(),
        "installedMtimeNs": installed_mtime_ns,
    }


def _installed_plugin_candidate_roots(state_root: Path) -> list[Path]:
    """Return only deterministic CogentNexus package locations.

    OpenClaw can expose a historical unpacked extension directly under
    `.openclaw/extensions/<plugin-id>`, or create an npm project wrapper below
    `.openclaw/npm/projects/<generation>` whose installed package is under
    `node_modules/<npm-package-name>`.  Some OpenClaw builds may unpack the
    package directly at the project root, so both exact locations are checked.

    This intentionally does not recursively scan arbitrary node_modules trees.
    """
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
        if key in seen:
            continue
        seen.add(key)
        deduped.append(root)
    return deduped


def resolve_installed_bootstrap(state_root: Path | None = None) -> Path:
    """Resolve the verified bootstrap from legacy or managed npm layouts.

    OpenClaw 2026.7.1-2 installs npm-pack plugins below `.openclaw/npm/projects`.
    The project directory can itself be only an npm wrapper, with the actual
    CogentNexus package under `node_modules/openclaw-plugin-cogentnexus-rotation`.
    Reset must use the installed release payload without depending on either
    layout alone.
    """
    resolved_state = (state_root or base.STATE_ROOT).resolve()
    roots = _installed_plugin_candidate_roots(resolved_state)

    payloads = [payload for root in roots if (payload := _plugin_payload(root)) is not None]
    if not payloads:
        searched = [str(root) for root in roots]
        raise RuntimeError(
            "installed CogentNexus plugin lacks a verified scripts/bootstrap-ticket-db.mjs payload; "
            f"searched legacy and managed OpenClaw plugin package roots: {searched}"
        )

    highest_version = max(payload["versionKey"] for payload in payloads)
    highest = [payload for payload in payloads if payload["versionKey"] == highest_version]
    fingerprints = {payload["fingerprint"] for payload in highest}
    if len(fingerprints) != 1:
        roots_text = [str(payload["root"]) for payload in highest]
        raise RuntimeError(
            "multiple installed CogentNexus plugin payloads have the same highest version but conflicting bootstrap/runtime bytes; "
            f"refusing ambiguous fresh reset: {roots_text}"
        )

    selected = max(highest, key=lambda payload: (payload["installedMtimeNs"], str(payload["root"])))
    return Path(selected["bootstrap"])


def bootstrap_ticket_database() -> Path:
    bootstrap = resolve_installed_bootstrap()
    base.run(
        [base.node_executable(), str(bootstrap), "--workspace", str(base.WORKSPACE)],
        timeout=120,
        check=True,
    )
    return bootstrap


def resolve_fresh_provider(explicit: str | None) -> str:
    if explicit:
        return provider.normalize_provider(explicit)
    installed = provider.installed_providers()
    if len(installed) == 1:
        return installed[0]
    if not installed:
        raise RuntimeError("reset cannot return MANAGED: no supported local provider is installed")
    raise RuntimeError(
        "reset requires an explicit provider because both Ollama and LM Studio are installed; "
        "use 'cnx.cmd reset --provider ollama' or 'cnx.cmd reset --provider lmstudio'"
    )


def seed_transition(root: Path, target: str) -> None:
    path = root / "host" / "controller.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state.pop("selectedProvider", None)
    state.pop("providerSelection", None)
    state["providerTransition"] = {
        "from": None,
        "to": target,
        "source": "reset-explicit" if len(provider.installed_providers()) > 1 else "reset-single-installed",
        "startedAt": now_iso(),
    }
    atomic_json(path, state)


def commit_selection(root: Path, target: str) -> None:
    path = root / "host" / "controller.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state["selectedProvider"] = target
    state["providerTransition"] = None
    state["desiredProvider"] = "running"
    state["providerSelection"] = {
        "selectedAt": now_iso(),
        "selectionSource": "reset",
        "lastVerifiedAt": now_iso(),
    }
    state["generation"] = int(state.get("generation", 0)) + 1
    atomic_json(path, state)


def reset(root: Path, explicit_provider: str | None = None) -> int:
    try:
        target = resolve_fresh_provider(explicit_provider)
        route_plan = openclaw_route.plan(root, target)
        if not route_plan.get("ok"):
            raise RuntimeError(f"OpenClaw route preflight failed: {route_plan}")
        # Resolve the immutable installed plugin bootstrap before any destructive
        # state removal. This is read-only and fails closed if the installation
        # cannot prove a coherent release payload.
        resolve_installed_bootstrap()
    except Exception as error:
        print(json.dumps({"result": "error", "action": "reset", "error": str(error), "stateChanged": False}, ensure_ascii=False, indent=2))
        return 2

    if not base.confirm("reset"):
        return 0
    route_started = False
    try:
        # host_control_v092 disable restores the native route and verifies a
        # Gateway process boundary before returning success.
        base.disable_managed(root)
        restored = openclaw_route.restore_native(root)
        if not restored.get("ok"):
            raise RuntimeError(f"native OpenClaw route restore failed before reset: {restored}")

        base.disable_startup(root)
        base.reset_plugin_configuration()
        if root.exists():
            shutil.rmtree(root)

        base.run([sys.executable, str(HOST), "--root", str(root), "init"], timeout=120, check=True)
        bootstrap_ticket_database()
        base.run([sys.executable, str(HOST), "--root", str(root), "policy", "apply"], timeout=120, check=True)

        seed_transition(root, target)
        route_result = openclaw_route.begin(root, target)
        if not route_result.get("ok"):
            raise RuntimeError(f"OpenClaw route transaction failed after reset: {route_result}")
        route_started = True

        enabled = base.run([sys.executable, str(HOST_CONTROL), "--root", str(root), "enable"], timeout=300, check=False)
        base.forward(enabled)
        if enabled.returncode != 0:
            raise RuntimeError("CogentNexus transactional enable failed after reset")

        # v0.9.1 lifecycle start may skip Gateway start when it is already
        # healthy. Force one process boundary so verification observes the new
        # provider route and newly enabled plugin in the running Gateway.
        managed_boundary = runtime_boundary.activate_current_config()
        if not managed_boundary.get("ok"):
            raise RuntimeError(f"Gateway failed to activate fresh MANAGED route after reset: {managed_boundary}")

        plugin = base.verify_plugin_loaded()
        gateway = base.gateway_health()
        provider_health = provider.probe(target, timeout=5.0)
        route_after = openclaw_route.plan(root, target)
        route_ready = (
            route_after.get("ok")
            and route_after.get("currentProvider") == target
            and route_after.get("currentModel") == route_after.get("model")
        )
        if not gateway.get("healthy"):
            raise RuntimeError("OpenClaw Gateway failed health verification after CogentNexus reset")
        if not provider_health.get("healthy"):
            raise RuntimeError(f"selected provider '{target}' failed health verification after CogentNexus reset")
        if not route_ready:
            raise RuntimeError(f"OpenClaw model route failed verification after CogentNexus reset: {route_after}")

        route_commit = openclaw_route.commit(root)
        if not route_commit.get("ok"):
            raise RuntimeError(f"OpenClaw route commit failed after reset: {route_commit}")
        commit_selection(root, target)

        print("")
        print("COGENTNEXUS RESET: PASS")
        print(f"Workspace : {base.WORKSPACE}")
        print(f"Plugin    : {plugin.get('status')}")
        print(f"Provider  : {target}")
        print(f"Model     : {route_after.get('model')}")
        print("State     : fresh-install MANAGED")
        return 0
    except Exception as error:
        try:
            if route_started:
                openclaw_route.rollback(root)
        except Exception:
            pass
        try:
            if (root / "host" / "controller.json").exists():
                base.run([sys.executable, str(HOST_CONTROL), "--root", str(root), "disable"], timeout=240, check=False)
        except Exception:
            pass
        print(json.dumps({
            "result": "error",
            "action": "reset",
            "provider": target,
            "error": str(error),
            "safety": "CogentNexus was left disabled/PASSTHROUGH when possible; no automatic inference recovery was attempted",
        }, ensure_ascii=False, indent=2))
        return 1


def uninstall(root: Path) -> int:
    if not base.confirm("uninstall"):
        return 0
    try:
        # host_control_v092 refuses to return success until the native route is
        # active in a healthy Gateway process.
        base.disable_managed(root)
        restored = openclaw_route.restore_native(root)
        if not restored.get("ok"):
            raise RuntimeError(f"native OpenClaw route restore failed before uninstall: {restored}")

        base.disable_startup(root)
        base.uninstall_plugin()

        gateway = base.gateway_health()
        if not gateway.get("healthy"):
            raise RuntimeError("native OpenClaw Gateway is not healthy after CogentNexus uninstall boundary")

        owned = base.uninstall_owned_paths(root)
        if os.name == "nt":
            base.schedule_windows_cleanup(owned)
        else:
            for path in owned:
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=False)
                elif path.exists():
                    path.unlink()

        print("")
        print("COGENTNEXUS UNINSTALL: PASS")
        print("OpenClaw : native / healthy / pre-CNX route restored")
        print("Providers: unchanged")
        if os.name == "nt":
            print("Cleanup  : cnx.cmd and remaining CNX files/backups scheduled for removal after command exit")
        return 0
    except Exception as error:
        print(json.dumps({
            "result": "error",
            "action": "uninstall",
            "error": str(error),
            "safety": "destructive file cleanup was not scheduled unless native OpenClaw health and route restoration were verified",
        }, ensure_ascii=False, indent=2))
        return 1


def main(command: str, root: Path | None = None, explicit_provider: str | None = None) -> int:
    resolved = (root or base.DEFAULT_ROOT).resolve()
    if command == "reset":
        return reset(resolved, explicit_provider)
    if command == "uninstall":
        return uninstall(resolved)
    raise ValueError(f"unsupported lifecycle command: {command}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in {"reset", "uninstall"}:
        print("Usage: lifecycle_v092.py reset|uninstall [--provider ollama|lmstudio]", file=sys.stderr)
        raise SystemExit(2)
    command = sys.argv[1]
    explicit = None
    if "--provider" in sys.argv[2:]:
        index = sys.argv.index("--provider")
        if index + 1 >= len(sys.argv):
            raise SystemExit("--provider requires a value")
        explicit = sys.argv[index + 1]
    raise SystemExit(main(command, explicit_provider=explicit))
