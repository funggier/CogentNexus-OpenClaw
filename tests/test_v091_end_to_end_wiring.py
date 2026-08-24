from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

HOST_SCRIPT = SCRIPTS / "host_v091.py"
host_spec = importlib.util.spec_from_file_location("cnx_host_v091_e2e", HOST_SCRIPT)
cnx = importlib.util.module_from_spec(host_spec)
assert host_spec and host_spec.loader
host_spec.loader.exec_module(cnx)

STARTUP_SCRIPT = SCRIPTS / "startup_v091.py"
startup_spec = importlib.util.spec_from_file_location("cnx_startup_v091_e2e", STARTUP_SCRIPT)
startup_v091 = importlib.util.module_from_spec(startup_spec)
assert startup_spec and startup_spec.loader
startup_spec.loader.exec_module(startup_v091)


class V091EndToEndWiringTests(unittest.TestCase):
    def setUp(self):
        self.restore = []

    def tearDown(self):
        for obj, name, value in reversed(self.restore):
            setattr(obj, name, value)

    def patch(self, obj, name, value):
        self.restore.append((obj, name, getattr(obj, name)))
        setattr(obj, name, value)

    @staticmethod
    def completed(stdout="{}", returncode=0, stderr=""):
        return subprocess.CompletedProcess(["stub"], returncode, stdout, stderr)

    def seed_passthrough(self, root: Path, generation: int = 40):
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "generation": generation,
        })

    def install_common_success_stubs(self, startup_impl=None, runtime_impl=None, gateway_impl=None):
        self.patch(cnx, "configure_managed_plugin", lambda: None)
        self.patch(cnx, "validate_managed_config", lambda: None)
        self.patch(cnx.legacy, "apply_policy", lambda _workspace, _root: True)
        self.patch(cnx.legacy, "startup", startup_impl or (lambda *_args, **_kwargs: self.completed('{"enabled":true}')))
        self.patch(cnx.legacy, "runtime", runtime_impl or (lambda *_args, **_kwargs: self.completed('{"ok":true}')))
        self.patch(cnx.legacy, "gateway_status", gateway_impl or (lambda: {"healthy": True}))
        self.patch(cnx.legacy, "reconcile_default_session", lambda: {"ok": True, "created": False})
        self.patch(cnx.legacy, "promote_interrupted_direct", lambda *_args, **_kwargs: [])

    def test_fresh_initialization_is_passthrough_and_uses_v091_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            state = cnx.legacy.initialize(root)
            persisted = cnx.legacy.load_state(root)

            self.assertEqual(state["mode"], "passthrough")
            self.assertEqual(persisted["mode"], "passthrough")
            self.assertEqual(persisted["desiredProvider"], "unchanged")
            self.assertEqual(persisted["generation"], 1)
            self.assertEqual(cnx.legacy.startup_path().name, "startup_v091.py")
            self.assertEqual(startup_v091.legacy.host_control_path().name, "host_control_v091.py")

    def test_configure_failure_stays_passthrough_and_restores_native_gateway(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            before = self.seed_passthrough(root)
            plugin_calls = []
            gateway_restores = []
            self.patch(cnx.legacy, "plugin_enabled", lambda enabled: plugin_calls.append(enabled))
            self.patch(cnx, "configure_managed_plugin", lambda: (_ for _ in ()).throw(RuntimeError("configure failed")))
            self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed())
            self.patch(cnx, "_restore_native_gateway", lambda: gateway_restores.append(True) or {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(plugin_calls, [False, False])
            self.assertEqual(gateway_restores, [True])

    def test_plugin_enable_failure_stays_passthrough(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            before = self.seed_passthrough(root)
            calls = []
            self.install_common_success_stubs()

            def plugin(enabled):
                calls.append(enabled)
                if enabled:
                    raise RuntimeError("plugin enable failed")

            self.patch(cnx.legacy, "plugin_enabled", plugin)
            self.patch(cnx, "_restore_native_gateway", lambda: {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(calls, [False, True, False])

    def test_startup_partial_failure_removes_created_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            before = self.seed_passthrough(root)
            marker = workspace / "scheduled-task-created"
            startup_calls = []

            def startup(_root, action, check=True):
                startup_calls.append((action, check))
                if action == "enable":
                    marker.write_text("created", encoding="utf-8")
                    raise RuntimeError("startup verification failed")
                marker.unlink(missing_ok=True)
                return self.completed('{"disabled":true}')

            self.install_common_success_stubs(startup_impl=startup)
            self.patch(cnx.legacy, "plugin_enabled", lambda _enabled: None)
            self.patch(cnx, "_restore_native_gateway", lambda: {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertFalse(marker.exists())
            self.assertEqual(startup_calls, [("enable", True), ("disable", False)])
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])

    def test_lifecycle_start_failure_disables_startup_and_restores_gateway(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            before = self.seed_passthrough(root)
            startup_calls = []
            gateway_restores = []

            def startup(_root, action, check=True):
                startup_calls.append(action)
                return self.completed('{}')

            def runtime(_root, *args, **_kwargs):
                if args[:2] == ("lifecycle", "start"):
                    raise RuntimeError("lifecycle start failed")
                return self.completed('{}')

            self.install_common_success_stubs(startup_impl=startup, runtime_impl=runtime)
            self.patch(cnx.legacy, "plugin_enabled", lambda _enabled: None)
            self.patch(cnx, "_restore_native_gateway", lambda: gateway_restores.append(True) or {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(startup_calls, ["enable", "disable"])
            self.assertEqual(gateway_restores, [True])
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])

    def test_gateway_verify_failure_rolls_back_all_activation_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            before = self.seed_passthrough(root)
            startup_calls = []
            plugin_calls = []
            gateway_restores = []

            def startup(_root, action, check=True):
                startup_calls.append(action)
                return self.completed('{}')

            self.install_common_success_stubs(startup_impl=startup, gateway_impl=lambda: {"healthy": False})
            self.patch(cnx.legacy, "plugin_enabled", lambda enabled: plugin_calls.append(enabled))
            self.patch(cnx, "_restore_native_gateway", lambda: gateway_restores.append(True) or {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(startup_calls, ["enable", "disable"])
            self.assertEqual(plugin_calls, [False, True, False])
            self.assertEqual(gateway_restores, [True])
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])

    def test_failure_from_non_passthrough_prior_state_forces_safe_passthrough_without_generation_bump(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            prior = cnx.legacy.save_state(root, {
                "schemaVersion": 1,
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "generation": 55,
            })
            self.patch(cnx.legacy, "plugin_enabled", lambda _enabled: None)
            self.patch(cnx, "configure_managed_plugin", lambda: (_ for _ in ()).throw(RuntimeError("configure failed")))
            self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed())
            self.patch(cnx, "_restore_native_gateway", lambda: {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["desiredProvider"], "unchanged")
            self.assertEqual(after["generation"], prior["generation"])


if __name__ == "__main__":
    unittest.main()
