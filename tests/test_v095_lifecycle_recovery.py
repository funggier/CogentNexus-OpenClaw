import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
import sys
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_provider_v092 as hp


CLAIM = {
    "ticket_id": "T-LIFECYCLE",
    "run_id": "R-LIFECYCLE",
    "call_id": "C-LIFECYCLE",
}


class V095LifecycleRecoveryTests(unittest.TestCase):
    def test_prepare_failure_does_not_attempt_stop_or_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            calls = []

            def runtime(_root, *args, timeout=180, check=True):
                calls.append(args)
                if args[:2] == ("lifecycle", "prepare"):
                    raise RuntimeError("prepare failed")
                raise AssertionError(f"unexpected lifecycle call: {args!r}")

            with mock.patch.object(hp.legacy, "runtime", side_effect=runtime):
                with self.assertRaisesRegex(RuntimeError, "prepare failed"):
                    hp.recover_terminal_error_direct_model_call(root, CLAIM)

            self.assertEqual([args[:2] for args in calls], [("lifecycle", "prepare")])

    def test_classification_failure_after_stop_restores_gateway(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            calls = []

            def runtime(_root, *args, timeout=180, check=True):
                calls.append(args)
                if args[:2] in {("lifecycle", "prepare"), ("lifecycle", "stop"), ("lifecycle", "start")}:
                    return {"result": args[1]}
                raise AssertionError(f"unexpected lifecycle call: {args!r}")

            with mock.patch.object(hp.legacy, "runtime", side_effect=runtime), \
                 mock.patch.object(hp, "classify_quiesced_terminal_error_direct_model_call", side_effect=RuntimeError("classification failed")):
                with self.assertRaisesRegex(RuntimeError, "classification failed"):
                    hp.recover_terminal_error_direct_model_call(root, CLAIM)

            self.assertEqual([args[:2] for args in calls], [
                ("lifecycle", "prepare"),
                ("lifecycle", "stop"),
                ("lifecycle", "start"),
            ])

    def test_start_failure_retries_gateway_restore_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            calls = []
            start_attempts = 0

            def runtime(_root, *args, timeout=180, check=True):
                nonlocal start_attempts
                calls.append(args)
                if args[:2] == ("lifecycle", "prepare"):
                    return {"result": "prepared"}
                if args[:2] == ("lifecycle", "stop"):
                    return {"result": "stopped"}
                if args[:2] == ("lifecycle", "start"):
                    start_attempts += 1
                    if start_attempts == 1:
                        raise RuntimeError("first gateway start failed")
                    return {"result": "started"}
                raise AssertionError(f"unexpected lifecycle call: {args!r}")

            with mock.patch.object(hp.legacy, "runtime", side_effect=runtime), \
                 mock.patch.object(hp, "classify_quiesced_terminal_error_direct_model_call", return_value={"action": "authorized"}), \
                 mock.patch.object(hp.legacy, "gateway_status", return_value={"healthy": True}):
                with self.assertRaisesRegex(RuntimeError, "first gateway start failed"):
                    hp.recover_terminal_error_direct_model_call(root, CLAIM)

            self.assertEqual([args[:2] for args in calls], [
                ("lifecycle", "prepare"),
                ("lifecycle", "stop"),
                ("lifecycle", "start"),
                ("lifecycle", "start"),
            ])

    def test_unhealthy_gateway_after_start_does_not_duplicate_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogentnexus-openclaw"
            root.mkdir()
            calls = []

            def runtime(_root, *args, timeout=180, check=True):
                calls.append(args)
                if args[:2] == ("lifecycle", "prepare"):
                    return {"result": "prepared"}
                if args[:2] == ("lifecycle", "stop"):
                    return {"result": "stopped"}
                if args[:2] == ("lifecycle", "start"):
                    return {"result": "started"}
                raise AssertionError(f"unexpected lifecycle call: {args!r}")

            with mock.patch.object(hp.legacy, "runtime", side_effect=runtime), \
                 mock.patch.object(hp, "classify_quiesced_terminal_error_direct_model_call", return_value={"action": "authorized"}), \
                 mock.patch.object(hp.legacy, "gateway_status", return_value={"healthy": False, "error": "gateway unhealthy"}):
                result = hp.recover_terminal_error_direct_model_call(root, CLAIM)

            self.assertEqual(result["result"], "terminal-model-call-recovery-failed")
            self.assertEqual([args[:2] for args in calls], [
                ("lifecycle", "prepare"),
                ("lifecycle", "stop"),
                ("lifecycle", "start"),
            ])


if __name__ == "__main__":
    unittest.main()
