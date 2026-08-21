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
            payload = json.loads(result.stdout)
            self.assertEqual(payload["provider"], "lmstudio")

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

    def _create_direct_call_db(self, root: Path) -> Path:
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
                  outcome TEXT,
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
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at) "
                "VALUES (?,?,?,?,?,?,?)",
                ("T1", "R1", "agent:main:test", "accepted", 0, None, None),
            )
            db.execute(
                "INSERT INTO cnx_direct_model_call("
                "ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,outcome,recovery_attempt_count,updated_at"
                ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "T1", "R1", "C1", "active", "lmstudio_local", "qwen/qwen3.5-9b",
                    (now - timedelta(minutes=10)).isoformat(),
                    (now - timedelta(seconds=1)).isoformat(),
                    None, 0, now.isoformat(),
                ),
            )
            db.commit()
        finally:
            db.close()
        return path

    def test_lmstudio_long_running_grace_does_not_consume_recovery_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = self._create_direct_call_db(root)
            result = hp._defer_lmstudio_long_running_call(root, 600)
            self.assertIsNotNone(result)
            self.assertEqual(result["classification"], "cold_model_long_running")
            self.assertFalse(result["recoveryEligible"])
            self.assertFalse(result["providerRestart"])

            db = sqlite3.connect(path)
            try:
                row = db.execute(
                    "SELECT state,outcome,recovery_attempt_count,deadline_at FROM cnx_direct_model_call WHERE ticket_id='T1'"
                ).fetchone()
                event = db.execute(
                    "SELECT event_type,payload_json FROM ticket_events WHERE ticket_id='T1'"
                ).fetchone()
            finally:
                db.close()

            self.assertEqual(row[0], "active")
            self.assertEqual(row[1], "cold-model-long-running-grace:600s")
            self.assertEqual(row[2], 0)
            self.assertGreater(
                datetime.fromisoformat(row[3]),
                datetime.now(timezone.utc) + timedelta(minutes=9),
            )
            self.assertEqual(event[0], "host_direct_model_long_running_grace")
            payload = json.loads(event[1])
            self.assertEqual(payload["classification"], "cold_model_long_running")
            self.assertIsNone(hp._defer_lmstudio_long_running_call(root, 600))

    def test_open_circuit_does_not_claim_or_restart_healthy_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            state = {
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "selectedProvider": "lmstudio",
            }
            healthy = {"healthy": True, "name": "lmstudio"}
            gate = {
                "provider": "lmstudio",
                "allowed": False,
                "circuitOpen": True,
                "recoveriesLastHour": 2,
                "maximumRecoveriesPerHour": 2,
                "cooldownSeconds": 900,
                "longRunningGraceSeconds": 600,
            }
            with mock.patch.object(hp.legacy, "load_state", return_value=state), \
                 mock.patch.object(hp, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(hp.providers, "probe", return_value=healthy), \
                 mock.patch.object(hp.v091, "gateway_fast_probe", return_value=True), \
                 mock.patch.object(hp, "_defer_lmstudio_long_running_call", return_value=None), \
                 mock.patch.object(hp.recovery_policy, "gate", return_value=gate), \
                 mock.patch.object(hp, "_run_base_supervisor", return_value={"result": "base"}) as base, \
                 mock.patch.object(hp.stall, "claim_expired_direct_model_call") as claim:
                result = hp.supervisor_tick(root, execute_safe=True)

            claim.assert_not_called()
            base.assert_called()
            self.assertEqual(result["result"], "provider-recovery-circuit-open")
            self.assertFalse(result["providerRecovery"]["providerRestart"])


if __name__ == "__main__":
    unittest.main()
