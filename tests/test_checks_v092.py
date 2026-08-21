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
    def _root(self, directory: str) -> tuple[Path, Path]:
        root = Path(directory) / ".cogent"
        path = root / "host" / "controller.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({
            "schemaVersion": 1,
            "mode": "managed",
            "selectedProvider": "ollama",
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


if __name__ == "__main__":
    unittest.main()
