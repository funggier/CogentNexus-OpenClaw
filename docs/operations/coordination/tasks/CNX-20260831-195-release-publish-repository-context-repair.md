# CNX-20260831-195 — Release Publish Repository-Context Repair

Status: `IN_PROGRESS`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Executor: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Working branch: `agent/v0.9.3-full-stabilization`
Frozen published-candidate main SHA: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
Failed Release run: `33399493141`

## Problem

Task 194 dispatched `.github/workflows/release.yml` exactly once with `version=0.9.3` and `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`.

The `package` job passed, but `publish / Publish GitHub Release` failed with:

`failed to run git: fatal: not a git repository (or any of the parent directories): .git`

The publish job intentionally downloads validated artifacts without checking out the repository. Its `gh release view` / `gh release create` commands therefore must identify the target repository explicitly instead of relying on GitHub CLI repository discovery from a local `.git` directory.

## Scope

Allowed:

- add a focused regression test for repository-explicit release publication;
- minimally repair `.github/workflows/release.yml` so the publish step identifies `funggier/CogentNexus-OpenClaw` through GitHub Actions repository context;
- coordination/report/review documentation for this repair;
- normal PR/CI merge of the workflow-only repair into `main` after GREEN.

Not allowed:

- product/runtime/plugin/installer/provider behavior changes;
- package payload changes;
- release metadata/version changes;
- manual tag/release creation outside the workflow;
- retargeting the v0.9.3 candidate away from `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- force push.

## TDD contract

### RED

Add a regression assertion that the `publish` job can resolve the repository without requiring `actions/checkout` / current-working-directory git metadata. The test must fail against the Task-194 workflow shape.

### Minimal fix

Prefer repository-explicit GitHub CLI context in the publish step, for example `GH_REPO: ${{ github.repository }}` or equivalent explicit `--repo` arguments. Do not add an unnecessary checkout merely to make repository discovery work.

### GREEN

The focused release workflow policy test and normal repository Validate/PR gates must pass on the exact repaired head.

## Publication fence

Do not dispatch Release again until:

1. RED is proven;
2. minimal workflow repair is GREEN;
3. workflow-only repair is merged to `main` through a fresh PR;
4. exact new `main` SHA is frozen as workflow execution ref while `candidate_sha` remains the already accepted release candidate `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
5. tag/release `v0.9.3` are still absent.

A subsequent publication task must authorize the second Release dispatch explicitly and must preserve the original candidate SHA as the release target.
