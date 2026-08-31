# CNX-20260823-027 — Reconcile Task 025 Tree, Index, and Working-Tree State

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-026` (`REWORK`)

## Objective

Resolve the internal contradiction in Task 026 using exact read-only Git tree, index, and filesystem evidence for the Task 025 control worktree. Do not repeat the broader Task 026 diagnosis and do not change any state.

## Exact target

Control path:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-025`

Commit:

`5dbf0425ed42f23da95ba3fa25ecbc57893f1d92`

Parent:

`a67515d46927da5b2565d91a6a4bbec532e82aba`

Task 020 path:

`docs/operations/coordination/reports/CNX-20260823-020-isolated-adjudication-and-task017-removal.md`

Task 025 path:

`docs/operations/coordination/reports/CNX-20260823-025-publish-task020-from-immutable-blob.md`

## Execution control

Use only the watcher-provided clean Task 027 control after verifying it is registered at freshly fetched coordination HEAD and operation-free. The Task 025 target is inspection-only. No fallback worktree.

## Required evidence

Record exact commands, exit codes, and unabridged outputs for:

1. `git cat-file -t` and `git cat-file -p` for commit `5dbf0425...`, sufficient to show parent and tree.
2. `git diff-tree --no-commit-id --name-status -r 5dbf0425...`.
3. `git ls-tree -r 5dbf0425... -- <Task020 path> <Task025 path>`.
4. `git ls-tree -r a67515d... -- <Task020 path> <Task025 path>`.
5. From the exact Task 025 worktree:
   - top-level/common-dir and HEAD;
   - `git status --porcelain=v2 --untracked-files=all`;
   - `git ls-files --stage -- <Task020 path> <Task025 path>`;
   - read-only filesystem existence, byte count, SHA256, and first heading for each path, or explicit ABSENT.
6. Resolve whether `D` represents deletion relative to HEAD/index, a committed deletion, an index-only difference, or another state.
7. State separately:
   - membership of each path in parent tree;
   - membership of each path in commit tree;
   - membership/blob in index;
   - working-tree presence/content;
   - changed paths parent-to-commit.

## Results

Return exactly one:

- `PASS_TREE_INDEX_WORKTREE_RECONCILED`
- `BLOCKED_OBJECT_MISSING`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_EVIDENCE_INCOMPLETE`

Include `Human decision required: YES|NO`.

## Prohibited

No restore, checkout, reset, clean, prune, add, commit, ref creation, worktree removal or creation except watcher-provided Task 027 control; no file modification/deletion/publication; no process action; no runtime/recovery/provider/`cnx`/OpenClaw/Ollama action; no lifecycle, merge, tag, or release action.

## Duplicate-execution fence

If the matching Task 027 report exists at fetched HEAD, perform no repeated inspection and stop awaiting ChatGPT review.

## Matching report

`docs/operations/coordination/reports/CNX-20260823-027-reconcile-task025-tree-index-worktree.md`

Commit begins `report: CNX-20260823-027`.
