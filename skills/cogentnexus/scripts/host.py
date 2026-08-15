#!/usr/bin/env python3
"""CogentNexus Host Controller.

Runs outside OpenClaw inference. It owns desired runtime state, managed policy
selection, Gateway/provider lifecycle coordination, deterministic recovery,
Ticket/session cancellation, and MANAGED/PASSTHROUGH/MAINTENANCE semantics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogent"
PLUGIN_ID = "cogentnexus-rotation"
BEGIN = "<!-- cogentnexus:begin -->"
END = "<!-- cogentnexus:end -->"
TERMINAL_TICKETS = {"completed", "failed", "cancelled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def run(cmd: list[str], timeout: int = 120, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, creationflags=creation_flags())
    if check and result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f"command failed: {cmd}").strip())
    return result


def python_exe() -> str:
    return sys.executable or "python"


def openclaw_executable() -> str:
    # npm installs OpenClaw through platform shims on Windows. PowerShell can
    # resolve openclaw.ps1/openclaw.cmd automatically, but CreateProcess used by
    # subprocess.run(shell=False) cannot reliably execute a bare shim name.
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


def host_state_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def policy_snapshot_path(root: Path) -> Path:
    return root / "host" / "managed-policy.md"


def default_policy_template() -> Path:
    return SKILL / "templates" / "AGENTS.cogentnexus.md"


def default_state() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "mode": "managed",
        "desiredGateway": "running",
        "desiredProvider": "running",
        "generation": 1,
        "updatedAt": now_iso(),
    }


def load_state(root: Path) -> dict[str, Any]:
    try:
        data = json.loads(host_state_path(root).read_text(encoding="utf-8"))
        if data.get("schemaVersion") != 1 or data.get("mode") not in {"managed", "passthrough", "maintenance"}:
            raise ValueError("invalid host state")
        return data
    except FileNotFoundError:
        return default_state()


def save_state(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    path = host_state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    next_state = dict(state)
    next_state["schemaVersion"] = 1
    next_state["updatedAt"] = now_iso()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(next_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return next_state


def transition(root: Path, **changes: Any) -> dict[str, Any]:
    state = load_state(root)
    state.update(changes)
    state["generation"] = int(state.get("generation", 0)) + 1
    return save_state(root, state)


def runtime_path() -> Path: return HERE.with_name("runtime.py")
def startup_path() -> Path: return HERE.with_name("startup.py")
def workflow_path() -> Path: return HERE.with_name("workflow.py")


def runtime(root: Path, *args: str, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([python_exe(), str(runtime_path()), "--root", str(root), *args], timeout=timeout, check=check)


def startup(root: Path, action: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([python_exe(), str(startup_path()), "--root", str(root), action], timeout=120, check=check)


def gateway_status(timeout: int = 30) -> dict[str, Any]:
    try:
        result = run([openclaw_executable(), "gateway", "status"], timeout=timeout)
        return {
            "healthy": result.returncode == 0,
            "exitCode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {"healthy": False, "error": str(error)}


def plugin_enabled(enabled: bool) -> None:
    run([openclaw_executable(), "plugins", "enable" if enabled else "disable", PLUGIN_ID], timeout=60, check=True)


def configure_managed_plugin() -> None:
    settings = [
        ("ticketFirst", "true"),
        ("preInferenceAdmission", "true"),
        ("autoWorkflowCompletion", "true"),
        ("enforcedMode", "true"),
        ("autoResume", "true"),
        ("ticketDispatchLimit", "1"),
        ("ticketMaximumRunning", "1"),
        ("ticketMaximumAttempts", "5"),
        ("ticketRecoveryPollMs", "5000"),
        ("ticketDispatchPollMs", "5000"),
        ("ticketOutboxPollMs", "5000"),
    ]
    for key, value in settings:
        run([openclaw_executable(), "config", "set", f"plugins.entries.{PLUGIN_ID}.config.{key}", value], timeout=60, check=True)
    run([openclaw_executable(), "config", "set", f"plugins.entries.{PLUGIN_ID}.hooks.allowConversationAccess", "true"], timeout=60, check=True)


def normalize_policy(text: str) -> str:
    if not text.strip() or "\ufffd" in text:
        raise RuntimeError("managed policy is empty or invalid UTF-8")
    if BEGIN in text or END in text:
        raise RuntimeError("managed policy source must not contain CogentNexus block markers")
    return text.strip() + "\n"


def read_policy(root: Path) -> tuple[str, str]:
    snapshot = policy_snapshot_path(root)
    if snapshot.exists():
        return normalize_policy(snapshot.read_text(encoding="utf-8")), "registered"
    template = default_policy_template()
    if not template.exists():
        raise RuntimeError(f"CogentNexus default policy template not found: {template}")
    return normalize_policy(template.read_text(encoding="utf-8")), "core-default"


def save_policy_snapshot(root: Path, text: str) -> Path:
    policy = normalize_policy(text)
    path = policy_snapshot_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(policy, encoding="utf-8", newline="\n")
    os.replace(temporary, path)
    return path


def policy_info(root: Path) -> dict[str, Any]:
    policy, source = read_policy(root)
    return {
        "source": source,
        "path": str(policy_snapshot_path(root)),
        "sha256": hashlib.sha256(policy.encode("utf-8")).hexdigest(),
        "bytes": len(policy.encode("utf-8")),
    }


def merge_policy(existing: str, policy: str) -> str:
    block = f"{BEGIN}\n{policy.strip()}\n{END}"
    start, finish = existing.find(BEGIN), existing.find(END)
    if (start < 0) != (finish < 0) or (start >= 0 and finish < start):
        raise RuntimeError("AGENTS.md contains an incomplete CogentNexus managed block")
    if start >= 0:
        finish += len(END)
        updated = existing[:start] + block + existing[finish:]
    else:
        updated = existing.rstrip() + ("\n\n" if existing.strip() else "") + block + "\n"
    return updated if updated.endswith("\n") else updated + "\n"


def remove_policy_text(existing: str) -> str:
    start, finish = existing.find(BEGIN), existing.find(END)
    if start < 0 and finish < 0:
        return existing
    if start < 0 or finish < 0 or finish < start:
        raise RuntimeError("AGENTS.md contains an incomplete CogentNexus managed block")
    finish += len(END)
    before = existing[:start].rstrip()
    after = existing[finish:].lstrip("\r\n")
    result = (before + "\n\n" + after) if before and after else before + after
    return result.rstrip() + ("\n" if result.strip() else "")


def write_agents(workspace: Path, content: str) -> bool:
    agents = workspace / "AGENTS.md"
    previous = agents.read_text(encoding="utf-8") if agents.exists() else ""
    if previous == content:
        return False
    if agents.exists():
        backup_root = workspace / ".cogent" / "install-backups"
        backup_root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(agents, backup_root / f"AGENTS.pre-host-change-{stamp}.md")
    workspace.mkdir(parents=True, exist_ok=True)
    temp = agents.with_suffix(".md.tmp")
    temp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temp, agents)
    return True


def apply_policy(workspace: Path, root: Path) -> bool:
    policy, _ = read_policy(root)
    agents = workspace / "AGENTS.md"
    existing = agents.read_text(encoding="utf-8") if agents.exists() else ""
    return write_agents(workspace, merge_policy(existing, policy))


def remove_policy(workspace: Path) -> bool:
    agents = workspace / "AGENTS.md"
    return False if not agents.exists() else write_agents(workspace, remove_policy_text(agents.read_text(encoding="utf-8")))


def register_policy(root: Path, source: Path) -> dict[str, Any]:
    source = source.resolve()
    if not source.is_file():
        raise RuntimeError(f"managed policy file not found: {source}")
    save_policy_snapshot(root, source.read_text(encoding="utf-8"))
    applied = False
    if load_state(root).get("mode") != "passthrough":
        applied = apply_policy(root.parent, root)
    return {"registeredFrom": str(source), "applied": applied, "policy": policy_info(root)}


def reset_policy(root: Path) -> dict[str, Any]:
    template = default_policy_template()
    if not template.exists():
        raise RuntimeError(f"CogentNexus default policy template not found: {template}")
    save_policy_snapshot(root, template.read_text(encoding="utf-8"))
    applied = False
    if load_state(root).get("mode") != "passthrough":
        applied = apply_policy(root.parent, root)
    return {"resetTo": str(template), "applied": applied, "policy": policy_info(root)}


def apply_registered_policy(root: Path) -> dict[str, Any]:
    if load_state(root).get("mode") == "passthrough":
        return {"applied": False, "reason": "passthrough", "policy": policy_info(root)}
    return {"applied": apply_policy(root.parent, root), "policy": policy_info(root)}


def ticket_db(root: Path) -> Path:
    return root / "runtime" / "cogentnexus.sqlite3"


def table_exists(db: sqlite3.Connection, table: str) -> bool:
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone() is not None


def promote_interrupted_direct(root: Path, cutoff_iso: str, reason: str) -> list[str]:
    path = ticket_db(root)
    if not path.exists():
        return []
    db = sqlite3.connect(path, timeout=5)
    try:
        db.execute("PRAGMA foreign_keys=ON")
        if not table_exists(db, "tickets") or not table_exists(db, "ticket_events"):
            return []
        db.execute("BEGIN IMMEDIATE")
        rows = db.execute(
            "SELECT ticket_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND created_at<? ORDER BY created_at,ticket_id",
            (cutoff_iso,),
        ).fetchall()
        updated = []
        stamp = now_iso()
        for (ticket_id,) in rows:
            changed = db.execute(
                "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0",
                (reason[:2000], stamp, ticket_id),
            )
            if changed.rowcount != 1:
                continue
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (ticket_id, "host_recovered_direct", json.dumps({"reason": reason, "cutoff": cutoff_iso}), stamp),
            )
            updated.append(ticket_id)
        db.commit()
        return updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def ticket_snapshot(root: Path) -> dict[str, Any]:
    path = ticket_db(root)
    if not path.exists():
        return {"database": str(path), "tickets": {}, "pendingOutbox": 0}
    db = sqlite3.connect(path, timeout=5)
    try:
        if not table_exists(db, "tickets"):
            return {"database": str(path), "tickets": {}, "pendingOutbox": 0}
        counts = {row[0]: int(row[1]) for row in db.execute("SELECT status,count(*) FROM tickets GROUP BY status")}
        pending = 0
        if table_exists(db, "ticket_outbox"):
            pending = int(db.execute("SELECT count(*) FROM ticket_outbox WHERE delivery_status='pending'").fetchone()[0])
        return {"database": str(path), "tickets": counts, "pendingOutbox": pending}
    finally:
        db.close()


def cancel_ticket(root: Path, ticket_id: str, reason: str) -> dict[str, Any]:
    path = ticket_db(root)
    if not path.exists():
        raise RuntimeError("Ticket database does not exist")
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        row = db.execute(
            "SELECT ticket_id,status,workflow_id,owner_session_key FROM tickets WHERE ticket_id=?", (ticket_id,)
        ).fetchone()
        if not row:
            raise RuntimeError(f"Ticket not found: {ticket_id}")
        if row["status"] in TERMINAL_TICKETS:
            return {"ticketId": ticket_id, "status": row["status"], "changed": False}
        if row["workflow_id"]:
            result = run(
                [python_exe(), str(workflow_path()), "--root", str(root.parent), "cancel", row["workflow_id"], "--reason", reason],
                timeout=60,
            )
            if result.returncode != 0:
                raise RuntimeError((result.stderr or result.stdout or "workflow cancellation failed").strip())
        stamp = now_iso()
        db.execute("BEGIN IMMEDIATE")
        changed = db.execute(
            "UPDATE tickets SET status='cancelled',worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=? AND status NOT IN ('completed','failed','cancelled')",
            (reason[:2000], stamp, ticket_id),
        )
        if changed.rowcount == 1:
            db.execute(
                "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
                (ticket_id, "cancelled", json.dumps({"reason": reason, "source": "host"}), stamp),
            )
            if table_exists(db, "ticket_outbox"):
                payload = json.dumps({"classification": "interrupted", "message": reason, "source": "host"})
                db.execute(
                    "INSERT OR IGNORE INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,created_at) VALUES (?,?,'cancelled',?,'pending',?)",
                    (ticket_id, row["owner_session_key"], payload, stamp),
                )
        db.commit()
        return {"ticketId": ticket_id, "status": "cancelled", "changed": changed.rowcount == 1}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def cancel_session(root: Path, session_key: str, reason: str) -> dict[str, Any]:
    path = ticket_db(root)
    if not path.exists():
        return {"sessionKey": session_key, "cancelled": []}
    db = sqlite3.connect(path, timeout=5)
    try:
        ids = [
            row[0]
            for row in db.execute(
                "SELECT ticket_id FROM tickets WHERE owner_session_key=? AND status NOT IN ('completed','failed','cancelled') ORDER BY created_at",
                (session_key,),
            ).fetchall()
        ]
    finally:
        db.close()
    return {"sessionKey": session_key, "cancelled": [cancel_ticket(root, ticket_id, reason) for ticket_id in ids]}


def list_tickets(root: Path, limit: int = 50) -> list[dict[str, Any]]:
    path = ticket_db(root)
    if not path.exists():
        return []
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        return [
            dict(row)
            for row in db.execute(
                "SELECT ticket_id,owner_session_key,status,workflow_eligible,workflow_id,attempt_count,failure_class,created_at,updated_at FROM tickets ORDER BY created_at DESC LIMIT ?",
                (max(1, min(limit, 500)),),
            ).fetchall()
        ]
    finally:
        db.close()


def initialize(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    state = load_state(root)
    if not host_state_path(root).exists():
        state = save_state(root, state)
    if not policy_snapshot_path(root).exists():
        template = default_policy_template()
        if not template.exists():
            raise RuntimeError(f"CogentNexus default policy template not found: {template}")
        save_policy_snapshot(root, template.read_text(encoding="utf-8"))
    return state


def parse_json_output(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def enable(root: Path) -> dict[str, Any]:
    initialize(root)
    workspace = root.parent
    started = now_iso()
    state = transition(root, mode="managed", desiredGateway="running", desiredProvider="running")
    policy_changed = apply_policy(workspace, root)
    plugin_enabled(True)
    configure_managed_plugin()
    startup_result = startup(root, "enable", check=True)
    lifecycle = runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)
    recovered = promote_interrupted_direct(root, started, "CogentNexus Host enabled after an interrupted OpenClaw runtime")
    runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)
    return {
        "mode": state["mode"],
        "policyChanged": policy_changed,
        "policy": policy_info(root),
        "startup": parse_json_output(startup_result.stdout),
        "lifecycle": parse_json_output(lifecycle.stdout),
        "recoveredTickets": recovered,
    }


def disable(root: Path) -> dict[str, Any]:
    initialize(root)
    workspace = root.parent
    state = transition(root, mode="passthrough", desiredGateway="running", desiredProvider="unchanged")
    startup_result = startup(root, "disable", check=True)
    policy_changed = remove_policy(workspace)
    plugin_enabled(False)
    runtime(root, "lifecycle", "cancel", timeout=60, check=False)
    restart = run([openclaw_executable(), "gateway", "restart"], timeout=180)
    if restart.returncode != 0:
        restart = run([openclaw_executable(), "gateway", "start"], timeout=180, check=True)
    return {
        "mode": state["mode"],
        "policyChanged": policy_changed,
        "policy": policy_info(root),
        "startup": parse_json_output(startup_result.stdout),
        "gateway": {"exitCode": restart.returncode, "stdout": restart.stdout.strip(), "stderr": restart.stderr.strip()},
        "note": "OpenClaw is running in passthrough mode; CogentNexus no longer intercepts new turns. The registered managed policy is preserved for the next enable.",
    }


def start_managed(root: Path, provider: bool = True) -> dict[str, Any]:
    initialize(root)
    prior = load_state(root)
    started = now_iso()
    state = transition(
        root,
        mode="managed",
        desiredGateway="running",
        desiredProvider="running" if provider else prior.get("desiredProvider", "unchanged"),
    )
    result = runtime(root, "lifecycle", "start", *(["--provider"] if provider else []), timeout=240, check=True)
    recovered = promote_interrupted_direct(root, started, "Gateway resumed by CogentNexus Host after interruption")
    runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)
    return {"state": state, "lifecycle": parse_json_output(result.stdout), "recoveredTickets": recovered}


def stop_managed(root: Path, provider: bool = True) -> dict[str, Any]:
    initialize(root)
    prior = load_state(root)
    state = transition(
        root,
        mode="maintenance",
        desiredGateway="stopped",
        desiredProvider="stopped" if provider else prior.get("desiredProvider", "unchanged"),
    )
    result = runtime(root, "lifecycle", "stop", *(["--provider"] if provider else []), timeout=240, check=True)
    return {"state": state, "lifecycle": parse_json_output(result.stdout)}


def restart_managed(root: Path) -> dict[str, Any]:
    initialize(root)
    started = now_iso()
    state = transition(root, mode="managed", desiredGateway="running")
    result = runtime(root, "lifecycle", "restart", "--reason", "CogentNexus Host requested restart", timeout=240, check=True)
    recovered = promote_interrupted_direct(root, started, "Gateway restarted by CogentNexus Host")
    runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)
    return {"state": state, "lifecycle": parse_json_output(result.stdout), "recoveredTickets": recovered}


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    initialize(root)
    state = load_state(root)
    if state.get("mode") != "managed":
        return {"result": "passthrough", "mode": state.get("mode"), "action": "none"}
    if state.get("desiredGateway") != "running":
        return {"result": "maintenance", "desiredGateway": state.get("desiredGateway"), "action": "none"}
    cutoff = now_iso()
    before = gateway_status()
    lifecycle_status = runtime(root, "lifecycle", "status", timeout=60, check=False)
    lifecycle_before = (
        parse_json_output(lifecycle_status.stdout)
        if lifecycle_status.stdout.strip()
        else {"exitCode": lifecycle_status.returncode, "stderr": lifecycle_status.stderr.strip()}
    )
    provider_required = state.get("desiredProvider") == "running"
    provider_healthy = bool(
        isinstance(lifecycle_before, dict)
        and isinstance(lifecycle_before.get("ollama"), dict)
        and lifecycle_before["ollama"].get("healthy")
    )
    reconcile = None
    if execute_safe and (not before.get("healthy") or (provider_required and not provider_healthy)):
        reconcile_args = ["lifecycle", "start"] + (["--provider"] if provider_required else [])
        reconcile_result = runtime(root, *reconcile_args, timeout=240, check=False)
        reconcile = {
            "exitCode": reconcile_result.returncode,
            "output": parse_json_output(reconcile_result.stdout) if reconcile_result.stdout.strip() else None,
            "stderr": reconcile_result.stderr.strip(),
            "providerRequired": provider_required,
        }
    args = ["supervisor", "tick"] + (["--execute-safe"] if execute_safe else [])
    result = runtime(root, *args, timeout=180, check=False)
    after = gateway_status()
    recovered = []
    if not before.get("healthy") and after.get("healthy"):
        recovered = promote_interrupted_direct(root, cutoff, "CogentNexus Host confirmed Gateway recovery; prior direct turn was interrupted")
    return {
        "result": "ok" if result.returncode == 0 else "runtime-error",
        "before": before,
        "lifecycleBefore": lifecycle_before,
        "reconcile": reconcile,
        "after": after,
        "runtime": parse_json_output(result.stdout) if result.stdout.strip() else {"stderr": result.stderr.strip()},
        "recoveredTickets": recovered,
    }


def status(root: Path) -> dict[str, Any]:
    initialize(root)
    state = load_state(root)
    startup_result = startup(root, "status", check=False)
    return {
        "state": state,
        "policy": policy_info(root),
        "gateway": gateway_status(),
        "startup": parse_json_output(startup_result.stdout) if startup_result.stdout else {"exitCode": startup_result.returncode},
        "tickets": ticket_snapshot(root),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["init", "status", "enable", "disable", "start", "stop", "restart"]:
        sub.add_parser(name)

    gateway = sub.add_parser("gateway")
    gateway.add_argument("action", choices=["start", "stop", "restart"])

    supervisor = sub.add_parser("supervisor")
    supervisor.add_argument("action", choices=["tick"])
    supervisor.add_argument("--execute-safe", action="store_true")

    ticket = sub.add_parser("ticket")
    ticket_sub = ticket.add_subparsers(dest="ticket_action", required=True)
    list_cmd = ticket_sub.add_parser("list")
    list_cmd.add_argument("--limit", type=int, default=50)
    cancel_cmd = ticket_sub.add_parser("cancel")
    cancel_cmd.add_argument("ticket_id")
    cancel_cmd.add_argument("--reason", default="cancelled by operator")

    session = sub.add_parser("session")
    session_sub = session.add_subparsers(dest="session_action", required=True)
    session_cancel = session_sub.add_parser("cancel")
    session_cancel.add_argument("session_key")
    session_cancel.add_argument("--reason", default="session cancelled by operator")

    policy = sub.add_parser("policy")
    policy_sub = policy.add_subparsers(dest="policy_action", required=True)
    policy_sub.add_parser("status")
    register = policy_sub.add_parser("register")
    register.add_argument("path", type=Path)
    policy_sub.add_parser("reset")
    policy_sub.add_parser("apply")
    return parser


def command(args: argparse.Namespace) -> Any:
    root = args.root.resolve()
    if args.command == "init":
        return {"state": initialize(root), "policy": policy_info(root)}
    if args.command == "status":
        return status(root)
    if args.command == "enable":
        return enable(root)
    if args.command == "disable":
        return disable(root)
    if args.command in {"start", "stop", "restart"}:
        if load_state(root).get("mode") == "passthrough":
            raise RuntimeError(
                "CogentNexus is disabled (PASSTHROUGH). Use 'cnx enable' to enter MANAGED mode, "
                "or use 'cnx gateway <start|stop|restart>' / native OpenClaw lifecycle commands "
                "without changing CogentNexus mode."
            )
        if args.command == "start":
            return start_managed(root, True)
        if args.command == "stop":
            return stop_managed(root, True)
        return restart_managed(root)
    if args.command == "gateway":
        if load_state(root).get("mode") == "passthrough":
            result = run([openclaw_executable(), "gateway", args.action], timeout=180, check=True)
            return {"mode": "passthrough", "gateway": {"action": args.action, "stdout": result.stdout.strip()}}
        if args.action == "start":
            return start_managed(root, False)
        if args.action == "stop":
            return stop_managed(root, False)
        return restart_managed(root)
    if args.command == "supervisor":
        return supervisor_tick(root, args.execute_safe)
    if args.command == "ticket":
        return {"tickets": list_tickets(root, args.limit)} if args.ticket_action == "list" else cancel_ticket(root, args.ticket_id, args.reason)
    if args.command == "session":
        return cancel_session(root, args.session_key, args.reason)
    if args.command == "policy":
        initialize(root)
        if args.policy_action == "status":
            return {"policy": policy_info(root)}
        if args.policy_action == "register":
            return register_policy(root, args.path)
        if args.policy_action == "reset":
            return reset_policy(root)
        if args.policy_action == "apply":
            return apply_registered_policy(root)
    raise RuntimeError("unsupported command")


def main() -> int:
    args = build_parser().parse_args()
    try:
        emit(command(args))
        return 0
    except Exception as error:
        emit({"result": "error", "error": str(error)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
