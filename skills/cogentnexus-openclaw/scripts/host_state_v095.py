#!/usr/bin/env python3
"""Provider-independent Host authority state translation and persistence for v0.9.5."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_MODES = {"active", "disabled", "maintenance"}
VALID_GATEWAY_STATES = {"running", "stopped"}
VALID_OLLAMA_ADAPTER_STATES = {"auto", "disabled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def default_state() -> dict[str, Any]:
    return {
        "schemaVersion": 2,
        "cnxMode": "active",
        "desiredGateway": "running",
        "providerOwnership": "openclaw",
        "managedLocalAdapters": {"ollama": "auto"},
        "generation": 1,
        "updatedAt": now_iso(),
    }


def _canonical_adapters(value: Any) -> dict[str, str]:
    adapters = dict(value) if isinstance(value, dict) else {"ollama": "auto"}
    ollama = adapters.get("ollama", "auto")
    if ollama not in VALID_OLLAMA_ADAPTER_STATES:
        raise ValueError(f"invalid Ollama local-adapter state: {ollama!r}")
    return {"ollama": str(ollama)}


def migrate_v094_state(state: dict[str, Any], plugin_enabled: bool | None) -> dict[str, Any]:
    """Translate v0.9.4 Host state into provider-independent v0.9.5 semantics.

    The translation is deliberately route-neutral. Provider selection, model
    selection, credentials, and provider transition metadata are not carried
    into the canonical Host authority state.
    """
    source = dict(state)
    schema = source.get("schemaVersion")

    if schema == 2:
        mode = source.get("cnxMode")
        if mode not in VALID_MODES:
            raise ValueError(f"invalid v0.9.5 cnxMode: {mode!r}")
        desired_gateway = source.get("desiredGateway", "running")
        if desired_gateway not in VALID_GATEWAY_STATES:
            raise ValueError(f"invalid v0.9.5 desiredGateway: {desired_gateway!r}")
        return {
            "schemaVersion": 2,
            "cnxMode": mode,
            "desiredGateway": desired_gateway,
            "providerOwnership": "openclaw",
            "managedLocalAdapters": _canonical_adapters(source.get("managedLocalAdapters")),
            "generation": int(source.get("generation", 1)),
            **({"updatedAt": source["updatedAt"]} if isinstance(source.get("updatedAt"), str) else {}),
        }

    if schema not in {None, 1}:
        raise ValueError(f"unsupported Host state schema: {schema!r}")

    legacy_mode = source.get("mode", "managed")
    if legacy_mode == "managed":
        cnx_mode = "active"
    elif legacy_mode == "maintenance":
        cnx_mode = "maintenance"
    elif legacy_mode == "passthrough":
        cnx_mode = "active" if plugin_enabled is True else "disabled"
    else:
        raise ValueError(f"invalid v0.9.4 Host mode: {legacy_mode!r}")

    desired_gateway = source.get("desiredGateway", "running")
    if desired_gateway not in VALID_GATEWAY_STATES:
        desired_gateway = "running"

    return {
        "schemaVersion": 2,
        "cnxMode": cnx_mode,
        "desiredGateway": desired_gateway,
        "providerOwnership": "openclaw",
        "managedLocalAdapters": {"ollama": "auto"},
        "generation": int(source.get("generation", 1)),
        **({"updatedAt": source["updatedAt"]} if isinstance(source.get("updatedAt"), str) else {}),
    }


def load_state(root: Path, plugin_enabled: bool | None = None) -> dict[str, Any]:
    """Read and translate Host state without mutating the persisted file."""
    path = state_path(root)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default_state()
    if not isinstance(raw, dict):
        raise ValueError("Host state must be a JSON object")
    return migrate_v094_state(raw, plugin_enabled)


def save_state(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    """Persist only canonical v0.9.5 authority fields using atomic replacement."""
    canonical = migrate_v094_state(state, None)
    canonical["updatedAt"] = now_iso()
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    payload = json.dumps(canonical, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, path)
    return canonical


def transition_mode(
    root: Path,
    mode: str,
    *,
    desired_gateway: str | None = None,
) -> dict[str, Any]:
    """Change only CogentNexus authority state; provider routing is not an input."""
    if mode not in VALID_MODES:
        raise ValueError(f"invalid v0.9.5 cnxMode: {mode!r}")
    if desired_gateway is not None and desired_gateway not in VALID_GATEWAY_STATES:
        raise ValueError(f"invalid v0.9.5 desiredGateway: {desired_gateway!r}")

    current = load_state(root)
    target_gateway = current["desiredGateway"] if desired_gateway is None else desired_gateway
    if current["cnxMode"] == mode and current["desiredGateway"] == target_gateway:
        return current

    changed = dict(current)
    changed["cnxMode"] = mode
    changed["desiredGateway"] = target_gateway
    changed["generation"] = int(current.get("generation", 0)) + 1
    return save_state(root, changed)
