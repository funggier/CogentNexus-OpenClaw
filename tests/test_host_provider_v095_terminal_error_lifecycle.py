import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


class HostProviderV095TerminalErrorLifecycleTests(unittest.TestCase):
    def test_recovery_quiesces_gateway_and_never_takes_provider_lifecycle_authority(self):
        root = Path("/tmp/cnx-v095-terminal-error-lifecycle")
        claim = {
            "ticket_id": "T-REC",
            "run_id": "R-REC",
            "call_id": "C-REC",
            "state": "recovering",
            "provider": "future-cloud-provider",
            "model": "future-model",
            "error_category": "network",
            "failure_kind": "connection_reset",
        }
        calls = []

        def runtime(_root, *args, **_kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, "{}", "")

        classification = {
            "ticketId": "T-REC",
            "action": "pre-response-recovery-authorized",
            "recoveryAuthority": "terminal-model-call-error",
        }
        with mock.patch.object(hp.legacy, "runtime", side_effect=runtime), \
             mock.patch.object(
                 hp,
                 "classify_quiesced_terminal_error_direct_model_call",
                 return_value=classification,
             ) as classify, \
             mock.patch.object(hp.legacy, "gateway_status", return_value={"healthy": True}), \
             mock.patch.object(hp, "_state_provider") as state_provider, \
             mock.patch.object(hp.providers, "probe") as provider_probe, \
             mock.patch.object(hp.providers, "start") as provider_start:
            result = hp.recover_terminal_error_direct_model_call(root, claim)

        self.assertEqual(result["result"], "terminal-model-call-recovered")
        self.assertEqual(result["classification"], classification)
        classify.assert_called_once_with(root, claim)
        self.assertEqual([call[:2] for call in calls], [
            ("lifecycle", "prepare"),
            ("lifecycle", "stop"),
            ("lifecycle", "start"),
        ])
        self.assertFalse(any("--provider" in call for call in calls))
        for call in calls:
            joined = " ".join(str(part).lower() for part in call)
            self.assertNotIn("timeout", joined)
        state_provider.assert_not_called()
        provider_probe.assert_not_called()
        provider_start.assert_not_called()


if __name__ == "__main__":
    unittest.main()
