import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import openclaw_runtime_boundary_v092 as boundary


class OpenClawRuntimeBoundaryV092Tests(unittest.TestCase):
    @staticmethod
    def completed(args, code=0, stdout="", stderr=""):
        return subprocess.CompletedProcess(args=args, returncode=code, stdout=stdout, stderr=stderr)

    def test_restart_then_healthy_status_passes(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            if args[-2:] == ["gateway", "status"]:
                return self.completed(args, stdout="Runtime: running\nConnectivity probe: ok\n")
            return self.completed(args)

        with mock.patch.object(boundary, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(boundary.subprocess, "run", side_effect=fake_run):
            result = boundary.activate_current_config()

        self.assertTrue(result["ok"])
        self.assertEqual(calls[0], ["openclaw", "gateway", "restart"])
        self.assertEqual(calls[-1], ["openclaw", "gateway", "status"])
        self.assertIsNone(result["fallbackStart"])

    def test_restart_failure_uses_start_fallback(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            if args[-2:] == ["gateway", "restart"]:
                return self.completed(args, code=1, stderr="restart failed")
            if args[-2:] == ["gateway", "status"]:
                return self.completed(args, stdout="Runtime: running\nConnectivity probe: ok\n")
            return self.completed(args)

        with mock.patch.object(boundary, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(boundary.subprocess, "run", side_effect=fake_run):
            result = boundary.activate_current_config()

        self.assertTrue(result["ok"])
        self.assertIn(["openclaw", "gateway", "start"], calls)
        self.assertIsNotNone(result["fallbackStart"])

    def test_unhealthy_post_boundary_status_fails_closed(self):
        def fake_run(args, **kwargs):
            if args[-2:] == ["gateway", "status"]:
                return self.completed(args, stdout="Runtime: stopped\nConnectivity probe: failed\n")
            return self.completed(args)

        with mock.patch.object(boundary, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(boundary.subprocess, "run", side_effect=fake_run):
            result = boundary.activate_current_config()

        self.assertFalse(result["ok"])
        self.assertEqual(result["phase"], "gateway-verification")

    def test_missing_openclaw_cli_fails_closed(self):
        with mock.patch.object(boundary, "openclaw_executable", return_value=None):
            result = boundary.activate_current_config()
        self.assertFalse(result["ok"])
        self.assertIn("unavailable", result["error"])


if __name__ == "__main__":
    unittest.main()
