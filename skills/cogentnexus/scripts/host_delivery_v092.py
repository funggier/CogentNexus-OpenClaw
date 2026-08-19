#!/usr/bin/env python3
"""CogentNexus v0.9.2 assistant-delivery transport entry.

Windows npm installs expose ``openclaw.cmd`` as a command shim. Python's
CreateProcess path is not a reliable execution boundary for that shim and can
fail with WinError 2 even while the same command works from PowerShell.

This entry keeps the v0.9.1 durable delivery/lease implementation, replaces
its Gateway RPC transport with a direct ``node.exe openclaw.mjs`` invocation,
and preserves ``tickets.response_ready_at`` as the immutable timestamp of the
first durable response. Delivery retry timing belongs to the delivery row's
``updated_at``/lease fields, not to the response-ready boundary.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
from pathlib import Path
from typing import Any

import host_delivery as base


def _openclaw_node_command() -> list[str]:
    node = shutil.which("node.exe" if os.name == "nt" else "node") or shutil.which("node")
    if not node:
        raise FileNotFoundError("Node executable not found on PATH")

    shim = base.openclaw_executable()
    shim_path = Path(shim).resolve()
    candidates = [
        shim_path.with_name("node_modules") / "openclaw" / "openclaw.mjs",
        Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "openclaw" / "openclaw.mjs",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return [node, str(candidate)]
    raise FileNotFoundError(
        "OpenClaw JavaScript CLI entry not found next to npm shim: "
        + ", ".join(str(path) for path in candidates)
    )


def gateway_rpc(method: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    command = [
        *_openclaw_node_command(),
        "gateway",
        "call",
        method,
        "--params",
        json.dumps(params or {}, ensure_ascii=False, separators=(",", ":")),
        "--json",
    ]
    result = base.run(command, timeout=timeout, check=True)
    return base._parse_json_stream(method, result)


def mark_failed(root: Path, delivery_id: int, error: str, claim_token: str | None = None) -> None:
    """Record a transport failure without moving the response-ready boundary.

    A pending durable ``direct_result`` is itself the regeneration fence. The
    original ``response_ready_at`` therefore remains immutable while retry
    cadence is represented by ``cnx_assistant_delivery.updated_at`` and its
    lease fields.
    """
    path = base.ticket_db(root)
    if not path.exists():
        return
    db = sqlite3.connect(path, timeout=5)
    try:
        base.ensure_schema(db)
        stamp = base.now_iso()
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
        if changed.rowcount == 1 and row[0] and str(row[1]) == "direct_result" and base.table_exists(db, "tickets"):
            db.execute(
                """UPDATE tickets
                   SET delivery_last_error=?,updated_at=?
                   WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0
                         AND response_ready_at IS NOT NULL AND delivery_confirmed_at IS NULL""",
                (message, stamp, str(row[0])),
            )
            base._event(
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


# Base functions resolve these module globals at execution time. Redirect every
# Gateway RPC and retry bookkeeping operation without duplicating the durable
# claim/settlement implementation.
base.gateway_rpc = gateway_rpc
base.mark_failed = mark_failed


if __name__ == "__main__":
    raise SystemExit(base.main())
