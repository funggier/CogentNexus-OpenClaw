# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `REPOSITORY_TASK167_VERIFICATION_COMPLETION_HERMES`
Current authorization: `CNX-20260831-168_HERMES_TASK167_VERIFICATION_COMPLETION`
Task ID: `CNX-20260831-168`
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

[`tasks/CNX-20260831-168-hermes-task167-verification-completion.md`](tasks/CNX-20260831-168-hermes-task167-verification-completion.md)

Task 168 is the verification/evidence-completion checkpoint for the Task-167 repository repair.

## Task-167 repair under review

Exact product repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Task-167 report:

`reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`

Task-167 ChatGPT review:

`reviews/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair-review.md`

Disposition:

`REWORK_REQUIRED — EVIDENCE_CONTRACT_INCOMPLETE`

The review does not reject the proposed root cause or repair. It requires the executor to complete the mandatory exact-SHA validation, acceptance matrix, risk/crash-window analysis, and Reviewer Verification Packet before ChatGPT can accept the repair.

Pinned OpenClaw remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

## Current gate

Hermes/Codex must validate exact repair SHA `231761fc...` without changing production source by default.

Required evidence includes:

- missing local build/plugin/baseline/package validations;
- final exact-SHA GitHub workflow results;
- changed-file/lineage verification;
- crash-window and duplicate/recovery analysis;
- acceptance matrix;
- 3–10 claim Reviewer Verification Packet.

At the earlier ChatGPT review snapshot:

- PS5.1 Acceptance Smoke `33330458475`: `SUCCESS`;
- Validate `33330458434`: still `IN_PROGRESS`;
- Windows Installer Pack Smoke `33330458470`: still `IN_PROGRESS`.

Task 168 must record their final states from GitHub rather than relying on this snapshot.

## Hard fence

Task 168 is repository verification-only by default.

No Dashboard semantic Send; no other semantic OpenClaw input; no `chat.inject`; no install-over/uninstall/reinstall/reset; no live Gateway/Ollama/Supervisor/OpenClaw mutation; no manual live Ticket/workflow/result/outbox/delivery/database/transcript mutation; no production-source change merely to improve acceptance; no OpenClaw/dependency upgrade; no unrelated repair; no release/promotion; no default/release merge; no force push.

If validation proves the repair needs additional product changes, report `FAIL`/`REWORK_REQUIRED` and stop. ChatGPT must open a separate repair task.

Even Task-168 PASS does not authorize installation or Dashboard semantic testing. ChatGPT review is required first; only an accepted repair may move to a separate Windows install-over/provenance checkpoint.
