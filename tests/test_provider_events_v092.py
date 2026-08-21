import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider_events_v092 as events


class ProviderEventsV092Tests(unittest.TestCase):
    def test_lmstudio_runtime_prompt_progress_is_parsed_as_suppression_evidence(self):
        parsed = events.parse_runtime_line("Prompt processing progress: 87.0%")
        self.assertIsNotNone(parsed)
        event_type, evidence = parsed
        self.assertEqual(event_type, "prompt_progress")
        self.assertEqual(evidence["percent"], 87.0)

        parsed = events.parse_runtime_line("llama prompt eval progress = 35%")
        self.assertEqual(parsed[0], "prompt_progress")
        self.assertEqual(parsed[1]["percent"], 35.0)

    def test_irrelevant_runtime_line_does_not_create_event(self):
        self.assertIsNone(events.parse_runtime_line("server listening on port 1234"))

    def test_failure_event_is_consumed_exactly_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            first = events.publish(root, "lmstudio", "provider_dead", {"source": "runtime-eof"})
            self.assertGreater(first["sequence"], 0)
            consumed = events.consume_failure(root, "lmstudio")
            self.assertEqual(consumed["sequence"], first["sequence"])
            self.assertIsNone(events.consume_failure(root, "lmstudio"))

            second = events.publish(root, "lmstudio", "provider_unreachable", {"source": "connection-refused"})
            consumed_second = events.consume_failure(root, "lmstudio")
            self.assertEqual(consumed_second["sequence"], second["sequence"])

    def test_progress_event_never_becomes_failure_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            event = events.publish(root, "lmstudio", "prompt_progress", {"percent": 52.0})
            progress = events.latest_progress(root, "lmstudio")
            self.assertEqual(progress["sequence"], event["sequence"])
            self.assertEqual(progress["evidence"]["percent"], 52.0)
            self.assertIsNone(events.consume_failure(root, "lmstudio"))

    def test_selecting_non_lmstudio_stops_lmstudio_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            with mock.patch.object(events, "stop_adapter", return_value={"stopped": []}) as stop:
                result = events.ensure_adapter(root, "ollama")
            stop.assert_called_once_with(root, "lmstudio")
            self.assertFalse(result["supported"])
            self.assertFalse(result["running"])

    def test_adapter_status_is_read_only_and_rejects_unowned_reused_pid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = events.pid_path(root, "lmstudio")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("777", encoding="utf-8")
            before = path.read_bytes()

            with mock.patch.object(events, "_pid_alive", return_value=True), \
                 mock.patch.object(events, "_ownership_state", return_value={"held": False, "path": "owner"}):
                status = events.adapter_status(root, "lmstudio")

            self.assertFalse(status["running"])
            self.assertEqual(status["observedPid"], 777)
            self.assertTrue(status["pidAlive"])
            self.assertFalse(status["ownershipHeld"])
            self.assertEqual(path.read_bytes(), before)

    def test_stop_adapter_never_kills_stale_pid_without_ownership(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = events.pid_path(root, "lmstudio")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("888", encoding="utf-8")

            with mock.patch.object(events, "_pid_alive", return_value=True), \
                 mock.patch.object(events, "_ownership_state", return_value={"held": False, "path": "owner"}), \
                 mock.patch.object(events, "_terminate_process_tree") as terminate:
                result = events.stop_adapter(root, "lmstudio")

            terminate.assert_not_called()
            self.assertFalse(path.exists())
            self.assertTrue(result["stopped"][0]["stalePidSuppressed"])

    def test_stop_adapter_refuses_unknown_pid_when_ownership_is_live(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            path = events.pid_path(root, "lmstudio")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("999", encoding="utf-8")

            with mock.patch.object(events, "_pid_alive", return_value=False), \
                 mock.patch.object(events, "_ownership_state", return_value={"held": True, "path": "owner"}), \
                 mock.patch.object(events, "_terminate_process_tree") as terminate:
                result = events.stop_adapter(root, "lmstudio")

            terminate.assert_not_called()
            self.assertTrue(path.exists())
            self.assertFalse(result["stopped"][0]["stopped"])
            self.assertIn("refusing process termination", result["stopped"][0]["error"])

    def test_ensure_lmstudio_adapter_returns_only_after_owned_pid_is_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / ".cogent"
            fake = SimpleNamespace(pid=424242, poll=mock.Mock(return_value=None))
            not_running = {
                "provider": "lmstudio",
                "running": False,
                "pid": None,
                "observedPid": None,
                "ownershipHeld": False,
            }
            ready = {
                "provider": "lmstudio",
                "running": True,
                "pid": 424242,
                "observedPid": 424242,
                "pidAlive": True,
                "ownershipHeld": True,
            }
            with mock.patch.object(events, "adapter_status", side_effect=[not_running, not_running, ready]), \
                 mock.patch.object(events, "_cleanup_unowned_files"), \
                 mock.patch.object(events.provider, "find_lms_cli", return_value="lms"), \
                 mock.patch.object(events.subprocess, "Popen", return_value=fake), \
                 mock.patch.object(events.time, "sleep"):
                result = events.ensure_adapter(root, "lmstudio")

            self.assertTrue(result["running"])
            self.assertTrue(result["started"])
            self.assertEqual(result["pid"], 424242)
            fake.poll.assert_called_once()


if __name__ == "__main__":
    unittest.main()
