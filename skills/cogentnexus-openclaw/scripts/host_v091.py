#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.1 Host façade.

The proven v0.9.4-era v0.9.1 hardening payload remains executable unchanged.
This façade removes only the legacy global provider-lifecycle request from the
transactional enable path. OpenClaw owns provider/model/auth routing in v0.9.5.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
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
GATEWAY_STARTUP_GRACE_SECONDS = 180.0


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


GATEWAY_HARD_HANG_REASON = "CogentNexus-OpenClaw external supervisor confirmed an unresponsive Gateway"


def _recover_gateway_interrupted_direct_calls(
    root: Path,
    interruption_evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    """Classify only exact Direct calls captured before Gateway quiescence."""
    import host_stall_v091 as stall

    return stall.classify_quiesced_gateway_interrupted_direct_calls(
        root,
        interruption_evidence=interruption_evidence,
    )


def _gateway_current_direct_evidence(root: Path) -> dict[str, Any] | None:
    """Snapshot exact active Direct calls owned by the Gateway being replaced."""
    import host_stall_v091 as stall

    if not stall.has_active_direct_model_calls(root):
        return None
    boundary = _current_gateway_boot_boundary(require_healthy=False)
    if boundary is None:
        return None
    calls = stall.find_current_gateway_direct_calls(root, boundary["startedAt"])
    if not calls:
        return None
    return {
        "kind": "confirmed-hard-hang-current-boot",
        "boundary": boundary,
        "orphans": calls,
    }


def _restart_unresponsive_gateway(root: Path) -> dict[str, Any]:
    """Replace a confirmed hung Gateway and authorize only exact interrupted calls.

    Pending Direct recovery rows are committed before the replacement Gateway
    starts so startup liveness can observe them.
    """
    interruption_evidence = _gateway_current_direct_evidence(root)
    prepared = legacy.runtime(
        root,
        "lifecycle",
        "prepare",
        "--reason",
        GATEWAY_HARD_HANG_REASON,
        "--owner",
        "cogentnexus-openclaw-host",
        "--recovery-policy",
        "healthy-runtime",
        timeout=60,
        check=True,
    )
    stopped = False
    started = False
    stop_result = None
    start_result = None
    interrupted: list[dict[str, Any]] = []
    try:
        stopped = True
        stop_result = legacy.runtime(
            root,
            "lifecycle",
            "stop",
            "--reason",
            GATEWAY_HARD_HANG_REASON,
            "--owner",
            "cogentnexus-openclaw-host",
            "--force",
            timeout=240,
            check=True,
        )
        interrupted = (
            _recover_gateway_interrupted_direct_calls(root, interruption_evidence)
            if interruption_evidence is not None
            else []
        )
        start_result = legacy.runtime(root, "lifecycle", "start", timeout=240, check=True)
        started = True
        return {
            "attempted": True,
            "exitCode": int(getattr(start_result, "returncode", 0)),
            "prepared": legacy.parse_json_output(getattr(prepared, "stdout", "") or ""),
            "stopped": legacy.parse_json_output(getattr(stop_result, "stdout", "") or ""),
            "started": legacy.parse_json_output(getattr(start_result, "stdout", "") or ""),
            "interruptionEvidence": interruption_evidence,
            "interruptedDirectRecoveries": interrupted,
        }
    finally:
        if stopped and not started:
            legacy.runtime(root, "lifecycle", "start", timeout=240, check=True)


def _current_gateway_boot_boundary(require_healthy: bool = True) -> dict[str, Any] | None:
    """Resolve the currently running Gateway PID to its OpenClaw boot row."""
    status = legacy.gateway_status() if require_healthy else legacy.gateway_status(timeout=5)
    if require_healthy and not status.get("healthy"):
        return None
    stdout = str(status.get("stdout") or "")
    match = re.search(r"Runtime:\s+running \(pid\s+(\d+)", stdout)
    if not match:
        return None
    pid = int(match.group(1))
    state_dir = Path(os.environ.get("OPENCLAW_STATE_DIR") or (Path.home() / ".openclaw"))
    database = state_dir / "state" / "openclaw.sqlite"
    if not database.exists():
        return None
    try:
        db = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True, timeout=0.1)
        try:
            row = db.execute(
                "SELECT boot_id,pid,started_at_ms FROM gateway_boot_lifecycle "
                "WHERE pid=? ORDER BY started_at_ms DESC LIMIT 1",
                (pid,),
            ).fetchone()
            previous = None
            if row is not None:
                previous = db.execute(
                    "SELECT boot_id,pid,started_at_ms FROM gateway_boot_lifecycle "
                    "WHERE started_at_ms<? ORDER BY started_at_ms DESC LIMIT 1",
                    (int(row[2]),),
                ).fetchone()
        finally:
            db.close()
    except sqlite3.Error:
        return None
    if row is None:
        return None
    started_at_ms = int(row[2])
    started_at = datetime.fromtimestamp(started_at_ms / 1000.0, tz=timezone.utc).isoformat()
    result = {
        "bootId": str(row[0]),
        "pid": int(row[1]),
        "startedAtMs": started_at_ms,
        "startedAt": started_at,
    }
    if previous is not None:
        previous_started_ms = int(previous[2])
        result["previousBootId"] = str(previous[0])
        result["previousPid"] = int(previous[1])
        result["previousStartedAtMs"] = previous_started_ms
        result["previousStartedAt"] = datetime.fromtimestamp(
            previous_started_ms / 1000.0,
            tz=timezone.utc,
        ).isoformat()
    return result


