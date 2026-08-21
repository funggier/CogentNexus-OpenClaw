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
    def test_lmstudio_cooldown_blocks_immediate_second_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            after_first = recovery.record_attempt(
                root, "lmstudio", success=False, reason="first", current=start
            )
            self.assertFalse(after_first["allowed"])
            self.assertTrue(after_first["cooldownActive"])
            self.assertFalse(after_first["limitReached"])
            self.assertEqual(after_first["recoveriesLastHour"], 1)

            during_cooldown = recovery.gate(
                root, "lmstudio", current=start + timedelta(minutes=14)
            )
            self.assertFalse(during_cooldown["allowed"])
            self.assertTrue(during_cooldown["cooldownActive"])

            after_cooldown = recovery.gate(
                root, "lmstudio", current=start + timedelta(minutes=16)
            )
            self.assertTrue(after_cooldown["allowed"])
            self.assertFalse(after_cooldown["cooldownActive"])

    def test_lmstudio_rolling_hour_limit_blocks_after_second_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            recovery.record_attempt(root, "lmstudio", success=False, reason="first", current=start)
            second_time = start + timedelta(minutes=16)
            self.assertTrue(recovery.gate(root, "lmstudio", current=second_time)["allowed"])
            after_second = recovery.record_attempt(
                root, "lmstudio", success=False, reason="second", current=second_time
            )
            self.assertFalse(after_second["allowed"])
            self.assertTrue(after_second["circuitOpen"])
            self.assertTrue(after_second["limitReached"])
            self.assertEqual(after_second["recoveriesLastHour"], 2)
            self.assertEqual(after_second["cooldownSeconds"], 900)

            # Even after the second attempt's 15-minute cooldown expires, the
            # independent rolling-hour limit remains authoritative.
            still_limited = recovery.gate(
                root, "lmstudio", current=start + timedelta(minutes=40)
            )
            self.assertFalse(still_limited["allowed"])
            self.assertFalse(still_limited["cooldownActive"])
            self.assertTrue(still_limited["limitReached"])

    def test_old_attempts_and_cooldown_age_out(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            recovery.record_attempt(root, "ollama", success=True, reason="old", current=start)
            gate = recovery.gate(root, "ollama", current=start + timedelta(hours=2))
            self.assertTrue(gate["allowed"])
            self.assertEqual(gate["recoveriesLastHour"], 0)
            self.assertFalse(gate["cooldownActive"])

    def test_manual_verified_transition_clears_automatic_recovery_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            start = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
            recovery.record_attempt(root, "lmstudio", success=False, reason="one", current=start)
            self.assertFalse(recovery.gate(root, "lmstudio", current=start + timedelta(minutes=1))["allowed"])
            recovery.clear_after_manual_transition(root, "lmstudio")
            self.assertTrue(recovery.gate(root, "lmstudio")["allowed"])

    def test_lmstudio_has_long_running_grace_policy(self):
        policy = recovery.policy("lmstudio")
        self.assertEqual(policy["longRunningGraceSeconds"], 600)
        self.assertGreater(policy["cooldownSeconds"], 0)
        self.assertGreater(policy["maximumRecoveriesPerHour"], 0)


if __name__ == "__main__":
    unittest.main()
