# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-010`  
Updated: 2026-08-22 23:30 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-010-full-windows-v3-process-recovery.md`](tasks/CNX-20260822-010-full-windows-v3-process-recovery.md)

## Predecessor review

[`reviews/CNX-20260822-009-clean-windows-source-checkout-validation.md`](reviews/CNX-20260822-009-clean-windows-source-checkout-validation.md)

Task 009 is ACCEPT. It proved a reproducible complete clean full isolated clone at the exact synchronized HEAD with no tracked deletions, the required physical harness and blob, zero parser errors, successful exact `-SyntaxOnly`, and all eight applicable workflows successful. It performed no Windows runtime or lifecycle action.

## Purpose

Run the complete v3 Ollama-only real-Windows process-recovery suite once from a newly created full isolated clone and collect exact evidence for Gateway crash recovery, Ollama crash/provider incident recovery, and intentional `cnx stop`/`cnx start`.

## Execution authorization

Because `Execution mode` is `AUTO`, the Codex watcher may begin this exact task after synchronization and duplicate-fence checks.

Task 010 authorizes exactly one full suite invocation and exact lowercase `y` confirmation once. It requires a newly created complete clean clone, exact source/blob/load gates, complete green CI, healthy read-only preflight, exact-PID-only injection, and full evidence accounting.

Process-tree kill, a second suite/scenario run, manual post-injection transition, install, reset, uninstall, reinstall, source edits, package installation, tag, merge, and release are prohibited.

## Required behavior

1. re-read Task 010 and matching report state;
2. if the report exists, perform no local action;
3. create one new unique full isolated clone at the exact synchronized start HEAD;
4. prove clean status, no deletions, exact harness blob/SHA256/size, parser and `-SyntaxOnly`;
5. require all applicable exact-head CI to complete `success`;
6. require healthy MANAGED/Ollama/`READY` read-only preflight;
7. run the exact disruptive command once and type lowercase `y` once;
8. never rerun the suite or a scenario under any outcome;
9. preserve exact-PID safety and record every PASS, FAIL, BLOCKED, skipped, and not-reached item;
10. add only the matching Task 010 report and stop.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260822-010-full-windows-v3-process-recovery.md` already exists, do not inspect/create a checkout, observe CI/runtime, run preflight, request confirmation, run the suite, kill a process, invoke `cnx stop`/`cnx start`, or perform any other side effect. Exit awaiting ChatGPT review.
