# CNX-20260829-127 — Recovery Harness Fail-Closed Contract and CI Proof

## Verdict

**PASS — the recovery harness durable-convergence contract is now behaviorally exercised through the real non-disruptive PowerShell entrypoint, warning acceptance is fail-closed, the dedicated Recovery V3 smoke runs on direct push, all required exact-SHA workflows passed, and a fresh exact-SHA package proof was retained. No live lifecycle, provider mutation, or recovery replay was performed.**

## Scope and fences

This task was limited to repository source, tests, workflow, and CI/package proof. No install, install-over, reset, uninstall, reinstall, stop, start, restart, provider reconfiguration, process kill, live crash injection, cleanup, or recovery replay was performed.

The retained Task-125 evidence remained read-only input. The Task-126 review remained authoritative for the root-cause classification: provider process recovery was coherent, while the previous harness incorrectly required exact `READY` even though the intentionally open, circuit-closed provider incident made the read-only recovery verdict `READY_WITH_WARNINGS` pending stable model-success evidence.

Task-127 starting coordination commit:

- `4d0f7c30fbb6412945a7c0d44b15e1b583cc7461`

## TDD RED

A Python regression was changed to invoke the real PowerShell harness entrypoint with `-ContractSelfTest` instead of duplicating the predicate in Python or grepping source text.

Before the harness implementation existed, the actual PowerShell entrypoint rejected `-ContractSelfTest` with `NamedParameterNotFound`. This was the behavioral RED boundary.

## Repair

The implementation is responsibility-local to the recovery acceptance harness. Provider recovery runtime/policy was not changed.

`scripts/test-v093-ollama-recovery-windows-v3.ps1` now contains:

- `Test-DurableConvergenceObservation`, the single predicate used by `Wait-DurableConvergence`;
- `Invoke-ContractSelfTest`, exposed by the non-disruptive `-ContractSelfTest` switch;
- full recovery-check rows retained in convergence observations so the predicate can distinguish the one permitted provider-incident warning from unrelated warnings.

The fail-closed contract is:

- ordinary Gateway/operator convergence remains strict `READY`;
- `READY_WITH_WARNINGS` is eligible only when provider-incident convergence is explicitly required;
- exactly one `Provider event adapter` row must exist and `details.expected == false`;
- exactly one `Provider recovery incident` row must exist;
- for warning-state acceptance that incident must itself be `WARN`, `incidentOpen == true`, and `circuitOpen == false`;
- it must be the **only** WARN row;
- every other recovery check must be `PASS`;
- any `FAIL` or `INDETERMINATE` row rejects convergence;
- missing/duplicate adapter or incident rows reject convergence;
- managed host mode, host/provider selection `ollama`, Gateway listener, and Ollama listener remain required.

Listener/process health is not converted into stable model-success evidence and does not close the durable provider incident.

## Behavioral self-test cases

The harness-owned self-test exercises the reviewed recovery-convergence surface, including:

1. retained incident-scoped `READY_WITH_WARNINGS` state accepted;
2. the same warning state rejected on an ordinary/non-provider convergence path;
3. provider incident plus maintenance warning rejected;
4. provider incident plus supervisor warning rejected;
5. provider incident plus adapter warning rejected;
6. closed/non-warning incident under warning verdict rejected;
7. circuit-open incident rejected;
8. exact `READY` path accepted;
9. missing incident rejected;
10. duplicate incident rejected;
11. missing adapter rejected;
12. duplicate adapter rejected.

The production predicate additionally enforces the general invariant that the provider recovery incident must be the sole warning for the exceptional `READY_WITH_WARNINGS` path.

## Commit chain

- `51c0eca63e791b5ef5fac1a3c59caa959c5da579` — `test: add fail-closed recovery contract self-test`
- `ea0ab612e131f26af719aa123e980572e1e222e0` — `test: make recovery contract smoke Windows-specific`
- `1b922bf400fdbccb1f9c7019b89b69fd67f44070` — `ci: run recovery v3 smoke on exact push sha`

**Final source candidate:** `1b922bf400fdbccb1f9c7019b89b69fd67f44070`

The final commit adds direct-push path triggering for `.github/workflows/v093-ollama-recovery-v3-smoke.yml`, covering the harness, its behavioral test, and the workflow file itself.

## Local validation

Recorded Task-127 local results:

- PowerShell harness `-ContractSelfTest`: PASS;
- focused Python contract test: PASS on Windows; explicitly skipped where `powershell.exe` is unavailable;
- full Python suite: `485 passed, 3 skipped, 4 subtests passed`;
- PowerShell `-SyntaxOnly`: PASS;
- `python -m compileall -q skills scripts tests`: PASS;
- `sh -n scripts/install.sh`: PASS;
- `git diff --check`: PASS;
- workflow YAML parse: PASS;
- plugin tests: `50` files / `268` tests passed;
- plugin validation: PASS;
- plugin evaluation: PASS.

The first cross-platform Validate attempt exposed that the behavioral test unconditionally invoked `powershell.exe` on non-Windows runners. The correction scopes that test to hosts where Windows PowerShell is available while the dedicated Windows Recovery V3 smoke remains the authoritative execution of the actual harness-owned self-test.

## Exact-SHA CI proof

All required workflows completed successfully for exact final candidate `1b922bf400fdbccb1f9c7019b89b69fd67f44070`:

- Validate — run `33226001453` — `success`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke — run `33226001456` — `success`
- PS5.1 Acceptance Smoke — run `33226001472` — `success`
- Windows Installer Pack Smoke — run `33226001471` — `success`

The dedicated Recovery V3 smoke ran on a direct `push` event and its Windows PowerShell 5.1 job passed:

- parser/syntax validation;
- real harness-owned `-ContractSelfTest`;
- existing recovery harness schema/safety-contract assertions.

Validate completed all seven jobs successfully, including Windows Python 3.11 and 3.14 matrix jobs and the package dry-run proof job.

## Exact-SHA package proof

Fresh Validate artifact:

- Artifact ID: `9706878201`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- GitHub artifact digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- Package version: `0.9.3`
- Source commit recorded in `PACKAGE_IDENTITY.json`: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- Payload file count: `178`
- Payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `cogentnexus-openclaw-v0.9.3.tar.gz` SHA256: `9a4634e41d21271b92d0c6ce69f4931bca11455808a9e1b8567e48db85bb432d`
- `cogentnexus-openclaw-v0.9.3.zip` SHA256: `526ca264db77b960d2d81d3f6cf7c100e8c45f2d6243eaab00801da9ee293c3e`

The downloaded artifact was independently inspected and its outer SHA256 matched the GitHub artifact digest; `PACKAGE_IDENTITY.json` matched the exact candidate, payload count, fingerprint, and both archive hashes above.

## Safety boundary

Task 127 performed **no live Windows lifecycle or recovery acceptance operation**:

- no provider crash injection;
- no recovery-suite execution;
- no install/install-over/reset/uninstall/reinstall;
- no standalone stop/start/restart;
- no provider/OpenClaw configuration mutation;
- no process kill or reboot;
- no manual cleanup/normalization;
- no credential/secret access;
- no Dashboard semantic Send;
- no merge/tag/release/force push.

The repaired exact candidate may advance only after independent review to a separately authorized real-Windows recovery re-acceptance task.