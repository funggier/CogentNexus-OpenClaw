from __future__ import annotations

import queue
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"


class InteractiveDelegationTests(unittest.TestCase):
    def test_normal_noninteractive_delegation_still_captures_and_forwards(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_host = tmp_path / "fake_host.py"
            fake_host.write_text(
                "print('NORMAL_OK', flush=True)\n",
                encoding="utf-8",
            )
            runner = tmp_path / "runner.py"
            runner.write_text(
                textwrap.dedent(
                    f"""
                    import sys
                    from pathlib import Path
                    sys.path.insert(0, {str(SCRIPTS)!r})
                    import cnxclaw
                    cnxclaw.HOST_CONTROL = Path({str(fake_host)!r})
                    raise SystemExit(cnxclaw.delegate(Path({str(tmp_path)!r}), ['harmless-normal']))
                    """
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(runner)],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "NORMAL_OK\n")
            self.assertEqual(result.stderr, "")

    def test_nested_interactive_prompt_is_visible_before_child_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_host = tmp_path / "fake_host.py"
            fake_host.write_text(
                "import sys\n"
                "sys.stdout.write('Continue? [y/N]: ')\n"
                "sys.stdout.flush()\n"
                "answer = sys.stdin.readline().rstrip('\\r\\n')\n"
                "print('ACK:' + answer, flush=True)\n"
                "sys.exit(0 if answer == 'y' else 1)\n",
                encoding="utf-8",
            )
            runner = tmp_path / "runner.py"
            runner.write_text(
                textwrap.dedent(
                    f"""
                    import sys
                    from pathlib import Path
                    sys.path.insert(0, {str(SCRIPTS)!r})
                    import cnxclaw
                    cnxclaw.HOST_CONTROL = Path({str(fake_host)!r})
                    raise SystemExit(cnxclaw.delegate(Path({str(tmp_path)!r}), ['harmless-interactive']))
                    """
                ),
                encoding="utf-8",
            )
            proc = subprocess.Popen(
                [sys.executable, str(runner)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            assert proc.stdout is not None
            chunks: queue.Queue[str] = queue.Queue()

            def drain_stdout() -> None:
                assert proc.stdout is not None
                for chunk in iter(lambda: proc.stdout.read(1), ""):
                    chunks.put(chunk)

            reader = threading.Thread(target=drain_stdout, daemon=True)
            reader.start()
            deadline = time.monotonic() + 2.0
            observed = ""
            while time.monotonic() < deadline and "Continue? [y/N]: " not in observed:
                try:
                    observed += chunks.get(timeout=0.05)
                except queue.Empty:
                    pass
            prompt_before_input = "Continue? [y/N]: " in observed
            assert proc.stdin is not None
            proc.stdin.write("y\n")
            proc.stdin.flush()
            proc.stdin.close()
            proc.wait(timeout=5)
            reader.join(timeout=1)
            stdout = ""
            while True:
                try:
                    stdout += chunks.get_nowait()
                except queue.Empty:
                    break
            assert proc.stderr is not None
            stderr = proc.stderr.read()
            if proc.stdout is not None:
                proc.stdout.close()
            proc.stderr.close()
            self.assertTrue(
                prompt_before_input,
                "interactive prompt must propagate before delegated child exits",
            )
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(stderr, "")
            self.assertIn("ACK:y", observed + stdout)


if __name__ == "__main__":
    unittest.main()
