# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_DIAGNOSTIC_INSTALL_OVER_RETRY`
Current authorization: `CNX-20260830-159_WINDOWS_DIAGNOSTIC_INSTALL_OVER_RETRY`
Task ID: `CNX-20260830-159`
Updated: 2026-08-30 ICT
Owner / coordinator / reviewer: ChatGPT
Executor: Hermes on the operator's real Windows/OpenClaw environment

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-159-windows-diagnostic-install-over-retry.md`](tasks/CNX-20260830-159-windows-diagnostic-install-over-retry.md)

Task 158 is durably reviewed **ACCEPT** at:

`docs/operations/coordination/reviews/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis-review.md`

Accepted installer observability production repair:

`2e8ff49da2573d87236fa7a004bc156d8c94b880`

Task-159 creation commit:

`758ea7ab0fd7f782ed14e86450453171bcd22ace`

## Task-159 execution contract

Hermes must:

1. recover and inspect the complete Task-157 raw `install-over.txt` before any new mutation if the file still exists;
2. publish/hash that original raw log as durable evidence when available;
3. stop before retry if the old raw log proves a concrete defect that makes unchanged retry unsafe;
4. prove exact candidate/source/package provenance including accepted production repair `2e8ff49...` and no later unreviewed production delta;
5. launch exactly one install-over process through the established workflow;
6. preserve one unique installer PID across executor calls and never treat an orchestration timeout as permission to relaunch;
7. durably capture raw stdout/stderr plus all `CNXCLAW_INSTALL_STAGE_START` / `CNXCLAW_INSTALL_STAGE_COMPLETE` records;
8. observe the same process until exit or proven termination;
9. if successful, prove installed identity/provenance plus lifecycle/loader/non-semantic command health;
10. publish Task-159 report/evidence and STOP for ChatGPT review.

## Required durable report

`docs/operations/coordination/reports/CNX-20260830-159-windows-diagnostic-install-over-retry.md`

Expected raw evidence paths when available/reasonably sized:

- `docs/operations/coordination/reports/CNX-20260830-159-task157-original-install-over-log.txt`
- `docs/operations/coordination/reports/CNX-20260830-159-diagnostic-install-over-log.txt`

## Hard fence

No Dashboard semantic Send or semantic Dashboard interaction; no new semantic message; no manual Ticket/workflow/outbox/delivery/DB mutation; no reset; no clean uninstall; no fresh reinstall after uninstall; no arbitrary live-state deletion; no manual source patch; no dependency upgrade; no OpenClaw source patch; no `--force` redesign; no retry/timeout/rollback/kill behavior redesign; no merge/tag/release/publish/promotion; no force push.

After report/evidence publication Hermes must STOP. Even a Task-159 PASS does not authorize Dashboard semantic reacceptance.