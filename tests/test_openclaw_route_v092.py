import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import openclaw_route_v092 as route


class OpenClawRouteV092Tests(unittest.TestCase):
    def _config(self):
        return {
            "agents": {
                "defaults": {
                    "model": {"primary": "ollama/qwen3.5:9b"},
                    "timeoutSeconds": 600,
                }
            },
            "diagnostics": {"stuckSessionAbortMs": 360000},
            "models": {
                "providers": {
                    "lmstudio_local": {
                        "baseUrl": "http://127.0.0.1:1234/v1",
                        "apiKey": "lmstudio-local",
                        "api": "openai-completions",
                        "timeoutSeconds": 600,
                        "models": [{
                            "id": "qwen/qwen3.5-9b",
                            "name": "Qwen3.5 9B via LM Studio",
                            "compat": {"unsupportedToolSchemaKeywords": ["pattern"]},
                        }],
                    }
                }
            },
        }

    def _write_config(self, directory):
        path = Path(directory) / "openclaw.json"
        path.write_text(json.dumps(self._config(), indent=2) + "\n", encoding="utf-8")
        return path

    def test_plan_resolves_existing_lmstudio_catalog_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            config_path = self._write_config(directory)
            before = config_path.read_bytes()
            with mock.patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config_path)}, clear=False):
                result = route.plan(root, "lmstudio")
            self.assertTrue(result["ok"])
            self.assertEqual(result["model"], "lmstudio_local/qwen/qwen3.5-9b")
            self.assertEqual(config_path.read_bytes(), before)
            self.assertFalse(route.state_path(root).exists())

    def test_begin_applies_lmstudio_route_timeouts_and_schema_compat(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            config_path = self._write_config(directory)
            with mock.patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config_path)}, clear=False), \
                 mock.patch.object(route, "validate_openclaw_config", return_value={"ok": True}):
                result = route.begin(root, "lmstudio")
            self.assertTrue(result["ok"])
            value = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(value["agents"]["defaults"]["model"]["primary"], "lmstudio_local/qwen/qwen3.5-9b")
            self.assertEqual(value["models"]["providers"]["lmstudio_local"]["timeoutSeconds"], 1100)
            self.assertEqual(value["diagnostics"]["stuckSessionAbortMs"], 1_140_000)
            self.assertEqual(value["agents"]["defaults"]["timeoutSeconds"], 1200)
            compat = value["models"]["providers"]["lmstudio_local"]["models"][0]["compat"]["unsupportedToolSchemaKeywords"]
            self.assertEqual(compat, ["pattern", "maxLength"])
            self.assertTrue(route.rollback_path(root).is_file())

    def test_rollback_restores_exact_pretransition_config(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            config_path = self._write_config(directory)
            before = config_path.read_bytes()
            with mock.patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config_path)}, clear=False), \
                 mock.patch.object(route, "validate_openclaw_config", return_value={"ok": True}):
                self.assertTrue(route.begin(root, "lmstudio")["ok"])
                result = route.rollback(root)
            self.assertTrue(result["ok"])
            self.assertTrue(result["rolledBack"])
            self.assertEqual(config_path.read_bytes(), before)
            state = json.loads(route.state_path(root).read_text(encoding="utf-8"))
            self.assertIsNone(state["transaction"])

    def test_commit_then_restore_native_restores_pre_cnx_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            config_path = self._write_config(directory)
            baseline = self._config()
            with mock.patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config_path)}, clear=False), \
                 mock.patch.object(route, "validate_openclaw_config", return_value={"ok": True}):
                self.assertTrue(route.begin(root, "lmstudio")["ok"])
                self.assertTrue(route.commit(root)["committed"])
                restored = route.restore_native(root)
            self.assertTrue(restored["ok"])
            self.assertTrue(restored["restored"])
            value = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(value["agents"]["defaults"]["model"], baseline["agents"]["defaults"]["model"])
            self.assertEqual(value["agents"]["defaults"]["timeoutSeconds"], 600)
            self.assertEqual(value["diagnostics"]["stuckSessionAbortMs"], 360000)
            self.assertEqual(value["models"]["providers"]["lmstudio_local"]["timeoutSeconds"], 600)
            self.assertEqual(
                value["models"]["providers"]["lmstudio_local"]["models"][0]["compat"],
                {"unsupportedToolSchemaKeywords": ["pattern"]},
            )
            self.assertFalse(route.state_path(root).exists())

    def test_pending_transaction_is_recovered_before_next_begin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            config_path = self._write_config(directory)
            baseline = config_path.read_bytes()
            with mock.patch.dict(os.environ, {"OPENCLAW_CONFIG_PATH": str(config_path)}, clear=False), \
                 mock.patch.object(route, "validate_openclaw_config", return_value={"ok": True}):
                self.assertTrue(route.begin(root, "lmstudio")["ok"])
                recovered = route.recover_pending(root)
            self.assertTrue(recovered["ok"])
            self.assertTrue(recovered["recovered"])
            self.assertEqual(config_path.read_bytes(), baseline)


if __name__ == "__main__":
    unittest.main()
