from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
spec = importlib.util.spec_from_file_location("cnx_host_v091", SCRIPTS / "host_v091.py")
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostV091Tests(unittest.TestCase):
    def setUp(self):
        self.restore = []

    def tearDown(self):
        for obj, name, value in reversed(self.restore):
            setattr(obj, name, value)

    def patch(self, obj, name, value):
        self.restore.append((obj, name, getattr(obj, name)))
        setattr(obj, name, value)

    def seed_managed(self, root: Path):
        cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "managed",
            "desiredGateway": "running",
            "desiredProvider": "running",
            "generation": 9,
        })

    def test_idle_supervisor_never_enters_heavy_path_when_responsive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("heavy supervisor must remain asleep"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertEqual(result["action"], "none")
            self.assertEqual(result["probe"], "lightweight-http+sqlite-ro")

    def test_confirmed_gateway_hang_is_bounded_without_heavy_supervisor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            calls = []
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: self.fail("provider probe must not precede gateway recovery"))
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: calls.append("restart") or {"attempted": True, "exitCode": 0})
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: calls.append("heavy") or {"result":"recovery","execute":execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(calls, ["restart"])
            self.assertEqual(result["result"], "gateway-recovery")
            self.assertEqual(result["hardHangRecovery"], {"attempted": True, "exitCode": 0})
            self.assertFalse(result["heavyPath"])

    def test_transient_gateway_probe_failure_does_not_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            outcomes = iter([False, True])
            self.patch(cnx, "gateway_fast_probe", lambda: next(outcomes))
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: self.fail("transient probe must not restart Gateway"))
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("recovered fast probe must remain on idle path"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")


if __name__ == "__main__":
    unittest.main()
