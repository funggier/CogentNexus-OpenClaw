# Active Coordination Task

Status: `IN_PROGRESS`
Execution mode: `TASK188_RELEASE_PUBLICATION`
Current disposition: `TASK193_PASS__PR26_READY_TO_MERGE`
Task ID: `CNX-20260831-188`
Completed repair: `CNX-20260831-191`
Accepted requalification: `CNX-20260831-192`
Completed CI contract repair: `CNX-20260831-193`
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

## Accepted Windows semantic requalification

Task-192 report:

[`reports/CNX-20260831-192-no-reply-repair-windows-requalification.md`](reports/CNX-20260831-192-no-reply-repair-windows-requalification.md)

Task-192 review:

[`reviews/CNX-20260831-192-no-reply-repair-windows-requalification-review.md`](reviews/CNX-20260831-192-no-reply-repair-windows-requalification-review.md)

Disposition: `PASS`

The real-Windows repaired-candidate acceptance proved:

`1 human Send -> 1 Ticket -> 1 logical OpenClaw run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical visible Dashboard assistant result`

with no bare `NO_REPLY`, no duplicate, no direct recovery, and no pending outbox residue.

## Task-193 CI contract closeout

[`tasks/CNX-20260831-193-recovery-reality-installer-contract-repair.md`](tasks/CNX-20260831-193-recovery-reality-installer-contract-repair.md)

Disposition: `PASS`

Task 193 corrected only the stale Recovery Reality workflow assertion so that:

- managed runtime/recovery remains Ollama-only;
- Windows/POSIX installers remain provider-neutral;
- no product/runtime/plugin/installer/test/dependency behavior was changed.

The exact pre-closeout PR head `743d51d0d789354a419086072fa83eeeacc048cb` passed Validate, PS5.1 Acceptance, Windows Installer Pack, Recovery Reality, Recovery V2/V3, Gateway Convergence, Partial Repair, and Live Runner checks.

## Frozen repaired product candidate

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

This remains the exact product candidate identity for Task-188 real-Windows acceptance evidence. Coordination/CI-contract/report commits after that freeze do not redefine the installed product candidate. The installable plugin payload remains `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files.

## Current objective

Complete final v0.9.3 publication:

1. validate the final coordination-only PR head;
2. fresh-check PR #26 head/base/mergeability and `main` authority;
3. merge PR #26 only when exact-head checks are green, with `expected_head_sha` and no force;
4. freeze exact merged `main` SHA;
5. dispatch `.github/workflows/release.yml` with `version=0.9.3` and `candidate_sha=<exact merged main SHA>`;
6. verify Release workflow success;
7. verify tag `v0.9.3` targets the exact merged SHA;
8. verify release assets and independent checksums;
9. publish final Task-188 report/review and stop.

## Publication fence

Do not dispatch the Release workflow before PR #26 is successfully merged and the exact merged `main` SHA is independently re-read from GitHub.

## Hard fence

No force push, destructive lifecycle action, provider replacement, OpenClaw version change, unrelated product edit, stale PR reuse, or release publication from a non-main SHA is authorized.
