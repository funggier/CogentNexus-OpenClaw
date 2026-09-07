from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_authority_v091 as authority
import host_provider_v092 as provider
import host_stall_v091 as stall
import host_v091 as recovery
import supervisor_quiescence as quiescence


class ActivationSafetyContractTests(unittest.TestCase):
    def test_composed_supervisor_quiesces_before_overlay_work(self):
        for name, boundary in (("provider", provider.supervisor_tick), ("stall", stall.supervisor_tick)):
            with self.subTest(boundary=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / ".cogentnexus-openclaw"
                quiescence.acquire(root, "activation-test", ttl=60)
                with mock.patch.object(stall.legacy, "load_state", side_effect=AssertionError("overlay work ran")), mock.patch.object(
                    provider.provider_events, "ensure_adapter", side_effect=AssertionError("adapter ran")
                ):
                    result = boundary(root, True)
                self.assertEqual(result["result"], "quiesced")
                self.assertEqual(result["action"], "none")

    def test_enable_releases_lease_when_pretransaction_reconciler_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(authority.legacy, "initialize"), mock.patch.object(
                authority.legacy, "load_state", return_value={"mode": "passthrough", "generation": 7}
            ), mock.patch.object(
                authority.legacy, "reconcile_terminal_fences", side_effect=RuntimeError("classifier failed")
            ):
                with self.assertRaisesRegex(RuntimeError, "classifier failed"):
                    authority.enable(root)
            self.assertEqual(quiescence.read(root)["status"], "absent")

    def test_interrupted_promotion_requires_fresh_identified_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
            path.parent.mkdir(parents=True)
            db = sqlite3.connect(path)
            db.executescript(
                """
                CREATE TABLE tickets(
                  ticket_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, owner_session_key TEXT NOT NULL,
                  status TEXT NOT NULL, workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT,
                  response_ready_at TEXT, delivery_confirmed_at TEXT, failure_class TEXT, failure_message TEXT,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE ticket_events(
                  event_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL,
                  event_type TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE cnx_sessions(
                  session_key TEXT PRIMARY KEY, state TEXT NOT NULL, generation INTEGER NOT NULL,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL, session_id TEXT
                );
                """
            )
            sessions = [
                ("agent:main:test:stale", "active", 1, "2026-08-18T08:00:00Z", "2026-08-18T08:00:00Z", "old-session"),
                ("agent:main:test:activation-aged", "active", 1, "2026-08-18T09:40:00Z", "2026-08-18T09:50:00Z", "aged-session"),
                ("agent:main:test:ambiguous", "active", 1, "2026-08-18T09:50:00Z", "2026-08-18T10:15:00Z", None),
                ("agent:main:test:fresh", "active", 0, "2026-08-18T09:50:00Z", "2026-08-18T10:10:00Z", "fresh-session"),
            ]
            db.executemany("INSERT INTO cnx_sessions VALUES (?,?,?,?,?,?)", sessions)
            tickets = [
                ("T-stale", "run-stale", sessions[0][0]),
                ("T-activation-aged", "run-activation-aged", sessions[1][0]),
                ("T-ambiguous", "run-ambiguous", sessions[2][0]),
                ("T-fresh", "run-fresh", sessions[3][0]),
            ]
            db.executemany(
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,created_at,updated_at) "
                "VALUES (?,?,?,'accepted',0,NULL,NULL,'2026-08-18T09:51:00Z','2026-08-18T09:51:00Z')",
                tickets,
            )
            db.commit()
            db.close()

            with mock.patch.object(recovery.legacy, "now_iso", return_value="2026-08-18T10:20:00Z"):
                promoted = recovery.promote_interrupted_direct_v091(root, "2026-08-18T10:00:00Z", "activation")
            self.assertEqual(promoted, ["T-fresh"])
            check = sqlite3.connect(path)
            states = dict(check.execute("SELECT ticket_id,workflow_eligible FROM tickets ORDER BY ticket_id"))
            check.close()
            self.assertEqual(states, {"T-activation-aged": 0, "T-ambiguous": 0, "T-fresh": 1, "T-stale": 0})


if __name__ == "__main__":
    unittest.main()
