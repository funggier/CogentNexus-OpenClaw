# Active Coordination Task

Status: `IN_PROGRESS`
Execution mode: `TASK188_RELEASE_PUBLICATION`
Current disposition: `TASK192_ACCEPTED_RELEASE_PUBLICATION_READY`
Task ID: `CNX-20260831-188`
Completed repair: `CNX-20260831-191`
Accepted requalification: `CNX-20260831-192`
Updated: 2026-08-31 ICT
Executor: ChatGPT / GitHub repository + Actions
Coordinator / final reviewer: ChatGPT
Human release authority: User

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative for coordination history.

## Active umbrella task

[`tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md`](tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md)

## Task-192 acceptance

Task-192 report:

[`reports/CNX-20260831-192-no-reply-repair-windows-requalification.md`](reports/CNX-20260831-192-no-reply-repair-windows-requalification.md)

Task-192 review:

[`reviews/CNX-20260831-192-no-reply-repair-windows-requalification-review.md`](reviews/CNX-20260831-192-no-reply-repair-windows-requalification-review.md)

Review disposition:

`PASS`

The real-Windows repaired-candidate acceptance proved:

`1 human Send -> 1 Ticket -> 1 logical OpenClaw run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical visible Dashboard assistant result`

with no bare `NO_REPLY`, no duplicate, no direct recovery, and no pending outbox residue.

## Frozen repaired product candidate

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

This remains the exact product candidate identity for Task 188 acceptance evidence.

Later coordination/review/report commits do not redefine that product candidate.

## Current objective

Resume final v0.9.3 publication:

1. fresh-check `main`, current branch, open PRs, tags/releases, and publication topology;
2. create a fresh PR from `agent/v0.9.3-full-stabilization` to `main`;
3. inspect exact PR diff/topology/checks and ensure historical PR #24 is not reused;
4. merge only when green, with no force;
5. freeze exact merged `main` SHA;
6. dispatch `.github/workflows/release.yml` with `version=0.9.3` and `candidate_sha=<exact merged main SHA>`;
7. verify Release workflow success;
8. verify tag `v0.9.3` targets the exact merged SHA;
9. verify release assets and independent checksums;
10. publish final Task-188 report/review and stop.

## Publication fence

Do not dispatch the Release workflow before a fresh PR review and exact successful merge to `main`.

## Hard fence

No force push, destructive lifecycle action, provider replacement, OpenClaw version change, unrelated product edit, or stale PR reuse is authorized.
