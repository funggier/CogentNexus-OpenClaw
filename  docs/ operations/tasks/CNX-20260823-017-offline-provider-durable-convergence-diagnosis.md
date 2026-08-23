# CNX-20260823-017 — Offline Provider Durable-Convergence Diagnosis in One Task-Owned Worktree

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current provider recovery blocker  
Predecessor: `CNX-20260823-016` (`ACCEPT` of safe `BLOCKED` report)  
Execution mode: `AUTO`

## Objective

Complete the offline/read-only diagnosis that Task 016 could not start because no environment-provided isolated checkout was supplied.

Determine why the Ollama listener and runtime health recovered while the durable provider incident remained open and `cnx check recovery` stayed `READY_WITH_WARNINGS` for the full 420-second observation fuse. Publish the corrected Task 015 evidence matrix. Do not implement a product fix.

## Duplicate-execution and collision fence

Before reading evidence or source:

1. fetch `origin agent/v0.9.3-recovery-reality-tests`;
2. confirm remote `ACTIVE.md` names `CNX-20260823-017` with `READY_FOR_CODEX` and `AUTO`;
3. check for `docs/operations/coordination/reports/CNX-20260823-017-offline-provider-durable-convergence-diagnosis.md` at the fetched remote head;
4. if that report exists, perform no further observation or action and stop awaiting ChatGPT review;
5. use exactly this task-owned path:
   `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-017`;
6. if that path or its Git worktree registration already exists, do not inspect it, reuse it, remove it, create a suffix, or create an alternative. Publish `BLOCKED` from the available repository context if safely possible; otherwise report the publication blocker without changing local state;
7. create at most one detached worktree at the exact fetched remote head. No clone, nested worktree, fallback checkout, or second path is authorized.

Record the source repository path, task-owned worktree path, fetched remote head, and diagnosis start HEAD.

## Narrow cleanup authorization

After the matching report commit has been pushed successfully:

- return to the source repository path;
- verify the task-owned worktree is clean and still registered at the exact task path;
- remove only that exact Task 017 worktree and prune only its now-stale registration if needed;
- do not use force removal;
- do not inspect, remove, prune, repair, rename, or reuse any Task 007–016 path;
- if the Task 017 worktree is dirty, in use, or publication was not confirmed, leave it intact and record `CLEANUP_BLOCKED`.

No process may be killed or closed to enable cleanup.

## Immutable evidence inputs

Read only:

1. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`
   - bytes: `1802394`
   - SHA256: `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
2. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`
   - bytes: `5900085`
   - SHA256: `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`
3. Task 015 report and ChatGPT review.
4. Repository source in the exact Task 017 worktree.

Verify both evidence identities before extraction. Do not search for or substitute other evidence.

## Bounded source scope

Start with:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- `skills/cogentnexus/scripts/cnx_v093.py`
- `skills/cogentnexus/scripts/provider_v093.py`
- relevant tracked tests under `tests/`

A bounded read-only `rg` search is allowed only inside `skills/cogentnexus/scripts`, `scripts`, and `tests` for exact transition tokens, including:

- `provider_unreachable`
- `Provider recovery incident`
- `recoveryAttempts`
- `circuitOpen`
- `incidentOpen`
- `READY_WITH_WARNINGS`
- `stable`
- `incident`
- `healthy-runtime`

Record every search command/token and exit code. Do not broaden to user data, other repositories, other worktrees, sessions, caches, or live Windows state.

## Required diagnosis

### 1. Corrected Task 015 matrix

For every Task 015 provenance, chronology, injection-safety, and gate field, publish the exact recorded value or `NOT_RECORDED`.

Do not infer tested source HEAD, branch, version, kill exit status, persistence timestamp, duration, or transition timing.

Apply these rules:

- a replacement listener is an observed runtime outcome;
- an exact-PID injection gate is `PROVEN` only if every required safety and outcome field exists;
- a complete provider incident lifecycle is not `PROVEN` unless normal closure is recorded;
- cleanup-induced health does not prove natural provider convergence;
- a fuse is observation safety only, never recovery authority.

### 2. Source transition map

Identify exact files and functions/classes/symbols for:

- provider failure detection;
- incident creation/classification;
- attempt advancement;
- recovery-success recording;
- stable-success accumulation;
- incident/circuit closure;
- maintenance/recovery marker closure;
- `READY` versus `READY_WITH_WARNINGS` derivation;
- any background/event/reconcile path required for closure.

For every transition, state the durable precondition, writer, reader/validator, expected next state, evidence of occurrence/non-occurrence, and why it could remain open after runtime health returned.

### 3. Harness assertion analysis

Determine whether `Wait-DurableConvergence -RequireProviderIncident` checks the real normal-closure contract or an incompatible field/timing expectation.

The required harness blob is:

`6d4c9347de12bbe4e3e5c428f2fe80333f92757f`

Verify the checked-out harness blob. A match does not prove the unrecorded tested source HEAD.

### 4. Root-cause classification

Return exactly one:

- `RUNTIME_CLOSE_TRANSITION_MISSING`
- `RUNTIME_CLOSE_TRANSITION_NOT_SCHEDULED`
- `STABLE_SUCCESS_PRECONDITION_NOT_MET`
- `HARNESS_ASSERTION_MISMATCH`
- `SOURCE_PROVENANCE_INSUFFICIENT`

If evidence supports multiple possibilities but cannot distinguish them, use `SOURCE_PROVENANCE_INSUFFICIENT` and name the smallest additional offline evidence required.

### 5. Next disposition

Return exactly one:

- `NARROW_FIX_READY` with exact files/symbols, an invariant-preserving proposed change, and non-runtime validations;
- `MORE_OFFLINE_DIAGNOSTIC_REQUIRED` with one exact missing question;
- `HUMAN_DECISION_REQUIRED` with one exact material choice.

Do not implement the fix.

## Prohibited actions

- no recovery harness/scenario, syntax mode, preflight, or CI wait;
- no live process, listener, service, Scheduled Task, `cnx`, OpenClaw, or Ollama command;
- no process kill, restart, suspend, process-tree action, UI/window/app action, or configuration change;
- no install, reset, uninstall, reinstall, package change, merge, tag, release, force-push, or source/evidence modification;
- no inspection or cleanup of Task 007–016 paths;
- no chat, Project, session, cache, or unrelated user-data access.

## Problem-report contract

If `BLOCKED` or `FAIL`, still include:

- exact blocker and blocker class;
- evidence inspected;
- commands and exit codes;
- safety/side-effect accounting;
- proven, failed, skipped, and unproven items;
- safe remediation options and recommended option;
- `Human decision required: YES|NO`;
- duplicate-execution/collision fence result;
- Task 017 cleanup status.

A safe stop is not permission to omit the matching report.

## Report and publication

Write only:

`docs/operations/coordination/reports/CNX-20260823-017-offline-provider-durable-convergence-diagnosis.md`

Commit message must begin:

`report: CNX-20260823-017`

Immediately before push, fetch the coordination branch again. If another matching Task 017 report now exists, do not push or overwrite it. Never force-push. Stop after publication and the exact-path cleanup attempt.
