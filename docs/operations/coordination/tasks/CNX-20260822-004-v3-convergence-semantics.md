# CNX-20260822-004 — Align V3 Suite with Durable Convergence Evidence

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-003` (ACCEPT)

## Objective

Correct the v3 full process-recovery harness so post-transition acceptance waits for observed durable/runtime convergence instead of asserting `READY` immediately after a replacement listener appears.

Task 003 proved that Gateway process recovery and durable recovery are separate evidence gates: the replacement listener appeared first, and durable state naturally converged from `READY_WITH_WARNINGS` to `READY` after 8 observations in 14.769 seconds.

This is a harness/evidence-semantics task only. Do not modify CogentNexus runtime recovery behavior and do not run a disruptive Windows scenario in this task.

## Source gates

Repository: `funggier/cogentnexus`  
Coordination branch: `agent/v0.9.3-recovery-reality-tests`  
Required ancestor: `05c61c73494c0282d42ae342eeaafa3e9151fc97`  
Target harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Pre-change harness blob: `8ef976e52b9a9d112b418bee7afb63ee0a377f8b`  
Target smoke workflow: `.github/workflows/v093-ollama-recovery-v3-smoke.yml`  
Pre-change workflow blob: `7f9c62771848316a8e06712349595cd1e833d3d4`

Use a clean isolated worktree. Preserve unrelated and dirty worktrees. Before editing, verify the required ancestor, the two pre-change blobs, and empty `git status --short`.

If either target already differs, classify whether an equivalent accepted fix is already present. Do not overwrite newer work blindly; report `BLOCKED` or `SUPERSEDED` evidence as appropriate.

## Required implementation behavior

Add a bounded read-only convergence observation path for post-transition checks.

It must:

1. observe actual runtime evidence rather than succeed because time elapsed;
2. repeatedly read `cnx status`, `cnx provider status --json`, `cnx check recovery --json`, Gateway listener state, and Ollama listener state as applicable;
3. succeed only when mode is MANAGED, Ollama is selected/healthy, required listeners are healthy, and recovery verdict is `READY`;
4. record the first verdict, final verdict, attempts, elapsed time, last observation, and relevant maintenance/provider-incident diagnostics in JSON evidence;
5. use `RecoveryFuseSeconds` only as an observation/test fuse;
6. fail honestly when convergence is not observed inside the fuse.

Apply the convergence observation after:

- replacement Gateway listener detection;
- replacement Ollama listener detection, while preserving provider-incident evidence;
- the explicitly authorized operator `cnx start` following the intentional-stop scenario.

The pre-scenario baseline may remain a strict immediate baseline assertion.

## Immutable safety invariants

- exact validated listener PID only;
- no process-tree kill or `taskkill /T`;
- no manual `cnx start`, `cnx stop`, or `cnx restart` after Gateway/Ollama crash injection;
- the intentional-stop scenario may use only its documented `cnx stop` and subsequent `cnx start`;
- no timer/cooldown becomes recovery authority;
- do not weaken harness/harness-ancestor/protected-process rejection;
- do not hide `READY_WITH_WARNINGS`, skipped observations, failure, or timeout;
- do not change the frozen v0.9.2 baseline;
- do not reintroduce LM Studio;
- do not install, reset, or uninstall CogentNexus;
- do not execute the disruptive suite in this task.

## Smoke and regression contract

Update the PS5.1 v3 smoke workflow so it rejects regression to immediate post-listener `Assert-Baseline` acceptance and confirms the new convergence-observation contract is present.

Run all safe applicable validation, including:

- PowerShell 5.1 parser validation;
- harness `-SyntaxOnly`;
- the v3 smoke contract;
- existing relevant non-disruptive repository tests.

Record commands and exit codes. CI for the implementation commit must be cited when available; never invent a green result.

## Allowed changes

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- `.github/workflows/v093-ollama-recovery-v3-smoke.yml`
- `docs/V093_RECOVERY_REALITY_TESTS.md` only if needed to document the corrected evidence semantics
- matching Codex report

Do not change runtime implementation files in this task.

## Acceptance criteria

PASS requires:

- source/isolation gates pass;
- post-transition scenarios use the read-only convergence observer;
- convergence requires durable `READY` plus MANAGED/Ollama/listener health;
- evidence records first/final verdict, attempts, elapsed time, and last/relevant diagnostic state;
- provider incident and circuit-open checks remain enforced;
- intentional-stop semantics remain enforced;
- exact-PID and protected-process safety remains unchanged or stronger;
- parser, `-SyntaxOnly`, smoke contract, and relevant tests pass;
- implementation commit and changed-file list are recorded;
- no disruptive local runtime action was executed.

## Report

Write:

`docs/operations/coordination/reports/CNX-20260822-004-v3-convergence-semantics.md`

Include source gates, exact changes, validation commands/exit codes, CI state, safety review, changed files, implementation commit, unproven items, and the exact recommended full-suite command for the later execution task.

Commit/push authorized code and the matching report normally. Use commit messages beginning with:

- `test: align v3 recovery convergence evidence`
- `report: CNX-20260822-004`

Never force-push. Stop after publishing the report.
