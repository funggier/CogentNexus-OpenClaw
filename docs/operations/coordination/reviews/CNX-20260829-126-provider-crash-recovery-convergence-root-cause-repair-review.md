# Independent Review — CNX-20260829-126

## Verdict

**REJECTED CANDIDATE ADVANCEMENT — ROOT-CAUSE CLASSIFICATION IS ACCEPTED, BUT THE HARNESS REPAIR IS NOT YET FAIL-CLOSED OR BEHAVIORALLY PROVEN, AND THE AFFECTED RECOVERY-SPECIFIC SMOKE DID NOT RUN ON THE EXACT CANDIDATE SHA.**

## Accepted findings

Task-126 report:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

Report commit:

`ae75520bb075a32562ce78c10e9ce408906b6ea4`

The retained Task-125 evidence analysis is accepted for root-cause classification:

- `converge-provider-after` contained 90 observations across 420.652 seconds;
- host mode remained `managed`;
- host and provider selection remained `ollama`;
- Gateway and Ollama listeners remained present during the convergence series;
- provider-event adapter remained coherent with `expected=false`;
- exactly one provider recovery incident remained open with `circuitOpen=false` and one successful automatic recovery attempt;
- recovery verdict remained `READY_WITH_WARNINGS` throughout;
- the only reported unsatisfied reviewed predicate was exact `recoveryVerdict == READY`;
- the incident is intentionally not closed by process/listener recovery alone; stable model success or a verified operator transition closes it.

Therefore the deepest proven Task-125 failure is accepted as an **acceptance-harness contract mismatch**, not a provider process-recovery failure. Provider recovery policy must remain unchanged; listener/process health must not be promoted to stable model-success evidence.

## Candidate reviewed

Task 126 proposed:

`69a3efa1feb7711f22c83055a8571035240ec81c`

The reported exact-SHA workflows are independently confirmed successful:

- Validate `33223319908` — success;
- Windows Installer Pack Smoke `33223319175` — success;
- PS5.1 Acceptance Smoke `33223319261` — success.

However, these successes are insufficient for candidate advancement for the reasons below.

## Blocking finding 1 — RED does not execute the real harness contract

Task 126 required that a harness defect be reproduced by a focused RED test demonstrating that the actual harness rejects a state the product contract defines as recovered.

The added `tests/test_recovery_harness_contract.py` does not do that.

Its first test evaluates a test-local Python helper `_provider_recovery_converged()` that duplicates the desired predicate. That helper is not production or harness code and therefore cannot prove the PowerShell harness behavior.

Its second test reads the PowerShell source as text and asserts that a literal expression exists. The reported RED was therefore a source-text absence, not execution of `Wait-DurableConvergence` against the retained recovered/open-incident state.

This violates the Task-126 requirement that the regression assert the real state-transition/postcondition rather than merely grep source text.

A successor must execute the actual PowerShell convergence predicate or an extracted production/harness-owned pure predicate used by `Wait-DurableConvergence`, with the retained Task-125 observation shape as input.

## Blocking finding 2 — `READY_WITH_WARNINGS` acceptance is too broad

Final candidate `69a3efa...` changes the convergence predicate to accept `READY_WITH_WARNINGS` whenever `$RequireProviderIncident` is true.

That is broader than the retained evidence and broader than the intended repair.

The current predicate verifies that a Provider recovery incident row exists and `circuitOpen=false`, but it does not require all of the following before allowing `READY_WITH_WARNINGS`:

- the incident row itself is `WARN`;
- `details.incidentOpen == true`;
- the incident warning is the **only** warning in the recovery component;
- no unrelated maintenance, supervisor-health, adapter, or other recovery warning is being masked.

Consequently a future provider-crash run could return `READY_WITH_WARNINGS` for a different warning while the incident row merely exists with a closed circuit, and the harness could incorrectly declare convergence.

The repair must be fail-closed:

- ordinary/gateway/operator convergence remains exact `READY`;
- provider-crash may accept `READY_WITH_WARNINGS` only when the sole warning is exactly `Provider recovery incident`, that row represents the expected open/circuit-closed recovered incident, and all other recovery checks are PASS;
- exact `READY` remains valid when the incident has already closed normally.

## Blocking finding 3 — affected recovery-specific smoke did not run

The modified file is:

`scripts/test-v093-ollama-recovery-windows-v3.ps1`

Its dedicated workflow is:

`.github/workflows/v093-ollama-recovery-v3-smoke.yml`

That workflow currently triggers on `pull_request` paths and `workflow_dispatch`, but not on branch `push`.

GitHub reports only three workflow runs on exact candidate `69a3efa...`: Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke. The dedicated `PS5.1 v0.9.3 Ollama Recovery V3 Smoke` did not run on the candidate SHA.

Because Task 126 explicitly required any recovery-specific smoke affected by the change, exact-SHA CI proof is incomplete.

A successor should make this smoke part of the direct-push candidate gate (preferably by adding an appropriate `push` path trigger) or otherwise produce unambiguous exact-candidate execution evidence under the repository's coordination model.

## What remains accepted

The following Task-126 conclusions are retained and do not need to be rediscovered from scratch:

- do not weaken provider recovery policy;
- do not close an incident merely because Ollama listener/process health returned;
- Task-125 live recovery suite remains consumed and must not be replayed during repository repair;
- Task-126 performed no prohibited live lifecycle/recovery mutation;
- provider-crash warning-state acceptance belongs in the acceptance harness layer, but must be narrowly fail-closed and behaviorally tested.

## Required successor

Open a repository-only TDD task that:

1. writes a real behavioral RED against the harness-owned convergence predicate using the retained Task-125 observation shape;
2. proves ordinary/gateway convergence rejects unrelated `READY_WITH_WARNINGS`;
3. proves provider-crash convergence accepts `READY_WITH_WARNINGS` only for the sole expected open/circuit-closed provider-incident warning;
4. proves provider-crash convergence rejects warning states containing any additional/unrelated WARN;
5. applies the smallest harness-only repair;
6. ensures the recovery-v3 smoke runs on the exact direct-push candidate SHA;
7. reruns focused/full validation, exact-SHA CI, and package proof;
8. publishes a new candidate and stops for independent review.

## Live-operation fence

No live recovery replay, provider crash, install/reset/uninstall/reinstall, stop/start/restart, Dashboard semantic Send, provider/OpenClaw mutation, process kill, reboot, or manual normalization is authorized by this review.

The final Dashboard durable-delivery acceptance remains prohibited.
