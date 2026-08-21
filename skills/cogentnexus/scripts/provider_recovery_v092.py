#!/usr/bin/env python3
"""Bounded provider recovery policy for CogentNexus v0.9.2."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

POLICY = {
    "ollama": {
        "maximumRecoveriesPerHour": 3,
        "cooldownSeconds": 300,
        "longRunningGraceSeconds": 0,
    },
    "lmstudio": {
        "maximumRecoveriesPerHour": 2,
        "cooldownSeconds": 900,
        "longRunningGraceSeconds": 600,
    },
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_iso(value: datetime | None = None) -> str:
    return (value or now_utc()).astimezone(timezone.utc).isoformat()


def state_path(root: Path) -> Path:
    return root / "host" / "provider-recovery-v092.json"


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        return {"schemaVersion": 1, "providers": {}}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"schemaVersion": 1, "providers": {}}
    if not isinstance(value, dict):
        return {"schemaVersion": 1, "providers": {}}
    value.setdefault("schemaVersion", 1)
    value.setdefault("providers", {})
    return value


def policy(provider_name: str) -> dict[str, int]:
    if provider_name not in POLICY:
        raise ValueError(f"unsupported provider recovery policy: {provider_name}")
    return dict(POLICY[provider_name])


def _provider_state(state: dict[str, Any], provider_name: str) -> dict[str, Any]:
    providers = state.setdefault("providers", {})
    value = providers.get(provider_name)
    if not isinstance(value, dict):
        value = {}
        providers[provider_name] = value
    value.setdefault("attempts", [])
    return value


def _recent_attempts(value: dict[str, Any], current: datetime) -> list[dict[str, Any]]:
    cutoff = current - timedelta(hours=1)
    result = []
    for row in value.get("attempts", []):
        if not isinstance(row, dict):
            continue
        stamp = _parse(row.get("at"))
        if stamp is not None and stamp >= cutoff:
            result.append(row)
    return result


def gate(root: Path, provider_name: str, current: datetime | None = None) -> dict[str, Any]:
    current = (current or now_utc()).astimezone(timezone.utc)
    settings = policy(provider_name)
    state = load_state(root)
    value = _provider_state(state, provider_name)
    attempts = _recent_attempts(value, current)
    cooldown_until = _parse(value.get("cooldownUntil"))
    cooldown_active = cooldown_until is not None and cooldown_until > current
    limit_reached = len(attempts) >= settings["maximumRecoveriesPerHour"]
    allowed = not cooldown_active and not limit_reached
    return {
        "provider": provider_name,
        "allowed": allowed,
        "circuitOpen": cooldown_active or limit_reached,
        "cooldownActive": cooldown_active,
        "limitReached": limit_reached,
        "cooldownUntil": cooldown_until.isoformat() if cooldown_until else None,
        "recoveriesLastHour": len(attempts),
        **settings,
    }


def record_attempt(
    root: Path,
    provider_name: str,
    *,
    success: bool,
    reason: str,
    current: datetime | None = None,
) -> dict[str, Any]:
    """Record one recovery that already occurred and gate the next one.

    Every automatic attempt starts the provider-specific cooldown immediately.
    The rolling-hour maximum is an independent upper bound. Production callers
    must check :func:`gate` before invoking a recovery adapter.
    """
    current = (current or now_utc()).astimezone(timezone.utc)
    settings = policy(provider_name)
    state = load_state(root)
    value = _provider_state(state, provider_name)
    attempts = _recent_attempts(value, current)
    attempts.append({
        "at": current.isoformat(),
        "success": bool(success),
        "reason": str(reason)[:500],
    })
    value["attempts"] = attempts
    value["lastAttemptAt"] = current.isoformat()
    value["lastAttemptSuccess"] = bool(success)
    value["cooldownUntil"] = (
        current + timedelta(seconds=settings["cooldownSeconds"])
    ).isoformat()
    state["updatedAt"] = current.isoformat()
    _atomic_json(state_path(root), state)
    return gate(root, provider_name, current=current)


def clear_after_manual_transition(root: Path, provider_name: str) -> dict[str, Any]:
    """Manual verified provider selection starts with a fresh automatic-recovery budget."""
    state = load_state(root)
    value = _provider_state(state, provider_name)
    value["attempts"] = []
    value.pop("cooldownUntil", None)
    value["lastManualTransitionAt"] = now_iso()
    state["updatedAt"] = now_iso()
    _atomic_json(state_path(root), state)
    return gate(root, provider_name)
