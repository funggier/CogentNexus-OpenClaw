#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 provider-neutral v0.9.2 Host façade.

The proven v0.9.4-era provider-event and recovery payload remains executable
unchanged behind this compatibility façade. v0.9.5 moves provider/model/auth
routing and provider process lifecycle back to OpenClaw. Legacy provider fields
may remain on disk for migration and diagnostics, but they are not execution
authority.
"""
from __future__ import annotations

import json
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


legacy.runtime = provider_aware_runtime


def claim_terminal_error_direct_model_call(root: Path, now_iso: str | None = None):
    """Claim one exact terminal model-call failure without provider authority."""
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
            "AND m.recovery_attempt_count<? ORDER BY m.updated_at,m.ticket_id LIMIT 1",
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


def classify_quiesced_terminal_error_direct_model_call(root: Path, claim: dict, now_iso: str | None = None):
    """Authorize exact terminal-error Direct recovery while CNX is quiesced."""
    cutoff = now_iso or legacy.now_iso()
    delivery_fences = v091.reconcile_direct_delivery_before_recovery(root, cutoff)
    path = legacy.ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,"
            "response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?",
            (claim["ticket_id"],),
        ).fetchone()
        if row is None:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='interrupted',ended_at=?,outcome='terminal-error-ticket-missing',updated_at=? "
                "WHERE ticket_id=? AND run_id=? AND call_id=? AND state='recovering'",
                (cutoff, cutoff, claim["ticket_id"], claim["run_id"], claim["call_id"]),
            )
            db.commit()
            return {"ticketId": claim["ticket_id"], "action": "ticket-missing", "recoveryAuthority": "terminal-model-call-error", "deliveryFences": delivery_fences}

        ticket_id = str(row["ticket_id"])
        current_call = db.execute(
            "SELECT state,outcome FROM cnx_direct_model_call WHERE ticket_id=? AND run_id=? AND call_id=? LIMIT 1",
            (ticket_id, claim["run_id"], claim["call_id"]),
        ).fetchone()
        if current_call is None or str(current_call["state"]) != "recovering":
            db.rollback()
            raise RuntimeError(f"terminal model-call recovery claim changed before quiesced classification: ticket={ticket_id} run={claim['run_id']} call={claim['call_id']}")

        terminal = str(row["status"]) in {"completed", "failed", "cancelled"}
        delivery_evidence = None
        if v091._db_table_exists(db, "cnx_assistant_delivery"):
            delivery_evidence = db.execute(
                "SELECT status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result' ORDER BY delivery_id DESC LIMIT 1",
                (ticket_id,),
            ).fetchone()
        if terminal or row["response_ready_at"] is not None or row["delivery_confirmed_at"] is not None or row["workflow_id"] is not None or delivery_evidence is not None:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='ended',ended_at=?,outcome='terminal-error-delivery-or-terminal-fence',updated_at=? "
                "WHERE ticket_id=? AND run_id=? AND call_id=? AND state='recovering'",
                (cutoff, cutoff, ticket_id, claim["run_id"], claim["call_id"]),
            )
            db.commit()
            return {"ticketId": ticket_id, "action": "held-no-inference", "status": row["status"], "responseReady": row["response_ready_at"] is not None, "durableDirectResult": delivery_evidence is not None, "recoveryAuthority": "terminal-model-call-error", "deliveryFences": delivery_fences}

        if str(row["status"]) not in {"accepted", "waiting"}:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='ended',ended_at=?,outcome='terminal-error-unsupported-ticket-state',updated_at=? "
                "WHERE ticket_id=? AND run_id=? AND call_id=? AND state='recovering'",
                (cutoff, cutoff, ticket_id, claim["run_id"], claim["call_id"]),
            )
            db.commit()
            return {"ticketId": ticket_id, "action": "unsupported-state", "status": row["status"], "recoveryAuthority": "terminal-model-call-error", "deliveryFences": delivery_fences}

        reason = (f"CogentNexus-OpenClaw Host terminal model-call error: callId={claim['call_id']} provider={claim.get('provider') or 'unknown'} model={claim.get('model') or 'unknown'} errorCategory={claim.get('error_category') or 'unknown'} failureKind={claim.get('failure_kind') or 'unknown'}")[:2000]
        changed = db.execute(
            "UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? "
            "WHERE ticket_id=? AND status IN ('accepted','waiting') AND workflow_id IS NULL AND response_ready_at IS NULL",
            (reason, reason, cutoff, ticket_id),
        )
        if changed.rowcount != 1:
            db.rollback()
            raise RuntimeError(f"terminal model-call Ticket changed during quiesced Host classification: {ticket_id}")

        owner_generation = stall._queue_host_authorized_direct_recovery(
            db, ticket_id=ticket_id, owner_session_key=str(row["owner_session_key"]), reason=reason, stamp=cutoff,
        )
        db.execute(
            "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
            (ticket_id, "host_direct_model_terminal_error_authorized", json.dumps({
                "runId": str(row["run_id"] or claim["run_id"]), "callId": claim["call_id"], "provider": claim.get("provider"), "model": claim.get("model"),
                "errorCategory": claim.get("error_category"), "failureKind": claim.get("failure_kind"), "startedAt": claim.get("started_at"), "endedAt": claim.get("ended_at"),
                "reason": reason, "recoveryAuthority": "terminal-model-call-error", "recoveryMode": "resume", "ownerGeneration": owner_generation, "source": "host-v095-terminal-model-error",
            }, ensure_ascii=False), cutoff),
        )
        settled = db.execute(
            "UPDATE cnx_direct_model_call SET state='interrupted',ended_at=?,outcome='host-terminal-error-authorized',updated_at=? "
            "WHERE ticket_id=? AND run_id=? AND call_id=? AND state='recovering'",
            (cutoff, cutoff, ticket_id, claim["run_id"], claim["call_id"]),
        )
        if settled.rowcount != 1:
            db.rollback()
            raise RuntimeError(f"terminal model-call recovery claim changed while committing authorization: {ticket_id}")
        db.commit()
        return {"ticketId": ticket_id, "action": "pre-response-recovery-authorized", "recoveryState": "pending", "recoveryAuthority": "terminal-model-call-error", "ownerGeneration": owner_generation, "deliveryFences": delivery_fences}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def recover_terminal_error_direct_model_call(root: Path, claim: dict):
    """Recover one exact terminal model-call error through CNX/Gateway only."""
    prepare_result = legacy.runtime(root, "lifecycle", "prepare", timeout=180, check=True)
    stopped = False
    started = False
    classification = None
    try:
        stopped = True
        legacy.runtime(root, "lifecycle", "stop", timeout=180, check=True)
        classification = classify_quiesced_terminal_error_direct_model_call(root, claim)
        legacy.runtime(root, "lifecycle", "start", timeout=180, check=True)
        started = True
        gateway = legacy.gateway_status(root)
        if not gateway.get("healthy", False):
            return {"result": "terminal-model-call-recovery-failed", "classification": classification, "gateway": gateway, "prepared": prepare_result}
        return {"result": "terminal-model-call-recovered", "classification": classification, "gateway": gateway, "prepared": prepare_result}
    finally:
        if stopped and not started:
            legacy.runtime(root, "lifecycle", "start", timeout=180, check=True)


def _single_open_circuit_diagnostic(root: Path):
    """Return one legacy open circuit for read-only compatibility diagnostics."""
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

    state = legacy.load_state(root)
    if state.get("mode") != "managed" or state.get("desiredGateway") != "running":
        return _run_base_supervisor(root, execute_safe, True)

    if execute_safe:
        claim = claim_terminal_error_direct_model_call(root)
        if claim is not None:
            return recover_terminal_error_direct_model_call(root, claim)

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
    result["providerIncident"] = {"provider": target, "authority": "diagnostic-only"}
    result["result"] = "provider-recovery-circuit-open"
    return result


legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
