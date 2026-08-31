# CNX-20260824-040 — Classify Task038 Worktree 415-Path Loss

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: AUTO  
Predecessor: CNX-20260824-039 (reviewed BLOCKED)

## Role split and reason for local proof

ChatGPT identified the exact causal boundary: the Task 038 detached worktree has an intact detached HEAD/index/registration record but 415 tracked paths are absent from its working tree.

ChatGPT cannot access the operator machine's exact missing/remaining path inventory or NTFS metadata. Codex is therefore delegated only the narrow local path-metadata proof required to classify the loss pattern. Codex must not design a fix, repair or remove the worktree, or broaden diagnosis beyond this exact path.

## Objective

Using read-only Git and filesystem metadata, determine the exact selection pattern of the 415 tracked deletions and whether it matches an explainable checkout/materialization boundary or the earlier mass-loss signature recorded in durable reports.

Do not identify a process/PID without direct evidence. Do not convert correlation into cause.

## Exact identities

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Primary workspace:

`C:\Users\CDQ-P\.openclaw\workspace`

Exact target worktree:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260824-038`

Expected target HEAD:

`c4973137d4abce9340903498a717821ea7e333c8`

Matching report:

`docs/operations/coordination/reports/CNX-20260824-040-classify-task038-worktree-415-path-loss.md`

## Duplicate-execution fence

Freshly fetch the coordination branch from the existing primary workspace.

If the matching Task 040 report exists at fetched HEAD:

- do not inspect the target again;
- do not publish a duplicate report;
- stop awaiting ChatGPT review.

Do not create/register a worktree, clone, branch, repository, temporary checkout, or index.

## Immutable read-only boundary

Set and prove `GIT_OPTIONAL_LOCKS=0` for every Git query against the target.

Do not run any command that refreshes or rewrites an index. Prohibited examples include `git add`, `git update-index`, `git checkout`, `git reset`, `git clean`, `git restore`, `git worktree repair`, `git worktree prune`, and `git worktree remove`.

Do not open ordinary tracked-file contents. Path names, tree object metadata, filesystem metadata, and durable coordination report text are sufficient.

Do not access the Task 027 worktree. Historical comparison may use only already committed Task 027–034 coordination reports/reviews and evidence references that can be read from the primary repository.

## Required classification

Record without writing a local manifest:

1. target path existence, exact gitdir/common-dir identity, HEAD, detached/branch state, and registration entry;
2. pre-query hashes/sizes/write timestamps for the target index and registration metadata;
3. total tracked path count at HEAD;
4. exact count and SHA256 of a canonical UTF-8 sorted deleted-path list, computed in memory;
5. exact count and SHA256 of a canonical UTF-8 sorted present-tracked-path list, computed in memory;
6. full present tracked path list in the report when small; otherwise first/last bounded samples plus counts and hash;
7. deleted and present distributions by top-level directory and file extension;
8. whether the 415 deleted paths form complete directory subtrees, all paths except a small allowlist, a filename/extension class, or another exact deterministic predicate;
9. index flags for deleted and present paths, including skip-worktree and assume-unchanged indicators, without changing them;
10. file modes/object types/sizes available from `git ls-tree -r -l`, without reading blob content;
11. filesystem enumeration of remaining files/directories, junction/reparse attributes, and timestamps under the exact target only;
12. sparse-checkout/config.worktree, submodule, nested-repository, operation-marker, lock, locked/prunable, and case-sensitivity indicators;
13. narrow process attachment for the exact target, excluding the inventory process itself;
14. comparison against committed Task 030–034 report/review path counts or hashes when those durable records provide an exact comparable signature; clearly state when comparison is unavailable;
15. post-query hashes/sizes/write timestamps for target index and registration metadata.

## Acceptance results

Return exactly one:

- `PASS_PATH_LOSS_PATTERN_CLASSIFIED` — an exact deterministic selection predicate is proven, but no actor/process cause is claimed without direct evidence;
- `BLOCKED_PATH_LOSS_PATTERN_AMBIGUOUS`;
- `BLOCKED_TARGET_IDENTITY_CHANGED`;
- `BLOCKED_ACTIVE_PROCESS_ATTACHMENT`;
- `BLOCKED_READ_ONLY_CLASSIFICATION_MUTATED_STATE`;
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`.

A PASS authorizes no repair, restoration, removal, pruning, Procmon action, capture, or runtime action.

## Report publication fence

The only repository mutation permitted is the matching Task 040 report.

Publish from the existing primary workspace only. Before publication, prove no unrelated staged/unstaged state would be included. Stage exactly the report path; prohibit `git add .`, `git add -A`, and `git commit -a`.

Commit message begins:

`report: CNX-20260824-040`

Verify the report commit changes exactly one path.

If publication cannot be proven safe without a new worktree or broad mutation, return `BLOCKED_REPORT_PUBLICATION_UNSAFE` through the safest available coordination path without creating another worktree.

## Required report fields

Include:

- fetched start HEAD;
- exact commands and `GIT_OPTIONAL_LOCKS=0` proof;
- identity/registration/HEAD result;
- tracked/deleted/present counts and canonical hashes;
- present-path list or bounded samples;
- directory/extension/index-flag/tree-object/filesystem-attribute distributions;
- deterministic predicate result;
- comparison with durable earlier evidence;
- process-attachment result;
- pre/post metadata identity;
- exact acceptance result;
- direct evidence vs inference separation;
- side-effect accounting;
- remaining uncertainty;
- explicit confirmation that no worktree/index/tracked path/process/runtime/Procmon state was modified;
- `Human decision required: YES|NO`.

## Prohibited

No tracked-file content read, Task 027 worktree access, new manifest file, worktree/clone/branch/repository creation, repair, removal, prune, checkout, reset, clean, restore, add/refresh, index rewrite, process termination, watcher/Supervisor/task/config change, Procmon launch/config/load/capture, PML/CSV/backing file, retained-evidence cleanup, CogentNexus/OpenClaw/Ollama runtime/recovery/lifecycle action, force push, merge, tag, or release.
