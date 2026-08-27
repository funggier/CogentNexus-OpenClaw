from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
PLUGIN_DIR = "plugins/cogentnexus-openclaw"
REQUIRED_ARCHIVE_PAYLOAD = (
    f"{PLUGIN_DIR}/dist/v091-release-entry.js",
    f"{PLUGIN_DIR}/scripts/bootstrap-ticket-db.mjs",
    f"{PLUGIN_DIR}/openclaw.plugin.json",
    f"{PLUGIN_DIR}/README.md",
    f"{PLUGIN_DIR}/package.json",
)


def _package_steps():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return workflow["jobs"]["package-dry-run"]["steps"]


def _step_runs():
    return [
        (
            step.get("name", ""),
            step.get("working-directory", ""),
            str(step.get("run", "")),
        )
        for step in _package_steps()
    ]


def _index_of_run(fragment: str) -> int:
    for index, (_, _, run) in enumerate(_step_runs()):
        if fragment in run:
            return index
    raise AssertionError(f"package-dry-run is missing required command: {fragment}")


def test_package_dry_run_builds_and_validates_plugin_before_staging_archive():
    steps = _step_runs()
    npm_ci = [index for index, (_, cwd, run) in enumerate(steps) if cwd == PLUGIN_DIR and "npm ci" in run]
    plugin_validate = [
        index
        for index, (_, cwd, run) in enumerate(steps)
        if cwd == PLUGIN_DIR and "npm run plugin:validate" in run
    ]
    assert npm_ci, "package-dry-run must install plugin dependencies on its own clean runner"
    assert plugin_validate, "package-dry-run must build/validate the plugin before archiving"

    stage = _index_of_run("rsync -a")
    assert npm_ci[0] < plugin_validate[0] < stage


def test_package_dry_run_proves_required_payload_in_stage_and_both_archives():
    script = "\n".join(run for _, _, run in _step_runs())

    for path in REQUIRED_ARCHIVE_PAYLOAD:
        assert path in script, f"package-dry-run never asserts required payload path: {path}"

    # Archive integrity alone is insufficient. The job must list both archive
    # formats and compare required paths against those listings.
    assert "tar -tzf" in script
    assert "unzip -Z1" in script or "zipinfo -1" in script
    assert "grep -F" in script or "comm " in script or "diff " in script


def test_package_dry_run_records_exact_candidate_provenance_and_uploads_proof():
    steps = _package_steps()
    script = "\n".join(str(step.get("run", "")) for step in steps)

    plugin_validate = _index_of_run("npm run plugin:validate")
    identity = _index_of_run("plugin_payload_identity.py")
    stage = _index_of_run("rsync -a")
    assert plugin_validate < identity < stage

    for marker in (
        "PACKAGE_IDENTITY.json",
        "GITHUB_SHA",
        "sourceCommit",
        "packageVersion",
        "payloadV2Fingerprint",
        "payloadFileCount",
        "archiveSha256",
        "SHA256SUMS.txt",
    ):
        assert marker in script, f"package provenance is missing semantic marker: {marker}"

    uploads = [
        step for step in steps
        if str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]
    assert uploads, "package-dry-run must retain the exact package proof as an Actions artifact"
    assert any(
        "release" in str(step.get("with", {}).get("path", "")).lower()
        for step in uploads
    ), "package proof upload must include the release/provenance directory"
