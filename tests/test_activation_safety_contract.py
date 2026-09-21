from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_authority_v091 as authority
import host_provider_v092 as provider
import host_stall_v091 as stall
import host_v091 as recovery
import supervisor_quiescence as quiescence


class ActivationSafetyContractTests(unittest.TestCase):
    def test_composed_supervisor_quiesces_before_overlay_work(self):
        for name, boundary in (("provider", provider.supervisor_tick), ("stall", stall.supervisor_tick)):
            with self.subTest(boundary=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / ".cogentnexus-openclaw"
                quiescence.acquire(root, "activation-test", ttl=60)
                with mock.patch.object(stall.legacy, "load_state", side_effect=AssertionError("overlay work ran")), mock.patch.object(
                    provider.provider_events, "ensure_adapter", side_effect=AssertionError("adapter ran")
                ):
                    result = boundary(root, True)
                self.assertEqual(result["result"], "quiesced")
                self.assertEqual(result["action"], "none")

    def test_enable_releases_lease_when_pretransaction_reconciler_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(authority.legacy, "initialize"), mock.patch.object(
                authority.legacy, "load_state", return_value={"mode": "passthrough", "generation": 7}
            ), mock.patch.object(
                authority.legacy, "reconcile_terminal_fences", side_effect=RuntimeError("classifier failed")
            ):
                with self.assertRaisesRegex(RuntimeError, "classifier failed"):
                    authority.enable(root)
            self.assertEqual(quiescence.read(root)["status"], "absent")

    def test_enable_waits_for_native_gateway_readiness_before_plugin_activation(self):
        events = []
        completed = mock.Mock(returncode=0, stdout="{}", stderr="")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            with mock.patch.object(authority.legacy, "initialize"), mock.patch.object(
                authority.legacy, "load_state", return_value={"mode": "passthrough", "generation": 1}
            ), mock.patch.object(
                authority.v091, "_snapshot_file", return_value=None
            ), mock.patch.object(
                authority.legacy, "reconcile_terminal_fences", return_value={}
            ), mock.patch.object(
                authority.v091, "reconcile_direct_delivery_before_recovery", return_value={}
            ), mock.patch.object(
                authority.legacy, "plugin_enabled", side_effect=lambda enabled: events.append(f"plugin:{enabled}")
            ), mock.patch.object(
                authority.v091, "configure_managed_plugin"
            ), mock.patch.object(
                authority.v091, "validate_managed_config"
            ), mock.patch.object(
                authority.legacy, "apply_policy", return_value=False
            ), mock.patch.object(
                authority.legacy, "startup", return_value=completed
            ), mock.patch.object(
                authority.v091, "_wait_native_gateway_ready",
                side_effect=lambda: events.append("gateway-ready") or {"healthy": True, "attempts": 3},
            ) as readiness, mock.patch.object(
                authority.legacy, "transition", return_value={"mode": "managed", "generation": 2}
            ), mock.patch.object(
                authority.legacy, "runtime", side_effect=lambda _root, *args, **_kwargs: events.append("runtime:" + ":".join(args)) or completed
            ), mock.patch.object(
                authority.legacy, "gateway_status", return_value={"healthy": True}
            ), mock.patch.object(
                authority.legacy, "reconcile_default_session", return_value={"ok": True, "created": False}
            ), mock.patch.object(
                authority.v091, "promote_interrupted_direct_v091", return_value=[]
            ), mock.patch.object(
                authority.legacy, "policy_info", return_value={}
            ):
                result = authority._enable_under_lease(root, "2026-09-21T13:00:00Z")

        self.assertEqual(result["mode"], "managed")
        self.assertEqual(readiness.call_count, 3)
        first_ready = events.index("gateway-ready")
        second_ready = events.index("gateway-ready", first_ready + 1)
        third_ready = events.index("gateway-ready", second_ready + 1)
        self.assertLess(first_ready, events.index("plugin:False"))
        self.assertLess(events.index("plugin:False"), second_ready)
        self.assertLess(second_ready, events.index("plugin:True"))
        self.assertLess(events.index("runtime:lifecycle:start"), third_ready)

    def test_interrupted_promotion_requires_fresh_identified_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            path = root / "runtime" / "cogentnexus-openclaw.sqlite3"
            path.parent.mkdir(parents=True)
            db = sqlite3.connect(path)
            db.executescript(
                """
                CREATE TABLE tickets(
                  ticket_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, owner_session_key TEXT NOT NULL,
                  status TEXT NOT NULL, workflow_eligible INTEGER NOT NULL DEFAULT 0, workflow_id TEXT,
                  response_ready_at TEXT, delivery_confirmed_at TEXT, failure_class TEXT, failure_message TEXT,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE ticket_events(
                  event_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL,
                  event_type TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE cnx_sessions(
                  session_key TEXT PRIMARY KEY, state TEXT NOT NULL, generation INTEGER NOT NULL,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL, session_id TEXT
                );
                """
            )
            sessions = [
                ("agent:main:test:stale", "active", 1, "2026-08-18T08:00:00Z", "2026-08-18T08:00:00Z", "old-session"),
                ("agent:main:test:activation-aged", "active", 1, "2026-08-18T09:40:00Z", "2026-08-18T09:50:00Z", "aged-session"),
                ("agent:main:test:ambiguous", "active", 1, "2026-08-18T09:50:00Z", "2026-08-18T10:15:00Z", None),
                ("agent:main:test:fresh", "active", 0, "2026-08-18T09:50:00Z", "2026-08-18T10:10:00Z", "fresh-session"),
            ]
            db.executemany("INSERT INTO cnx_sessions VALUES (?,?,?,?,?,?)", sessions)
            tickets = [
                ("T-stale", "run-stale", sessions[0][0]),
                ("T-activation-aged", "run-activation-aged", sessions[1][0]),
                ("T-ambiguous", "run-ambiguous", sessions[2][0]),
                ("T-fresh", "run-fresh", sessions[3][0]),
            ]
            db.executemany(
                "INSERT INTO tickets(ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,response_ready_at,created_at,updated_at) "
                "VALUES (?,?,?,'accepted',0,NULL,NULL,'2026-08-18T09:51:00Z','2026-08-18T09:51:00Z')",
                tickets,
            )
            db.commit()
            db.close()

            with mock.patch.object(recovery.legacy, "now_iso", return_value="2026-08-18T10:20:00Z"):
                promoted = recovery.promote_interrupted_direct_v091(root, "2026-08-18T10:00:00Z", "activation")
            self.assertEqual(promoted, ["T-fresh"])
            check = sqlite3.connect(path)
            states = dict(check.execute("SELECT ticket_id,workflow_eligible FROM tickets ORDER BY ticket_id"))
            check.close()
            self.assertEqual(states, {"T-activation-aged": 0, "T-ambiguous": 0, "T-fresh": 1, "T-stale": 0})


if __name__ == "__main__":
    unittest.main()
