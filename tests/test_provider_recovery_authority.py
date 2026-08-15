from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]

def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module

runtime = load("cnx_runtime_provider_test", ROOT / "skills/cogentnexus/scripts/runtime.py")
host = load("cnx_host_provider_test", ROOT / "skills/cogentnexus/scripts/host.py")

class ProviderRecoveryAuthorityTests(unittest.TestCase):
    def config(self):
        return runtime.deep_merge(runtime.DEFAULT_CONFIG, {"supervisor": {"allowOllamaStart": False}})

    def test_explicit_provider_start_bypasses_only_autonomous_fence(self):
        config = self.config()
        with mock.patch.object(runtime.os, "name", "nt"), mock.patch.object(
            runtime, "start_ollama_windows", return_value={"ok": True, "command": ["ollama", "serve"]}
        ) as starter:
            result = runtime.recover_component("ollama", config, explicit_authority=True)
        self.assertTrue(result["ok"])
        starter.assert_called_once_with()

    def test_autonomous_provider_recovery_stays_fenced_by_default(self):
        config = self.config()
        with mock.patch.object(runtime.os, "name", "nt"), mock.patch.object(runtime, "start_ollama_windows") as starter:
            result = runtime.recover_component("ollama", config)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "no authorized recovery adapter")
        starter.assert_not_called()

    def test_gateway_only_readiness_does_not_require_ollama(self):
        config = self.config()
        with mock.patch.object(runtime, "gateway_probe", return_value={"healthy": True}), mock.patch.object(
            runtime, "ollama_probe", return_value={"healthy": False}
        ):
            _, _, gateway_only = runtime.wait_for_runtime_health(config, timeout_seconds=0, require_ollama=False)
            _, _, provider_required = runtime.wait_for_runtime_health(config, timeout_seconds=0, require_ollama=True)
        self.assertTrue(gateway_only)
        self.assertFalse(provider_required)

    def test_host_desired_provider_reconciles_with_explicit_lifecycle_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            host.save_state(root, {
                "schemaVersion": 1, "mode": "managed", "desiredGateway": "running",
                "desiredProvider": "running", "generation": 3
            })
            calls = []
            def fake_runtime(_root, *args, **kwargs):
                calls.append(args)
                if args[:2] == ("lifecycle", "status"):
                    return subprocess.CompletedProcess(args, 0, json.dumps({
                        "gateway": {"healthy": True}, "ollama": {"healthy": False}
                    }), "")
                if args[:2] == ("lifecycle", "start"):
                    return subprocess.CompletedProcess(args, 0, json.dumps({"started": True}), "")
                return subprocess.CompletedProcess(args, 0, json.dumps({"status": "healthy"}), "")
            with mock.patch.object(host, "gateway_status", return_value={"healthy": True}), mock.patch.object(host, "runtime", side_effect=fake_runtime):
                result = host.supervisor_tick(root, True)
            self.assertIn(("lifecycle", "start", "--provider"), calls)
            self.assertTrue(result["reconcile"]["providerRequired"])
            self.assertEqual(result["reconcile"]["exitCode"], 0)

if __name__ == "__main__":
    unittest.main()
