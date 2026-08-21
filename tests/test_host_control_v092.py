import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_control_v092 as control


class HostControlV092Tests(unittest.TestCase):
    def test_delegate_failure_does_not_continue_native_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(control.openclaw_route, "restore_native") as restore, \
                 mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 2)
            self.assertEqual(code, 2)
            restore.assert_not_called()
            activate.assert_not_called()

    def test_route_restore_failure_blocks_runtime_activation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": False, "error": "restore failed"}
            ), mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)
            activate.assert_not_called()

    def test_unhealthy_gateway_after_restore_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": True, "restored": True}
            ), mock.patch.object(
                control.runtime_boundary, "activate_current_config", return_value={"ok": False, "phase": "gateway-verification"}
            ):
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)

    def test_native_route_and_gateway_boundary_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": True, "restored": True}
            ) as restore, mock.patch.object(
                control.runtime_boundary, "activate_current_config", return_value={"ok": True, "phase": "verified"}
            ) as activate:
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 0)
            restore.assert_called_once_with(root)
            activate.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
