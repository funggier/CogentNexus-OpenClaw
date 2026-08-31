# CNX-20260831-195 — Release Publish Repository-Context Repair

Status: `PASS`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Executor: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Working branch: `agent/v0.9.3-full-stabilization`
Frozen v0.9.3 release target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
Failed Release run: `33399493141`

## Problem

Task 194 dispatched `.github/workflows/release.yml` exactly once with `version=0.9.3` and `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`.

The package job passed, but publish failed because the publish job intentionally had no repository checkout while `gh release view` / `gh release create` relied on local Git repository discovery.

Observed failure:

`failed to run git: fatal: not a git repository (or any of the parent directories): .git`

## TDD evidence

### RED

Commit:

`7fc267dc15cb072079685790850ad57ca4574680`

Added regression test:

`test_release_publish_job_is_repository_explicit_without_checkout_dependency`

Validate run:

`33403409766`

Observed pytest result:

`1 failed, 474 passed, 33 skipped, 4 subtests passed`

The sole failure was the new repository-context assertion.

### Minimal fix

Commit:

`6d522806114d46f16a8efcc1c6722fa64ddd75e3`

Changed only `.github/workflows/release.yml` by one line in the `Publish GitHub Release` environment:

`GH_REPO: ${{ github.repository }}`

No checkout was added to the publish job and no product/runtime/plugin/installer/provider/package bytes changed.

### GREEN

Exact fix-head runs:

- Validate `33403566461`: `completed/success`;
- PS5.1 Acceptance Smoke `33403566370`: `completed/success`;
- Windows Installer Pack Smoke `33403566408`: `completed/success`.

The regression test passed as part of the full pytest matrix, including Windows.

## Disposition

`PASS`

Task 195 proves the release publication workflow can resolve the repository explicitly without depending on a local `.git` checkout in the publish job.

## Publication invariant

The v0.9.3 release target remains frozen at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

The workflow repair must be merged into `main` before a separately authorized second Release dispatch. The repair merge SHA is a workflow-execution identity only and must not replace the accepted v0.9.3 `candidate_sha`.
