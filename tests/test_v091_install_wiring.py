from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V091InstallWiringTests(unittest.TestCase):
    def test_installers_keep_v091_host_core_and_enter_through_v092_cli(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        # Initialization/policy still use the accepted v0.9.1 Host core.
        self.assertIn("host_v091.py", ps)
        self.assertIn("host_v091.py", sh)

        # Managed lifecycle/provider selection enters through the v0.9.2 CLI,
        # which layers provider-neutral orchestration over the accepted core.
        self.assertIn("scripts\\cnx.py", ps)
        self.assertIn("scripts/cnx.py", sh)

        cnx = (ROOT / "skills/cogentnexus/scripts/cnx.py").read_text(encoding="utf-8")
        control_v092 = (ROOT / "skills/cogentnexus/scripts/host_control_v092.py").read_text(encoding="utf-8")
        self.assertIn('HERE.with_name("host_control_v092.py")', cnx)
        self.assertIn("import host_control_v091 as v091", control_v092)

    def test_safe_staging_requires_passthrough_and_leaves_plugin_disabled(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        for text in (ps, sh):
            self.assertIn("PASSTHROUGH", text.upper())
            self.assertIn("plugins disable cogentnexus-rotation", text.lower())
            self.assertIn("plugins install", text.lower())
            self.assertIn("skip", text.lower())

    def test_portable_cnx_template_uses_v092_cli_facade(self):
        launcher = (ROOT / "skills/cogentnexus/templates/lifecycle/cnx.cmd").read_text(encoding="utf-8")
        self.assertIn("scripts\\cnx.py", launcher)
        self.assertNotIn('scripts\\host.py"', launcher)
        self.assertNotIn('scripts\\host_v091.py"', launcher)

        cnx = (ROOT / "skills/cogentnexus/scripts/cnx.py").read_text(encoding="utf-8")
        self.assertIn('HOST_CONTROL = HERE.with_name("host_control_v092.py")', cnx)

    def test_v091_startup_adapter_targets_v091_control_wrapper(self):
        startup = (ROOT / "skills/cogentnexus/scripts/startup_v091.py").read_text(encoding="utf-8")
        host = (ROOT / "skills/cogentnexus/scripts/host_v091.py").read_text(encoding="utf-8")
        self.assertIn('HERE.with_name("host_control_v091.py")', startup)
        self.assertIn('HERE.with_name("startup_v091.py")', host)


if __name__ == "__main__":
    unittest.main()
