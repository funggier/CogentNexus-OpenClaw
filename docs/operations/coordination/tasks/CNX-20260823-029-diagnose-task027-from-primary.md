# CNX-20260823-029 — Diagnose Task 027 Control From Primary Repository

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-028` (`ACCEPT` for safe stop only)

## Objective

Determine, using read-only Git and filesystem evidence, why the existing Task 027 registered control contains widespread tracked/indexed paths absent from its working tree. This task intentionally does not require, create, adopt, repair, or remove a Task 029 control worktree.

Do not resume Task 025, diagnose provider convergence, or touch CogentNexus/OpenClaw/Ollama runtime state.

## Exact identities

Primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

Affected control:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Repair commit required as ancestor of fetched branch HEAD:

`af53fb3d19d6245552699795c638e159edc83204`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Matching report:

`docs/operations/coordination/reports/CNX-20260823-029-diagnose-task027-from-primary.md`

## Execution model

Run read-only inspection from the primary repository or another already-existing, verified complete checkout. The presence, absence, dirtiness, or registration of a watcher-created Task 029 path is irrelevant and must not block this task.

Do not create or require a Task 029 worktree. Do not use any fallback target in place of the exact Task 027 affected control.

Before inspection:

1. fetch the exact coordination branch;
2. verify `af53fb3d19d6245552699795c638e159edc83204` is an ancestor of fetched branch HEAD;
3. read ACTIVE, this task, predecessor report, and predecessor review from fetched HEAD;
4. verify the matching Task 029 report is absent at fetched HEAD;
5. verify no merge, rebase, cherry-pick, revert, bisect, or index lock is active in the primary repository or Task 027 control;
6. capture primary-repository status but do not modify it.

If the report already exists, stop without repeating inspection.

## Required read-only evidence

Record exact commands, exit codes, complete outputs or durable evidence references, and SHA256 hashes for lengthy captures.

### A. Registration and identity

- `git worktree list --porcelain`;
- exact Task 027 registration, HEAD, detached/branch state, lock/prunable annotations;
- Task 027 `--git-dir`, `--git-common-dir`, top level, and common repository identity;
- primary repository HEAD, fetched branch HEAD, and required-ancestor result.

### B. Status and aggregate materialization

- `git status --porcelain=v2 --untracked-files=all` for Task 027;
- exact counts grouped by porcelain status;
- SHA256 of the full status capture;
- count of index-tracked paths;
- count of tracked paths physically materialized;
- count and list/hash of tracked paths absent from filesystem;
- do not hash large external/user data.

### C. Configuration and sparse state

Capture value and origin at system, global, repository, and worktree scope where applicable:

- `core.sparseCheckout`;
- `core.sparseCheckoutCone`;
- `core.worktree`;
- `extensions.worktreeConfig`;
- `core.ignoreCase`;
- `core.longpaths`.

Record existence, content, and SHA256 of sparse-checkout and worktree-specific config files. Do not change configuration.

### D. Tree, index, filesystem comparison

For at least five representative missing tracked paths, including:

- one under `.github/workflows`;
- one coordination file;
- one source/script file;
- one test file when available;
- one additional path from a different directory;

record:

- fetched/Task027 HEAD tree membership and blob SHA;
- index membership and blob SHA;
- skip-worktree and assume-unchanged flags;
- filesystem presence;
- parent-directory presence;
- path length.

### E. Failure indicators

Read-only inspect for:

- in-progress Git operations and lock files;
- filesystem/path-length/access errors visible in relevant logs or Git trace already present;
- sparse materialization;
- interrupted checkout evidence;
- watcher/pre-materialization behavior evidenced by registration metadata or existing logs;
- unique staged, unstaged, or untracked content in Task 027 that cleanup must preserve.

Do not speculate beyond evidence. Classify ambiguous causes as blocked.

### F. Narrow remediation manifest

If the cause is identified, propose—but do not execute—the narrowest remediation. It must name exact paths, preservation steps, verification gates, and non-force cleanup rules. If unique content or ambiguous filesystem state exists, require preservation before any repair/removal.

## Report publication safety fence

The diagnostic itself is read-only. The only authorized repository mutation is publication of the matching report.

Before committing:

1. confirm the publisher checkout is complete enough that tracked files are not broadly absent;
2. write only the matching report path;
3. stage only that exact path using a path-scoped command;
4. never use `git add .`, `git add -A`, `git commit -a`, reset, clean, restore, checkout, or sparse-checkout;
5. capture `git diff --cached --name-status`;
6. require exactly one entry: `A` or `M` for the matching report path;
7. require zero `D` entries and zero other paths;
8. if any fence fails, do not commit or push; return/publish the narrowest safe blocker through an already-safe channel only;
9. after commit, verify the commit changes exactly the matching report path before push;
10. push without force and verify remote branch contains the report.

The report commit message begins `report: CNX-20260823-029`.

## Results

Return exactly one:

- `PASS_CAUSE_IDENTIFIED_SAFE_REMEDIATION_DEFINED`
- `BLOCKED_CAUSE_AMBIGUOUS`
- `BLOCKED_EVIDENCE_INCOMPLETE`
- `BLOCKED_PRESERVATION_REQUIRED`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Prohibited

No worktree creation/removal/repair, restore, checkout, reset, clean, prune, sparse-checkout change, configuration change, ref movement, force push, broad staging, file deletion, process action, runtime/recovery/provider/`cnx`/OpenClaw/Ollama action, lifecycle action, merge, tag, release, or repetition of Task 025/028 side effects.

## Duplicate-execution fence

If the matching report exists at freshly fetched HEAD, perform no repeated inspection and stop awaiting ChatGPT review.
