import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider_recovery_v092 as recovery


class ProviderRecoveryV092Tests(unittest.TestCase):
    def test_lmstudio_circuit_opens_after_bounded_attempts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            first = recovery.record_attempt(root, "lmstudio", success=False, reason="first", current=start)
            self.assertTrue(first["allowed"])
            second = recovery.record_attempt(
                root, "lmstudio", success=False, reason="second",
                current=start + timedelta(minutes=1),
            )
            self.assertFalse(second["allowed"])
            self.assertTrue(second["circuitOpen"])
            self.assertEqual(second["recoveriesLastHour"], 2)
            self.assertEqual(second["cooldownSeconds"], 900)

    def test_old_attempts_age_out_of_hour_window(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            recovery.record_attempt(root, "ollama", success=True, reason="old", current=start)
            gate = recovery.gate(root, "ollama", current=start + timedelta(hours=2))
            self.assertTrue(gate["allowed"])
            self.assertEqual(gate["recoveriesLastHour"], 0)

    def test_manual_verified_transition_clears_automatic_recovery_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            recovery.record_attempt(root, "lmstudio", success=False, reason="one", current=start)
            recovery.record_attempt(
                root, "lmstudio", success=False, reason="two",
                current=start + timedelta(minutes=1),
            )
            self.assertFalse(recovery.gate(root, "lmstudio", current=start + timedelta(minutes=2))["allowed"])
            recovery.clear_after_manual_transition(root, "lmstudio")
            self.assertTrue(recovery.gate(root, "lmstudio")["allowed"])

    def test_lmstudio_has_long_running_grace_policy(self):
        policy = recovery.policy("lmstudio")
        self.assertEqual(policy["longRunningGraceSeconds"], 600)
        self.assertGreater(policy["cooldownSeconds"], 0)
        self.assertGreater(policy["maximumRecoveriesPerHour"], 0)


if __name__ == "__main__":
    unittest.main()
