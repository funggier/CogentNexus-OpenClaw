# Coordination Channel Status

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

## PR promotion state

```text
PR #38                     OPEN
PR head                    fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Promotion                  COMPLETE (non-force fast-forward)
Mergeable                  TRUE (current GitHub metadata)
Merged                     FALSE
```

## Candidate-sensitive CI

Exact-head PR-triggered workflows are currently pending/queued:

```text
PS5.1 Live Runner Smoke
Windows Installer Pack Smoke
Validate
PS5.1 Acceptance Smoke
PS5.1 v0.9.3 Ollama Recovery Reality Smoke
```

Combined commit status currently has no completed status entries. CI therefore remains `PENDING`.

## Required next step

Verify all release-relevant candidate-sensitive workflow runs reach terminal conclusions for exact candidate `fc3f4bc0...`. Inspect any failures before corrective action, then publish the promotion/requalification report. Do not merge until current exact-head evidence is green.

## Release fence

```text
Merge                      BLOCKED
Tag v0.9.5                 NONE
GitHub Release             NONE
Force-push                 NOT PERFORMED
Provider/model mutation    NONE
```

## Hard fences

- No force-push.
- No merge in Task 323.
- No `v0.9.5` tag creation/move/deletion.
- No GitHub Release publication.
- No provider/model/config mutation.
- No unrelated service or Scheduled Task changes.
- Do not claim CI PASS before terminal exact-head evidence exists.
- A genuine code defect requires a new TDD candidate and renewed acceptance.

## Evidence locations

- Task 322 report: `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md`
- Task 322 report commit: `eb1e4ca8968019e440a070f33f681f77ab2f452e`
- PR #38: `https://github.com/funggier/CogentNexus-OpenClaw/pull/38`
