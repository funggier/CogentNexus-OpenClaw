#!/usr/bin/env python3
"""Ownership-safe CogentNexus-OpenClaw v0.9.2 OpenClaw route facade.

The original v0.9.2 route implementation remains in
``openclaw_route_v092_legacy``. This facade preserves its public API while
hardening transaction rollback so the route layer restores only fields it
owns. In particular, accepted v0.9.1 remains the sole owner of
``diagnostics.stuckSessionAbortMs``.

A full-file rollback can resurrect an older value of an unrelated field after
another authority has legitimately changed it while the route transaction was
in progress. The live Windows acceptance sequence exposed exactly that race:
v0.9.1 restored the native watchdog, then a v0.9.2 byte-for-byte route rollback
wrote the managed 24h watchdog back. Rollback and crash recovery below merge
only route-owned fields from the transaction backup into the current config.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import openclaw_route_v092_legacy as _legacy
from openclaw_route_v092_legacy import *  # noqa: F401,F403

# Preserve the backend validator separately so the facade can keep the existing
# monkeypatch contract used by tests without recursively calling itself.
_backend_validate_openclaw_config = _legacy.validate_openclaw_config

# Preserve private helpers used by the existing regression suite and by this
# ownership-safe overlay.
_atomic_json = _legacy._atomic_json
_atomic_bytes = _legacy._atomic_bytes
_load_json = _legacy._load_json
_load_state = _legacy._load_state
_save_state = _legacy._save_state
_snapshot = _legacy._snapshot
_restore = _legacy._restore
_ensure_dict = _legacy._ensure_dict
_find_model_entry = _legacy._find_model_entry


def validate_openclaw_config() -> dict[str, Any]:
    """Facade validator retained as an overridable test/runtime seam."""
    return _backend_validate_openclaw_config()


def _dict_child(container: Any, key: str) -> dict[str, Any] | None:
    if not isinstance(container, dict):
        return None
    value = container.get(key)
    return value if isinstance(value, dict) else None


def _restore_route_owned_fields(
    current: dict[str, Any],
    original: dict[str, Any],
    state: dict[str, Any],
) -> dict[str, Any]:
    """Restore only fields owned by the v0.9.2 route layer.

    The transaction backup is still a complete OpenClaw config because it is
    useful forensic evidence and gives exact source values. It is *not*
    written back wholesale. Everything outside the route-owned surface keeps
    its current value, including the v0.9.1 watchdog, plugin state, operator
    edits, and future OpenClaw settings unknown to this release.
    """
    current_agents = _ensure_dict(current, "agents")
    current_defaults = _ensure_dict(current_agents, "defaults")
    original_agents = _dict_child(original, "agents") or {}
    original_defaults = _dict_child(original_agents, "defaults") or {}

    _restore(current_defaults, "model", _snapshot(original_defaults, "model"))
    _restore(
        current_defaults,
        "timeoutSeconds",
        _snapshot(original_defaults, "timeoutSeconds"),
    )

    current_models = _ensure_dict(current, "models")
    current_providers = _ensure_dict(current_models, "providers")
    original_models = _dict_child(original, "models") or {}
    original_providers = _dict_child(original_models, "providers") or {}

    # The backend restores baseline timeout knobs before applying a new target,
    # so either local provider timeout may be touched during a switch.
    for provider_key in _legacy.PROVIDER_PREFIX.values():
        current_provider = current_providers.get(provider_key)
        if not isinstance(current_provider, dict):
            continue
        original_provider = original_providers.get(provider_key)
        original_provider = original_provider if isinstance(original_provider, dict) else {}
        _restore(
            current_provider,
            "timeoutSeconds",
            _snapshot(original_provider, "timeoutSeconds"),
        )

    # Route management can restore previously captured LM Studio compat fields
    # and then add the unsupported schema keywords to the target model. Restore
    # the complete compat object for every model ref the route state can own,
    # without touching any other model properties.
    model_refs: set[str] = set()
    baseline = state.get("baseline")
    if isinstance(baseline, dict):
        baseline_compat = baseline.get("modelCompat")
        if isinstance(baseline_compat, dict):
            model_refs.update(str(value) for value in baseline_compat.keys())
    transaction = state.get("transaction")
    if isinstance(transaction, dict):
        model = transaction.get("model")
        if isinstance(model, str):
            model_refs.add(model)
    routes = state.get("routes")
    if isinstance(routes, dict):
        lmstudio_route = routes.get("lmstudio")
        if isinstance(lmstudio_route, str):
            model_refs.add(lmstudio_route)

    for model_ref in model_refs:
        if not model_ref.startswith(_legacy.PROVIDER_PREFIX["lmstudio"] + "/"):
            continue
        current_row = _find_model_entry(current, model_ref)
        original_row = _find_model_entry(original, model_ref)
        if current_row is None or original_row is None:
            continue
        _restore(current_row, "compat", _snapshot(original_row, "compat"))

    return current


def _rollback_pending(root: Path, *, recovery: bool) -> dict[str, Any]:
    state = _load_state(root)
    transaction = state.get("transaction")
    backup = _legacy.rollback_path(root)

    if recovery:
        if not isinstance(transaction, dict) or transaction.get("status") != "pending":
            return {"ok": True, "recovered": False}
        if not backup.is_file():
            return {
                "ok": False,
                "recovered": False,
                "error": "pending OpenClaw route transaction has no rollback copy",
            }
    elif not backup.is_file():
        state["transaction"] = None
        _save_state(root, state)
        return {"ok": True, "rolledBack": False, "reason": "rollback copy absent"}

    config_path = _legacy.openclaw_config_path()
    try:
        original = _load_json(backup)
        current = _load_json(config_path)
        merged = _restore_route_owned_fields(current, original, state)
        _atomic_json(config_path, merged)
    except Exception as error:
        key = "recovered" if recovery else "rolledBack"
        return {
            "ok": False,
            key: False,
            "error": f"ownership-safe route rollback failed: {error}",
        }

    # Call through the facade so existing monkeypatch/test seams remain valid.
    validation = validate_openclaw_config()
    if not validation.get("ok"):
        key = "recovered" if recovery else "rolledBack"
        payload = {
            "ok": False,
            key: False,
            "validation": validation,
        }
        if recovery:
            payload["error"] = "rollback config failed validation"
        return payload

    backup.unlink(missing_ok=True)
    state["transaction"] = None
    state["lastRollbackAt"] = _legacy.now_iso()
    _save_state(root, state)

    if recovery:
        return {
            "ok": True,
            "recovered": True,
            "rollbackMode": "route-owned-fields",
            "validation": validation,
        }
    return {
        "ok": True,
        "rolledBack": True,
        "rollbackMode": "route-owned-fields",
        "validation": validation,
    }


def recover_pending(root: Path) -> dict[str, Any]:
    return _rollback_pending(root, recovery=True)


def rollback(root: Path) -> dict[str, Any]:
    return _rollback_pending(root, recovery=False)


def _sync_backend_overrides() -> None:
    """Keep backend global lookups bound to facade ownership/test seams."""
    _legacy.validate_openclaw_config = validate_openclaw_config
    _legacy.recover_pending = recover_pending
    _legacy.rollback = rollback


def begin(root: Path, provider_name: str) -> dict[str, Any]:
    _sync_backend_overrides()
    return _legacy.begin(root, provider_name)


def commit(root: Path) -> dict[str, Any]:
    _sync_backend_overrides()
    return _legacy.commit(root)


def restore_native(root: Path) -> dict[str, Any]:
    _sync_backend_overrides()
    return _legacy.restore_native(root)


_sync_backend_overrides()
