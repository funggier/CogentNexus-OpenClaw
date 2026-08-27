from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


def _workflow():
    # BaseLoader keeps the GitHub Actions key `on` as text instead of YAML 1.1 bool.
    return yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def _all_run_scripts(workflow) -> str:
    scripts = []
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            if "run" in step:
                scripts.append(str(step["run"]))
    return "\n".join(scripts)


def test_release_publication_requires_explicit_human_dispatch_not_push():
    workflow = _workflow()
    triggers = workflow.get("on", {})

    assert "push" not in triggers, "publication workflow must never publish from a branch/tag push"
    dispatch = triggers.get("workflow_dispatch")
    assert isinstance(dispatch, dict), "publication must require explicit workflow_dispatch"

    inputs = dispatch.get("inputs", {})
    for name in ("version", "candidate_sha"):
        assert name in inputs, f"workflow_dispatch is missing required input {name}"
        assert inputs[name].get("required") == "true", f"{name} must be required"


def test_release_checks_out_and_verifies_the_exact_candidate_sha():
    workflow = _workflow()
    steps = workflow["jobs"]["package"]["steps"]
    checkout_steps = [
        step for step in steps
        if str(step.get("uses", "")).startswith("actions/checkout@")
    ]
    assert checkout_steps, "release job must checkout the requested candidate"
    assert any(
        "candidate_sha" in str(step.get("with", {}).get("ref", ""))
        for step in checkout_steps
    ), "release checkout must be pinned to workflow_dispatch candidate_sha"

    scripts = _all_run_scripts(workflow)
    assert "candidate_sha" in scripts
    assert "GITHUB_SHA" in scripts or "git rev-parse HEAD" in scripts
    assert "[0-9a-f]{40}" in scripts or "40" in scripts, "candidate SHA must be exact, not a branch name"


def test_release_version_and_candidate_metadata_are_fail_closed_before_publish():
    workflow = _workflow()
    scripts = _all_run_scripts(workflow)

    for marker in (
        "inputs.version",
        "VERSION",
        "package.json",
        "openclaw.plugin.json",
        "package-lock.json",
        "docs/releases/",
        "candidate_sha",
    ):
        assert marker in scripts, f"release verification is missing {marker}"


def test_release_keeps_duplicate_fence_and_only_publishes_from_dispatch_candidate():
    workflow = _workflow()
    scripts = _all_run_scripts(workflow)

    assert 'gh release view "$tag"' in scripts, "duplicate-release refusal fence must remain"
    assert "gh release create" in scripts
    assert "--target" in scripts
    assert "candidate_sha" in scripts
    assert "GITHUB_REF_TYPE" not in scripts
    assert "GITHUB_REF_NAME#release/" not in scripts
