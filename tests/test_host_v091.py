from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
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
            root = workspace / ".cogent"
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

    def test_enable_failure_preserves_passthrough_generation_and_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogent"
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
            root = Path(tmp) / ".cogent"
            cnx.legacy.save_state(root, {
                "schemaVersion": 1,
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "generation": 2,
            })
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("heavy supervisor must remain asleep"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertEqual(result["action"], "none")
            self.assertEqual(result["probe"], "lightweight-http")

    def test_failed_fast_probe_delegates_to_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            cnx.legacy.save_state(root, {
                "schemaVersion": 1,
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "generation": 2,
            })
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result":"recovery","execute":execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result, {"result":"recovery","execute":True})


if __name__ == "__main__":
    unittest.main()
