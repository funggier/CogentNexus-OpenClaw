# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-014`  
Updated: 2026-08-23 02:28 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-014-complete-task010-evidence-fields.md`](tasks/CNX-20260823-014-complete-task010-evidence-fields.md)

## Predecessor review

[`reviews/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`](reviews/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md)

Task 013 is `REWORK`. It verified the exact TXT/JSON identities and produced a plausible partial adjudication, but omitted mandatory exact provenance, per-step timestamps, listener endpoints, kill exit statuses, and provider incident transition details.

No recovery gate is newly accepted from Task 013. The existing suite must not be repeated.

## Purpose

Read only the same two immutable evidence files and publish every missing required field as an exact value or `NOT_RECORDED`. Correct the gate adjudication so no gate is marked proven without its required safety and outcome evidence.

## Execution authorization

Because `Execution mode` is `AUTO`, the Codex watcher may execute this exact offline evidence-completion task after synchronization and duplicate-fence checks.

Task 014 does not authorize the recovery harness, scenario, confirmation, live process/runtime inspection, checkout operation, memory reclaim, install/reset/uninstall/reinstall, or any state-changing action.

Task 011 remains deferred while RAM remains stable.

## Required behavior

1. re-read Task 014 and matching report state;
2. if the matching report exists, perform no local observation;
3. verify both exact evidence identities;
4. use bounded focused extraction only;
5. report exact values or `NOT_RECORDED` for every required field;
6. do not repeat or extend any runtime side effect;
7. publish only the matching Task 014 report.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-014-complete-task010-evidence-fields.md` already exists, do not read any local evidence, path, process, runtime, checkout, or UI. Exit awaiting ChatGPT review.
