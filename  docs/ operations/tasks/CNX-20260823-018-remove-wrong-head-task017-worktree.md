# CNX-20260823-018 — Remove the Wrong-Head Task 017 Worktree Safely

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: unblock offline provider diagnosis  
Predecessor: `CNX-20260823-017` (`ACCEPT` of safe `BLOCKED` report)  
Execution mode: `AUTO`

## Objective

Verify and safely remove only the exact Task 017 worktree that was created at the wrong HEAD because an unset ref variable was used.

This task is cleanup only. Do not recreate a worktree and do not perform provider diagnosis.

## Exact target

Authorized path:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-017`

Expected recorded wrong HEAD:

`78f6cba4748e59d5975940ca9854961d0e7ff550`

Expected intended Task 017 remote HEAD, for comparison only:

`eb4cefefb2a9859d28dd1d45fb50096835674ec0`

## Duplicate-execution fence

Before any target inspection:

1. fetch `origin agent/v0.9.3-recovery-reality-tests`;
2. confirm remote `ACTIVE.md` names `CNX-20260823-018` with `READY_FOR_CODEX` and `AUTO`;
3. check for `docs/operations/coordination/reports/CNX-20260823-018-remove-wrong-head-task017-worktree.md`;
4. if that report exists, do nothing and stop awaiting ChatGPT review.

## Required pre-removal gates

Read only the exact target and its registration. Record commands and exit codes.

All gates must pass:

- the exact path exists;
- Git registers that exact path as a worktree;
- its HEAD is exactly `78f6cba4748e59d5975940ca9854961d0e7ff550`;
- it has no tracked modification, staged change, untracked file, ignored task output, lock, rebase, merge, cherry-pick, or other Git operation;
- it contains no matching Task 018 report or unpublished commit;
- no process has current directory, executable, or command line bound to the exact target path;
- removal can use normal non-force `git worktree remove <exact-path>`.

If any gate is false or cannot be proven, publish `BLOCKED`. Do not remove, repair, reset, clean, prune broadly, kill a process, close an app, or alter the target.

Process inspection must be path-filtered to the exact target. Record only PID, process name, and the matching path relationship needed for the gate. Do not inventory unrelated processes or sessions.

## Authorized action

If and only if every gate passes:

1. run normal non-force `git worktree remove` for the exact target;
2. verify the filesystem path is absent;
3. verify the exact path is absent from `git worktree list --porcelain`;
4. if only that exact registration remains stale, prune that exact stale registration using the narrowest Git-supported method; do not run broad cleanup against other paths;
5. publish the matching report.

Do not use `--force`, recursive deletion, `git clean`, reset, checkout repair, manual `.git/worktrees` editing, or an alternate removal method.

## Prohibited actions

- no new worktree, clone, nested checkout, fallback path, or suffix;
- no inspection, modification, removal, prune, repair, or reuse of Task 007–016 paths other than the exact Task 017 target;
- no source/evidence diagnosis or modification;
- no recovery harness, Windows runtime command, `cnx`, OpenClaw, Ollama, listener/service action, process kill, restart, suspend, or process-tree operation;
- no install, reset, uninstall, reinstall, package change, merge, tag, release, or force-push;
- no chat, Project, session, cache, or unrelated user-data access.

## Result classification

Return exactly one:

- `PASS_REMOVED_EXACT_TARGET`
- `BLOCKED_TARGET_IDENTITY_MISMATCH`
- `BLOCKED_TARGET_DIRTY`
- `BLOCKED_TARGET_IN_USE`
- `BLOCKED_TARGET_OPERATION_ACTIVE`
- `BLOCKED_REMOVAL_FAILED`
- `BLOCKED_PUBLICATION_FAILED`

Include exact pre/post state, commands, exit codes, side-effect accounting, and whether a human decision is required.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-018-remove-wrong-head-task017-worktree.md`

Commit message must begin:

`report: CNX-20260823-018`

Before push, fetch the coordination branch and verify no matching Task 018 report exists. Never force-push. Stop after publishing the report.
