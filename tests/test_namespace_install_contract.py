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
    verify = source.index('"scripts\\namespace_ownership.py") verify --root')
    enable = source.index("enable --provider ollama")
    skip_preflight = source.index("preflight-skip-plugin")
    assert proof < skip_preflight < handoff < mutation < manifest < verify < enable
    assert source.count("& $handoffLauncher disable") == 1
    assert "migration-report.json" in source
    assert "Legacy plugin uninstall failed" in source
    assert "plugins.entries.cogentnexus-rotation" in source
    assert source.index("classify-install --workspace") < source.index("Copy-Item -Recurse -Force -LiteralPath $sourceSkill")


def test_windows_installer_applies_verified_rollover_before_single_candidate_resolution():
    source = read("scripts/install.ps1")
    install = source.index('openclaw plugins install ("npm-pack:" + $packagePath) --force')
    inventory = source.index("openclaw plugins list --json", install)
    plan = source.index('"rollover-plan"', inventory)
    apply = source.index('"rollover-apply"', plan)
    resolve = source.index(" resolve-plugin --openclaw-state", apply)
    assert install < inventory < plan < apply < resolve
    plugin_guard = source.index("if (-not $SkipPlugin) {")
    upgrade_guard = source.index('if ($classification.mode -eq "upgrade") {', install)
    assert plugin_guard < install < upgrade_guard < plan
    assert "-LinkPlugin is incompatible with ownership-safe managed installation" in source
    assert source.count("openclaw plugins list --json", install, apply) == 2
    assert "$rolloverApplyInventoryPath" in source


def test_posix_installer_uses_only_new_fresh_layout_and_has_interruption_report():
    source = read("scripts/install.sh")
    assert 'LAUNCHER="$WORKSPACE/cnxclaw"' in source
    assert 'TARGET_SKILL="$WORKSPACE/skills/cogentnexus-openclaw"' in source
    assert 'COGENT_ROOT="$WORKSPACE/.cogentnexus-openclaw"' in source
    assert "migration-report.json" in source
    assert source.index("classify-install") < source.index('cp -R "$SOURCE_SKILL"')
    assert source.index("preflight-skip-plugin") < source.index('cp -R "$SOURCE_SKILL"')
    assert source.index(' create --root "$COGENT_ROOT"') < source.index(' verify --root "$COGENT_ROOT"') < source.index('enable --provider ollama')
    assert "plugins.entries.cogentnexus-rotation" in source
    assert "openclaw plugins uninstall cogentnexus-rotation --force" in source


def test_posix_installer_matches_windows_rollover_order_and_rejects_link_mix():
    source = read("scripts/install.sh")
    install = source.index('openclaw plugins install "npm-pack:$PLUGIN_DIR/$PACKAGE_FILE" --force')
    inventory = source.index("openclaw plugins list --json", install)
    plan = source.index("rollover-plan", inventory)
    apply = source.index("rollover-apply", plan)
    resolve = source.index(" resolve-plugin --openclaw-state", apply)
    assert install < inventory < plan < apply < resolve
    plugin_guard = source.index('if [ "$SKIP_PLUGIN" -eq 0 ]; then')
    upgrade_guard = source.index('if [ "$INSTALL_MODE" = upgrade ]; then', install)
    assert plugin_guard < install < upgrade_guard < plan
    assert "--link-plugin is incompatible with ownership-safe managed installation" in source
    assert source.count("openclaw plugins list --json", install, apply) == 2
    linked_filter = source.index("filter_plugin_paths.py", plugin_guard)
    assert linked_filter < install
    assert "plugins.load.paths" in source[linked_filter - 300:linked_filter + 300]


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
    assert 'CogentNexus-OpenClaw-Clean-Reinstall-Backups' in reinstall
    assert "validate-boundary" in reinstall
    assert "write-recovery" in reinstall
    assert 'Copy-Backup $applicationDataRoot "application-data\\CogentNexus-OpenClaw"' in reinstall
    assert "Remove-OwnedPath $applicationDataRoot" in reinstall
    assert "clean-reinstall-backups" not in reinstall
    assert "[switch]$NoBackup" in reinstall
    assert "-NoBackup selected" in reinstall
