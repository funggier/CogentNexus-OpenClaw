# CNX-20260823-020 — Isolated Adjudication and Exact Task 017 Worktree Removal

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: unblock offline provider diagnosis  
Predecessor: `CNX-20260823-019` (`ACCEPT` of safe blocked report)  
Execution mode: `AUTO`

## Objective

Use one exact watcher-compatible control worktree to adjudicate the three tracked deletions in the wrong-head Task 017 worktree. If and only if every preservation and no-use gate passes, restore only those paths from the target's own HEAD and remove only that exact target using normal non-force Git removal.

## Exact paths

Control worktree (may be created once):

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-020`

Cleanup target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-017`

Required target HEAD:

`78f6cba4748e59d5975940ca9854961d0e7ff550`

Allowed deleted paths:

1. `docs/operations/coordination/reports/CNX-20260822-009-clean-windows-source-checkout-validation.md`
2. `docs/operations/coordination/reports/CNX-20260823-012-task010-checkout-collision-diagnostic.md`
3. `docs/operations/coordination/reports/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`

## Duplicate and collision fence

Before any creation or target inspection:

1. fetch `origin agent/v0.9.3-recovery-reality-tests`;
2. verify remote `ACTIVE.md` names Task 020 with `READY_FOR_CODEX` and `AUTO`;
3. verify the matching Task 020 report is absent;
4. verify the exact control path is absent from the filesystem and worktree registry;
5. if the report or control path/registration exists, perform no fallback, suffix, cleanup, or target inspection; report the exact blocker.

Create the control worktree only at the exact path from the fetched remote branch head. Verify its HEAD equals the fetched head before continuing. No alternate path, clone, suffix, or second control worktree is authorized.

## Target preservation gates

All must pass and exact commands/values/exit codes must be recorded:

- target path and exact registration exist;
- target HEAD equals the required HEAD;
- target status contains exactly the three named tracked deletions and nothing else, including no untracked or ignored files;
- no Git operation or lock is active;
- no target commit is unreachable from source repository refs;
- each deleted path exists at `HEAD:<path>`; record Git blob ID and SHA256;
- a durable coordination-branch/history copy exists for each path; record identity;
- restoration would not overwrite an existing filesystem file;
- no process has current directory, executable, or command line bound to the exact target;
- distinguish the outside inspection shell carrying the path as an argument from actual target use.

Any failed or ambiguous gate requires `BLOCKED` with no restore/removal.

## Authorized action

Only after all gates pass:

1. restore the three exact paths from target HEAD using pathspec-safe Git restore;
2. verify restored SHA256 values;
3. verify the entire target is clean with no ignored/untracked content or Git operation;
4. remove only the exact Task 017 target using normal non-force `git worktree remove`;
5. verify target path and registration are absent;
6. publish the matching report;
7. after successful publication only, remove the Task 020 control worktree using normal non-force removal if it is clean and not in use; otherwise leave it and record the blocker.

## Result classification

Return exactly one primary result:

- `PASS_RESTORED_AND_REMOVED_EXACT_TARGET`
- `BLOCKED_CONTROL_COLLISION`
- `BLOCKED_CONTROL_HEAD_MISMATCH`
- `BLOCKED_DELETION_SET_MISMATCH`
- `BLOCKED_BLOB_NOT_DURABLE`
- `BLOCKED_UNPUBLISHED_COMMIT`
- `BLOCKED_TARGET_IN_USE`
- `BLOCKED_TARGET_OPERATION_ACTIVE`
- `BLOCKED_RESTORE_FAILED`
- `BLOCKED_REMOVAL_FAILED`
- `BLOCKED_PUBLICATION_FAILED`

Report exact before/after state, hashes, commands, exit codes, side effects, control cleanup result, and `Human decision required: YES|NO`.

## Prohibited actions

No force, reset, clean, recursive deletion, broad checkout, broad prune, metadata edit, fallback path, process kill/close/restart/suspend, runtime/recovery/`cnx`/OpenClaw/Ollama action, install/reset/uninstall/reinstall, provider diagnosis, source change, merge, tag, release, or force-push.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-020-isolated-adjudication-and-task017-removal.md`

Commit message begins `report: CNX-20260823-020`. Re-fetch and re-check the report fence before push. Never force-push. Stop after publication/control cleanup accounting.
