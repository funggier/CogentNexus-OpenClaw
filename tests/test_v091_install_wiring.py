from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V091InstallWiringTests(unittest.TestCase):
    def test_installers_use_v091_host_and_control_wrappers(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        self.assertIn('"scripts\\host_v091.py"', ps)
        self.assertIn('"scripts\\host_control_v091.py"', ps)
        self.assertIn('HOST_SCRIPT="$TARGET_SKILL/scripts/host_v091.py"', sh)
        self.assertIn('HOST_CONTROL_SCRIPT="$TARGET_SKILL/scripts/host_control_v091.py"', sh)

    def test_safe_staging_requires_passthrough_and_leaves_plugin_disabled(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        for text in (ps, sh):
            self.assertIn("PASSTHROUGH", text)
            self.assertIn("plugins disable cogentnexus-rotation", text)
            self.assertIn("plugin installation", text.lower())

    def test_portable_cnx_template_uses_transactional_control_wrapper(self):
        launcher = (ROOT / "skills/cogentnexus/templates/lifecycle/cnx.cmd").read_text(encoding="utf-8")
        self.assertIn("host_control_v091.py", launcher)
        self.assertNotIn('scripts\\host.py"', launcher)

    def test_v091_startup_adapter_targets_v091_control_wrapper(self):
        startup = (ROOT / "skills/cogentnexus/scripts/startup_v091.py").read_text(encoding="utf-8")
        host = (ROOT / "skills/cogentnexus/scripts/host_v091.py").read_text(encoding="utf-8")
        self.assertIn('HERE.with_name("host_control_v091.py")', startup)
        self.assertIn('HERE.with_name("startup_v091.py")', host)


if __name__ == "__main__":
    unittest.main()
