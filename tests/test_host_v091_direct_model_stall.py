from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_stall_v091 as stall  # noqa: E402


TICKET = "CNXT-11111111-1111-1111-1111-111111111111"
OWNER = "agent:main:dashboard:test"


def make_db(root: Path, *, response_ready_at=None):
    path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(
        """
        CREATE TABLE tickets (
          ticket_id TEXT PRIMARY KEY,
          run_id TEXT NOT NULL,
          owner_session_key TEXT NOT NULL,
          status TEXT NOT NULL,
          workflow_eligible INTEGER NOT NULL,
          workflow_id TEXT,
          response_ready_at TEXT,
          delivery_confirmed_at TEXT,
          worker_id TEXT,
          lease_token TEXT,
          lease_expires_at TEXT,
          heartbeat_at TEXT,
          failure_class TEXT,
          failure_message TEXT,
          delivery_last_error TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE ticket_events (
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          ticket_id TEXT NOT NULL,
          event_type TEXT NOT NULL,
          payload_json TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE cnx_direct_model_call (
          ticket_id TEXT PRIMARY KEY,
          run_id TEXT NOT NULL,
          call_id TEXT NOT NULL,
          state TEXT NOT NULL,
          provider TEXT,
          model TEXT,
          started_at TEXT NOT NULL,
          deadline_at TEXT NOT NULL,
          ended_at TEXT,
          outcome TEXT,
          duration_ms INTEGER,
          recovery_started_at TEXT,
          recovery_attempt_count INTEGER NOT NULL DEFAULT 0,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE cnx_sessions (
          session_key TEXT PRIMARY KEY,
          state TEXT NOT NULL,
          generation INTEGER NOT NULL,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE cnx_direct_recovery (
          ticket_id TEXT PRIMARY KEY,
          mode TEXT NOT NULL,
          state TEXT NOT NULL,
          attempt_count INTEGER NOT NULL DEFAULT 0,
          active_run_id TEXT,
          next_attempt_at TEXT,
          last_error TEXT,
          owner_generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        """
    )
    db.execute(
        "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,delivery_confirmed_at,"
        "created_at,updated_at) VALUES (?,?,?,'accepted',0,NULL,?,NULL,?,?)",
        (TICKET, "run-live", OWNER, response_ready_at,
         "2026-08-18T13:00:00+00:00", "2026-08-18T13:00:00+00:00"),
    )
    db.execute(
        "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',7,?,?)",
        (OWNER, "2026-08-18T13:00:00+00:00", "2026-08-18T13:00:00+00:00"),
    )
    db.execute(
        "INSERT INTO cnx_direct_model_call(ticket_id,run_id,call_id,state,provider,model,started_at,deadline_at,updated_at) "
        "VALUES (?,?,?,'active','ollama','qwen3.5:9b',?,?,?)",
        (TICKET, "run-live", "call-live", "2026-08-18T13:00:00+00:00", "2026-08-18T13:15:00+00:00", "2026-08-18T13:00:00+00:00"),
    )
    db.commit()
    db.close()
    return path


