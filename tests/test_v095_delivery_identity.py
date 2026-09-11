from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
spec = importlib.util.spec_from_file_location("cnx_host_delivery_v095", SCRIPTS / "host_delivery.py")
delivery = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(delivery)


class DeliveryWakeIdentityTests(unittest.TestCase):
    NOW = datetime(2026, 9, 12, 0, 0, tzinfo=timezone.utc)

    def _root(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / ".cogentnexus-openclaw"
        (root / "runtime").mkdir(parents=True, exist_ok=True)
        self.addCleanup(temp.cleanup)
        return root

    def _seed(self, root: Path, *, status: str = "accepted", kind: str = "notice", attempt_count: int = 0,
              updated_at: datetime | None = None, claim_expires_at: datetime | None = None) -> int:
        path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
        db = sqlite3.connect(path)
        db.executescript("""
          CREATE TABLE tickets(
            ticket_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            workflow_eligible INTEGER NOT NULL DEFAULT 0,
            workflow_id TEXT
          );
          CREATE TABLE cnx_sessions(
            session_key TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            generation INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          );
        """)
        delivery.ensure_schema(db)
        stamp = (updated_at or self.NOW).isoformat()
        lease = claim_expires_at.isoformat() if claim_expires_at else None
        db.execute("INSERT INTO tickets(ticket_id,status) VALUES ('T1',?)", (status,))
        db.execute("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES ('S1','active',2,?,?)", (stamp, stamp))
        cursor = db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 ticket_id,owner_session_key,owner_generation,kind,text,target_json,
                 idempotency_key,status,attempt_count,created_at,updated_at,claim_expires_at)
               VALUES ('T1','S1',2,?,'answer','{"kind":"notice"}','k1','pending',?,?,?,?)""",
            (kind, attempt_count, stamp, stamp, lease),
        )
        db.commit(); db.close()
        return int(cursor.lastrowid)

    def test_exact_due_delivery_returns_identity(self):
        root = self._root()
        delivery_id = self._seed(root)
        item = delivery.next_actionable_delivery(root, self.NOW)
        self.assertIsNotNone(item)
        self.assertEqual(item["delivery_id"], delivery_id)
        self.assertEqual(item["ticket_id"], "T1")
        self.assertEqual(item["owner_session_key"], "S1")
        self.assertEqual(item["owner_generation"], 2)
        self.assertIsNone(item["claim_token"])

    def test_held_lease_is_not_a_second_wake_source(self):
        root = self._root()
        self._seed(root, claim_expires_at=self.NOW + timedelta(seconds=30))
        self.assertIsNone(delivery.next_actionable_delivery(root, self.NOW))

    def test_old_retry_after_attempt_is_not_a_permanent_wake_source(self):
        root = self._root()
        self._seed(root, attempt_count=2, updated_at=self.NOW - timedelta(minutes=10))
        self.assertIsNone(delivery.next_actionable_delivery(root, self.NOW))

    def test_direct_result_remains_actionable_after_completed_ticket(self):
        root = self._root()
        delivery_id = self._seed(root, status="completed", kind="direct_result")
        item = delivery.next_actionable_delivery(root, self.NOW)
        self.assertIsNotNone(item)
        self.assertEqual(item["delivery_id"], delivery_id)

    def test_direct_result_does_not_bypass_cancelled_ticket(self):
        root = self._root()
        self._seed(root, status="cancelled", kind="direct_result")
        self.assertIsNone(delivery.next_actionable_delivery(root, self.NOW))


if __name__ == "__main__":
    unittest.main()
