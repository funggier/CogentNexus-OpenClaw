import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_baseline_consistency.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("cnx_baseline_checker_under_test", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _copy_tree(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", "node_modules", ".pytest_cache", "__pycache__", "dist", "coverage"),
    )
    return target


def _run_checker(tree: Path) -> int:
    checker = _load_checker()
    checker.ROOT = tree
    return checker.main()


def _rewrite_json_version(path: Path, version: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    if path.name == "package-lock.json":
        data["packages"][""]["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def test_checker_accepts_good_current_tree(tmp_path):
    assert _run_checker(_copy_tree(tmp_path)) == 0


def test_checker_rejects_bridge_metadata_that_disagrees_with_root_version(tmp_path):
    tree = _copy_tree(tmp_path)
    plugin = tree / "plugins" / "cogentnexus-openclaw"
    for name in ("package.json", "openclaw.plugin.json", "package-lock.json"):
        _rewrite_json_version(plugin / name, "0.9.2")

    assert (tree / "VERSION").read_text(encoding="utf-8").strip() == "0.9.3"
    assert _run_checker(tree) == 1


def test_checker_rejects_current_lmstudio_provider_command_drift(tmp_path):
    tree = _copy_tree(tmp_path)
    readme = tree / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\nCurrent command regression: `.\\cnxclaw.cmd start --provider lmstudio`\n",
        encoding="utf-8",
    )

    assert _run_checker(tree) == 1


def test_checker_rejects_non_ollama_v093_provider_facade(tmp_path):
    tree = _copy_tree(tmp_path)
    provider = tree / "skills" / "cogentnexus-openclaw" / "scripts" / "provider_v093.py"
    text = provider.read_text(encoding="utf-8")
    marker = 'SUPPORTED_PROVIDERS = ("ollama",)'
    assert marker in text
    provider.write_text(text.replace(marker, 'SUPPORTED_PROVIDERS = ("ollama", "lmstudio")', 1), encoding="utf-8")

    assert _run_checker(tree) == 1


def test_checker_rejects_stale_generic_launcher_in_current_docs(tmp_path):
    tree = _copy_tree(tmp_path)
    readme = tree / "README.md"
    legacy_launcher = ".\\cnx" + ".cmd status"
    readme.write_text(
        readme.read_text(encoding="utf-8") + f"\nCurrent namespace regression: `{legacy_launcher}`\n",
        encoding="utf-8",
    )

    assert _run_checker(tree) == 1


def test_checker_rejects_missing_verified_delivery_registration(tmp_path):
    tree = _copy_tree(tmp_path)
    entry = tree / "plugins" / "cogentnexus-openclaw" / "src" / "v091-release-entry.ts"
    text = entry.read_text(encoding="utf-8")
    marker = "installV091DashboardVerifiedDelivery(api, config);"
    assert marker in text
    entry.write_text(text.replace(marker, "// verified delivery registration removed by fixture", 1), encoding="utf-8")

    assert _run_checker(tree) == 1


def test_checker_allows_historical_release_notes_to_preserve_lmstudio_evidence(tmp_path):
    tree = _copy_tree(tmp_path)
    historical = tree / "docs" / "releases" / "v0.9.2.md"
    historical.write_text(
        historical.read_text(encoding="utf-8")
        + "\nHistorical evidence: `.\\cnxclaw.cmd start --provider lmstudio`\n",
        encoding="utf-8",
    )

    assert _run_checker(tree) == 0
