#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.1 live-hardening compatibility layer.

Keeps the proven Host implementation intact while adding the invariants found
by live Windows acceptance and end-to-end wiring review:

1. enable is transactional: failure returns to native passthrough state;
2. disable commits passthrough only after CNXCLAW surfaces are removed and native
   Gateway health is verified;
3. fresh initialization starts in passthrough until enable commits managed;
4. startup adapters route through the v0.9.1 control wrapper; and
5. an idle healthy runtime is quiescent: the external supervisor uses small
   socket/read-only durable probes and enters heavy reconciliation only when
   health is lost or actionable committed work exists.
"""
from __future__ import annotations

import json
import os
import socket
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import host as legacy
import openclaw_runtime_boundary_v092 as runtime_boundary

HERE = Path(__file__).resolve()
LEGACY_SUPERVISOR_TICK = legacy.supervisor_tick
LEGACY_PROMOTE_INTERRUPTED_DIRECT = legacy.promote_interrupted_direct
IDLE_GATEWAY_PORT = 18789
IDLE_OLLAMA_PORT = 11434
IDLE_PROBE_TIMEOUT_SECONDS = 0.75
HARD_HANG_CONFIRM_DELAY_SECONDS = 1.0
UNVERIFIABLE_DIRECT_MESSAGE = (
    "direct response delivery became unverifiable before the final payload was durably captured; "
    "refusing regeneration to avoid duplicate output"
)


def safe_default_state() -> dict[str, Any]:
    """Fresh installs are native until transactional enable commits MANAGED."""
    return {
        "schemaVersion": 1,
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
        "generation": 1,
        "updatedAt": legacy.now_iso(),
    }


def startup_path_v091() -> Path:
    return HERE.with_name("startup_v091.py")


# All calls routed through this compatibility layer inherit safe initialization
# and scheduler wiring without rewriting the proven legacy implementation.
legacy.default_state = safe_default_state
legacy.startup_path = startup_path_v091


def _snapshot_file(path: Path) -> tuple[bool, bytes]:
    if not path.exists():
        return False, b""
    return True, path.read_bytes()


def _restore_file(path: Path, snapshot: tuple[bool, bytes]) -> None:
    existed, data = snapshot
    if existed:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".v091-rollback")
        temporary.write_bytes(data)
        os.replace(temporary, path)
    else:
        path.unlink(missing_ok=True)


def _openclaw_config() -> dict[str, Any]:
    configured = os.environ.get("OPENCLAW_CONFIG_PATH")
    path = Path(configured).expanduser() if configured else Path.home() / ".openclaw" / "openclaw.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _gateway_port() -> int:
    config = _openclaw_config()
    gateway = config.get("gateway") if isinstance(config.get("gateway"), dict) else {}
    try:
        port = int(gateway.get("port", IDLE_GATEWAY_PORT))
    except (TypeError, ValueError):
        return IDLE_GATEWAY_PORT
    return port if 1 <= port <= 65535 else IDLE_GATEWAY_PORT


def _http_probe(port: int, path: str) -> bool:
    """Small responsiveness probe that avoids Node/OpenClaw CLI startup."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=IDLE_PROBE_TIMEOUT_SECONDS) as connection:
            connection.settimeout(IDLE_PROBE_TIMEOUT_SECONDS)
            request = f"GET {path} HTTP/1.0\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"
            connection.sendall(request.encode("ascii"))
            response = connection.recv(32)
            return response.startswith(b"HTTP/")
    except OSError:
        return False


def gateway_fast_probe() -> bool:
    return _http_probe(_gateway_port(), "/")


def ollama_fast_probe() -> bool:
    return _http_probe(IDLE_OLLAMA_PORT, "/api/tags")


def _db_table_exists(db: sqlite3.Connection, name: str) -> bool:
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None


DIRECT_RECOVERY_SESSION_LIVENESS_SECONDS = 15 * 60


