# Active Coordination Task

Status: `FINAL_PRE_MERGE_GATE_REVIEW`
State: `V0.9.5_CANDIDATE_READY_FOR_SEPARATE_MERGE_REVIEW`
Execution mode: `GITHUB_CONTROLLED_REVIEW__NO_MERGE`
Task ID: `CNX-20260913-325`
Parent: `CNX-20260913-324`
Executor: `Hermes`
Runtime witness: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Promoted PR head: `feat/v0.9.5-release-readiness-clean`
Authority branch: `coord/v0.9.5-final-acceptance`

## Verified acceptance lineage

- Task 322 live acceptance evidence is published.
- Task 324 exact-head CI classification is published.
- Candidate-sensitive release-gating workflows: PASS.
- Supporting PS5.1 Live Runner Smoke: PASS.
- Legacy v0.9.3 Recovery Reality workflow: FAIL classified as stale/non-gating due to v0.9.3-specific assertions and over-broad shared-installer path filter.
- No genuine v0.9.5 product defect identified by Task 324.

## Current PR state

```text
PR #38                     OPEN
head                        fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
mergeable                   TRUE (last verified)
merged                      FALSE
base                        main
```

## Task 325 objective

Perform an evidence-only final pre-merge review. Confirm exact head, current main, terminal release-gating CI, legacy required-check semantics, high-level PR diff integrity, and all release safety fences.

The desired result is `READY_FOR_SEPARATE_MERGE_DECISION`, but the task must not merge.

## Hard fences

- No merge in Task 325.
- No tag creation/move/deletion.
- No GitHub Release.
- No source-code changes.
- No workflow changes.
- No force-push or history rewrite.
- No provider/model/config mutation.
- No unrelated service or Scheduled Task changes.
- If a genuine v0.9.5 defect is found, stop and report it rather than patching in place.

## Evidence

- Task 322: `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`
- Task 324: `docs/operations/coordination/reports/CNX-20260913-324-exact-head-ci-gate-classification.md`
- Task 325: `docs/operations/coordination/tasks/CNX-20260913-325-final-pre-merge-gate-review.md`
- PR #38: `https://github.com/funggier/CogentNexus-OpenClaw/pull/38`
