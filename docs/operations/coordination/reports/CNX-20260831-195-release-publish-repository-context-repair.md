# CNX-20260831-195 — Release Publish Repository-Context Repair Report

Status: `PASS`
Date: 2026-08-31 ICT
Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-full-stabilization`
Parent: `CNX-20260831-188`

## Summary

Task 194's first v0.9.3 publication attempt failed after the package job because GitHub CLI release commands in the checkout-free publish job had no explicit repository context.

The defect was repaired under TDD without changing any product/runtime/plugin/installer/provider/package payload behavior.

## Failure evidence

Release workflow run `33399493141`:

- event: `workflow_dispatch`;
- requested version: `0.9.3`;
- candidate SHA: `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- package job: PASS;
- publish job: FAIL;
- observed error: `fatal: not a git repository` from GitHub CLI repository discovery;
- no `v0.9.3` tag or GitHub Release was created.

## RED

Commit:

`7fc267dc15cb072079685790850ad57ca4574680`

Regression test:

`tests/test_release_workflow_policy.py::test_release_publish_job_is_repository_explicit_without_checkout_dependency`

Validate run `33403409766` produced the intended RED result. A sampled failing matrix reported:

`1 failed, 474 passed, 33 skipped, 4 subtests passed`

with the new test as the sole pytest failure.

## Minimal repair

Commit:

`6d522806114d46f16a8efcc1c6722fa64ddd75e3`

Diff from RED to fix:

- `.github/workflows/release.yml`: +1 line;
- added `GH_REPO: ${{ github.repository }}` to the `Publish GitHub Release` step;
- no other file changed in the fix commit.

This makes both `gh release view` and `gh release create` repository-explicit while preserving the intentional checkout-free publish job.

## GREEN

Exact fix head `6d522806114d46f16a8efcc1c6722fa64ddd75e3`:

- Validate run `33403566461`: PASS;
- PS5.1 Acceptance Smoke `33403566370`: PASS;
- Windows Installer Pack Smoke `33403566408`: PASS;
- package dry-run in Validate: PASS;
- pytest across Ubuntu/macOS/Windows matrices: PASS;
- npm test/evaluation/audit/plugin validation: PASS.

## Scope proof

No product/runtime/plugin/installer/provider/package payload change was made to repair publication.

The accepted release target remains:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

A future second Release dispatch must execute the repaired workflow from the then-current repaired `main` while still passing `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Final disposition

`PASS`

Ready for a fresh workflow-repair PR to `main`.