class HostDirectModelStallTests(unittest.TestCase):
    def test_claim_is_host_durable_but_does_not_mutate_ticket(self):
        with tempfile.TemporaryDirectory(prefix="cnxclaw-host-stall-") as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = make_db(root)
            claim = stall.claim_expired_direct_model_call(root, "2026-08-18T13:16:00+00:00")
            self.assertIsNotNone(claim)
            self.assertEqual(claim["ticket_id"], TICKET)
            db = sqlite3.connect(path)
            self.assertEqual(db.execute("SELECT status FROM tickets WHERE ticket_id=?", (TICKET,)).fetchone()[0], "accepted")
            self.assertEqual(db.execute("SELECT state,recovery_attempt_count FROM cnx_direct_model_call WHERE ticket_id=?", (TICKET,)).fetchone(), ("recovering", 1))
            db.close()

    def test_quiesced_classification_authorizes_direct_recovery_without_workflow_promotion(self):
        with tempfile.TemporaryDirectory(prefix="cnxclaw-host-stall-classify-") as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = make_db(root)
            claim = stall.claim_expired_direct_model_call(root, "2026-08-18T13:16:00+00:00")
            result = stall.classify_quiesced_direct_model_call(root, claim)
            self.assertEqual(result["action"], "pre-response-recovery-authorized")
            self.assertEqual(result["recoveryState"], "pending")
            self.assertEqual(result["ownerGeneration"], 7)
            db = sqlite3.connect(path)
            self.assertEqual(
                db.execute("SELECT status,workflow_eligible,failure_class,workflow_id FROM tickets WHERE ticket_id=?", (TICKET,)).fetchone(),
                ("accepted", 0, "interrupted", None),
            )
            self.assertEqual(
                db.execute("SELECT mode,state,attempt_count,active_run_id,owner_generation FROM cnx_direct_recovery WHERE ticket_id=?", (TICKET,)).fetchone(),
                ("resume", "pending", 0, None, 7),
            )
            self.assertEqual(db.execute("SELECT state,outcome FROM cnx_direct_model_call WHERE ticket_id=?", (TICKET,)).fetchone(),
                             ("interrupted", "host-timeout-authorized"))
            events = [row[0] for row in db.execute("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id", (TICKET,))]
            self.assertEqual(events, ["host_direct_model_timeout_authorized"])
            db.close()

    def test_response_ready_wins_and_is_never_promoted_by_stall_path(self):
        with tempfile.TemporaryDirectory(prefix="cnxclaw-host-stall-ready-") as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = make_db(root, response_ready_at="2026-08-18T13:14:59+00:00")
            # The Host can only claim rows whose Ticket is still pre-response.
            claim = stall.claim_expired_direct_model_call(root, "2026-08-18T13:16:00+00:00")
            self.assertIsNone(claim)
            db = sqlite3.connect(path)
            self.assertEqual(db.execute("SELECT status,workflow_eligible FROM tickets WHERE ticket_id=?", (TICKET,)).fetchone(), ("accepted", 0))
            self.assertEqual(db.execute("SELECT count(*) FROM cnx_direct_recovery").fetchone()[0], 0)
            db.close()

    def test_missing_direct_recovery_schema_fails_without_ticket_promotion(self):
        with tempfile.TemporaryDirectory(prefix="cnxclaw-host-stall-schema-") as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            path = make_db(root)
            db = sqlite3.connect(path)
            db.execute("DROP TABLE cnx_direct_recovery")
            db.commit()
            db.close()
            claim = stall.claim_expired_direct_model_call(root, "2026-08-18T13:16:00+00:00")
            with self.assertRaisesRegex(RuntimeError, "Direct recovery schema missing"):
                stall.classify_quiesced_direct_model_call(root, claim)
            db = sqlite3.connect(path)
            self.assertEqual(
                db.execute("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?", (TICKET,)).fetchone(),
                ("accepted", 0, None),
            )
            self.assertEqual(
                db.execute("SELECT state FROM cnx_direct_model_call WHERE ticket_id=?", (TICKET,)).fetchone()[0],
                "recovering",
            )
            db.close()

    def test_source_orders_quiescence_before_ticket_classification_and_restart(self):
        source = (SCRIPTS / "host_stall_v091.py").read_text(encoding="utf-8")
        function = source[source.index("def recover_expired_direct_model_call"):source.index("def supervisor_tick")]
        prepare = function.index('"prepare",')
        stop = function.index('"stop",', prepare)
        provider_stop = function.index('"--provider",', stop)
        classify = function.index("classify_quiesced_direct_model_call(root, claim)", provider_stop)
        start = function.index('"start", "--provider"', classify)
        self.assertLess(prepare, stop)
        self.assertLess(stop, provider_stop)
        self.assertLess(provider_stop, classify)
        self.assertLess(classify, start)


if __name__ == "__main__":
    unittest.main()
