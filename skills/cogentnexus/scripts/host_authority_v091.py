#!/usr/bin/env python3
"""CogentNexus v0.9.1 single-authority activation overlay.

This overlay moves the MANAGED Host state transition to the one durable
linearization point between safe staging and inference-capable plugin startup.
The plugin itself accepts only controller.mode=managed.

Power-loss semantics:
- before the MANAGED commit: plugin discovery/reload is inert;
- after the MANAGED commit: startup adapter + enabled plugin config already
  exist, so reboot can resume the requested managed runtime deterministically.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import host_v091 as v091

legacy = v091.legacy
BASE_DIRECT_DELIVERY_FENCE = v091.reconcile_direct_delivery_before_recovery


def _rollback_to_passthrough(root: Path, prior: dict[str, Any]) -> dict[str, Any]:
    """Restore native authority without incrementing generation during rollback."""
    restored = dict(prior)
    restored.update({
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
    })
    return legacy.save_state(root, restored)


def reconcile_direct_delivery_authority(root: Path, cutoff_iso: str) -> dict[str, Any]:
    """Apply the v0.9.1 delivery fence and revoke any inference retry it supersedes.

    A durable Direct result is exact transport-owned text. If an older recovery
    row is still pending/running from a prior generation or compatibility path,
    leaving it inference-eligible would let the Direct Recovery worker regenerate
    a response that already exists durably. The Host therefore moves such rows
    to `awaiting_delivery` at the same authoritative fence that restores the
    Ticket to accepted/workflow_eligible=0.
    """
    result = BASE_DIRECT_DELIVERY_FENCE(root, cutoff_iso)
    held = [str(ticket_id) for ticket_id in result.get("durableDeliveryHeld", []) if ticket_id]
    if not held:
        return result

    path = legacy.ticket_db(root)
    if not path.exists():
        return result
    db = sqlite3.connect(path, timeout=5)
    try:
        if not v091._db_table_exists(db, "cnx_direct_recovery"):
            return result
        stamp = legacy.now_iso()
        db.execute("BEGIN IMMEDIATE")
        has_events = v091._db_table_exists(db, "ticket_events")
        for ticket_id in held:
            changed = db.execute(
                "UPDATE cnx_direct_recovery "
                "SET state='awaiting_delivery',active_run_id=NULL,next_attempt_at=NULL,"
                "last_error='durable direct result owns delivery; inference recovery suppressed',updated_at=? "
                "WHERE ticket_id=? AND state NOT IN ('cancelled','done','awaiting_delivery')",
                (stamp, ticket_id),
            )
            if changed.rowcount and has_events:
                db.execute(
                    "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                    (
                        ticket_id,
                        "host_direct_recovery_suppressed_by_durable_delivery",
                        json.dumps(
                            {
                                "source": "host-v091-single-authority-fence",
                                "recoveryState": "awaiting_delivery",
                                "reason": "durable direct result owns delivery; inference recovery suppressed",
                            },
                            ensure_ascii=False,
                        ),
                        stamp,
                    ),
                )
        db.commit()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Every v0.9.1 Host path imported after this overlay, including the Direct
# model-call stall overlay, uses the same transport-before-inference fence.
v091.reconcile_direct_delivery_before_recovery = reconcile_direct_delivery_authority


def enable(root: Path) -> dict[str, Any]:
    """Commit MANAGED exactly once before inference-capable plugin activation."""
    legacy.initialize(root)
    prior = legacy.load_state(root)
    workspace = root.parent
    agents_path = workspace / "AGENTS.md"
    agents_snapshot = v091._snapshot_file(agents_path)
    started = legacy.now_iso()

    # These classifiers are authoritative before any plugin surface may execute.
    terminal_fences = legacy.reconcile_terminal_fences(root)
    direct_delivery_fences = v091.reconcile_direct_delivery_before_recovery(root, started)

    policy_changed = False
    configuration_attempted = False
    startup_attempted = False
    plugin_enable_attempted = False
    authority_committed = False
    runtime_restart_attempted = False
    runtime_start_attempted = False
    rollback: list[dict[str, Any]] = []

    try:
        # Stage everything that is safe while Host remains PASSTHROUGH.
        legacy.plugin_enabled(False)
        configuration_attempted = True
        v091.configure_managed_plugin()
        v091.validate_managed_config()

        policy_changed = legacy.apply_policy(workspace, root)

        # Install the external recovery substrate before the authority commit.
        # If interrupted here, scheduled ticks observe PASSTHROUGH and do nothing.
        startup_attempted = True
        startup_result = legacy.startup(root, "enable", check=True)

        # Enable plugin configuration while still PASSTHROUGH. The release-entry
        # Host gate deliberately suppresses runtime registration at this point.
        plugin_enable_attempted = True
        legacy.plugin_enabled(True)

        # Durable linearization point. From this write onward the user's enable
        # intent is committed and plugin recovery authority is valid.
        state = legacy.transition(
            root,
            mode="managed",
            desiredGateway="running",
            desiredProvider="running",
        )
        authority_committed = True

        # Force a post-commit Gateway process boundary so a plugin that was
        # suppressed during PASSTHROUGH is registered only under MANAGED state.
        runtime_restart_attempted = True
        restart = legacy.runtime(
            root,
            "lifecycle",
            "restart",
            "--reason",
            "CogentNexus MANAGED authority committed; reload plugin under Host authority",
            timeout=240,
            check=True,
        )

        runtime_start_attempted = True
        lifecycle = legacy.runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)

        gateway = legacy.gateway_status()
        if not gateway.get("healthy"):
            raise RuntimeError(f"Gateway failed managed health verification: {gateway}")

        session_bootstrap = legacy.reconcile_default_session()
        if session_bootstrap.get("ok") is False and not session_bootstrap.get("skipped"):
            raise RuntimeError(f"default session bootstrap failed: {session_bootstrap}")
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
            v091._restore_file(agents_path, agents_snapshot)
            rollback.append({"stage": "policy-restore", "ok": True})
        except Exception as rollback_error:
            rollback.append({"stage": "policy-restore", "error": str(rollback_error)})

        if configuration_attempted or plugin_enable_attempted or authority_committed or runtime_restart_attempted or runtime_start_attempted:
            try:
                rollback.append({"stage": "native-gateway-restore", **v091._restore_native_gateway()})
            except Exception as rollback_error:
                rollback.append({"stage": "native-gateway-restore", "error": str(rollback_error)})

        try:
            rolled_state = _rollback_to_passthrough(root, prior)
            rollback.append({
                "stage": "host-state-rollback",
                "mode": rolled_state.get("mode"),
                "generation": rolled_state.get("generation"),
                "authorityHadCommitted": authority_committed,
            })
        except Exception as rollback_error:
            rollback.append({"stage": "host-state-rollback", "error": str(rollback_error)})

        current = legacy.load_state(root)
        raise RuntimeError(
            "CogentNexus transactional enable failed; native passthrough rollback executed. "
            f"cause={error}; priorMode={prior.get('mode')}; currentMode={current.get('mode')}; "
            f"authorityCommitted={authority_committed}; rollback={rollback}"
        ) from error

    recovery_error = None
    recovered: list[str] = []
    try:
        recovered = v091.promote_interrupted_direct_v091(
            root,
            started,
            "CogentNexus Host enabled after an interrupted OpenClaw runtime",
        )
        legacy.runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)
    except Exception as error:
        recovery_error = str(error)

    return {
        "mode": state["mode"],
        "authorityCommit": {
            "mode": state["mode"],
            "generation": state.get("generation"),
            "linearizedBeforePluginReload": True,
        },
        "policyChanged": policy_changed,
        "policy": legacy.policy_info(root),
        "startup": legacy.parse_json_output(startup_result.stdout),
        "reload": legacy.parse_json_output(restart.stdout),
        "lifecycle": legacy.parse_json_output(lifecycle.stdout),
        "sessionBootstrap": session_bootstrap,
        "terminalFences": terminal_fences,
        "directDeliveryFences": direct_delivery_fences,
        "recoveredTickets": recovered,
        "postCommitRecoveryError": recovery_error,
        "transactional": True,
    }


# Importing host_v091 installs every other hardened v0.9.1 path. Replace only
# enable with the single-authority activation ordering above.
legacy.enable = enable


if __name__ == "__main__":
    raise SystemExit(legacy.main())
