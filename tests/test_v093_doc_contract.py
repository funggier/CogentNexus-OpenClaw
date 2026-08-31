from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_DOCS = (
    ROOT / "README.md",
    ROOT / "docs" / "CURRENT_STATE.md",
    ROOT / "docs" / "INSTALL.md",
    ROOT / "docs" / "INSTALL.th.md",
    ROOT / "docs" / "PROVIDERS.md",
    ROOT / "docs" / "CHECK_SYSTEM.md",
    ROOT / "docs" / "BASELINE.md",
    ROOT / "skills" / "cogentnexus-openclaw" / "SKILL.md",
    ROOT / "plugins" / "cogentnexus-openclaw" / "README.md",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_v093_current_docs_do_not_advertise_lmstudio_provider_commands():
    forbidden = (
        "--provider lmstudio",
        "-Provider lmstudio",
        "--provider=lmstudio",
    )
    violations = []
    for path in CURRENT_DOCS:
        text = _text(path)
        for literal in forbidden:
            if literal in text:
                violations.append(f"{path.relative_to(ROOT)}: {literal}")
    assert not violations, "current v0.9.3 docs advertise LM Studio commands:\n" + "\n".join(violations)


def test_v093_docs_name_validated_openclaw_baseline():
    for path in (ROOT / "README.md", ROOT / "docs" / "CURRENT_STATE.md", ROOT / "docs" / "INSTALL.md"):
        assert "2026.7.1-2" in _text(path), f"{path.relative_to(ROOT)} lacks validated OpenClaw baseline"


def test_current_install_docs_do_not_claim_unpublished_v093_release_exists():
    for path in (ROOT / "docs" / "INSTALL.md", ROOT / "docs" / "INSTALL.th.md"):
        text = _text(path)
        forbidden = (
            "from the v0.9.3 GitHub Release",
            "จาก GitHub Release v0.9.3",
        )
        assert not any(literal in text for literal in forbidden), (
            f"{path.relative_to(ROOT)} claims an unpublished v0.9.3 release exists"
        )


def test_v093_current_docs_state_ollama_only_managed_provider():
    required = "Ollama only"
    for path in (ROOT / "README.md", ROOT / "docs" / "CURRENT_STATE.md", ROOT / "docs" / "INSTALL.md"):
        assert required in _text(path), f"{path.relative_to(ROOT)} does not state the v0.9.3 Ollama-only contract"
