# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-008`  
Updated: 2026-08-22 23:00 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-008-full-windows-v3-process-recovery.md`](tasks/CNX-20260822-008-full-windows-v3-process-recovery.md)

## Predecessor review

[`reviews/CNX-20260822-007-full-windows-v3-process-recovery.md`](reviews/CNX-20260822-007-full-windows-v3-process-recovery.md)

Task 007 is BLOCKED. Its report stopped before CI observation, Windows preflight, confirmation, suite invocation, process kill, lifecycle command, evidence collection, source edit, or package/runtime mutation.

The immutable Task 007 contained valid workflow-fix commit `929fbcc663251941d88f38f09544068a9b3e069d`. The invalid SHA in the Task 007 report was an executor-side transcription/reconstruction error.

## Purpose

Run the full real-Windows v3 Ollama-only process-recovery suite exactly once after literal SHA, source, CI, and read-only health gates. Preserve exact-PID, durable convergence, provider-incident, intentional-stop, evidence-file, and final-state proof.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and every source, duplicate-execution, CI, health, and safety check passes.

Task 008 is the sole new authorization for one disruptive suite invocation and exact lowercase `y` confirmation. Task 007 must not be resumed. This does not authorize a second Task 008 run, manual scenario replay, source edit, package install, `cnx reset`, `cnx uninstall`, release-path install/reinstall, tag, merge, or release.

## Required behavior

1. re-read Task 008 and matching report state;
2. read and compare the exact workflow-fix SHA literally, without reconstruction;
3. verify all required ancestors and the exact harness blob;
4. use a clean isolated worktree;
5. wait for complete green CI for the exact Task 008 start HEAD;
6. perform only the specified read-only Windows preflight;
7. if healthy, invoke the exact full-suite command once and type lowercase `y` once;
8. never rerun the suite or a scenario under any result;
9. hash and parse both TXT/JSON evidence files;
10. record final state read-only;
11. add only the Task 008 report and stop.

## Duplicate-execution fence

If a matching report for `CNX-20260822-008` already exists, do not repeat SHA/source checks, CI observation, preflight, confirmation, PID kills, stop/start, suite execution, evidence collection, or any other side effect. Exit awaiting ChatGPT review.