def _parse_iso_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def durable_work_hint(root: Path, now: str | None = None) -> bool:
    """Return true only for durable work actionable under Host contracts.

    Direct recovery deliberately mirrors ``dueDirectRecovery``: the owner must
    be active, exact-generation, recently updated, due, and outside the model
    call fence. Stored nonterminal Direct rows alone are not a wake signal.
    """
    path = legacy.ticket_db(root)
    if not path.exists():
        return False
    current = _parse_iso_timestamp(now) if now else datetime.now(timezone.utc)
    if current is None:
        current = datetime.now(timezone.utc)
    cutoff = current - timedelta(seconds=DIRECT_RECOVERY_SESSION_LIVENESS_SECONDS)
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=0.25)
        db.row_factory = sqlite3.Row
    except sqlite3.Error:
        return True
    try:
        if not _db_table_exists(db, "tickets"):
            return False

        ticket_columns = {row["name"] for row in db.execute("PRAGMA table_info(tickets)")}
        if {"workflow_eligible", "workflow_id"}.issubset(ticket_columns):
            # Workflow Tickets remain actionable only when explicitly admitted;
            # an accepted Direct Ticket is not a workflow wake signal.
            if db.execute(
                """SELECT 1 FROM tickets
                   WHERE status NOT IN ('completed','failed','cancelled')
                     AND (workflow_eligible <> 0 OR workflow_id IS NOT NULL)
                   LIMIT 1"""
            ).fetchone():
                return True
        elif db.execute(
            "SELECT 1 FROM tickets WHERE status NOT IN ('completed','failed','cancelled') LIMIT 1"
        ).fetchone():
            # Legacy schemas cannot identify Direct ownership; preserve their
            # historical nonterminal workflow fallback.
            return True

        if _db_table_exists(db, "ticket_outbox") and db.execute(
            "SELECT 1 FROM ticket_outbox WHERE delivery_status='pending' LIMIT 1"
        ).fetchone():
            return True
        if _db_table_exists(db, "cnx_assistant_delivery") and db.execute(
            "SELECT 1 FROM cnx_assistant_delivery WHERE status='pending' LIMIT 1"
        ).fetchone():
            return True
        if _db_table_exists(db, "cnx_context_maintenance") and db.execute(
            "SELECT 1 FROM cnx_context_maintenance WHERE state IN ('pending','running','degraded') LIMIT 1"
        ).fetchone():
            return True

        required = {"cnx_direct_recovery", "cnx_sessions"}
        table_names = {row["name"] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "cnx_direct_recovery" in table_names and not required.issubset(table_names):
            # Legacy delivery-only rows predate owner/session fences but remain
            # Host-owned transport work; preserve this narrow fallback.
            recovery_columns = {row["name"] for row in db.execute("PRAGMA table_info(cnx_direct_recovery)")}
            if recovery_columns == {"state"} and db.execute(
                "SELECT 1 FROM cnx_direct_recovery WHERE state='awaiting_delivery' LIMIT 1"
            ).fetchone():
                return True
        if not required.issubset(table_names):
            return False
        model_fenced = _db_table_exists(db, "cnx_direct_model_call")
        rows = db.execute(
            """SELECT r.ticket_id,r.state,r.next_attempt_at,r.owner_generation,
                      t.status,t.workflow_eligible,t.workflow_id,s.state AS session_state,
                      s.generation,s.updated_at AS session_updated_at
               FROM cnx_direct_recovery r
               JOIN tickets t ON t.ticket_id=r.ticket_id
               JOIN cnx_sessions s ON s.session_key=t.owner_session_key
               WHERE r.state='pending' AND t.status='accepted'
                 AND t.workflow_eligible=0 AND t.workflow_id IS NULL
                 AND s.state='active' AND s.generation=r.owner_generation"""
        ).fetchall()
        for row in rows:
            session_updated = _parse_iso_timestamp(row["session_updated_at"])
            if session_updated is None or session_updated < cutoff:
                continue
            due_at = _parse_iso_timestamp(row["next_attempt_at"])
            if due_at is not None and due_at > current:
                continue
            if model_fenced and db.execute(
                "SELECT 1 FROM cnx_direct_model_call WHERE ticket_id=? AND state IN ('active','recovering') LIMIT 1",
                (row["ticket_id"],),
            ).fetchone():
                continue
            return True
        return False
    except sqlite3.Error:
        # Lock/schema uncertainty is not proof of quiescence. Fail toward the
        # bounded recovery path rather than sleeping over committed work.
        return True
    finally:
        db.close()


def configure_managed_plugin() -> None:
    """Stage all managed settings while the plugin is disabled.

    Compatibility interval fields are kept conservative for older internal
    layers, while v0.9.1 replaces the production workers with event/deadline
    driven services. They are no longer the primary execution mechanism.
    """
    settings = [
        ("ticketFirst", "true"),
        ("preInferenceAdmission", "true"),
        ("autoWorkflowCompletion", "true"),
        ("enforcedMode", "true"),
        ("autoResume", "true"),
        ("workspaceDir", str(legacy.WORKSPACE)),
        ("ticketDispatchLimit", "1"),
        ("ticketMaximumRunning", "1"),
        ("ticketMaximumAttempts", "5"),
        ("ticketRecoveryPollMs", "60000"),
        ("ticketDispatchPollMs", "60000"),
        ("ticketOutboxPollMs", "60000"),
        ("completionPollMs", "60000"),
        ("contextMaintenancePollMs", "30000"),
    ]
    for key, value in settings:
        legacy.run(
            [legacy.openclaw_executable(), "config", "set", f"plugins.entries.{legacy.PLUGIN_ID}.config.{key}", value],
            timeout=60,
            check=True,
        )
    legacy.run(
        [legacy.openclaw_executable(), "config", "set", f"plugins.entries.{legacy.PLUGIN_ID}.hooks.allowConversationAccess", "true"],
        timeout=60,
        check=True,
    )


def validate_managed_config() -> None:
    legacy.run([legacy.openclaw_executable(), "config", "validate"], timeout=60, check=True)


def _restore_native_gateway() -> dict[str, Any]:
    restart = legacy.run([legacy.openclaw_executable(), "gateway", "restart"], timeout=180)
    if restart.returncode != 0:
        restart = legacy.run([legacy.openclaw_executable(), "gateway", "start"], timeout=180)
    if restart.returncode != 0:
        raise RuntimeError((restart.stderr or restart.stdout or "native Gateway restore command failed").strip())
    status = legacy.gateway_status()
    if not status.get("healthy"):
        raise RuntimeError(f"native Gateway failed health verification after restore: {status}")
    return {
        "exitCode": restart.returncode,
        "stdout": (restart.stdout or "").strip(),
        "stderr": (restart.stderr or "").strip(),
        "healthy": True,
    }


def _restart_unresponsive_gateway(root: Path) -> dict[str, Any]:
    """Restart a confirmed hard-hung Gateway under recoverable maintenance authority."""
    result = legacy.runtime(
        root,
        "lifecycle",
        "restart",
        "--reason",
        "CogentNexus-OpenClaw external supervisor confirmed an unresponsive Gateway",
        timeout=240,
        check=False,
    )
    return {
        "attempted": True,
        "exitCode": result.returncode,
        "output": legacy.parse_json_output(result.stdout) if (result.stdout or "").strip() else None,
        "stderr": (result.stderr or "").strip(),
    }


def _force_passthrough_without_generation_bump(root: Path, prior: dict[str, Any]) -> dict[str, Any]:
    """Fail-safe durable rollback while preserving the pre-attempt generation."""
    if prior.get("mode") == "passthrough":
        return legacy.load_state(root)
    restored = dict(prior)
    restored.update({
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
    })
    return legacy.save_state(root, restored)


def _enqueue_failed_ticket_outbox(
    db: sqlite3.Connection,
    ticket_id: str,
    owner_session_key: str,
    message: str,
    stamp: str,
) -> None:
    if not _db_table_exists(db, "ticket_outbox"):
        return
    payload = json.dumps(
        {"classification": "permanent", "message": message, "source": "host-v091-pre-recovery-fence"},
        ensure_ascii=False,
    )
    db.execute(
        "INSERT OR IGNORE INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) "
        "VALUES (?,?, 'failed', ?, 'pending', 0, ?)",
        (ticket_id, owner_session_key, payload, stamp),
    )


def reconcile_direct_delivery_before_recovery(root: Path, cutoff_iso: str) -> dict[str, Any]:
    """Fence response-ready Direct Tickets before any Host recovery can wake inference.

    A response that may already have reached the user must never be regenerated
    merely because a lifecycle transition occurred. Exact durable Direct results
    remain transport-owned; response-ready Tickets without such a payload fail
    closed as unverifiable. Previously mis-promoted waiting rows are repaired too
    when they do not yet have a workflow owner.
    """
    path = legacy.ticket_db(root)
    result: dict[str, Any] = {
        "unverifiableFailed": [],
        "durableDeliveryHeld": [],
        "confirmedHeld": [],
        "workflowOwnedSkipped": [],
    }
    if not path.exists():
        return result
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        if not _db_table_exists(db, "tickets") or not _db_table_exists(db, "ticket_events"):
            return result
        columns = {row[1] for row in db.execute("PRAGMA table_info(tickets)").fetchall()}
        required = {"response_ready_at", "delivery_confirmed_at", "workflow_eligible", "workflow_id", "run_id", "owner_session_key"}
        if not required.issubset(columns):
            raise RuntimeError("Ticket schema lacks v0.9.1 direct-delivery columns; refusing recovery promotion")

        db.execute("BEGIN IMMEDIATE")
        rows = db.execute(
            "SELECT ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,delivery_confirmed_at "
            "FROM tickets WHERE status IN ('accepted','waiting') AND created_at<? AND response_ready_at IS NOT NULL "
            "AND delivery_confirmed_at IS NULL ORDER BY created_at,ticket_id",
            (cutoff_iso,),
        ).fetchall()
        stamp = legacy.now_iso()
        has_delivery = _db_table_exists(db, "cnx_assistant_delivery")
        has_recovery = _db_table_exists(db, "cnx_direct_recovery")

        for row in rows:
            ticket_id = str(row["ticket_id"])
            if row["workflow_id"]:
                result["workflowOwnedSkipped"].append(ticket_id)
                continue
            durable = None
            if has_delivery:
                durable = db.execute(
                    "SELECT status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result' ORDER BY delivery_id DESC LIMIT 1",
                    (ticket_id,),
                ).fetchone()
            if durable is not None:
                # Exact text exists. It belongs to the transport retry path, never
                # to inference recovery. Undo an older Host promotion if necessary.
                if row["status"] == "waiting" or int(row["workflow_eligible"] or 0) != 0:
                    db.execute(
                        "UPDATE tickets SET status='accepted',workflow_eligible=0,failure_class=NULL,failure_message=NULL,updated_at=? "
                        "WHERE ticket_id=? AND workflow_id IS NULL AND delivery_confirmed_at IS NULL",
                        (stamp, ticket_id),
                    )
                    db.execute(
                        "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                        (
                            ticket_id,
                            "host_restored_durable_delivery",
                            json.dumps({"runId": row["run_id"], "source": "host-v091-pre-recovery-fence"}),
                            stamp,
                        ),
                    )
                result["durableDeliveryHeld"].append(ticket_id)
                continue

            message = UNVERIFIABLE_DIRECT_MESSAGE
            changed = db.execute(
                "UPDATE tickets SET status='failed',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,"
                "failure_class='permanent',failure_message=?,delivery_last_error=?,updated_at=? "
                "WHERE ticket_id=? AND status IN ('accepted','waiting') AND response_ready_at IS NOT NULL "
                "AND delivery_confirmed_at IS NULL AND workflow_id IS NULL",
                (message, message, stamp, ticket_id),
            )
            if changed.rowcount != 1:
                continue
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (
                    ticket_id,
                    "failed",
                    json.dumps(
                        {
                            "runId": row["run_id"],
                            "classification": "permanent",
                            "message": message,
                            "source": "host-v091-pre-recovery-fence",
                        },
                        ensure_ascii=False,
                    ),
                    stamp,
                ),
            )
            _enqueue_failed_ticket_outbox(db, ticket_id, str(row["owner_session_key"]), message, stamp)
            if has_recovery:
                db.execute(
                    "UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=?,updated_at=? "
                    "WHERE ticket_id=? AND state<>'cancelled'",
                    (message, stamp, ticket_id),
                )
            result["unverifiableFailed"].append(ticket_id)

        db.commit()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def promote_interrupted_direct_v091(root: Path, cutoff_iso: str, reason: str) -> list[str]:
    """Promote only Direct work that never reached response_ready."""
    reconcile_direct_delivery_before_recovery(root, cutoff_iso)
    path = legacy.ticket_db(root)
    if not path.exists():
        return []
    db = sqlite3.connect(path, timeout=5)
    try:
        db.execute("PRAGMA foreign_keys=ON")
        if not _db_table_exists(db, "tickets") or not _db_table_exists(db, "ticket_events"):
            return []
        db.execute("BEGIN IMMEDIATE")
        rows = db.execute(
            "SELECT ticket_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL "
            "AND response_ready_at IS NULL AND created_at<? ORDER BY created_at,ticket_id",
            (cutoff_iso,),
        ).fetchall()
        updated: list[str] = []
        stamp = legacy.now_iso()
        for (ticket_id,) in rows:
            changed = db.execute(
                "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,updated_at=? "
                "WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0 AND workflow_id IS NULL AND response_ready_at IS NULL",
                (reason[:2000], stamp, ticket_id),
            )
            if changed.rowcount != 1:
                continue
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (
                    ticket_id,
                    "host_recovered_direct",
                    json.dumps({"reason": reason, "cutoff": cutoff_iso, "source": "host-v091"}),
                    stamp,
                ),
            )
            updated.append(str(ticket_id))
        db.commit()
        return updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def enable(root: Path) -> dict[str, Any]:
    """Enter MANAGED only after every activation stage is verified."""
    legacy.initialize(root)
    prior = legacy.load_state(root)
    workspace = root.parent
    agents_path = workspace / "AGENTS.md"
    agents_snapshot = _snapshot_file(agents_path)
    started = legacy.now_iso()

    # Terminal intent and response-ready delivery ambiguity must be authoritative
    # before any inference-capable CNXCLAW surface can wake.
    terminal_fences = legacy.reconcile_terminal_fences(root)
    direct_delivery_fences = reconcile_direct_delivery_before_recovery(root, started)

    policy_changed = False
    configuration_attempted = False
    plugin_enable_attempted = False
    startup_attempted = False
    runtime_start_attempted = False
    rollback: list[dict[str, Any]] = []

    try:
        legacy.plugin_enabled(False)
        configuration_attempted = True
        configure_managed_plugin()
        validate_managed_config()

        policy_changed = legacy.apply_policy(workspace, root)
        plugin_enable_attempted = True
        legacy.plugin_enabled(True)

        # Mark the attempt before invoking startup. The adapter may have been
        # created successfully even if its final verification then raises.
        startup_attempted = True
        startup_result = legacy.startup(root, "enable", check=True)

        runtime_start_attempted = True
        lifecycle = legacy.runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)

        # lifecycle start may intentionally skip an already-healthy Gateway.
        # Force a process boundary after install-over replacement so the
        # enabled process cannot remain a predecessor runtime.
        managed_boundary = runtime_boundary.activate_current_config()
        if not managed_boundary.get("ok"):
            raise RuntimeError(f"Gateway failed managed process-boundary verification: {managed_boundary}")

        gateway = legacy.gateway_status()
        if not gateway.get("healthy"):
            raise RuntimeError(f"Gateway failed managed health verification: {gateway}")

        session_bootstrap = legacy.reconcile_default_session()
        if session_bootstrap.get("ok") is False and not session_bootstrap.get("skipped"):
            raise RuntimeError(f"default session bootstrap failed: {session_bootstrap}")

        state = legacy.transition(root, mode="managed", desiredGateway="running", desiredProvider="running")
    except Exception as error:
        if startup_attempted:
            try:
                result = legacy.startup(root, "disable", check=False)
                rollback.append({"stage": "startup-disable", "exitCode": result.returncode})
            except Exception as rollback_error:
                rollback.append({"stage": "startup-disable", "error": str(rollback_error)})
        try:
            legacy.plugin_enabled(False)
            rollback.append({"stage": "plugin-disable", "ok": True})
        except Exception as rollback_error:
            rollback.append({"stage": "plugin-disable", "error": str(rollback_error)})
        try:
            legacy.runtime(root, "lifecycle", "cancel", timeout=60, check=False)
            rollback.append({"stage": "lifecycle-cancel", "ok": True})
        except Exception as rollback_error:
            rollback.append({"stage": "lifecycle-cancel", "error": str(rollback_error)})
        try:
            _restore_file(agents_path, agents_snapshot)
            rollback.append({"stage": "policy-restore", "ok": True})
        except Exception as rollback_error:
            rollback.append({"stage": "policy-restore", "error": str(rollback_error)})

        if configuration_attempted or plugin_enable_attempted or startup_attempted or runtime_start_attempted:
            try:
                rollback.append({"stage": "native-gateway-restore", **_restore_native_gateway()})
            except Exception as rollback_error:
                rollback.append({"stage": "native-gateway-restore", "error": str(rollback_error)})

        try:
            rolled_state = _force_passthrough_without_generation_bump(root, prior)
            rollback.append({
                "stage": "host-state-rollback",
                "mode": rolled_state.get("mode"),
                "generation": rolled_state.get("generation"),
            })
        except Exception as rollback_error:
            rollback.append({"stage": "host-state-rollback", "error": str(rollback_error)})

        current = legacy.load_state(root)
        raise RuntimeError(
            "CogentNexus-OpenClaw transactional enable failed; native passthrough rollback executed. "
            f"cause={error}; priorMode={prior.get('mode')}; currentMode={current.get('mode')}; rollback={rollback}"
        ) from error

    recovery_error = None
    recovered: list[str] = []
    try:
        recovered = promote_interrupted_direct_v091(
            root,
            started,
            "CogentNexus-OpenClaw Host enabled after an interrupted OpenClaw runtime",
        )
        legacy.runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)
    except Exception as error:
        recovery_error = str(error)

    return {
        "mode": state["mode"],
        "policyChanged": policy_changed,
        "policy": legacy.policy_info(root),
        "startup": legacy.parse_json_output(startup_result.stdout),
        "lifecycle": legacy.parse_json_output(lifecycle.stdout),
        "gatewayBoundary": managed_boundary,
        "sessionBootstrap": session_bootstrap,
        "terminalFences": terminal_fences,
        "directDeliveryFences": direct_delivery_fences,
        "recoveredTickets": recovered,
        "postCommitRecoveryError": recovery_error,
        "transactional": True,
    }


