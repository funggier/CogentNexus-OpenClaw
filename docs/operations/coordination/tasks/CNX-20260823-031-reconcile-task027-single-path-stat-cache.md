# CNX-20260823-031 — Reconcile Task 027 Single-Path Stat Cache

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-030` (`BLOCKED`)

## Objective

Diagnose and, only when the immutable content gates prove it safe, reconcile the Git filesystem/index stat-cache anomaly for exactly one Task 027 path so the already-restored worktree can demonstrate a clean status.

Do not repeat the 382-path restoration. Do not resume Task 025 in this task.

## Exact identities

Primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

Target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached target HEAD:

`748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Exact anomalous path:

`docs/operations/coordination/reports/CNX-20260823-027-reconcile-task025-tree-index-worktree.md`

Required HEAD/index/filesystem blob:

`d81361b07c42ff612f4f0ab7657cf4e6b9164944`

Matching report:

`docs/operations/coordination/reports/CNX-20260823-031-reconcile-task027-single-path-stat-cache.md`

## Duplicate-execution fence

After a fresh fetch, if the matching Task 031 report exists, do nothing and stop awaiting review.

If Task 027 already has an empty porcelain-v2 status and all verification gates below pass, make no mutation and report `PASS_ALREADY_CLEAN`.

## Mandatory pre-mutation gates

1. Read ACTIVE, Task 031, Task 030 report, and Task 030 review from freshly fetched HEAD.
2. Verify exact target registration, detached HEAD, common-dir identity, and absence of active Git operations or index lock.
3. Verify 387 indexed paths, 387 materialized tracked paths, and zero absent tracked paths.
4. Capture porcelain-v2 status, `git diff-files --raw`, `git diff -- <exact-path>`, `git ls-files --stage --debug -- <exact-path>`, filesystem metadata, and HEAD/index/filesystem hashes.
5. Require no staged entry, no untracked path, no content diff, and no status anomaly outside the exact path.
6. Require HEAD, index, and filesystem blob for the exact path all equal the required blob.
7. Preserve before-state hashes for the target index file, exact file bytes, primary repository status, refs/config, and worktree registration.

If any content/blob identity differs, any other path is dirty, or target identity changed, stop without mutation.

## Authorized narrow reconciliation

Only after every pre-mutation gate passes, one exact-path index stat refresh is authorized:

`git -C <Task027> update-index --refresh -- <exact-path>`

If normal refresh does not clear the anomaly while all three blobs remain identical, one exact-path `--really-refresh` attempt is authorized:

`git -C <Task027> update-index --really-refresh -- <exact-path>`

These commands may update index stat metadata only. They must not change the path's blob identity, stage content, rewrite file bytes, or touch another path.

No `git add`, restore, checkout, reset, clean, touch/write, broad refresh, or timestamp manipulation is authorized.

## Mandatory post-verification

Require all of the following:

- empty `git status --porcelain=v2 --untracked-files=all`;
- empty `git diff-files --raw`;
- empty staged diff;
- 387 indexed and 387 materialized tracked paths, zero absent paths;
- exact path HEAD/index/filesystem blob remains the required blob;
- exact file byte hash is unchanged;
- index tree entries/blob identities are unchanged; only stat-cache metadata may differ;
- target identity, refs, config, worktree registration, and primary repository status are unchanged;
- no path outside the exact target path was mutated.

If status remains anomalous, report the diagnostic evidence without attempting another repair.

## Report publication fence

The only authorized primary-repository content mutation is the matching report. Stage and commit only that exact report path. Prohibit `git add .`, `git add -A`, `git commit -a`, force push, and any deletion. Verify the report commit changes exactly one path.

Commit begins `report: CNX-20260823-031`.

## Results

Return exactly one:

- `PASS_RECONCILED_CLEAN`
- `PASS_ALREADY_CLEAN`
- `BLOCKED_CONTENT_IDENTITY_DRIFT`
- `BLOCKED_OTHER_DIRTINESS`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_STAT_ANOMALY_PERSISTS`
- `BLOCKED_POSTVERIFY_FAILED`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Prohibited

No repetition of Task 030 restoration; no file-content/timestamp write; no broad index refresh; no add/restore/checkout/reset/clean; no worktree create/remove/re-register/prune; no Task 025 execution; no process kill/action; no runtime/provider/recovery/`cnx`/OpenClaw/Ollama action; no lifecycle action; no repository rename/reference migration; no force push, merge, tag, or release.
