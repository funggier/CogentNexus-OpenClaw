from __future__ import annotations

import importlib.util
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "skills" / "cogentnexus" / "scripts" / "host.py"
spec = importlib.util.spec_from_file_location("cnx_host", HOST)
cnx_host = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx_host)


class HostControllerTests(unittest.TestCase):
    def test_state_is_atomic_and_defaults_managed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            state = cnx_host.initialize(root)
            self.assertEqual(state["mode"], "managed")
            next_state = cnx_host.transition(root, mode="passthrough")
            self.assertEqual(next_state["mode"], "passthrough")
            self.assertGreater(next_state["generation"], state["generation"])
            self.assertFalse(cnx_host.host_state_path(root).with_suffix(".tmp").exists())

    def test_policy_round_trip_preserves_user_content(self):
        original = "# User policy\n\nKeep this.\n"
        policy = "## Managed\nTicket first."
        merged = cnx_host.merge_policy(original, policy)
        self.assertIn("Keep this.", merged)
        self.assertIn(cnx_host.BEGIN, merged)
        restored = cnx_host.remove_policy_text(merged)
        self.assertEqual(restored, original)

    def test_initialize_seeds_durable_core_policy_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            cnx_host.initialize(root)
            snapshot = cnx_host.policy_snapshot_path(root)
            self.assertTrue(snapshot.is_file())
            text = snapshot.read_text(encoding="utf-8")
            self.assertIn("CogentNexus - Managed Continuity", text)
            info = cnx_host.policy_info(root)
            self.assertEqual(info["source"], "registered")
            self.assertGreater(info["bytes"], 0)
            self.assertEqual(len(info["sha256"]), 64)

    def test_registered_policy_persists_across_passthrough_and_reapply(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogent"
            workspace.mkdir(parents=True)
            cnx_host.initialize(root)
            cnx_host.save_state(
                root,
                {
                    "schemaVersion": 1,
                    "mode": "passthrough",
                    "desiredGateway": "running",
                    "desiredProvider": "unchanged",
                    "generation": 2,
                },
            )
            custom = Path(tmp) / "ecosystem-policy.md"
            custom.write_text("## Ecosystem Managed Policy\n\nDIRECT first.\n", encoding="utf-8")
            result = cnx_host.register_policy(root, custom)
            self.assertFalse(result["applied"])
            self.assertIn("Ecosystem Managed Policy", cnx_host.policy_snapshot_path(root).read_text(encoding="utf-8"))
            self.assertFalse((workspace / "AGENTS.md").exists())

            cnx_host.save_state(
                root,
                {
                    "schemaVersion": 1,
                    "mode": "managed",
                    "desiredGateway": "running",
                    "desiredProvider": "running",
                    "generation": 3,
                },
            )
            applied = cnx_host.apply_registered_policy(root)
            self.assertTrue(applied["applied"])
            agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Ecosystem Managed Policy", agents)
            self.assertEqual(agents.count(cnx_host.BEGIN), 1)
            self.assertEqual(agents.count(cnx_host.END), 1)

    def test_reset_policy_restores_core_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogent"
            workspace.mkdir(parents=True)
            cnx_host.initialize(root)
            custom = Path(tmp) / "custom.md"
            custom.write_text("## Custom\n", encoding="utf-8")
            cnx_host.register_policy(root, custom)
            self.assertIn("Custom", cnx_host.policy_snapshot_path(root).read_text(encoding="utf-8"))
            result = cnx_host.reset_policy(root)
            self.assertTrue(result["applied"])
            self.assertIn("CogentNexus - Managed Continuity", cnx_host.policy_snapshot_path(root).read_text(encoding="utf-8"))

    def _ticket_db(self, root: Path) -> sqlite3.Connection:
        path = cnx_host.ticket_db(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.executescript("""
        CREATE TABLE tickets(
          ticket_id TEXT PRIMARY KEY, owner_session_key TEXT NOT NULL, status TEXT NOT NULL,
          workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT, worker_id TEXT,
          lease_token TEXT, lease_expires_at TEXT, heartbeat_at TEXT, attempt_count INTEGER NOT NULL DEFAULT 0,
          failure_class TEXT, failure_message TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE ticket_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT,ticket_id TEXT,event_type TEXT,payload_json TEXT,created_at TEXT);
        CREATE TABLE ticket_outbox(outbox_id INTEGER PRIMARY KEY AUTOINCREMENT,ticket_id TEXT UNIQUE,owner_session_key TEXT,terminal_status TEXT,payload_json TEXT,delivery_status TEXT,created_at TEXT);
        CREATE TABLE cnx_direct_recovery(ticket_id TEXT PRIMARY KEY,state TEXT,active_run_id TEXT,next_attempt_at TEXT,last_error TEXT,updated_at TEXT);
        """)
        return db

    def test_interrupted_direct_ticket_promotes_to_waiting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            db = self._ticket_db(root)
            db.execute("INSERT INTO tickets(ticket_id,owner_session_key,status,workflow_eligible,created_at,updated_at) VALUES ('T1','S1','accepted',0,'2026-01-01T00:00:00+00:00','2026-01-01T00:00:00+00:00')")
            db.commit(); db.close()
            recovered = cnx_host.promote_interrupted_direct(root, "2026-01-02T00:00:00+00:00", "gateway recovered")
            self.assertEqual(recovered, ["T1"])
            db = sqlite3.connect(cnx_host.ticket_db(root))
            row = db.execute("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id='T1'").fetchone()
            event = db.execute("SELECT event_type FROM ticket_events WHERE ticket_id='T1'").fetchone()
            db.close()
            self.assertEqual(row, ("waiting", 1, "interrupted"))
            self.assertEqual(event[0], "host_recovered_direct")

    def test_ticket_cancel_is_terminal_silent_and_suppresses_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            db = self._ticket_db(root)
            db.execute("INSERT INTO tickets(ticket_id,owner_session_key,status,workflow_eligible,created_at,updated_at) VALUES ('T2','S2','waiting',1,'2026-01-01T00:00:00+00:00','2026-01-01T00:00:00+00:00')")
            db.execute("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,created_at) VALUES ('T2','S2','failed','{}','pending','2026-01-01T00:00:00+00:00')")
            db.execute("INSERT INTO cnx_direct_recovery(ticket_id,state,active_run_id,next_attempt_at,last_error,updated_at) VALUES ('T2','pending','old-run','2026-01-02T00:00:00+00:00',NULL,'2026-01-01T00:00:00+00:00')")
            db.commit(); db.close()
            result = cnx_host.cancel_ticket(root, "T2", "operator cancelled")
            self.assertTrue(result["changed"])
            db = sqlite3.connect(cnx_host.ticket_db(root))
            row = db.execute("SELECT status,failure_class FROM tickets WHERE ticket_id='T2'").fetchone()
            outbox = db.execute("SELECT count(*) FROM ticket_outbox WHERE ticket_id='T2' AND delivery_status='pending'").fetchone()[0]
            recovery = db.execute("SELECT state,active_run_id,next_attempt_at FROM cnx_direct_recovery WHERE ticket_id='T2'").fetchone()
            db.close()
            self.assertEqual(row, ("cancelled", None))
            self.assertEqual(outbox, 0)
            self.assertEqual(recovery, ("cancelled", None, None))

    def test_gateway_status_requires_connectivity_not_only_zero_exit(self):
        original_run = cnx_host.run
        original_executable = cnx_host.openclaw_executable
        try:
            cnx_host.openclaw_executable = lambda: "openclaw"
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: stopped\n", "Connectivity probe: failed\n")
            self.assertFalse(cnx_host.gateway_status()["healthy"])
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: running\nConnectivity probe: ok\n", "")
            self.assertTrue(cnx_host.gateway_status()["healthy"])
        finally:
            cnx_host.run = original_run
            cnx_host.openclaw_executable = original_executable

    def test_passthrough_supervisor_does_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            cnx_host.save_state(root, {"schemaVersion":1,"mode":"passthrough","desiredGateway":"running","desiredProvider":"unchanged","generation":2})
            result = cnx_host.supervisor_tick(root, True)
            self.assertEqual(result["result"], "passthrough")
            self.assertEqual(result["action"], "none")

    def test_maintenance_supervisor_does_not_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            cnx_host.save_state(root, {"schemaVersion":1,"mode":"managed","desiredGateway":"stopped","desiredProvider":"stopped","generation":2})
            result = cnx_host.supervisor_tick(root, True)
            self.assertEqual(result["result"], "maintenance")
            self.assertEqual(result["action"], "none")


if __name__ == "__main__":
    unittest.main()
