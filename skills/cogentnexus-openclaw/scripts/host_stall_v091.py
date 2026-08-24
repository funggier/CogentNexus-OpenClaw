#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.1 Host-owned Direct model-call stall recovery.

The plugin records only sanitized model_call_started/model_call_ended telemetry.
An expired provider-call lease is not itself permission for plugin recovery.
The external Host claims the lease, quiesces Gateway + provider, classifies the
Ticket while inference is impossible, durably authorizes exactly one Direct
recovery, and only then restarts the managed runtime.

Power-loss semantics:
- a claimed `recovering` lease is durable and can be reclaimed after a bounded
  interval by the next Host supervisor tick;
- maintenance uses recoveryPolicy=healthy-runtime, so a crash after quiescing
  cannot strand the machine in manual maintenance;
- if the original model call wins the race and reaches response_ready before
  quiescence, the v0.9.1 delivery fence wins and no regeneration is authorized;
- after quiescent classification, the Host-authored `cnx_direct_recovery`
  pending row is the recovery authority. The plugin only consumes that durable
  authorization after runtime startup.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import host_authority_v091 as authority
import host_v091 as v091

legacy = authority.legacy
BASE_SUPERVISOR_TICK = legacy.supervisor_tick
RECLAIM_AFTER_SECONDS = 90
MAX_STALL_RECOVERY_ATTEMPTS = 5
STALL_REASON = "CogentNexus-OpenClaw Host direct model-call deadline exceeded"


def _model_call_table(db: sqlite3.Connection) -> bool:
    return db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_direct_model_call'"
    ).fetchone() is not None


def _stamp(value: str | None = None) -> str:
    return value or legacy.now_iso()


def claim_expired_direct_model_call(root: Path, now_iso: str | None = None) -> dict[str, Any] | None:
    """Claim one expired active provider call without mutating its Ticket."""
    path = legacy.ticket_db(root)
    if not path.exists():
        return None
    now_value = _stamp(now_iso)
    now_dt = datetime.fromisoformat(now_value.replace("Z", "+00:00"))
    reclaim_before = (now_dt - timedelta(seconds=RECLAIM_AFTER_SECONDS)).astimezone(timezone.utc).isoformat()
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not _model_call_table(db) or not v091._db_table_exists(db, "tickets"):
            return None
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT m.ticket_id,m.run_id,m.call_id,m.state,m.provider,m.model,m.started_at,m.deadline_at,"
            "m.recovery_started_at,m.recovery_attempt_count,t.owner_session_key,t.status,t.response_ready_at,t.workflow_id "
            "FROM cnx_direct_model_call m JOIN tickets t ON t.ticket_id=m.ticket_id "
            "WHERE t.status='accepted' AND t.workflow_eligible=0 AND t.workflow_id IS NULL AND t.response_ready_at IS NULL "
            "AND m.deadline_at<=? AND m.recovery_attempt_count<? AND ("
            "m.state='active' OR (m.state='recovering' AND m.recovery_started_at IS NOT NULL AND m.recovery_started_at<=?)) "
            "ORDER BY m.deadline_at,m.ticket_id LIMIT 1",
            (now_value, MAX_STALL_RECOVERY_ATTEMPTS, reclaim_before),
        ).fetchone()
        if row is None:
            db.commit()
            return None
        changed = db.execute(
            "UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,"
            "recovery_attempt_count=recovery_attempt_count+1,updated_at=? "
            "WHERE ticket_id=? AND call_id=? AND state=?",
            (now_value, now_value, row["ticket_id"], row["call_id"], row["state"]),
        )
        if changed.rowcount != 1:
            db.rollback()
            return None
        claimed = dict(row)
        claimed["state"] = "recovering"
        claimed["recovery_started_at"] = now_value
        claimed["recovery_attempt_count"] = int(row["recovery_attempt_count"] or 0) + 1
        db.commit()
        return claimed
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _release_model_call_claim(root: Path, claim: dict[str, Any], error: str) -> None:
    """Return a failed Host attempt to active with a bounded retry delay."""
    path = legacy.ticket_db(root)
    if not path.exists():
        return
    stamp = legacy.now_iso()
    retry_at = (datetime.now(timezone.utc) + timedelta(seconds=RECLAIM_AFTER_SECONDS)).isoformat()
    db = sqlite3.connect(path, timeout=5)
    try:
        if not _model_call_table(db):
            return
        db.execute(
            "UPDATE cnx_direct_model_call SET state='active',deadline_at=?,recovery_started_at=NULL,outcome=?,updated_at=? "
            "WHERE ticket_id=? AND call_id=? AND state='recovering'",
            (retry_at, f"host-recovery-error:{error[:500]}", stamp, claim["ticket_id"], claim["call_id"]),
        )
        db.commit()
    finally:
        db.close()


