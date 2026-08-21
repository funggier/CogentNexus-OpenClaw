import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


class HostProviderV092Tests(unittest.TestCase):
    def test_start_provider_boundary_strips_legacy_provider_flag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            calls = []

            def fake_runtime(root_arg, *args, timeout=180, check=True):
                calls.append((root_arg, args, timeout, check))
                return subprocess.CompletedProcess(args=list(args), returncode=0, stdout=json.dumps({"started": True}), stderr="")

            healthy = {"healthy": True, "installed": True, "name": "lmstudio"}
            with mock.patch.object(hp, "ORIGINAL_RUNTIME", side_effect=fake_runtime), \
                 mock.patch.object(hp, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": True}), \
                 mock.patch.object(hp.providers, "start", return_value={"ok": True, "after": healthy}):
                result = hp.provider_aware_runtime(root, "lifecycle", "start", "--provider", timeout=30, check=True)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(calls[0][1], ("lifecycle", "start"))
            self.assertEqual(json.loads(result.stdout)["provider"], "lmstudio")

    def test_stop_quiesces_gateway_before_selected_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            order = []

            def fake_runtime(root_arg, *args, timeout=180, check=True):
                order.append("gateway-stop")
                return subprocess.CompletedProcess(args=list(args), returncode=0, stdout=json.dumps({"stopped": True}), stderr="")

            def fake_stop(name, timeout=30):
                order.append(f"provider-stop:{name}")
                return {"ok": True}

            with mock.patch.object(hp, "ORIGINAL_RUNTIME", side_effect=fake_runtime), \
                 mock.patch.object(hp, "_state_provider", return_value="ollama"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(hp.providers, "stop", side_effect=fake_stop):
                result = hp.provider_aware_runtime(root, "lifecycle", "stop", "--provider", timeout=30, check=True)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(order, ["gateway-stop", "provider-stop:ollama"])

    def test_missing_selection_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            with mock.patch.object(hp, "_state_provider", return_value=None):
                result = hp.provider_aware_runtime(root, "lifecycle", "start", "--provider", timeout=30, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("provider selection required", result.stdout)

    def _create_direct_call_db(self, root: Path, *, deadline_delta=-1, state="active", outcome=None) -> Path:
        path = root / "runtime" / "cogentnexus.sqlite3"
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
                  recovery_started_at TEXT,
                  recovery_attempt_count INTEGER,
                  updated_at TEXT
                );
                CREATE TABLE ticket_events(
                  ticket_id TEXT,
                  event_type TEXT,
                  payload_json TEXT,
                  created_at TEXT
                );
                """
            )
            now = datetime.now(timezone.utc)
            db.execute(
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at) VALUES (?,?,?,?,?,?,?)",
                ("T1", "R1", "agent:main:test", "accepted", 0, None, None),
            )
            ended_at = now.isoformat() if state == "ended" else None
            db.execute(
                "INSERT INTO cnx_direct_model_call(ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,ended_at,outcome,recovery_started_at,recovery_attempt_count,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "T1", "R1", "C1", state, "lmstudio_local", "qwen/qwen3.5-9b",
                    (now - timedelta(minutes=10)).isoformat(),
                    (now + timedelta(seconds=deadline_delta)).isoformat(),
                    ended_at, outcome, None, 0, now.isoformat(),
                ),
            )
            db.commit()
        finally:
            db.close()
        return path

    def test_healthy_expired_call_is_guarded_without_extending_deadline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = self._create_direct_call_db(root)
            db = sqlite3.connect(path)
            before = db.execute("SELECT deadline_at FROM cnx_direct_model_call WHERE ticket_id='T1'").fetchone()[0]
            db.close()

            first = hp._guard_healthy_active_call(root, "lmstudio")
            second = hp._guard_healthy_active_call(root, "lmstudio")
            self.assertEqual(first["classification"], "active_model_processing_unknown")
            self.assertFalse(first["recoveryEligible"])
            self.assertFalse(first["providerRestart"])
            self.assertEqual(second["callId"], "C1")

            db = sqlite3.connect(path)
            try:
                row = db.execute(
                    "SELECT state,outcome,recovery_attempt_count,deadline_at FROM cnx_direct_model_call WHERE ticket_id='T1'"
                ).fetchone()
                events = db.execute(
                    "SELECT event_type,payload_json FROM ticket_events WHERE ticket_id='T1'"
                ).fetchall()
            finally:
                db.close()
            self.assertEqual(row, ("active", None, 0, before))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0][0], "host_direct_model_waiting_for_event_evidence")

    def test_provider_failure_event_makes_active_call_immediately_claimable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = self._create_direct_call_db(root, deadline_delta=3600)
            changed = hp._mark_active_calls_provider_failed(
                root, "lmstudio", "provider_unreachable", {"endpoint": "refused"}
            )
            self.assertEqual(changed, 1)
            db = sqlite3.connect(path)
            try:
                deadline, outcome = db.execute(
                    "SELECT deadline_at,outcome FROM cnx_direct_model_call WHERE ticket_id='T1'"
                ).fetchone()
                event = db.execute(
                    "SELECT event_type,payload_json FROM ticket_events WHERE ticket_id='T1'"
                ).fetchone()
            finally:
                db.close()
            self.assertLessEqual(datetime.fromisoformat(deadline), datetime.now(timezone.utc))
            self.assertEqual(outcome, "provider-event:provider_unreachable")
            self.assertEqual(event[0], "host_direct_model_provider_failure")
            self.assertEqual(json.loads(event[1])["recoveryAuthority"], "explicit-provider-failure-event")

    def test_durable_success_event_closes_provider_incident(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = self._create_direct_call_db(root, state="ended", outcome="ok")
            opened = hp.recovery_policy.begin_incident(
                root, "lmstudio", "provider_unreachable",
                current=datetime.now(timezone.utc) - timedelta(seconds=1),
            )
            self.assertTrue(opened["incidentOpen"])
            closed = hp._reconcile_stable_success(root, "lmstudio")
            self.assertIsNotNone(closed)
            self.assertFalse(closed["incidentOpen"])
            self.assertFalse(closed["circuitOpen"])
            self.assertTrue(path.exists())

    def test_open_incident_circuit_does_not_claim_or_restart_healthy_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            hp.recovery_policy.begin_incident(root, "lmstudio", "provider_unreachable")
            hp.recovery_policy.record_attempt(root, "lmstudio", success=False, reason="one")
            hp.recovery_policy.record_attempt(root, "lmstudio", success=False, reason="two")
            state = {
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "selectedProvider": "lmstudio",
            }
            healthy = {"healthy": True, "name": "lmstudio"}
            with mock.patch.object(hp.legacy, "load_state", return_value=state), \
                 mock.patch.object(hp, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(hp.providers, "probe", return_value=healthy), \
                 mock.patch.object(hp.v091, "gateway_fast_probe", return_value=True), \
                 mock.patch.object(hp, "_run_base_supervisor", return_value={"result": "base"}) as base, \
                 mock.patch.object(hp.stall, "claim_expired_direct_model_call") as claim:
                result = hp.supervisor_tick(root, execute_safe=True)

            claim.assert_not_called()
            base.assert_called()
            self.assertEqual(result["result"], "provider-recovery-circuit-open")
            self.assertFalse(result["providerRecovery"]["providerRestart"])
            self.assertEqual(result["providerRecovery"]["gate"]["recoveryAttempts"], 2)

    def test_base_reconciliation_cannot_use_legacy_timer_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            observed = []

            def fake_base(root_arg, execute_safe):
                observed.append(hp.stall.claim_expired_direct_model_call(root_arg))
                return {"result": "base"}

            with mock.patch.object(hp, "BASE_SUPERVISOR_TICK", side_effect=fake_base), \
                 mock.patch.object(hp.stall, "claim_expired_direct_model_call", return_value={"ticketId": "timer"}) as original_claim:
                result = hp._run_base_supervisor(root, True, True)

            self.assertEqual(result["result"], "base")
            self.assertEqual(observed, [None])
            self.assertIs(hp.stall.claim_expired_direct_model_call, original_claim)


if __name__ == "__main__":
    unittest.main()
