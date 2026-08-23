# CNX-20260823-016 — Offline Provider Durable-Convergence Diagnosis

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current provider recovery blocker  
Predecessor: `CNX-20260823-015` (`REWORK`)  
Execution mode: `AUTO`

## Objective

Determine, without another Windows recovery run, why the Ollama listener and runtime health recovered while the durable provider incident remained open and `cnx check recovery` stayed `READY_WITH_WARNINGS` for the full 420-second observation fuse.

Also publish the corrected Task 015 evidence matrix using exact recorded values or `NOT_RECORDED`. Do not implement a product fix in this task.

## Duplicate-execution fence

Before reading local evidence or source:

1. fetch the coordination branch;
2. confirm `ACTIVE.md` names `CNX-20260823-016` with `READY_FOR_CODEX` and `AUTO`;
3. check for `docs/operations/coordination/reports/CNX-20260823-016-offline-provider-durable-convergence-diagnosis.md`;
4. if that report exists, perform no further observation or action and stop awaiting ChatGPT review.

## Checkout boundary

Use only the isolated checkout supplied for the current Codex/Scheduled-task run.

- Do not execute `git worktree add`.
- Do not create a clone, nested worktree, fallback checkout, alternate path, or suffixed path.
- Record the environment-supplied repository path and its start HEAD.
- If no usable isolated checkout is supplied and execution would require creating another checkout, publish `BLOCKED`; do not create one.
- Do not inspect, modify, remove, prune, repair, rename, or reuse any Task 007–015 worktree or clone.

This distinction is intentional: an environment-provided isolated checkout is allowed; manually creating another checkout is not.

## Immutable evidence inputs

Read only:

1. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`
   - bytes: `1802394`
   - SHA256: `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
2. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`
   - bytes: `5900085`
   - SHA256: `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`
3. Task 015 report and ChatGPT review.
4. Repository source in the environment-supplied checkout.

Verify the evidence identities before extraction. Do not search for or substitute another evidence file.

## Bounded source scope

Start with these tracked files:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- `skills/cogentnexus/scripts/cnx_v093.py`
- `skills/cogentnexus/scripts/provider_v093.py`
- relevant tests already tracked under `tests/`

A bounded read-only `rg` search is allowed only inside `skills/cogentnexus/scripts`, `scripts`, and `tests` for exact state-transition tokens found in the evidence or source, including:

- `provider_unreachable`
- `Provider recovery incident`
- `recoveryAttempts`
- `circuitOpen`
- `incidentOpen`
- `READY_WITH_WARNINGS`
- `stable`
- `incident`
- `healthy-runtime`

Record every searched token, returned path, command, and exit code. Do not broaden to user data, other repositories, worktrees, sessions, caches, or live Windows state.

## Required diagnosis

### 1. Corrected Task 015 matrix

For every Task 015 required provenance, chronology, injection-safety, and gate field:

- publish the exact recorded value; or
- publish `NOT_RECORDED`.

Do not infer tested source HEAD, branch, version, kill exit status, persistence timestamp, duration, or transition timing.

Use these gate rules:

- a replacement listener may be recorded as an observed runtime outcome;
- an exact-PID injection gate is `PROVEN` only if every required safety and outcome field exists;
- a complete provider incident lifecycle is not `PROVEN` unless normal closure is recorded;
- cleanup-induced health does not prove natural provider convergence;
- a fuse is observation safety only, never recovery authority.

### 2. Source transition map

Identify exact files, functions/classes, and relevant line ranges or symbols for:

- provider failure detection;
- incident creation/classification;
- attempt advancement;
- recovery-success recording;
- stable-success accumulation, if any;
- incident/circuit closure;
- maintenance/recovery marker closure;
- `READY` versus `READY_WITH_WARNINGS` derivation;
- any background/event/reconcile path required to execute closure.

For each transition state:

- durable input/precondition;
- writer;
- reader/validator;
- expected next state;
- evidence showing whether it occurred;
- reason it could remain open after runtime health returned.

### 3. Harness assertion analysis

Determine whether `Wait-DurableConvergence -RequireProviderIncident` is checking the actual normal closure contract or an incompatible field/timing expectation.

The harness blob at the report head is:

`6d4c9347de12bbe4e3e5c428f2fe80333f92757f`

Verify whether the checked-out harness matches that blob. A match does not establish the unrecorded tested source HEAD.

### 4. Root-cause classification

Return exactly one:

- `RUNTIME_CLOSE_TRANSITION_MISSING`
- `RUNTIME_CLOSE_TRANSITION_NOT_SCHEDULED`
- `STABLE_SUCCESS_PRECONDITION_NOT_MET`
- `HARNESS_ASSERTION_MISMATCH`
- `SOURCE_PROVENANCE_INSUFFICIENT`

If evidence supports more than one possibility but cannot distinguish them, use `SOURCE_PROVENANCE_INSUFFICIENT` and identify the smallest additional offline evidence needed.

### 5. Next disposition

Return one:

- `NARROW_FIX_READY` with exact files/symbols, proposed invariant-preserving change, and non-runtime validations;
- `MORE_OFFLINE_DIAGNOSTIC_REQUIRED` with one exact missing question;
- `HUMAN_DECISION_REQUIRED` with one exact material choice.

Do not write or apply the fix in this task.

## Prohibited actions

- no recovery harness/scenario execution, syntax mode, preflight, or CI wait;
- no live process, listener, service, Scheduled Task, `cnx`, OpenClaw, or Ollama command;
- no process kill, restart, suspend, process-tree action, UI/window/app action, or configuration change;
- no install, reset, uninstall, reinstall, package change, merge, tag, release, or force-push;
- no source/evidence modification;
- no Task 007–015 checkout inspection or cleanup;
- no chat, Project, session, cache, or unrelated user-data access.

## Problem-report contract

If `BLOCKED` or `FAIL`, the report must still include:

- exact blocker and blocker class;
- evidence inspected;
- commands and exit codes;
- safety/side-effect accounting;
- proven, failed, skipped, and unproven items;
- safe remediation options;
- recommended option;
- `Human decision required: YES|NO`;
- duplicate-execution fence result.

Stop the unsafe or impossible action, not the reporting loop.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-016-offline-provider-durable-convergence-diagnosis.md`

Commit message must begin:

`report: CNX-20260823-016`

Never force-push. Stop after publishing the matching report.
