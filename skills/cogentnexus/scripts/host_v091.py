#!/usr/bin/env python3
"""CogentNexus v0.9.1 live-hardening compatibility layer.

Keeps the proven Host implementation intact while adding the invariants found
by live Windows acceptance and end-to-end wiring review:

1. enable is transactional: failure returns to native passthrough state;
2. disable commits passthrough only after CNX surfaces are removed and native
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
from pathlib import Path
from typing import Any

import host as legacy

HERE = Path(__file__).resolve()
LEGACY_SUPERVISOR_TICK = legacy.supervisor_tick
IDLE_GATEWAY_PORT = 18789
IDLE_OLLAMA_PORT = 11434
IDLE_PROBE_TIMEOUT_SECONDS = 0.75


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


def durable_work_hint(root: Path) -> bool:
    """Read-only fallback hint for committed work that should wake recovery.

    The scheduled supervisor must not assume that healthy TCP endpoints imply
    healthy workers. If a Ticket/outbox/recovery row remains actionable, enter
    the proven heavy reconciliation path even while Gateway and Ollama respond.
    """
    path = legacy.ticket_db(root)
    if not path.exists():
        return False
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=0.25)
    except sqlite3.Error:
        return True
    try:
        if not _db_table_exists(db, "tickets"):
            return False
        if db.execute("SELECT 1 FROM tickets WHERE status NOT IN ('completed','failed','cancelled') LIMIT 1").fetchone():
            return True
        if _db_table_exists(db, "ticket_outbox") and db.execute(
            "SELECT 1 FROM ticket_outbox WHERE delivery_status='pending' LIMIT 1"
        ).fetchone():
            return True
        if _db_table_exists(db, "cnx_direct_recovery") and db.execute(
            "SELECT 1 FROM cnx_direct_recovery WHERE state IN ('pending','claimed','running','degraded') LIMIT 1"
        ).fetchone():
            return True
        if _db_table_exists(db, "cnx_context_maintenance") and db.execute(
            "SELECT 1 FROM cnx_context_maintenance WHERE state IN ('pending','running','degraded') LIMIT 1"
        ).fetchone():
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

    Polling defaults are deliberately relaxed from 5s to 60s. Event hooks still
    handle normal request/delivery boundaries immediately; periodic work is a
    recovery safety net, not the primary execution mechanism.
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


def enable(root: Path) -> dict[str, Any]:
    """Enter MANAGED only after every activation stage is verified."""
    legacy.initialize(root)
    prior = legacy.load_state(root)
    workspace = root.parent
    agents_path = workspace / "AGENTS.md"
    agents_snapshot = _snapshot_file(agents_path)
    started = legacy.now_iso()

    # Terminal intent must be authoritative before any inference-capable CNX
    # surface can wake. This cleanup is durable/idempotent and intentionally is
    # not rolled back if a later activation stage fails.
    terminal_fences = legacy.reconcile_terminal_fences(root)

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
            "CogentNexus transactional enable failed; native passthrough rollback executed. "
            f"cause={error}; priorMode={prior.get('mode')}; currentMode={current.get('mode')}; rollback={rollback}"
        ) from error

    recovery_error = None
    recovered: list[str] = []
    try:
        recovered = legacy.promote_interrupted_direct(
            root,
            started,
            "CogentNexus Host enabled after an interrupted OpenClaw runtime",
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
        "sessionBootstrap": session_bootstrap,
        "terminalFences": terminal_fences,
        "recoveredTickets": recovered,
        "postCommitRecoveryError": recovery_error,
        "transactional": True,
    }


def disable(root: Path) -> dict[str, Any]:
    """Remove CNX surfaces first; commit PASSTHROUGH only after native health."""
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
            "CogentNexus transactional disable failed; pre-disable Host state was preserved. "
            f"cause={error}; priorMode={prior.get('mode')}; currentMode={current.get('mode')}; rollback={rollback}"
        ) from error

    return {
        "mode": state["mode"],
        "policyChanged": policy_changed,
        "policy": legacy.policy_info(root),
        "startup": legacy.parse_json_output(startup_result.stdout),
        "gateway": gateway,
        "transactional": True,
        "note": "OpenClaw is running in passthrough mode; CogentNexus no longer intercepts new turns. The registered managed policy is preserved for the next enable.",
    }


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    """Quiescent fast path for the external scheduled supervisor."""
    legacy.initialize(root)
    state = legacy.load_state(root)
    if state.get("mode") != "managed":
        return {"result": "passthrough", "mode": state.get("mode"), "action": "none"}
    if state.get("desiredGateway") != "running":
        return {"result": "maintenance", "desiredGateway": state.get("desiredGateway"), "action": "none"}

    gateway_ok = gateway_fast_probe()
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

    # Only endpoint failure or visible committed work pays the cost of OpenClaw
    # CLI, lifecycle status, durable reconciliation, and recovery promotion.
    return LEGACY_SUPERVISOR_TICK(root, execute_safe)


# Keep the proven parser/command surface and replace only hardened paths.
legacy.enable = enable
legacy.disable = disable
legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
