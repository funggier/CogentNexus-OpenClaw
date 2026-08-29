# CNX-20260829-127 — Recovery Harness Fail-Closed Contract and Exact-SHA CI Proof

- Status: `READY_FOR_HERMES`
- Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the remaining Task-126 review defects in the v0.9.3 Windows recovery-reality acceptance harness without changing provider recovery policy or replaying any live recovery/lifecycle action.

Task-126 root-cause classification is retained:

- Task-125 provider process recovery was coherent;
- the retained 420-second series stayed `READY_WITH_WARNINGS` because the recovered provider incident intentionally remained open pending stable model-success evidence;
- the acceptance harness, not provider recovery policy, owned the mismatch.

Task-126 candidate `69a3efa1feb7711f22c83055a8571035240ec81c` is **not accepted for advancement** because its regression test does not execute the real harness contract, its warning acceptance is broader than the evidence, and the affected recovery-specific smoke did not run on the exact candidate SHA.

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair-review.md`

## Accepted evidence — do not rediscover or weaken

Retain these proven facts from Task 126:

- 90 provider-convergence observations across 420.652 seconds;
- mode `managed` throughout;
- host selected provider `ollama` throughout;
- provider selected provider `ollama` throughout;
- recovery verdict `READY_WITH_WARNINGS` throughout;
- Gateway listener present throughout;
- Ollama listener present throughout;
- one Provider event adapter row with `status=PASS`, `details.expected=false` throughout;
- one Provider recovery incident row with `status=WARN`, `incidentOpen=true`, `circuitOpen=false`, incident `ollama:1`, `recoveryAttempts=1` throughout;
- the automatic recovery attempt recorded `success=true`;
- no stable model completion occurred before convergence polling;
- provider recovery policy intentionally closes the incident only on stable model success or a verified operator transition.

Do **not** change `provider_recovery_v092.py` to equate listener/process health with stable success.

## Blocking defects to repair

### 1. Behavioral RED fidelity

The existing `tests/test_recovery_harness_contract.py` is insufficient because:

- `_provider_recovery_converged()` is test-local duplicated logic, not harness behavior;
- the second test only greps PowerShell source text.

Task 127 must test harness-owned executable logic.

Preferred design:

- extract the convergence decision into a harness-owned pure PowerShell function used by `Wait-DurableConvergence`, for example `Test-DurableConvergenceObservation` (name may differ);
- add a non-disruptive self-test entrypoint or another deterministic invocation surface that executes that exact function with synthetic observation/check documents;
- the Python/PowerShell regression must invoke the actual harness-owned predicate, not a duplicate implementation and not a source-text assertion.

TDD order is mandatory:

1. add focused regression first;
2. run it against the pre-repair harness and capture RED for the expected behavioral reason;
3. only then modify production/harness code;
4. rerun to GREEN.

### 2. Fail-closed warning semantics

Provider-crash convergence may accept `READY_WITH_WARNINGS` **only** for the exact retained state class.

Required semantics:

- common structural predicates still hold:
  - mode `managed`;
  - host selected provider `ollama`;
  - provider selected provider `ollama`;
  - one Provider event adapter row with `details.expected == false`;
  - Gateway listener present;
  - Ollama listener present;
  - exactly one Provider recovery incident row;
- exact `READY` remains acceptable normally;
- `READY_WITH_WARNINGS` is acceptable only when `RequireProviderIncident == true` **and**:
  - Provider recovery incident row has `status == WARN`;
  - `details.incidentOpen == true`;
  - `details.circuitOpen == false`;
  - that provider-incident row is the **only WARN** in the recovery component;
  - every other recovery check row is `PASS`;
  - no `FAIL` or `INDETERMINATE` row is present.

Fail closed on all other warning combinations.

Required focused cases at minimum:

1. provider-crash retained state: sole open/circuit-closed incident WARN + otherwise PASS -> accepted;
2. same state under ordinary/gateway convergence (`RequireProviderIncident=false`) -> rejected;
3. provider incident WARN plus Maintenance/recovery fence WARN -> rejected;
4. provider incident WARN plus Supervisor health snapshot WARN -> rejected;
5. provider incident WARN plus adapter WARN -> rejected;
6. incident row PASS/closed while another WARN exists -> rejected as warning convergence;
7. incident circuit open -> rejected;
8. exact READY with coherent predicates -> accepted;
9. missing/duplicate incident row when required -> rejected;
10. missing/duplicate adapter row -> rejected.

Do not make `READY_WITH_WARNINGS` a generic success class.

### 3. Recovery-specific exact-SHA CI

The affected workflow is:

`.github/workflows/v093-ollama-recovery-v3-smoke.yml`

At Task-126 candidate `69a3efa...`, it did not run because it is currently only `pull_request` + `workflow_dispatch`.

Task 127 must produce unambiguous exact-SHA execution of this smoke for the final candidate.

Preferred repository-local repair:

- add a `push` path trigger for:
  - `scripts/test-v093-ollama-recovery-windows-v3.ps1`;
  - `.github/workflows/v093-ollama-recovery-v3-smoke.yml`;
  - the focused harness-contract regression surface if relevant.

The final exact candidate must show a successful `PS5.1 v0.9.3 Ollama Recovery V3 Smoke` run in addition to the established exact-SHA workflows.

The smoke itself must execute the harness-owned non-disruptive contract self-test, not only parse/grep source, so CI proves the actual convergence decision logic.

## Phase A — fresh repository fence

Before edits:

- fetch branch HEAD and coordination files;
- confirm Task 127 is authoritative and not superseded;
- inspect Task-126 report/review and current candidate;
- preserve all live one-shot ledgers;
- no live Windows lifecycle/recovery command is authorized.

## Phase B — TDD RED

Create the smallest focused test that invokes the real harness-owned convergence predicate/self-test.

RED must fail against the current Task-126 harness for the exact missing fail-closed behavior, not due syntax, missing files, or a test-local duplicate.

Capture:

- RED commit SHA;
- exact command;
- exact failing assertion/output.

No harness production modification before RED is observed.

## Phase C — minimal harness repair

Apply only the minimal responsibility-local change needed to:

- expose/use one harness-owned convergence predicate;
- encode the fail-closed warning rules above;
- keep `Wait-DurableConvergence` using that predicate;
- provide a non-disruptive contract self-test path if needed by local/CI tests.

Do not modify provider recovery semantics, installer behavior, OpenClaw runtime policy, provider model/endpoint/config, or unrelated lifecycle code.

## Phase D — workflow proof repair

Ensure `.github/workflows/v093-ollama-recovery-v3-smoke.yml` runs for direct-push candidate changes and executes the real non-disruptive convergence contract tests/self-test.

Do not add any disruptive recovery invocation to GitHub Actions.

## Phase E — validation

At minimum require:

- focused harness behavioral regression GREEN;
- PowerShell syntax/AST parse on Windows PowerShell 5.1;
- harness `-SyntaxOnly` or equivalent load proof;
- harness-owned convergence contract self-test GREEN;
- full Python suite;
- provider/recovery/check focused tests;
- plugin tests;
- plugin/package validation;
- evaluation suite;
- `python -m compileall` for modified Python;
- `git diff --check`;
- applicable shell syntax checks;
- npm audit under repository contract.

## Phase F — exact-SHA CI and package proof

Final candidate must have successful exact-SHA runs for at least:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke;
- **PS5.1 v0.9.3 Ollama Recovery V3 Smoke**.

Record all run IDs and conclusions.

Produce fresh package proof and record:

- exact source SHA;
- artifact ID/name/digest;
- ZIP SHA256;
- tar.gz SHA256;
- payload count;
- payload/plugin fingerprint.

If any required workflow or package proof is missing: `BLOCKED`, not candidate-ready.

## Phase G — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`

Report must include:

- Task-126 review findings addressed one by one;
- RED commit/output proving actual harness behavior;
- final harness predicate semantics;
- focused negative/positive case results;
- changed files/commits;
- full validation results;
- exact candidate SHA;
- all four required exact-SHA workflow runs;
- package proof;
- explicit statement that no live lifecycle/recovery replay occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`.

Then stop for independent ChatGPT review. Do not open a live acceptance task automatically.

## Hard fence

Task 127 does **not** authorize:

- live provider crash injection;
- recovery-suite replay;
- install/install-over/reset/uninstall/reinstall;
- standalone stop/start/restart;
- provider/OpenClaw live configuration mutation;
- provider/model/endpoint/timeout changes;
- process kill/reboot;
- manual Windows cleanup/normalization;
- credentials/secrets;
- Dashboard semantic Send;
- merge/tag/release;
- force push.

All previously consumed lifecycle/recovery operations remain consumed.
