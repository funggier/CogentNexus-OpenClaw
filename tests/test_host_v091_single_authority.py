from pathlib import Path
import py_compile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_authority_v091.py"
STALL = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_stall_v091.py"
CONTROL = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_control_v091.py"
ENTRY = ROOT / "plugins" / "cogentnexus-openclaw" / "src" / "v091-release-entry.ts"


class HostSingleAuthorityTests(unittest.TestCase):
    def test_overlay_and_control_compile(self):
        py_compile.compile(str(HOST), doraise=True)
        py_compile.compile(str(STALL), doraise=True)
        py_compile.compile(str(CONTROL), doraise=True)

    def test_control_routes_through_stall_overlay_that_imports_authority_overlay(self):
        control = CONTROL.read_text(encoding="utf-8")
        stall = STALL.read_text(encoding="utf-8")
        self.assertIn('HERE.with_name("host_stall_v091.py")', control)
        self.assertIn("import host_authority_v091 as authority", stall)
        self.assertIn("legacy = authority.legacy", stall)

    def test_enable_linearization_order_is_fail_closed(self):
        source = HOST.read_text(encoding="utf-8")
        startup = source.index('legacy.startup(root, "enable", check=True)')
        plugin_config_enable = source.index('legacy.plugin_enabled(True)', startup)
        managed_commit = source.index('state = legacy.transition(', plugin_config_enable)
        gateway_reload = source.index('"lifecycle",\n            "restart",', managed_commit)
        verified_start = source.index('"lifecycle", "start", "--provider"', gateway_reload)
        self.assertLess(startup, plugin_config_enable)
        self.assertLess(plugin_config_enable, managed_commit)
        self.assertLess(managed_commit, gateway_reload)
        self.assertLess(gateway_reload, verified_start)

    def test_plugin_authority_has_no_policy_marker_bypass(self):
        source = ENTRY.read_text(encoding="utf-8")
        self.assertNotIn("host-activation-staged", source)
        self.assertNotIn("POLICY_BEGIN", source)
        self.assertNotIn("POLICY_END", source)
        self.assertIn('if (mode === "managed") return { authorized: true', source)
        self.assertIn('return { authorized: false, reason: "passthrough"', source)

    def test_power_loss_semantics_are_explicit(self):
        source = HOST.read_text(encoding="utf-8")
        self.assertIn("before the MANAGED commit: plugin discovery/reload is inert", source)
        self.assertIn("after the MANAGED commit: startup adapter + enabled plugin config already", source)
        self.assertIn("authorityHadCommitted", source)
        stall = STALL.read_text(encoding="utf-8")
        self.assertIn("a claimed `recovering` lease is durable", stall)
        self.assertIn("recoveryPolicy=healthy-runtime", stall)


if __name__ == "__main__":
    unittest.main()