def _queue_host_authorized_direct_recovery(
    db: sqlite3.Connection,
    *,
    ticket_id: str,
    owner_session_key: str,
    reason: str,
    stamp: str,
) -> int:
    """Persist the Direct recovery authority chosen by the quiesced Host.

    The Direct recovery worker deliberately consumes only accepted,
    workflow_eligible=0 Tickets. Keeping that shape prevents the generic Ticket
    dispatcher from compiling the interrupted conversational prompt into a
    durable workflow and makes the Host-authored recovery row the single source
    of inference-recovery authority.
    """
    if not v091._db_table_exists(db, "cnx_sessions") or not v091._db_table_exists(db, "cnx_direct_recovery"):
        raise RuntimeError("Direct recovery schema missing during quiesced Host classification")
    owner = db.execute(
        "SELECT state,generation FROM cnx_sessions WHERE session_key=?",
        (owner_session_key,),
    ).fetchone()
    if owner is None:
        raise RuntimeError(f"Direct recovery owner session is missing: {owner_session_key}")
    if str(owner["state"]) != "active":
        raise RuntimeError(
            f"Direct recovery owner session is not active: {owner_session_key} state={owner['state']}"
        )
    owner_generation = int(owner["generation"] or 0)
    db.execute(
        """INSERT INTO cnx_direct_recovery(
             ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
             owner_generation,created_at,updated_at
           ) VALUES (?,'resume','pending',0,NULL,?,?,?,?,?)
           ON CONFLICT(ticket_id) DO UPDATE SET
             mode='resume',state='pending',active_run_id=NULL,next_attempt_at=excluded.next_attempt_at,
             last_error=excluded.last_error,owner_generation=excluded.owner_generation,
             updated_at=excluded.updated_at""",
        (ticket_id, stamp, reason[:2000], owner_generation, stamp, stamp),
    )
    return owner_generation


