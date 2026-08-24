from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_control_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_control_v091", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostControlV091Tests(unittest.TestCase):
    def test_failed_enable_restores_watchdog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            original_argv = list(cnx.legacy.sys.argv)
            original_apply = cnx.legacy.apply_watchdog_compat
            original_delegate = cnx.legacy.delegate
            original_restore = cnx.legacy.restore_watchdog_compat
            original_audit = cnx.legacy.append_audit
            calls = []
            try:
                cnx.legacy.sys.argv = ["host_control_v091.py", "--root", str(root), "enable"]
                cnx.legacy.apply_watchdog_compat = lambda _root: calls.append("apply") or {"changed": True}
                cnx.legacy.delegate = lambda _argv: calls.append("delegate") or 1
                cnx.legacy.restore_watchdog_compat = lambda _root: calls.append("restore") or {"restored": True}
                cnx.legacy.append_audit = lambda *_args, **_kwargs: calls.append("audit")
                self.assertEqual(cnx.main(), 1)
            finally:
                cnx.legacy.sys.argv = original_argv
                cnx.legacy.apply_watchdog_compat = original_apply
                cnx.legacy.delegate = original_delegate
                cnx.legacy.restore_watchdog_compat = original_restore
                cnx.legacy.append_audit = original_audit
            self.assertEqual(calls, ["apply", "delegate", "restore", "audit"])

    def test_reset_routes_to_lifecycle_without_controller(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            original_argv = list(cnx.legacy.sys.argv)
            original_lifecycle = cnx.lifecycle.main
            calls = []
            try:
                cnx.legacy.sys.argv = ["host_control_v091.py", "--root", str(root), "reset"]
                cnx.lifecycle.main = lambda command, resolved: calls.append((command, resolved)) or 17
                self.assertEqual(cnx.main(), 17)
            finally:
                cnx.legacy.sys.argv = original_argv
                cnx.lifecycle.main = original_lifecycle
            self.assertEqual(calls, [("reset", root.resolve())])

    def test_uninstall_routes_to_lifecycle_without_controller(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            original_argv = list(cnx.legacy.sys.argv)
            original_lifecycle = cnx.lifecycle.main
            calls = []
            try:
                cnx.legacy.sys.argv = ["host_control_v091.py", "--root", str(root), "uninstall"]
                cnx.lifecycle.main = lambda command, resolved: calls.append((command, resolved)) or 23
                self.assertEqual(cnx.main(), 23)
            finally:
                cnx.legacy.sys.argv = original_argv
                cnx.lifecycle.main = original_lifecycle
            self.assertEqual(calls, [("uninstall", root.resolve())])


if __name__ == "__main__":
    unittest.main()
