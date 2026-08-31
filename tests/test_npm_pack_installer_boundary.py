"""CNX-20260827-082 — npm pack artifact boundary contract."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / "scripts" / "resolve-npm-pack-artifact.ps1"
INSTALLER = REPO / "scripts" / "install.ps1"


def run_helper(payload, plugin_dir: Path):
    fixture = plugin_dir / "pack-fixture.json"
    fixture.write_text(json.dumps(payload), encoding="utf-8")
    harness = plugin_dir / "invoke-helper.ps1"
    harness.write_text(
        "$ErrorActionPreference='Stop'\n"
        f". '{HELPER.as_posix()}'\n"
        f"$result=Resolve-NpmPackArtifact -PackJson ([IO.File]::ReadAllText('{fixture.as_posix()}')) -PluginDir '{plugin_dir.as_posix()}'\n"
        "$result | ConvertTo-Json -Compress\n",
        encoding="utf-8",
    )
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(harness)],
        text=True,
        capture_output=True,
        check=False,
    )


def item(filename: str):
    return {"filename": filename}


def test_npm11_array_resolves_existing_exact_artifact(tmp_path: Path):
    artifact = tmp_path / "openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz"
    artifact.write_bytes(b"artifact")
    result = run_helper([item(artifact.name)], tmp_path)
    assert result.returncode == 0, result.stderr
    assert Path(json.loads(result.stdout)["path"]) == artifact


def test_npm12_keyed_object_resolves_existing_exact_artifact(tmp_path: Path):
    artifact = tmp_path / "openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz"
    artifact.write_bytes(b"artifact")
    result = run_helper({"openclaw-plugin-cogentnexus-openclaw": item(artifact.name)}, tmp_path)
    assert result.returncode == 0, result.stderr
    assert Path(json.loads(result.stdout)["path"]) == artifact


def test_malformed_pack_shapes_fail_closed(tmp_path: Path):
    cases = [None, [], [item("a.tgz"), item("b.tgz")], {}, {"a": item("a.tgz"), "b": item("b.tgz")}, ["not-an-item"], [item("")], [item("../escape.tgz")], [item("nested/escape.tgz")], [item("C:\\escape.tgz")]]
    for payload in cases:
        result = run_helper(payload, tmp_path)
        assert result.returncode != 0, payload


def test_missing_artifact_fails_closed(tmp_path: Path):
    result = run_helper([item("missing.tgz")], tmp_path)
    assert result.returncode != 0


def test_install_wires_single_normalizer_and_exact_artifact(tmp_path: Path):
    source = INSTALLER.read_text(encoding="utf-8")
    assert "resolve-npm-pack-artifact.ps1" in source
    assert "Resolve-NpmPackArtifact" in source
    assert "Test-Path -LiteralPath $packagePath" in source
    assert 'openclaw plugins install $packagePath --force' in source
    assert 'openclaw plugins install ("npm-pack:" + $packagePath) --force' not in source
    assert "Remove-Item -LiteralPath $packagePath" in source


def test_install_does_not_rollover_before_artifact_resolution():
    source = INSTALLER.read_text(encoding="utf-8")
    artifact_pos = source.index("Resolve-NpmPackArtifact")
    rollover_pos = source.index("$rolloverStaging")
    assert artifact_pos < rollover_pos
