from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = (ROOT / "docs" / "INSTALL.md", ROOT / "docs" / "INSTALL.th.md")


def test_canonical_install_docs_separate_install_prerequisites_from_runtime_readiness():
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        requirements = text.lower().split("## what the installer does")[0] if path.name == "INSTALL.md" else text.split("## สิ่งที่ installer ทำ")[0]
        assert "ollama" not in requirements
        assert "ollama" not in requirements.lower()


def test_canonical_install_docs_use_provider_free_source_install_commands():
    english = (ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8")
    thai = (ROOT / "docs" / "INSTALL.th.md").read_text(encoding="utf-8")
    assert '.\\scripts\\install.ps1 -Workspace "$HOME\\.openclaw\\workspace"' in english
    assert './scripts/install.sh --workspace "$HOME/.openclaw/workspace"' in english
    assert '.\\scripts\\install.ps1 -Workspace "$HOME\\.openclaw\\workspace"' in thai
    assert './scripts/install.sh --workspace "$HOME/.openclaw/workspace"' in thai


def test_canonical_install_docs_do_not_claim_installer_owns_provider_preflight():
    for path in DOCS:
        text = path.read_text(encoding="utf-8").lower()
        assert "provider/gateway preflight" not in text
        assert "ตรวจ provider/gateway preflight" not in text
        assert "--provider ollama" not in text
        assert "-provider ollama" not in text


def test_doc_contract_does_not_use_coordination_tasks_as_public_command_authority():
    source = (ROOT / "tests" / "test_posix_provider_neutral_installer_boundary.py").read_text(encoding="utf-8")
    assert "docs/operations/coordination/tasks" not in source
