from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V091InstallWiringTests(unittest.TestCase):
    def test_installers_keep_v091_host_core_and_enter_through_v093_cli(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        # Initialization/policy still use the accepted v0.9.1 Host core.
        self.assertIn("host_v091.py", ps)
        self.assertIn("host_v091.py", sh)

        # v0.9.3 narrows the operator/provider surface to Ollama while retaining
        # the accepted v0.9.2 orchestration backend underneath the facade.
        self.assertIn("scripts\\cnx_v093.py", ps)
        self.assertIn("scripts/cnx_v093.py", sh)
        self.assertIn('[ValidateSet("ollama")]', ps)
        self.assertIn('PROVIDER="ollama"', sh)

        cnx_v093 = (ROOT / "skills/cogentnexus/scripts/cnx_v093.py").read_text(encoding="utf-8")
        provider_v093 = (ROOT / "skills/cogentnexus/scripts/provider_v093.py").read_text(encoding="utf-8")
        legacy_cnx = (ROOT / "skills/cogentnexus/scripts/cnx.py").read_text(encoding="utf-8")
        control_v092 = (ROOT / "skills/cogentnexus/scripts/host_control_v092.py").read_text(encoding="utf-8")

        self.assertIn("import cnx as legacy", cnx_v093)
        self.assertIn("import provider_v093 as ollama_provider", cnx_v093)
        self.assertIn('SUPPORTED_PROVIDERS = ("ollama",)', provider_v093)
        self.assertIn('HERE.with_name("host_control_v092.py")', legacy_cnx)
        self.assertIn("import host_control_v091 as v091", control_v092)

    def test_safe_staging_requires_passthrough_and_leaves_plugin_disabled(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        for text in (ps, sh):
            self.assertIn("PASSTHROUGH", text.upper())
            self.assertIn("plugins disable cogentnexus-rotation", text.lower())
            self.assertIn("plugins install", text.lower())
            self.assertIn("skip", text.lower())

    def test_upgrade_handoff_precedes_skill_and_plugin_mutation(self):
        ps = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")

        # A reinstall can start while the prior accepted runtime is MANAGED.
        # The old launcher must disable that authority before replacing its
        # skill or changing OpenClaw plugin configuration.
        self.assertIn("& $existingLauncher disable", ps)
        self.assertIn('"$EXISTING_LAUNCHER" disable', sh)
        self.assertIn("Pre-install native handoff: PASS", ps)
        self.assertIn("Pre-install native handoff: PASS", sh)

        ps_handoff = ps.index("Enter-NativeInstallBoundary\n")
        ps_skill_mutation = ps.index("Copy-Item -Recurse -Force -LiteralPath $sourceSkill -Destination $stagedSkill")
        ps_plugin_mutation = ps.index("openclaw plugins install")
        self.assertLess(ps_handoff, ps_skill_mutation)
        self.assertLess(ps_handoff, ps_plugin_mutation)

        sh_handoff = sh.index("existing_mode=$(read_existing_mode)")
        sh_skill_mutation = sh.index('cp -R "$SOURCE_SKILL" "$STAGED_SKILL"')
        sh_plugin_mutation = sh.index("openclaw plugins install")
        self.assertLess(sh_handoff, sh_skill_mutation)
        self.assertLess(sh_handoff, sh_plugin_mutation)

        # Corrupt/unknown prior authority must fail closed rather than guessing.
        self.assertIn("not a recognized safe upgrade source", ps)
        self.assertIn("not a recognized safe upgrade source", sh)

    def test_portable_cnx_template_uses_v092_cli_facade(self):
        # The portable template is a released-v0.9.2 compatibility artifact; the
        # v0.9.3 installers generate their launcher against cnx_v093.py directly.
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
