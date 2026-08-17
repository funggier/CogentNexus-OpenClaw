from __future__ import annotations

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
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
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.commit()
            db.close()
            self.assertFalse(cnx.durable_work_hint(root))

    def test_pending_outbox_is_actionable_even_with_terminal_ticket(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('completed')")
            db.execute("INSERT INTO ticket_outbox(delivery_status) VALUES ('pending')")
            db.commit()
            db.close()
            self.assertTrue(cnx.durable_work_hint(root))

    def test_healthy_endpoints_with_pending_work_enter_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            _path, db = self.create_ticket_db(root)
            db.execute("INSERT INTO tickets(status) VALUES ('waiting')")
            db.commit()
            db.close()

            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result": "recovery", "execute": execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result, {"result": "recovery", "execute": True})

    def test_gateway_failure_enters_proven_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "durable_work_hint", lambda _root: False)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result": "gateway-recovery", "execute": execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result, {"result": "gateway-recovery", "execute": True})

    def test_required_provider_failure_enters_proven_recovery_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: False)
            self.patch(cnx, "durable_work_hint", lambda _root: False)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: {"result": "provider-recovery", "execute": execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result, {"result": "provider-recovery", "execute": True})

    def test_healthy_endpoints_without_work_stay_on_lightweight_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "ollama_fast_probe", lambda: True)
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda *_args, **_kwargs: self.fail("idle runtime must not enter heavy recovery"))

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(result["result"], "idle")
            self.assertFalse(result["durableWorkPending"])
            self.assertEqual(result["probe"], "lightweight-http+sqlite-ro")


if __name__ == "__main__":
    unittest.main()
