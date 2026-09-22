from __future__ import annotations

import importlib.util
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "host_v091.py"
spec = importlib.util.spec_from_file_location("cnx_host_v091", SCRIPT)
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

    @staticmethod
    def completed(stdout="{}", returncode=0, stderr=""):
        return subprocess.CompletedProcess(["stub"], returncode, stdout, stderr)

    def seed_passthrough(self, root: Path):
        cnx.legacy.initialize(root)
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "generation": 40,
        })

    def seed_managed(self, root: Path):
        return cnx.legacy.save_state(root, {
            "schemaVersion": 1,
            "mode": "managed",
            "desiredGateway": "running",
            "desiredProvider": "running",
            "generation": 2,
        })

    def stub_enable_dependencies(self):
        self.patch(cnx.legacy, "plugin_enabled", lambda _enabled: None)
        self.patch(cnx, "configure_managed_plugin", lambda: None)
        self.patch(cnx, "validate_managed_config", lambda: None)
        self.patch(cnx.legacy, "apply_policy", lambda _workspace, _root: True)
        self.patch(cnx.legacy, "startup", lambda *_args, **_kwargs: self.completed('{"enabled":true}'))
        self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed('{"ok":true}'))
        self.patch(cnx.legacy, "gateway_status", lambda: {"healthy": True})
        self.patch(cnx.runtime_boundary, "activate_current_config", lambda: {"ok": True, "phase": "verified"})
        self.patch(cnx.legacy, "reconcile_default_session", lambda: {"ok": True, "created": False})
        self.patch(cnx.legacy, "promote_interrupted_direct", lambda *_args, **_kwargs: [])

    def test_enable_commits_managed_only_after_activation_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            before = self.seed_passthrough(root)
            self.stub_enable_dependencies()
            runtime_calls = []
            self.patch(
                cnx.legacy,
                "runtime",
                lambda _root, *args, **_kwargs: runtime_calls.append(args) or self.completed('{"ok":true}'),
            )

            result = cnx.enable(root)
            after = cnx.legacy.load_state(root)

            self.assertEqual(result["mode"], "managed")
            self.assertTrue(result["transactional"])
            self.assertEqual(after["mode"], "managed")
            self.assertEqual(after["cnxMode"], "active")
            self.assertEqual(after["desiredGateway"], "running")
            self.assertEqual(after["providerOwnership"], "openclaw")
            self.assertNotIn("desiredProvider", after)
            self.assertNotIn("selectedProvider", after)
            self.assertNotIn("providerTransition", after)
            self.assertEqual(after["generation"], before["generation"] + 1)
            self.assertNotIn(
                ("lifecycle", "start", "--provider"),
                runtime_calls,
                "v0.9.5 enable must leave provider lifecycle/routing under OpenClaw ownership",
            )

    def test_enable_reconciles_terminal_fences_before_plugin_activation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            self.seed_passthrough(root)
            self.stub_enable_dependencies()
            calls = []
            fences = {
                "cancelledOutboxSuppressed": 2,
                "terminalRecoverySuppressed": 3,
                "cancelledClassificationNormalized": 1,
            }
            self.patch(cnx.legacy, "reconcile_terminal_fences", lambda _root: calls.append("terminal-fence") or fences)
            self.patch(cnx.legacy, "plugin_enabled", lambda enabled: calls.append(f"plugin:{enabled}"))

            result = cnx.enable(root)

            self.assertEqual(calls[0], "terminal-fence")
            self.assertEqual(calls[1], "plugin:False")
            self.assertIn("plugin:True", calls)
            self.assertEqual(result["terminalFences"], fences)

    def test_enable_failure_preserves_passthrough_generation_and_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            root = workspace / ".cogentnexus-openclaw"
            workspace.mkdir(parents=True)
            agents = workspace / "AGENTS.md"
            agents.write_text("# Native policy\n", encoding="utf-8")
            before = self.seed_passthrough(root)

            self.patch(cnx, "configure_managed_plugin", lambda: None)
            self.patch(cnx, "validate_managed_config", lambda: None)
            self.patch(cnx.legacy, "apply_policy", lambda _workspace, _root: agents.write_text("managed\n", encoding="utf-8") or True)
            calls = []
            def plugin(enabled):
                calls.append(enabled)
                if enabled:
                    raise RuntimeError("injected plugin enable failure")
            self.patch(cnx.legacy, "plugin_enabled", plugin)
            self.patch(cnx.legacy, "runtime", lambda *_args, **_kwargs: self.completed())
            self.patch(cnx, "_restore_native_gateway", lambda: {"exitCode": 0})

            with self.assertRaisesRegex(RuntimeError, "transactional enable failed"):
                cnx.enable(root)

            after = cnx.legacy.load_state(root)
            self.assertEqual(after["mode"], "passthrough")
            self.assertEqual(after["generation"], before["generation"])
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Native policy\n")
            self.assertEqual(calls, [False, True, False])

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

    def test_confirmed_gateway_hang_is_bounded_without_heavy_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            calls = []
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx, "ollama_fast_probe", lambda: self.fail("provider probe must not precede gateway recovery"))
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "gateway_startup_grace", lambda: {"active": False, "reason": "no-active-boot"})
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: calls.append("restart") or {"attempted": True, "exitCode": 0})
            self.patch(cnx, "LEGACY_SUPERVISOR_TICK", lambda _root, execute: calls.append("heavy") or {"result":"recovery","execute":execute})

            result = cnx.supervisor_tick(root, True)
            self.assertEqual(calls, ["restart"])
            self.assertEqual(result["result"], "gateway-recovery")
            self.assertEqual(result["hardHangRecovery"], {"attempted": True, "exitCode": 0})
            self.assertFalse(result["heavyPath"])

    def test_active_openclaw_boot_grace_suppresses_false_hard_hang_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: False)
            self.patch(cnx.time, "sleep", lambda _seconds: None)
            self.patch(cnx, "gateway_startup_grace", lambda: {
                "active": True,
                "bootId": "boot-427",
                "ageSeconds": 70.0,
                "graceSeconds": 180.0,
                "reason": "active-boot-grace",
            })
            self.patch(cnx, "_restart_unresponsive_gateway", lambda _root: self.fail("active startup grace must not restart Gateway"))

            result = cnx.supervisor_tick(root, True)

            self.assertEqual(result["result"], "gateway-starting")
            self.assertEqual(result["action"], "none")
            self.assertEqual(result["wakeReason"], "gateway/startup-grace")
            self.assertEqual(result["startupGrace"]["bootId"], "boot-427")
            self.assertFalse(result["heavyPath"])

    def test_gateway_startup_grace_reads_openclaw_boot_lifecycle_and_expires(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "openclaw-state"
            database = state_dir / "state" / "openclaw.sqlite"
            database.parent.mkdir(parents=True)
            db = sqlite3.connect(database)
            db.execute("CREATE TABLE gateway_boot_lifecycle(boot_id TEXT,pid INTEGER,started_at_ms INTEGER,completed_at_ms INTEGER,outcome TEXT,startup_reason TEXT,reason TEXT)")
            db.execute("INSERT INTO gateway_boot_lifecycle VALUES(?,?,?,?,?,?,?)", ("boot-live", 123, 1_000_000, None, None, None, None))
            db.commit()
            db.close()
            with mock.patch.dict(os.environ, {"OPENCLAW_STATE_DIR": str(state_dir)}):
                active = cnx.gateway_startup_grace(now_ms=1_070_000)
                expired = cnx.gateway_startup_grace(now_ms=1_181_000)

            self.assertTrue(active["active"])
            self.assertEqual(active["bootId"], "boot-live")
            self.assertEqual(active["ageSeconds"], 70.0)
            self.assertFalse(expired["active"])
            self.assertEqual(expired["reason"], "active-boot-grace-expired")

    def test_current_gateway_boot_boundary_matches_live_status_pid(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "openclaw-state"
            database = state_dir / "state" / "openclaw.sqlite"
            database.parent.mkdir(parents=True)
            db = sqlite3.connect(database)
            db.execute(
                "CREATE TABLE gateway_boot_lifecycle("
                "boot_id TEXT,pid INTEGER,started_at_ms INTEGER,"
                "completed_at_ms INTEGER,outcome TEXT,startup_reason TEXT,reason TEXT)"
            )
            db.execute(
                "INSERT INTO gateway_boot_lifecycle VALUES(?,?,?,?,?,?,?)",
                ("boot-old", 111, 1000, None, None, None, None),
            )
            db.execute(
                "INSERT INTO gateway_boot_lifecycle VALUES(?,?,?,?,?,?,?)",
                ("boot-live", 222, 2000, None, None, None, None),
            )
            db.commit()
            db.close()

            self.patch(
                cnx.legacy,
                "gateway_status",
                lambda: {
                    "healthy": True,
                    "stdout": "Runtime: running (pid 222, last run 0, Gateway process detected for gateway port 18789.)",
                },
            )
            with mock.patch.dict(os.environ, {"OPENCLAW_STATE_DIR": str(state_dir)}):
                boundary = cnx._current_gateway_boot_boundary()

            self.assertEqual(boundary["bootId"], "boot-live")
            self.assertEqual(boundary["pid"], 222)
            self.assertEqual(boundary["startedAtMs"], 2000)
            self.assertEqual(boundary["startedAt"], "1970-01-01T00:00:02+00:00")
            self.assertEqual(boundary["previousBootId"], "boot-old")
            self.assertEqual(boundary["previousPid"], 111)
            self.assertEqual(boundary["previousStartedAtMs"], 1000)
            self.assertEqual(boundary["previousStartedAt"], "1970-01-01T00:00:01+00:00")

    def test_current_gateway_boot_orphan_triggers_exact_boundary_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            boundary = {
                "bootId": "boot-current",
                "pid": 4321,
                "startedAt": "2026-09-22T11:22:30+00:00",
            }
            evidence = {
                "boundary": boundary,
                "orphans": [{"ticket_id": "T-OLD", "call_id": "C-OLD"}],
            }
            recovered = {
                "result": "gateway-boundary-direct-recovery",
                "interruptedDirectRecoveries": [{"ticketId": "T-OLD"}],
            }

            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "_gateway_boundary_orphan_evidence", lambda _root: evidence)
            self.patch(
                cnx,
                "_recover_gateway_boundary_orphans",
                lambda _root, found: recovered if found is evidence else self.fail("wrong evidence"),
            )
            self.patch(cnx, "classify_wake", lambda _root: self.fail("orphan recovery must precede idle wake classification"))

            result = cnx.supervisor_tick(root, True)

            self.assertEqual(result, recovered)

    def test_current_gateway_boot_without_old_active_call_preserves_idle_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            self.patch(cnx, "gateway_fast_probe", lambda: True)
            self.patch(cnx, "_gateway_boundary_orphan_evidence", lambda _root: None)
            self.patch(
                cnx,
                "classify_wake",
                lambda _root: type("Decision", (), {
                    "actionable": False,
                    "authority": "none",
                    "work_id": None,
                    "reason": "idle",
                })(),
            )

            result = cnx.supervisor_tick(root, True)

            self.assertEqual(result["result"], "idle")
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



    def test_confirmed_gateway_restart_classifies_active_direct_calls_while_quiesced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            calls = []

            def runtime(_root, *args, **_kwargs):
                calls.append(args[:2])
                return self.completed('{"ok":true}')

            evidence = {
                "kind": "confirmed-hard-hang-current-boot",
                "boundary": {"bootId": "boot-current", "startedAt": "2026-09-22T11:00:00+00:00"},
                "orphans": [{"ticket_id": "T-GATEWAY", "call_id": "C-GATEWAY"}],
            }
            self.patch(cnx.legacy, "runtime", runtime)
            with mock.patch.object(
                cnx,
                "_gateway_current_direct_evidence",
                side_effect=lambda _root: calls.append(("evidence", "current")) or evidence,
                create=True,
            ) as current_evidence, mock.patch.object(
                cnx,
                "_recover_gateway_interrupted_direct_calls",
                side_effect=lambda _root, found: calls.append(("classify", "direct")) or [{"ticketId": "T-GATEWAY"}],
                create=True,
            ) as classify:
                result = cnx._restart_unresponsive_gateway(root)

            self.assertEqual(
                calls,
                [
                    ("evidence", "current"),
                    ("lifecycle", "prepare"),
                    ("lifecycle", "stop"),
                    ("classify", "direct"),
                    ("lifecycle", "start"),
                ],
            )
            current_evidence.assert_called_once_with(root)
            classify.assert_called_once_with(root, evidence)
            self.assertEqual(result["interruptedDirectRecoveries"], [{"ticketId": "T-GATEWAY"}])

    def test_gateway_restart_restores_gateway_if_interruption_classification_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            self.seed_managed(root)
            calls = []

            def runtime(_root, *args, **_kwargs):
                calls.append(args[:2])
                return self.completed('{"ok":true}')

            evidence = {
                "kind": "confirmed-hard-hang-current-boot",
                "boundary": {"bootId": "boot-current", "startedAt": "2026-09-22T11:00:00+00:00"},
                "orphans": [{"ticket_id": "T-PARTIAL", "call_id": "C-PARTIAL"}],
            }
            self.patch(cnx.legacy, "runtime", runtime)
            with mock.patch.object(
                cnx,
                "_gateway_current_direct_evidence",
                return_value=evidence,
                create=True,
            ), mock.patch.object(
                cnx,
                "_recover_gateway_interrupted_direct_calls",
                side_effect=RuntimeError("classification failed"),
                create=True,
            ):
                with self.assertRaisesRegex(RuntimeError, "classification failed"):
                    cnx._restart_unresponsive_gateway(root)

            self.assertEqual(
                calls,
                [
                    ("lifecycle", "prepare"),
                    ("lifecycle", "stop"),
                    ("lifecycle", "start"),
                ],
            )

if __name__ == "__main__":
    unittest.main()
