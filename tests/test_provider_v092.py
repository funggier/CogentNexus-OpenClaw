import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import checks
import cnx
import provider


class ProviderV092Tests(unittest.TestCase):
    def test_provider_aliases(self):
        self.assertEqual(provider.normalize_provider("ollama"), "ollama")
        self.assertEqual(provider.normalize_provider("LM-Studio"), "lmstudio")
        self.assertEqual(provider.normalize_provider("lm"), "lmstudio")
        with self.assertRaises(ValueError):
            provider.normalize_provider("unknown")

    def test_lmstudio_gui_without_lms_is_installed_but_not_controllable(self):
        with mock.patch.object(provider, "find_lms_cli", return_value=None), mock.patch.object(provider, "find_lmstudio_gui", return_value="/fake/LM Studio.exe"):
            value = provider.detect("lmstudio")
        self.assertTrue(value["installed"])
        self.assertFalse(value["controllable"])

    def test_transition_target_wins_over_previous_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "ollama",
                "providerTransition": {"from": "ollama", "to": "lmstudio"},
            }), encoding="utf-8")
            target, source = cnx.resolve_target(root, None)
            self.assertEqual((target, source), ("lmstudio", "resume-transition"))

    def test_commit_provider_is_durable_and_clears_transition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "mode": "managed",
                "generation": 4,
                "providerTransition": {"from": "ollama", "to": "lmstudio"},
            }), encoding="utf-8")
            cnx.commit_provider(root, "lmstudio", "explicit")
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value["selectedProvider"], "lmstudio")
            self.assertIsNone(value["providerTransition"])
            self.assertEqual(value["desiredProvider"], "running")
            self.assertEqual(value["providerSelection"]["selectionSource"], "explicit")

    def test_component_check_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            original = {
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "ollama",
                "desiredGateway": "running",
                "desiredProvider": "running",
            }
            path.write_text(json.dumps(original, sort_keys=True), encoding="utf-8")
            before = path.read_bytes()
            fake = {
                "name": "ollama", "installed": True, "controllable": True,
                "cli": "/fake/ollama", "application": None,
                "endpoint": "http://127.0.0.1:11434", "reachable": True,
                "healthy": True, "ready": True, "models": ["qwen"],
                "modelCount": 1, "evidence": {},
            }
            missing = {
                "name": "lmstudio", "installed": False, "controllable": False,
                "cli": None, "application": None, "endpoint": "http://127.0.0.1:1234",
                "reachable": False, "healthy": False, "ready": False,
                "models": [], "modelCount": 0, "evidence": {},
            }
            with mock.patch.object(provider, "inventory", return_value={"ollama": fake, "lmstudio": missing}):
                report = checks.component_check(root, "provider")
            self.assertTrue(report["readOnly"])
            self.assertFalse(report["stateChanged"])
            self.assertEqual(path.read_bytes(), before)

    def test_preflight_rejects_missing_provider_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"schemaVersion": 1, "mode": "passthrough"}), encoding="utf-8")
            before = path.read_bytes()
            missing = {
                "name": "lmstudio", "installed": False, "controllable": False,
                "healthy": False, "reachable": False,
            }
            with mock.patch.object(checks, "check_cogentnexus", return_value=[]), mock.patch.object(checks, "check_openclaw", return_value=[]), mock.patch.object(checks, "check_config", return_value=[]), mock.patch.object(provider, "probe", return_value=missing):
                report = checks.preflight_start(root, "lmstudio")
            self.assertEqual(report["verdict"], "NOT_READY")
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
