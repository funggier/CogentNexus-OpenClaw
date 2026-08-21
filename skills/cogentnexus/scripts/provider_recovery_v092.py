#!/usr/bin/env python3
"""Event-driven provider recovery authority for CogentNexus v0.9.2.

Recovery authority is derived from durable incident evidence, never from elapsed
wall-clock time. Timestamps are audit/order metadata only. A provider incident
opens on an explicit failure event, consumes a bounded number of automatic
recovery attempts, and closes only on stable-success evidence or a verified
manual provider transition.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
POLICY = {
    "ollama": {"maximumRecoveriesPerIncident": 3},
    "lmstudio": {"maximumRecoveriesPerIncident": 2},
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


def _blank_state() -> dict[str, Any]:
    return {"schemaVersion": SCHEMA_VERSION, "providers": {}}


def _normalize_provider_state(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        value = {}
    incident = value.get("incident")
    if not isinstance(incident, dict) or incident.get("state") != "open":
        incident = None
    return {
        "generation": max(0, int(value.get("generation", 0) or 0)),
        "incident": incident,
        "lastClosedIncident": value.get("lastClosedIncident") if isinstance(value.get("lastClosedIncident"), dict) else None,
        "lastStableSuccessAt": value.get("lastStableSuccessAt"),
        "lastManualTransitionAt": value.get("lastManualTransitionAt"),
        "lastEvent": value.get("lastEvent") if isinstance(value.get("lastEvent"), dict) else None,
    }


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        return _blank_state()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _blank_state()
    if not isinstance(raw, dict):
        return _blank_state()

    # v0.9.2 development briefly used rolling-hour/cooldown state. It never
    # shipped. Deliberately migrate by dropping time-derived recovery authority;
    # stale timers must not authorize or block the event-driven policy.
    if raw.get("schemaVersion") != SCHEMA_VERSION:
        providers = raw.get("providers") if isinstance(raw.get("providers"), dict) else {}
        migrated = _blank_state()
        for name in POLICY:
            old = providers.get(name)
            if isinstance(old, dict):
                migrated["providers"][name] = {
                    "generation": 0,
                    "incident": None,
                    "lastClosedIncident": None,
                    "lastStableSuccessAt": None,
                    "lastManualTransitionAt": old.get("lastManualTransitionAt"),
                    "lastEvent": {
                        "type": "policy_migrated_to_event_driven",
                        "at": now_iso(),
                        "evidence": {"discardedTimedRecoveryState": True},
                    },
                }
        return migrated

    providers = raw.get("providers") if isinstance(raw.get("providers"), dict) else {}
    state = _blank_state()
    for name, value in providers.items():
        if name in POLICY:
            state["providers"][name] = _normalize_provider_state(value)
    state["updatedAt"] = raw.get("updatedAt")
    return state


def policy(provider_name: str) -> dict[str, int]:
    if provider_name not in POLICY:
        raise ValueError(f"unsupported provider recovery policy: {provider_name}")
    return dict(POLICY[provider_name])


def _provider_state(state: dict[str, Any], provider_name: str) -> dict[str, Any]:
    if provider_name not in POLICY:
        raise ValueError(f"unsupported provider recovery policy: {provider_name}")
    providers = state.setdefault("providers", {})
    value = _normalize_provider_state(providers.get(provider_name))
    providers[provider_name] = value
    return value


def _event(value: dict[str, Any], event_type: str, evidence: Any = None, *, current: datetime | None = None) -> None:
    value["lastEvent"] = {
        "type": str(event_type),
        "at": now_iso(current),
        "evidence": evidence if evidence is not None else {},
    }


def _save(root: Path, state: dict[str, Any], *, current: datetime | None = None) -> None:
    state["schemaVersion"] = SCHEMA_VERSION
    state["updatedAt"] = now_iso(current)
    _atomic_json(state_path(root), state)


def begin_incident(
    root: Path,
    provider_name: str,
    classification: str,
    evidence: Any = None,
    *,
    current: datetime | None = None,
) -> dict[str, Any]:
    """Open (or update) the provider's current incident from explicit evidence."""
    state = load_state(root)
    value = _provider_state(state, provider_name)
    existing = value.get("incident")
    if isinstance(existing, dict) and existing.get("state") == "open":
        existing["classification"] = str(classification)
        existing["lastEvidence"] = evidence if evidence is not None else {}
        existing["lastEventAt"] = now_iso(current)
        _event(value, "incident_evidence", {"classification": classification, "evidence": evidence}, current=current)
        _save(root, state, current=current)
        return gate(root, provider_name)

    generation = int(value.get("generation", 0)) + 1
    value["generation"] = generation
    stamp = now_iso(current)
    value["incident"] = {
        "id": f"{provider_name}:{generation}",
        "state": "open",
        "classification": str(classification),
        "openedAt": stamp,
        "lastEventAt": stamp,
        "lastEvidence": evidence if evidence is not None else {},
        "recoveryAttempts": [],
        "circuitOpen": False,
    }
    _event(value, "incident_opened", {"classification": classification, "evidence": evidence}, current=current)
    _save(root, state, current=current)
    return gate(root, provider_name)


