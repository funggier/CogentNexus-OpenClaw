from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_control_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_control_v091_idle", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostControlV091IdleTests(unittest.TestCase):
    def test_periodic_supervisor_tick_bypasses_watchdog_cli_recheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            original_argv = list(cnx.legacy.sys.argv)
            original_delegate = cnx.legacy.delegate
            original_apply = cnx.legacy.apply_watchdog_compat
            original_main = cnx.legacy.main
            calls = []
            try:
                cnx.legacy.sys.argv = [
                    "host_control_v091.py",
                    "--root",
                    str(root),
                    "supervisor",
                    "tick",
                    "--execute-safe",
                ]
                cnx.legacy.delegate = lambda argv: calls.append(("delegate", list(argv))) or 0
                cnx.legacy.apply_watchdog_compat = lambda _root: self.fail("periodic idle tick must not invoke OpenClaw config CLI")
                cnx.legacy.main = lambda: self.fail("periodic idle tick must bypass legacy control main")

                self.assertEqual(cnx.main(), 0)
            finally:
                cnx.legacy.sys.argv = original_argv
                cnx.legacy.delegate = original_delegate
                cnx.legacy.apply_watchdog_compat = original_apply
                cnx.legacy.main = original_main

            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0], "delegate")
            self.assertIn("supervisor", calls[0][1])
            self.assertIn("tick", calls[0][1])


if __name__ == "__main__":
    unittest.main()
