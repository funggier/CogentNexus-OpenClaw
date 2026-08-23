from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_authority_v091 as authority  # noqa: E402


TICKET = "CNXT-durable-authority"


class HostV091AuthorityDeliveryHoldTests(unittest.TestCase):
    def test_durable_result_suppresses_pending_inference_recovery(self):
        with tempfile.TemporaryDirectory(prefix="cnx-durable-hold-") as tmp:
            root = Path(tmp) / ".cogent"
            path = root / "runtime" / "cogentnexus.sqlite3"
            path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(path)
            db.executescript(
                """
                CREATE TABLE tickets(
                  ticket_id TEXT PRIMARY KEY,
                  run_id TEXT NOT NULL,
                  owner_session_key TEXT NOT NULL,
                  status TEXT NOT NULL,
                  workflow_eligible INTEGER NOT NULL DEFAULT 0,
                  workflow_id TEXT,
                  worker_id TEXT,
                  lease_token TEXT,
                  lease_expires_at TEXT,
                  heartbeat_at TEXT,
                  failure_class TEXT,
                  failure_message TEXT,
                  result_json TEXT,
                  response_ready_at TEXT,
                  delivery_confirmed_at TEXT,
                  delivery_last_error TEXT,
                  created_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                );
                CREATE TABLE ticket_events(
                  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id TEXT NOT NULL,
                  event_type TEXT NOT NULL,
                  payload_json TEXT NOT NULL,
                  created_at TEXT NOT NULL
                );
                CREATE TABLE cnx_assistant_delivery(
                  delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id TEXT NOT NULL,
                  kind TEXT NOT NULL,
                  status TEXT NOT NULL
                );
                CREATE TABLE cnx_direct_recovery(
                  ticket_id TEXT PRIMARY KEY,
                  state TEXT NOT NULL,
                  active_run_id TEXT,
                  next_attempt_at TEXT,
                  last_error TEXT,
                  updated_at TEXT NOT NULL
                );
                """
            )
            created = "2026-08-18T13:00:00Z"
            ready = "2026-08-18T13:10:00Z"
            db.execute(
                """INSERT INTO tickets(
                     ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,
                     failure_class,failure_message,response_ready_at,created_at,updated_at
                   ) VALUES (?,?,?,'waiting',1,NULL,'interrupted','legacy promotion',?,?,?)""",
                (TICKET, "run-durable", "agent:main:dashboard:durable", ready, created, created),
            )
            db.execute(
                "INSERT INTO cnx_assistant_delivery(ticket_id,kind,status) VALUES (?,'direct_result','pending')",
                (TICKET,),
            )
            db.execute(
                """INSERT INTO cnx_direct_recovery(ticket_id,state,active_run_id,next_attempt_at,last_error,updated_at)
                   VALUES (?,'pending',NULL,'2026-08-18T13:20:00Z','legacy retry',?)""",
                (TICKET, created),
            )
            db.commit()
            db.close()

            result = authority.reconcile_direct_delivery_authority(root, "2026-08-18T14:00:00Z")
            self.assertEqual(result["durableDeliveryHeld"], [TICKET])

            db = sqlite3.connect(path)
            try:
                self.assertEqual(
                    db.execute(
                        "SELECT status,workflow_eligible,failure_class,failure_message FROM tickets WHERE ticket_id=?",
                        (TICKET,),
                    ).fetchone(),
                    ("accepted", 0, None, None),
                )
                recovery = db.execute(
                    "SELECT state,active_run_id,next_attempt_at,last_error FROM cnx_direct_recovery WHERE ticket_id=?",
                    (TICKET,),
                ).fetchone()
                self.assertEqual(recovery[0], "awaiting_delivery")
                self.assertIsNone(recovery[1])
                self.assertIsNone(recovery[2])
                self.assertIn("inference recovery suppressed", recovery[3])
                events = [
                    row[0]
                    for row in db.execute(
                        "SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id",
                        (TICKET,),
                    )
                ]
                self.assertIn("host_restored_durable_delivery", events)
                self.assertIn("host_direct_recovery_suppressed_by_durable_delivery", events)
            finally:
                db.close()


if __name__ == "__main__":
    unittest.main()
