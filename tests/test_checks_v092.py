import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import checks_v092 as checks


class ChecksV092Tests(unittest.TestCase):
    def _root(self, directory: str, selected: str = "ollama") -> tuple[Path, Path]:
        root = Path(directory) / ".cogent"
        path = root / "host" / "controller.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({
            "schemaVersion": 1,
            "mode": "managed",
            "selectedProvider": selected,
            "desiredGateway": "running",
            "desiredProvider": "running",
        }), encoding="utf-8")
        return root, path

    def test_explicit_lmstudio_check_is_prospective_not_current_route_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root, state_path = self._root(directory)
            before = state_path.read_bytes()
            planned = {
                "ok": True,
                "provider": "lmstudio",
                "model": "lmstudio_local/qwen/qwen3.5-9b",
                "currentModel": "ollama/qwen3.5:9b",
                "currentProvider": "ollama",
                "mutatesState": False,
            }
            probe = {
                "healthy": True,
                "modelCount": 1,
                "models": ["qwen/qwen3.5-9b"],
            }
            with mock.patch.object(checks.route, "plan", return_value=planned), \
                 mock.patch.object(checks.provider, "probe", return_value=probe), \
                 mock.patch.object(checks.provider, "openclaw_model_status") as current_status:
                entries = checks.check_model(root, "lmstudio")

            current_status.assert_not_called()
            prospective = next(row for row in entries if row["name"] == "OpenClaw prospective model route")
            self.assertEqual(prospective["status"], "PASS")
            self.assertEqual(prospective["details"]["currentProvider"], "ollama")
            self.assertEqual(prospective["details"]["prospectiveModel"], "lmstudio_local/qwen/qwen3.5-9b")
            self.assertEqual(state_path.read_bytes(), before)

    def test_prospective_route_plan_failure_is_fail_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, state_path = self._root(directory)
            before = state_path.read_bytes()
            planned = {"ok": False, "provider": "lmstudio", "error": "route missing"}
            probe = {"healthy": False, "modelCount": 0, "models": []}
            with mock.patch.object(checks.route, "plan", return_value=planned), \
                 mock.patch.object(checks.provider, "probe", return_value=probe):
                entries = checks.check_model(root, "lmstudio")
            prospective = next(row for row in entries if row["name"] == "OpenClaw prospective model route")
            self.assertEqual(prospective["status"], "FAIL")
            self.assertEqual(state_path.read_bytes(), before)

    def test_no_override_keeps_strict_current_route_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self._root(directory)
            current = {"ok": True, "defaultModel": "lmstudio_local/qwen/qwen3.5-9b"}
            probe = {"healthy": True, "modelCount": 1, "models": ["qwen3.5:9b"]}
            with mock.patch.object(checks.provider, "openclaw_model_status", return_value=current), \
                 mock.patch.object(checks.provider, "probe", return_value=probe):
                entries = checks.check_model(root, None)
            routing = next(row for row in entries if row["name"] == "OpenClaw model routing")
            self.assertEqual(routing["status"], "FAIL")

    def test_recovery_check_reports_incident_and_adapter_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, state_path = self._root(directory, selected="lmstudio")
            before = state_path.read_bytes()
            gate = {
                "provider": "lmstudio",
                "allowed": True,
                "circuitOpen": False,
                "incidentOpen": True,
                "incidentId": "lmstudio:4",
                "classification": "provider_unreachable",
                "recoveryAttempts": 1,
                "maximumRecoveriesPerIncident": 2,
                "lastEvent": {"type": "automatic_recovery_attempted"},
            }
            with mock.patch.object(checks.base, "check_recovery", return_value=[]), \
                 mock.patch.object(checks.recovery_policy, "gate", return_value=gate), \
                 mock.patch.object(
                     checks.provider_events,
                     "adapter_status",
                     return_value={"provider": "lmstudio", "running": True, "pid": 4321},
                 ):
                entries = checks.check_recovery(root)

            incident = next(row for row in entries if row["name"] == "Provider recovery incident")
            adapter = next(row for row in entries if row["name"] == "Provider event adapter")
            self.assertEqual(incident["status"], "WARN")
            self.assertEqual(incident["details"]["incidentId"], "lmstudio:4")
            self.assertEqual(incident["details"]["recoveryAttempts"], 1)
            self.assertEqual(adapter["status"], "PASS")
            self.assertTrue(adapter["details"]["running"])
            self.assertEqual(state_path.read_bytes(), before)

    def test_recovery_check_warns_when_lmstudio_adapter_expected_but_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self._root(directory, selected="lmstudio")
            gate = {
                "provider": "lmstudio",
                "allowed": False,
                "circuitOpen": False,
                "incidentOpen": False,
                "incidentId": None,
                "classification": None,
                "recoveryAttempts": 0,
                "maximumRecoveriesPerIncident": 2,
                "lastEvent": None,
            }
            with mock.patch.object(checks.base, "check_recovery", return_value=[]), \
                 mock.patch.object(checks.recovery_policy, "gate", return_value=gate), \
                 mock.patch.object(
                     checks.provider_events,
                     "adapter_status",
                     return_value={"provider": "lmstudio", "running": False, "pid": None},
                 ):
                entries = checks.check_recovery(root)
            adapter = next(row for row in entries if row["name"] == "Provider event adapter")
            self.assertEqual(adapter["status"], "WARN")
            self.assertTrue(adapter["details"]["expected"])


if __name__ == "__main__":
    unittest.main()
