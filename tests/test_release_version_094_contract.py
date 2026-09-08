from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "0.9.4"


def test_release_metadata_is_aligned_to_next_stability_version():
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == EXPECTED
    package = json.loads((ROOT / "plugins/cogentnexus-openclaw/package.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "plugins/cogentnexus-openclaw/openclaw.plugin.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "plugins/cogentnexus-openclaw/package-lock.json").read_text(encoding="utf-8"))
    assert package["version"] == EXPECTED
    assert manifest["version"] == EXPECTED
    assert lock["version"] == EXPECTED
    assert lock["packages"][""]["version"] == EXPECTED
    assert (ROOT / f"docs/releases/v{EXPECTED}.md").is_file()


def test_release_note_describes_stability_bugfix_followup():
    text = (ROOT / "docs/releases/v0.9.4.md").read_text(encoding="utf-8")
    assert "stability" in text.lower()
    assert "bug" in text.lower() or "fix" in text.lower()


def test_current_facing_documents_use_next_stability_version():
    paths = [
        "README.md",
        "docs/BASELINE.md",
        "docs/CURRENT_STATE.md",
        "docs/INSTALL.md",
        "docs/INSTALL.th.md",
        "docs/PROVIDERS.md",
        "docs/CHECK_SYSTEM.md",
        "docs/CLEAN_REINSTALL.md",
        "docs/CLEAN_REINSTALL.th.md",
        "skills/cogentnexus-openclaw/SKILL.md",
        "skills/cogentnexus-openclaw/templates/lifecycle/README.md",
        "plugins/cogentnexus-openclaw/README.md",
    ]
    for relative in paths:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "v0.9.3" not in text, relative
        assert "v0.9.4" in text, relative


def test_release_workflow_rejects_existing_tag_and_release_before_publication():
    text = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    tag_guard = 'gh api "repos/$GH_REPO/git/ref/tags/$tag"'
    release_guard = 'gh release view "$tag"'
    create = 'gh release create "$tag"'
    assert tag_guard in text
    assert release_guard in text
    assert "already exists" in text
    assert text.index(tag_guard) < text.index(create)
    assert text.index(release_guard) < text.index(create)


def test_internal_v093_compatibility_filename_remains_stable():
    facade = ROOT / "skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py"
    assert facade.is_file()
    assert "cnxclaw_v093.py" in (ROOT / "skills/cogentnexus-openclaw/templates/lifecycle/README.md").read_text(encoding="utf-8")
