from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091_idle_hint", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class V091IdleRecoveryHintTests(unittest.TestCase):
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

    def write_maintenance_marker(self, root: Path, recovery_policy: str = "healthy-runtime"):
        path = root / "runtime" / "maintenance.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "schemaVersion": 1,
            "active": True,
            "reason": "test restart recovery",
            "owner": "operator",
            "recoveryPolicy": recovery_policy,
        }), encoding="utf-8")
        return path

    def create_ticket_db(self, root: Path):
        path = cnx.legacy.ticket_db(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.execute("CREATE TABLE tickets(status TEXT NOT NULL)")
        db.execute("CREATE TABLE ticket_outbox(delivery_status TEXT NOT NULL)")
        db.commit()
        return path, db

    def test_terminal_database_is_idle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.commit()
            db.close()
            self.assertFalse(cnx.durable_work_hint(root))

    def test_pending_outbox_is_actionable_even_with_terminal_ticket(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.execute("INSERT INTO ticket_outbox(delivery_status) VALUES ('pending')")
            db.commit()
            db.close()
            self.assertTrue(cnx.durable_work_hint(root))

    def test_pending_assistant_delivery_is_actionable_even_with_terminal_ticket(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.execute("CREATE TABLE cnx_assistant_delivery(status TEXT NOT NULL)")
            db.execute("INSERT INTO cnx_assistant_delivery(status) VALUES ('pending')")
            db.commit()
            db.close()
            self.assertTrue(cnx.durable_work_hint(root))

    def test_awaiting_direct_delivery_is_actionable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.execute("CREATE TABLE cnx_direct_recovery(state TEXT NOT NULL)")
            db.execute("INSERT INTO cnx_direct_recovery(state) VALUES ('awaiting_delivery')")
            db.commit()
            db.close()
            self.assertTrue(cnx.durable_work_hint(root))

    def test_healthy_endpoints_with_pending_work_enter_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('waiting')")
            db.commit()
            db.close()

            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result": "recovery", "execute": execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "recovery")
            self.assertTrue(result["execute"])
            self.assertEqual(result["wakeAuthority"], "ticket")
            self.assertEqual(result["wakeReason"], "wake/ticket/legacy")
            self.assertEqual(result["wakeWorkId"], "1")
            self.assertTrue(result["heavyPath"])

    def test_gateway_failure_restarts_then_enters_proven_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "durable_work_hint", lambda _root: False)
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: {"attempted": True, "exitCode": 0})
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result": "gateway-recovery", "execute": execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "gateway-recovery")
            self.assertEqual(result["hardHangRecovery"], {"attempted": True, "exitCode": 0})

    def test_provider_failure_alone_does_not_enter_global_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: False)
            self.patch(cnx, "durable_work_hint", lambda _root: False)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("provider health alone must not wake global Host recovery"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertFalse(result["providerRequired"])
            self.assertFalse(result["durableWorkPending"])


    def test_healthy_runtime_marker_is_reconciled_before_idle_return(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            marker = self.write_maintenance_marker(root)
            calls = []

            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(
                cnx,
                "classify_wake",
                lambda _root: cnx.WakeDecision(False, "none", None, "idle/no-actionable-work"),
            )
            self.patch(
                cnx,
                "LEGACY_SUPERVISOR_TICK",
                lambda *_args, **_kwargs: self.fail("maintenance convergence must not re-enter legacy heavy supervisor"),
            )

            def runtime(_root, *args, timeout=180, check=True):
                calls.append((args, timeout, check))
                self.assertEqual(args, ("lifecycle", "start"))
                marker.unlink()
                return subprocess.CompletedProcess(
                    args=list(args),
                    returncode=0,
                    stdout=json.dumps({"started": True, "maintenance": None}),
                    stderr="",
                )

            self.patch(cnx.legacy, "runtime", runtime)

            result = cnx.supervisor_tick(root, True)

            self.assertEqual(len(calls), 1)
            self.assertFalse(marker.exists())
            self.assertEqual(result["result"], "idle")
            self.assertEqual(result["maintenanceRecovery"]["status"], "reconciled")
            self.assertFalse(result["heavyPath"])

    def test_read_only_tick_reports_healthy_runtime_marker_without_mutating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            marker = self.write_maintenance_marker(root)

            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(
                cnx.legacy,
                "runtime",
                lambda *_args, **_kwargs: self.fail("read-only supervisor tick must not mutate maintenance state"),
            )
            self.patch(
                cnx,
                "LEGACY_SUPERVISOR_TICK",
                lambda *_args, **_kwargs: self.fail("read-only marker observation must not enter legacy heavy supervisor"),
            )

            result = cnx.supervisor_tick(root, False)

            self.assertTrue(marker.exists())
            self.assertEqual(result["result"], "maintenance-recovery-pending")
            self.assertEqual(result["recoveryPolicy"], "healthy-runtime")
            self.assertFalse(result["heavyPath"])

    def test_healthy_endpoints_without_work_stay_on_lightweight_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("idle supervisor must not enter legacy heavy path"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertEqual(result["action"], "none")


if __name__ == "__main__":
    unittest.main()
