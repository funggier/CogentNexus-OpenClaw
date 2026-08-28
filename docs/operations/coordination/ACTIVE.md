# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-110_ROLLOVER_RETIRED_STATE_EXACTNESS_REPAIR`
Task ID: `CNX-20260828-110`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-110-rollover-retired-state-exactness-repair.md`](tasks/CNX-20260828-110-rollover-retired-state-exactness-repair.md)

Task 110 is a **source-only TDD repair** for the remaining fail-closed case where the retired project path still exists after external mutation but is no longer the exact pre-mutation owned generation.

## Task 109 closure

Task 109 report:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-109-rollover-finalize-failclosed-repair-review.md`

Review verdict:

`REJECTED — TDD PROVENANCE FAILURE + RESIDUAL RETIRED-STATE EXACTNESS DEFECT`

Task 109 is closed. Candidate `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce` and artifact `9681526010` are evidence only and are not authorized for live acceptance.

## Required Task-110 invariant

After external mutation and failed final ownership verification:

- normal ownership may return to `manifestBefore` only if the retired state is still **exactly** the transaction-proven pre-mutation generation;
- path existence alone is insufficient;
- an existing-but-altered/incomplete retired project must remain quarantined/fail-closed;
- replacement ownership must not be declared successful without final proof;
- backup/transaction evidence must remain durable.

## Required execution method

Strict TDD:

`reconcile -> TEST-ONLY RED COMMIT -> verify semantic RED -> minimal production commit -> GREEN targeted -> full validation -> exact same-source CI/package proof -> report`

The RED commit must be a separate GitHub commit before any Task-110 production edit.

## Hard fence

Task 110 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- manual live cleanup/normalization;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update/reinstall/uninstall/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/secrets access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership verification.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

The report must contain the separate RED commit SHA/evidence, minimal production fix commit, GREEN/full validation, exact candidate, exact workflow run IDs, and new package-proof identity/hashes. After report publication, stop for independent ChatGPT review. Do not create a live acceptance task.
