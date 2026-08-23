# CNX-20260823-021 — Remove Exact Stale Task 020 Control Worktree

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-020` (`ACCEPT` safe blocked)

## Objective

Safely remove only the stale Task 020 control worktree. Do not inspect or modify the Task 017 cleanup target in this task.

## Exact paths and identity

Execution control path:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-021`

Removal target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-020`

Required removal-target HEAD:

`1718ea450c546abb55ad2892745f19f6e840ee5c`

## Duplicate and execution-control fence

1. Fetch the coordination branch and verify Task 021 is remote `READY_FOR_CODEX` / `AUTO`.
2. Verify the matching report is absent.
3. The exact Task 021 control path may be:
   - absent, in which case create it once from the fetched remote head; or
   - already created by the watcher, in which case adopt it only if it is the exact registered path, detached at the fetched remote head, completely clean, has no untracked/ignored content or Git operation, and contains no unpublished commit.
4. Any mismatch is `BLOCKED_CONTROL_COLLISION`. No fallback, suffix, alternate path, clone, cleanup, or second control is allowed.

## Removal-target gates

All must pass:

- exact target path and registration exist;
- target HEAD equals the required HEAD;
- target is completely clean, including no untracked or ignored files;
- no Git operation/lock exists;
- no target commit is unreachable from source repository refs;
- no process has current directory, executable, or command line bound to the exact target;
- distinguish an outside inspection shell carrying the path as an argument from actual target use.

If any gate fails or is ambiguous, report `BLOCKED` and preserve the target.

## Authorized action

Only after every gate passes:

1. remove the exact Task 020 target using normal non-force `git worktree remove`;
2. verify exact path and registration are absent;
3. publish the report;
4. after successful publication, remove the exact Task 021 control worktree using normal non-force removal if it is clean and not in use; otherwise preserve it and account for the blocker.

## Results

Return exactly one primary result:

- `PASS_REMOVED_EXACT_TASK020_CONTROL`
- `BLOCKED_CONTROL_COLLISION`
- `BLOCKED_TARGET_IDENTITY`
- `BLOCKED_TARGET_DIRTY`
- `BLOCKED_TARGET_OPERATION_ACTIVE`
- `BLOCKED_UNPUBLISHED_COMMIT`
- `BLOCKED_TARGET_IN_USE`
- `BLOCKED_REMOVAL_FAILED`
- `BLOCKED_PUBLICATION_FAILED`

Record commands, exit codes, before/after state, exact side effects, control cleanup result, and `Human decision required: YES|NO`.

## Prohibited

No Task 017 inspection, restore, provider diagnosis, force, reset, clean, recursive delete, broad prune, metadata edit, fallback path, process action, runtime/recovery/`cnx`/OpenClaw/Ollama action, install/reset/uninstall/reinstall, source change, merge, tag, release, or force-push.

## Report

`docs/operations/coordination/reports/CNX-20260823-021-remove-stale-task020-control.md`

Commit begins `report: CNX-20260823-021`. Re-fetch and re-check the report fence before push. Stop after publication and control-cleanup accounting.
