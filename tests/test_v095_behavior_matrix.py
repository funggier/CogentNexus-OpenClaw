from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


host_state = load(
    "cnx_host_state_v095_matrix",
    SCRIPTS / "host_state_v095.py",
)
wake = load(
    "cnx_wake_authority_v095_matrix",
    SCRIPTS / "wake_authority_v095.py",
)


class BehaviorMatrixV095Tests(unittest.TestCase):
    NOW = datetime(2026, 9, 12, 0, 0, tzinfo=timezone.utc)

    def _root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / ".cogentnexus-openclaw"
        (root / "runtime").mkdir(parents=True)
        self.addCleanup(tmp.cleanup)
        return root

    def _db(self, root: Path) -> sqlite3.Connection:
        path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
        db = sqlite3.connect(path)
        db.execute(
            "CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY, status TEXT NOT NULL, "
            "workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT, "
            "owner_session_key TEXT)"
        )
        db.execute(
            "CREATE TABLE cnx_sessions(session_key TEXT PRIMARY KEY, state TEXT NOT NULL, "
            "generation INTEGER NOT NULL, updated_at TEXT NOT NULL)"
        )
        db.execute(
            "CREATE TABLE cnx_assistant_delivery(delivery_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "ticket_id TEXT NOT NULL, owner_session_key TEXT NOT NULL, "
            "owner_generation INTEGER NOT NULL, status TEXT NOT NULL, "
            "updated_at TEXT NOT NULL, kind TEXT NOT NULL)"
        )
        db.execute(
            "CREATE TABLE cnx_direct_recovery(ticket_id TEXT PRIMARY KEY, state TEXT NOT NULL, "
            "owner_generation INTEGER NOT NULL, next_attempt_at TEXT, updated_at TEXT NOT NULL)"
        )
        return db

    def test_provider_class_and_runtime_events_never_become_cnx_authority(self):
        provider_classes = ["local_ollama", "cloud", "unknown_future"]
        runtime_events = ["normal", "gateway_restart", "provider_switch", "idle_tick"]
        for provider in provider_classes:
            for event in runtime_events:
                with self.subTest(provider=provider, event=event):
                    source = {
                        "schemaVersion": 2,
                        "cnxMode": "active",
                        "desiredGateway": "running",
                        "providerOwnership": "openclaw",
                        "managedLocalAdapters": {"ollama": "auto"},
                        "generation": 7,
                        "updatedAt": "2026-09-12T00:00:00+00:00",
                        "selectedProvider": provider,
                        "runtimeEvent": event,
                        "desiredProvider": provider,
                    }
                    migrated = host_state.migrate_v094_state(source, plugin_enabled=True)
                    self.assertEqual(migrated["cnxMode"], "active")
                    self.assertEqual(migrated["desiredGateway"], "running")
                    self.assertEqual(migrated["generation"], 7)
                    self.assertEqual(migrated["providerOwnership"], "openclaw")
                    self.assertNotIn("selectedProvider", migrated)
                    self.assertNotIn("desiredProvider", migrated)

    def test_ollama_to_cloud_same_session_preserves_cnx_authority_and_generation(self):
        before = {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "selectedProvider": "local_ollama",
            "desiredProvider": "local_ollama",
            "generation": 12,
        }
        migrated = host_state.migrate_v094_state(before, plugin_enabled=True)
        self.assertEqual(migrated["cnxMode"], "active")
        self.assertEqual(migrated["generation"], 12)
        self.assertEqual(migrated["providerOwnership"], "openclaw")
        self.assertNotIn("selectedProvider", migrated)
        self.assertNotIn("desiredProvider", migrated)

    def test_cloud_a_to_cloud_b_durable_path_keeps_ticket_durable_and_provider_neutral(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-cloud','executing',1,'W-cloud','S-cloud')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) "
                "VALUES ('S-cloud','active',3,?)",
                (self.NOW.isoformat(),),
            )
            db.commit()
        finally:
            db.close()

        migrated = host_state.migrate_v094_state(
            {
                "schemaVersion": 1,
                "mode": "managed",
                "desiredGateway": "running",
                "selectedProvider": "cloud-b",
                "desiredProvider": "cloud-b",
                "generation": 3,
            },
            plugin_enabled=True,
        )
        self.assertEqual(migrated["generation"], 3)
        check = sqlite3.connect(root / "runtime" / "cogentnexus-openclaw.sqlite3")
        try:
            self.assertEqual(
                check.execute("SELECT status,workflow_eligible,workflow_id FROM tickets WHERE ticket_id='T-cloud'").fetchone(),
                ("executing", 1, "W-cloud"),
            )
        finally:
            check.close()

    def test_unknown_future_provider_has_both_direct_and_durable_authority_paths(self):
        direct = host_state.migrate_v094_state(
            {
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "unknown_future",
                "desiredProvider": "unknown_future",
                "generation": 4,
            },
            plugin_enabled=True,
        )
        durable = host_state.migrate_v094_state(
            {
                "schemaVersion": 1,
                "mode": "passthrough",
                "selectedProvider": "unknown_future",
                "desiredProvider": "unknown_future",
                "generation": 5,
            },
            plugin_enabled=True,
        )
        self.assertEqual(direct["cnxMode"], "active")
        self.assertEqual(durable["cnxMode"], "active")
        self.assertEqual(direct["generation"], 4)
        self.assertEqual(durable["generation"], 5)
        self.assertEqual(direct["providerOwnership"], "openclaw")
        self.assertEqual(durable["providerOwnership"], "openclaw")

    def test_disabled_mode_is_native_openclaw_boundary_for_all_provider_classes(self):
        for provider in ("local_ollama", "cloud", "unknown_future"):
            with self.subTest(provider=provider):
                migrated = host_state.migrate_v094_state(
                    {
                        "schemaVersion": 1,
                        "mode": "passthrough",
                        "desiredGateway": "running",
                        "selectedProvider": provider,
                        "desiredProvider": provider,
                        "generation": 11,
                    },
                    plugin_enabled=False,
                )
                self.assertEqual(migrated["cnxMode"], "disabled")
                self.assertEqual(migrated["generation"], 11)
                self.assertEqual(migrated["providerOwnership"], "openclaw")

    def test_gateway_restart_same_session_does_not_rotate_generation(self):
        source = {
            "schemaVersion": 2,
            "cnxMode": "active",
            "desiredGateway": "running",
            "providerOwnership": "openclaw",
            "managedLocalAdapters": {"ollama": "auto"},
            "generation": 9,
            "runtimeEvent": "gateway_restart",
        }
        migrated = host_state.migrate_v094_state(source, plugin_enabled=True)
        self.assertEqual(migrated["generation"], 9)

    def test_provider_failure_retains_ticket_as_actionable_durable_work(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-provider-failure','accepted',1,NULL,'S1')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S1','active',2,?)",
                (self.NOW.isoformat(),),
            )
            db.commit()
        finally:
            db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertTrue(decision.actionable)
        self.assertEqual(decision.authority, "ticket")
        self.assertEqual(decision.work_id, "T-provider-failure")

    def test_interrupted_direct_run_uses_exact_same_generation_recovery(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-interrupted','accepted',0,NULL,'S2')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S2','active',6,?)",
                (self.NOW.isoformat(),),
            )
            db.execute(
                "INSERT INTO cnx_direct_recovery(ticket_id,state,owner_generation,next_attempt_at,updated_at) "
                "VALUES ('T-interrupted','pending',6,?,?)",
                (self.NOW.isoformat(), self.NOW.isoformat()),
            )
            db.commit()
        finally:
            db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertTrue(decision.actionable)
        self.assertEqual(decision.authority, "direct_recovery")
        self.assertEqual(decision.work_id, "T-interrupted")

    def test_delivery_failure_does_not_promote_failed_delivery_into_inference_wake(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-delivery-failed','completed',0,NULL,'S3')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S3','active',3,?)",
                (self.NOW.isoformat(),),
            )
            db.execute(
                "INSERT INTO cnx_assistant_delivery(ticket_id,owner_session_key,owner_generation,status,updated_at,kind) "
                "VALUES ('T-delivery-failed','S3',3,'failed',?,'direct_result')",
                (self.NOW.isoformat(),),
            )
            db.commit()
        finally:
            db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertFalse(decision.actionable)
        self.assertEqual(decision.authority, "none")
        self.assertEqual(decision.reason, "idle/no-actionable-work")

    def test_final_payload_delivery_failure_keeps_ticket_terminal_without_regeneration_wake(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-terminal','completed',0,NULL,'S4')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S4','active',4,?)",
                (self.NOW.isoformat(),),
            )
            db.execute(
                "INSERT INTO cnx_assistant_delivery(ticket_id,owner_session_key,owner_generation,status,updated_at,kind) "
                "VALUES ('T-terminal','S4',4,'failed',?,'direct_result')",
                (self.NOW.isoformat(),),
            )
            db.commit()
        finally:
            db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertFalse(decision.actionable)
        check = sqlite3.connect(root / "runtime" / "cogentnexus-openclaw.sqlite3")
        try:
            self.assertEqual(check.execute("SELECT status FROM tickets WHERE ticket_id='T-terminal'").fetchone(), ("completed",))
            self.assertEqual(check.execute("SELECT COUNT(*) FROM cnx_direct_recovery").fetchone(), (0,))
        finally:
            check.close()

    def test_idle_event_has_no_wake_when_durable_runtime_is_empty(self):
        root = self._root()
        decision = wake.classify_wake(root, self.NOW)
        self.assertFalse(decision.actionable)
        self.assertEqual(decision.authority, "none")
        self.assertEqual(decision.reason, "idle/no-actionable-work")

    def test_final_delivery_wins_over_completed_ticket_in_cross_boundary_matrix(self):
        root = self._root()
        db = self._db(root)
        try:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) "
                "VALUES ('T-final','completed',0,NULL,'S1')"
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation,updated_at) "
                "VALUES ('S1','active',4,?)",
                (self.NOW.isoformat(),),
            )
            db.execute(
                "INSERT INTO cnx_assistant_delivery(ticket_id,owner_session_key,owner_generation,status,updated_at,kind) "
                "VALUES ('T-final','S1',4,'pending',?,'direct_result')",
                (self.NOW.isoformat(),),
            )
            db.commit()
        finally:
            db.close()

        decision = wake.classify_wake(root, self.NOW)
        self.assertTrue(decision.actionable)
        self.assertEqual(decision.authority, "delivery")
        self.assertEqual(decision.work_id, "1")


if __name__ == "__main__":
    unittest.main()
