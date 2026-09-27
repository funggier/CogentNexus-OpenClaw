from __future__ import annotations

import hashlib
import importlib.util
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_documentation_archive.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("cnx_doc_archive", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_documentation_archive_is_deterministic_and_bounded(tmp_path):
    builder = _load_builder()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    a = builder.build_archive(ROOT, version, first)
    b = builder.build_archive(ROOT, version, second)
    assert a["fileCount"] > 20
    assert a["sha256"] == b["sha256"]
    assert hashlib.sha256(first.read_bytes()).hexdigest() == a["sha256"]
    prefix = f"cogentnexus-openclaw-v{version}-document/"
    with zipfile.ZipFile(first) as archive:
        names = set(archive.namelist())
    required = {
        prefix + "DOCUMENTATION_INDEX.md",
        prefix + "README.md",
        prefix + "LICENSE",
        prefix + "VERSION",
        prefix + "docs/INSTALL.md",
        prefix + "docs/INSTALL.th.md",
        prefix + "docs/COMMANDS.th.md",
        prefix + "docs/CLEAN_REINSTALL.md",
        prefix + "docs/CLEAN_REINSTALL.th.md",
        prefix + "docs/CURRENT_STATE.md",
        prefix + "docs/BASELINE.md",
        prefix + "docs/PROVIDERS.md",
        prefix + "docs/operations/ROADMAP.md",
        prefix + "docs/operations/STATUS.md",
        prefix + f"docs/releases/v{version}.md",
        prefix + "skills/cogentnexus-openclaw/SKILL.md",
        prefix + "skills/cogentnexus-openclaw/references/runtime-lifecycle.md",
        prefix + "plugins/cogentnexus-openclaw/README.md",
    }
    assert required <= names
    assert all(name.startswith(prefix) for name in names)
    assert not any("/docs/operations/coordination/" in "/" + name for name in names)
    assert not any("/.git/" in "/" + name for name in names)
    assert not any("/node_modules/" in "/" + name for name in names)
