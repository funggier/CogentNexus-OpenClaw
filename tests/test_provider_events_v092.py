import sys
import tempfile
import unittest
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
