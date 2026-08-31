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
spec = importlib.util.spec_from_file_location("cnx_host_v091_disable", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class V091DisableTransactionTests(unittest.TestCase):
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

    def seed(self, root: Path, mode="managed", generation=70):
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": mode,
            "desiredGateway": "running",
            "desiredProvider": "running" if mode != "passthrough" else "unchanged",
            "generation": generation,
        })

    def test_disable_commits_passthrough_only_after_native_gateway_is_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            before = self.seed(root)
            order = []
            original_transition = cnx.legacy.transition

            self.patch(cnx.legacy, "startup", lambda _root, action, check=True: order.append(f"startup-{action}") or self.completed('{}'))
            self.patch(cnx.legacy, "remove_policy", lambda _workspace: order.append("policy-remove") or True)
            self.patch(cnx.legacy, "plugin_enabled", lambda enabled: order.append(f"plugin-{enabled}"))
            self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: order.append("runtime-cancel") or self.completed('{}'))
            self.patch(cnx, "_restore_native_gateway", lambda: order.append("native-verified") or {"exitCode": 0, "healthy": True})

            def transition(_root, **changes):
                order.append("state-commit")
                return original_transition(_root, **changes)

            self.patch(cnx.legacy, "transition", transition)

            result = cnx.disable(root)
            after = cnx.legacy.load_state(root)

            self.assertEqual(result["mode"], "passthrough")
            self.assertTrue(result["transactional"])
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"] + 1)
            self.assertLess(order.index("native-verified"), order.index("state-commit"))
            self.assertEqual(order[:4], ["startup-disable", "policy-remove", "plugin-False", "runtime-cancel"])

    def test_disable_failure_restores_managed_surfaces_without_state_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            agents = workspace / "AGENTS.md"
            agents.write_text("# managed policy\n", encoding="utf-8")
            before = self.seed(root)
            startup_calls = []
            plugin_calls = []
            runtime_calls = []

            def startup(_root, action, check=True):
                startup_calls.append(action)
                return self.completed('{}')

            def remove_policy(_workspace):
                agents.write_text("# native policy\n", encoding="utf-8")
                return True

            def plugin(enabled):
                plugin_calls.append(enabled)
                if enabled is False:
                    raise RuntimeError("plugin disable failed")

            self.patch(cnx.legacy, "startup", startup)
            self.patch(cnx.legacy, "remove_policy", remove_policy)
            self.patch(cnx.legacy, "plugin_enabled", plugin)
            self.patch(cnx.legacy, "runtime", lambda _root, *args, **_kwargs: runtime_calls.append(args) or self.completed('{}'))

            with self.assertRaisesRegex(RuntimeError, "transactional disable failed"):
                cnx.disable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "managed")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(agents.read_text(encoding="utf-8"), "# managed policy\n")
            self.assertEqual(plugin_calls, [False, True])
            self.assertEqual(startup_calls, ["disable", "enable"])
            self.assertTrue(any(call[:2] == ("lifecycle", "start") for call in runtime_calls))

    def test_passthrough_disable_failure_never_reenables_cnx(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace" / ".cogentnexus-openclaw"
            before = self.seed(root, mode="passthrough", generation=80)
            plugin_calls = []
            startup_calls = []

            self.patch(cnx.legacy, "startup", lambda _root, action, check=True: startup_calls.append(action) or self.completed('{}'))
            self.patch(cnx.legacy, "remove_policy", lambda _workspace: False)

            def plugin(enabled):
                plugin_calls.append(enabled)
                if enabled is False:
                    raise RuntimeError("disable failed")

            self.patch(cnx.legacy, "plugin_enabled", plugin)

            with self.assertRaisesRegex(RuntimeError, "transactional disable failed"):
                cnx.disable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(plugin_calls, [False])
            self.assertEqual(startup_calls, ["disable"])


if __name__ == "__main__":
    unittest.main()
