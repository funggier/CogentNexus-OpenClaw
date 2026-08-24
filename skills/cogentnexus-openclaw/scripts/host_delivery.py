#!/usr/bin/env python3
"""Host-owned, session-isolated assistant delivery for CogentNexus-OpenClaw.

Synthetic workers never write control prompts into an owner transcript. They
queue user-facing assistant text here, and this bridge injects that text into
the exact owner session through OpenClaw's official ``chat.inject`` Gateway
method. Session generation/state checks make late delivery after Stop/Delete
non-authoritative.

Delivery attempts are durably leased before any Gateway RPC. This prevents
multiple detached wakeups from issuing concurrent history/injection calls for
the same delivery. Windows CLI timeouts terminate the full process tree so a
command-shim timeout cannot strand descendant Node processes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import sqlite3
import subprocess
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogentnexus-openclaw"
TERMINAL_TICKET_STATUSES = {"completed", "failed", "cancelled"}
DELIVERY_LEASE_SECONDS = 60
DELIVERY_RETRY_AFTER_SECONDS = 30
HISTORY_LIMIT = 24
HISTORY_MAX_CHARS = 120_000
HISTORY_TIMEOUT_SECONDS = 10
INJECT_TIMEOUT_SECONDS = 15


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def captured_text(value: str | bytes | None) -> str:
    """Return subprocess output as text even when Windows supplies no stream."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return str(value)


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    """Terminate a timed-out CLI including descendants created by Windows shims."""
    if process.poll() is not None:
        return
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=creation_flags(),
            )
            return
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
            return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except Exception:
        try:
            process.kill()
        except Exception:
            pass


def run(cmd: list[str], timeout: int = 60, check: bool = False) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=creation_flags(),
        start_new_session=(os.name != "nt"),
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        _terminate_process_tree(process)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except Exception:
                pass
            stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(
            cmd,
            timeout,
            output=stdout if stdout else error.output,
            stderr=stderr if stderr else error.stderr,
        ) from error
    result = subprocess.CompletedProcess(cmd, process.returncode, stdout, stderr)
    if check and result.returncode != 0:
        detail = captured_text(result.stderr) or captured_text(result.stdout) or f"command failed: {cmd}"
        raise RuntimeError(detail.strip())
    return result


def openclaw_executable() -> str:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


def _parse_json_stream(method: str, result: subprocess.CompletedProcess[str]) -> Any:
    """Parse the Gateway JSON response without assuming which captured stream owns it.

    OpenClaw normally writes ``--json`` output to stdout. Windows command shims
    can, however, leave one captured stream unavailable. Prefer stdout, then
    accept stderr only when it is itself valid JSON. Empty successful output is
    not proof of delivery and therefore fails closed with stage diagnostics.
    """
    stdout = captured_text(result.stdout).strip()
    stderr = captured_text(result.stderr).strip()
    candidates = [("stdout", stdout), ("stderr", stderr)]
    parse_errors: list[str] = []
    for name, value in candidates:
        if not value:
            continue
        try:
            return json.loads(value)
        except json.JSONDecodeError as error:
            parse_errors.append(f"{name}: {error.msg} at {error.pos}")
    if not stdout and not stderr:
        raise RuntimeError(
            f"OpenClaw Gateway RPC {method} returned no JSON output "
            f"(exit={result.returncode}, stdout={'none' if result.stdout is None else 'empty'}, "
            f"stderr={'none' if result.stderr is None else 'empty'})"
        )
    preview = stdout or stderr
    detail = "; ".join(parse_errors) or "no parseable JSON stream"
    raise RuntimeError(f"OpenClaw Gateway RPC {method} returned invalid JSON ({detail}): {preview[:500]}")


