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
