from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_v095_idle_quiescence.py"


class CheckV095IdleQuiescenceTests(unittest.TestCase):
    def _run(self, log: str, state: str | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            root.mkdir(parents=True)
            log_path = root / "host.log"
            log_path.write_text(log, encoding="utf-8")
            if state is not None:
                (root / "host-state.json").write_text(state, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "--log", str(log_path), "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

    def test_all_idle_window_is_pass_without_heavy_actions(self):
        output = self._run(
            """
{"result":"idle","action":"none","wakeReason":"idle/no-actionable-work","heavyPath":false}
{"result":"idle","action":"none","wakeReason":"idle/no-actionable-work","heavyPath":false}
"""
        )
        self.assertEqual(output["verdict"], "PASS")
        self.assertEqual(output["heavySupervisorCalls"], 0)
        self.assertEqual(output["providerRecoveryActions"], 0)
        self.assertEqual(output["configMutations"], 0)
        self.assertEqual(output["gatewayLifecycleActions"], 0)
        self.assertEqual(output["idleTicks"], 2)

    def test_one_heavy_wake_is_observed(self):
        output = self._run(
            """
{"result":"idle","action":"none","wakeReason":"idle/no-actionable-work","heavyPath":false}
{"result":"recovery","action":"delivery","wakeAuthority":"delivery","heavyPath":true}
"""
        )
        self.assertEqual(output["verdict"], "PASS")
        self.assertEqual(output["heavySupervisorCalls"], 1)
        self.assertEqual(output["idleTicks"], 1)

    def test_missing_evidence_is_indeterminate(self):
        output = self._run("")
        self.assertEqual(output["verdict"], "INDETERMINATE")

    def test_checker_is_read_only_with_state_file(self):
        state = '{"mode":"managed","desiredGateway":"running","generation":3}\n'
        output = self._run(
            '{"result":"idle","action":"none","wakeReason":"idle/no-actionable-work","heavyPath":false}\n',
            state,
        )
        self.assertEqual(output["verdict"], "PASS")

    def test_idle_window_with_repeated_heavy_activity_is_fail(self):
        output = self._run(
            """
{"result":"idle","action":"none","wakeReason":"idle/no-actionable-work","heavyPath":false}
{"result":"recovery","action":"delivery","wakeAuthority":"delivery","heavyPath":true}
{"result":"recovery","action":"delivery","wakeAuthority":"delivery","heavyPath":true}
"""
        )
        self.assertEqual(output["verdict"], "FAIL")
        self.assertGreaterEqual(output["heavySupervisorCalls"], 2)


if __name__ == "__main__":
    unittest.main()
