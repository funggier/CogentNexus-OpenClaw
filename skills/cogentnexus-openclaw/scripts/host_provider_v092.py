#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.2 provider-neutral, event-authorized Host overlay.

The accepted v0.9.1 Ticket, delivery, single-authority and Direct-recovery
fences remain authoritative. v0.9.2 changes the provider boundary and recovery
authorization: elapsed time is only a reconciliation/safety checkpoint. It does
not by itself authorize a provider restart or repeated inference.

Provider failure evidence opens a durable incident. Stable model completion or
a verified operator transition closes it. A healthy provider + healthy Gateway
+ silent model call is treated as active/unknown work, never as proof of death.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import host_stall_v091 as stall
import provider as providers
import provider_events_v092 as provider_events
import provider_recovery_v092 as recovery_policy

legacy = stall.legacy
v091 = stall.v091
ORIGINAL_RUNTIME = legacy.runtime
BASE_SUPERVISOR_TICK = stall.BASE_SUPERVISOR_TICK
HERE = Path(__file__).resolve()

SUCCESS_OUTCOMES = {"ok", "success", "completed", "stop", "agent_end_ok"}
FAILURE_INCIDENTS = {"provider_dead", "provider_unreachable", "provider_connection_refused"}


def startup_path_v092() -> Path:
    return HERE.with_name("startup_v092.py")


legacy.startup_path = startup_path_v092


def _state_provider(root: Path) -> str | None:
    override = os.environ.get("CNXCLAW_PROVIDER_TARGET")
    if override:
        return providers.normalize_provider(override)
    state = legacy.load_state(root)
    transition = state.get("providerTransition")
    if isinstance(transition, dict) and transition.get("to"):
        return providers.normalize_provider(str(transition["to"]))
    selected = state.get("selectedProvider")
    if selected:
        return providers.normalize_provider(str(selected))
    installed = providers.installed_providers()
    return installed[0] if len(installed) == 1 else None


def _runtime_config_path(root: Path) -> Path:
    return root / "runtime" / "config.json"


def _set_legacy_ollama_mode(root: Path, selected: str | None) -> dict[str, Any]:
    """Keep the v0.9.1 generic supervisor from reviving an unselected Ollama."""
    path = _runtime_config_path(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schemaVersion": 1}
    except Exception as error:
        raise RuntimeError(f"invalid CogentNexus-OpenClaw runtime config: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError("CogentNexus-OpenClaw runtime config must be a JSON object")
    supervisor = value.get("supervisor") if isinstance(value.get("supervisor"), dict) else {}
    desired = "auto" if selected == "ollama" else "disabled"
    previous = supervisor.get("ollamaMode")
    if previous == desired:
        return {"changed": False, "before": previous, "after": desired}
    supervisor["ollamaMode"] = desired
    value["supervisor"] = supervisor
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return {"changed": True, "before": previous, "after": desired}


def _parse_stdout(value: str | None) -> Any:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _completed(args: list[str], returncode: int, payload: dict[str, Any], stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        stderr=stderr,
    )


def _finish(result: subprocess.CompletedProcess[str], check: bool) -> subprocess.CompletedProcess[str]:
    if check and result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "provider-aware runtime lifecycle failed").strip())
    return result


