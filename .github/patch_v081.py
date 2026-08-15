from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

host_path = ROOT / "skills/cogentnexus/scripts/host.py"
host = host_path.read_text(encoding="utf-8")
needle = '''def python_exe() -> str:\n    return sys.executable or "python"\n'''
helper = '''def python_exe() -> str:\n    return sys.executable or "python"\n\n\ndef openclaw_executable() -> str:\n    # npm installs OpenClaw through platform shims on Windows. PowerShell can\n    # resolve openclaw.ps1/openclaw.cmd automatically, but CreateProcess used by\n    # subprocess.run(shell=False) cannot reliably execute a bare shim name.\n    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)\n    for name in candidates:\n        found = shutil.which(name)\n        if found:\n            return found\n    raise FileNotFoundError("OpenClaw CLI not found on PATH")\n'''
if needle not in host:
    raise SystemExit("host.py python_exe anchor not found")
host = host.replace(needle, helper, 1)
count = host.count('["openclaw",')
if count < 6:
    raise SystemExit(f"expected at least 6 direct OpenClaw subprocess calls, found {count}")
host = host.replace('["openclaw",', '[openclaw_executable(),')
host_path.write_text(host, encoding="utf-8", newline="\n")

installer_path = ROOT / "scripts/install.ps1"
installer = installer_path.read_text(encoding="utf-8")
old = '''            $currentPaths = openclaw config get plugins.load.paths 2>$null\n            if ($LASTEXITCODE -eq 0) {\n                $filteredPaths = $currentPaths | python (Join-Path $repoRoot "scripts\\filter_plugin_paths.py") --plugin-id cogentnexus-rotation\n                if ($LASTEXITCODE -ne 0) { throw "failed to inspect existing plugin load paths" }\n                openclaw config set plugins.load.paths $filteredPaths --strict-json --replace\n                if ($LASTEXITCODE -ne 0) { throw "failed to remove an existing linked plugin path" }\n            }\n'''
new = '''            # plugins.load.paths is optional on a fresh OpenClaw install. Native\n            # stderr from `openclaw config get` must not terminate this script when\n            # the key is absent; only clean an existing linked path when the query\n            # itself succeeds.\n            $currentPaths = $null\n            $pathExit = 1\n            $savedErrorActionPreference = $ErrorActionPreference\n            try {\n                $ErrorActionPreference = "Continue"\n                $currentPaths = openclaw config get plugins.load.paths 2>$null\n                $pathExit = $LASTEXITCODE\n            }\n            finally {\n                $ErrorActionPreference = $savedErrorActionPreference\n            }\n            if ($pathExit -eq 0) {\n                $filteredPaths = $currentPaths | python (Join-Path $repoRoot "scripts\\filter_plugin_paths.py") --plugin-id cogentnexus-rotation\n                if ($LASTEXITCODE -ne 0) { throw "failed to inspect existing plugin load paths" }\n                openclaw config set plugins.load.paths $filteredPaths --strict-json --replace\n                if ($LASTEXITCODE -ne 0) { throw "failed to remove an existing linked plugin path" }\n            }\n'''
if old not in installer:
    raise SystemExit("install.ps1 optional plugin-path block not found")
installer_path.write_text(installer.replace(old, new, 1), encoding="utf-8", newline="\n")

(ROOT / "VERSION").write_text("0.8.1\n", encoding="utf-8")
for rel in [
    "plugins/cogentnexus-rotation/package.json",
    "plugins/cogentnexus-rotation/openclaw.plugin.json",
]:
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = "0.8.1"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

release = ROOT / "docs/releases/v0.8.1.md"
release.write_text('''# CogentNexus v0.8.1\n\nv0.8.1 is a Windows installation/runtime portability patch for the v0.8 Host-managed baseline.\n\n## Fixed\n\n- Host Controller now resolves the installed OpenClaw CLI through the Windows npm shim (`openclaw.cmd`) before invoking plugin/config/Gateway commands from Python subprocesses.\n- The PowerShell installer no longer aborts when the optional `plugins.load.paths` config key does not exist on a fresh managed-plugin installation.\n- Adds regression coverage for Windows shim resolution and the optional plugin-path probe contract.\n\nNo architecture or Ticket/continuity semantics change from v0.8.0. Existing v0.8.0 state, Tickets, managed policy snapshots, and installed plugin data remain compatible.\n''', encoding="utf-8")

test = ROOT / "tests/test_windows_cli_shim.py"
test.write_text('''import importlib.util\nimport unittest\nfrom pathlib import Path\nfrom unittest import mock\n\nROOT = Path(__file__).resolve().parents[1]\nHOST_PATH = ROOT / "skills" / "cogentnexus" / "scripts" / "host.py"\n\nspec = importlib.util.spec_from_file_location("cnx_host_windows_test", HOST_PATH)\nhost = importlib.util.module_from_spec(spec)\nassert spec.loader is not None\nspec.loader.exec_module(host)\n\n\nclass WindowsCliShimTests(unittest.TestCase):\n    def test_windows_prefers_openclaw_cmd_shim(self):\n        def fake_which(name):\n            return r"C:\\\\Users\\\\test\\\\AppData\\\\Roaming\\\\npm\\\\openclaw.cmd" if name == "openclaw.cmd" else None\n\n        with mock.patch.object(host.os, "name", "nt"), mock.patch.object(host.shutil, "which", side_effect=fake_which):\n            self.assertTrue(host.openclaw_executable().lower().endswith("openclaw.cmd"))\n\n    def test_host_has_no_bare_openclaw_subprocess_literal(self):\n        source = HOST_PATH.read_text(encoding="utf-8")\n        self.assertNotIn('["openclaw",', source)\n\n    def test_installer_treats_missing_plugin_load_paths_as_optional(self):\n        source = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")\n        self.assertIn('$savedErrorActionPreference = $ErrorActionPreference', source)\n        self.assertIn('$pathExit = $LASTEXITCODE', source)\n        self.assertIn('if ($pathExit -eq 0)', source)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")
