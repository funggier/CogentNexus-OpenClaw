# Independent Review — CNX-20260829-127

## Verdict

**ACCEPTED PASS — RECOVERY HARNESS CONTRACT IS BEHAVIORALLY EXERCISED THROUGH THE REAL POWERSHELL ENTRYPOINT, THE PROVIDER-WARNING EXCEPTION IS FAIL-CLOSED, THE DEDICATED RECOVERY V3 SMOKE PASSES ON THE EXACT CANDIDATE SHA, AND THE REPAIRED CANDIDATE MAY ADVANCE TO A NEW, SEPARATELY AUTHORIZED REAL-WINDOWS RECOVERY ACCEPTANCE.**

## Accepted candidate

Exact source candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Candidate commit:

`ci: run recovery v3 smoke on exact push sha`

Task-127 final report:

`docs/operations/coordination/reports/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`

Report-only commit after the candidate:

`974b74877293630c603cd1b068e36d013ec49792`

A direct compare from candidate to report commit shows only the Task-127 report changed; no source, test, workflow, runtime, package, or candidate content drifted after exact-SHA validation.

## Root-cause boundary retained

Task 126 correctly established from Task-125 retained evidence that the old provider-crash acceptance failure was a harness-contract mismatch, not a provider-recovery engine failure:

- Gateway and Ollama listeners had recovered;
- provider selection remained coherent;
- the provider recovery attempt succeeded;
- the single provider incident intentionally remained open and circuit-closed pending stable model-success evidence;
- `check recovery` therefore correctly returned `READY_WITH_WARNINGS`;
- the old harness incorrectly required exact `READY` during that incident-scoped provider convergence state.

Task 127 preserves that product safety invariant. It does not equate listener/process health with stable model success and does not close the durable incident prematurely.

## Behavioral-proof review

The Task-126 review defect is repaired:

- the Python regression invokes the actual PowerShell harness with `-ContractSelfTest`;
- the pre-implementation entrypoint failed with `NamedParameterNotFound`, providing a real behavioral RED;
- the actual harness now owns `Test-DurableConvergenceObservation`;
- `Wait-DurableConvergence` calls that same predicate rather than a duplicated test implementation;
- the dedicated Windows workflow executes the real non-disruptive harness-owned self-test under Windows PowerShell 5.1.

The exceptional warning path is fail-closed:

- ordinary convergence remains strict `READY`;
- `READY_WITH_WARNINGS` is considered only when provider-incident convergence is explicitly required;
- exactly one provider incident must exist;
- that incident must be the sole WARN row, must remain open, and must have a closed circuit;
- every other recovery check must be PASS;
- any FAIL/INDETERMINATE row rejects convergence;
- structural host/provider/listener/adapter requirements remain mandatory;
- missing or duplicate incident/adapter evidence rejects convergence.

## Focused self-test note

The synthetic self-test cases for supervisor-warning and adapter-warning currently also inherit the helper's maintenance-warning mutation, so those two named cases are not perfectly isolated fixtures. This is a test-quality imperfection, not a functional acceptance gap: the production predicate independently enforces `warns.Count == 1` and requires the sole warning to be `Provider recovery incident`, so any additional supervisor, adapter, maintenance, or other warning is rejected.

The synthetic exact-READY fixture also retains the default open incident row. In real `check recovery` composition an open WARN incident would prevent a `READY` aggregate verdict. The READY branch remains acceptable for the reviewed harness because ordinary structural readiness is still strict, while provider warning acceptance is controlled separately by the fail-closed warning branch. These fixture-shape issues do not justify source drift or another candidate cycle before live re-acceptance.

## Exact-SHA CI

All required workflows passed on exact candidate `1b922bf400fdbccb1f9c7019b89b69fd67f44070`:

- Validate — run `33226001453` — `success`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke — run `33226001456` — `success`
- PS5.1 Acceptance Smoke — run `33226001472` — `success`
- Windows Installer Pack Smoke — run `33226001471` — `success`

The dedicated Recovery V3 smoke was triggered by a direct push on the exact candidate SHA and passed parser/syntax validation, the real `-ContractSelfTest`, and the established harness schema/safety checks.

Validate completed all seven jobs successfully, including Windows Python 3.11 and 3.14.

## Exact-SHA package proof

Artifact:

- ID `9706878201`
- name `cogentnexus-openclaw-v0.9.3-package-proof-1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- GitHub artifact digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`

`PACKAGE_IDENTITY.json` independently inspected from the downloaded artifact records:

- source commit `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- package version `0.9.3`
- payload count `178`
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256 `9a4634e41d21271b92d0c6ce69f4931bca11455808a9e1b8567e48db85bb432d`
- ZIP SHA256 `526ca264db77b960d2d81d3f6cf7c100e8c45f2d6243eaab00801da9ee293c3e`

The downloaded artifact outer SHA256 matched the GitHub artifact digest.

## Safety review

Task 127 and the owner-side CI trigger correction performed no live runtime mutation:

- no recovery-suite execution;
- no live crash injection;
- no install/install-over/reset/uninstall/reinstall;
- no standalone stop/start/restart;
- no provider/OpenClaw configuration mutation;
- no process kill or reboot;
- no manual cleanup;
- no secrets/credentials;
- no Dashboard semantic Send;
- no merge/tag/release/force push.

## Advancement decision

The repository/source/CI/package gate is accepted for exact candidate `1b922bf400fdbccb1f9c7019b89b69fd67f44070`.

A new task may now authorize **one new real-Windows recovery acceptance execution** against this repaired candidate. Earlier Task-121/124 lifecycle operations and the Task-125 recovery suite remain consumed and must not be replayed under their old authorizations.

The successor must be narrowly scoped to recovery re-acceptance, preserve the existing installed runtime/provider state, use a true interactive PowerShell console for the exact harness confirmation, and remain fail-stop/no-rerun. Final Dashboard durable-delivery acceptance remains prohibited until that live recovery re-acceptance passes and is independently reviewed.