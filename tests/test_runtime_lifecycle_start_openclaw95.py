from __future__ import annotations

import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "runtime.py"
SPEC = importlib.util.spec_from_file_location("cnx436_runtime", SCRIPT)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class OpenClaw95LifecycleStartReadinessTests(unittest.TestCase):
    def config(self):
        return runtime.deep_merge(
            runtime.DEFAULT_CONFIG,
            {"supervisor": {"commandTimeoutSeconds": 30, "verifyDelaySeconds": 0}},
        )

    def _args(self, root: Path):
        return argparse.Namespace(
            root=root,
            command_name="start",
            provider=False,
        )

    def test_lifecycle_start_uses_openclaw95_bounded_readiness_budget(self):
        config = self.config()
        emitted = []
        healthy = {
            "gateway": {"healthy": True},
            "ollama": {"enabled": True, "healthy": True},
        }
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value={"active": True}), \
             mock.patch.object(runtime, "gateway_probe", return_value={"healthy": False}), \
             mock.patch.object(runtime, "ollama_probe", return_value={"enabled": True, "healthy": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(
                 runtime,
                 "wait_for_runtime_health",
                 return_value=(healthy, 5, True),
             ) as waiter, \
             mock.patch.object(runtime, "clear_maintenance"), \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(self._args(Path(tmp)))

        self.assertEqual(code, 0)
        waiter.assert_called_once_with(
            config,
            timeout_seconds=runtime.LIFECYCLE_START_READY_TIMEOUT_SECONDS,
            require_ollama=False,
        )
        self.assertEqual(
            runtime.LIFECYCLE_START_READY_TIMEOUT_SECONDS,
            180.0,
        )
        self.assertEqual(
            emitted[-1]["verification"]["timeoutSeconds"],
            180.0,
        )

    def test_lifecycle_start_still_fails_closed_after_readiness_budget(self):
        config = self.config()
        emitted = []
        unhealthy = {
            "gateway": {"healthy": False, "error": "timeout"},
            "ollama": {"enabled": True, "healthy": True},
        }
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value={"active": True}), \
             mock.patch.object(runtime, "gateway_probe", return_value={"healthy": False}), \
             mock.patch.object(runtime, "ollama_probe", return_value={"enabled": True, "healthy": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(
                 runtime,
                 "wait_for_runtime_health",
                 return_value=(unhealthy, 7, False),
             ), \
             mock.patch.object(runtime, "clear_maintenance") as clear, \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(self._args(Path(tmp)))

        self.assertEqual(code, 2)
        clear.assert_not_called()
        self.assertFalse(emitted[-1]["started"])
        self.assertEqual(
            emitted[-1]["verification"]["timeoutSeconds"],
            180.0,
        )


if __name__ == "__main__":
    unittest.main()
