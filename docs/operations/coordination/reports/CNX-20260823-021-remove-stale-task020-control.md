# CNX-20260823-021 — Remove Exact Stale Task 020 Control Worktree

Task ID: `CNX-20260823-021`
Status: `BLOCKED`
Primary result: `BLOCKED_TARGET_IDENTITY`
Repository path: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-021`
Branch: detached control worktree
Start/fetched HEAD: `30ba9488bb210363ec9cd2d1778aa4c831f159e2`
ACTIVE verification: remote `ACTIVE.md` read after fetch; `Status: READY_FOR_CODEX`, `Execution mode: AUTO`, Task ID `CNX-20260823-021`.

## Commands and observations

- `git fetch --prune origin agent/v0.9.3-recovery-reality-tests` — exit `0`; fetched HEAD `30ba9488bb210363ec9cd2d1778aa4c831f159e2`.
- Read remote `CODEX_BOOTSTRAP.md`, `WATCH_MODE.md`, `SIGNALS.md`, `README.md`, `PROBLEM_LOOP.md`, `ACTIVE.md`, and the exact Task 021 contract.
- Matching-report fence checked before execution — report absent.
- `git worktree add --detach C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-021 FETCH_HEAD` — exit `0`; control path registered at fetched HEAD and clean.
- `git worktree list --porcelain` — exit `0`; exact removal target registered at `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-020`.
- `git -C C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-020 rev-parse HEAD` — exit `0`; observed `2bda9b71952f838da515e046fb3efa10a75f2089`.
- Required removal-target HEAD was `1718ea450c546abb55ad2892745f19f6e840ee5c`; exact identity gate failed.
- Target `git status --porcelain=v1 --untracked-files=all` and `git status --ignored --porcelain=v1` produced no entries in the observation performed.

## Safety accounting

The target was preserved. No `git worktree remove` was attempted. No Task 017 inspection, restore, cleanup, reset, force, prune, process action, runtime/recovery action, `cnx`/OpenClaw/Ollama action, source change, merge, tag, release, or force-push occurred. The only local state change was creation of the required clean Task 021 control worktree for reporting.

The target identity mismatch makes removal unsafe; reachability, lock/operation, and process-use gates were not used to override or compensate for the failed identity gate. No evidence supports removing this target.

Cause classification: task safety precondition / target identity mismatch.

Safe remediation options:

1. ChatGPT publishes a corrected Task 021 with the exact intended target HEAD and refreshed identity evidence.
2. ChatGPT closes or supersedes this task if the target is no longer the stale Task 020 control worktree.

Recommended next step: review the target registration and publish a narrow corrected task only after confirming the intended exact HEAD.

Human decision required: NO

Control cleanup: pending report publication; the control worktree will be removed only with normal non-force removal after successful publication if it remains clean and unused.

## Unproven

No claim is made about whether the observed target commit is safe to remove, whether it is reachable from source refs, whether any Git operation is active, or whether a process is using the target. Those checks were not needed after the exact identity gate failed.
