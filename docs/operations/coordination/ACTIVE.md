# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TEST_MATRIX_GATE`
Current authorization: `CNX-20260828-114_INTERRUPTED_REENTRY_DIRECT_MATRIX_VALIDATION`
Task ID: `CNX-20260828-114`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md`](tasks/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md)

Task 114 is a **validation-first test-matrix gate** for the interrupted-rollover re-entry shortcut.

## Task 113 closure

Task-113 report:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure-review.md`

Review verdict:

`SOURCE REPAIR ACCEPTED; TASK COMPLETION BLOCKED — REQUIRED DIRECT CLASSIFY_INSTALL MATRIX INCOMPLETE`

Task-113 source candidate `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06` is accepted as source-repair evidence: its direct/managed conflicting-wrapper RED was real, its production fix was separate and narrow, all exact CI workflows passed, and artifact `9685376213` was independently verified.

It is not yet live-authorized because the Task-113 test-only commit did not contain the complete direct `classify_install(...)` matrix that the task explicitly required before production editing.

## Task-114 method

Task 114 must first commit the complete direct matrix as tests only.

- If the entire matrix is GREEN on current production, do not edit production source.
- If a matrix case exposes a real defect, preserve that tests-only commit as RED evidence and only then make a separate minimal production repair.
- Never manufacture retroactive RED provenance.

After matrix/targeted/full validation, require exact same-source Validate, Windows Installer Pack Smoke, PS5.1 Acceptance Smoke, and a new package-proof artifact before publishing the Task-114 report.

## Preserved live boundary

No task after Task 107 has authorized live machine mutation. Task 107 remains the last authoritative live evidence. Any later Windows acceptance must first re-prove the current machine state read-only rather than assume historical residue still exists.

## Hard fence

Task 114 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- Task-107 replay or manual normalization;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update/reinstall/uninstall/stop/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/secrets access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace/wrapper/manifest/payload/ownership/product-evidence verification.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md`

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.
