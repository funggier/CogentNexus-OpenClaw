import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import checks_v092 as checks
import provider_event_liveness_v092 as liveness


class _FakeKernel32:
    def __init__(self, handle=123, exit_code=liveness.STILL_ACTIVE, get_exit_ok=True):
        self.handle = handle
        self.exit_code = exit_code
        self.get_exit_ok = get_exit_ok
        self.closed = []

    def OpenProcess(self, access, inherit, pid):
        self.open_args = (access, inherit, pid)
        return self.handle

    def GetExitCodeProcess(self, handle, pointer):
        if not self.get_exit_ok:
            return 0
        pointer._obj.value = self.exit_code
        return 1

    def CloseHandle(self, handle):
        self.closed.append(handle)
        return 1


class LiveProbeRegressionV092Tests(unittest.TestCase):
    def test_windows_pid_liveness_uses_query_handle_not_os_kill(self):
        kernel = _FakeKernel32()
        self.assertTrue(liveness._pid_alive_windows(26776, kernel32=kernel))
        self.assertEqual(kernel.open_args[2], 26776)
        self.assertEqual(kernel.closed, [123])

        with mock.patch.object(liveness.os, "name", "nt"), \
             mock.patch.object(liveness, "_pid_alive_windows", return_value=True) as windows_probe, \
             mock.patch.object(liveness.os, "kill") as destructive_probe:
            self.assertTrue(liveness.safe_pid_alive(26776))
        windows_probe.assert_called_once_with(26776)
        destructive_probe.assert_not_called()

    def test_windows_pid_liveness_reports_exited_process_without_mutation(self):
        kernel = _FakeKernel32(exit_code=0)
        self.assertFalse(liveness._pid_alive_windows(26776, kernel32=kernel))
        self.assertEqual(kernel.closed, [123])

    def test_recovery_health_snapshot_has_non_conflicting_detail_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            runtime = root / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "health.json").write_text(json.dumps({
                "status": "healthy",
                "timestamp": "2026-08-22T02:17:49+00:00",
            }), encoding="utf-8")

            rows = checks._base_recovery_checks(root)
            health = next(row for row in rows if row["name"] == "Supervisor health snapshot")
            self.assertEqual(health["status"], "PASS")
            self.assertEqual(health["details"]["snapshotStatus"], "healthy")
            self.assertNotIn("status", health["details"])


if __name__ == "__main__":
    unittest.main()
