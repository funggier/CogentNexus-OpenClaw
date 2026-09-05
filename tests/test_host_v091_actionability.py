from __future__ import annotations

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091_actionability", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)

SCHEMA = """
CREATE TABLE tickets(
 ticket_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, owner_session_key TEXT NOT NULL,
 status TEXT NOT NULL, workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT,
 prompt TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE cnx_sessions(
 session_key TEXT PRIMARY KEY, state TEXT NOT NULL, generation INTEGER NOT NULL,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE cnx_direct_recovery(
 ticket_id TEXT PRIMARY KEY, mode TEXT NOT NULL, state TEXT NOT NULL,
 attempt_count INTEGER NOT NULL DEFAULT 0, active_run_id TEXT, next_attempt_at TEXT,
 owner_generation INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE cnx_direct_model_call(
 ticket_id TEXT PRIMARY KEY, state TEXT NOT NULL
);
CREATE TABLE ticket_outbox(
 outbox_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL,
 delivery_status TEXT NOT NULL
);
CREATE TABLE cnx_assistant_delivery(
 delivery_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL,
 kind TEXT NOT NULL, status TEXT NOT NULL
);
CREATE TABLE cnx_context_maintenance(
 id INTEGER PRIMARY KEY AUTOINCREMENT, state TEXT NOT NULL
);
"""


class HostActionabilityTests(unittest.TestCase):
    NOW = datetime(2026, 9, 6, 18, 0, tzinfo=timezone.utc)
    OWNER = "agent:main:discord:channel:test"
    TICKET = "T-direct"

    def make_db(self, root: Path, *, session_state="active", session_age=5,
                session_generation=7, owner_generation=7, next_attempt=None,
                ticket_status="accepted", workflow_eligible=0, workflow_id=None,
                recovery_state="pending"):
        path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.executescript(SCHEMA)
        now = self.NOW
        stamp = now.isoformat()
        session_stamp = (now - timedelta(minutes=session_age)).isoformat()
        db.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?)", (
            self.TICKET, "run-1", self.OWNER, ticket_status, workflow_eligible,
            workflow_id, "prompt", stamp, stamp))
        db.execute("INSERT INTO cnx_sessions VALUES (?,?,?,?,?)", (
            self.OWNER, session_state, session_generation, session_stamp, session_stamp))
        db.execute("INSERT INTO cnx_direct_recovery VALUES (?,?,?,?,?,?,?,?,?)", (
            self.TICKET, "resume", recovery_state, 0, None, next_attempt,
            owner_generation, stamp, stamp))
        db.commit()
        db.close()
        return path

    def test_stale_direct_owner_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_age=16, next_attempt="2026-09-06T17:00:00+00:00")
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_fresh_exact_due_direct_owner_wakes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_age=5, next_attempt="2026-09-06T17:00:00+00:00")
            self.assertTrue(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_owner_generation_mismatch_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, owner_generation=6, next_attempt="2026-09-06T17:00:00+00:00")
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_future_direct_recovery_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, next_attempt="2026-09-06T19:00:00+00:00")
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_deleted_owner_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_state="deleted", next_attempt="2026-09-06T17:00:00+00:00")
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_deleting_owner_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_state="deleting", next_attempt="2026-09-06T17:00:00+00:00")
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_accepted_direct_ticket_alone_does_not_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
            path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(path); db.executescript(SCHEMA)
            stamp = self.NOW.isoformat()
            db.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?)", (self.TICKET, "run", self.OWNER, "accepted", 0, None, "p", stamp, stamp))
            db.commit(); db.close()
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_workflow_ticket_still_wakes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, ticket_status="waiting", workflow_eligible=1, workflow_id="wf-1")
            self.assertTrue(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_pending_transport_delivery_still_wakes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = self.make_db(root, next_attempt="2026-09-06T19:00:00+00:00")
            db = sqlite3.connect(path)
            db.execute("INSERT INTO ticket_outbox(ticket_id,delivery_status) VALUES (?, 'pending')", ("other",))
            db.commit(); db.close()
            self.assertTrue(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_active_model_call_blocks_direct_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = self.make_db(root, next_attempt="2026-09-06T17:00:00+00:00")
            db = sqlite3.connect(path); db.execute("INSERT INTO cnx_direct_model_call VALUES (?, 'active')", (self.TICKET,)); db.commit(); db.close()
            self.assertFalse(cnx.durable_work_hint(root, self.NOW.isoformat()))

    def test_supervisor_healthy_stale_direct_state_stays_idle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_age=16, next_attempt="2026-09-06T17:00:00+00:00")
            cnx.legacy.save_state(root, {
                "schemaVersion": 1, "mode": "managed", "desiredGateway": "running",
                "desiredProvider": "running", "generation": 1,
            })
            original = cnx.LEGACY_SUPERVISOR_TICK
            cnx.gateway_fast_probe = lambda: True
            cnx.ollama_fast_probe = lambda: True
            cnx.LEGACY_SUPERVISOR_TICK = lambda *_args, **_kwargs: self.fail("heavy path must stay asleep")
            try:
                result = cnx.supervisor_tick(root, True)
            finally:
                cnx.LEGACY_SUPERVISOR_TICK = original
            self.assertEqual(result["result"], "idle")
    def test_supervisor_healthy_deleting_direct_state_stays_idle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.make_db(root, session_state="deleting", next_attempt="2026-09-06T17:00:00+00:00")
            cnx.legacy.save_state(root, {
                "schemaVersion": 1, "mode": "managed", "desiredGateway": "running",
                "desiredProvider": "running", "generation": 1,
            })
            original = cnx.LEGACY_SUPERVISOR_TICK
            cnx.gateway_fast_probe = lambda: True
            cnx.ollama_fast_probe = lambda: True
            cnx.LEGACY_SUPERVISOR_TICK = lambda *_args, **_kwargs: self.fail("heavy path must stay asleep")
            try:
                result = cnx.supervisor_tick(root, True)
            finally:
                cnx.LEGACY_SUPERVISOR_TICK = original
            self.assertEqual(result["result"], "idle")


if __name__ == "__main__":
    unittest.main()