def gate(root: Path, provider_name: str) -> dict[str, Any]:
    """Return recovery authority from incident evidence only; elapsed time is irrelevant."""
    settings = policy(provider_name)
    state = load_state(root)
    value = _provider_state(state, provider_name)
    incident = value.get("incident")
    open_incident = isinstance(incident, dict) and incident.get("state") == "open"
    attempts = incident.get("recoveryAttempts", []) if open_incident else []
    if not isinstance(attempts, list):
        attempts = []
    maximum = settings["maximumRecoveriesPerIncident"]
    circuit_open = bool(open_incident and (incident.get("circuitOpen") or len(attempts) >= maximum))
    return {
        "provider": provider_name,
        "allowed": bool(open_incident and not circuit_open),
        "circuitOpen": circuit_open,
        "incidentOpen": bool(open_incident),
        "incidentId": incident.get("id") if open_incident else None,
        "classification": incident.get("classification") if open_incident else None,
        "recoveryAttempts": len(attempts),
        "maximumRecoveriesPerIncident": maximum,
        "lastEvent": value.get("lastEvent"),
    }


def record_attempt(
    root: Path,
    provider_name: str,
    *,
    success: bool,
    reason: str,
    evidence: Any = None,
    current: datetime | None = None,
) -> dict[str, Any]:
    """Consume one automatic recovery attempt inside the current incident."""
    settings = policy(provider_name)
    state = load_state(root)
    value = _provider_state(state, provider_name)
    incident = value.get("incident")
    if not isinstance(incident, dict) or incident.get("state") != "open":
        raise RuntimeError("automatic provider recovery requires an explicit open incident")
    attempts = incident.setdefault("recoveryAttempts", [])
    maximum = settings["maximumRecoveriesPerIncident"]
    if incident.get("circuitOpen") or len(attempts) >= maximum:
        incident["circuitOpen"] = True
        _event(value, "recovery_suppressed_circuit_open", {"reason": reason}, current=current)
        _save(root, state, current=current)
        return gate(root, provider_name)

    stamp = now_iso(current)
    attempts.append({
        "sequence": len(attempts) + 1,
        "at": stamp,
        "success": bool(success),
        "reason": str(reason)[:500],
        "evidence": evidence if evidence is not None else {},
    })
    incident["lastEventAt"] = stamp
    incident["lastRecoverySuccess"] = bool(success)
    incident["circuitOpen"] = len(attempts) >= maximum
    _event(value, "automatic_recovery_attempted", {
        "incidentId": incident.get("id"),
        "sequence": len(attempts),
        "success": bool(success),
        "reason": reason,
        "evidence": evidence,
    }, current=current)
    _save(root, state, current=current)
    return gate(root, provider_name)


def close_incident(
    root: Path,
    provider_name: str,
    reason: str,
    evidence: Any = None,
    *,
    current: datetime | None = None,
) -> dict[str, Any]:
    state = load_state(root)
    value = _provider_state(state, provider_name)
    incident = value.get("incident")
    if isinstance(incident, dict) and incident.get("state") == "open":
        closed = dict(incident)
        closed["state"] = "closed"
        closed["closedAt"] = now_iso(current)
        closed["closeReason"] = str(reason)
        closed["closeEvidence"] = evidence if evidence is not None else {}
        value["lastClosedIncident"] = closed
        value["incident"] = None
    _event(value, "incident_closed", {"reason": reason, "evidence": evidence}, current=current)
    _save(root, state, current=current)
    return gate(root, provider_name)


def record_stable_success(
    root: Path,
    provider_name: str,
    evidence: Any = None,
    *,
    current: datetime | None = None,
) -> dict[str, Any]:
    """Stable model completion is positive evidence that closes the incident."""
    state = load_state(root)
    value = _provider_state(state, provider_name)
    value["lastStableSuccessAt"] = now_iso(current)
    _save(root, state, current=current)
    return close_incident(root, provider_name, "stable_success", evidence, current=current)


def clear_after_manual_transition(root: Path, provider_name: str) -> dict[str, Any]:
    """A verified operator transition is an explicit new-incident boundary."""
    state = load_state(root)
    value = _provider_state(state, provider_name)
    value["lastManualTransitionAt"] = now_iso()
    _save(root, state)
    return close_incident(root, provider_name, "verified_manual_transition", {"operatorVerified": True})
