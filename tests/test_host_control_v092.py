import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_control_v092 as control


class HostControlV092Tests(unittest.TestCase):
    def test_verified_stop_waits_for_ownership_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            held = {"running": True, "ownershipHeld": True, "pid": 123}
            released = {"running": False, "ownershipHeld": False, "pid": None}
            with mock.patch.object(
                control.provider_events, "stop_adapter", side_effect=[{"stopped": [{"stopped": True}]}, {"stopped": []}]
            ) as stop, mock.patch.object(
                control.provider_events, "adapter_status", side_effect=[held, released]
            ), mock.patch.object(control.time, "sleep") as sleep:
                result = control._stop_provider_events_verified(root)

            self.assertTrue(result["ok"])
            self.assertEqual(result["verification"], "ownership-released")
            self.assertEqual(stop.call_count, 2)
            sleep.assert_called_once_with(0.025)

    def test_verified_stop_fails_closed_when_ownership_does_not_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            held = {"running": True, "ownershipHeld": True, "pid": 123}
            with mock.patch.object(
                control.provider_events, "stop_adapter", return_value={"stopped": [{"stopped": True}]}
            ), mock.patch.object(
                control.provider_events, "adapter_status", return_value=held
            ), mock.patch.object(
                control, "ADAPTER_STOP_VERIFY_SECONDS", 0.0
            ):
                result = control._stop_provider_events_verified(root)

            self.assertFalse(result["ok"])
            self.assertEqual(result["verification"], "ownership-not-released")

    def test_delegate_failure_does_not_continue_native_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(control, "_stop_provider_events_verified") as stop, \
                 mock.patch.object(control.openclaw_route, "restore_native") as restore, \
                 mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 2)
            self.assertEqual(code, 2)
            stop.assert_not_called()
            restore.assert_not_called()
            activate.assert_not_called()

    def test_disable_blocks_native_activation_when_adapter_cannot_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            failed_stop = {"ok": False, "verification": "ownership-not-released"}
            with mock.patch.object(
                control, "_stop_provider_events_verified", return_value=failed_stop
            ), mock.patch.object(control.openclaw_route, "restore_native") as restore, \
                 mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)
            restore.assert_not_called()
            activate.assert_not_called()

    def test_route_restore_failure_blocks_runtime_activation_after_verified_adapter_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(
                control, "_stop_provider_events_verified", return_value={"ok": True}
            ), mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": False, "error": "restore failed"}
            ), mock.patch.object(control.runtime_boundary, "activate_current_config") as activate:
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)
            activate.assert_not_called()

    def test_unhealthy_gateway_after_restore_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(
                control, "_stop_provider_events_verified", return_value={"ok": True}
            ), mock.patch.object(
                control.openclaw_route, "restore_native", return_value={"ok": True, "restored": True}
            ), mock.patch.object(
                control.runtime_boundary, "activate_current_config", return_value={"ok": False, "phase": "gateway-verification"}
            ):
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 1)

    def test_native_route_and_gateway_boundary_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            order = []

            def stop(root_arg):
                order.append("stop-adapter")
                return {"ok": True}

            def restore(root_arg):
                order.append("restore-route")
                return {"ok": True, "restored": True}

            def activate():
                order.append("activate-gateway")
                return {"ok": True, "phase": "verified"}

            with mock.patch.object(control, "_stop_provider_events_verified", side_effect=stop), \
                 mock.patch.object(control.openclaw_route, "restore_native", side_effect=restore), \
                 mock.patch.object(control.runtime_boundary, "activate_current_config", side_effect=activate):
                code = control._finish_disable_native_boundary(root, 0)
            self.assertEqual(code, 0)
            self.assertEqual(order, ["stop-adapter", "restore-route", "activate-gateway"])

    def test_intentional_stop_verifies_adapter_before_host_shutdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            order = []

            def stop(root_arg):
                order.append("stop-adapter")
                return {"ok": True}

            def legacy_main():
                order.append("host-stop")
                return 0

            argv = ["host_control_v092.py", "--root", str(root), "stop"]
            with mock.patch.object(control.v091.legacy.sys, "argv", argv), \
                 mock.patch.object(control, "_stop_provider_events_verified", side_effect=stop), \
                 mock.patch.object(control.v091, "main", side_effect=legacy_main):
                code = control.main()
            self.assertEqual(code, 0)
            self.assertEqual(order, ["stop-adapter", "host-stop"])

    def test_intentional_stop_does_not_shutdown_provider_if_adapter_is_still_owned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            argv = ["host_control_v092.py", "--root", str(root), "stop"]
            with mock.patch.object(control.v091.legacy.sys, "argv", argv), \
                 mock.patch.object(
                     control, "_stop_provider_events_verified", return_value={"ok": False}
                 ), mock.patch.object(control.v091, "main") as legacy_main:
                code = control.main()
            self.assertEqual(code, 1)
            legacy_main.assert_not_called()


if __name__ == "__main__":
    unittest.main()
