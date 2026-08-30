# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `CI_TASK167_EXACT_SHA_VALIDATE_RERUN_HERMES`
Current authorization: `CNX-20260831-169_HERMES_TASK167_EXACT_SHA_VALIDATE_RERUN`
Task ID: `CNX-20260831-169`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun.md`](tasks/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun.md)

Task 169 is the CI-only completion gate for the single remaining Task-167 acceptance gap.

## Frozen product candidate

Exact repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

No later coordination commit is a replacement product candidate.

Pinned OpenClaw:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

## Task 168 review

Task-168 report:

`reports/CNX-20260831-168-hermes-task167-verification-completion.md`

ChatGPT review:

`reviews/CNX-20260831-168-hermes-task167-verification-completion-review.md`

Disposition:

`REWORK_REQUIRED — EXACT_SHA_VALIDATE_CANCELLED_BY_COORDINATION_CONCURRENCY`

Task 168 completed the local/build/package/Python/evaluation evidence, risk analysis, acceptance matrix, and verification packet. Exact-SHA PS5.1 and Windows Installer Pack workflows succeeded. Exact-SHA Validate remained unproven because run `33330458434` was cancelled by branch-level concurrency after a later coordination push.

## Current gate

Hermes/Codex must rerun Validate `33330458434` against exact product SHA `231761f...`, preserve that exact head SHA, inspect the full final matrix, and publish its report only after the rerun is terminal.

### Coordination freeze

After this Task-169 activation commit is visible remotely, no branch commit may be pushed while the exact-SHA Validate rerun is queued or in progress.

This freeze exists because `.github/workflows/validate.yml` uses branch-level concurrency with `cancel-in-progress: true`; another push can cancel the evidence run.

## Hard fence

CI verification only.

No source/test/workflow modification; no dependency/OpenClaw upgrade; no Dashboard semantic Send; no live runtime/install/database/transcript mutation; no release/promotion; no default/release merge; no force push; and no report/coordination push before the exact-SHA rerun reaches terminal state.

Task-169 PASS still requires ChatGPT review before the Task-167 repair can be accepted and before a separate Windows install-over/provenance task may be opened.
