import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


class HostProviderV095TerminalErrorTests(unittest.TestCase):
    def _create_terminal_error_db(self, root: Path) -> Path:
        path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        try:
            db.executescript(
                """
                CREATE TABLE tickets(
                  ticket_id TEXT PRIMARY KEY,
                  run_id TEXT,
                  owner_session_key TEXT,
                  status TEXT,
                  workflow_eligible INTEGER,
                  workflow_id TEXT,
                  response_ready_at TEXT
                );
                CREATE TABLE cnx_direct_model_call(
                  ticket_id TEXT,
                  run_id TEXT,
                  call_id TEXT,
                  state TEXT,
                  provider TEXT,
                  model TEXT,
                  started_at TEXT,
                  deadline_at TEXT,
                  ended_at TEXT,
                  outcome TEXT,
                  error_category TEXT,
                  failure_kind TEXT,
                  recovery_started_at TEXT,
                  recovery_attempt_count INTEGER,
                  updated_at TEXT
                );
                """
            )
            db.execute(
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at) "
                "VALUES (?,?,?,?,?,?,?)",
                ("T-TERM", "R-TERM", "agent:main:dashboard:test", "accepted", 0, None, None),
            )
            db.execute(
                "INSERT INTO cnx_direct_model_call("
                "ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,ended_at,outcome,"
                "error_category,failure_kind,recovery_started_at,recovery_attempt_count,updated_at"
                ") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "T-TERM", "R-TERM", "C-TERM", "terminal_error", "future-cloud-provider", "future-model",
                    "2026-09-09T13:00:00+00:00", "2026-09-09T13:15:00+00:00", "2026-09-09T13:00:02+00:00",
                    "error", "network", "connection_reset", None, 0, "2026-09-09T13:00:03+00:00",
                ),
            )
            db.commit()
        finally:
            db.close()
        return path

    def test_claims_exact_terminal_error_without_global_provider_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = self._create_terminal_error_db(root)

            with mock.patch.object(hp, "_state_provider") as state_provider, \
                 mock.patch.object(hp.providers, "probe") as provider_probe, \
                 mock.patch.object(hp.providers, "start") as provider_start:
                claim = hp.claim_terminal_error_direct_model_call(
                    root, now_iso="2026-09-09T13:00:04+00:00"
                )

            state_provider.assert_not_called()
            provider_probe.assert_not_called()
            provider_start.assert_not_called()
            self.assertEqual(claim["ticket_id"], "T-TERM")
            self.assertEqual(claim["run_id"], "R-TERM")
            self.assertEqual(claim["call_id"], "C-TERM")
            self.assertEqual(claim["provider"], "future-cloud-provider")
            self.assertEqual(claim["model"], "future-model")
            self.assertEqual(claim["outcome"], "error")
            self.assertEqual(claim["error_category"], "network")
            self.assertEqual(claim["failure_kind"], "connection_reset")
            self.assertEqual(claim["state"], "recovering")
            self.assertEqual(claim["recovery_started_at"], "2026-09-09T13:00:04+00:00")
            self.assertEqual(claim["recovery_attempt_count"], 1)

            db = sqlite3.connect(path)
            try:
                row = db.execute(
                    "SELECT state,recovery_started_at,recovery_attempt_count,provider,model,outcome "
                    "FROM cnx_direct_model_call WHERE ticket_id='T-TERM'"
                ).fetchone()
            finally:
                db.close()
            self.assertEqual(
                row,
                ("recovering", "2026-09-09T13:00:04+00:00", 1, "future-cloud-provider", "future-model", "error"),
            )


if __name__ == "__main__":
    unittest.main()
