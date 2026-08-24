from __future__ import annotations

import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host.py"
spec = importlib.util.spec_from_file_location("cnx_host_passthrough", HOST)
cnx_host = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx_host)


class PassthroughLifecycleTests(unittest.TestCase):
    def _root(self, temporary: str) -> Path:
        root = Path(temporary) / "workspace" / ".cogentnexus-openclaw"
        cnx_host.save_state(
            root,
            {
                "schemaVersion": 1,
                "mode": "passthrough",
                "desiredGateway": "running",
                "desiredProvider": "unchanged",
                "generation": 2,
            },
        )
        return root

    def test_managed_lifecycle_commands_require_explicit_enable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root(temporary)
            for command in ("start", "stop", "restart"):
                args = argparse.Namespace(root=root, command=command)
                with self.assertRaisesRegex(RuntimeError, "PASSTHROUGH"):
                    cnx_host.command(args)
                self.assertEqual(cnx_host.load_state(root)["mode"], "passthrough")


if __name__ == "__main__":
    unittest.main()
