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

    def test_lifecycle_start_delegates_without_provider_or_adapter_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            delegated = subprocess.CompletedProcess(
                args=["lifecycle", "start"], returncode=0,
                stdout=json.dumps({"started": True}), stderr=""
            )

            with mock.patch.object(self.host, "BASE_PROVIDER_RUNTIME", return_value=delegated) as runtime, \
                 mock.patch.object(self.host.base, "_state_provider") as state_provider, \
                 mock.patch.object(self.host.base, "_set_legacy_ollama_mode") as ollama_mode, \
                 mock.patch.object(self.host.providers, "start") as provider_start, \
                 mock.patch.object(self.host.provider_events, "ensure_adapter") as adapter_start, \
                 mock.patch.object(self.host.base, "ORIGINAL_RUNTIME") as original_runtime:
                result = self.host.provider_event_aware_runtime(
                    root, "lifecycle", "start", "--provider", timeout=30, check=True
                )

            self.assertIs(result, delegated)
            runtime.assert_called_once_with(
                root, "lifecycle", "start", "--provider", timeout=30, check=True
            )
            state_provider.assert_not_called()
            ollama_mode.assert_not_called()
            provider_start.assert_not_called()
            adapter_start.assert_not_called()
            original_runtime.assert_not_called()

    def test_failed_gateway_start_does_not_create_or_rollback_provider_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            failed = subprocess.CompletedProcess(
                args=["lifecycle", "start"], returncode=1,
                stdout=json.dumps({"result": "error"}), stderr="gateway failed"
            )
            with mock.patch.object(self.host, "BASE_PROVIDER_RUNTIME", return_value=failed) as runtime, \
                 mock.patch.object(self.host.base, "_state_provider") as state_provider, \
                 mock.patch.object(self.host.base, "_set_legacy_ollama_mode") as ollama_mode, \
                 mock.patch.object(self.host.providers, "start") as provider_start, \
                 mock.patch.object(self.host.provider_events, "ensure_adapter") as adapter_start, \
                 mock.patch.object(self.host.provider_events, "stop_adapter") as adapter_stop, \
                 mock.patch.object(self.host.base, "ORIGINAL_RUNTIME") as original_runtime:
                result = self.host.provider_event_aware_runtime(
                    root, "lifecycle", "start", "--provider", timeout=30, check=False
                )

            self.assertIs(result, failed)
            runtime.assert_called_once_with(
                root, "lifecycle", "start", "--provider", timeout=30, check=False
            )
            state_provider.assert_not_called()
            ollama_mode.assert_not_called()
            provider_start.assert_not_called()
            adapter_start.assert_not_called()
            adapter_stop.assert_not_called()
            original_runtime.assert_not_called()

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

    def test_restart_delegates_without_provider_state_or_adapter_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            restarted = {"result": "restarted"}

            with mock.patch.object(self.host, "ORIGINAL_RESTART_MANAGED", return_value=restarted) as gateway_restart, \
                 mock.patch.object(self.host.base, "_state_provider") as state_provider, \
                 mock.patch.object(self.host.legacy, "transition") as transition, \
                 mock.patch.object(self.host.providers, "start") as provider_start, \
                 mock.patch.object(self.host.provider_events, "ensure_adapter") as adapter_start:
                result = self.host.restart_managed(root)

            self.assertIs(result, restarted)
            gateway_restart.assert_called_once_with(root)
            state_provider.assert_not_called()
            transition.assert_not_called()
            provider_start.assert_not_called()
            adapter_start.assert_not_called()


if __name__ == "__main__":
    unittest.main()
