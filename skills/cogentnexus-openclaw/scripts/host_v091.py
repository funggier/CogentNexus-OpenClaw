#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.1 Host façade.

The proven v0.9.4-era v0.9.1 hardening payload remains executable unchanged.
This façade removes only the legacy global provider-lifecycle request from the
transactional enable path. OpenClaw owns provider/model/auth routing in v0.9.5.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable


_WRAPPER_NAME = __name__
_LEGACY_PATH = Path(__file__).with_name("host_v091_legacy_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_host_v091_legacy_v094_embedded"
try:
    exec(compile(_LEGACY_PATH.read_text(encoding="utf-8"), str(_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME


_WAKE_PATH = Path(__file__).with_name("wake_authority_v095.py")
_WAKE_MODULE_NAME = "cogentnexus_openclaw_wake_authority_v095"
_WAKE_SPEC = importlib.util.spec_from_file_location(_WAKE_MODULE_NAME, _WAKE_PATH)
assert _WAKE_SPEC and _WAKE_SPEC.loader
_WAKE_MODULE = importlib.util.module_from_spec(_WAKE_SPEC)
sys.modules[_WAKE_MODULE_NAME] = _WAKE_MODULE
try:
    _WAKE_SPEC.loader.exec_module(_WAKE_MODULE)
except Exception:
    sys.modules.pop(_WAKE_MODULE_NAME, None)
    raise
WakeDecision = _WAKE_MODULE.WakeDecision
classify_wake = _WAKE_MODULE.classify_wake

_LEGACY_ENABLE = enable
_LEGACY_SUPERVISOR_TICK = supervisor_tick


def _provider_neutral_runtime(original: Callable[..., Any]) -> Callable[..., Any]:
    """Drop only the obsolete global provider-start request from enable."""
    def invoke(root: Path, *args: str, **kwargs: Any):
        values = list(args)
        if len(values) >= 2 and values[0] == "lifecycle" and values[1] == "start":
            values = [value for value in values if value != "--provider"]
        return original(root, *values, **kwargs)

    return invoke


def enable(root: Path) -> dict[str, Any]:
    """Run the proven transactional enable path without provider ownership."""
    original_runtime = legacy.runtime
    legacy.runtime = _provider_neutral_runtime(original_runtime)
    try:
        return _LEGACY_ENABLE(root)
    finally:
        legacy.runtime = original_runtime



def _read_maintenance_marker(root: Path) -> dict[str, Any] | None:
    """Read the CNX runtime maintenance marker without mutating runtime state."""
    path = root.resolve() / "runtime" / "maintenance.json"
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        return {
            "active": True,
            "recoveryPolicy": "invalid",
            "error": f"invalid-maintenance-marker:{error}",
        }
    if not isinstance(value, dict):
        return {
            "active": True,
            "recoveryPolicy": "invalid",
            "error": "invalid-maintenance-marker:expected-object",
        }
    return value


def _reconcile_healthy_runtime_marker(root: Path, execute_safe: bool) -> dict[str, Any] | None:
    """Retire recoverable restart maintenance through the supported lifecycle path."""
    marker = _read_maintenance_marker(root)
    if not marker or not marker.get("active"):
        return None

    policy = str(marker.get("recoveryPolicy") or "")
    if policy != "healthy-runtime":
        return {
            "status": "blocked",
            "result": "maintenance-recovery-pending",
            "recoveryPolicy": policy or "unknown",
            "marker": marker,
        }

    if not execute_safe:
        return {
            "status": "pending",
            "result": "maintenance-recovery-pending",
            "recoveryPolicy": policy,
        }

    lifecycle = legacy.runtime(root, "lifecycle", "start", timeout=60, check=False)
    after = _read_maintenance_marker(root)
    marker_active = bool(after and after.get("active"))
    if lifecycle.returncode != 0 or marker_active:
        return {
            "status": "incomplete",
            "result": "maintenance-recovery-incomplete",
            "recoveryPolicy": policy,
            "exitCode": int(lifecycle.returncode),
            "markerStillActive": marker_active,
        }

    return {
        "status": "reconciled",
        "result": "maintenance-reconciled",
        "recoveryPolicy": policy,
        "exitCode": int(lifecycle.returncode),
    }


def durable_work_hint(root: Path, now: str | None = None) -> bool:
    """Compatibility boolean backed exclusively by the canonical wake authority."""
    parsed_now = _parse_iso_timestamp(now) if now else None
    return bool(classify_wake(root, parsed_now).actionable)


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    """Use one canonical durable wake decision before provider/heavy work."""
    legacy.initialize(root)
    state = legacy.load_state(root)
    if state.get("mode") != "managed":
        return {"result": "passthrough", "mode": state.get("mode"), "action": "none"}
    if state.get("desiredGateway") != "running":
        return {"result": "maintenance", "desiredGateway": state.get("desiredGateway"), "action": "none"}

    gateway_ok = gateway_fast_probe()
    hard_hang_restart = None
    if not gateway_ok:
        time.sleep(HARD_HANG_CONFIRM_DELAY_SECONDS)
        gateway_ok = gateway_fast_probe()
        if not gateway_ok:
            if execute_safe:
                hard_hang_restart = _restart_unresponsive_gateway(root)
                return {
                    "result": "gateway-recovery",
                    "action": "gateway-recovery",
                    "wakeAuthority": "none",
                    "wakeWorkId": None,
                    "wakeReason": "gateway/unresponsive",
                    "probe": "lightweight-http+sqlite-ro",
                    "gatewayHealthy": False,
                    "durableWorkPending": False,
                    "providerRequired": False,
                    "heavyPath": False,
                    "hardHangRecovery": hard_hang_restart,
                }
            return {
                "result": "gateway-unhealthy",
                "action": "gateway-status",
                "wakeAuthority": "none",
                "wakeWorkId": None,
                "wakeReason": "gateway/unresponsive",
                "probe": "lightweight-http+sqlite-ro",
                "gatewayHealthy": False,
                "durableWorkPending": False,
                "providerRequired": False,
                "heavyPath": False,
            }

    maintenance_recovery = _reconcile_healthy_runtime_marker(root, execute_safe)
    if maintenance_recovery is not None and maintenance_recovery.get("status") != "reconciled":
        return {
            "result": maintenance_recovery["result"],
            "action": "none",
            "recoveryPolicy": maintenance_recovery.get("recoveryPolicy"),
            "gatewayHealthy": gateway_ok,
            "durableWorkPending": False,
            "providerRequired": False,
            "heavyPath": False,
            "maintenanceRecovery": maintenance_recovery,
        }

    decision = classify_wake(root)
    if not decision.actionable:
        result: dict[str, Any] = {
            "result": "idle",
            "action": "none",
            "wakeAuthority": decision.authority,
            "wakeWorkId": decision.work_id,
            "wakeReason": decision.reason,
            "probe": "lightweight-http+sqlite-ro",
            "gatewayHealthy": gateway_ok,
            "providerRequired": False,
            "providerHealthy": None,
            "durableWorkPending": False,
            "heavyPath": False,
        }
        if maintenance_recovery is not None:
            result["maintenanceRecovery"] = maintenance_recovery
        return result

    result = _LEGACY_SUPERVISOR_TICK(root, execute_safe)
    if isinstance(result, dict):
        result = dict(result)
        result.setdefault("wakeAuthority", decision.authority)
        result.setdefault("wakeWorkId", decision.work_id)
        result.setdefault("wakeReason", decision.reason)
        result.setdefault("heavyPath", True)
    return result


legacy.durable_work_hint = durable_work_hint
legacy.enable = enable
legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
