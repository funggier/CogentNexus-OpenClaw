# CNX-20260823-028 — Diagnose Incomplete Watcher Control Materialization

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-027` (`ACCEPT` for safe stop only)

## Objective

Determine, using read-only evidence, why watcher-provided coordination control worktrees contain many tracked/indexed paths that are absent from the working tree. Do not repair any checkout and do not resume Task 025 reconciliation.

## Exact targets

Primary diagnostic path:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-028`

Prior affected control:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Common repository expected:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Branch:

`agent/v0.9.3-recovery-reality-tests`

## Execution control

The watcher-provided Task 028 control may be inspected even if it is not clean; cleanliness is the subject of this diagnostic. Verify exact path registration, common-dir identity, freshly fetched coordination HEAD, and absence of an active Git operation before continuing. No fallback path and no new worktree may be created.

## Required evidence

Record exact commands, exit codes, and complete outputs or durable evidence-file references sufficient to prove:

1. registered worktree entries for Task 027 and Task 028, their HEADs, branches/detached state, lock/prunable annotations, and common-dir identity;
2. `git status --porcelain=v2 --untracked-files=all` for both existing paths, with exact counts by status and a SHA256 of the complete captured output if it is lengthy;
3. repository, worktree, global, and system configuration origins for:
   - `core.sparseCheckout`
   - `core.sparseCheckoutCone`
   - `core.worktree`
   - `extensions.worktreeConfig`
   - `core.ignoreCase`
   - `core.longpaths`;
4. existence and exact content/hash of any sparse-checkout or worktree-specific config files;
5. for at least three representative `.D` paths including one under `.github/workflows`:
   - HEAD tree membership/blob;
   - index membership/blob and skip-worktree/assume-unchanged flags;
   - filesystem presence or absence;
6. aggregate comparison of tracked index paths versus materialized files, without hashing large external/user data;
7. whether an in-progress Git operation, filesystem error, path-length failure, sparse materialization, interrupted checkout, or another evidenced condition best explains the state;
8. whether Task 027 and Task 028 controls contain any unique uncommitted content that a later cleanup must preserve;
9. the narrowest safe remediation proposal, naming exact paths and prohibiting data-loss assumptions.

## Results

Return exactly one:

- `PASS_CAUSE_IDENTIFIED_SAFE_REMEDIATION_DEFINED`
- `BLOCKED_CAUSE_AMBIGUOUS`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_EVIDENCE_INCOMPLETE`

Include `Human decision required: YES|NO`.

## Prohibited

No restore, checkout, reset, clean, prune, add, commit, ref update, sparse-checkout change, configuration change, file modification/deletion, worktree creation/removal, process action, runtime/recovery/provider/`cnx`/OpenClaw/Ollama action, lifecycle action, merge, tag, or release action.

## Duplicate-execution fence

If the matching Task 028 report exists at freshly fetched HEAD, perform no repeated inspection and stop awaiting ChatGPT review.

## Matching report

`docs/operations/coordination/reports/CNX-20260823-028-diagnose-incomplete-watcher-control.md`

Commit begins `report: CNX-20260823-028`.
