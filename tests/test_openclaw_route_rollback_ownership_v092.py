import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import openclaw_route_v092 as route


class OpenClawRouteRollbackOwnershipV092Tests(unittest.TestCase):
    def _config(self):
        return {
            "agents": {
                "defaults": {
                    "model": {"primary": "ollama/qwen3.5:9b"},
                    "timeoutSeconds": 600,
                }
            },
            "diagnostics": {"stuckSessionAbortMs": 86400000},
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
            "meta": {"operatorValue": "before"},
        }

    def _write(self, directory):
        path = Path(directory) / "openclaw.json"
        path.write_text(json.dumps(self._config(), indent=2) + "\n", encoding="utf-8")
        return path

    def _simulate_host_native_restore(self, path):
        value = json.loads(path.read_text(encoding="utf-8"))
        value.setdefault("diagnostics", {}).pop("stuckSessionAbortMs", None)
        value["meta"]["operatorValue"] = "changed-during-route-transaction"
        value["plugins"] = {
            "entries": {"cogentnexus-openclaw": {"enabled": False}}
        }
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def _assert_owned_fields_restored_and_unrelated_preserved(self, path):
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            value["agents"]["defaults"]["model"],
            {"primary": "ollama/qwen3.5:9b"},
        )
        self.assertEqual(value["agents"]["defaults"]["timeoutSeconds"], 600)
        self.assertEqual(
            value["models"]["providers"]["lmstudio_local"]["timeoutSeconds"],
            600,
        )
        self.assertEqual(
            value["models"]["providers"]["lmstudio_local"]["models"][0]["compat"],
            {"unsupportedToolSchemaKeywords": ["pattern"]},
        )
        self.assertNotIn("stuckSessionAbortMs", value.get("diagnostics", {}))
        self.assertEqual(
            value["meta"]["operatorValue"],
            "changed-during-route-transaction",
        )
        self.assertFalse(value["plugins"]["entries"]["cogentnexus-openclaw"]["enabled"])

    def test_rollback_does_not_resurrect_v091_watchdog_or_clobber_unrelated_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            config_path = self._write(directory)
            with mock.patch.dict(
                os.environ,
                {"OPENCLAW_CONFIG_PATH": str(config_path)},
                clear=False,
            ), mock.patch.object(
                route,
                "validate_openclaw_config",
                return_value={"ok": True},
            ):
                self.assertTrue(route.begin(root, "lmstudio")["ok"])
                self._simulate_host_native_restore(config_path)
                result = route.rollback(root)

            self.assertTrue(result["ok"])
            self.assertTrue(result["rolledBack"])
            self.assertEqual(result["rollbackMode"], "route-owned-fields")
            self._assert_owned_fields_restored_and_unrelated_preserved(config_path)
            state = json.loads(route.state_path(root).read_text(encoding="utf-8"))
            self.assertIsNone(state["transaction"])
            self.assertFalse(route.rollback_path(root).exists())

    def test_crash_recovery_uses_same_route_owned_merge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            config_path = self._write(directory)
            with mock.patch.dict(
                os.environ,
                {"OPENCLAW_CONFIG_PATH": str(config_path)},
                clear=False,
            ), mock.patch.object(
                route,
                "validate_openclaw_config",
                return_value={"ok": True},
            ):
                self.assertTrue(route.begin(root, "lmstudio")["ok"])
                self._simulate_host_native_restore(config_path)
                recovered = route.recover_pending(root)

            self.assertTrue(recovered["ok"])
            self.assertTrue(recovered["recovered"])
            self.assertEqual(recovered["rollbackMode"], "route-owned-fields")
            self._assert_owned_fields_restored_and_unrelated_preserved(config_path)
            self.assertFalse(route.rollback_path(root).exists())


if __name__ == "__main__":
    unittest.main()
