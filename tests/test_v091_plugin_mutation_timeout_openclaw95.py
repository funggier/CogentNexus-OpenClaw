from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091_plugin_timeout", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class V091PluginMutationTimeoutTests(unittest.TestCase):
    def test_plugin_enable_disable_timeout_covers_openclaw95_startup_window(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        seen = []
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"
            def fake_run(cmd, timeout=30, check=False):
                seen.append({"cmd": cmd, "timeout": timeout, "check": check})
                return subprocess.CompletedProcess(cmd, 0, "", "")
            cnx.legacy.run = fake_run
            cnx.legacy.plugin_enabled(False)
            cnx.legacy.plugin_enabled(True)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable

        self.assertEqual(len(seen), 2)
        self.assertTrue(all(item["timeout"] >= 180 for item in seen), seen)
        self.assertTrue(all(item["check"] is True for item in seen), seen)

    def test_timeout_after_disable_mutation_is_accepted_only_after_openclaw_reconciliation(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        seen = []
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"

            def fake_run(cmd, timeout=30, check=False):
                seen.append({"cmd": cmd, "timeout": timeout, "check": check})
                if cmd[1:3] == ["plugins", "disable"]:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                if cmd[1:3] == ["config", "get"]:
                    return subprocess.CompletedProcess(cmd, 0, "false\n", "")
                if cmd[1:3] == ["plugins", "registry"]:
                    return subprocess.CompletedProcess(cmd, 0, "Plugin registry refreshed.\n", "")
                if cmd[1:3] == ["plugins", "inspect"]:
                    return subprocess.CompletedProcess(
                        cmd,
                        0,
                        '{"plugin":{"id":"cogentnexus-openclaw","enabled":false,"status":"disabled"},"diagnostics":[]}\n',
                        "",
                    )
                raise AssertionError(cmd)

            cnx.legacy.run = fake_run
            cnx.legacy.plugin_enabled(False)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable

        self.assertEqual(
            [item["cmd"][1:3] for item in seen],
            [["plugins", "disable"], ["config", "get"], ["plugins", "registry"], ["plugins", "inspect"]],
        )

    def test_timeout_after_enable_mutation_is_accepted_only_after_openclaw_reconciliation(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"

            def fake_run(cmd, timeout=30, check=False):
                if cmd[1:3] == ["plugins", "enable"]:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                if cmd[1:3] == ["config", "get"]:
                    return subprocess.CompletedProcess(cmd, 0, "true\n", "")
                if cmd[1:3] == ["plugins", "registry"]:
                    return subprocess.CompletedProcess(cmd, 0, "Plugin registry refreshed.\n", "")
                if cmd[1:3] == ["plugins", "inspect"]:
                    return subprocess.CompletedProcess(
                        cmd,
                        0,
                        '{"plugin":{"id":"cogentnexus-openclaw","enabled":true,"status":"loaded"},"diagnostics":[]}\n',
                        "",
                    )
                raise AssertionError(cmd)

            cnx.legacy.run = fake_run
            cnx.legacy.plugin_enabled(True)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable

    def test_timeout_reconciliation_fails_closed_when_effective_config_does_not_match(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        seen = []
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"

            def fake_run(cmd, timeout=30, check=False):
                seen.append(cmd)
                if cmd[1:3] == ["plugins", "disable"]:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                if cmd[1:3] == ["config", "get"]:
                    return subprocess.CompletedProcess(cmd, 0, "true\n", "")
                raise AssertionError(cmd)

            cnx.legacy.run = fake_run
            with self.assertRaises(subprocess.TimeoutExpired):
                cnx.legacy.plugin_enabled(False)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable

        self.assertEqual([cmd[1:3] for cmd in seen], [["plugins", "disable"], ["config", "get"]])

    def test_timeout_reconciliation_fails_closed_when_registry_refresh_fails(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"

            def fake_run(cmd, timeout=30, check=False):
                if cmd[1:3] == ["plugins", "enable"]:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                if cmd[1:3] == ["config", "get"]:
                    return subprocess.CompletedProcess(cmd, 0, "true\n", "")
                if cmd[1:3] == ["plugins", "registry"]:
                    return subprocess.CompletedProcess(cmd, 1, "", "registry refresh failed")
                raise AssertionError(cmd)

            cnx.legacy.run = fake_run
            with self.assertRaises(subprocess.TimeoutExpired):
                cnx.legacy.plugin_enabled(True)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable

    def test_timeout_reconciliation_fails_closed_when_inspector_disagrees(self):
        original_run = cnx.legacy.run
        original_openclaw_executable = cnx.legacy.openclaw_executable
        try:
            cnx.legacy.openclaw_executable = lambda: "openclaw"

            def fake_run(cmd, timeout=30, check=False):
                if cmd[1:3] == ["plugins", "disable"]:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                if cmd[1:3] == ["config", "get"]:
                    return subprocess.CompletedProcess(cmd, 0, "false\n", "")
                if cmd[1:3] == ["plugins", "registry"]:
                    return subprocess.CompletedProcess(cmd, 0, "Plugin registry refreshed.\n", "")
                if cmd[1:3] == ["plugins", "inspect"]:
                    return subprocess.CompletedProcess(
                        cmd,
                        0,
                        '{"plugin":{"id":"cogentnexus-openclaw","enabled":true,"status":"loaded"},"diagnostics":[]}\n',
                        "",
                    )
                raise AssertionError(cmd)

            cnx.legacy.run = fake_run
            with self.assertRaises(subprocess.TimeoutExpired):
                cnx.legacy.plugin_enabled(False)
        finally:
            cnx.legacy.run = original_run
            cnx.legacy.openclaw_executable = original_openclaw_executable


if __name__ == "__main__":
    unittest.main()
