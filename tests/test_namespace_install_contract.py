from pathlib import Path


ROOT = Path(__file__).parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_canonical_file_layout_has_no_permanent_generic_aliases():
    assert (ROOT / "skills/cogentnexus-openclaw/scripts/cnxclaw.py").is_file()
    assert (ROOT / "skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py").is_file()
    assert (ROOT / "plugins/cogentnexus-openclaw/openclaw.plugin.json").is_file()
    assert (ROOT / "templates/AGENTS.cogentnexus-openclaw.md").is_file()
    assert not (ROOT / "skills/cogentnexus").exists()
    assert not (ROOT / "plugins/cogentnexus-rotation").exists()
    assert not (ROOT / "templates/AGENTS.cogentnexus.md").exists()


def test_windows_installer_orders_proof_handoff_manifest_and_enable():
    source = read("scripts/install.ps1")
    proof = source.index("classify-install --workspace")
    handoff = source.index("Enter-NativeInstallBoundary\n")
    mutation = source.index("Copy-Item -Recurse -Force -LiteralPath $sourceSkill")
    manifest = source.index('"scripts\\namespace_ownership.py"), "create"')
    enable = source.index("enable --provider ollama")
    assert proof < handoff < mutation < manifest < enable
    assert source.count("& $handoffLauncher disable") == 1
    assert "migration-report.json" in source
    assert "Legacy plugin uninstall failed" in source
    assert "plugins.entries.cogentnexus-rotation" in source
    assert source.index("classify-install --workspace") < source.index("Copy-Item -Recurse -Force -LiteralPath $sourceSkill")


def test_posix_installer_uses_only_new_fresh_layout_and_has_interruption_report():
    source = read("scripts/install.sh")
    assert 'LAUNCHER="$WORKSPACE/cnxclaw"' in source
    assert 'TARGET_SKILL="$WORKSPACE/skills/cogentnexus-openclaw"' in source
    assert 'COGENT_ROOT="$WORKSPACE/.cogentnexus-openclaw"' in source
    assert "migration-report.json" in source
    assert source.index("classify-install") < source.index('cp -R "$SOURCE_SKILL"')
    assert "plugins.entries.cogentnexus-rotation" in source
    assert "openclaw plugins uninstall cogentnexus-rotation --force" in source


def test_release_package_names_are_variant_scoped():
    validate = read(".github/workflows/validate.yml")
    release = read(".github/workflows/release.yml")
    assert 'name="cogentnexus-openclaw-v0.9.3"' in validate
    assert 'name="cogentnexus-openclaw-$tag"' in release
    assert '--title "CogentNexus-OpenClaw $tag"' in release


def test_destructive_current_paths_are_manifest_gated():
    lifecycle = read("skills/cogentnexus-openclaw/scripts/lifecycle_v092.py")
    reinstall = read("scripts/clean-reinstall.ps1")
    assert lifecycle.count("namespace_ownership.verify_manifest") >= 2
    assert "Ownership manifest mismatch; refusing clean-reinstall mutation." in reinstall
    classify = reinstall.index("classify-install --workspace")
    first_backup = reinstall.index("New-Item -ItemType Directory -Force -Path $backup")
    first_delete = reinstall.index("Remove-OwnedPath $extension")
    assert classify < first_backup < first_delete
    assert "Registered plugin/task exists without a coherent ownership manifest" in reinstall
