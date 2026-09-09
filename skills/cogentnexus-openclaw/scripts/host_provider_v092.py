#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.2 Host façade.

The proven v0.9.4-era provider-event and recovery payload remains executable
unchanged behind this compatibility façade. v0.9.5 moves provider/model/auth
routing and provider process lifecycle back to OpenClaw. Legacy provider fields
may remain on disk for migration and diagnostics, but they are not execution
authority.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path


_WRAPPER_NAME = __name__
_LEGACY_PATH = Path(__file__).with_name("host_provider_v092_legacy_v094.py")
globals()["__name__"] = "cogentnexus_openclaw_host_provider_v092_legacy_v094_embedded"
try:
    exec(compile(_LEGACY_PATH.read_text(encoding="utf-8"), str(_LEGACY_PATH), "exec"), globals(), globals())
finally:
    globals()["__name__"] = _WRAPPER_NAME


def provider_aware_runtime(root: Path, *args: str, timeout: int = 180, check: bool = True):
    """Delegate lifecycle operations without taking provider lifecycle authority."""
    values = list(args)
    if len(values) >= 2 and values[0] == "lifecycle" and values[1] in {"start", "stop"}:
        values = [value for value in values if value != "--provider"]
    return ORIGINAL_RUNTIME(root, *values, timeout=timeout, check=check)


# Replace the legacy provider-lifecycle translation surface. The compatibility
# payload remains available for event evidence helpers while lifecycle ownership
# stays with OpenClaw.
legacy.runtime = provider_aware_runtime


def claim_terminal_error_direct_model_call(root: Path, now_iso: str | None = None):
    """Claim one exact terminal model-call failure without provider authority.

    `terminal_error` is written only after OpenClaw has emitted a failing
    `agent_end` for the exact run. The provider/model values on the row are
    therefore provenance, not routing input: this function deliberately never
    normalizes, probes, starts, stops, or selects a provider.
    """
    path = legacy.ticket_db(root)
    if not path.exists():
        return None
    stamp = now_iso or legacy.now_iso()
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not stall._model_call_table(db) or not v091._db_table_exists(db, "tickets"):
            return None
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT m.ticket_id,m.run_id,m.call_id,m.state,m.provider,m.model,m.started_at,m.deadline_at,"
            "m.ended_at,m.outcome,m.error_category,m.failure_kind,m.recovery_started_at,m.recovery_attempt_count,m.updated_at "
            "FROM cnx_direct_model_call m JOIN tickets t ON t.ticket_id=m.ticket_id "
            "WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL "
            "AND t.response_ready_at IS NULL AND m.state='terminal_error' AND m.outcome='error' "
            "AND m.recovery_attempt_count<? "
            "ORDER BY m.updated_at,m.ticket_id LIMIT 1",
            (stall.MAX_STALL_RECOVERY_ATTEMPTS,),
        ).fetchone()
        if row is None:
            db.commit()
            return None
        changed = db.execute(
            "UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,"
            "recovery_attempt_count=recovery_attempt_count+1,updated_at=? "
            "WHERE ticket_id=? AND run_id=? AND call_id=? AND state='terminal_error' AND outcome='error'",
            (stamp, stamp, row["ticket_id"], row["run_id"], row["call_id"]),
        )
        if changed.rowcount != 1:
            db.rollback()
            return None
        claim = dict(row)
        claim["state"] = "recovering"
        claim["recovery_started_at"] = stamp
        claim["recovery_attempt_count"] = int(row["recovery_attempt_count"] or 0) + 1
        claim["updated_at"] = stamp
        db.commit()
        return claim
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _single_open_circuit_diagnostic(root: Path):
    """Return one legacy open circuit for read-only compatibility diagnostics.

    This deliberately does not select, probe, start, stop, or otherwise control
    a provider. Multiple incidents are not guessed between.
    """
    state = recovery_policy.load_state(root)
    providers_state = state.get("providers") if isinstance(state.get("providers"), dict) else {}
    open_names = []
    for name, value in providers_state.items():
        if not isinstance(value, dict):
            continue
        incident = value.get("incident")
        if isinstance(incident, dict) and incident.get("state") == "open":
            open_names.append(str(name))
    if len(open_names) != 1:
        return None
    target = open_names[0]
    try:
        gate = recovery_policy.gate(root, target)
    except (ValueError, RuntimeError):
        return None
    if not gate.get("circuitOpen"):
        return None
    return target, gate


def supervisor_tick(root: Path, execute_safe: bool):
    """Run CNX reconciliation without global provider execution authority."""
    quiesced = stall.authority.supervisor_quiescence.supervisor_quiesced_result(root)
    if quiesced is not None:
        return quiesced

    diagnostic = _single_open_circuit_diagnostic(root)
    result = _run_base_supervisor(root, execute_safe, True)
    if diagnostic is None:
        return result

    target, gate = diagnostic
    result["providerRecovery"] = {
        "classification": "provider_recovery_circuit_open",
        "recoveryEligible": False,
        "providerRestart": False,
        "gate": gate,
    }
    result["providerIncident"] = {
        "provider": target,
        "authority": "diagnostic-only",
    }
    result["result"] = "provider-recovery-circuit-open"
    return result


# The steady-state supervisor no longer derives authority from selectedProvider,
# desiredProvider, adapter health, or local provider process state. The base
# reconciliation path still suppresses legacy timer-only Direct-call recovery.
legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
