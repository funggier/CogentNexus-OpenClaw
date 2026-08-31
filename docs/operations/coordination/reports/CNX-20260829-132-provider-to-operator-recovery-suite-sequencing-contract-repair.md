# CNX-20260829-132 — Provider-to-Operator Recovery Suite Sequencing Contract Repair

## Verdict

**PASS — repository/source TDD repair complete.** The recovery harness now carries the exact accepted provider incident from a directly preceding provider-crash PASS into the operator-before boundary, while preserving strict standalone and post-operator-start `READY` semantics. Exact-SHA CI and fresh package proof passed. No live recovery, lifecycle, provider, model, configuration, or runtime operation was performed under Task 132.

## Task-131 diagnosis

Task 131 used the corrected authoritative root and proved:

- baseline: PASS;
- gateway-crash: PASS;
- provider-crash: PASS under the reviewed fail-closed exception;
- provider listener recovered with a different PID;
- recovery remained `READY_WITH_WARNINGS` because one open, circuit-closed `ollama` provider incident remained intentionally active;
- operator-stop failed before its scenario because `Assert-Baseline 'operator-before'` required exact `READY` with no awareness of the immediately preceding accepted provider-crash state.

The product policy was not the repair target. `provider_recovery_v092.py` semantics remain unchanged: automatic restart success does not close an incident; stable model success or verified manual transition closes it. Listener health is not treated as model-success evidence.

## TDD RED

A tests-only change was made first in:

- `tests/test_recovery_harness_contract.py`

The new test invokes the real Windows PowerShell harness entrypoint with `-ContractSelfTest` and requires the provider-to-operator sequence case. Before harness modification, the focused run produced the expected behavioral RED:

```text
1 failed, 1 passed in 1.18s
AssertionError: assert 'provider-to-operator-carried-incident' in result.stdout
```

The initial environment attempt without project dependencies also recorded `No module named pytest`; the test was then run with the documented ephemeral `uv run --no-project --with pytest` environment. RED test-only commit:

`d7a8c02296cd29a924cc298f4fc196f20c51b4c4`

## Minimal repair

Modified only:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- `tests/test_recovery_harness_contract.py`

Repair behavior:

1. `Scenario-Provider` stores the exact accepted incident ID/classification only after provider convergence PASS.
2. `Scenario-OperatorStop` passes that carried record only when the immediately preceding scenario in the same process was `provider-crash`.
3. `Test-OperatorBoundaryObservation` requires the carried identity and the existing fail-closed provider-warning predicate, plus exact `READY_WITH_WARNINGS`, one WARN incident, open incident, closed circuit, matching classification where available, healthy managed/Ollama/listener structure, and all other checks PASS.
4. Standalone operator-stop has no carried expectation and remains strict `READY`.
5. The carried expectation is cleared when consumed and cannot leak into post-start convergence.
6. Post-operator-start calls the existing strict `Wait-DurableConvergence` path with no provider-incident allowance.
7. No artificial model completion or normalization was introduced.

## Behavioral GREEN and negative cases

Real PowerShell harness self-test output:

```text
provider-to-operator-carried-incident: PASS
v0.9.3 Ollama recovery convergence contract self-test: PASS
```

Focused repository test:

```text
2 passed in 1.16s
```

The self-test covers the existing strict/incident matrix plus sequence-specific cases:

- exact carried incident after provider-crash: accepted;
- standalone same open incident: rejected;
- different incident ID: rejected;
- missing incident: rejected;
- extra warning: rejected;
- `READY` with carried exception instead of `READY_WITH_WARNINGS`: rejected;
- existing cases for ordinary warnings, maintenance/supervisor/adapter warnings, closed incident, circuit-open, exact READY, duplicate/missing incident, and duplicate/missing adapter remain covered.

## Validation

- PowerShell syntax/load: PASS
- PowerShell `-ContractSelfTest`: PASS
- focused recovery harness contract tests: `2 passed`
- full Python suite: `486 passed, 3 skipped, 4 subtests passed`
- `python -m compileall -q .`: PASS
- `bash -n scripts/install.sh`: PASS
- `git diff --check`: PASS
- plugin tests: `50 files passed, 268 tests passed`
- plugin validation: PASS; packed file count `178`
- evaluation: PASS; `passed=true`; database integrity `ok`

`npm audit --audit-level=high` was executed and returned exit `1` for 4 high transitive findings in `tar` and `undici` through the pinned `openclaw` dependency. The suggested `npm audit fix --force` would install `openclaw@0.0.1` and introduce a breaking change, so it was not run. No dependency or unrelated package change was made. This is recorded as a pre-existing dependency audit finding, not hidden or converted into a false PASS.

A first package-proof capture used `/tmp`, which is not visible to native Windows Python; this was an executor path-boundary issue. The package proof was then regenerated and downloaded from the exact Validate run successfully.

## Exact candidate and CI proof

Final candidate source SHA:

`b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

Local and remote branch HEAD matched this SHA. Exact repaired harness blob:

`8158e4f227e0eafb5c08e89d5f12564e421d460b`

Exact-SHA workflows, all completed with conclusion `success`:

- Validate: `33234315933`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke: `33234315938`
- PS5.1 Acceptance Smoke: `33234315948`
- Windows Installer Pack Smoke: `33234315959`

The Recovery V3 Smoke executed the real non-disruptive PowerShell `-ContractSelfTest` on the exact candidate SHA; it was not a grep-only proof.

Fresh exact package proof from artifact:

- artifact ID: `9709442638`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-b7074c8cb5b10c77624cfe7b5223e3bae338c80d`
- package digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- package version: `0.9.3`
- payload count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `0b510eb4b5380483c58b0207b94551a32d6e1a98407d7c79e995787cc7768c9b`
- ZIP SHA256: `0f22081734b67e6e724a6067a19cd1ba1016983eab0c4aa21643fb35e6c091be`

## Safety and live-operation ledger

- live recovery suite: `0`
- gateway/provider crash injection: `0`
- live operator-stop: `0`
- install/install-over/reset/uninstall/reinstall: `0`
- live start/stop/restart/enable/disable: `0`
- provider/model/OpenClaw/config mutation: `0`
- process kill/task-service mutation: `0`
- cleanup/normalization/reboot: `0`
- Dashboard semantic Send: **not performed**

Task 131's consumed live ledger remains unchanged. Task 132 produced no live acceptance claim and did not open a successor live task.

## Completion

Task 132 report publication is the only remaining repository mutation. After publication, stop for independent ChatGPT review. Do not automatically create or run a live recovery acceptance task.
