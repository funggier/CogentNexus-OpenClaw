import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import checks
import cnxclaw as cnx
import provider


class ProviderV092Tests(unittest.TestCase):
    def test_provider_aliases(self):
        self.assertEqual(provider.normalize_provider("ollama"), "ollama")
        self.assertEqual(provider.normalize_provider("LM-Studio"), "lmstudio")
        self.assertEqual(provider.normalize_provider("lm"), "lmstudio")
        with self.assertRaises(ValueError):
            provider.normalize_provider("unknown")

    def test_lmstudio_gui_without_lms_is_installed_but_not_controllable(self):
        with mock.patch.object(provider, "find_lms_cli", return_value=None), \
             mock.patch.object(provider, "find_lmstudio_gui", return_value="/fake/LM Studio.exe"):
            value = provider.detect("lmstudio")
        self.assertTrue(value["installed"])
        self.assertFalse(value["controllable"])

    def test_transition_target_wins_over_previous_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
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
            root = Path(directory) / ".cogentnexus-openclaw"
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
            root = Path(directory) / ".cogentnexus-openclaw"
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
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"schemaVersion": 1, "mode": "passthrough"}), encoding="utf-8")
            before = path.read_bytes()
            missing = {
                "name": "lmstudio", "installed": False, "controllable": False,
                "healthy": False, "reachable": False,
            }
            with mock.patch.object(checks, "check_cogentnexus", return_value=[]), \
                 mock.patch.object(checks, "check_openclaw", return_value=[]), \
                 mock.patch.object(checks, "check_config", return_value=[]), \
                 mock.patch.object(provider, "probe", return_value=missing):
                report = checks.preflight_start(root, "lmstudio")
            self.assertEqual(report["verdict"], "NOT_READY")
            self.assertEqual(path.read_bytes(), before)

    def test_route_preflight_failure_is_zero_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "ollama",
                "generation": 7,
            }, sort_keys=True), encoding="utf-8")
            before = path.read_bytes()
            ready = {"verdict": "READY", "exitCode": 0, "checks": []}
            with mock.patch.object(cnx.checks, "preflight_start", return_value=ready), \
                 mock.patch.object(cnx.openclaw_route, "plan", return_value={"ok": False, "error": "no route"}), \
                 mock.patch.object(cnx, "run_host") as run_host:
                code, result = cnx.provider_transition(root, "start", "lmstudio")
            self.assertEqual(code, 2)
            self.assertEqual(result["phase"], "route-preflight")
            self.assertFalse(result["stateChanged"])
            self.assertEqual(path.read_bytes(), before)
            run_host.assert_not_called()

    def test_host_failure_rolls_back_route_but_preserves_transition_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "ollama",
                "generation": 2,
            }), encoding="utf-8")
            ready = {"verdict": "READY", "exitCode": 0, "checks": []}
            route_plan = {
                "ok": True,
                "provider": "lmstudio",
                "model": "lmstudio_local/qwen/qwen3.5-9b",
                "currentProvider": "ollama",
                "currentModel": "ollama/qwen3.5:9b",
            }
            with mock.patch.object(cnx.checks, "preflight_start", return_value=ready), \
                 mock.patch.object(cnx.openclaw_route, "plan", return_value=route_plan), \
                 mock.patch.object(cnx.openclaw_route, "begin", return_value={"ok": True}), \
                 mock.patch.object(cnx.openclaw_route, "rollback", return_value={"ok": True, "rolledBack": True}) as rollback, \
                 mock.patch.object(cnx, "run_host", return_value={"ok": False, "exitCode": 1}):
                code, result = cnx.provider_transition(root, "start", "lmstudio")

            self.assertEqual(code, 1)
            self.assertEqual(result["phase"], "host-transition")
            rollback.assert_called_once_with(root)
            state = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(state["selectedProvider"], "ollama")
            self.assertEqual(state["providerTransition"]["from"], "ollama")
            self.assertEqual(state["providerTransition"]["to"], "lmstudio")
            self.assertFalse(result["selectionCommitted"])

    def test_success_commits_route_before_provider_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "host" / "controller.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "mode": "managed",
                "selectedProvider": "ollama",
                "generation": 1,
            }), encoding="utf-8")
            ready = {"verdict": "READY", "exitCode": 0, "checks": []}
            before_plan = {
                "ok": True,
                "provider": "lmstudio",
                "model": "lmstudio_local/qwen/qwen3.5-9b",
                "currentProvider": "ollama",
                "currentModel": "ollama/qwen3.5:9b",
            }
            after_plan = {
                "ok": True,
                "provider": "lmstudio",
                "model": "lmstudio_local/qwen/qwen3.5-9b",
                "currentProvider": "lmstudio",
                "currentModel": "lmstudio_local/qwen/qwen3.5-9b",
            }
            healthy = {"healthy": True, "name": "lmstudio"}
            order = []

            def route_commit(root_arg):
                order.append("route")
                return {"ok": True, "committed": True, "provider": "lmstudio", "model": after_plan["model"]}

            def provider_commit(root_arg, target, source):
                order.append("provider")
                return {
                    "selectedProvider": target,
                    "providerTransition": None,
                    "providerSelection": {"selectionSource": source},
                }

            with mock.patch.object(cnx.checks, "preflight_start", return_value=ready), \
                 mock.patch.object(cnx.openclaw_route, "plan", side_effect=[before_plan, after_plan]), \
                 mock.patch.object(cnx.openclaw_route, "begin", return_value={"ok": True}), \
                 mock.patch.object(cnx.openclaw_route, "commit", side_effect=route_commit), \
                 mock.patch.object(cnx, "run_host", return_value={"ok": True, "output": {"started": True}}), \
                 mock.patch.object(cnx.provider, "probe", return_value=healthy), \
                 mock.patch.object(cnx.checks, "check_gateway", return_value=[{"status": "PASS"}]), \
                 mock.patch.object(cnx, "commit_provider", side_effect=provider_commit):
                code, result = cnx.provider_transition(root, "start", "lmstudio")

            self.assertEqual(code, 0)
            self.assertEqual(order, ["route", "provider"])
            self.assertEqual(result["provider"], "lmstudio")
            self.assertEqual(result["route"]["model"], after_plan["model"])


if __name__ == "__main__":
    unittest.main()
