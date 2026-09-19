from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import openclaw_runtime_boundary_v092 as boundary


class OpenClawRuntimeBoundaryOpenClaw95Tests(unittest.TestCase):
    @staticmethod
    def status(*, healthy: bool, marker: str = ""):
        if healthy:
            return {
                "ok": True,
                "exitCode": 0,
                "stdout": "Runtime: running\nConnectivity probe: ok",
                "stderr": "",
            }
        return {
            "ok": True,
            "exitCode": 0,
            "stdout": "Runtime: running\nListening: 127.0.0.1:18789",
            "stderr": marker or "Connectivity probe: timed out before reaching Gateway",
        }

    def test_wait_gateway_ready_retries_transient_cold_start_until_healthy(self):
        statuses = [
            self.status(healthy=False, marker="ECONNREFUSED"),
            self.status(healthy=False, marker="ETIMEDOUT"),
            self.status(healthy=True),
        ]
        calls = []

        def fake_run(argv, timeout):
            calls.append((list(argv), timeout))
            return statuses.pop(0)

        with mock.patch.object(boundary, "_run", side_effect=fake_run), \
             mock.patch.object(boundary.time, "sleep", return_value=None):
            result = boundary._wait_gateway_ready(
                "openclaw",
                timeout_seconds=180,
                poll_interval_seconds=0,
            )

        self.assertTrue(result["healthy"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(call[0][-2:] == ["gateway", "status"] for call in calls))
        self.assertTrue(all(call[1] <= 20 for call in calls))

    def test_wait_gateway_ready_fails_closed_after_zero_budget(self):
        with mock.patch.object(boundary, "_run", return_value=self.status(healthy=False)):
            result = boundary._wait_gateway_ready(
                "openclaw",
                timeout_seconds=0,
                poll_interval_seconds=0,
            )

        self.assertFalse(result["healthy"])
        self.assertEqual(result["attempts"], 1)
        self.assertIn("lastStatus", result)

    def test_activate_current_config_surfaces_bounded_readiness_evidence(self):
        restart = {
            "ok": True,
            "exitCode": 0,
            "stdout": "Restarted Scheduled Task: OpenClaw Gateway",
            "stderr": "",
            "command": ["openclaw", "gateway", "restart"],
        }
        ready = {
            "healthy": True,
            "attempts": 5,
            "elapsedSeconds": 78.593,
            "probeTimeoutSeconds": 20,
            "lastStatus": self.status(healthy=True),
        }

        with mock.patch.object(boundary, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(boundary, "_run", return_value=restart), \
             mock.patch.object(boundary, "_wait_gateway_ready", return_value=ready):
            result = boundary.activate_current_config()

        self.assertTrue(result["ok"])
        self.assertEqual(result["phase"], "verified")
        self.assertEqual(result["readinessAttempts"], 5)
        self.assertEqual(result["readinessElapsedSeconds"], 78.593)
        self.assertEqual(result["status"], ready["lastStatus"])


if __name__ == "__main__":
    unittest.main()
