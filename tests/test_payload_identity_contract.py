import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNERSHIP_SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "namespace_ownership.py"
IDENTITY_SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "plugin_payload_identity.py"
SPEC = importlib.util.spec_from_file_location("namespace_ownership_payload_identity", OWNERSHIP_SCRIPT)
assert SPEC and SPEC.loader
ownership = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ownership)


def _write_plugin(root: Path) -> Path:
    (root / "dist").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "package.json").write_text(json.dumps({
        "name": ownership.PLUGIN_PACKAGE,
        "version": ownership.INSTALLED_VERSION,
        "files": ["dist", "scripts/bootstrap-ticket-db.mjs", "openclaw.plugin.json", "README.md"],
    }), encoding="utf-8")
    (root / "openclaw.plugin.json").write_text(json.dumps({
        "id": ownership.PRODUCT_ID,
        "version": ownership.INSTALLED_VERSION,
    }), encoding="utf-8")
    (root / "README.md").write_text("readme", encoding="utf-8")
    (root / "scripts" / "bootstrap-ticket-db.mjs").write_text("bootstrap", encoding="utf-8")
    (root / "dist" / "v091-release-entry.js").write_text("entry", encoding="utf-8")
    return root


def test_payload_identity_helper_reuses_payload_v2_fingerprint_and_exact_file_count(tmp_path: Path):
    plugin = _write_plugin(tmp_path / "plugin")
    existing = ownership.plugin_fingerprint(plugin)
    result = subprocess.run(
        [
            sys.executable,
            str(IDENTITY_SCRIPT),
            "--plugin-root",
            str(plugin),
            "--version",
            ownership.INSTALLED_VERSION,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    identity = json.loads(result.stdout)
    assert identity["version"] == ownership.INSTALLED_VERSION
    assert identity["fingerprint"] == existing["fingerprint"]
    assert identity["fileCount"] == 5
    assert len(identity["fingerprint"]) == 64
