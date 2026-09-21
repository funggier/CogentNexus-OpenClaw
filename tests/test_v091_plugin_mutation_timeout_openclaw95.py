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


if __name__ == "__main__":
    unittest.main()