def provider_aware_runtime(root: Path, *args: str, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Translate legacy lifecycle --provider into the selected provider adapter.

    Gateway is quiesced before provider stop, and provider readiness is verified
    before Gateway start. This preserves the accepted v0.9.1 recovery ordering.
    """
    values = list(args)
    provider_requested = "--provider" in values
    lifecycle = len(values) >= 2 and values[0] == "lifecycle"
    action = values[1] if lifecycle else None
    if not provider_requested or action not in {"start", "stop"}:
        return ORIGINAL_RUNTIME(root, *args, timeout=timeout, check=check)

    target = _state_provider(root)
    cleaned = [value for value in values if value != "--provider"]
    command = [sys.executable, str(legacy.runtime_path()), "--root", str(root), *cleaned]
    if not target:
        return _finish(_completed(command, 2, {
            "result": "error",
            "error": "provider selection required; use cnxclaw start --provider ollama|lmstudio",
            "provider": None,
        }), check)

    _set_legacy_ollama_mode(root, target)
    if action == "start":
        provider_result = providers.start(target, timeout=min(60.0, float(timeout)))
        if not provider_result.get("ok"):
            return _finish(_completed(command, 2, {
                "result": "error",
                "phase": "provider-start",
                "provider": target,
                "providerLifecycle": provider_result,
            }), check)
        runtime_result = ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
        return _finish(_completed(command, runtime_result.returncode, {
            "provider": target,
            "providerLifecycle": provider_result,
            "runtime": _parse_stdout(runtime_result.stdout),
        }, runtime_result.stderr or ""), check)

    runtime_result = ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
    if runtime_result.returncode != 0:
        return _finish(runtime_result, check)
    provider_result = providers.stop(target, timeout=min(60.0, float(timeout)))
    code = 0 if provider_result.get("ok") else 2
    return _finish(_completed(command, code, {
        "provider": target,
        "runtime": _parse_stdout(runtime_result.stdout),
        "providerLifecycle": provider_result,
        "safeToPowerOff": code == 0,
    }), check)


legacy.runtime = provider_aware_runtime


def _run_base_supervisor(root: Path, execute_safe: bool, provider_healthy: bool) -> dict[str, Any]:
    """Reuse v0.9.1 reconciliation while suppressing timer-only model recovery."""
    original_probe = v091.ollama_fast_probe
    original_claim = stall.claim_expired_direct_model_call
    v091.ollama_fast_probe = lambda: provider_healthy
    stall.claim_expired_direct_model_call = lambda _root: None
    try:
        return BASE_SUPERVISOR_TICK(root, execute_safe)
    finally:
        v091.ollama_fast_probe = original_probe
        stall.claim_expired_direct_model_call = original_claim


def _provider_ref_matches(target: str, value: Any) -> bool:
    text = str(value or "").strip().lower().replace("-", "")
    if target == "lmstudio":
        return "lmstudio" in text
    return text == "ollama" or text.startswith("ollama/")


def _incident_record(root: Path, target: str) -> dict[str, Any] | None:
    state = recovery_policy.load_state(root)
    providers_state = state.get("providers") if isinstance(state.get("providers"), dict) else {}
    value = providers_state.get(target) if isinstance(providers_state.get(target), dict) else {}
    incident = value.get("incident") if isinstance(value, dict) else None
    return incident if isinstance(incident, dict) and incident.get("state") == "open" else None


def _reconcile_stable_success(root: Path, target: str) -> dict[str, Any] | None:
    """Close an open provider incident from a durable successful model-call event."""
    incident = _incident_record(root, target)
    if incident is None:
        return None
    opened_at = str(incident.get("openedAt") or "")
    path = legacy.ticket_db(root)
    if not path.exists():
        return None
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not stall._model_call_table(db):
            return None
        rows = db.execute(
            "SELECT ticket_id,run_id,call_id,provider,model,outcome,ended_at,updated_at "
            "FROM cnx_direct_model_call WHERE state='ended' AND updated_at>=? "
            "ORDER BY updated_at DESC LIMIT 25",
            (opened_at,),
        ).fetchall()
    finally:
        db.close()
    for row in rows:
        outcome = str(row["outcome"] or "").strip().lower()
        if outcome not in SUCCESS_OUTCOMES or not _provider_ref_matches(target, row["provider"]):
            continue
        evidence = {
            "source": "direct_model_call_ended",
            "ticketId": row["ticket_id"],
            "runId": row["run_id"],
            "callId": row["call_id"],
            "provider": row["provider"],
            "model": row["model"],
            "outcome": row["outcome"],
            "endedAt": row["ended_at"],
        }
        closed = recovery_policy.record_stable_success(root, target, evidence)
        provider_events.publish(root, target, "stable_success", evidence)
        return closed
    return None


def _mark_active_calls_provider_failed(root: Path, target: str, classification: str, evidence: Any) -> int:
    """Turn explicit provider failure evidence into an immediately claimable lease."""
    path = legacy.ticket_db(root)
    if not path.exists():
        return 0
    stamp = datetime.now(timezone.utc).isoformat()
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    changed_count = 0
    try:
        if not stall._model_call_table(db) or not v091._db_table_exists(db, "tickets"):
            return 0
        db.execute("BEGIN IMMEDIATE")
        rows = db.execute(
            "SELECT m.ticket_id,m.run_id,m.call_id,m.provider,m.model "
            "FROM cnx_direct_model_call m JOIN tickets t ON t.ticket_id=m.ticket_id "
            "WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL "
            "AND t.response_ready_at IS NULL AND m.state='active'"
        ).fetchall()
        for row in rows:
            if not _provider_ref_matches(target, row["provider"]):
                continue
            marker = f"provider-event:{classification}"
            changed = db.execute(
                "UPDATE cnx_direct_model_call SET deadline_at=?,outcome=?,updated_at=? "
                "WHERE ticket_id=? AND call_id=? AND state='active'",
                (stamp, marker, stamp, row["ticket_id"], row["call_id"]),
            )
            if changed.rowcount != 1:
                continue
            changed_count += 1
            if v091._db_table_exists(db, "ticket_events"):
                db.execute(
                    "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                    (
                        row["ticket_id"],
                        "host_direct_model_provider_failure",
                        json.dumps({
                            "runId": row["run_id"],
                            "callId": row["call_id"],
                            "provider": row["provider"],
                            "model": row["model"],
                            "classification": classification,
                            "recoveryAuthority": "explicit-provider-failure-event",
                            "evidence": evidence,
                        }, ensure_ascii=False),
                        stamp,
                    ),
                )
        db.commit()
        return changed_count
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _progress_for_call(root: Path, target: str, started_at: str) -> dict[str, Any] | None:
    progress = provider_events.latest_progress(root, target)
    if not isinstance(progress, dict):
        return None
    event_at = str(progress.get("at") or "")
    if not event_at or event_at < str(started_at or ""):
        return None
    return progress


def _guard_healthy_active_call(root: Path, target: str) -> dict[str, Any] | None:
    """Prevent elapsed lease age from becoming destructive recovery authority."""
    path = legacy.ticket_db(root)
    if not path.exists():
        return None
    now_value = datetime.now(timezone.utc).isoformat()
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not stall._model_call_table(db) or not v091._db_table_exists(db, "tickets"):
            return None
        rows = db.execute(
            "SELECT m.ticket_id,m.run_id,m.call_id,m.provider,m.model,m.started_at,m.deadline_at,m.outcome "
            "FROM cnx_direct_model_call m JOIN tickets t ON t.ticket_id=m.ticket_id "
            "WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL "
            "AND t.response_ready_at IS NULL AND m.state='active' AND m.deadline_at<=? "
            "ORDER BY m.deadline_at,m.ticket_id LIMIT 10",
            (now_value,),
        ).fetchall()
        selected = next((item for item in rows if _provider_ref_matches(target, item["provider"])), None)
        if selected is None:
            return None

        progress = _progress_for_call(root, target, selected["started_at"])
        classification = "active_model_processing" if progress is not None else "active_model_processing_unknown"
        decision_source = (
            "provider-runtime-prompt-progress"
            if progress is not None
            else "provider-and-gateway-healthy-without-explicit-failure-event"
        )
        already = None
        if v091._db_table_exists(db, "ticket_events"):
            candidates = db.execute(
                "SELECT payload_json FROM ticket_events WHERE ticket_id=? AND event_type='host_direct_model_waiting_for_event_evidence' ORDER BY created_at DESC LIMIT 10",
                (selected["ticket_id"],),
            ).fetchall()
            for candidate in candidates:
                try:
                    value = json.loads(candidate["payload_json"] or "{}")
                except Exception:
                    continue
                if value.get("callId") == selected["call_id"]:
                    already = value
                    break

        payload = {
            "runId": selected["run_id"],
            "callId": selected["call_id"],
            "provider": selected["provider"],
            "model": selected["model"],
            "startedAt": selected["started_at"],
            "deadlineAt": selected["deadline_at"],
            "classification": classification,
            "decisionSource": decision_source,
            "providerProgress": progress,
            "recoveryEligible": False,
            "providerRestart": False,
        }
        if already is None and v091._db_table_exists(db, "ticket_events"):
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (
                    selected["ticket_id"],
                    "host_direct_model_waiting_for_event_evidence",
                    json.dumps(payload, ensure_ascii=False),
                    now_value,
                ),
            )
            db.commit()
        return {"result": classification.replace("_", "-"), "ticketId": selected["ticket_id"], **payload}
    finally:
        db.close()


def _circuit_open_result(root: Path, execute_safe: bool, target: str, current: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    result = _run_base_supervisor(root, execute_safe, bool(current.get("healthy")))
    result["selectedProvider"] = target
    result["providerHealth"] = current
    result["providerRecovery"] = {
        "classification": "provider_recovery_circuit_open",
        "recoveryEligible": False,
        "providerRestart": False,
        "gate": gate,
    }
    result["result"] = "provider-recovery-circuit-open"
    return result


def _recover_claimed_direct_call(root: Path, target: str, before: dict[str, Any], provider_recovery: dict[str, Any] | None) -> dict[str, Any] | None:
    gate = recovery_policy.gate(root, target)
    if not gate.get("allowed"):
        return None
    claim = stall.claim_expired_direct_model_call(root)
    if claim is None:
        return None
    try:
        recovered = stall.recover_expired_direct_model_call(root, claim)
        gate_after = recovery_policy.record_attempt(
            root,
            target,
            success=True,
            reason="direct-model-call-recovery-authorized-by-provider-failure-event",
            evidence={"claim": claim},
        )
        recovered["selectedProvider"] = target
        recovered["providerHealthBefore"] = before
        recovered["providerRecoveryBeforeStall"] = provider_recovery
        recovered["providerRecoveryPolicy"] = gate_after
        recovered["recoveryAuthority"] = "provider-failure-incident"
        return recovered
    except Exception as error:
        try:
            recovery_policy.record_attempt(
                root,
                target,
                success=False,
                reason=f"direct-model-call-recovery-error:{error}",
                evidence={"claim": claim},
            )
        except Exception:
            pass
        try:
            stall._release_model_call_claim(root, claim, str(error))
        except Exception:
            pass
        raise


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    state = legacy.load_state(root)
    if state.get("mode") != "managed" or state.get("desiredGateway") != "running":
        return _run_base_supervisor(root, execute_safe, True)

    target = _state_provider(root)
    if not target:
        _set_legacy_ollama_mode(root, None)
        result = _run_base_supervisor(root, execute_safe, True)
        result["selectedProvider"] = None
        result["providerHealth"] = {"healthy": False, "error": "provider selection required"}
        result["providerRecovery"] = "none"
        result["result"] = "provider-selection-required"
        return result

    _set_legacy_ollama_mode(root, target)
    adapter = provider_events.ensure_adapter(root, target)
    failure_event = provider_events.consume_failure(root, target)
    stable = _reconcile_stable_success(root, target)

    if failure_event is not None:
        classification = str(failure_event.get("type") or "provider_dead")
        recovery_policy.begin_incident(root, target, classification, failure_event)
        _mark_active_calls_provider_failed(root, target, classification, failure_event)

    before = providers.probe(target, timeout=3.0)
    current = before
    recovery: dict[str, Any] | None = None

    if state.get("desiredProvider") == "running" and not before.get("healthy"):
        classification = (
            str(failure_event.get("type"))
            if isinstance(failure_event, dict) and failure_event.get("type") in FAILURE_INCIDENTS
            else "provider_unreachable"
        )
        gate = recovery_policy.begin_incident(root, target, classification, {
            "source": "provider-health-reconciliation",
            "probe": before,
            "providerEvent": failure_event,
        })
        marked = _mark_active_calls_provider_failed(root, target, classification, before)
        if execute_safe:
            if not gate.get("allowed"):
                result = _circuit_open_result(root, execute_safe, target, current, gate)
                result["providerEventAdapter"] = adapter
                return result
            recovery = providers.start(target, timeout=45)
            current = providers.probe(target, timeout=3.0)
            gate = recovery_policy.record_attempt(
                root,
                target,
                success=bool(recovery.get("ok") and current.get("healthy")),
                reason="provider-failure-event-recovery",
                evidence={"before": before, "after": current, "markedModelCalls": marked, "providerEvent": failure_event},
            )
            recovery = {**recovery, "recoveryPolicy": gate}
            if current.get("healthy"):
                provider_events.publish(root, target, "provider_ready", {"afterAutomaticRecovery": True, "health": current})

    gate = recovery_policy.gate(root, target)
    if state.get("desiredProvider") == "running" and not current.get("healthy"):
        result = _run_base_supervisor(root, execute_safe, False)
        result["selectedProvider"] = target
        result["providerHealth"] = current
        result["providerRecovery"] = recovery or "none"
        result["providerRecoveryPolicy"] = gate
        result["providerEventAdapter"] = adapter
        result["result"] = "provider-degraded"
        return result

    gateway_healthy = bool(v091.gateway_fast_probe())
    if execute_safe and current.get("healthy") and gateway_healthy:
        incident = _incident_record(root, target)
        if incident is not None and incident.get("classification") in FAILURE_INCIDENTS:
            gate = recovery_policy.gate(root, target)
            if not gate.get("allowed"):
                result = _circuit_open_result(root, execute_safe, target, current, gate)
                result["providerEventAdapter"] = adapter
                return result
            recovered = _recover_claimed_direct_call(root, target, before, recovery)
            if recovered is not None:
                recovered["providerEventAdapter"] = adapter
                return recovered

        guarded = _guard_healthy_active_call(root, target)
        if guarded is not None:
            result = _run_base_supervisor(root, execute_safe, True)
            result["selectedProvider"] = target
            result["providerHealth"] = current
            result["providerRecovery"] = recovery or "none"
            result["providerRecoveryPolicy"] = recovery_policy.gate(root, target)
            result["providerEventAdapter"] = adapter
            result["modelCallClassification"] = guarded
            result["result"] = "waiting-for-model-event-evidence"
            return result

    result = _run_base_supervisor(root, execute_safe, bool(current.get("healthy")))
    result["selectedProvider"] = target
    result["providerHealth"] = current
    result["providerRecovery"] = recovery or "none"
    result["providerRecoveryPolicy"] = recovery_policy.gate(root, target)
    result["providerEventAdapter"] = adapter
    if stable is not None:
        result["providerStableSuccess"] = stable
    return result


legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
