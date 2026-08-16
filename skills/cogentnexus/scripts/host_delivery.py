#!/usr/bin/env python3
"""Host-owned, session-isolated assistant delivery for CogentNexus.

Synthetic workers never write control prompts into an owner transcript. They
queue user-facing assistant text here, and this bridge injects that text into
the exact owner session through OpenClaw's official ``chat.inject`` Gateway
method. Session generation/state checks make late delivery after Stop/Delete
non-authoritative.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogent"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def run(cmd: list[str], timeout: int = 60, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
    )
    if check and result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f"command failed: {cmd}").strip())
    return result


def openclaw_executable() -> str:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


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
    value = result.stdout.strip()
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"OpenClaw Gateway RPC {method} returned invalid JSON: {value[:500]}") from error


def ticket_db(root: Path) -> Path:
    return root / "runtime" / "cogentnexus.sqlite3"


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
          delivered_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_cnx_assistant_delivery_pending
          ON cnx_assistant_delivery(status,owner_session_key,delivery_id);
        """
    )
    if not column_exists(db, "cnx_assistant_delivery", "owner_generation"):
        db.execute("ALTER TABLE cnx_assistant_delivery ADD COLUMN owner_generation INTEGER NOT NULL DEFAULT 0")


def delivery_marker(idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()[:32]
    return f"<!-- cogentnexus-delivery:{digest} -->"


def history_contains(session_key: str, marker: str) -> bool:
    history = gateway_rpc(
        "chat.history",
        {"sessionKey": session_key, "limit": 100, "maxChars": 500000},
        timeout=30,
    )
    return marker in json.dumps(history, ensure_ascii=False, separators=(",", ":"))


def inject_assistant(session_key: str, text: str, idempotency_key: str) -> dict[str, Any]:
    marker = delivery_marker(idempotency_key)
    if history_contains(session_key, marker):
        return {"ok": True, "deduplicated": True}
    payload = gateway_rpc(
        "chat.inject",
        {"sessionKey": session_key, "message": f"{text.rstrip()}\n\n{marker}"},
        timeout=30,
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
    path = workspace / ".cogent" / "workflows" / task_id / "completion.json"
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


def settle_delivery(root: Path, delivery_id: int, target: dict[str, Any], stamp: str) -> None:
    path = ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT ticket_id,status,owner_session_key,owner_generation FROM cnx_assistant_delivery WHERE delivery_id=?",
            (delivery_id,),
        ).fetchone()
        if not row or row[1] == "delivered":
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
                "SELECT ticket_id,status,owner_session_key,owner_generation FROM cnx_assistant_delivery WHERE delivery_id=?",
                (delivery_id,),
            ).fetchone()
            if not row or row[1] == "delivered":
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
        db.execute(
            """UPDATE cnx_assistant_delivery
               SET status='delivered',last_error=NULL,updated_at=?,delivered_at=?
               WHERE delivery_id=? AND status='pending'""",
            (stamp, stamp, delivery_id),
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


def mark_failed(root: Path, delivery_id: int, error: str) -> None:
    path = ticket_db(root)
    if not path.exists():
        return
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        stamp = now_iso()
        db.execute(
            """UPDATE cnx_assistant_delivery
               SET attempt_count=attempt_count+1,last_error=?,updated_at=?
               WHERE delivery_id=? AND status='pending'""",
            (error[:2000], stamp, delivery_id),
        )
        db.commit()
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
                          idempotency_key,attempt_count,last_error
                   FROM cnx_assistant_delivery
                   WHERE status='pending'
                   ORDER BY owner_session_key,delivery_id LIMIT ?""",
                (max(1, min(limit, 1000)),),
            ).fetchall()
        ]
    finally:
        db.close()


def delivery_is_authoritative(root: Path, item: dict[str, Any]) -> bool:
    path = ticket_db(root)
    db = sqlite3.connect(path, timeout=5)
    try:
        ensure_schema(db)
        authority = session_authority(db, str(item["owner_session_key"]))
        return authority == ("active", int(item["owner_generation"]))
    finally:
        db.close()


def flush_deliveries(
    root: Path,
    limit: int = 200,
    injector: Callable[[str, str, str], dict[str, Any]] = inject_assistant,
) -> dict[str, Any]:
    """Flush independently per session while preserving order inside each session."""
    delivered: list[int] = []
    suppressed: list[int] = []
    failed: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in pending_deliveries(root, limit):
        grouped[str(item["owner_session_key"])].append(item)

    for session_key in sorted(grouped):
        for item in grouped[session_key]:
            delivery_id = int(item["delivery_id"])
            if not delivery_is_authoritative(root, item):
                suppress_delivery(root, delivery_id, "session deleted or generation superseded")
                suppressed.append(delivery_id)
                continue
            try:
                target = json.loads(item.get("target_json") or '{"kind":"notice"}')
                injector(session_key, item["text"], item["idempotency_key"])
                settle_delivery(root, delivery_id, target, now_iso())
                delivered.append(delivery_id)
            except Exception as error:
                mark_failed(root, delivery_id, str(error))
                failed.append({"deliveryId": delivery_id, "sessionKey": session_key, "error": str(error)})
                # Preserve ordering only for this session; another session must not be blocked.
                break
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
