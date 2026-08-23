# CNX-20260823-019 — Adjudicate Three Deletions and Remove Exact Task 017 Worktree

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: unblock offline provider diagnosis  
Predecessor: `CNX-20260823-018` (`ACCEPT` of safe `BLOCKED_TARGET_DIRTY`)  
Execution mode: `AUTO`

## Objective

Determine whether the three tracked deletions in the exact wrong-head Task 017 worktree can be restored without losing unpublished work. If and only if every preservation and no-use gate passes, restore exactly those paths from the worktree's own HEAD and remove only that exact worktree using normal non-force Git removal.

This task is cleanup only. Do not create a worktree or perform provider diagnosis.

## Exact target and allowed files

Target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-017`

Required target HEAD:

`78f6cba4748e59d5975940ca9854961d0e7ff550`

Only these deleted paths may be adjudicated or restored:

1. `docs/operations/coordination/reports/CNX-20260822-009-clean-windows-source-checkout-validation.md`
2. `docs/operations/coordination/reports/CNX-20260823-012-task010-checkout-collision-diagnostic.md`
3. `docs/operations/coordination/reports/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`

No other target content may be changed.

## Duplicate-execution fence

Before target inspection:

1. fetch `origin agent/v0.9.3-recovery-reality-tests`;
2. confirm remote `ACTIVE.md` names Task 019 with `READY_FOR_CODEX` and `AUTO`;
3. confirm the matching Task 019 report is absent;
4. if present, do nothing and stop awaiting ChatGPT review.

## Preservation gates

Record commands, exact values, and exit codes. All must pass:

- target path exists and exact registration exists;
- target HEAD equals the required wrong HEAD;
- status contains exactly the three named tracked deletions and nothing else, including no untracked/ignored files;
- no lock, merge, rebase, cherry-pick, bisect, revert, sequencer, index lock, or other Git operation exists;
- no local commit exists in the target that is unreachable from the source repository's refs;
- for each deleted path, the blob at target `HEAD:<path>` exists and its SHA256 is recorded;
- for each path, a durable copy is present in the coordination branch history or current branch and its content identity is recorded;
- restoring from target HEAD would recreate only the tracked blob and would not overwrite a present filesystem file;
- path-filtered process inspection finds no process whose current directory, executable, or command line is bound to the exact target;
- do not treat the task's own inspection shell, if launched outside the target and merely containing the path as an argument, as proof of target use; record this distinction exactly.

If any gate fails or any intent remains ambiguous, publish `BLOCKED` without restoring or removing.

## Authorized action

Only if every gate passes:

1. restore the three exact paths from the target's own HEAD using pathspec-safe Git restore;
2. verify each restored file hash matches its recorded target-HEAD blob content;
3. verify the entire target is clean, with no untracked or ignored content and no active Git operation;
4. run normal non-force `git worktree remove` for the exact target;
5. verify the filesystem path and exact registration are absent;
6. publish the report.

Do not use `--force`, reset, clean, recursive deletion, broad checkout, manual Git metadata edits, or broad prune.

## Result classification

Return exactly one:

- `PASS_RESTORED_AND_REMOVED_EXACT_TARGET`
- `BLOCKED_DELETION_SET_MISMATCH`
- `BLOCKED_BLOB_NOT_DURABLE`
- `BLOCKED_UNPUBLISHED_COMMIT`
- `BLOCKED_TARGET_IN_USE`
- `BLOCKED_TARGET_OPERATION_ACTIVE`
- `BLOCKED_RESTORE_FAILED`
- `BLOCKED_REMOVAL_FAILED`
- `BLOCKED_PUBLICATION_FAILED`

Report before/after state, hashes, commands, exit codes, exact files changed, exact path removed or preserved, side effects, and `Human decision required: YES|NO`.

## Prohibited actions

- no new worktree/clone/fallback/suffix;
- no other worktree or path inspection/cleanup;
- no process kill/close/restart/suspend/tree action;
- no runtime, recovery, `cnx`, OpenClaw, Ollama, listener/service, install, reset, uninstall, reinstall, package, source/evidence, merge, tag, release, or force-push action;
- no chat, Project, session, cache, or unrelated user-data access.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md`

Commit message must begin `report: CNX-20260823-019`.

Before push, fetch the coordination branch and re-check the matching-report fence. Never force-push. Stop after publication.
