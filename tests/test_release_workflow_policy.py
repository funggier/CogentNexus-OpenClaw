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

    source = WORKFLOW.read_text(encoding="utf-8")
    scripts = _all_run_scripts(workflow)
    assert "inputs.candidate_sha" in source
    assert "CANDIDATE_SHA" in scripts
    assert "git rev-parse HEAD" in scripts
    assert "[0-9a-f]{40}" in scripts or "40" in scripts, "candidate SHA must be exact, not a branch name"


def test_release_version_and_candidate_metadata_are_fail_closed_before_publish():
    workflow = _workflow()
    source = WORKFLOW.read_text(encoding="utf-8")
    scripts = _all_run_scripts(workflow)

    assert "inputs.version" in source
    assert "inputs.candidate_sha" in source
    assert "REQUESTED_VERSION" in scripts
    assert "CANDIDATE_SHA" in scripts
    for marker in (
        "VERSION",
        "package.json",
        "openclaw.plugin.json",
        "package-lock.json",
        "docs/releases/",
    ):
        assert marker in scripts, f"release verification is missing {marker}"


def test_release_keeps_duplicate_fence_and_only_publishes_from_dispatch_candidate():
    workflow = _workflow()
    scripts = _all_run_scripts(workflow)

    assert 'gh release view "$tag"' in scripts, "duplicate-release refusal fence must remain"
    assert "gh release create" in scripts
    assert "--target" in scripts
    assert "CANDIDATE_SHA" in scripts
    assert "GITHUB_REF_TYPE" not in scripts
    assert "GITHUB_REF_NAME#release/" not in scripts


def test_release_publish_job_is_repository_explicit_without_checkout_dependency():
    workflow = _workflow()
    publish_steps = workflow["jobs"]["publish"]["steps"]
    release_steps = [
        step for step in publish_steps
        if "gh release create" in str(step.get("run", ""))
    ]
    assert release_steps, "publish job must contain the GitHub Release publication step"

    step = release_steps[0]
    env = step.get("env", {})
    run = str(step.get("run", ""))
    gh_repo = str(env.get("GH_REPO", ""))
    has_explicit_repo_env = "github.repository" in gh_repo
    has_explicit_repo_arg = "--repo" in run and (
        "GITHUB_REPOSITORY" in run or "github.repository" in run
    )

    assert has_explicit_repo_env or has_explicit_repo_arg, (
        "publish job must identify the GitHub repository explicitly instead of relying "
        "on current-working-directory git metadata"
    )
