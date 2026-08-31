import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as provider_base


class HostV092ProviderEventBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.saved_runtime = provider_base.legacy.runtime
        self.saved_enable = provider_base.legacy.enable
        self.saved_restart = provider_base.legacy.restart_managed
        self.saved_progress_for_call = provider_base._progress_for_call
        sys.modules.pop("host_v092", None)
        self.host = importlib.import_module("host_v092")

    def tearDown(self):
        provider_base.legacy.runtime = self.saved_runtime
        provider_base.legacy.enable = self.saved_enable
        provider_base.legacy.restart_managed = self.saved_restart
        provider_base._progress_for_call = self.saved_progress_for_call
        sys.modules.pop("host_v092", None)

    def test_lifecycle_start_attaches_adapter_before_gateway_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            order = []

            def provider_start(name, timeout=45):
                order.append("provider")
                return {"ok": True, "provider": name}

            def adapter_start(root_arg, name):
                order.append("adapter")
                return {"provider": name, "running": True, "pid": 123}

            def gateway_start(root_arg, *args, timeout=180, check=True):
                order.append("gateway")
                return subprocess.CompletedProcess(
                    args=list(args), returncode=0, stdout=json.dumps({"started": True}), stderr=""
                )

            with mock.patch.object(self.host.base, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(self.host.base, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(self.host.providers, "start", side_effect=provider_start), \
                 mock.patch.object(self.host.provider_events, "ensure_adapter", side_effect=adapter_start), \
                 mock.patch.object(self.host.base, "ORIGINAL_RUNTIME", side_effect=gateway_start):
                result = self.host.provider_event_aware_runtime(
                    root, "lifecycle", "start", "--provider", timeout=30, check=True
                )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(order, ["provider", "adapter", "gateway"])
            payload = json.loads(result.stdout)
            self.assertTrue(payload["providerEventAdapter"]["running"])
            self.assertIsNone(payload["providerEventAdapterRollback"])

    def test_failed_gateway_start_rolls_back_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            failed = subprocess.CompletedProcess(
                args=["lifecycle", "start"], returncode=1, stdout=json.dumps({"result": "error"}), stderr="gateway failed"
            )
            with mock.patch.object(self.host.base, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(self.host.base, "_set_legacy_ollama_mode", return_value={"changed": False}), \
                 mock.patch.object(self.host.providers, "start", return_value={"ok": True}), \
                 mock.patch.object(self.host.provider_events, "ensure_adapter", return_value={"running": True}), \
                 mock.patch.object(self.host.provider_events, "stop_adapter", return_value={"stopped": [{"provider": "lmstudio"}]}) as stop, \
                 mock.patch.object(self.host.base, "ORIGINAL_RUNTIME", return_value=failed):
                result = self.host.provider_event_aware_runtime(
                    root, "lifecycle", "start", "--provider", timeout=30, check=False
                )

            self.assertEqual(result.returncode, 1)
            stop.assert_called_once_with(root, "lmstudio")
            payload = json.loads(result.stdout)
            self.assertIsNotNone(payload["providerEventAdapterRollback"])

    def test_failed_transactional_enable_stops_all_provider_adapters(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(
                self.host, "ORIGINAL_ENABLE_MANAGED", side_effect=RuntimeError("enable failed")
            ), mock.patch.object(
                self.host.provider_events, "stop_adapter", return_value={"stopped": []}
            ) as stop:
                with self.assertRaisesRegex(RuntimeError, "enable failed"):
                    self.host.enable_managed(root)
            stop.assert_called_once_with(root)

    def test_watcher_cleanup_error_does_not_mask_enable_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(
                self.host, "ORIGINAL_ENABLE_MANAGED", side_effect=RuntimeError("original enable failure")
            ), mock.patch.object(
                self.host.provider_events, "stop_adapter", side_effect=RuntimeError("cleanup failure")
            ):
                with self.assertRaisesRegex(RuntimeError, "original enable failure"):
                    self.host.enable_managed(root)

    def test_progress_timestamp_normalizes_z_and_offset_forms(self):
        progress = {
            "at": "2026-08-21T13:00:00+00:00",
            "type": "prompt_progress",
            "evidence": {"percent": 52.0},
        }
        with mock.patch.object(self.host.provider_events, "latest_progress", return_value=progress):
            same_in_z = self.host.progress_for_call(
                Path("."), "lmstudio", "2026-08-21T13:00:00.000Z"
            )
            same_in_bangkok = self.host.progress_for_call(
                Path("."), "lmstudio", "2026-08-21T20:00:00+07:00"
            )
        self.assertEqual(same_in_z, progress)
        self.assertEqual(same_in_bangkok, progress)

    def test_progress_before_call_start_is_rejected_after_normalization(self):
        progress = {
            "at": "2026-08-21T12:59:59.999+00:00",
            "type": "prompt_progress",
            "evidence": {"percent": 87.0},
        }
        with mock.patch.object(self.host.provider_events, "latest_progress", return_value=progress):
            self.assertIsNone(
                self.host.progress_for_call(Path("."), "lmstudio", "2026-08-21T13:00:00Z")
            )

    def test_restart_attaches_adapter_before_gateway_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            order = []

            def provider_start(name, timeout=45):
                order.append("provider")
                return {"ok": True, "provider": name}

            def adapter_start(root_arg, name):
                order.append("adapter")
                return {"provider": name, "running": True, "pid": 456}

            def gateway_restart(root_arg):
                order.append("gateway")
                return {"result": "restarted"}

            with mock.patch.object(self.host.base, "_state_provider", return_value="lmstudio"), \
                 mock.patch.object(self.host.legacy, "transition"), \
                 mock.patch.object(self.host.providers, "start", side_effect=provider_start), \
                 mock.patch.object(self.host.provider_events, "ensure_adapter", side_effect=adapter_start), \
                 mock.patch.object(self.host, "ORIGINAL_RESTART_MANAGED", side_effect=gateway_restart):
                result = self.host.restart_managed(root)

            self.assertEqual(order, ["provider", "adapter", "gateway"])
            self.assertTrue(result["providerEventAdapter"]["running"])


if __name__ == "__main__":
    unittest.main()
