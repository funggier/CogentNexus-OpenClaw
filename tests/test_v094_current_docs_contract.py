from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_DOCS = (
    ROOT / "README.md",
    ROOT / "docs" / "BASELINE.md",
    ROOT / "docs" / "CURRENT_STATE.md",
    ROOT / "docs" / "PROVIDERS.md",
    ROOT / "docs" / "INSTALL.md",
    ROOT / "docs" / "TRANSIENT_STALL_RECOVERY.md",
    ROOT / "docs" / "operations" / "ROADMAP.md",
    ROOT / "docs" / "operations" / "STATUS.md",
    ROOT / "docs" / "releases" / "v0.9.4.md",
)


def test_v094_current_docs_identify_the_candidate_as_unreleased():
    for path in CURRENT_DOCS:
        text = path.read_text(encoding="utf-8").lower()
        assert "unreleased" in text or "not released" in text, path


def test_current_provider_docs_preserve_managed_and_passthrough_boundaries():
    for path in (ROOT / "README.md", ROOT / "docs" / "CURRENT_STATE.md", ROOT / "docs" / "PROVIDERS.md"):
        text = path.read_text(encoding="utf-8")
        assert "Ollama" in text and "health" in text and "lifecycle" in text and "recovery" in text, path
        assert "OpenClaw-owned" in text and "Cloud" in text, path
        for authority in ("authentication", "routing", "runtime", "probing"):
            assert authority in text, (path, authority)
        assert "credentials" in text, path


def test_current_provider_docs_do_not_collapse_cloud_passthrough_into_ollama_only():
    forbidden = {
        ROOT / "docs" / "PROVIDERS.md": ("Current v0.9.4 source exposes Ollama only.",),
        ROOT / "docs" / "INSTALL.md": ("The v0.9.4 runtime/provider target is Ollama only.",),
        ROOT / "docs" / "INSTALL.th.md": ("runtime/provider target ของ v0.9.4 คือ Ollama เท่านั้น",),
    }
    for path, claims in forbidden.items():
        text = path.read_text(encoding="utf-8")
        for claim in claims:
            assert claim not in text, (path, claim)


def test_thai_command_guide_covers_managed_and_cloud_boundaries():
    guide = (ROOT / "docs" / "COMMANDS.th.md").read_text(encoding="utf-8")
    required = (
        "cnxclaw.cmd cloud",
        "openclaw models set <provider/model>",
        "cnxclaw.cmd enable",
        "cnxclaw.cmd disable",
        "cnxclaw.cmd status",
        "cnxclaw.cmd check system",
        "cnxclaw.cmd ticket list",
        "cnxclaw.cmd ticket cancel <ticket-id>",
        "cnxclaw.cmd session cancel <session-key>",
        "ไม่ใช้แทนการลบ",
        "OpenClaw เป็นเจ้าของ",
        "ห้ามส่ง credential",
        "read-only",
    )
    for text in required:
        assert text in guide
    assert guide.index("cnxclaw.cmd cloud") < guide.index("openclaw models set <provider/model>")
    assert "docs/COMMANDS.th.md" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "COMMANDS.th.md" in (ROOT / "docs" / "INSTALL.th.md").read_text(encoding="utf-8")


def test_windows_rollover_recovery_docs_match_current_implemented_interfaces():
    installer = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")
    guide = (ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8")

    for parameter in ("Workspace", "RecoverRolloverTransaction", "RecoverRolloverTransactionSha256", "RecoverRolloverSourcePluginRoot", "SkipPlugin", "SkipGatewayRestart", "SkipAgentsPolicy", "LinkPlugin"):
        assert f"${parameter}" in installer, parameter
        assert f"-{parameter}" in guide, parameter
    assert '"--expected-transaction-sha256", $RecoverRolloverTransactionSha256' in installer
    assert '"--expected-replacement-fingerprint", $recoverySourceFingerprint' in installer
    assert "verified-artifact plugin root" in guide
    assert "InstallSourceCommit" not in installer
    assert "no `-InstallSourceCommit`" in guide
