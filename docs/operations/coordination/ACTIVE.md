# Active Coordination Task

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

## Current objective

Task 322 controlled-wake acceptance is complete and its exact-candidate evidence report is published. The next authorized step is to promote the accepted candidate into PR #38 safely and requalify candidate-sensitive GitHub checks against the exact candidate before any merge, tag, or release decision.

## Verified Task 322 completion

- Controlled Wake PASS with exactly one durable work item.
- Candidate identity bound to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
- Runtime, OpenAI, Ollama, Idle Quiescence, and Controlled Wake are PASS.
- Evidence report published at `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`.
- Report commit: `eb1e4ca8968019e440a070f33f681f77ab2f452e`.

## Verified branch relationship

PR #38 current head is `a986f3261b1570d1bcb1574d2458fe7068207a9c`.

The accepted candidate is a strict fast-forward descendant:

```text
base:       a986f3261b1570d1bcb1574d2458fe7068207a9c
candidate:  fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
status:     ahead
 ahead_by:  9
 behind_by: 0
```

Therefore promotion must use a non-force fast-forward update only.

## Required next actions

1. Reconfirm PR #38 is still open and unchanged in base branch, repository, and merge safety metadata.
2. Update the PR head branch `feat/v0.9.5-release-readiness-clean` to candidate `fc3f4bc0...` using non-force fast-forward only.
3. Re-fetch PR #38 and verify its exact head SHA is `fc3f4bc0...`.
4. Re-run and verify candidate-sensitive CI/checks for the promoted PR head.
5. Review the resulting PR diff against `main` and ensure only the accepted candidate lineage is represented.
6. Publish a successor promotion/requalification report with exact evidence.
7. Stop before merge, tag, or GitHub Release; those require a separate successor decision.

## Hard fences

- Do not force-push.
- Do not merge PR #38 in this task.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish GitHub Release.
- Do not mutate provider/model configuration.
- Do not change unrelated services, Scheduled Tasks, or configuration.
- Do not rewrite the accepted candidate history.
- If the PR head cannot be advanced by a non-force fast-forward, stop `BLOCKED` rather than forcing it.
- If candidate-sensitive CI reveals a genuine defect, stop promotion, reproduce, create a new candidate through the normal TDD path, and restart acceptance.
- Do not claim CI or promotion PASS without exact current-head evidence.

## Evidence contract

Promotion evidence must include PR #38 metadata before and after head update, exact candidate SHA, fast-forward relationship, candidate-sensitive check/run results, PR diff identity, and the published successor report location.

## Stop condition

After safe PR promotion and candidate requalification evidence are published, stop. Merge, tagging, and release remain separate successor decisions.
