#!/usr/bin/env python3
"""Provider-independent Host authority state translation for v0.9.5."""
from __future__ import annotations

from typing import Any


VALID_MODES = {"active", "disabled", "maintenance"}
VALID_GATEWAY_STATES = {"running", "stopped"}


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
        adapters = source.get("managedLocalAdapters")
        if not isinstance(adapters, dict):
            adapters = {"ollama": "auto"}
        return {
            "schemaVersion": 2,
            "cnxMode": mode,
            "desiredGateway": desired_gateway,
            "providerOwnership": "openclaw",
            "managedLocalAdapters": dict(adapters),
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
