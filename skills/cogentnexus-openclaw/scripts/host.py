#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 Host compatibility façade.

The proven v0.9.4 Host behavior remains executable in this module namespace so
existing overlays keep their dynamic monkey-patching semantics. Only Host
authority-state translation/persistence is replaced here; provider routing and
lifecycle decoupling are repaired in later TDD steps.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


# Execute the exact v0.9.4 Host payload in this module namespace. This preserves
# function-global lookups used by host_v091/host_v092 overlays while allowing
# the narrow v0.9.5 state façade below to replace selected global functions.
_WRAPPER_NAME = __name__
_LEGACY_PATH = Path(__file__).with_name("host_legacy_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_host_legacy_v094_embedded"
try:
    exec(compile(_LEGACY_PATH.read_text(encoding="utf-8"), str(_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME

import host_state_v095 as _host_state_v095


_LEGACY_PROVIDER_FIELDS = {
    "desiredProvider",
    "selectedProvider",
    "providerTransition",
    "providerSelection",
}
_LEGACY_TO_CANONICAL_MODE = {
    "managed": "active",
    "passthrough": "disabled",
    "maintenance": "maintenance",
}
_CANONICAL_TO_LEGACY_MODE = {
    "active": "managed",
    "disabled": "passthrough",
    "maintenance": "maintenance",
}


def _compatibility_view(state: dict[str, Any]) -> dict[str, Any]:
    """Expose legacy `mode` only in memory; never restore provider authority."""
    view = dict(state)
    for key in _LEGACY_PROVIDER_FIELDS:
        view.pop(key, None)
    mode = view.get("cnxMode")
    if mode not in _CANONICAL_TO_LEGACY_MODE:
        raise ValueError(f"invalid v0.9.5 cnxMode: {mode!r}")
    view["mode"] = _CANONICAL_TO_LEGACY_MODE[str(mode)]
    return view


def default_state() -> dict[str, Any]:
    return _compatibility_view(_host_state_v095.default_state())


def load_state(root: Path, plugin_enabled: bool | None = None) -> dict[str, Any]:
    """Read canonical state without mutating disk and derive legacy mode."""
    path = host_state_path(root)
    if not path.exists():
        # Deliberately call the global default_state so the proven v0.9.1 safe
        # initialization overlay can still replace it dynamically.
        raw_default = default_state()
        canonical = _host_state_v095.migrate_v094_state(raw_default, plugin_enabled)
    else:
        canonical = _host_state_v095.load_state(root, plugin_enabled=plugin_enabled)
    return _compatibility_view(canonical)


def save_state(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    """Persist only canonical v0.9.5 authority fields and return a legacy view."""
    candidate = dict(state)
    legacy_mode = candidate.pop("mode", None)
    for key in _LEGACY_PROVIDER_FIELDS:
        candidate.pop(key, None)
    if legacy_mode is not None:
        # At this compatibility boundary an explicitly supplied legacy mode is
        # the caller's mutation intent. It must override a stale cnxMode that
        # may have travelled with an in-memory compatibility view.
        try:
            candidate["cnxMode"] = _LEGACY_TO_CANONICAL_MODE[str(legacy_mode)]
        except KeyError as error:
            raise ValueError(f"invalid legacy Host mode: {legacy_mode!r}") from error
    # Once a legacy compatibility mode has been translated, persist it as the
    # canonical schema. Leaving schemaVersion=1 would make the lower layer
    # reinterpret the already-translated state and could turn passthrough back
    # into managed when explicit plugin evidence is unavailable.
    candidate["schemaVersion"] = 2
    canonical = _host_state_v095.save_state(root, candidate)
    return _compatibility_view(canonical)


def transition(root: Path, **changes: Any) -> dict[str, Any]:
    """Translate legacy authority changes while ignoring provider-route metadata."""
    current = load_state(root)
    requested = dict(changes)

    legacy_mode = requested.pop("mode", None)
    canonical_mode = requested.pop("cnxMode", None)
    if canonical_mode is None and legacy_mode is not None:
        try:
            canonical_mode = _LEGACY_TO_CANONICAL_MODE[str(legacy_mode)]
        except KeyError as error:
            raise ValueError(f"invalid legacy Host mode: {legacy_mode!r}") from error
    if canonical_mode is None:
        canonical_mode = current["cnxMode"]
    if canonical_mode not in _host_state_v095.VALID_MODES:
        raise ValueError(f"invalid v0.9.5 cnxMode: {canonical_mode!r}")

    desired_gateway = requested.pop("desiredGateway", current["desiredGateway"])
    if desired_gateway not in _host_state_v095.VALID_GATEWAY_STATES:
        raise ValueError(f"invalid v0.9.5 desiredGateway: {desired_gateway!r}")

    for key in _LEGACY_PROVIDER_FIELDS:
        requested.pop(key, None)
    if requested:
        unknown = ", ".join(sorted(requested))
        raise ValueError(f"unsupported Host authority transition fields: {unknown}")

    if current["cnxMode"] == canonical_mode and current["desiredGateway"] == desired_gateway:
        return current

    canonical = dict(current)
    canonical.pop("mode", None)
    canonical["cnxMode"] = canonical_mode
    canonical["desiredGateway"] = desired_gateway
    canonical["generation"] = int(current.get("generation", 0)) + 1
    return save_state(root, canonical)


if __name__ == "__main__":
    raise SystemExit(main())
