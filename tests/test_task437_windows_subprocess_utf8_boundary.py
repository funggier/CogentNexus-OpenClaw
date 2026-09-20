from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


host = load("cnx437_host", SCRIPTS / "host.py")
host_control = load("cnx437_host_control", SCRIPTS / "host_control.py")
cnxclaw = load("cnx437_cnxclaw", SCRIPTS / "cnxclaw.py")


class WindowsSubprocessUtf8BoundaryTests(unittest.TestCase):
    def _assert_utf8_replace(self, kwargs):
        self.assertEqual(kwargs.get("encoding"), "utf-8")
        self.assertEqual(kwargs.get("errors"), "replace")
        self.assertTrue(kwargs.get("text"))

    def test_legacy_openclaw_runner_decodes_utf8_loss_tolerantly(self):
        seen = {}

        def fake_run(cmd, **kwargs):
            seen.update(kwargs)
            return subprocess.CompletedProcess(cmd, 0, stdout="{}", stderr="")

        with mock.patch.object(host.subprocess, "run", side_effect=fake_run):
            result = host.run(["openclaw", "agents", "list", "--json"])

        self.assertEqual(result.returncode, 0)
        self._assert_utf8_replace(seen)

    def test_host_control_runner_decodes_utf8_loss_tolerantly(self):
        seen = {}

        def fake_run(cmd, **kwargs):
            seen.update(kwargs)
            return subprocess.CompletedProcess(cmd, 0, stdout="{}", stderr="")

        with mock.patch.object(host_control.subprocess, "run", side_effect=fake_run):
            result = host_control.run(["openclaw", "gateway", "health"])

        self.assertEqual(result.returncode, 0)
        self._assert_utf8_replace(seen)

    def test_cnxclaw_host_runner_decodes_utf8_loss_tolerantly(self):
        seen = {}

        def fake_run(cmd, **kwargs):
            seen.update(kwargs)
            return subprocess.CompletedProcess(cmd, 0, stdout='{"ok":true}\n', stderr="")

        with mock.patch.object(cnxclaw.subprocess, "run", side_effect=fake_run):
            result = cnxclaw.run_host(Path("."), ["status"])

        self.assertTrue(result["ok"])
        self._assert_utf8_replace(seen)

    def test_legacy_runner_decodes_real_utf8_bytes_that_break_cp1252(self):
        result = host.run([
            sys.executable,
            "-c",
            "import sys; sys.stdout.buffer.write('ก'.encode('utf-8'))",
        ])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "ก")

    def test_default_agent_id_fails_controlled_when_captured_stdout_is_missing(self):
        completed = subprocess.CompletedProcess(["openclaw"], 0, stdout=None, stderr=None)
        with mock.patch.object(host, "run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "agents list returned invalid JSON"):
                host.default_agent_id()


if __name__ == "__main__":
    unittest.main()
