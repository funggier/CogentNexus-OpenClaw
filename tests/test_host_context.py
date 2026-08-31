from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_context.py"
spec = importlib.util.spec_from_file_location("cnx_host_context", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostContextTests(unittest.TestCase):
    def setUp(self):
        self.original_executable = cnx.openclaw_executable
        self.original_run = subprocess.run

    def tearDown(self):
        cnx.openclaw_executable = self.original_executable
        subprocess.run = self.original_run

    def test_validate_session_key_rejects_empty_nul_and_oversized_values(self):
        with self.assertRaises(ValueError):
            cnx.validate_session_key("")
        with self.assertRaises(ValueError):
            cnx.validate_session_key("agent:main:dashboard:A\x00B")
        with self.assertRaises(ValueError):
            cnx.validate_session_key("a" * 2049)
        self.assertEqual(cnx.validate_session_key(" agent:main:dashboard:A "), "agent:main:dashboard:A")

    def test_compact_uses_only_sessions_compact_with_fixed_argv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            captured: list[str] = []
            cnx.openclaw_executable = lambda: "openclaw"

            def fake_run(command, **kwargs):
                captured.extend(command)
                return subprocess.CompletedProcess(
                    command,
                    0,
                    json.dumps({"ok": True, "tokensAfter": 7000}),
                    "",
                )

            subprocess.run = fake_run
            result = cnx.compact(root, "agent:main:dashboard:A", 120, 90_000)
            self.assertEqual(result, {"ok": True, "tokensAfter": 7000})
            self.assertEqual(captured[:4], ["openclaw", "gateway", "call", "sessions.compact"])
            self.assertIn("--params", captured)
            params = json.loads(captured[captured.index("--params") + 1])
            self.assertEqual(params, {"key": "agent:main:dashboard:A", "maxLines": 120})
            self.assertNotIn("chat.abort", captured)
            audit = root / "runtime" / "context-host-events.jsonl"
            self.assertTrue(audit.is_file())
            record = json.loads(audit.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual(record["action"], "sessions.compact")
            self.assertTrue(record["ok"])

    def test_compact_rejects_out_of_bounds_max_lines_before_process_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            launched = False
            cnx.openclaw_executable = lambda: "openclaw"

            def fake_run(*args, **kwargs):
                nonlocal launched
                launched = True
                raise AssertionError("process must not launch")

            subprocess.run = fake_run
            with self.assertRaises(ValueError):
                cnx.compact(root, "agent:main:dashboard:A", 0, 90_000)
            with self.assertRaises(ValueError):
                cnx.compact(root, "agent:main:dashboard:A", 20_001, 90_000)
            self.assertFalse(launched)

    def test_parser_exposes_only_compact_operation(self):
        parser = cnx.build_parser()
        parsed = parser.parse_args(["compact", "--session-key", "agent:main:dashboard:A"])
        self.assertEqual(parsed.command, "compact")
        with self.assertRaises(SystemExit):
            parser.parse_args(["chat.abort", "--session-key", "agent:main:dashboard:A"])


if __name__ == "__main__":
    unittest.main()
