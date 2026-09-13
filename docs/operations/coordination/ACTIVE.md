# Active Coordination Task

Status: `CI_REQUALIFICATION_PENDING`
State: `V0.9.5_CANDIDATE_CI_PENDING`
Execution mode: `GITHUB_CONTROLLED_PROMOTION__NO_MERGE`
Task ID: `CNX-20260913-323`
Parent: `CNX-20260913-322`
Executor: `ChatGPT`
Runtime witness: `Hermes`
Reviewer: `Hermes`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Promoted PR head: `feat/v0.9.5-release-readiness-clean`
Authority branch: `coord/v0.9.5-final-acceptance`

## Verified promotion

- Task 322 Controlled Wake PASS evidence is published.
- Candidate branch resolves exactly to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
- PR #38 head branch was advanced from `a986f3261b1570d1bcb1574d2458fe7068207a9c` to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` using a non-force fast-forward update.
- PR #38 now reports exact candidate head and remains open/unmerged.
- PR #38 description was refreshed to bind the current accepted candidate and current acceptance state.

## Current CI gate

Candidate-sensitive PR-triggered workflow runs have been observed for exact candidate `fc3f4bc0...`:

```text
PS5.1 Live Runner Smoke                 queued
Windows Installer Pack Smoke            queued
Validate                                queued
PS5.1 Acceptance Smoke                  pending
PS5.1 v0.9.3 Ollama Recovery Reality Smoke queued
```

The combined commit status currently has no completed status entries. Therefore CI is **PENDING**, not PASS.

## Required next actions

1. Re-check the exact-head workflow runs until all release-relevant candidate-sensitive checks have reached terminal conclusions.
2. Inspect failures, if any, before taking any corrective action.
3. Verify the final PR diff and mergeability against current `main`.
4. Publish a successor promotion/requalification report recording exact run IDs/conclusions.
5. Stop before merge, tag, or GitHub Release.

## Current PR state

```text
PR #38                     OPEN
head                        fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
mergeable                   TRUE (current GitHub metadata)
merged                      FALSE
candidate-sensitive CI     PENDING
```

## Hard fences

- No force-push.
- No merge in this task.
- No `v0.9.5` tag creation/move/deletion.
- No GitHub Release publication.
- No provider/model/config mutation.
- No unrelated service or Scheduled Task changes.
- No history rewrite.
- Do not claim CI PASS before current exact-head terminal evidence exists.
- If any workflow reveals a genuine code defect, stop and restart through TDD with a new candidate rather than patching in place.

## Evidence locations

- Task 322 report: `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`
- Task 322 report commit: `eb1e4ca8968019e440a070f33f681f77ab2f452e`
- PR #38: `https://github.com/funggier/CogentNexus-OpenClaw/pull/38`
