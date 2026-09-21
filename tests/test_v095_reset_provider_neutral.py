import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(SCRIPTS))

import reset_v095


class V095ResetProviderNeutralTests(unittest.TestCase):
    def test_run_host_uses_extended_budget_for_enable_only(self):
        root = Path("C:/tmp/cnx-reset-test")
        completed = mock.Mock(returncode=0, stdout="", stderr="")
        with mock.patch.object(reset_v095.base, "run", return_value=completed) as run:
            reset_v095._run_host(root, "enable")
            self.assertEqual(run.call_args.kwargs["timeout"], 600)

            reset_v095._run_host(root, "disable")
            self.assertEqual(run.call_args.kwargs["timeout"], 300)

    def test_retry_timeout_reclaims_dead_enable_lease_before_fail_closed_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            calls = []
            failed = mock.Mock(returncode=1, stdout="first transient", stderr="ETIMEDOUT")
            ok = mock.Mock(returncode=0, stdout="{}", stderr="")

            def run_host(_root, command):
                calls.append(command)
                if command == "enable" and calls.count("enable") == 1:
                    return failed
                if command == "enable":
                    raise subprocess.TimeoutExpired(cmd=["host_provider_v092.py", "enable"], timeout=600)
                return ok

            with (
                mock.patch.object(reset_v095.namespace_ownership, "verify_manifest", return_value={"version": "0.9.6"}),
                mock.patch.object(reset_v095, "resolve_installed_bootstrap", return_value=root / "bootstrap-ticket-db.mjs"),
                mock.patch.object(reset_v095.base, "confirm", return_value=True),
                mock.patch.object(reset_v095, "_run_host", side_effect=run_host),
                mock.patch.object(reset_v095.openclaw_route, "restore_native", return_value={"ok": True}),
                mock.patch.object(reset_v095, "bootstrap_ticket_database"),
                mock.patch.object(reset_v095.supervisor_quiescence, "reclaim_dead_enable_owner", return_value={"reclaimed": True, "reason": "dead-enable-owner"}) as reclaim,
                mock.patch.object(reset_v095.base, "disable_startup"),
                mock.patch.object(reset_v095.base, "reset_plugin_configuration"),
                mock.patch.object(reset_v095.base, "verify_plugin_loaded", return_value={"status": "loaded"}),
                mock.patch.object(reset_v095.base, "gateway_health", return_value={"healthy": True}),
                mock.patch.object(reset_v095.runtime_boundary, "activate_current_config", return_value={"ok": True}),
                mock.patch("reset_v095.shutil.rmtree"),
            ):
                code = reset_v095.reset(root)

            self.assertEqual(code, 1)
            reclaim.assert_called_once_with(root)
            self.assertGreaterEqual(calls.count("disable"), 2)

    def test_reset_never_selects_or_commits_provider(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fake_process = mock.Mock(returncode=0)
            with mock.patch.object(reset_v095.namespace_ownership, "verify_manifest", return_value={"version": "0.9.4"}), \
                 mock.patch.object(reset_v095, "resolve_installed_bootstrap", return_value=root / "bootstrap-ticket-db.mjs"), \
                 mock.patch.object(reset_v095.base, "confirm", return_value=True), \
                 mock.patch.object(reset_v095, "_run_host", return_value=fake_process) as run_host, \
                 mock.patch.object(reset_v095.openclaw_route, "restore_native", return_value={"ok": True}) as restore_native, \
                 mock.patch.object(reset_v095.openclaw_route, "begin") as route_begin, \
                 mock.patch.object(reset_v095.openclaw_route, "commit") as route_commit, \
                 mock.patch.object(reset_v095.openclaw_route, "plan") as route_plan, \
                 mock.patch.object(reset_v095, "bootstrap_ticket_database"), \
                 mock.patch.object(reset_v095.base, "disable_startup"), \
                 mock.patch.object(reset_v095.base, "reset_plugin_configuration"), \
                 mock.patch.object(reset_v095.base, "verify_plugin_loaded", return_value={"status": "loaded"}), \
                 mock.patch.object(reset_v095.base, "gateway_health", return_value={"healthy": True}), \
                 mock.patch.object(reset_v095.runtime_boundary, "activate_current_config", return_value={"ok": True}), \
                 mock.patch("reset_v095.shutil.rmtree") as rmtree, \
                 mock.patch.object(reset_v095, "provider", create=True) as provider_module:
                code = reset_v095.reset(root)

            self.assertEqual(code, 0)
            restore_native.assert_called_once_with(root)
            route_begin.assert_not_called()
            route_commit.assert_not_called()
            route_plan.assert_not_called()
            provider_module.probe.assert_not_called()
            provider_module.start.assert_not_called()
            provider_module.stop.assert_not_called()
            rmtree.assert_called_once_with(root)
            run_host.assert_any_call(root, "disable")
            run_host.assert_any_call(root, "init")
            run_host.assert_any_call(root, "enable")

    def test_reset_retries_one_transactional_enable_after_gateway_recovers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            calls = []
            failed = mock.Mock(returncode=1, stdout="first enable transient", stderr="ETIMEDOUT")
            succeeded = mock.Mock(returncode=0, stdout="managed", stderr="")
            ok = mock.Mock(returncode=0, stdout="{}", stderr="")

            def run_host(_root, command):
                calls.append(command)
                if command == "enable":
                    return failed if calls.count("enable") == 1 else succeeded
                return ok

            with (
                mock.patch.object(reset_v095.namespace_ownership, "verify_manifest", return_value={"version": "0.9.6"}),
                mock.patch.object(reset_v095, "resolve_installed_bootstrap", return_value=root / "bootstrap-ticket-db.mjs"),
                mock.patch.object(reset_v095.base, "confirm", return_value=True),
                mock.patch.object(reset_v095, "_run_host", side_effect=run_host),
                mock.patch.object(reset_v095.openclaw_route, "restore_native", return_value={"ok": True}),
                mock.patch.object(reset_v095, "bootstrap_ticket_database"),
                mock.patch.object(reset_v095.base, "disable_startup"),
                mock.patch.object(reset_v095.base, "reset_plugin_configuration"),
                mock.patch.object(reset_v095.base, "verify_plugin_loaded", return_value={"status": "loaded"}),
                mock.patch.object(reset_v095.base, "gateway_health", side_effect=[{"healthy": True}, {"healthy": True}]) as gateway_health,
                mock.patch.object(reset_v095.runtime_boundary, "activate_current_config", return_value={"ok": True}),
                mock.patch("reset_v095.shutil.rmtree"),
            ):
                code = reset_v095.reset(root)

            self.assertEqual(code, 0)
            self.assertEqual(calls.count("enable"), 2)
            self.assertGreaterEqual(gateway_health.call_count, 2)

    def test_reset_recovers_one_timed_out_enable_through_disabled_gateway_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            calls = []
            succeeded = mock.Mock(returncode=0, stdout="managed", stderr="")
            ok = mock.Mock(returncode=0, stdout="{}", stderr="")

            def run_host(_root, command):
                calls.append(command)
                if command == "enable" and calls.count("enable") == 1:
                    raise subprocess.TimeoutExpired(cmd=["host_provider_v092.py", "enable"], timeout=300)
                if command == "enable":
                    return succeeded
                return ok

            with (
                mock.patch.object(reset_v095.namespace_ownership, "verify_manifest", return_value={"version": "0.9.6"}),
                mock.patch.object(reset_v095, "resolve_installed_bootstrap", return_value=root / "bootstrap-ticket-db.mjs"),
                mock.patch.object(reset_v095.base, "confirm", return_value=True),
                mock.patch.object(reset_v095, "_run_host", side_effect=run_host),
                mock.patch.object(reset_v095.openclaw_route, "restore_native", return_value={"ok": True}),
                mock.patch.object(reset_v095, "bootstrap_ticket_database"),
                mock.patch.object(reset_v095.supervisor_quiescence, "reclaim_dead_enable_owner", return_value={"reclaimed": True, "reason": "dead-enable-owner"}) as reclaim,
                mock.patch.object(reset_v095.base, "disable_startup"),
                mock.patch.object(reset_v095.base, "reset_plugin_configuration"),
                mock.patch.object(reset_v095.base, "verify_plugin_loaded", return_value={"status": "loaded"}),
                mock.patch.object(reset_v095.base, "gateway_health", side_effect=[{"healthy": True}, {"healthy": True}]) as gateway_health,
                mock.patch.object(reset_v095.runtime_boundary, "activate_current_config", return_value={"ok": True}),
                mock.patch("reset_v095.shutil.rmtree"),
            ):
                code = reset_v095.reset(root)

            self.assertEqual(code, 0)
            self.assertEqual(calls.count("enable"), 2)
            self.assertGreaterEqual(calls.count("disable"), 2)
            reclaim.assert_called_once_with(root)
            self.assertGreaterEqual(gateway_health.call_count, 2)

    def test_reset_source_has_no_provider_transition_authority(self):
        source = Path(reset_v095.__file__).read_text(encoding="utf-8")
        self.assertNotIn("resolve_fresh_provider", source)
        self.assertNotIn("selectedProvider", source)
        self.assertNotIn("desiredProvider", source)
        self.assertNotIn("openclaw_route.begin", source)
        self.assertNotIn("openclaw_route.commit", source)
        self.assertNotIn("provider.probe", source)


if __name__ == "__main__":
    unittest.main()
