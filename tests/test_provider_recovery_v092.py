import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider_recovery_v092 as recovery


class ProviderRecoveryV092Tests(unittest.TestCase):
    def test_recovery_requires_explicit_incident(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            gate = recovery.gate(root, "lmstudio")
            self.assertFalse(gate["incidentOpen"])
            self.assertFalse(gate["allowed"])
            with self.assertRaises(RuntimeError):
                recovery.record_attempt(root, "lmstudio", success=False, reason="no incident")

    def test_lmstudio_circuit_opens_after_two_attempts_in_same_incident(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            opened = recovery.begin_incident(root, "lmstudio", "provider_dead", {"endpoint": "down"})
            self.assertTrue(opened["allowed"])
            self.assertTrue(opened["incidentOpen"])
            incident_id = opened["incidentId"]

            after_first = recovery.record_attempt(root, "lmstudio", success=False, reason="start-1")
            self.assertTrue(after_first["allowed"])
            self.assertEqual(after_first["recoveryAttempts"], 1)
            self.assertEqual(after_first["incidentId"], incident_id)

            after_second = recovery.record_attempt(root, "lmstudio", success=False, reason="start-2")
            self.assertFalse(after_second["allowed"])
            self.assertTrue(after_second["circuitOpen"])
            self.assertEqual(after_second["recoveryAttempts"], 2)
            self.assertEqual(after_second["maximumRecoveriesPerIncident"], 2)

    def test_elapsed_time_cannot_reopen_circuit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            ancient = datetime(2000, 1, 1, tzinfo=timezone.utc)
            recovery.begin_incident(root, "lmstudio", "provider_dead", current=ancient)
            recovery.record_attempt(root, "lmstudio", success=False, reason="one", current=ancient)
            recovery.record_attempt(root, "lmstudio", success=False, reason="two", current=ancient)

            # Authorization does not inspect attempt age. Even decades-old audit
            # timestamps remain part of the same open incident until success or
            # an explicit verified operator boundary closes it.
            gate = recovery.gate(root, "lmstudio")
            self.assertFalse(gate["allowed"])
            self.assertTrue(gate["circuitOpen"])
            self.assertEqual(gate["recoveryAttempts"], 2)

    def test_stable_success_closes_incident_and_next_failure_gets_new_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            first = recovery.begin_incident(root, "lmstudio", "provider_dead")
            recovery.record_attempt(root, "lmstudio", success=True, reason="provider-started")
            closed = recovery.record_stable_success(root, "lmstudio", {"modelCallOutcome": "ok"})
            self.assertFalse(closed["incidentOpen"])
            self.assertFalse(closed["allowed"])

            second = recovery.begin_incident(root, "lmstudio", "provider_dead")
            self.assertTrue(second["allowed"])
            self.assertNotEqual(second["incidentId"], first["incidentId"])
            self.assertEqual(second["recoveryAttempts"], 0)

    def test_manual_verified_transition_closes_incident(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            recovery.begin_incident(root, "ollama", "provider_unreachable")
            recovery.record_attempt(root, "ollama", success=False, reason="attempt")
            closed = recovery.clear_after_manual_transition(root, "ollama")
            self.assertFalse(closed["incidentOpen"])
            self.assertFalse(closed["circuitOpen"])

            reopened = recovery.begin_incident(root, "ollama", "provider_dead")
            self.assertTrue(reopened["allowed"])
            self.assertEqual(reopened["recoveryAttempts"], 0)

    def test_development_timer_state_migrates_without_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = recovery.state_path(root)
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "providers": {
                    "lmstudio": {
                        "attempts": [{"at": "2026-08-21T12:00:00+00:00", "success": False}],
                        "cooldownUntil": "2099-01-01T00:00:00+00:00",
                    }
                },
            }), encoding="utf-8")

            state = recovery.load_state(root)
            self.assertEqual(state["schemaVersion"], 2)
            gate = recovery.gate(root, "lmstudio")
            self.assertFalse(gate["incidentOpen"])
            self.assertFalse(gate["circuitOpen"])
            self.assertFalse(gate["allowed"])

    def test_policy_contains_no_timer_based_recovery_authority(self):
        for name in ("ollama", "lmstudio"):
            policy = recovery.policy(name)
            self.assertIn("maximumRecoveriesPerIncident", policy)
            self.assertNotIn("maximumRecoveriesPerHour", policy)
            self.assertNotIn("cooldownSeconds", policy)
            self.assertNotIn("longRunningGraceSeconds", policy)


if __name__ == "__main__":
    unittest.main()
