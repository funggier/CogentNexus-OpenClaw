# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-009`  
Updated: 2026-08-22 23:08 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-009-clean-windows-source-checkout-validation.md`](tasks/CNX-20260822-009-clean-windows-source-checkout-validation.md)

## Predecessor review

[`reviews/CNX-20260822-008-full-windows-v3-process-recovery.md`](reviews/CNX-20260822-008-full-windows-v3-process-recovery.md)

Task 008 is BLOCKED. Source, literal SHA, harness blob, CI, and read-only Windows health passed, but its isolated checkout lacked the physical harness and contained tracked deletion residue. The single command attempt exited before loading the script. No scenario, process kill, lifecycle command, or runtime mutation occurred.

## Purpose

Diagnose the unusable Task 008 checkout and prove a reproducible complete, clean isolated Windows source checkout containing the exact v3 harness.

## Execution authorization

Because `Execution mode` is `AUTO`, the Codex watcher may begin this exact non-disruptive task after synchronization and duplicate-fence checks.

Task 009 authorizes only read-only diagnosis of the failed Task 008 checkout and creation/validation of one new unique full isolated clone. It does not authorize Windows runtime preflight, confirmation input, the disruptive harness, process kill, `cnx start`/`stop`, reset, uninstall, install, reinstall, source edits, tag, merge, or release.

## Required behavior

1. re-read Task 009 and matching report state;
2. inspect the old Task 008 checkout read-only without repairing or deleting it;
3. fetch the branch and verify exact ancestors;
4. create one unique full isolated clone at the exact Task 009 start HEAD;
5. prove clean status, no tracked deletions, exact harness path/blob, parser and `-SyntaxOnly` success;
6. verify applicable CI for the exact start HEAD;
7. add only the Task 009 report and stop.

## Duplicate-execution fence

If a matching report for `CNX-20260822-009` already exists, do not inspect the old checkout, create a clone/worktree, run parser/`-SyntaxOnly`, observe CI, or perform any other side effect. Exit awaiting ChatGPT review.
