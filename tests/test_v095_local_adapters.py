import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import local_adapters_v095 as adapters


class V095LocalAdaptersTests(unittest.TestCase):
    def test_status_uses_only_local_provider_probe(self):
        with mock.patch.object(adapters.provider, "probe", return_value={"healthy": True}) as probe:
            result = adapters.local_ollama_status()
        self.assertEqual(result["adapter"], "ollama")
        self.assertTrue(result["status"]["healthy"])
        probe.assert_called_once_with("ollama")

    def test_start_delegates_to_ollama_start(self):
        with mock.patch.object(adapters.provider, "start", return_value={"ok": True}) as start:
            code, result = adapters.local_ollama_start()
        self.assertEqual(code, 0)
        self.assertEqual(result["adapter"], "ollama")
        start.assert_called_once_with("ollama")

    def test_stop_delegates_to_ollama_stop(self):
        with mock.patch.object(adapters.provider, "stop", return_value={"ok": True}) as stop:
            code, result = adapters.local_ollama_stop()
        self.assertEqual(code, 0)
        self.assertEqual(result["action"], "stop")
        stop.assert_called_once_with("ollama")

    def test_restart_is_stop_then_start(self):
        with mock.patch.object(adapters.provider, "stop", return_value={"ok": True}) as stop, \
             mock.patch.object(adapters.provider, "start", return_value={"ok": True}) as start:
            code, result = adapters.local_ollama_restart()
        self.assertEqual(code, 0)
        self.assertEqual(result["action"], "restart")
        stop.assert_called_once_with("ollama")
        start.assert_called_once_with("ollama")

    def test_restart_does_not_start_after_failed_stop(self):
        with mock.patch.object(adapters.provider, "stop", return_value={"ok": False}), \
             mock.patch.object(adapters.provider, "start") as start:
            code, result = adapters.local_ollama_restart()
        self.assertNotEqual(code, 0)
        self.assertEqual(result["phase"], "stop")
        start.assert_not_called()

    def test_adapter_source_contains_no_openclaw_route_import_or_call(self):
        source = Path(adapters.__file__).read_text(encoding="utf-8")
        self.assertNotIn("openclaw_route", source)
        self.assertNotIn("route.begin", source)
        self.assertNotIn("route.commit", source)


if __name__ == "__main__":
    unittest.main()
