import json
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

    def _create_quiesced_recovery_db(self, root: Path) -> tuple[Path, dict]:
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
                  response_ready_at TEXT,
                  delivery_confirmed_at TEXT,
                  worker_id TEXT,
                  lease_token TEXT,
                  lease_expires_at TEXT,
                  heartbeat_at TEXT,
                  failure_class TEXT,
                  failure_message TEXT,
                  delivery_last_error TEXT,
                  updated_at TEXT
                );
                CREATE TABLE cnx_direct_model_call(
                  ticket_id TEXT PRIMARY KEY,
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
                CREATE TABLE cnx_sessions(
                  session_key TEXT PRIMARY KEY,
                  state TEXT,
                  generation INTEGER
                );
                CREATE TABLE cnx_direct_recovery(
                  ticket_id TEXT PRIMARY KEY,
                  mode TEXT,
                  state TEXT,
                  attempt_count INTEGER,
                  active_run_id TEXT,
                  next_attempt_at TEXT,
                  last_error TEXT,
                  owner_generation INTEGER,
                  created_at TEXT,
                  updated_at TEXT
                );
                CREATE TABLE ticket_events(
                  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id TEXT,
                  event_type TEXT,
                  payload_json TEXT,
                  created_at TEXT
                );
                """
            )
            db.execute(
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,"
                "delivery_confirmed_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    "T-REC", "R-REC", "agent:main:dashboard:test", "accepted", 0, None, None, None,
                    "2026-09-09T13:00:03+00:00",
                ),
            )
            db.execute(
                "INSERT INTO cnx_direct_model_call(ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,ended_at,"
                "outcome,error_category,failure_kind,recovery_started_at,recovery_attempt_count,updated_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "T-REC", "R-REC", "C-REC", "recovering", "future-cloud-provider", "future-model",
                    "2026-09-09T13:00:00+00:00", "2026-09-09T13:15:00+00:00", "2026-09-09T13:00:02+00:00",
                    "error", "network", "connection_reset", "2026-09-09T13:00:04+00:00", 1,
                    "2026-09-09T13:00:04+00:00",
                ),
            )
            db.execute(
                "INSERT INTO cnx_sessions(session_key,state,generation) VALUES (?,?,?)",
                ("agent:main:dashboard:test", "active", 7),
            )
            db.commit()
        finally:
            db.close()
        return path, {
            "ticket_id": "T-REC",
            "run_id": "R-REC",
            "call_id": "C-REC",
            "state": "recovering",
            "provider": "future-cloud-provider",
            "model": "future-model",
            "started_at": "2026-09-09T13:00:00+00:00",
            "deadline_at": "2026-09-09T13:15:00+00:00",
            "ended_at": "2026-09-09T13:00:02+00:00",
            "outcome": "error",
            "error_category": "network",
            "failure_kind": "connection_reset",
            "recovery_started_at": "2026-09-09T13:00:04+00:00",
            "recovery_attempt_count": 1,
        }

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

    def test_quiesced_terminal_error_queues_recovery_with_exact_non_timeout_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path, claim = self._create_quiesced_recovery_db(root)
            fences = {
                "unverifiableFailed": [],
                "durableDeliveryHeld": [],
                "confirmedHeld": [],
                "workflowOwnedSkipped": [],
            }

            with mock.patch.object(hp.v091, "reconcile_direct_delivery_before_recovery", return_value=fences) as delivery_fence, \
                 mock.patch.object(hp, "_state_provider") as state_provider, \
                 mock.patch.object(hp.providers, "probe") as provider_probe, \
                 mock.patch.object(hp.providers, "start") as provider_start:
                result = hp.classify_quiesced_terminal_error_direct_model_call(
                    root, claim, now_iso="2026-09-09T13:00:05+00:00"
                )

            delivery_fence.assert_called_once_with(root, "2026-09-09T13:00:05+00:00")
            state_provider.assert_not_called()
            provider_probe.assert_not_called()
            provider_start.assert_not_called()
            self.assertEqual(result["action"], "pre-response-recovery-authorized")
            self.assertEqual(result["recoveryAuthority"], "terminal-model-call-error")
            self.assertEqual(result["ownerGeneration"], 7)
            self.assertEqual(result["deliveryFences"], fences)

            db = sqlite3.connect(path)
            db.row_factory = sqlite3.Row
            try:
                recovery = db.execute(
                    "SELECT mode,state,attempt_count,active_run_id,owner_generation,last_error "
                    "FROM cnx_direct_recovery WHERE ticket_id='T-REC'"
                ).fetchone()
                model_call = db.execute(
                    "SELECT state,outcome,provider,model,error_category,failure_kind "
                    "FROM cnx_direct_model_call WHERE ticket_id='T-REC'"
                ).fetchone()
                event = db.execute(
                    "SELECT event_type,payload_json FROM ticket_events WHERE ticket_id='T-REC' ORDER BY event_id DESC LIMIT 1"
                ).fetchone()
            finally:
                db.close()

            self.assertEqual(dict(recovery), {
                "mode": "resume",
                "state": "pending",
                "attempt_count": 0,
                "active_run_id": None,
                "owner_generation": 7,
                "last_error": mock.ANY,
            })
            self.assertEqual(dict(model_call), {
                "state": "interrupted",
                "outcome": "host-terminal-error-authorized",
                "provider": "future-cloud-provider",
                "model": "future-model",
                "error_category": "network",
                "failure_kind": "connection_reset",
            })
            self.assertEqual(event["event_type"], "host_direct_model_terminal_error_authorized")
            payload = json.loads(event["payload_json"])
            self.assertEqual(payload["recoveryAuthority"], "terminal-model-call-error")
            self.assertEqual(payload["runId"], "R-REC")
            self.assertEqual(payload["callId"], "C-REC")
            self.assertEqual(payload["provider"], "future-cloud-provider")
            self.assertEqual(payload["model"], "future-model")
            self.assertEqual(payload["errorCategory"], "network")
            self.assertEqual(payload["failureKind"], "connection_reset")
            self.assertNotIn("timeout", event["event_type"])
            self.assertNotIn("timeout", payload["recoveryAuthority"])


if __name__ == "__main__":
    unittest.main()
