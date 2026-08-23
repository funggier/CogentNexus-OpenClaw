# CNX-20260823-030 — Restore Task 027 Working-Tree Materialization

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-029` (`ACCEPT`)

## Objective

Restore only the exact tracked paths currently absent from the registered Task 027 working tree, using the Task 027 control's own verified HEAD and a NUL-delimited exact pathspec.

Do not remove, recreate, re-register, switch, reset, clean, or broadly restore the worktree. Do not resume Task 025 in this task.

## Exact identities

Primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

Repair target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required target HEAD:

`748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Required coordination ancestor:

`af53fb3d19d6245552699795c638e159edc83204`

Expected pre-repair deleted-path count:

`382`

Expected SHA256 of the Task 029 full porcelain-v2 capture:

`23C7BA8F5B2DED772AFB5B34891A3573A0C5909866EDD9E1566840DC16F97F40`

Expected SHA256 of the Task 029 absent-path capture:

`6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Matching report:

`docs/operations/coordination/reports/CNX-20260823-030-restore-task027-materialization.md`

## Execution model

Run control and publication commands from the primary repository or another already-existing verified complete publisher checkout.

A Task 030 watcher worktree is neither required nor authorized. Its presence, absence, registration, or dirtiness must not be used as a substitute target.

## Duplicate-execution fence

After fresh fetch, if the matching Task 030 report already exists, do nothing and stop awaiting review.

If the Task 027 target is already fully materialized and clean, do not repeat restoration. Record `PASS_ALREADY_RESTORED` only after all post-repair verification gates below pass.

## Mandatory pre-mutation gates

Before any restoration:

1. fetch the exact coordination branch;
2. verify the required coordination ancestor;
3. read ACTIVE, Task 030, Task 029 report, and Task 029 review from fetched HEAD;
4. verify the matching Task 030 report is absent;
5. verify exact Task 027 path registration, common-dir identity, detached state, and exact HEAD;
6. verify no merge, rebase, cherry-pick, revert, bisect, index lock, or process actively using Task 027 for a Git mutation;
7. capture `git status --porcelain=v2 --untracked-files=all`;
8. require no staged modification, no unstaged non-deletion modification, and no untracked paths;
9. derive the absent tracked paths using a NUL-safe Git command from the exact target;
10. require exactly 382 paths;
11. persist the exact NUL-delimited pathspec outside the target working tree in a task-specific temporary location;
12. produce a canonical evidence representation and require its SHA256 to match the accepted Task 029 absent-path evidence, or stop `BLOCKED_PRESTATE_DRIFT`;
13. verify every selected path exists in target HEAD and index with matching blob identity and normal flags;
14. verify every selected filesystem path is absent;
15. verify the target has no unique content that restoration could overwrite.

If any precondition differs, do not restore and report the narrowest blocker.

## Authorized repair

The only authorized target mutation is equivalent to:

`git -C <Task027> restore --source=HEAD --worktree --pathspec-from-file=<exact-nul-file> --pathspec-file-nul`

The pathspec must be generated from the verified absent tracked set. Do not use a directory, wildcard, dot pathspec, broad checkout, or manually shortened path list.

Capture command, exit code, and stderr/stdout.

## Mandatory post-repair verification

Require all of the following:

- Task 027 remains registered at the exact path, exact detached HEAD, and expected common repository;
- `git status --porcelain=v2 --untracked-files=all` is empty;
- tracked index count remains 387;
- physically materialized tracked count is 387;
- absent tracked count is 0;
- no staged entries, untracked files, or unexpected new files exist;
- representative paths cited in Task 029 exist and hash to their verified HEAD blobs;
- no configuration, ref, index content, branch, or worktree-registration change occurred;
- no path outside Task 027 was changed by the restoration;
- retain before/after counts and SHA256 evidence.

Do not remove Task 027 after repair. Task 025 reconciliation requires a separate reviewed task.

## Report publication fence

The only authorized primary-repository mutation is the matching report.

1. use a verified complete publisher checkout;
2. write and stage only the matching report path;
3. prohibit `git add .`, `git add -A`, `git commit -a`, reset, clean, checkout, and broad restore;
4. require cached diff to contain exactly one `A` or `M` entry for the report and zero deletions/other paths;
5. after commit, verify the commit changes exactly the report path;
6. push without force and verify remote report presence.

Commit begins `report: CNX-20260823-030`.

## Results

Return exactly one:

- `PASS_RESTORED_COMPLETE_CLEAN`
- `PASS_ALREADY_RESTORED`
- `BLOCKED_PRESTATE_DRIFT`
- `BLOCKED_UNIQUE_CONTENT`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_REPAIR_FAILED`
- `BLOCKED_POSTVERIFY_FAILED`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Prohibited

No worktree create/remove/re-register/prune, reset, clean, checkout, broad restore, index mutation, configuration/ref/branch mutation, force push, deletion, Task 025 execution, provider diagnosis, process kill/action, runtime/recovery/provider/`cnx`/OpenClaw/Ollama action, lifecycle action, merge, tag, or release.