def gateway_rpc(method: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    command = [
        openclaw_executable(),
        "gateway",
        "call",
        method,
        "--params",
        json.dumps(params or {}, ensure_ascii=False, separators=(",", ":")),
        "--json",
    ]
    result = run(command, timeout=timeout, check=True)
    return _parse_json_stream(method, result)


def ticket_db(root: Path) -> Path:
    return root / "runtime" / "cogentnexus-openclaw.sqlite3"


def table_exists(db: sqlite3.Connection, table: str) -> bool:
    return db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def column_exists(db: sqlite3.Connection, table: str, column: str) -> bool:
    if not table_exists(db, table):
        return False
    return any(row[1] == column for row in db.execute(f"PRAGMA table_info({table})"))


def ensure_schema(db: sqlite3.Connection) -> None:
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS cnx_sessions(
          session_key TEXT PRIMARY KEY,
          state TEXT NOT NULL DEFAULT 'active'
            CHECK(state IN ('active','deleting','deleted')),
          generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          deleted_at TEXT,
          delete_reason TEXT
        );
        CREATE TABLE IF NOT EXISTS cnx_assistant_delivery(
          delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
          ticket_id TEXT REFERENCES tickets(ticket_id) ON DELETE CASCADE,
          owner_session_key TEXT NOT NULL,
          owner_generation INTEGER NOT NULL DEFAULT 0,
          kind TEXT NOT NULL,
          text TEXT NOT NULL,
          target_json TEXT,
          idempotency_key TEXT NOT NULL UNIQUE,
          status TEXT NOT NULL DEFAULT 'pending'
            CHECK(status IN ('pending','delivered')),
          attempt_count INTEGER NOT NULL DEFAULT 0,
          last_error TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          delivered_at TEXT,
          claim_token TEXT,
          claim_expires_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_pending
          ON cnx_assistant_delivery(status,owner_session_key,delivery_id);
        """
    )
    if not column_exists(db, "cnx_assistant_delivery", "owner_generation"):
        db.execute("ALTER TABLE cnx_assistant_delivery ADD COLUMN owner_generation INTEGER NOT NULL DEFAULT 0")
    if not column_exists(db, "cnx_assistant_delivery", "claim_token"):
        db.execute("ALTER TABLE cnx_assistant_delivery ADD COLUMN claim_token TEXT")
    if not column_exists(db, "cnx_assistant_delivery", "claim_expires_at"):
        db.execute("ALTER TABLE cnx_assistant_delivery ADD COLUMN claim_expires_at TEXT")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_claim "
        "ON cnx_assistant_delivery(status,claim_expires_at,owner_session_key,delivery_id)"
    )


def delivery_marker(idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()[:32]
    return f"<!-- cogentnexus-delivery:{digest} -->"


def history_contains(session_key: str, marker: str) -> bool:
    history = gateway_rpc(
        "chat.history",
        {"sessionKey": session_key, "limit": HISTORY_LIMIT, "maxChars": HISTORY_MAX_CHARS},
        timeout=HISTORY_TIMEOUT_SECONDS,
    )
    return marker in json.dumps(history, ensure_ascii=False, separators=(",", ":"))


def inject_assistant(session_key: str, text: str, idempotency_key: str) -> dict[str, Any]:
    marker = delivery_marker(idempotency_key)
    # Observation failure is never permission to repeat the side effect. If
    # history cannot be read, this function raises before chat.inject.
    if history_contains(session_key, marker):
        return {"ok": True, "deduplicated": True}
    payload = gateway_rpc(
        "chat.inject",
        {"sessionKey": session_key, "message": f"{text.rstrip()}\n\n{marker}"},
        timeout=INJECT_TIMEOUT_SECONDS,
    )
    if not isinstance(payload, dict) or payload.get("ok") is not True:
        raise RuntimeError(f"chat.inject did not confirm assistant delivery: {payload!r}")
    return {"ok": True, "deduplicated": False, "messageId": payload.get("messageId")}


def session_authority(db: sqlite3.Connection, session_key: str) -> tuple[str, int] | None:
    row = db.execute(
        "SELECT state,generation FROM cnx_sessions WHERE session_key=?", (session_key,)
    ).fetchone()
    if not row:
        return None
    return str(row[0]), int(row[1])


def _event(db: sqlite3.Connection, ticket_id: str, event_type: str, payload: dict[str, Any], stamp: str) -> None:
    if not table_exists(db, "ticket_events"):
        return
    db.execute(
        "INSERT INTO ticket_events(ticket_id,event_type,payload_json,created_at) VALUES (?,?,?,?)",
        (ticket_id, event_type, json.dumps(payload, ensure_ascii=False), stamp),
    )


def suppress_delivery(root: Path, delivery_id: int, reason: str) -> None:
    path = ticket_db(root)
    if not path.exists():
        return
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,owner_session_key,owner_generation FROM cnx_assistant_delivery WHERE delivery_id=? AND status='pending'",
            (delivery_id,),
        ).fetchone()
        if row:
            if row[0]:
                _event(
                    db,
                    str(row[0]),
                    "assistant_delivery_suppressed",
                    {
                        "deliveryId": delivery_id,
                        "ownerSessionKey": row[1],
                        "ownerGeneration": int(row[2]),
                        "reason": reason,
                    },
                    now_iso(),
                )
            db.execute("DELETE FROM cnx_assistant_delivery WHERE delivery_id=? AND status='pending'", (delivery_id,))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _write_completion(workspace: Path, target: dict[str, Any], stamp: str) -> None:
    task_id = str(target.get("taskId") or "")
    revision = int(target.get("stateRevision") or 0)
    if not task_id:
        raise RuntimeError("workflow delivery target has no taskId")
    path = workspace / ".cogentnexus-openclaw" / "workflows" / task_id / "completion.json"
    if not path.is_file():
        raise RuntimeError(f"workflow completion file not found: {path}")
    notice = json.loads(path.read_text(encoding="utf-8"))
    if notice.get("deliveryStatus") == "delivered":
        return
    if notice.get("taskId") != task_id or int(notice.get("stateRevision") or 0) != revision:
        raise RuntimeError("workflow completion delivery target no longer matches durable state")
    notice["deliveryStatus"] = "delivered"
    notice["deliveredAt"] = stamp
    notice.pop("lastDeliveryError", None)
    notice.pop("scheduledAt", None)
    notice.pop("deliveryRunId", None)
    temporary = path.with_suffix(f".json.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(notice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def settle_delivery(
    root: Path,
    delivery_id: int,
    target: dict[str, Any],
    stamp: str,
    claim_token: str | None = None,
) -> None:
    path = ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,status,owner_session_key,owner_generation,claim_token FROM cnx_assistant_delivery WHERE delivery_id=?",
            (delivery_id,),
        ).fetchone()
        if not row or row[1] == "delivered":
            db.commit()
            return
        if claim_token is not None and row[4] != claim_token:
            db.commit()
            return
        authority = session_authority(db, str(row[2]))
        if authority != ("active", int(row[3])):
            db.rollback()
            suppress_delivery(root, delivery_id, "session authority changed before settlement")
            return
        ticket_id = row[0]
        kind = str(target.get("kind") or "notice")
        if kind == "workflow":
            db.commit()
            db.close()
            _write_completion(root.parent, target, stamp)
            db = sqlite3.connect(path, timeout=5)
            ensure_schema(db)
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT ticket_id,status,owner_session_key,owner_generation,claim_token FROM cnx_assistant_delivery WHERE delivery_id=?",
                (delivery_id,),
            ).fetchone()
            if not row or row[1] == "delivered":
                db.commit()
                return
            if claim_token is not None and row[4] != claim_token:
                db.commit()
                return
            authority = session_authority(db, str(row[2]))
            if authority != ("active", int(row[3])):
                db.rollback()
                suppress_delivery(root, delivery_id, "session authority changed during workflow settlement")
                return
        elif kind == "direct":
            direct_ticket = str(target.get("ticketId") or ticket_id or "")
            if not direct_ticket:
                raise RuntimeError("direct assistant delivery has no Ticket id")
            changed = db.execute(
                """UPDATE tickets
                   SET status='completed',delivery_confirmed_at=?,delivery_last_error=NULL,
                       failure_class=NULL,failure_message=NULL,updated_at=?
                   WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0
                         AND workflow_id IS NULL AND response_ready_at IS NOT NULL""",
                (stamp, stamp, direct_ticket),
            )
            if changed.rowcount != 1:
                current = db.execute("SELECT status FROM tickets WHERE ticket_id=?", (direct_ticket,)).fetchone()
                if not current or current[0] != "completed":
                    raise RuntimeError("direct Ticket no longer owns assistant delivery")
            if table_exists(db, "cnx_direct_recovery"):
                db.execute(
                    """UPDATE cnx_direct_recovery
                       SET state='done',active_run_id=NULL,next_attempt_at=NULL,last_error=NULL,updated_at=?
                       WHERE ticket_id=?""",
                    (stamp, direct_ticket),
                )
            _event(db, direct_ticket, "delivery_confirmed", {"source": "host-chat-inject"}, stamp)
            _event(db, direct_ticket, "completed", {"directRecovery": True, "deliveryMode": "host-chat-inject"}, stamp)
        elif kind == "ticket":
            outbox_id = int(target.get("outboxId") or 0)
            if outbox_id <= 0:
                raise RuntimeError("ticket delivery target has no outboxId")
            db.execute(
                """UPDATE ticket_outbox
                   SET delivery_status='delivered',delivered_at=?,last_delivery_error=NULL,
                       scheduled_at=NULL,delivery_run_id=NULL
                   WHERE outbox_id=? AND delivery_status='pending'""",
                (stamp, outbox_id),
            )
        elif kind != "notice":
            raise RuntimeError(f"unsupported assistant delivery target: {kind}")
        params: list[Any] = [stamp, stamp, delivery_id]
        claim_clause = ""
        if claim_token is not None:
            claim_clause = " AND claim_token=?"
            params.append(claim_token)
        db.execute(
            f"""UPDATE cnx_assistant_delivery
               SET status='delivered',last_error=NULL,updated_at=?,delivered_at=?,
                   claim_token=NULL,claim_expires_at=NULL
               WHERE delivery_id=? AND status='pending'{claim_clause}""",
            params,
        )
        db.commit()
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        raise
    finally:
        db.close()


def mark_failed(root: Path, delivery_id: int, error: str, claim_token: str | None = None) -> None:
    """Record transport failure and release the durable attempt lease.

    While a direct_result row is still pending, the expensive/side-effect-aware
    recovery path must not infer a brand-new answer merely because transport is
    unhealthy. Refresh response_ready_at on each active delivery attempt so the
    undelivered-response detector continues retrying this exact durable text
    instead of launching another hidden LLM run.
    """
    path = ticket_db(root)
    if not path.exists():
        return
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        stamp = now_iso()
        message = error[:2000]
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,kind,claim_token FROM cnx_assistant_delivery WHERE delivery_id=? AND status='pending'",
            (delivery_id,),
        ).fetchone()
        if not row or (claim_token is not None and row[2] != claim_token):
            db.commit()
            return
        params: list[Any] = [message, stamp, delivery_id]
        claim_clause = ""
        if claim_token is not None:
            claim_clause = " AND claim_token=?"
            params.append(claim_token)
        changed = db.execute(
            f"""UPDATE cnx_assistant_delivery
               SET attempt_count=attempt_count+1,last_error=?,updated_at=?,
                   claim_token=NULL,claim_expires_at=NULL
               WHERE delivery_id=? AND status='pending'{claim_clause}""",
            params,
        )
        if changed.rowcount == 1 and row[0] and str(row[1]) == "direct_result" and table_exists(db, "tickets"):
            db.execute(
                """UPDATE tickets
                   SET response_ready_at=?,delivery_last_error=?,updated_at=?
                   WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0
                         AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL""",
                (stamp, message, stamp, str(row[0])),
            )
            _event(
                db,
                str(row[0]),
                "assistant_delivery_retry",
                {"deliveryId": delivery_id, "error": message, "recoveryDeferred": True},
                stamp,
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def pending_deliveries(root: Path, limit: int = 200) -> list[dict[str, Any]]:
    path = ticket_db(root)
    if not path.exists():
        return []
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        ensure_schema(db)
        return [
            dict(row)
            for row in db.execute(
                """SELECT delivery_id,ticket_id,owner_session_key,owner_generation,kind,text,target_json,
                          idempotency_key,attempt_count,last_error,claim_token,claim_expires_at
                   FROM cnx_assistant_delivery
                   WHERE status='pending'
                   ORDER BY owner_session_key,delivery_id LIMIT ?""",
                (max(1, min(limit, 1000)),),
            ).fetchall()
        ]
    finally:
        db.close()


def claim_next_delivery(root: Path, excluded_sessions: set[str] | None = None) -> dict[str, Any] | None:
    """Atomically lease one due head-of-line delivery across all Host processes."""
    path = ticket_db(root)
    if not path.exists():
        return None
    excluded = sorted(excluded_sessions or set())
    now_dt = datetime.now(timezone.utc)
    stamp = now_dt.isoformat()
    cutoff = (now_dt - timedelta(seconds=DELIVERY_RETRY_AFTER_SECONDS)).isoformat()
    lease_until = (now_dt + timedelta(seconds=DELIVERY_LEASE_SECONDS)).isoformat()
    token = f"{os.getpid()}:{uuid.uuid4().hex}"
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        ensure_schema(db)
        db.execute("BEGIN IMMEDIATE")
        exclusion_sql = ""
        params: list[Any] = [stamp, cutoff]
        if excluded:
            placeholders = ",".join("?" for _ in excluded)
            exclusion_sql = f" AND d.owner_session_key NOT IN ({placeholders})"
            params.extend(excluded)
        row = db.execute(
            f"""SELECT d.delivery_id,d.ticket_id,d.owner_session_key,d.owner_generation,d.kind,d.text,
                       d.target_json,d.idempotency_key,d.attempt_count,d.last_error
                FROM cnx_assistant_delivery d
                WHERE d.status='pending'
                  AND (d.claim_token IS NULL OR d.claim_expires_at IS NULL OR d.claim_expires_at<=?)
                  AND (d.attempt_count=0 OR d.updated_at<=?)
                  AND NOT EXISTS (
                    SELECT 1 FROM cnx_assistant_delivery p
                    WHERE p.owner_session_key=d.owner_session_key
                      AND p.status='pending' AND p.delivery_id<d.delivery_id
                  )
                  {exclusion_sql}
                ORDER BY d.owner_session_key,d.delivery_id LIMIT 1""",
            params,
        ).fetchone()
        if row is None:
            db.commit()
            return None
        changed = db.execute(
            """UPDATE cnx_assistant_delivery
               SET claim_token=?,claim_expires_at=?,updated_at=?
               WHERE delivery_id=? AND status='pending'
                 AND (claim_token IS NULL OR claim_expires_at IS NULL OR claim_expires_at<=?)""",
            (token, lease_until, stamp, int(row["delivery_id"]), stamp),
        )
        if changed.rowcount != 1:
            db.rollback()
            return None
        claimed = dict(row)
        claimed["claim_token"] = token
        claimed["claim_expires_at"] = lease_until
        db.commit()
        return claimed
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def delivery_is_authoritative(root: Path, item: dict[str, Any]) -> bool:
    """Require both exact-session authority and a non-terminal Ticket before injection."""
    path = ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        authority = session_authority(db, str(item["owner_session_key"]))
        if authority != ("active", int(item["owner_generation"])):
            return False
        ticket_id = item.get("ticket_id")
        if not ticket_id:
            return True
        if not table_exists(db, "tickets"):
            return False
        row = db.execute("SELECT status FROM tickets WHERE ticket_id=?", (str(ticket_id),)).fetchone()
        return bool(row and str(row[0]) not in TERMINAL_TICKET_STATUSES)
    finally:
        db.close()


def flush_deliveries(
    root: Path,
    limit: int = 200,
    injector: Callable[[str, str, str], dict[str, Any]] = inject_assistant,
) -> dict[str, Any]:
    """Flush due deliveries with one durable lease per owner-session head item."""
    delivered: list[int] = []
    suppressed: list[int] = []
    failed: list[dict[str, Any]] = []
    blocked_sessions: set[str] = set()
    processed = 0

    while processed < max(1, min(limit, 1000)):
        item = claim_next_delivery(root, blocked_sessions)
        if item is None:
            break
        processed += 1
        delivery_id = int(item["delivery_id"])
        session_key = str(item["owner_session_key"])
        claim_token = str(item["claim_token"])
        if not delivery_is_authoritative(root, item):
            suppress_delivery(root, delivery_id, "session authority changed or Ticket became terminal before injection")
            suppressed.append(delivery_id)
            continue
        try:
            target = json.loads(item.get("target_json") or '{"kind":"notice"}')
            injector(session_key, item["text"], item["idempotency_key"])
            settle_delivery(root, delivery_id, target, now_iso(), claim_token)
            delivered.append(delivery_id)
        except Exception as error:
            mark_failed(root, delivery_id, str(error), claim_token)
            failed.append({"deliveryId": delivery_id, "sessionKey": session_key, "error": str(error)})
            # Preserve ordering only for this session; another session may continue.
            blocked_sessions.add(session_key)
    return {
        "delivered": delivered,
        "suppressed": suppressed,
        "failed": failed,
        "pending": len(pending_deliveries(root, 1000)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("action", choices=["flush", "status"])
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action == "flush":
        result = flush_deliveries(root, args.limit)
    else:
        result = {"pending": pending_deliveries(root, args.limit)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result.get("failed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
