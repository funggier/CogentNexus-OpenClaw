import importlib.util
import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "cogentnexus" / "scripts" / "host_delivery.py"
SPEC = importlib.util.spec_from_file_location("cnx_host_delivery_v090", MODULE_PATH)
assert SPEC and SPEC.loader
host_delivery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host_delivery)


class HostSessionDeliveryTests(unittest.TestCase):
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
        stamp = "2026-01-01T00:00:00Z"
        db.execute(
            "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES ('A','active',3,?,?)",
            (stamp, stamp),
        )
        db.execute(
            "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES ('B','active',7,?,?)",
            (stamp, stamp),
        )
        db.commit()
        db.close()
        self.db_path = path
        self.original_run = host_delivery.run
        self.original_openclaw = host_delivery.openclaw_executable

    def tearDown(self):
        host_delivery.run = self.original_run
        host_delivery.openclaw_executable = self.original_openclaw
        self.temp.cleanup()

    def queue(self, session_key: str, generation: int, key: str, text: str) -> None:
        db = sqlite3.connect(self.db_path)
        stamp = "2026-01-01T00:00:00Z"
        db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
                 attempt_count,created_at,updated_at)
               VALUES (?,?, 'notice', ?, '{"kind":"notice"}', ?, 'pending', 0, ?, ?)""",
            (session_key, generation, text, key, stamp, stamp),
        )
        db.commit()
        db.close()

    def queue_direct(self, ticket_id: str = "CNXT-direct") -> int:
        db = sqlite3.connect(self.db_path)
        stamp = "2026-01-01T00:00:00Z"
        db.execute(
            """INSERT INTO tickets(
                 ticket_id,status,workflow_eligible,workflow_id,response_ready_at,
                 delivery_confirmed_at,delivery_last_error,failure_class,failure_message,updated_at)
               VALUES (?,'accepted',0,NULL,?,NULL,NULL,'interrupted','old delivery timeout',?)""",
            (ticket_id, stamp, stamp),
        )
        db.execute(
            """INSERT INTO cnx_direct_recovery(ticket_id,state,active_run_id,next_attempt_at,last_error,updated_at)
               VALUES (?,'awaiting_delivery',NULL,NULL,NULL,?)""",
            (ticket_id, stamp),
        )
        cursor = db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
                 attempt_count,last_error,created_at,updated_at)
               VALUES (?,'A',3,'direct_result','ready answer',?,?,'pending',0,NULL,?,?)""",
            (
                ticket_id,
                json.dumps({"kind": "direct", "ticketId": ticket_id, "runId": "recovery-run"}),
                f"direct:{ticket_id}",
                stamp,
                stamp,
            ),
        )
        delivery_id = int(cursor.lastrowid)
        db.commit()
        db.close()
        return delivery_id

    def test_generation_mismatch_is_suppressed_without_injection(self):
        self.queue("A", 2, "stale-a", "stale")
        calls = []
        result = host_delivery.flush_deliveries(
            self.root,
            injector=lambda *args: calls.append(args) or {"ok": True},
        )
        self.assertEqual(calls, [])
        self.assertEqual(len(result["suppressed"]), 1)
        db = sqlite3.connect(self.db_path)
        self.assertEqual(db.execute("SELECT count(*) FROM cnx_assistant_delivery WHERE status='pending'").fetchone()[0], 0)
        db.close()

    def test_terminal_ticket_delivery_is_suppressed_before_injection(self):
        delivery_id = self.queue_direct()
        db = sqlite3.connect(self.db_path)
        db.execute("UPDATE tickets SET status='cancelled' WHERE ticket_id='CNXT-direct'")
        db.execute("UPDATE cnx_direct_recovery SET state='cancelled' WHERE ticket_id='CNXT-direct'")
        db.commit()
        db.close()

        calls = []
        result = host_delivery.flush_deliveries(
            self.root,
            injector=lambda *args: calls.append(args) or {"ok": True},
        )

        self.assertEqual(calls, [])
        self.assertEqual(result["suppressed"], [delivery_id])
        self.assertEqual(result["pending"], 0)
        db = sqlite3.connect(self.db_path)
        event = db.execute(
            "SELECT payload_json FROM ticket_events WHERE ticket_id='CNXT-direct' AND event_type='assistant_delivery_suppressed' ORDER BY event_id DESC LIMIT 1"
        ).fetchone()
        db.close()
        self.assertIn("Ticket became terminal", json.loads(event[0])["reason"])

    def test_failure_in_one_session_does_not_block_another_session(self):
        self.queue("A", 3, "a-1", "A first")
        self.queue("A", 3, "a-2", "A second")
        self.queue("B", 7, "b-1", "B first")
        seen = []

        def inject(session_key, text, _key):
            seen.append((session_key, text))
            if session_key == "A":
                raise RuntimeError("A unavailable")
            return {"ok": True}

        result = host_delivery.flush_deliveries(self.root, injector=inject)
        self.assertEqual(seen[0], ("A", "A first"))
        self.assertIn(("B", "B first"), seen)
        self.assertNotIn(("A", "A second"), seen)
        self.assertEqual(len(result["delivered"]), 1)
        self.assertEqual(len(result["failed"]), 1)
        self.assertEqual(result["failed"][0]["sessionKey"], "A")

        db = sqlite3.connect(self.db_path)
        status = dict(db.execute("SELECT idempotency_key,status FROM cnx_assistant_delivery"))
        self.assertEqual(status["a-1"], "pending")
        self.assertEqual(status["a-2"], "pending")
        self.assertEqual(status["b-1"], "delivered")
        db.close()

    def test_deleted_session_is_suppressed_while_other_session_delivers(self):
        self.queue("A", 3, "a-delete", "A stale")
        self.queue("B", 7, "b-live", "B live")
        db = sqlite3.connect(self.db_path)
        db.execute("UPDATE cnx_sessions SET state='deleted',generation=4 WHERE session_key='A'")
        db.commit()
        db.close()
        seen = []
        result = host_delivery.flush_deliveries(
            self.root,
            injector=lambda session_key, text, key: seen.append((session_key, text, key)) or {"ok": True},
        )
        self.assertEqual([item[0] for item in seen], ["B"])
        self.assertEqual(len(result["suppressed"]), 1)
        self.assertEqual(len(result["delivered"]), 1)

    def test_gateway_rpc_missing_streams_fails_closed_without_attribute_error(self):
        host_delivery.openclaw_executable = lambda: "openclaw.cmd"
        host_delivery.run = lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, stdout=None, stderr=None
        )
        with self.assertRaisesRegex(RuntimeError, r"chat\.history returned no JSON output"):
            host_delivery.gateway_rpc("chat.history", {"sessionKey": "A"})

    def test_gateway_rpc_accepts_json_from_secondary_captured_stream(self):
        host_delivery.openclaw_executable = lambda: "openclaw.cmd"
        host_delivery.run = lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, stdout=None, stderr='{"ok":true,"messageId":"m1"}'
        )
        self.assertEqual(
            host_delivery.gateway_rpc("chat.inject", {"sessionKey": "A", "message": "hello"}),
            {"ok": True, "messageId": "m1"},
        )

    def test_direct_delivery_success_completes_ticket_and_recovery(self):
        delivery_id = self.queue_direct()
        result = host_delivery.flush_deliveries(
            self.root,
            injector=lambda *_args: {"ok": True},
        )
        self.assertEqual(result["delivered"], [delivery_id])
        self.assertEqual(result["pending"], 0)

        db = sqlite3.connect(self.db_path)
        self.assertEqual(
            db.execute("SELECT status,delivery_confirmed_at,failure_class,failure_message FROM tickets WHERE ticket_id='CNXT-direct'").fetchone()[0],
            "completed",
        )
        self.assertEqual(
            db.execute("SELECT state FROM cnx_direct_recovery WHERE ticket_id='CNXT-direct'").fetchone()[0],
            "done",
        )
        self.assertEqual(
            db.execute("SELECT status FROM cnx_assistant_delivery WHERE delivery_id=?", (delivery_id,)).fetchone()[0],
            "delivered",
        )
        db.close()

    def test_direct_transport_failure_refreshes_delivery_deadline_instead_of_regenerating(self):
        delivery_id = self.queue_direct()
        db = sqlite3.connect(self.db_path)
        before = db.execute("SELECT response_ready_at FROM tickets WHERE ticket_id='CNXT-direct'").fetchone()[0]
        db.close()

        host_delivery.mark_failed(self.root, delivery_id, "transport unavailable")

        db = sqlite3.connect(self.db_path)
        response_ready_at, delivery_error = db.execute(
            "SELECT response_ready_at,delivery_last_error FROM tickets WHERE ticket_id='CNXT-direct'"
        ).fetchone()
        attempts, last_error, status = db.execute(
            "SELECT attempt_count,last_error,status FROM cnx_assistant_delivery WHERE delivery_id=?",
            (delivery_id,),
        ).fetchone()
        event = db.execute(
            "SELECT payload_json FROM ticket_events WHERE ticket_id='CNXT-direct' AND event_type='assistant_delivery_retry' ORDER BY event_id DESC LIMIT 1"
        ).fetchone()
        db.close()

        self.assertNotEqual(response_ready_at, before)
        self.assertEqual(delivery_error, "transport unavailable")
        self.assertEqual((attempts, last_error, status), (1, "transport unavailable", "pending"))
        self.assertTrue(json.loads(event[0])["recoveryDeferred"])


if __name__ == "__main__":
    unittest.main()
