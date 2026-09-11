#!/usr/bin/env python3
"""Canonical read-only Supervisor wake classification for CogentNexus-OpenClaw v0.9.5."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

WakeAuthority = Literal["none", "ticket", "direct_recovery", "delivery", "provider_local", "session"]

DIRECT_RECOVERY_SESSION_LIVENESS_SECONDS = 15 * 60


@dataclass(frozen=True)
class WakeDecision:
    actionable: bool
    authority: WakeAuthority
    work_id: str | None
    reason: str


def _ticket_db(root: Path) -> Path:
    return root / "runtime" / "cogentnexus-openclaw.sqlite3"


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _table_exists(db: sqlite3.Connection, name: str) -> bool:
    return db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,)
    ).fetchone() is not None


def _columns(db: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in db.execute(f"PRAGMA table_info({table})")}


def _idle(reason: str = "idle/no-actionable-work") -> WakeDecision:
    return WakeDecision(False, "none", None, reason)


def _open_readonly(path: Path) -> sqlite3.Connection | None:
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=0.25)
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error:
        return None


def _find_pending_delivery(db: sqlite3.Connection, cutoff: str) -> WakeDecision | None:
    if not _table_exists(db, "cnx_assistant_delivery") or not _table_exists(db, "tickets"):
        return None

    delivery_columns = _columns(db, "cnx_assistant_delivery")
    required = {"delivery_id", "ticket_id", "status", "updated_at"}
    if not required.issubset(delivery_columns):
        # Older payloads may only persist a status column. Preserve that
        # compatibility signal without applying modern owner/session fences to
        # a schema that cannot express them.
        row = db.execute(
            "SELECT rowid AS row_id FROM cnx_assistant_delivery WHERE status='pending' LIMIT 1"
        ).fetchone()
        if row is not None:
            return WakeDecision(True, "delivery", str(row["row_id"]), "wake/delivery/legacy")
        return None

    if {"owner_session_key", "owner_generation"}.issubset(delivery_columns) and _table_exists(db, "cnx_sessions"):
        rows = db.execute(
            """SELECT d.delivery_id, d.ticket_id, d.owner_session_key, d.owner_generation,
                      d.updated_at, t.status AS ticket_status, s.state AS session_state,
                      s.generation AS session_generation
               FROM cnx_assistant_delivery d
               JOIN tickets t ON t.ticket_id=d.ticket_id
               JOIN cnx_sessions s ON s.session_key=d.owner_session_key
               WHERE d.status='pending'
                 AND d.updated_at>=?
                 AND t.status NOT IN ('completed','failed','cancelled')
                 AND s.state='active'
                 AND s.generation=d.owner_generation
               ORDER BY d.updated_at,d.delivery_id
               LIMIT 1""",
            (cutoff,),
        ).fetchone()
        if rows is not None:
            return WakeDecision(True, "delivery", str(rows["delivery_id"]), "wake/delivery")
        return None

    row = db.execute(
        "SELECT delivery_id,ticket_id FROM cnx_assistant_delivery WHERE status='pending' LIMIT 1"
    ).fetchone()
    if row is not None:
        return WakeDecision(True, "delivery", str(row["delivery_id"]), "wake/delivery/legacy")
    return None


def _find_direct_recovery(db: sqlite3.Connection, current: datetime, cutoff: str) -> WakeDecision | None:
    if not {_table_exists(db, "cnx_direct_recovery"), _table_exists(db, "tickets"), _table_exists(db, "cnx_sessions")} == {True}:
        return None
    rows = db.execute(
        """SELECT r.ticket_id, r.state, r.owner_generation, r.next_attempt_at,
                  s.state AS session_state, s.generation AS session_generation,
                  s.updated_at AS session_updated_at
           FROM cnx_direct_recovery r
           JOIN tickets t ON t.ticket_id=r.ticket_id
           JOIN cnx_sessions s ON s.session_key=t.owner_session_key
           WHERE r.state='pending'
             AND t.status='accepted'
             AND t.workflow_eligible=0
             AND t.workflow_id IS NULL
             AND s.state='active'
             AND s.generation=r.owner_generation
             AND s.updated_at>=?
           ORDER BY COALESCE(r.next_attempt_at,''),r.ticket_id
           LIMIT 1""",
        (cutoff,),
    ).fetchone()
    if rows is None:
        return None
    due_at = _parse_time(rows["next_attempt_at"])
    if due_at is not None and due_at > current:
        return None

    if _table_exists(db, "cnx_direct_model_call"):
        fenced = db.execute(
            "SELECT 1 FROM cnx_direct_model_call WHERE ticket_id=? AND state IN ('active','recovering') LIMIT 1",
            (rows["ticket_id"],),
        ).fetchone()
        if fenced is not None:
            return None
    return WakeDecision(True, "direct_recovery", str(rows["ticket_id"]), "wake/direct-recovery")


def _find_legacy_delivery_or_context(db: sqlite3.Connection) -> WakeDecision | None:
    if _table_exists(db, "ticket_outbox"):
        row = db.execute(
            "SELECT rowid AS row_id FROM ticket_outbox WHERE delivery_status='pending' LIMIT 1"
        ).fetchone()
        if row is not None:
            return WakeDecision(True, "delivery", str(row["row_id"]), "wake/delivery/outbox")

    if _table_exists(db, "cnx_context_maintenance"):
        row = db.execute(
            "SELECT rowid AS row_id FROM cnx_context_maintenance WHERE state IN ('pending','running','degraded') LIMIT 1"
        ).fetchone()
        if row is not None:
            return WakeDecision(True, "session", str(row["row_id"]), "wake/session/context-maintenance")

    if _table_exists(db, "cnx_direct_recovery"):
        cols = _columns(db, "cnx_direct_recovery")
        if cols == {"state"}:
            row = db.execute(
                "SELECT rowid AS row_id FROM cnx_direct_recovery WHERE state='awaiting_delivery' LIMIT 1"
            ).fetchone()
            if row is not None:
                return WakeDecision(True, "delivery", str(row["row_id"]), "wake/delivery/direct-legacy")
    return None


def _find_workflow_ticket(db: sqlite3.Connection) -> WakeDecision | None:
    if not _table_exists(db, "tickets"):
        return None
    cols = _columns(db, "tickets")
    if "ticket_id" not in cols or "status" not in cols:
        return None
    if {"workflow_eligible", "workflow_id"}.issubset(cols):
        row = db.execute(
            """SELECT ticket_id FROM tickets
               WHERE status NOT IN ('completed','failed','cancelled')
                 AND (workflow_eligible<>0 OR workflow_id IS NOT NULL)
               ORDER BY ticket_id LIMIT 1"""
        ).fetchone()
    else:
        row = db.execute(
            "SELECT rowid AS row_id FROM tickets WHERE status NOT IN ('completed','failed','cancelled') LIMIT 1"
        ).fetchone()
    if row is not None:
        work_id = str(row["ticket_id"]) if "ticket_id" in row.keys() else str(row["row_id"])
        return WakeDecision(True, "ticket", work_id, "wake/ticket")
    return None


def classify_wake(root: Path, now: datetime | None = None) -> WakeDecision:
    """Classify one exact wake authority using read-only durable evidence."""
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    cutoff = (current - timedelta(seconds=DIRECT_RECOVERY_SESSION_LIVENESS_SECONDS)).isoformat()
    path = _ticket_db(root)
    if not path.exists():
        return _idle()

    db = _open_readonly(path)
    if db is None:
        return WakeDecision(True, "ticket", None, "wake/schema-uncertain")
    try:
        if not _table_exists(db, "tickets"):
            return _idle()

        decision = _find_pending_delivery(db, cutoff)
        if decision is not None:
            return decision

        decision = _find_direct_recovery(db, current, cutoff)
        if decision is not None:
            return decision

        decision = _find_legacy_delivery_or_context(db)
        if decision is not None:
            return decision

        decision = _find_workflow_ticket(db)
        if decision is not None:
            return decision
        return _idle()
    except sqlite3.Error:
        return WakeDecision(True, "ticket", None, "wake/schema-uncertain")
    finally:
        db.close()
