#!/usr/bin/env python3
"""CogentNexus v0.9.2 provider-neutral Host overlay.

The accepted v0.9.1 Ticket, delivery, single-authority and Direct-stall recovery
logic remains unchanged. This layer replaces only the local provider lifecycle
boundary so `--provider` means the durable selected provider (Ollama or LM
Studio), not hard-coded Ollama.

v0.9.2 additionally adds two provider-specific recovery guards:
- one bounded LM Studio long-running grace before a healthy endpoint is treated
  as a stalled Direct call;
- a durable automatic-recovery circuit breaker so Host recovery cannot loop
  provider restarts indefinitely.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import host_stall_v091 as stall
import provider as providers
import provider_recovery_v092 as recovery_policy

legacy = stall.legacy
v091 = stall.v091
ORIGINAL_RUNTIME = legacy.runtime
BASE_SUPERVISOR_TICK = stall.BASE_SUPERVISOR_TICK
HERE = Path(__file__).resolve()


def startup_path_v092() -> Path:
    return HERE.with_name("startup_v092.py")


legacy.startup_path = startup_path_v092


def _state_provider(root: Path) -> str | None:
    override = os.environ.get("CNX_PROVIDER_TARGET")
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
        raise RuntimeError(f"invalid CogentNexus runtime config: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError("CogentNexus runtime config must be a JSON object")
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
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=json.dumps(payload, ensure_ascii=False, indent=2) + "\n", stderr=stderr)


def _finish(result: subprocess.CompletedProcess[str], check: bool) -> subprocess.CompletedProcess[str]:
    if check and result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "provider-aware runtime lifecycle failed").strip())
    return result


def provider_aware_runtime(root: Path, *args: str, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Translate legacy lifecycle --provider into the selected provider adapter.

    Gateway is always quiesced before provider stop, and provider readiness is
    verified before Gateway start. This preserves the v0.9.1 recovery ordering.
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
            "error": "provider selection required; use cnx start --provider ollama|lmstudio",
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
        payload = {
            "provider": target,
            "providerLifecycle": provider_result,
            "runtime": _parse_stdout(runtime_result.stdout),
        }
        return _finish(_completed(command, runtime_result.returncode, payload, runtime_result.stderr or ""), check)

    runtime_result = ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
    if runtime_result.returncode != 0:
        return _finish(runtime_result, check)
    provider_result = providers.stop(target, timeout=min(60.0, float(timeout)))
    code = 0 if provider_result.get("ok") else 2
    payload = {
        "provider": target,
        "runtime": _parse_stdout(runtime_result.stdout),
        "providerLifecycle": provider_result,
        "safeToPowerOff": code == 0,
    }
    return _finish(_completed(command, code, payload), check)


legacy.runtime = provider_aware_runtime


def _run_base_supervisor(root: Path, execute_safe: bool, provider_healthy: bool) -> dict[str, Any]:
    """Reuse v0.9.1 idle/hard-hang logic without an Ollama-only fast-probe bias."""
    original_probe = v091.ollama_fast_probe
    v091.ollama_fast_probe = lambda: provider_healthy
    try:
        return BASE_SUPERVISOR_TICK(root, execute_safe)
    finally:
        v091.ollama_fast_probe = original_probe


def _defer_lmstudio_long_running_call(root: Path, grace_seconds: int) -> dict[str, Any] | None:
    """Give one healthy LM Studio Direct call a bounded prefill grace.

    The OpenAI-compatible stream exposes no prompt-processing progress. Live
    testing proved valid cold prefill can remain silent for >360 seconds. When
    both Gateway and provider endpoints are healthy, the first expired LM Studio
    call is therefore reclassified as `cold_model_long_running` and its durable
    deadline is extended once without restarting the provider or consuming a
    recovery attempt. A second expiry falls back to the accepted v0.9.1 recovery.
    """
    if grace_seconds <= 0:
        return None
    path = legacy.ticket_db(root)
    if not path.exists():
        return None

    now = datetime.now(timezone.utc)
    now_value = now.isoformat()
    deadline = (now + timedelta(seconds=grace_seconds)).isoformat()
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not stall._model_call_table(db) or not v091._db_table_exists(db, "tickets"):
            return None
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT m.ticket_id,m.run_id,m.call_id,m.provider,m.model,m.started_at,m.deadline_at,m.outcome,"
            "m.recovery_attempt_count,t.owner_session_key "
            "FROM cnx_direct_model_call m JOIN tickets t ON t.ticket_id=m.ticket_id "
            "WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL "
            "AND t.response_ready_at IS NULL AND m.state='active' AND m.deadline_at<=? "
            "AND m.recovery_attempt_count=0 "
            "AND LOWER(COALESCE(m.provider,'')) LIKE '%lmstudio%' "
            "AND COALESCE(m.outcome,'') NOT LIKE 'cold-model-long-running-grace:%' "
            "ORDER BY m.deadline_at,m.ticket_id LIMIT 1",
            (now_value,),
        ).fetchone()
        if row is None:
            db.commit()
            return None

        marker = f"cold-model-long-running-grace:{grace_seconds}s"
        changed = db.execute(
            "UPDATE cnx_direct_model_call SET deadline_at=?,outcome=?,updated_at=? "
            "WHERE ticket_id=? AND call_id=? AND state='active' AND recovery_attempt_count=0",
            (deadline, marker, now_value, row["ticket_id"], row["call_id"]),
        )
        if changed.rowcount != 1:
            db.rollback()
            return None

        if v091._db_table_exists(db, "ticket_events"):
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (
                    row["ticket_id"],
                    "host_direct_model_long_running_grace",
                    json.dumps({
                        "runId": row["run_id"],
                        "callId": row["call_id"],
                        "provider": row["provider"],
                        "model": row["model"],
                        "startedAt": row["started_at"],
                        "deadlineBefore": row["deadline_at"],
                        "deadlineAfter": deadline,
                        "classification": "cold_model_long_running",
                        "recoveryEligible": False,
                        "providerRestart": False,
                        "graceSeconds": grace_seconds,
                        "source": "host-v092-provider-evidence",
                    }, ensure_ascii=False),
                    now_value,
                ),
            )
        db.commit()
        return {
            "result": "cold-model-long-running",
            "classification": "cold_model_long_running",
            "ticketId": row["ticket_id"],
            "callId": row["call_id"],
            "provider": row["provider"],
            "model": row["model"],
            "deadlineBefore": row["deadline_at"],
            "deadlineAfter": deadline,
            "graceSeconds": grace_seconds,
            "recoveryEligible": False,
            "providerRestart": False,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _circuit_open_result(
    root: Path,
    execute_safe: bool,
    target: str,
    current: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    result = _run_base_supervisor(root, execute_safe, True)
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
    before = providers.probe(target, timeout=3.0)
    recovery: dict[str, Any] | None = None
    current = before
    gate = recovery_policy.gate(root, target)

    if state.get("desiredProvider") == "running" and not before.get("healthy") and execute_safe:
        if gate.get("allowed"):
            recovery = providers.start(target, timeout=45)
            current = providers.probe(target, timeout=3.0)
            gate = recovery_policy.record_attempt(
                root,
                target,
                success=bool(recovery.get("ok") and current.get("healthy")),
                reason="provider-endpoint-unhealthy",
            )
            recovery = {**recovery, "recoveryPolicy": gate}
        else:
            return _circuit_open_result(root, execute_safe, target, current, gate)

    if state.get("desiredProvider") == "running" and not current.get("healthy"):
        result = _run_base_supervisor(root, execute_safe, True)
        result["selectedProvider"] = target
        result["providerHealth"] = current
        result["providerRecovery"] = recovery or "none"
        result["providerRecoveryPolicy"] = gate
        result["result"] = "provider-degraded"
        return result

    if execute_safe and current.get("healthy") and v091.gateway_fast_probe():
        if target == "lmstudio":
            deferred = _defer_lmstudio_long_running_call(
                root,
                recovery_policy.policy(target)["longRunningGraceSeconds"],
            )
            if deferred is not None:
                result = _run_base_supervisor(root, execute_safe, True)
                result["selectedProvider"] = target
                result["providerHealth"] = current
                result["providerRecovery"] = recovery or "none"
                result["providerRecoveryPolicy"] = gate
                result["modelCallClassification"] = deferred
                result["result"] = "cold-model-long-running"
                return result

        gate = recovery_policy.gate(root, target)
        if not gate.get("allowed"):
            return _circuit_open_result(root, execute_safe, target, current, gate)

        claim = stall.claim_expired_direct_model_call(root)
        if claim is not None:
            try:
                recovered = stall.recover_expired_direct_model_call(root, claim)
                gate_after = recovery_policy.record_attempt(
                    root,
                    target,
                    success=True,
                    reason="direct-model-call-stall-recovery",
                )
                recovered["selectedProvider"] = target
                recovered["providerHealthBefore"] = before
                recovered["providerRecoveryBeforeStall"] = recovery
                recovered["providerRecoveryPolicy"] = gate_after
                return recovered
            except Exception as error:
                try:
                    recovery_policy.record_attempt(
                        root,
                        target,
                        success=False,
                        reason=f"direct-model-call-stall-recovery-error:{error}",
                    )
                except Exception:
                    pass
                try:
                    stall._release_model_call_claim(root, claim, str(error))
                except Exception:
                    pass
                raise

    result = _run_base_supervisor(root, execute_safe, bool(current.get("healthy")))
    result["selectedProvider"] = target
    result["providerHealth"] = current
    result["providerRecovery"] = recovery or "none"
    result["providerRecoveryPolicy"] = recovery_policy.gate(root, target)
    return result


legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
