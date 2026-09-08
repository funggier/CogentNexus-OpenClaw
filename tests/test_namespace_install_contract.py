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
    enable = source.index("enable\n")
    skip_preflight = source.index("preflight-skip-plugin")
    assert proof < skip_preflight < handoff < mutation < manifest < verify < enable
    assert source.count("& $handoffLauncher disable") == 1
    assert "migration-report.json" in source
    assert "Legacy plugin uninstall failed" in source
    assert "plugins.entries.cogentnexus-rotation" in source
    assert source.index("classify-install --workspace") < source.index("Copy-Item -Recurse -Force -LiteralPath $sourceSkill")


def test_windows_installer_applies_verified_rollover_before_single_candidate_resolution():
    source = read("scripts/install.ps1")
    install = source.index('openclaw plugins install $packagePath --force')
    prepare = source.index('"rollover-prepare"')
    finalize = source.index('"rollover-finalize"')
    resolve = source.index(" resolve-plugin --openclaw-state", finalize)
    assert prepare < install < finalize < resolve
    plugin_guard = source.index("if (-not $SkipPlugin) {")
    upgrade_guard = source.index('if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin) {')
    assert plugin_guard < upgrade_guard < prepare < install < finalize
    assert "-LinkPlugin is incompatible with ownership-safe managed installation" in source
    assert source.count("openclaw plugins list --json", install, finalize) == 1
    assert "$rolloverTransactionPath" in source


def test_windows_skip_plugin_short_circuits_post_copy_plugin_resolution():
    source = read("scripts/install.ps1")
    launcher = source.index('Write-Host "Installed CogentNexus-OpenClaw launcher')
    resolve = source.index(" resolve-plugin --openclaw-state", launcher)
    verify = source.index('namespace_ownership.py") verify --root', resolve)
    guard = source.find("if ($SkipPlugin) {", launcher, resolve)
    assert guard > launcher, "SkipPlugin must guard post-copy plugin resolution"
    assert guard < resolve
    close = source.find("\n}\n", resolve)
    assert close > resolve
    assert "installedPluginFingerprint.ToLowerInvariant()" in source[resolve:close]
    assert "staging" in source[guard:close + 3].lower()
    assert verify < close, "normal plugin verification remains inside the else path"


def test_posix_skip_plugin_short_circuits_post_copy_plugin_resolution():
    source = read("scripts/install.sh")
    launcher = source.index('echo "Installed CogentNexus-OpenClaw launcher')
    resolve = source.index(" resolve-plugin --openclaw-state", launcher)
    guard = source.find('if [ "$SKIP_PLUGIN" -eq 1 ]; then', launcher, resolve)
    assert guard > launcher, "skip-plugin must guard post-copy plugin resolution"
    assert guard < resolve
    assert "staging" in source[launcher:source.index("fi", resolve) + 2].lower()


def test_posix_installer_uses_only_new_fresh_layout_and_has_interruption_report():
    source = read("scripts/install.sh")
    assert 'LAUNCHER="$WORKSPACE/cnxclaw"' in source
    assert 'TARGET_SKILL="$WORKSPACE/skills/cogentnexus-openclaw"' in source
    assert 'COGENT_ROOT="$WORKSPACE/.cogentnexus-openclaw"' in source
    assert "migration-report.json" in source
    assert source.index("classify-install") < source.index('cp -R "$SOURCE_SKILL"')
    assert source.index("preflight-skip-plugin") < source.index('cp -R "$SOURCE_SKILL"')
    assert source.index(' create --root "$COGENT_ROOT"') < source.index(' verify --root "$COGENT_ROOT"') < source.index(' enable\n')
    assert "plugins.entries.cogentnexus-rotation" in source
    assert "openclaw plugins uninstall cogentnexus-rotation --force" in source


def test_windows_installer_exposes_explicit_attested_rollover_recovery_before_preflight():
    source = read("scripts/install.ps1")
    parameter = source.index("[string]$RecoverRolloverTransaction")
    digest_parameter = source.index("[string]$RecoverRolloverTransactionSha256", parameter)
    source_parameter = source.index("[string]$RecoverRolloverSourcePluginRoot", digest_parameter)
    recovery = source.index('"rollover-recover"', source_parameter)
    inventory = source.rindex("openclaw plugins list --json", digest_parameter, recovery)
    preflight = source.index("recovery-preflight --workspace", recovery)
    classification = source.index("classify-install --workspace", preflight)
    assert parameter < digest_parameter < source_parameter < inventory < recovery < preflight < classification
    assert "-RecoverRolloverTransaction requires" in source
    recovery_window = source[recovery - 1200:recovery + 1400]
    assert '"--workspace", $Workspace' in recovery_window
    assert '"--app-data", $applicationDataRoot' in recovery_window
    assert '"--expected-transaction-sha256", $RecoverRolloverTransactionSha256' in recovery_window
    assert '"--expected-replacement-fingerprint", $recoverySourceFingerprint' in recovery_window
    assert "Invoke-NativeInstallerDiagnostic -Executable \"python\" -Arguments $rolloverRecoveryArgs" in recovery_window
    assert "plugin-fingerprint --plugin-root $RecoverRolloverSourcePluginRoot --version $version" in source[parameter:recovery]


def test_posix_installer_matches_windows_rollover_order_and_rejects_link_mix():
    source = read("scripts/install.sh")
    fingerprint = source.index("plugin-fingerprint")
    prepare = source.index("rollover-prepare", fingerprint)
    install = source.index('openclaw plugins install "npm-pack:$PLUGIN_DIR/$PACKAGE_FILE" --force')
    inventory = source.index("openclaw plugins list --json", install)
    finalize = source.index("rollover-finalize", inventory)
    resolve = source.index(" resolve-plugin --openclaw-state", finalize)
    assert fingerprint < prepare < install < inventory < finalize < resolve
    plugin_guard = source.index('if [ "$SKIP_PLUGIN" -eq 0 ] && [ "$PLUGIN_ALREADY_EXACT" -eq 0 ]; then')
    upgrade_guard = source.index('if [ "$INSTALL_MODE" = upgrade ]; then')
    assert fingerprint < upgrade_guard < plugin_guard < prepare
    assert "--expected-replacement-fingerprint" in source[prepare:finalize]
    assert "--link-plugin is incompatible with ownership-safe managed installation" in source
    assert source.count("openclaw plugins list --json", install, finalize) == 1
    linked_filter = source.index("filter_plugin_paths.py", plugin_guard)
    assert linked_filter < install
    assert "plugins.load.paths" in source[linked_filter - 300:linked_filter + 300]


def test_release_package_names_are_variant_scoped():
    validate = read(".github/workflows/validate.yml")
    release = read(".github/workflows/release.yml")
    assert 'name="cogentnexus-openclaw-v0.9.4"' in validate
    assert 'name="cogentnexus-openclaw-$tag"' in release
    assert '--title "CogentNexus-OpenClaw $tag"' in release


def test_recovery_reality_smoke_requires_the_variant_scoped_cli_facade():
    workflow = read(".github/workflows/ps51-v093-recovery-reality-smoke.yml")
    assert workflow.count("cnxclaw_v093\\.py") == 2
    assert "cnx_v093\\.py" not in workflow


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
