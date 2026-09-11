from __future__ import annotations

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

WAKE = SCRIPTS / "wake_authority_v095.py"
spec = importlib.util.spec_from_file_location("cnx_wake_authority_v095", WAKE)
wake = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = wake
spec.loader.exec_module(wake)


class WakeAuthorityV095Tests(unittest.TestCase):
    NOW = datetime(2026, 9, 12, 0, 0, tzinfo=timezone.utc)

    def _root(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / ".cogentnexus-openclaw"
        (root / "runtime").mkdir(parents=True, exist_ok=True)
        self.addCleanup(tmp.cleanup)
        return root

    def _db(self, root: Path) -> sqlite3.Connection:
        path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
        db = sqlite3.connect(path)
        db.execute("CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY, status TEXT NOT NULL, workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT, owner_session_key TEXT, response_ready_at TEXT, delivery_confirmed_at TEXT)")
        db.execute("CREATE TABLE cnx_sessions(session_key TEXT PRIMARY KEY, state TEXT NOT NULL, generation INTEGER NOT NULL, updated_at TEXT NOT NULL)")
        db.execute("CREATE TABLE cnx_assistant_delivery(delivery_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL, owner_session_key TEXT NOT NULL, owner_generation INTEGER NOT NULL, status TEXT NOT NULL, updated_at TEXT NOT NULL, kind TEXT NOT NULL)")
        db.execute("CREATE TABLE cnx_direct_recovery(ticket_id TEXT PRIMARY KEY, state TEXT NOT NULL, owner_generation INTEGER NOT NULL, next_attempt_at TEXT, updated_at TEXT NOT NULL)")
        return db

    def test_empty_runtime_is_idle(self):
        root = self._root()
        decision = wake.classify_wake(root, self.NOW)
        self.assertFalse(decision.actionable)
        self.assertEqual(decision.authority, "none")
        self.assertIsNone(decision.work_id)
        self.assertEqual(decision.reason, "idle/no-actionable-work")

    def test_stale_nonactionable_delivery_is_idle(self):
        root = self._root()
        db = self._db(root)
        stale = "2026-09-01T00:00:00+00:00"
        db.execute("INSERT INTO tickets(ticket_id,status,owner_session_key) VALUES ('T-stale','accepted','S1')")
        db.execute("INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S1','active',2,?)", (self.NOW.isoformat(),))
        db.execute("INSERT INTO cnx_assistant_delivery(ticket_id,owner_session_key,owner_generation,status,updated_at,kind) VALUES ('T-stale','S1',2,'pending',?,'assistant')", (stale,))
        db.commit(); db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertFalse(decision.actionable)
        self.assertEqual(decision.authority, "none")

    def test_exact_due_direct_recovery_returns_identity(self):
        root = self._root()
        db = self._db(root)
        db.execute("INSERT INTO tickets(ticket_id,status,workflow_eligible,workflow_id,owner_session_key) VALUES ('T1','accepted',0,NULL,'S1')")
        db.execute("INSERT INTO cnx_sessions(session_key,state,generation,updated_at) VALUES ('S1','active',2,?)", (self.NOW.isoformat(),))
        db.execute("INSERT INTO cnx_direct_recovery(ticket_id,state,owner_generation,next_attempt_at,updated_at) VALUES ('T1','pending',2,?,?)", (self.NOW.isoformat(), self.NOW.isoformat()))
        db.commit(); db.close()
        decision = wake.classify_wake(root, self.NOW)
        self.assertTrue(decision.actionable)
        self.assertEqual(decision.authority, "direct_recovery")
        self.assertEqual(decision.work_id, "T1")


if __name__ == "__main__":
    unittest.main()