def classify_quiesced_direct_model_call(root: Path, claim: dict[str, Any]) -> dict[str, Any]:
    """Classify one claimed Direct call only after Gateway/provider are stopped."""
    cutoff = legacy.now_iso()
    delivery_fences = v091.reconcile_direct_delivery_before_recovery(root, cutoff)
    path = legacy.ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,delivery_confirmed_at "
            "FROM tickets WHERE ticket_id=?",
            (claim["ticket_id"],),
        ).fetchone()
        if row is None:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='interrupted',ended_at=?,outcome='ticket-missing',updated_at=? "
                "WHERE ticket_id=? AND call_id=? AND state='recovering'",
                (cutoff, cutoff, claim["ticket_id"], claim["call_id"]),
            )
            db.commit()
            return {"ticketId": claim["ticket_id"], "action": "ticket-missing", "deliveryFences": delivery_fences}

        ticket_id = str(row["ticket_id"])
        terminal = str(row["status"]) in {"completed", "failed", "cancelled"}
        delivery_evidence = None
        if v091._db_table_exists(db, "cnx_assistant_delivery"):
            delivery_evidence = db.execute(
                "SELECT status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result' ORDER BY delivery_id DESC LIMIT 1",
                (ticket_id,),
            ).fetchone()

        # Any terminal, response-ready, confirmed, workflow-owned, or durable
        # result state belongs to delivery/terminal handling and can never be
        # converted into inference recovery by the stall path.
        if terminal or row["response_ready_at"] is not None or row["delivery_confirmed_at"] is not None or row["workflow_id"] or delivery_evidence is not None:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='ended',ended_at=?,outcome=?,updated_at=? "
                "WHERE ticket_id=? AND call_id=? AND state='recovering'",
                (cutoff, "delivery-or-terminal-fence", cutoff, ticket_id, claim["call_id"]),
            )
            db.commit()
            return {
                "ticketId": ticket_id,
                "action": "held-no-inference",
                "status": row["status"],
                "responseReady": row["response_ready_at"] is not None,
                "durableDirectResult": delivery_evidence is not None,
                "deliveryFences": delivery_fences,
            }

        if str(row["status"]) not in {"accepted", "waiting"}:
            db.execute(
                "UPDATE cnx_direct_model_call SET state='ended',ended_at=?,outcome='unsupported-ticket-state',updated_at=? "
                "WHERE ticket_id=? AND call_id=? AND state='recovering'",
                (cutoff, cutoff, ticket_id, claim["call_id"]),
            )
            db.commit()
            return {"ticketId": ticket_id, "action": "unsupported-state", "status": row["status"], "deliveryFences": delivery_fences}

        reason = (
            f"{STALL_REASON}: callId={claim['call_id']} provider={claim.get('provider') or 'unknown'} "
            f"model={claim.get('model') or 'unknown'} deadline={claim.get('deadline_at')}"
        )[:2000]

        # Keep the Ticket in the Direct lane. `waiting + workflow_eligible=1`
        # belongs to the generic durable-workflow dispatcher and would compile
        # a different execution path. The Host instead writes the pending
        # cnx_direct_recovery row while inference is quiesced.
        changed = db.execute(
            "UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,"
            "failure_class='interrupted',failure_message=?,delivery_last_error=?,updated_at=? "
            "WHERE ticket_id=? AND status IN ('accepted','waiting') AND workflow_id IS NULL AND response_ready_at IS NULL",
            (reason, reason, cutoff, ticket_id),
        )
        if changed.rowcount != 1:
            db.rollback()
            raise RuntimeError(f"Direct model-call Ticket changed during quiesced Host classification: {ticket_id}")

        owner_generation = _queue_host_authorized_direct_recovery(
            db,
            ticket_id=ticket_id,
            owner_session_key=str(row["owner_session_key"]),
            reason=reason,
            stamp=cutoff,
        )
        db.execute(
            "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
            (
                ticket_id,
                "host_direct_model_timeout_authorized",
                json.dumps({
                    "runId": row["run_id"],
                    "callId": claim["call_id"],
                    "provider": claim.get("provider"),
                    "model": claim.get("model"),
                    "startedAt": claim.get("started_at"),
                    "deadlineAt": claim.get("deadline_at"),
                    "reason": reason,
                    "recoveryMode": "resume",
                    "ownerGeneration": owner_generation,
                    "source": "host-v091-direct-model-stall",
                }, ensure_ascii=False),
                cutoff,
            ),
        )
        db.execute(
            "UPDATE cnx_direct_model_call SET state='interrupted',ended_at=?,outcome='host-timeout-authorized',updated_at=? "
            "WHERE ticket_id=? AND call_id=? AND state='recovering'",
            (cutoff, cutoff, ticket_id, claim["call_id"]),
        )
        db.commit()
        return {
            "ticketId": ticket_id,
            "action": "pre-response-recovery-authorized",
            "recoveryState": "pending",
            "ownerGeneration": owner_generation,
            "deliveryFences": delivery_fences,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def recover_expired_direct_model_call(root: Path, claim: dict[str, Any]) -> dict[str, Any]:
    """Quiesce -> classify -> restart. No inference-capable runtime spans classification."""
    reason = (
        f"{STALL_REASON}: ticket={claim['ticket_id']} call={claim['call_id']} "
        f"provider={claim.get('provider') or 'unknown'} model={claim.get('model') or 'unknown'}"
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
    stopped = legacy.runtime(
        root,
        "lifecycle",
        "stop",
        "--provider",
        "--reason",
        reason,
        "--owner",
        "cogentnexus-openclaw-host",
        timeout=240,
        check=True,
    )
    classification = classify_quiesced_direct_model_call(root, claim)
    started = legacy.runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)
    gateway = legacy.gateway_status()
    if not gateway.get("healthy"):
        raise RuntimeError(f"Gateway failed health verification after Direct model-call recovery: {gateway}")
    return {
        "result": "direct-model-call-recovered",
        "claim": claim,
        "prepared": legacy.parse_json_output(prepared.stdout),
        "stopped": legacy.parse_json_output(stopped.stdout),
        "classification": classification,
        "started": legacy.parse_json_output(started.stdout),
        "gateway": {"healthy": True},
    }


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    state = legacy.load_state(root)
    if state.get("mode") != "managed" or state.get("desiredGateway") != "running":
        return BASE_SUPERVISOR_TICK(root, execute_safe)

    # Endpoint loss remains owned by the proven hard-hang path. This overlay is
    # specifically for a provider call that exceeded its durable deadline while
    # Gateway and provider endpoints still answer health probes.
    if not v091.gateway_fast_probe() or (state.get("desiredProvider") == "running" and not v091.ollama_fast_probe()):
        return BASE_SUPERVISOR_TICK(root, execute_safe)
    if not execute_safe:
        return BASE_SUPERVISOR_TICK(root, execute_safe)

    claim = claim_expired_direct_model_call(root)
    if claim is None:
        return BASE_SUPERVISOR_TICK(root, execute_safe)
    try:
        return recover_expired_direct_model_call(root, claim)
    except Exception as error:
        try:
            _release_model_call_claim(root, claim, str(error))
        except Exception:
            pass
        raise


# Importing host_authority_v091 preserves the single MANAGED linearization point
# and all v0.9.1 delivery fences. Replace only the steady-state supervisor with
# the Direct provider-call lease recovery overlay.
legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
