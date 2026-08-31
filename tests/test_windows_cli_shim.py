import importlib.util
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HOST_PATH = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host.py"

spec = importlib.util.spec_from_file_location("cnx_host_windows_test", HOST_PATH)
host = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(host)


class WindowsCliShimTests(unittest.TestCase):
    def test_windows_prefers_openclaw_cmd_shim(self):
        def fake_which(name):
            return r"C:\\Users\\test\\AppData\\Roaming\\npm\\openclaw.cmd" if name == "openclaw.cmd" else None

        with mock.patch.object(host.os, "name", "nt"), mock.patch.object(host.shutil, "which", side_effect=fake_which):
            self.assertTrue(host.openclaw_executable().lower().endswith("openclaw.cmd"))

    def test_host_has_no_bare_openclaw_subprocess_literal(self):
        source = HOST_PATH.read_text(encoding="utf-8")
        self.assertNotIn('["openclaw",', source)

    def test_installer_treats_missing_plugin_load_paths_as_optional(self):
        source = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")
        self.assertIn('$savedErrorActionPreference = $ErrorActionPreference', source)
        self.assertIn('$pathExit = $LASTEXITCODE', source)
        self.assertIn('if ($pathExit -eq 0)', source)


if __name__ == "__main__":
    unittest.main()
