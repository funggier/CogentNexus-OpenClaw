from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091_delivery_fence", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


SCHEMA = """
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
CREATE TABLE ticket_outbox(
  outbox_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_id TEXT NOT NULL UNIQUE,
  owner_session_key TEXT NOT NULL,
  terminal_status TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  delivery_status TEXT NOT NULL DEFAULT 'pending',
  delivery_attempts INTEGER NOT NULL DEFAULT 0,
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


class HostV091DeliveryFenceTests(unittest.TestCase):
    def seed(self, root: Path) -> Path:
        path = root / "runtime" / "cogentnexus.sqlite3"
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.executescript(SCHEMA)
        created = "2026-08-18T10:00:00Z"
        ready = "2026-08-18T10:10:00Z"
        rows = [
            ("T-accepted-unverifiable", "run-a", "agent:main:dashboard:a", "accepted", 0, None, ready),
            ("T-waiting-unverifiable", "run-b", "agent:main:dashboard:b", "waiting", 1, None, ready),
            ("T-durable", "run-c", "agent:main:dashboard:c", "accepted", 0, None, ready),
            ("T-never-ready", "run-d", "agent:main:dashboard:d", "accepted", 0, None, None),
        ]
        db.executemany(
            "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,created_at,updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            [(a, b, c, d, e, f, g, created, created) for a, b, c, d, e, f, g in rows],
        )
        db.execute(
            "INSERT INTO cnx_assistant_delivery(ticket_id,kind,status) VALUES ('T-durable','direct_result','pending')"
        )
        db.execute(
            "INSERT INTO cnx_direct_recovery(ticket_id,state,active_run_id,next_attempt_at,last_error,updated_at) "
            "VALUES ('T-waiting-unverifiable','pending',NULL,'2026-08-18T10:20:00Z',NULL,?)",
            (created,),
        )
        db.commit()
        db.close()
        return path

    def test_response_ready_without_durable_payload_fails_before_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            path = self.seed(root)
            cutoff = "2026-08-18T11:00:00Z"

            fence = cnx.reconcile_direct_delivery_before_recovery(root, cutoff)
            recovered = cnx.promote_interrupted_direct_v091(root, cutoff, "test interruption")

            self.assertEqual(
                set(fence["unverifiableFailed"]),
                {"T-accepted-unverifiable", "T-waiting-unverifiable"},
            )
            self.assertEqual(fence["durableDeliveryHeld"], ["T-durable"])
            self.assertEqual(recovered, ["T-never-ready"])

            db = sqlite3.connect(path)
            db.row_factory = sqlite3.Row
            try:
                failed = {
                    row["ticket_id"]: dict(row)
                    for row in db.execute(
                        "SELECT ticket_id,status,workflow_eligible,failure_class,failure_message FROM tickets "
                        "WHERE ticket_id IN ('T-accepted-unverifiable','T-waiting-unverifiable')"
                    )
                }
                for ticket_id in ("T-accepted-unverifiable", "T-waiting-unverifiable"):
                    self.assertEqual(failed[ticket_id]["status"], "failed")
                    self.assertEqual(failed[ticket_id]["workflow_eligible"], 0)
                    self.assertEqual(failed[ticket_id]["failure_class"], "permanent")
                    self.assertIn("refusing regeneration", failed[ticket_id]["failure_message"])

                durable = db.execute(
                    "SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id='T-durable'"
                ).fetchone()
                self.assertEqual(dict(durable), {"status": "accepted", "workflow_eligible": 0, "failure_class": None})

                fresh = db.execute(
                    "SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id='T-never-ready'"
                ).fetchone()
                self.assertEqual(
                    dict(fresh),
                    {"status": "waiting", "workflow_eligible": 1, "failure_class": "interrupted"},
                )

                outbox = db.execute(
                    "SELECT ticket_id,terminal_status,delivery_status,payload_json FROM ticket_outbox ORDER BY ticket_id"
                ).fetchall()
                self.assertEqual([row["ticket_id"] for row in outbox], ["T-accepted-unverifiable", "T-waiting-unverifiable"])
                self.assertTrue(all(row["terminal_status"] == "failed" for row in outbox))
                self.assertTrue(all(row["delivery_status"] == "pending" for row in outbox))
                self.assertTrue(all(json.loads(row["payload_json"])["classification"] == "permanent" for row in outbox))

                recovery = db.execute(
                    "SELECT state,active_run_id,next_attempt_at,last_error FROM cnx_direct_recovery "
                    "WHERE ticket_id='T-waiting-unverifiable'"
                ).fetchone()
                self.assertEqual(recovery["state"], "cancelled")
                self.assertIsNone(recovery["active_run_id"])
                self.assertIsNone(recovery["next_attempt_at"])
                self.assertIn("refusing regeneration", recovery["last_error"])
            finally:
                db.close()


if __name__ == "__main__":
    unittest.main()
