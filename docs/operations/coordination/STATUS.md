# Coordination Channel Status

Status: `READY_FOR_PROMOTION`
State: `V0.9.5_PR_PROMOTION_REQUALIFICATION_PENDING`
Execution mode: `GITHUB_CONTROLLED_PROMOTION__NO_MERGE`
Task ID: `CNX-20260913-323`
Parent: `CNX-20260913-322`
Executor: `ChatGPT`
Runtime witness: `Hermes`
Reviewer: `Hermes`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 322 is complete. Its exact-candidate Controlled Wake evidence is published on the authority branch. Task 323 now governs safe promotion of the accepted candidate into PR #38 and candidate-sensitive CI requalification.

## Acceptance state

```text
Candidate                  fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime                    PASS
OpenAI                     PASS / REQUIRED
Ollama                     PASS / REQUIRED
LM Studio                  NOT REQUIRED
Idle Quiescence            PASS
Controlled Wake            PASS
Evidence                   PUBLISHED
Task 322                   COMPLETE
```

## PR promotion gate

```text
PR #38                     OPEN
Current PR head            a986f3261b1570d1bcb1574d2458fe7068207a9c
Accepted candidate         fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Relationship               candidate ahead 9 / behind 0
Promotion mode             FAST-FORWARD ONLY
Merge                      BLOCKED
Tag v0.9.5                 NONE
GitHub Release             NONE
```

## Required next step

Safely advance PR #38 head branch to the accepted candidate using a non-force fast-forward update, re-verify the exact PR head, then run and verify candidate-sensitive CI/checks against that exact head. Publish the promotion/requalification evidence before any merge decision.

## Hard fences

- No force-push.
- No merge.
- No `v0.9.5` tag creation/move/deletion.
- No GitHub Release publication.
- No provider/model/config mutation.
- No unrelated service or Scheduled Task changes.
- No history rewrite.
- If fast-forward promotion is not possible, stop `BLOCKED`.
- If candidate-sensitive CI fails due to a genuine code defect, stop and restart through a new TDD candidate/requalification path.
- No inferred PASS without current exact-head evidence.

## Evidence locations

- Task 322 report: `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`
- Task 322 report commit: `eb1e4ca8968019e440a070f33f681f77ab2f452e`
