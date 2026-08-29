# CNX-20260829-127 — Recovery Harness Fail-Closed Contract and CI Proof

## Verdict

**PASS — the recovery harness now executes its durable-convergence predicate through a real non-disruptive PowerShell self-test, with fail-closed warning semantics and a Windows PowerShell 5.1 CI step. No live lifecycle, provider mutation, or recovery replay was performed.**

## Scope and fences

This task was limited to repository source, tests, workflow, and CI proof. No install, install-over, reset, uninstall, reinstall, stop, start, restart, provider reconfiguration, process kill, live crash injection, cleanup, or recovery replay was performed.

The retained Task-125 evidence remained read-only input. The Task-126 candidate was used as the starting point:

- starting commit: `4d0f7c30fbb6412945a7c0d44b15e1b583cc7461`
- branch: `agent/v0.9.3-full-stabilization`

## RED

Added a Python test that invokes the real PowerShell harness with `-ContractSelfTest`. Before the implementation, the harness rejected the new parameter with `NamedParameterNotFound`. This established a behavioral RED against the actual entrypoint rather than a source-text assertion.

## Repair

The harness now contains:

- `Test-DurableConvergenceObservation`, the single responsibility-local predicate used by `Wait-DurableConvergence`;
- `Invoke-ContractSelfTest`, a non-disruptive entrypoint invoked by `-ContractSelfTest`;
- recovery-check observations preserved in each convergence observation so the predicate can distinguish the permitted incident-scoped warning from unrelated warnings.

The predicate remains fail-closed:

- ordinary convergence requires exact `READY`;
- incident-scoped `READY_WITH_WARNINGS` is accepted only when provider incident convergence is explicitly required;
- exactly one provider event-adapter row is required with `details.expected=false`;
- exactly one provider incident is required for incident-scoped warning acceptance;
- the incident must be `WARN`, open, and have `circuitOpen=false`;
- any additional warning, failure, indeterminate check, missing/duplicate adapter, missing/duplicate incident, or open circuit rejects convergence;
- managed mode, selected provider `ollama`, Gateway listener, and Ollama listener remain required.

The provider recovery policy was not weakened, and listener/process health was not treated as stable model success.

## Behavioral cases

The harness self-test exercises 12 cases:

1. retained incident-scoped warning accepted;
2. ordinary warning rejected without incident requirement;
3. extra maintenance warning rejected;
4. extra supervisor warning rejected;
5. extra adapter warning rejected;
6. closed/non-warning incident rejected;
7. open circuit rejected;
8. exact `READY` accepted;
9. missing incident rejected;
10. duplicate incident rejected;
11. missing adapter rejected;
12. duplicate adapter rejected.

## CI proof

Updated `.github/workflows/v093-ollama-recovery-v3-smoke.yml` to:

- trigger on the harness, its behavioral contract test, or the workflow itself;
- run `-ContractSelfTest` under Windows PowerShell 5.1 after parser/syntax validation;
- retain the existing static safety contract checks.

## Validation

Local results:

- actual PowerShell self-test: `v0.9.3 Ollama recovery convergence contract self-test: PASS`;
- focused Python contract test: `1 passed`;
- full Python suite: `485 passed, 3 skipped, 4 subtests passed`;
- PowerShell `-SyntaxOnly`: PASS;
- `python -m compileall -q skills scripts tests`: PASS;
- `sh -n scripts/install.sh`: PASS;
- `git diff --check`: PASS;
- workflow YAML parse: PASS;
- plugin tests: `50` files and `268` tests passed;
- plugin validation: PASS, packed file count `178`;
- plugin evaluation: `passed: true`.

No live Windows acceptance was claimed by this task.
