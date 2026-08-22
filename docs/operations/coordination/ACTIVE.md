# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-013`  
Updated: 2026-08-23 01:44 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`](tasks/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md)

## Predecessor review

[`reviews/CNX-20260823-012-task010-checkout-collision-diagnostic.md`](reviews/CNX-20260823-012-task010-checkout-collision-diagnostic.md)

Task 012 is `ACCEPT` as a metadata diagnostic. It proved that an overlapping watcher invoked a v3 full recovery suite outside the matching Task 010 report. The suite produced the exact TXT/JSON evidence pair and ended `FAIL` at provider durable-`READY` convergence.

This acceptance does not accept Task 010 or any process-recovery scenario. The disruptive suite must not be repeated.

## Purpose

Adjudicate only the already-existing Task 010 TXT/JSON evidence byte-for-byte. Determine exact scenario and step outcomes, exact-PID/no-tree-kill safety, provider incident behavior, provider convergence classification, skipped steps, cleanup effects, and the gate-by-gate evidence boundary.

## Execution authorization

Because `Execution mode` is `AUTO`, the Codex watcher may execute this exact offline evidence-reading task after synchronization and duplicate-fence checks.

Task 013 does not authorize the recovery harness, a scenario, confirmation, live process enumeration, process kill, `cnx`, OpenClaw/Ollama commands, Windows preflight, checkout inspection or cleanup, memory reclaim, install/reset/uninstall/reinstall, or another evidence search.

Task 011 remains deferred and must not execute while RAM remains stable unless explicitly activated later.

## Required behavior

1. re-read Task 013 and matching report state;
2. if the matching report exists, perform no local observation;
3. verify the exact two evidence files by path, byte size, and SHA256;
4. read only those exact evidence files;
5. distinguish executed, failed, skipped, and merely named scenarios;
6. do not repeat or extend any runtime side effect;
7. publish only the matching Task 013 report.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md` already exists, do not read any local evidence, path, process, runtime, checkout, or UI. Exit awaiting ChatGPT review.
