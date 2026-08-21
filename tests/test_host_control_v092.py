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
            with mock.patch.object(control.provider_events, "stop_adapter") as stop, \
                 mock.patch.object(control.openclaw_route, "restore_native") as restore, \
                 mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 2)
            self.assertEqual(code, 2)
            stop.assert_not_called()
            restore.assert_not_called()
            activate.assert_not_called()

    def test_route_restore_failure_blocks_runtime_activation_but_stops_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(
                control.provider_events, "stop_adapter", return_value={"stopped": []}
            ) as stop, mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": False, "error": "restore failed"}
            ), mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)
            stop.assert_called_once_with(root)
            activate.assert_not_called()

    def test_unhealthy_gateway_after_restore_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(
                control.provider_events, "stop_adapter", return_value={"stopped": []}
            ), mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": True, "restored": True}
            ), mock.patch.object(
                control.runtime_boundary, "activate_current_config", return_value={"ok": False, "phase": "gateway-verification"}
            ):
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)

    def test_native_route_and_gateway_boundary_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            order = []

            def stop(root_arg):
                order.append("stop-adapter")
                return {"stopped": []}

            def restore(root_arg):
                order.append("restore-route")
                return {"ok": True, "restored": True}

            def activate():
                order.append("activate-gateway")
                return {"ok": True, "phase": "verified"}

            with mock.patch.object(control.provider_events, "stop_adapter", side_effect=stop), \
                 mock.patch.object(control.openclaw_route, "restore_native", side_effect=restore), \
                 mock.patch.object(control.runtime_boundary, "activate_current_config", side_effect=activate):
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 0)
            self.assertEqual(order, ["stop-adapter", "restore-route", "activate-gateway"])

    def test_intentional_stop_silences_adapter_before_host_shutdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            order = []

            def stop(root_arg):
                order.append("stop-adapter")
                return {"stopped": []}

            def legacy_main():
                order.append("host-stop")
                return 0

            argv = ["host_control_v092.py", "--root", str(root), "stop"]
            with mock.patch.object(control.v091.legacy.sys, "argv", argv), \
                 mock.patch.object(control.provider_events, "stop_adapter", side_effect=stop), \
                 mock.patch.object(control.v091, "main", side_effect=legacy_main):
                code = control.main()
            self.assertEqual(code, 0)
            self.assertEqual(order, ["stop-adapter", "host-stop"])


if __name__ == "__main__":
    unittest.main()
