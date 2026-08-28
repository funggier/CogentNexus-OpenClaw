# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-111_INTERRUPTED_ROLLOVER_REENTRY_REPAIR`
Task ID: `CNX-20260828-111`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-111-interrupted-rollover-reentry-repair.md`](tasks/CNX-20260828-111-interrupted-rollover-reentry-repair.md)

Task 111 is a **source-only TDD repair** for safe re-entry from the preserved Task-107 interrupted plugin-rollover state.

## Task 110 closure

Task-110 report:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-110-rollover-retired-state-exactness-repair-review.md`

Review commit:

`ad9532fa88dcbc9b23db7abf0e47229794386b17`

Review verdict:

`ACCEPTED PASS — TASK-110 DEFECT REPAIRED; LIVE GATE BLOCKED BY PRE-EXISTING INTERRUPTED-ROLLOVER RE-ENTRY GAP`

Task 110 is closed and accepted for its source-only scope. Candidate `25d229cd496a11af37ea2ff556a0126dfc194377` and artifact `9683127656` remain historical proof only and are not live-authorized because Task 111 changes the required re-entry contract.

## Task-111 target

The last authoritative live machine boundary remains Task 107. Its old external plugin install removed the manifest-owned prior npm generation before ownership rollover failed.

Current installer classification still requires the manifest `pluginPath` artifact to exist, while `recovery-preflight` only auto-recovers incomplete fresh-install transactions. Therefore a new live install-over would currently fail closed during pre-mutation classification.

Task 111 must add a narrowly proven Task-107-shaped interrupted-rollover re-entry path without generic partial-state adoption.

## Required method

Strict TDD:

`reconcile -> TEST-ONLY RED COMMIT -> verify semantic RED -> minimal production fix -> GREEN targeted -> full validation -> exact same-source CI/package proof -> report`

The RED commit must be a separate Git commit before any production edit.

## Hard fence

Task 111 does **not** authorize:

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
- generic adoption of partial/unowned plugin state.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live Windows acceptance task.
