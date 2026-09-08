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
