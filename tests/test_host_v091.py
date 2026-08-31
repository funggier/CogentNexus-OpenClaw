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
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostV091Tests(unittest.TestCase):
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

    def seed_passthrough(self, root: Path):
        cnx.legacy.initialize(root)
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "generation": 40,
        })

    def seed_managed(self, root: Path):
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "managed",
            "desiredGateway": "running",
            "desiredProvider": "running",
            "generation": 2,
        })

    def stub_enable_dependencies(self):
        self.patch(cnx.legacy, "plugin_enabled", lambda _enabled: None)
        self.patch(cnx, "configure_managed_plugin", lambda: None)
        self.patch(cnx, "validate_managed_config", lambda: None)
        self.patch(cnx.legacy, "apply_policy", lambda _workspace, _root: True)
        self.patch(cnx.legacy, "startup", lambda *_args, **_kwargs: self.completed('{"enabled":true}'))
        self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed('{"ok":true}'))
        self.patch(cnx.legacy, "gateway_status", lambda: {"healthy": True})
        self.patch(cnx.legacy, "reconcile_default_session", lambda: {"ok": True, "created": False})
        self.patch(cnx.legacy, "promote_interrupted_direct", lambda *_args, **_kwargs: [])

    def test_enable_commits_managed_only_after_activation_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            before = self.seed_passthrough(root)
            self.stub_enable_dependencies()

            result = cnx.enable(root)
            after = cnx.legacy.load_state(root)

            self.assertEqual(result["mode"], "managed")
            self.assertTrue(result["transactional"])
            self.assertEqual(after["mode"], "managed")
            self.assertEqual(after["desiredGateway"], "running")
            self.assertEqual(after["desiredProvider"], "running")
            self.assertEqual(after["generation"], before["generation"] + 1)

    def test_enable_reconciles_terminal_fences_before_plugin_activation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            self.seed_passthrough(root)
            self.stub_enable_dependencies()
            calls = []
            fences = {
                "cancelledOutboxSuppressed": 2,
                "terminalRecoverySuppressed": 3,
                "cancelledClassificationNormalized": 1,
            }
            self.patch(cnx.legacy, "reconcile_terminal_fences", lambda _root: calls.append("terminal-fence") or fences)
            self.patch(cnx.legacy, "plugin_enabled", lambda enabled: calls.append(f"plugin:{enabled}"))

            result = cnx.enable(root)

            self.assertEqual(calls[0], "terminal-fence")
            self.assertEqual(calls[1], "plugin:False")
            self.assertIn("plugin:True", calls)
            self.assertEqual(result["terminalFences"], fences)

    def test_enable_failure_preserves_passthrough_generation_and_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            agents = workspace / "AGENTS.md"
            agents.write_text("# Native policy\n", encoding="utf-8")
            before = self.seed_passthrough(root)

            self.patch(cnx, "configure_managed_plugin", lambda: None)
            self.patch(cnx, "validate_managed_config", lambda: None)
            self.patch(cnx.legacy, "apply_policy", lambda _workspace, _root: agents.write_text("managed\n", encoding="utf-8") or True)
            calls = []
            def plugin(enabled):
                calls.append(enabled)
                if enabled:
                    raise RuntimeError("injected plugin enable failure")
            self.patch(cnx.legacy, "plugin_enabled", plugin)
            self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed())
            self.patch(cnx, "_restore_native_gateway", lambda: {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Native policy\n")
            self.assertEqual(calls, [False, True, False])

    def test_idle_supervisor_never_enters_heavy_path_when_responsive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("heavy supervisor must remain asleep"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertEqual(result["action"], "none")
            self.assertEqual(result["probe"], "lightweight-http+sqlite-ro")

    def test_confirmed_gateway_hang_restarts_before_heavy_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            calls = []
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: calls.append("restart") or {"attempted": True, "exitCode": 0})
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: calls.append("heavy") or {"result":"recovery","execute":execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(calls, ["restart", "heavy"])
            self.assertEqual(result["result"], "recovery")
            self.assertEqual(result["hardHangRecovery"], {"attempted": True, "exitCode": 0})

    def test_transient_gateway_probe_failure_does_not_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            outcomes = iter([False, True])
            self.patch(cnx, "gateway_fast_probe", lambda: next(outcomes))
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: self.fail("transient probe must not restart Gateway"))
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("recovered fast probe must remain on idle path"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")


if __name__ == "__main__":
    unittest.main()
