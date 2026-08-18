from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "cogentnexus" / "scripts" / "host_delivery.py"
SPEC = importlib.util.spec_from_file_location("cnx_host_delivery_dedupe", MODULE_PATH)
assert SPEC and SPEC.loader
host_delivery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host_delivery)


class HostDeliveryDedupeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cnx-host-delivery-dedupe-")
        self.workspace = Path(self.temp.name)
        self.root = self.workspace / ".cogent"
        self.path = self.root / "runtime" / "cogentnexus.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.path)
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
        stamp = "2026-08-18T13:00:00Z"
        db.execute(
            "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES ('A','active',3,?,?)",
            (stamp, stamp),
        )
        db.execute(
            """INSERT INTO tickets(
                 ticket_id,status,workflow_eligible,workflow_id,response_ready_at,
                 delivery_confirmed_at,delivery_last_error,failure_class,failure_message,updated_at)
               VALUES ('CNXT-dedupe','accepted',0,NULL,?,NULL,NULL,'interrupted','retry delivery',?)""",
            (stamp, stamp),
        )
        db.execute(
            """INSERT INTO cnx_direct_recovery(ticket_id,state,active_run_id,next_attempt_at,last_error,updated_at)
               VALUES ('CNXT-dedupe','awaiting_delivery',NULL,NULL,NULL,?)""",
            (stamp,),
        )
        self.idempotency_key = "cnx-direct-result:CNXT-dedupe:g3"
        cursor = db.execute(
            """INSERT INTO cnx_assistant_delivery(
                 ticket_id,owner_session_key,owner_generation,kind,text,target_json,idempotency_key,status,
                 attempt_count,last_error,created_at,updated_at)
               VALUES ('CNXT-dedupe','A',3,'direct_result','exact durable answer',?,?,'pending',0,NULL,?,?)""",
            (
                json.dumps({"kind": "direct", "ticketId": "CNXT-dedupe", "runId": "recovery-run"}),
                self.idempotency_key,
                stamp,
                stamp,
            ),
        )
        self.delivery_id = int(cursor.lastrowid)
        db.commit()
        db.close()
        self.original_gateway_rpc = host_delivery.gateway_rpc

    def tearDown(self):
        host_delivery.gateway_rpc = self.original_gateway_rpc
        self.temp.cleanup()

    def test_existing_history_marker_deduplicates_then_settles_without_second_inject(self):
        marker = host_delivery.delivery_marker(self.idempotency_key)
        calls: list[str] = []

        def fake_gateway_rpc(method, params=None, timeout=30):
            calls.append(method)
            if method == "chat.history":
                # Simulate: chat.inject succeeded before a crash, but the DB
                # transaction that settles cnx_assistant_delivery did not run.
                return {"messages": [{"role": "assistant", "content": f"exact durable answer\n\n{marker}"}]}
            if method == "chat.inject":
                raise AssertionError("duplicate chat.inject must not occur")
            raise AssertionError(f"unexpected RPC: {method}")

        host_delivery.gateway_rpc = fake_gateway_rpc
        result = host_delivery.flush_deliveries(self.root)

        self.assertEqual(calls, ["chat.history"])
        self.assertEqual(result["delivered"], [self.delivery_id])
        self.assertEqual(result["failed"], [])
        self.assertEqual(result["pending"], 0)

        db = sqlite3.connect(self.path)
        try:
            ticket = db.execute(
                "SELECT status,delivery_confirmed_at,failure_class,failure_message FROM tickets WHERE ticket_id='CNXT-dedupe'"
            ).fetchone()
            self.assertEqual(ticket[0], "completed")
            self.assertIsNotNone(ticket[1])
            self.assertIsNone(ticket[2])
            self.assertIsNone(ticket[3])
            self.assertEqual(
                db.execute("SELECT state FROM cnx_direct_recovery WHERE ticket_id='CNXT-dedupe'").fetchone()[0],
                "done",
            )
            self.assertEqual(
                db.execute("SELECT status FROM cnx_assistant_delivery WHERE delivery_id=?", (self.delivery_id,)).fetchone()[0],
                "delivered",
            )
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()
