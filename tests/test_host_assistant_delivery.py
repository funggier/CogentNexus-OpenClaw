import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "cogentnexus" / "scripts" / "host_delivery.py"
SPEC = importlib.util.spec_from_file_location("cnx_host_delivery", MODULE_PATH)
assert SPEC and SPEC.loader
host_delivery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host_delivery)


class HostAssistantDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        self.root = self.workspace / ".cogent"
        path = self.root / "runtime" / "cogentnexus.sqlite3"
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.executescript(
            """
            CREATE TABLE tickets(
              ticket_id TEXT PRIMARY KEY,
              status TEXT NOT NULL,
              workflow_eligible INTEGER NOT NULL DEFAULT 0,
              workflow_id TEXT,
              response_ready_at TEXT,
              delivery_confirmed_at TEXT,
              delivery_last_error TEXT,
              failure_class TEXT,
              failure_message TEXT,
              updated_at TEXT
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
              delivery_status TEXT NOT NULL DEFAULT 'pending',
              delivered_at TEXT,
              last_delivery_error TEXT,
              scheduled_at TEXT,
              delivery_run_id TEXT
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
        host_delivery.ensure_schema(db)
        db.commit()
        db.close()
        self.db_path = path

    def tearDown(self):
        self.temp.cleanup()

    def test_direct_delivery_completes_only_after_assistant_injection(self):
        db = sqlite3.connect(self.db_path)
        db.execute(
            "INSERT INTO tickets(ticket_id,status,workflow_eligible,response_ready_at,updated_at) VALUES ('T1','accepted',0,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')"
        )
        db.execute(
            "INSERT INTO cnx_direct_recovery(ticket_id,state,updated_at) VALUES ('T1','awaiting_delivery','2026-01-01T00:00:00Z')"
        )
        db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 ticket_id,owner_session_key,kind,text,target_json,idempotency_key,status,
                 attempt_count,created_at,updated_at)
               VALUES ('T1','agent:main:dashboard:test','direct_result','hello',?,
                 'cnx-direct-result:T1','pending',0,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')""",
            (json.dumps({"kind": "direct", "ticketId": "T1", "runId": "R1"}),),
        )
        db.commit()
        db.close()

        seen = []

        def inject(session_key, text, idempotency_key):
            seen.append((session_key, text, idempotency_key))
            return {"ok": True}

        result = host_delivery.flush_deliveries(self.root, injector=inject)
        self.assertEqual(result["failed"], [])
        self.assertEqual(len(result["delivered"]), 1)
        self.assertEqual(seen[0][0], "agent:main:dashboard:test")
        self.assertEqual(seen[0][1], "hello")

        db = sqlite3.connect(self.db_path)
        self.assertEqual(
            db.execute("SELECT status,workflow_eligible FROM tickets WHERE ticket_id='T1'").fetchone(),
            ("completed", 0),
        )
        self.assertEqual(
            db.execute("SELECT state FROM cnx_direct_recovery WHERE ticket_id='T1'").fetchone(),
            ("done",),
        )
        self.assertEqual(
            db.execute("SELECT status FROM cnx_assistant_delivery WHERE ticket_id='T1'").fetchone(),
            ("delivered",),
        )
        events = [row[0] for row in db.execute("SELECT event_type FROM ticket_events WHERE ticket_id='T1' ORDER BY event_id")]
        self.assertIn("delivery_confirmed", events)
        self.assertIn("completed", events)
        db.close()

    def test_failed_injection_remains_pending_with_error(self):
        db = sqlite3.connect(self.db_path)
        db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 owner_session_key,kind,text,target_json,idempotency_key,status,
                 attempt_count,created_at,updated_at)
               VALUES ('agent:main:dashboard:test','recovery_status','recovering','{"kind":"notice"}',
                 'notice:1','pending',0,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')"""
        )
        db.commit()
        db.close()

        def fail(_session_key, _text, _idempotency_key):
            raise RuntimeError("gateway unavailable")

        result = host_delivery.flush_deliveries(self.root, injector=fail)
        self.assertEqual(len(result["failed"]), 1)
        db = sqlite3.connect(self.db_path)
        row = db.execute(
            "SELECT status,attempt_count,last_error FROM cnx_assistant_delivery WHERE idempotency_key='notice:1'"
        ).fetchone()
        self.assertEqual(row[0], "pending")
        self.assertEqual(row[1], 1)
        self.assertIn("gateway unavailable", row[2])
        db.close()

    def test_ticket_outbox_is_settled_after_assistant_injection(self):
        db = sqlite3.connect(self.db_path)
        db.execute("INSERT INTO ticket_outbox(delivery_status,scheduled_at,delivery_run_id) VALUES ('pending','x','run')")
        outbox_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 owner_session_key,kind,text,target_json,idempotency_key,status,
                 attempt_count,created_at,updated_at)
               VALUES ('agent:main:dashboard:test','compatibility_result','done',?,
                 'ticket-delivery','pending',0,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')""",
            (json.dumps({"kind": "ticket", "outboxId": outbox_id}),),
        )
        db.commit()
        db.close()

        result = host_delivery.flush_deliveries(
            self.root,
            injector=lambda *_args: {"ok": True},
        )
        self.assertEqual(result["failed"], [])
        db = sqlite3.connect(self.db_path)
        self.assertEqual(
            db.execute("SELECT delivery_status FROM ticket_outbox WHERE outbox_id=?", (outbox_id,)).fetchone(),
            ("delivered",),
        )
        db.close()


if __name__ == "__main__":
    unittest.main()
