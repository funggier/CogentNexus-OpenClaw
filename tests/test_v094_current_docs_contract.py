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


def test_windows_rollover_recovery_docs_match_current_implemented_interfaces():
    installer = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")
    guide = (ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8")

    for parameter in ("Workspace", "RecoverRolloverTransaction", "RecoverRolloverTransactionSha256", "SkipPlugin", "SkipGatewayRestart", "SkipAgentsPolicy", "LinkPlugin"):
        assert f"${parameter}" in installer, parameter
        assert f"-{parameter}" in guide, parameter
    assert '"--expected-transaction-sha256", $RecoverRolloverTransactionSha256' in installer
    assert '"--expected-replacement-fingerprint", $recoverySourceFingerprint' in installer
    assert "source-derived expected replacement fingerprint" in guide
    assert "InstallSourceCommit" not in installer
    assert "no `-InstallSourceCommit`" in guide
