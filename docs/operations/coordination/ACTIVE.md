# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-112_INTERRUPTED_REENTRY_OWNERSHIP_PROOF_HARDENING`
Task ID: `CNX-20260828-112`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`](tasks/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md)

Task 112 is a **source-only TDD repair** for the residual ownership-boundary defect in Task-111 interrupted-rollover re-entry.

## Task 111 closure

Task-111 report:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-111-interrupted-rollover-reentry-repair-review.md`

Review verdict:

`REJECTED — RESIDUAL RE-ENTRY OWNERSHIP-PROOF DEFECT + INCOMPLETE NEGATIVE CONTRACT COVERAGE`

Task-111 candidate `f4c8c993be80eaf54468f5b2630fd107050a1385` and artifact `9683680142` are historical evidence only and are not live-authorized.

## Confirmed Task-112 defect

Task 111 correctly recognizes the Task-107-shaped state where the old manifest-owned plugin path is missing and one exact replacement is active. However, for active replacements under OpenClaw `npm/projects`, the shortcut proves only the child payload/registration and candidate count. It does not invoke the existing strict npm wrapper ownership proof.

An exact CogentNexus child payload inside a foreign/shared wrapper can therefore satisfy the shortcut even when unrelated user dependency evidence exists in the wrapper.

Task 112 must prove the replacement storage boundary before returning `interruptedRolloverReentry=True`.

## Required method

Strict TDD:

`reconcile -> TEST-ONLY RED COMMIT -> prove foreign/shared-wrapper acceptance defect -> minimal production repair -> GREEN negative matrix -> full validation -> exact same-source CI/package proof -> report`

The RED commit must be separate and test-only before production edits.

## Hard fence

Task 112 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- manual cleanup/normalization of Task-107 residue;
- Dashboard semantic Send;
- OpenClaw/Ollama update/reinstall/uninstall/stop/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/secrets access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening wrapper/namespace/ownership validation.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live Windows acceptance task.
