# CNX-20260913-325 — Final Pre-Merge Gate Review

## Authority

- **Task ID**: CNX-20260913-325
- **Parent**: CNX-20260913-324
- **Repository**: `funggier/CogentNexus-OpenClaw`
- **PR**: #38
- **Candidate SHA**: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
- **PR head**: `feat/v0.9.5-release-readiness-clean`
- **Base**: `main`
- **Executor**: Hermes
- **Reviewer**: ChatGPT

## Objective

Perform a final evidence-only pre-merge review of PR #38 after Task 324 classified the exact-head CI.

The purpose is to determine whether the candidate is ready for a **separate controlled merge decision**. This task must not merge, tag, release, or modify the candidate.

## Required checks

1. Re-verify PR #38 exact head is still `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Re-verify PR is OPEN and UNMERGED.
3. Re-verify current `main` head and the PR's mergeability metadata.
4. Verify all release-gating exact-head workflows from Task 324 remain terminal SUCCESS:
   - Validate
   - PS5.1 Acceptance Smoke
   - Windows Installer Pack Smoke
5. Verify supporting PS5.1 Live Runner Smoke remains SUCCESS.
6. Verify the v0.9.3 Ollama Recovery Reality failure is exactly the stale workflow-contract/path-filter issue documented in Task 324, and does not represent a v0.9.5 product failure.
7. Inspect the PR diff at a high level against current `main` for unexpected changes, unrelated files, release artifacts, or provider/config mutations.
8. Explicitly inspect whether the legacy failing workflow creates a GitHub required-check/merge-block condition. Do not assume `mergeable=true` means all branch-protection requirements are satisfied.
9. Confirm there is no evidence of force-push, history rewrite, tag movement, GitHub Release publication, provider/model mutation, or unrelated service changes.

## Decision output

Return one of:

- `READY_FOR_SEPARATE_MERGE_DECISION`
- `MERGE_BLOCKED`
- `CANDIDATE_INVALID`

The result must include exact evidence for every release-gating check and the required-check semantics of the legacy failure.

## Hard fences

- **NO merge** in this task.
- No tag create/move/delete.
- No GitHub Release.
- No source-code changes.
- No workflow changes.
- No force-push.
- No history rewrite.
- No provider/model/config mutation.
- No restoration of `ollama/qwen3.5:9b`.
- If a genuine v0.9.5 defect is discovered, stop and report it; do not patch in place.

## Evidence

Primary prior report:
`docs/operations/coordination/reports/CNX-20260913-324-exact-head-ci-gate-classification.md`

Runtime acceptance report:
`docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`
