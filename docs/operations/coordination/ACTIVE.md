# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-113_INTERRUPTED_REENTRY_CONFLICTING_WRAPPER_MATRIX_CLOSURE`
Task ID: `CNX-20260828-113`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`](tasks/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md)

Task 113 is a **source-only TDD repair** for the residual interrupted-rollover re-entry ambiguity where an exact active replacement coexists with separate conflicting CogentNexus wrapper evidence.

## Task 112 closure

Task-112 report:

`docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening-review.md`

Review commit:

`ee3f0dca79929ce771add3381d1817766b2ff8f7`

Review verdict:

`REJECTED — RESIDUAL CONFLICTING-WRAPPER RE-ENTRY DEFECT + REQUIRED MATRIX NOT COMMITTED`

Task-112 candidate `023be1a8075c0aa602adda357db9924c170ffb8e` and artifact `9684336683` are historical evidence only and are not live-authorized.

## Confirmed Task-113 defect

Task 112 correctly rejects an active replacement stored inside a foreign/shared wrapper. It still ignores **additional** CogentNexus product-wrapper evidence elsewhere under OpenClaw npm projects if that extra wrapper does not contain a second exact payload.

Independent reviewer reproduction against the exact Task-112 packaged candidate proved:

- valid managed-npm active replacement + separate `npmWrapper:user-shared-wrapper` -> incorrectly accepted re-entry;
- valid canonical direct-extension active replacement + separate `npmWrapper:user-shared-wrapper` -> incorrectly accepted re-entry.

Task 107 recorded the active replacement at the direct canonical extension path, so the direct scenario is production-relevant.

## Required method

Strict TDD:

`reconcile -> TEST-ONLY DIRECT MATRIX COMMIT -> prove direct+managed conflicting-wrapper RED -> minimal product-evidence proof -> GREEN matrix -> full validation -> exact same-source CI/package proof -> report`

The first implementation commit must be tests only and must include the full direct `classify_install(...)` matrix required by Task 113 before production edits.

## Hard fence

Task 113 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- manual cleanup/normalization of Task-107 residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update/reinstall/uninstall/stop/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/secrets access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening wrapper/namespace/manifest/payload/ownership validation.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.
