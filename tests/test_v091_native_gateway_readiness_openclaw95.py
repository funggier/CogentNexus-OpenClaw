from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091_native_ready", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class V091NativeGatewayReadinessTests(unittest.TestCase):
    def setUp(self):
        self.restore = []

    def tearDown(self):
        for obj, name, value in reversed(self.restore):
            setattr(obj, name, value)

    def patch(self, obj, name, value):
        self.restore.append((obj, name, getattr(obj, name)))
        setattr(obj, name, value)

    @staticmethod
    def completed(stdout="", returncode=0, stderr=""):
        return subprocess.CompletedProcess(["stub"], returncode, stdout, stderr)

    def test_wait_native_gateway_ready_retries_transient_openclaw95_cold_start(self):
        statuses = [
            {"healthy": False, "exitCode": 1, "stderr": "ECONNREFUSED"},
            {"healthy": False, "exitCode": 1, "stderr": "ETIMEDOUT"},
            {"healthy": True, "exitCode": 0, "stdout": "Runtime: running\nConnectivity probe: ok"},
        ]
        calls = []

        def gateway_status(timeout=30):
            calls.append(timeout)
            return statuses.pop(0)

        self.patch(cnx.legacy, "gateway_status", gateway_status)
        self.patch(cnx.time, "sleep", lambda _seconds: None)

        result = cnx._wait_native_gateway_ready(timeout_seconds=180, poll_interval_seconds=0)

        self.assertTrue(result["healthy"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(len(calls), 3)
        self.assertGreaterEqual(result["probeTimeoutSeconds"], 1)

    def test_wait_native_gateway_ready_fails_closed_when_budget_expires(self):
        self.patch(cnx.legacy, "gateway_status", lambda timeout=30: {
            "healthy": False,
            "exitCode": 1,
            "stderr": "still unavailable",
        })
        result = cnx._wait_native_gateway_ready(timeout_seconds=0, poll_interval_seconds=0)
        self.assertFalse(result["healthy"])
        self.assertEqual(result["attempts"], 1)
        self.assertIn("lastStatus", result)

    def test_restore_native_gateway_uses_bounded_readiness_wait(self):
        run_calls = []
        self.patch(cnx.legacy, "run", lambda cmd, timeout=120, check=False: (
            run_calls.append((cmd, timeout, check))
            or self.completed(stdout="restart accepted", returncode=0)
        ))
        self.patch(cnx, "_wait_native_gateway_ready", lambda: {
            "healthy": True,
            "attempts": 4,
            "elapsedSeconds": 91.2,
            "probeTimeoutSeconds": 20,
            "lastStatus": {"healthy": True},
        })

        result = cnx._restore_native_gateway()

        self.assertTrue(result["healthy"])
        self.assertEqual(result["readinessAttempts"], 4)
        self.assertEqual(result["readinessElapsedSeconds"], 91.2)
        self.assertEqual(run_calls[0][0][-2:], ["gateway", "restart"])
        self.assertEqual(run_calls[0][1], 180)


if __name__ == "__main__":
    unittest.main()
