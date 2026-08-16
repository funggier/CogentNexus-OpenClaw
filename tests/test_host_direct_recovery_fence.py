import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOST_PATH = ROOT / "skills" / "cogentnexus" / "scripts" / "host.py"
SPEC = importlib.util.spec_from_file_location("cnx_host_v085", HOST_PATH)
assert SPEC and SPEC.loader
host = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host)


class HostDirectRecoveryFenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / ".cogent"
        path = self.root / "runtime" / "cogentnexus.sqlite3"
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
        db.executescript(
            """
            CREATE TABLE tickets(
              ticket_id TEXT PRIMARY KEY,
              status TEXT NOT NULL,
              workflow_eligible INTEGER NOT NULL DEFAULT 0,
              failure_class TEXT,
              failure_message TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE ticket_events(
              event_id INTEGER PRIMARY KEY AUTOINCREMENT,
              ticket_id TEXT NOT NULL,
              event_type TEXT NOT NULL,
              payload_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE cnx_direct_recovery(
              ticket_id TEXT PRIMARY KEY,
              state TEXT NOT NULL
            );
            """
        )
        for ticket_id in ["owned-pending", "owned-running", "owned-delivery", "unowned"]:
            db.execute(
                "INSERT INTO tickets(ticket_id,status,workflow_eligible,created_at,updated_at) VALUES (?,'accepted',0,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')",
                (ticket_id,),
            )
        db.execute("INSERT INTO cnx_direct_recovery(ticket_id,state) VALUES ('owned-pending','pending')")
        db.execute("INSERT INTO cnx_direct_recovery(ticket_id,state) VALUES ('owned-running','running')")
        db.execute("INSERT INTO cnx_direct_recovery(ticket_id,state) VALUES ('owned-delivery','awaiting_delivery')")
        db.commit()
        db.close()
        self.db_path = path

    def tearDown(self):
        self.temp.cleanup()

    def test_host_promotes_only_direct_tickets_not_owned_by_recovery(self):
        recovered = host.promote_interrupted_direct(
            self.root,
            "2026-12-31T00:00:00Z",
            "Gateway recovered",
        )
        self.assertEqual(recovered, ["unowned"])
        db = sqlite3.connect(self.db_path)
        rows = dict(db.execute("SELECT ticket_id,status FROM tickets"))
        self.assertEqual(rows["owned-pending"], "accepted")
        self.assertEqual(rows["owned-running"], "accepted")
        self.assertEqual(rows["owned-delivery"], "accepted")
        self.assertEqual(rows["unowned"], "waiting")
        events = db.execute("SELECT ticket_id,event_type FROM ticket_events").fetchall()
        self.assertEqual(events, [("unowned", "host_recovered_direct")])
        db.close()

    def test_legacy_database_without_recovery_table_keeps_previous_host_behavior(self):
        db = sqlite3.connect(self.db_path)
        db.execute("DROP TABLE cnx_direct_recovery")
        db.execute("UPDATE tickets SET status='accepted',workflow_eligible=0")
        db.execute("DELETE FROM ticket_events")
        db.commit()
        db.close()
        recovered = host.promote_interrupted_direct(
            self.root,
            "2026-12-31T00:00:00Z",
            "Gateway recovered",
        )
        self.assertEqual(
            recovered,
            ["owned-delivery", "owned-pending", "owned-running", "unowned"],
        )


if __name__ == "__main__":
    unittest.main()
