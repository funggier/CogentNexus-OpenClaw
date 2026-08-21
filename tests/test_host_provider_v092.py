import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


class HostProviderV092Tests(unittest.TestCase):
    def test_start_provider_boundary_strips_legacy_provider_flag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            calls = []

            def fake_runtime(root_arg, *args, timeout=180, check=True):
                calls.append((root_arg, args, timeout, check))
                return subprocess.CompletedProcess(args=list(args), returncode=0, stdout=json.dumps({"started": True}), stderr="")

            healthy = {"healthy": True, "installed": True, "name": "lmstudio"}
            with mock.patch.object(hp, "ORIGINAL_RUNTIME", side_effect=fake_runtime), \
                 mock.patch.object(hp, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": True}), \
                 mock.patch.object(hp.providers, "start", return_value={"ok": True, "after": healthy}):
                result = hp.provider_aware_runtime(root, "lifecycle", "start", "--provider", timeout=30, check=True)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(calls[0][1], ("lifecycle", "start"))
            payload = json.loads(result.stdout)
            self.assertEqual(payload["provider"], "lmstudio")

    def test_stop_quiesces_gateway_before_selected_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            order = []

            def fake_runtime(root_arg, *args, timeout=180, check=True):
                order.append("gateway-stop")
                return subprocess.CompletedProcess(args=list(args), returncode=0, stdout=json.dumps({"stopped": True}), stderr="")

            def fake_stop(name, timeout=30):
                order.append(f"provider-stop:{name}")
                return {"ok": True}

            with mock.patch.object(hp, "ORIGINAL_RUNTIME", side_effect=fake_runtime), \
                 mock.patch.object(hp, "_state_provider", return_value="ollama"), \
                 mock.patch.object(hp, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(hp.providers, "stop", side_effect=fake_stop):
                result = hp.provider_aware_runtime(root, "lifecycle", "stop", "--provider", timeout=30, check=True)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(order, ["gateway-stop", "provider-stop:ollama"])

    def test_missing_selection_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            root.mkdir()
            with mock.patch.object(hp, "_state_provider", return_value=None):
                result = hp.provider_aware_runtime(root, "lifecycle", "start", "--provider", timeout=30, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("provider selection required", result.stdout)


if __name__ == "__main__":
    unittest.main()