def disable(root: Path) -> dict[str, Any]:
    """Remove CNXCLAW surfaces first; commit PASSTHROUGH only after native health."""
    legacy.initialize(root)
    prior = legacy.load_state(root)
    workspace = root.parent
    agents_path = workspace / "AGENTS.md"
    agents_snapshot = _snapshot_file(agents_path)
    prior_managed_surface = prior.get("mode") != "passthrough"
    startup_attempted = False
    policy_attempted = False
    plugin_disable_attempted = False
    rollback: list[dict[str, Any]] = []

    try:
        startup_attempted = True
        startup_result = legacy.startup(root, "disable", check=True)

        policy_attempted = True
        policy_changed = legacy.remove_policy(workspace)

        plugin_disable_attempted = True
        legacy.plugin_enabled(False)
        legacy.runtime(root, "lifecycle", "cancel", timeout=60, check=False)
        gateway = _restore_native_gateway()

        if prior.get("mode") == "passthrough":
            state = legacy.load_state(root)
        else:
            state = legacy.transition(root, mode="passthrough", desiredGateway="running", desiredProvider="unchanged")
    except Exception as error:
        if policy_attempted:
            try:
                _restore_file(agents_path, agents_snapshot)
                rollback.append({"stage": "policy-restore", "ok": True})
            except Exception as rollback_error:
                rollback.append({"stage": "policy-restore", "error": str(rollback_error)})
        if prior_managed_surface and plugin_disable_attempted:
            try:
                legacy.plugin_enabled(True)
                rollback.append({"stage": "plugin-enable", "ok": True})
            except Exception as rollback_error:
                rollback.append({"stage": "plugin-enable", "error": str(rollback_error)})
        if prior_managed_surface and startup_attempted:
            try:
                result = legacy.startup(root, "enable", check=False)
                rollback.append({"stage": "startup-enable", "exitCode": result.returncode})
            except Exception as rollback_error:
                rollback.append({"stage": "startup-enable", "error": str(rollback_error)})
        if prior_managed_surface and prior.get("desiredGateway") == "running":
            try:
                args = ["lifecycle", "start"]
                if prior.get("desiredProvider") == "running":
                    args.append("--provider")
                result = legacy.runtime(root, *args, timeout=240, check=False)
                rollback.append({"stage": "managed-runtime-restore", "exitCode": result.returncode})
            except Exception as rollback_error:
                rollback.append({"stage": "managed-runtime-restore", "error": str(rollback_error)})
        current = legacy.load_state(root)
        raise RuntimeError(
            "CogentNexus-OpenClaw transactional disable failed; pre-disable Host state was preserved. "
            f"cause={error}; priorMode={prior.get('mode')}; currentMode={current.get('mode')}; rollback={rollback}"
        ) from error

    return {
        "mode": state["mode"],
        "policyChanged": policy_changed,
        "policy": legacy.policy_info(root),
        "startup": legacy.parse_json_output(startup_result.stdout),
        "gateway": gateway,
        "transactional": True,
        "note": "OpenClaw is running in passthrough mode; CogentNexus-OpenClaw no longer intercepts new turns. The registered managed policy is preserved for the next enable.",
    }


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    """Quiescent fast path plus confirmed hard-hang recovery."""
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
        if not gateway_ok and execute_safe:
            hard_hang_restart = _restart_unresponsive_gateway(root)

    provider_required = state.get("desiredProvider") == "running"
    provider_ok = (not provider_required) or ollama_fast_probe()
    work_pending = durable_work_hint(root)
    if gateway_ok and provider_ok and not work_pending:
        return {
            "result": "idle",
            "action": "none",
            "probe": "lightweight-http+sqlite-ro",
            "gatewayHealthy": True,
            "providerRequired": provider_required,
            "providerHealthy": provider_ok,
            "durableWorkPending": False,
        }

    # Hard hangs are restarted first under recoverable maintenance authority.
    # The proven heavy path then verifies health, clears restart maintenance,
    # recovers provider/workflow state, and promotes interrupted Direct Tickets.
    result = LEGACY_SUPERVISOR_TICK(root, execute_safe)
    if hard_hang_restart is not None and isinstance(result, dict):
        result = dict(result)
        result["hardHangRecovery"] = hard_hang_restart
    return result


# Keep the proven parser/command surface and replace only hardened paths. All
# legacy lifecycle paths resolve this module attribute dynamically, so this
# assignment fences start/restart/supervisor promotion as well as enable.
legacy.promote_interrupted_direct = promote_interrupted_direct_v091
legacy.enable = enable
legacy.disable = disable
legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())