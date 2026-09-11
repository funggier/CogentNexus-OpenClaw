from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"


def load_host():
    spec = importlib.util.spec_from_file_location("cnx_host_v091_idle_quiescence", SCRIPTS / "host_v091.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


host = load_host()


class IdleQuiescenceTests(unittest.TestCase):
    def _managed_root(self) -> Path:
        root = Path(tempfile.mkdtemp()) / ".cogentnexus-openclaw"
        host.legacy.initialize(root)
        host.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "managed",
            "desiredGateway": "running",
            "desiredProvider": "running",
            "generation": 1,
        })
        self.addCleanup(lambda: __import__("shutil").rmtree(root.parent, ignore_errors=True))
        return root

    def test_idle_tick_never_calls_legacy_heavy_supervisor(self):
        root = self._managed_root()
        idle = host.WakeDecision(False, "none", None, "idle/no-actionable-work")
        with mock.patch.object(host, "classify_wake", return_value=idle), \
             mock.patch.object(host, "gateway_fast_probe", return_value=True), \
             mock.patch.object(host, "ollama_fast_probe") as provider_probe, \
             mock.patch.object(host, "LEGACY_SUPERVISOR_TICK") as heavy:
            result = host.supervisor_tick(root, execute_safe=True)

        heavy.assert_not_called()
        provider_probe.assert_not_called()
        self.assertEqual(result["result"], "idle")
        self.assertEqual(result["action"], "none")
        self.assertEqual(result["wakeReason"], "idle/no-actionable-work")

    def test_second_scheduled_tick_after_wake_is_consumed_stays_out_of_heavy_path(self):
        root = self._managed_root()
        actionable = host.WakeDecision(True, "delivery", "D1", "wake/delivery")
        consumed = host.WakeDecision(False, "none", None, "idle/no-actionable-work")
        decisions = iter([actionable, consumed])
        heavy_calls = []

        def heavy(_root, _execute_safe):
            heavy_calls.append("heavy")
            return {"result": "recovery", "action": "delivery"}

        with mock.patch.object(host, "classify_wake", side_effect=lambda _root, _now=None: next(decisions)), \
             mock.patch.object(host, "gateway_fast_probe", return_value=True), \
             mock.patch.object(host, "ollama_fast_probe") as provider_probe, \
             mock.patch.object(host, "LEGACY_SUPERVISOR_TICK", side_effect=heavy):
            first = host.supervisor_tick(root, execute_safe=True)
            second = host.supervisor_tick(root, execute_safe=True)

        self.assertEqual(first["result"], "recovery")
        self.assertEqual(second["result"], "idle")
        self.assertEqual(heavy_calls, ["heavy"])
        provider_probe.assert_not_called()


if __name__ == "__main__":
    unittest.main()
