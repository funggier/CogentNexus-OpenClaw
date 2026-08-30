# CNX-20260831-169 — Hermes/Codex Exact-SHA Validate Rerun Completion

Status: `READY_HERMES`

Execution mode: `CI_TASK167_EXACT_SHA_VALIDATE_RERUN_HERMES`

Current authorization: `CNX-20260831-169_HERMES_TASK167_EXACT_SHA_VALIDATE_RERUN`

Task ID: `CNX-20260831-169`

Updated: 2026-08-31 ICT

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

Review model: `executor-heavy / reviewer-light`

## Purpose

Close the single remaining repository acceptance gap for the Task-167 repair by obtaining one uninterrupted successful GitHub `Validate` execution against the exact frozen product repair SHA.

This task is CI-only. It does not authorize product/source changes or live/runtime actions.

## Frozen product candidate

Exact Task-167 repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Pinned OpenClaw target remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

Task-168 report:

`docs/operations/coordination/reports/CNX-20260831-168-hermes-task167-verification-completion.md`

Task-168 ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260831-168-hermes-task167-verification-completion-review.md`

## Accepted evidence entering this task

The following exact-SHA gates are already successful and do not need to be rerun merely for duplication:

- PS5.1 Acceptance Smoke `33330458475`: `SUCCESS`;
- Windows Installer Pack Smoke `33330458470`: `SUCCESS`.

Task 168 also reported PASS for local source/build/package/Python/evaluation validation and completed the required risk analysis, acceptance matrix, and Reviewer Verification Packet.

The only unresolved mandatory gate is:

- Validate `33330458434`: `CANCELLED`.

## Proven cancellation mechanism

The repair Validate run was not observed to fail a product assertion. It was cancelled by branch-level workflow concurrency after a later coordination push.

At repair SHA `231761f...`, `.github/workflows/validate.yml` defines:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref_name }}
  cancel-in-progress: true
```

Repair Validate `33330458434`:

- started: `2026-08-30T19:17:33Z`;
- final: `cancelled` at `2026-08-30T19:20:19Z`.

Later coordination commit `05f86ba565367d0e4ad91850c2ea291e40eae8f8` triggered newer Validate `33330579992` at `2026-08-30T19:20:07Z`.

Therefore Task 169 must prevent any new branch push from cancelling the exact-SHA rerun.

## Critical coordination freeze

After the coordination commit that activates Task 169 is visible on remote GitHub:

**DO NOT PUSH ANY COMMIT TO `agent/v0.9.3-full-stabilization` WHILE THE EXACT-SHA VALIDATE RERUN IS IN PROGRESS.**

This applies to executor reports, ACTIVE/STATUS updates, documentation, source, tests, and unrelated work.

The executor may publish the Task-169 report only after the exact-SHA Validate rerun has reached a terminal state and its final evidence has been captured.

If a concurrent external push occurs while the rerun is active, inspect whether it cancelled/replaced the rerun. If exact-SHA success can no longer be proven, report `REWORK_REQUIRED` rather than inferring success.

## Required execution

1. Fetch and synchronize current remote coordination state.
2. Verify `ACTIVE.md` and `STATUS.md` authorize only Task 169.
3. Verify frozen product candidate `231761fca24c315e90536955d3e384f55e2e232e` remains an ancestor and no later product/source change is being substituted as the candidate.
4. Reconfirm prior exact-SHA run states for `33330458475`, `33330458470`, and `33330458434`.
5. Rerun GitHub Validate run `33330458434` using the supported GitHub/`gh` rerun mechanism. The rerun must still target head SHA `231761fca24c315e90536955d3e384f55e2e232e`.
6. Record the resulting run ID and `run_attempt`.
7. Do not push while the rerun is queued or in progress.
8. Wait for the rerun to reach terminal state using GitHub Actions state, not a fixed sleep assumption.
9. Inspect the full job matrix and record each job conclusion.
10. Require overall workflow conclusion `success` and no unexpected cancelled/failed jobs.
11. If the rerun fails, investigate enough to distinguish product/test failure from infrastructure/orchestration failure, but do not modify product source in Task 169.
12. Only after terminal evidence is captured, publish the matching report.

## Acceptance contract

Task 169 is `PASS` only if all are true:

- rerun targets exact head SHA `231761fca24c315e90536955d3e384f55e2e232e`;
- GitHub reports the rerun completed;
- overall `Validate` conclusion is `success`;
- required matrix/jobs complete successfully without unexplained cancellation;
- no product/source/dependency change occurred;
- no live/runtime mutation occurred;
- coordination freeze was respected while rerun was active;
- report includes exact durable evidence and Reviewer Verification Packet.

A failed or cancelled rerun is not PASS.

## Hard fence

Task 169 must not:

- modify production source or tests;
- modify workflow definitions merely to obtain green CI;
- upgrade dependencies or OpenClaw;
- perform Dashboard semantic Send or any other semantic live input;
- install-over, uninstall, reinstall, or reset;
- mutate Gateway/Ollama/Supervisor/OpenClaw runtime;
- mutate live Ticket/database/transcript/delivery state;
- publish a release/tag/package;
- merge to default/release branch;
- force push;
- push a report or any other branch commit before the exact-SHA Validate rerun has reached terminal state.

If evidence indicates a real product or workflow defect requiring edits, report `FAIL` or `REWORK_REQUIRED` after the active rerun is terminal. ChatGPT will open a separate task.

## Required report

Create only after the exact-SHA rerun is terminal:

`docs/operations/coordination/reports/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun.md`

The report must include:

- disposition;
- starting coordination HEAD;
- frozen candidate SHA;
- prior run `33330458434` state;
- rerun command/action;
- run ID and run attempt;
- exact head SHA from GitHub;
- final workflow status/conclusion;
- full job/matrix verdict summary;
- evidence that no branch push occurred during the active rerun, or any concurrency anomaly that did occur;
- changed-file/product-drift check;
- hard-fence compliance;
- residual uncertainty;
- acceptance matrix;
- 3–10-claim Reviewer Verification Packet with narrow independent checks.

## Successor gate

Even Task-169 PASS requires ChatGPT review.

If accepted, ChatGPT may accept the Task-167 repository repair as fully validated and then open a separate repaired-candidate Windows install-over/provenance/health checkpoint. Task 169 does not authorize installation or semantic Dashboard reacceptance.
