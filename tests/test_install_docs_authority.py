from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = (ROOT / "docs" / "INSTALL.md", ROOT / "docs" / "INSTALL.th.md")


def test_canonical_install_docs_separate_install_prerequisites_from_runtime_readiness():
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        marker = "## Requirements" if path.name == "INSTALL.md" else "## สิ่งที่ต้องมี"
        end_marker = "## Development-candidate source install" if path.name == "INSTALL.md" else "## ติดตั้งจาก development candidate"
        requirements = text.split(marker, 1)[1].split(end_marker, 1)[0].lower()
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
        install_section = text.split("## development-candidate source install", 1)[1].split("## what the installer does", 1)[0] if path.name == "INSTALL.md" else text.split("## ติดตั้งจาก development candidate", 1)[1].split("## สิ่งที่ installer ทำ", 1)[0]
        assert "--provider" not in install_section.lower()
        assert "-provider" not in install_section.lower()


def test_doc_contract_does_not_use_coordination_tasks_as_public_command_authority():
    source = (ROOT / "tests" / "test_posix_provider_neutral_installer_boundary.py").read_text(encoding="utf-8")
    assert "docs/operations/coordination/tasks" not in source