def _gateway_boundary_orphan_evidence(root: Path) -> dict[str, Any] | None:
    """Return exact old-generation Direct calls under the current Gateway boot."""
    import host_stall_v091 as stall

    if not stall.has_active_direct_model_calls(root):
        return None
    boundary = _current_gateway_boot_boundary()
    if boundary is None:
        return None
    predecessor_started_at = boundary.get("previousStartedAt")
    if predecessor_started_at is None:
        return None
    orphans = stall.find_gateway_boundary_orphaned_direct_calls(
        root,
        boundary["startedAt"],
        predecessor_started_at,
    )
    if not orphans:
        return None
    return {"boundary": boundary, "orphans": orphans}


def _recover_gateway_boundary_orphans(root: Path, evidence: dict[str, Any]) -> dict[str, Any]:
    """Quiesce the current Gateway and authorize recovery for exact predecessor work."""
    import host_stall_v091 as stall

    boundary = evidence["boundary"]
    reason = (
        "CogentNexus-OpenClaw current Gateway boot superseded active Direct model work: "
        f"bootId={boundary.get('bootId')} pid={boundary.get('pid')} startedAt={boundary.get('startedAt')}"
    )
    prepared = legacy.runtime(
        root,
        "lifecycle",
        "prepare",
        "--reason",
        reason,
        "--owner",
        "cogentnexus-openclaw-host",
        "--recovery-policy",
        "healthy-runtime",
        timeout=60,
        check=True,
    )
    stopped = False
    started = False
    stop_result = None
    start_result = None
    try:
        stopped = True
        stop_result = legacy.runtime(
            root,
            "lifecycle",
            "stop",
            "--reason",
            reason,
            "--owner",
            "cogentnexus-openclaw-host",
            "--force",
            timeout=240,
            check=True,
        )
        interrupted = stall.classify_quiesced_gateway_interrupted_direct_calls(
            root,
            interruption_evidence=evidence,
        )
        start_result = legacy.runtime(root, "lifecycle", "start", timeout=240, check=True)
        started = True
        return {
            "result": "gateway-boundary-direct-recovery",
            "action": "gateway-boundary-direct-recovery",
            "gatewayBoundary": boundary,
            "detectedOrphans": evidence["orphans"],
            "interruptedDirectRecoveries": interrupted,
            "prepared": legacy.parse_json_output(getattr(prepared, "stdout", "") or ""),
            "stopped": legacy.parse_json_output(getattr(stop_result, "stdout", "") or ""),
            "started": legacy.parse_json_output(getattr(start_result, "stdout", "") or ""),
        }
    finally:
        if stopped and not started:
            legacy.runtime(root, "lifecycle", "start", timeout=240, check=True)

def durable_work_hint(root: Path, now: str | None = None) -> bool:
    """Compatibility boolean backed exclusively by the canonical wake authority."""
    parsed_now = _parse_iso_timestamp(now) if now else None
    return bool(classify_wake(root, parsed_now).actionable)


def gateway_startup_grace(now_ms: int | None = None) -> dict[str, Any]:
    """Return bounded OpenClaw boot/restart grace from authoritative lifecycle state.

    OpenClaw 2026.9.x may expose its HTTP socket well before plugin/model/channel
    startup reaches ``ready``. A failed lightweight probe during that admitted
    boot window is therefore not proof of a hard hang. The grace is deliberately
    bounded; once it expires, the existing two-probe hard-hang recovery remains
    authoritative.
    """
    state_dir = Path(os.environ.get("OPENCLAW_STATE_DIR") or (Path.home() / ".openclaw"))
    database = state_dir / "state" / "openclaw.sqlite"
    if not database.exists():
        return {"active": False, "reason": "boot-lifecycle-unavailable"}
    try:
        db = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True, timeout=0.1)
        try:
            row = db.execute(
                "SELECT boot_id,started_at_ms,startup_reason FROM gateway_boot_lifecycle "
                "WHERE completed_at_ms IS NULL ORDER BY started_at_ms DESC LIMIT 1"
            ).fetchone()
        finally:
            db.close()
    except sqlite3.Error as error:
        return {"active": False, "reason": "boot-lifecycle-read-failed", "error": str(error)}
    if not row:
        return {"active": False, "reason": "no-active-boot"}
    current_ms = int(time.time() * 1000) if now_ms is None else int(now_ms)
    started_ms = int(row[1])
    age_ms = max(0, current_ms - started_ms)
    grace_ms = int(GATEWAY_STARTUP_GRACE_SECONDS * 1000)
    return {
        "active": age_ms <= grace_ms,
        "bootId": str(row[0]),
        "ageSeconds": round(age_ms / 1000.0, 3),
        "graceSeconds": GATEWAY_STARTUP_GRACE_SECONDS,
        "startupReason": row[2],
        "reason": "active-boot-grace" if age_ms <= grace_ms else "active-boot-grace-expired",
    }


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
            startup_grace = gateway_startup_grace()
            if startup_grace.get("active"):
                return {
                    "result": "gateway-starting",
                    "action": "none",
                    "wakeAuthority": "none",
                    "wakeWorkId": None,
                    "wakeReason": "gateway/startup-grace",
                    "probe": "lightweight-http+sqlite-ro",
                    "gatewayHealthy": False,
                    "durableWorkPending": False,
                    "providerRequired": False,
                    "heavyPath": False,
                    "startupGrace": startup_grace,
                }
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

    if execute_safe:
        gateway_boundary_orphans = _gateway_boundary_orphan_evidence(root)
        if gateway_boundary_orphans is not None:
            return _recover_gateway_boundary_orphans(root, gateway_boundary_orphans)

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
