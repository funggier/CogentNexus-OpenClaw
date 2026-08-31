import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cnxclaw as cnx


class ProviderTransitionBoundaryV092Tests(unittest.TestCase):
    def test_start_switch_forces_gateway_restart_after_target_provider_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            calls = []

            def fake_run_host(root_arg, args, target=None, timeout=420):
                calls.append((tuple(args), target))
                return {"ok": True, "output": {"command": args[0]}}

            with mock.patch.object(cnx, "run_host", side_effect=fake_run_host):
                host, boundary = cnx._transition_host_runtime(root, "start", "lmstudio", True)

            self.assertTrue(host["ok"])
            self.assertEqual(calls, [(('start',), 'lmstudio'), (('restart',), 'lmstudio')])
            self.assertEqual(boundary["primary"]["output"]["command"], "start")
            self.assertEqual(boundary["gatewayRestart"]["output"]["command"], "restart")

    def test_start_same_route_does_not_restart_gateway(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            calls = []

            def fake_run_host(root_arg, args, target=None, timeout=420):
                calls.append((tuple(args), target))
                return {"ok": True, "output": {"command": args[0]}}

            with mock.patch.object(cnx, "run_host", side_effect=fake_run_host):
                host, boundary = cnx._transition_host_runtime(root, "start", "lmstudio", False)

            self.assertTrue(host["ok"])
            self.assertEqual(calls, [(('start',), 'lmstudio')])
            self.assertIsNone(boundary["gatewayRestart"])

    def test_enable_same_route_still_restarts_gateway_to_load_managed_knobs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            calls = []

            def fake_run_host(root_arg, args, target=None, timeout=420):
                calls.append((tuple(args), target))
                return {"ok": True, "output": {"command": args[0]}}

            with mock.patch.object(cnx, "run_host", side_effect=fake_run_host):
                host, boundary = cnx._transition_host_runtime(root, "enable", "lmstudio", False)

            self.assertTrue(host["ok"])
            self.assertEqual(calls, [(('enable',), 'lmstudio'), (('restart',), 'lmstudio')])
            self.assertEqual(boundary["primary"]["output"]["command"], "enable")
            self.assertEqual(boundary["gatewayRestart"]["output"]["command"], "restart")

    def test_restart_ensures_provider_then_restarts_gateway(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            calls = []

            def fake_run_host(root_arg, args, target=None, timeout=420):
                calls.append((tuple(args), target))
                return {"ok": True, "output": {"command": args[0]}}

            with mock.patch.object(cnx, "run_host", side_effect=fake_run_host):
                host, boundary = cnx._transition_host_runtime(root, "restart", "ollama", False)

            self.assertTrue(host["ok"])
            self.assertEqual(calls, [(('start',), 'ollama'), (('restart',), 'ollama')])
            self.assertEqual(boundary["providerStart"]["output"]["command"], "start")
            self.assertEqual(boundary["gatewayRestart"]["output"]["command"], "restart")

    def test_provider_start_failure_prevents_gateway_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            calls = []

            def fake_run_host(root_arg, args, target=None, timeout=420):
                calls.append((tuple(args), target))
                return {"ok": False, "exitCode": 2}

            with mock.patch.object(cnx, "run_host", side_effect=fake_run_host):
                host, boundary = cnx._transition_host_runtime(root, "restart", "lmstudio", True)

            self.assertFalse(host["ok"])
            self.assertEqual(calls, [(('start',), 'lmstudio')])
            self.assertIsNone(boundary)


if __name__ == "__main__":
    unittest.main()
