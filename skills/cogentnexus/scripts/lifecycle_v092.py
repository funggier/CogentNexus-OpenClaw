#!/usr/bin/env python3
"""CogentNexus v0.9.2 destructive lifecycle wrapper.

Uninstall reuses the accepted v0.9.1 safety path. Reset keeps v0.9.1 explicit-y,
PASSTHROUGH-first and verification semantics, but chooses the fresh-install
provider explicitly when more than one local provider is installed.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import lifecycle_v091 as base
import provider

HERE = Path(__file__).resolve()
HOST = HERE.with_name("host_provider_v092.py")
HOST_CONTROL = HERE.with_name("host_control_v092.py")
STARTUP = HERE.with_name("startup_v092.py")

# Uninstall/disable calls from the accepted lifecycle use current release wiring.
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
    except Exception as error:
        print(json.dumps({"result": "error", "action": "reset", "error": str(error), "stateChanged": False}, ensure_ascii=False, indent=2))
        return 2

    if not base.confirm("reset"):
        return 0
    try:
        base.disable_managed(root)
        base.disable_startup(root)
        base.reset_plugin_configuration()
        if root.exists():
            shutil.rmtree(root)

        base.run([sys.executable, str(HOST), "--root", str(root), "init"], timeout=120, check=True)
        base.bootstrap_ticket_database()
        base.run([sys.executable, str(HOST), "--root", str(root), "policy", "apply"], timeout=120, check=True)

        # Fresh reset state has no selected provider. Only an in-progress target
        # is durable until MANAGED + provider + Gateway verification succeeds.
        seed_transition(root, target)
        enabled = base.run([sys.executable, str(HOST_CONTROL), "--root", str(root), "enable"], timeout=300, check=False)
        base.forward(enabled)
        if enabled.returncode != 0:
            raise RuntimeError("CogentNexus transactional enable failed after reset")

        plugin = base.verify_plugin_loaded()
        gateway = base.gateway_health()
        provider_health = provider.probe(target, timeout=5.0)
        if not gateway.get("healthy"):
            raise RuntimeError("OpenClaw Gateway failed health verification after CogentNexus reset")
        if not provider_health.get("healthy"):
            raise RuntimeError(f"selected provider '{target}' failed health verification after CogentNexus reset")
        commit_selection(root, target)

        print("")
        print("COGENTNEXUS RESET: PASS")
        print(f"Workspace : {base.WORKSPACE}")
        print(f"Plugin    : {plugin.get('status')}")
        print(f"Provider  : {target}")
        print("State     : fresh-install MANAGED")
        return 0
    except Exception as error:
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


def main(command: str, root: Path | None = None, explicit_provider: str | None = None) -> int:
    resolved = (root or base.DEFAULT_ROOT).resolve()
    if command == "reset":
        return reset(resolved, explicit_provider)
    if command == "uninstall":
        return base.uninstall(resolved)
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
