# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-007`  
Updated: 2026-08-22 22:52 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-007-full-windows-v3-process-recovery.md`](tasks/CNX-20260822-007-full-windows-v3-process-recovery.md)

## Predecessor review

[`reviews/CNX-20260822-006-v3-validation-only.md`](reviews/CNX-20260822-006-v3-validation-only.md)

Task 006 is ACCEPTED. Sixteen direct tests passed, parser/`-SyntaxOnly` and the corrected convergence contract passed, and all eight applicable workflows for validation start HEAD `ef1f89eaf51749b741e0c14c32b1dc2e4248e456` completed successfully.

## Purpose

Run the full real-Windows v3 Ollama-only process-recovery suite exactly once after source, CI, and read-only health gates. Preserve exact PID, durable convergence, provider incident, intentional-stop, evidence-file, and final-state proof.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and all source, duplicate-execution, CI, health, and safety checks.

This task authorizes one disruptive suite invocation and exact lowercase `y` confirmation. It does not authorize any second run, manual scenario replay, source edit, package install, `cnx reset`, `cnx uninstall`, release-path install/reinstall, tag, merge, or release.

## Required behavior

1. re-read Task 007 and matching report state;
2. verify required ancestors and harness blob;
3. use a clean isolated worktree;
4. wait for complete green CI for the exact task start HEAD;
5. perform only the specified read-only Windows preflight;
6. if healthy, invoke the exact full-suite command once and type lowercase `y` once;
7. never rerun the suite or a scenario under any result;
8. hash and parse both TXT/JSON evidence files;
9. record final state read-only;
10. add only the Task 007 report and stop.

## Duplicate-execution fence

If a matching report for `CNX-20260822-007` already exists, do not repeat preflight, confirmation, PID kills, stop/start, suite execution, evidence collection, CI observation, or any other side effect. Exit awaiting ChatGPT review.
