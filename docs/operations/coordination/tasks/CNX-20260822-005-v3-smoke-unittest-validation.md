# CNX-20260822-005 — Correct V3 Smoke and Complete Safe Validation

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-004` (BLOCKED)

## Objective

Complete the Task 004 harness-validation gate without running disruptive scenarios or installing a new Python test dependency.

Correct only the false-positive v3 smoke contract, run the existing standard-library unit tests directly, push the narrow fix, and cite completed CI for the exact implementation head.

## Source gates

Repository: `funggier/cogentnexus`  
Coordination branch: `agent/v0.9.3-recovery-reality-tests`  
Required implementation ancestor: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`  
Harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Expected current harness blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`  
Smoke workflow: `.github/workflows/v093-ollama-recovery-v3-smoke.yml`  
Expected current workflow blob: `8d7d223a7fa8e4daee5125edf1de3db4142c5afb`  
Failed workflow run: `32582098442`  
Failed job: `97052907524`

Use a clean isolated worktree, or safely reuse the Task 004 isolated worktree only if it is present, synchronized, and clean. Preserve unrelated and dirty worktrees.

Before editing, verify the required ancestor, both expected blobs, and empty `git status --short`.

## Exact failure classification

The harness parser and `-SyntaxOnly` passed. GitHub CI failed only in the smoke contract with:

`Post-transition listener observation is not followed by convergence observation.`

The broad multiline regex crossed function boundaries: from a Gateway listener-observation line it could reach the later `Assert-Baseline 'provider-before'`. This is a smoke-test false positive, not evidence that the convergence call is absent.

## Required fix

Update only `.github/workflows/v093-ollama-recovery-v3-smoke.yml` so the contract verifies the explicit scenario calls without matching across function boundaries.

The contract must require these exact semantic calls:

- `Wait-DurableConvergence 'converge-gateway-after'`
- `Wait-DurableConvergence 'converge-provider-after' $true`
- `Wait-DurableConvergence 'converge-after-operator-start'`

It must reject these immediate post-transition assertions if present:

- `Assert-Baseline 'gateway-after'`
- `Assert-Baseline 'provider-after'`
- `Assert-Baseline 'operator-after'`

Remove or replace the cross-function regex that failed run `32582098442`.

Do not weaken the other schema, exact-PID, protected-process, evidence-field, or status-shape assertions.

Do not change the harness unless its current blob differs or a new directly observed parser/contract defect makes the workflow-only fix impossible. If so, report `BLOCKED` rather than expanding scope.

## Required local validation

Do not install `pytest`. Run exactly:

`python tests/test_provider_recovery_authority.py`

`python tests/test_provider_recovery_v092.py`

`python tests/test_checks_v092.py`

Also run:

- Windows PowerShell 5.1 parser validation for the v3 harness;
- v3 harness `-SyntaxOnly`;
- the corrected smoke contract commands locally;
- `git diff --check`.

Record every command and exit code.

## CI gate

Commit and push the workflow correction normally. Allow the push-triggered CI to run.

Use bounded read-only observation to record every applicable workflow name/status/conclusion for the exact implementation head. Do not claim CI green while a required workflow is failed, cancelled, skipped unexpectedly, or still in progress.

The v3 smoke workflow must complete with `success`.

Do not manually rerun failed workflows unless a new commit with the authorized fix triggers them normally.

## Safety invariants

- no disruptive Windows scenario;
- no PID kill;
- no `cnx start`, `cnx stop`, `cnx reset`, or `cnx uninstall`;
- no software or Python package installation;
- no runtime implementation change;
- no process-tree kill authorization;
- no change to v0.9.2, LM Studio scope, or recovery authority;
- no force-push or unrelated-worktree cleanup.

## Acceptance criteria

PASS requires:

- source and isolation gates pass;
- only the smoke workflow and matching report change;
- the false-positive cross-function regex is removed/replaced;
- exact per-scenario convergence calls are required;
- forbidden immediate post-transition assertions are rejected;
- all three Python unittest files pass when executed directly;
- parser, `-SyntaxOnly`, local contract, and `git diff --check` pass;
- exact implementation commit and changed files are recorded;
- all applicable CI for that head is complete and the v3 smoke succeeds;
- no disruptive/runtime/lifecycle action occurs;
- the report corrects Task 004 provenance by recognizing commit `592a6fbd37da05013b7a8a5875ccd8b17e188cfa` as the implementation/report commit.

## Report

Write:

`docs/operations/coordination/reports/CNX-20260822-005-v3-smoke-unittest-validation.md`

Include source gates, exact workflow change, all commands/exit codes, exact implementation commit, complete CI table, changed files, safety notes, remaining unproven items, and the exact recommended later full-suite command.

Use commit messages beginning:

- `ci: fix v3 convergence smoke contract`
- `report: CNX-20260822-005`

Never force-push. Stop after publishing the report.
