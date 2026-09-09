import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
import sys
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


class V095ProviderNeutralSupervisorTests(unittest.TestCase):
    def test_stale_global_provider_state_has_no_supervisor_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            stale_state = {
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "selectedProvider": "lmstudio",
            }

            with mock.patch.object(hp.legacy, "load_state", return_value=stale_state), \
                 mock.patch.object(hp, "_state_provider", return_value="lmstudio") as state_provider, \
                 mock.patch.object(hp, "_set_legacy_ollama_mode") as ollama_mode, \
                 mock.patch.object(hp.providers, "probe", return_value={"healthy": False}) as provider_probe, \
                 mock.patch.object(hp.providers, "start", return_value={"ok": True}) as provider_start, \
                 mock.patch.object(hp.provider_events, "ensure_adapter") as ensure_adapter, \
                 mock.patch.object(hp.provider_events, "consume_failure", return_value=None) as consume_failure, \
                 mock.patch.object(hp.recovery_policy, "load_state", return_value={"providers": {}}), \
                 mock.patch.object(hp.recovery_policy, "begin_incident", return_value={"allowed": False}) as begin_incident, \
                 mock.patch.object(hp, "_run_base_supervisor", return_value={"result": "base"}) as base:
                result = hp.supervisor_tick(root, execute_safe=True)

            self.assertEqual(result, {"result": "base"})
            base.assert_called_once_with(root, True, True)
            state_provider.assert_not_called()
            ollama_mode.assert_not_called()
            provider_probe.assert_not_called()
            provider_start.assert_not_called()
            ensure_adapter.assert_not_called()
            consume_failure.assert_not_called()
            begin_incident.assert_not_called()

    def test_consumes_exact_terminal_model_error_claim_before_legacy_stall_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            managed_state = {"mode": "managed", "desiredGateway": "running"}
            claim = {
                "ticket_id": "T-TERM",
                "run_id": "R-TERM",
                "call_id": "C-TERM",
                "state": "recovering",
                "provider": "future-cloud-provider",
                "model": "future-model",
                "outcome": "error",
                "error_category": "network",
                "failure_kind": "connection_reset",
                "recovery_attempt_count": 1,
            }
            recovered = {
                "result": "terminal-model-call-recovered",
                "classification": {
                    "ticketId": "T-TERM",
                    "action": "pre-response-recovery-authorized",
                    "recoveryAuthority": "terminal-model-call-error",
                },
            }

            with mock.patch.object(hp.legacy, "load_state", return_value=managed_state), \
                 mock.patch.object(hp.authority.supervisor_quiescence, "supervisor_quiesced_result", return_value=None), \
                 mock.patch.object(hp, "claim_terminal_error_direct_model_call", return_value=claim) as terminal_claim, \
                 mock.patch.object(hp, "recover_terminal_error_direct_model_call", return_value=recovered) as recover_terminal, \
                 mock.patch.object(hp, "claim_expired_direct_model_call") as expired_claim, \
                 mock.patch.object(hp, "_run_base_supervisor", return_value={"result": "base"}) as base:
                result = hp.supervisor_tick(root, execute_safe=True)

            self.assertEqual(result, recovered)
            terminal_claim.assert_called_once_with(root)
            recover_terminal.assert_called_once_with(root, claim)
            expired_claim.assert_not_called()
            base.assert_not_called()


if __name__ == "__main__":
    unittest.main()
