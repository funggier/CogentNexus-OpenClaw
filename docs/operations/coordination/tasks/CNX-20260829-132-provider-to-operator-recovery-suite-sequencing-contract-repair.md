# CNX-20260829-132 — Provider-to-Operator Recovery Suite Sequencing Contract Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the remaining recovery-v3 acceptance-harness sequencing defect proven by Task 131.

Task 131 established on real Windows that:

- authoritative-root preflight PASSed;
- baseline PASSed;
- gateway-crash PASSed;
- provider-crash PASSed under the Task-127 fail-closed provider-incident contract;
- provider recovery reached the accepted idle-crash state quickly with an open, circuit-closed provider incident and `READY_WITH_WARNINGS`;
- the suite then failed **before** operator-stop because `Scenario-OperatorStop` immediately called strict `Assert-Baseline 'operator-before'`, which requires recovery verdict `READY`;
- no stable model completion or verified manual transition occurred between provider-crash PASS and operator-before;
- provider policy deliberately does not close an incident merely because the provider listener/process restarted.

This task repairs the harness sequencing contract only. It must not weaken provider recovery policy or perform any live recovery/lifecycle operation.

## Authoritative Task-131 result

Task-131 report:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Task-131 independent review:

`docs/operations/coordination/reviews/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root-review.md`

Review verdict:

`ACCEPTED FAIL — AUTHORITATIVE-ROOT PREFLIGHT PASSED, GATEWAY-CRASH RECOVERY PASSED, AND PROVIDER-CRASH RECOVERY PASSED UNDER THE REPAIRED FAIL-CLOSED INCIDENT CONTRACT; FULL-SUITE ACCEPTANCE FAILED BEFORE OPERATOR-STOP BECAUSE THE HARNESS REQUIRES STRICT READY AT operator-before EVEN THOUGH ITS IMMEDIATELY PRECEDING PROVIDER-CRASH CONTRACT INTENTIONALLY PERMITS THE SAME OPEN, CIRCUIT-CLOSED PROVIDER INCIDENT TO REMAIN READY_WITH_WARNINGS. THIS IS A HARNESS SCENARIO-SEQUENCING DEFECT, NOT A NEW PROVIDER-RECOVERY PRODUCT FAILURE. OPERATOR-STOP REMAINS UNPROVEN.`

Task-131 live evidence retained:

- preflight root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx131-recovery-20260829T093000Z`
- harness text: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-111830.txt`
- harness JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-111830.json`

Task-131 one-shot ledger is consumed and must never be replayed under Task 132:

- suite `1 / 1`;
- confirmation `1 / 1`;
- baseline PASS;
- gateway-crash PASS;
- provider-crash PASS;
- operator-stop `0`, not reached;
- reruns `0`.

## Current accepted repository baseline

Task-127 accepted candidate used by Task 131:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Current recovery harness at that accepted candidate:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Existing behavioral contract test:

`tests/test_recovery_harness_contract.py`

Dedicated workflow:

`.github/workflows/v093-ollama-recovery-v3-smoke.yml`

Task 132 will produce a new candidate; do not continue treating `1b922bf...` as the final live candidate after a harness repair.

## Proven product-policy invariant — do not weaken

`skills/cogentnexus-openclaw/scripts/provider_recovery_v092.py` is authoritative for incident lifetime semantics:

- an explicit provider failure opens an incident;
- successful automatic recovery attempt does **not** itself close the incident;
- stable model completion closes through `record_stable_success(..., reason=stable_success)`;
- verified manual provider transition closes through `clear_after_manual_transition(..., reason=verified_manual_transition)`;
- elapsed time/listener health alone does not prove stable model success.

Task 132 must preserve this distinction.

Do **not** make provider listener/process recovery equivalent to stable model completion merely to make the acceptance suite pass.

## Exact sequencing defect

Current harness behavior:

1. `Scenario-Provider` begins from strict baseline.
2. It injects one exact Ollama listener crash.
3. It observes a different Ollama listener PID.
4. `Wait-DurableConvergence 'converge-provider-after' $true` permits only:
   - managed/Ollama structural health;
   - healthy Gateway/Ollama listeners;
   - provider event adapter PASS/expected=false;
   - either exact `READY`, or `READY_WITH_WARNINGS` where the **only** WARN is one open, circuit-closed `Provider recovery incident` and every other check is PASS.
5. Task 131 reached that accepted `READY_WITH_WARNINGS` state and `scenario-provider-crash` PASSed.
6. `Scenario-OperatorStop` immediately executes `Assert-Baseline 'operator-before'`.
7. `Assert-Baseline` requires recovery verdict exact `READY` and has no same-suite expected-incident allowance.
8. No allowed incident-closing evidence occurs between steps 5 and 6.

Thus the exact `all` sequence can reject a state it just accepted, before operator-stop is exercised.

## Required repair semantics

Make the operator-stop precondition sequence-aware and fail-closed.

### Standalone operator-stop

If `operator-stop` is selected without a directly preceding provider-crash PASS in the same harness process, retain current strict baseline semantics:

- mode `managed`;
- selected provider `ollama` at host/provider views;
- recovery exact `READY`;
- provider event adapter exactly one row with `expected=false`;
- Gateway listener healthy;
- Ollama listener healthy.

An arbitrary pre-existing `READY_WITH_WARNINGS` provider incident must **not** be accepted for standalone operator-stop.

### Same-suite provider-crash → operator-stop

If and only if operator-stop directly follows a provider-crash scenario that PASSed in this same harness process with the accepted intentional-open-incident state, the `operator-before` precondition may accept that exact expected incident.

The allowance must be bound to the prior provider-crash evidence, preferably by carrying the exact accepted provider incident identity/state from `Scenario-Provider` into `Scenario-OperatorStop` rather than re-inferring a generic warning exception.

At minimum require all of the following simultaneously:

- same harness process/run;
- immediately preceding provider-crash scenario recorded PASS;
- expected incident ID is non-empty and exactly equals the current single `Provider recovery incident` ID;
- incident status `WARN`;
- `incidentOpen=true`;
- `circuitOpen=false`;
- provider `ollama` / classification consistent with the preceding accepted provider incident where those fields are available;
- recovery verdict exactly `READY_WITH_WARNINGS` for this exceptional boundary;
- exactly one WARN total and it is `Provider recovery incident`;
- no FAIL/INDETERMINATE checks;
- every other recovery check PASS;
- exactly one Provider event adapter row with `expected=false`;
- host mode `managed`;
- host selected provider `ollama`;
- provider status selected provider `ollama`;
- Gateway listener healthy;
- Ollama listener healthy.

Reject:

- missing expected incident identity;
- different incident ID/generation;
- duplicate incident rows;
- closed/PASS incident paired with `READY_WITH_WARNINGS`;
- circuit-open incident;
- extra WARN of any kind;
- FAIL/INDETERMINATE check;
- missing/duplicate/expected=true adapter;
- listener loss;
- provider mismatch;
- non-managed mode;
- stale incident not proven to be the exact one accepted by the immediately preceding provider-crash scenario.

### Operator lifecycle after the precondition

Do not add an artificial model completion or a separate normalization command before operator-stop.

Once the sequence-aware precondition passes:

- run only the existing harness-owned `cnxclaw stop`;
- verify maintenance/stopped desired state;
- verify Gateway stays stopped for the observation period;
- run only the existing harness-owned `start-after-intentional-stop`;
- require Gateway/Ollama listeners return;
- require strict ordinary `READY` durable convergence after start.

The verified manual `start` transition may naturally close the prior provider incident under existing product policy. The post-start gate must not use the provider-warning exception.

## Phase A — authority / evidence reconciliation

Before edits:

1. Fresh-fetch branch HEAD, `ACTIVE.md`, and `STATUS.md`.
2. Confirm Task 132 remains authoritative and unsuperseded.
3. Read Task-131 report/review and the current harness/test/workflow.
4. Preserve all historical one-shot ledgers.
5. Do not access or mutate the live Windows runtime. Retained Task-131 evidence may be read-only consulted if available to the executor, but the repository report/review already establishes the required failing boundary.

## Phase B — TDD RED before harness modification

Before modifying `scripts/test-v093-ollama-recovery-windows-v3.ps1`, add the smallest deterministic behavioral regression proof.

The RED must execute the **real PowerShell harness-owned contract/self-test path** using Windows PowerShell 5.1 where available; do not substitute duplicated Python predicate logic or grep/string assertions as the behavioral proof.

Required RED semantics:

1. Construct/drive a synthetic same-suite sequence equivalent to Task 131:
   - provider-crash accepted observation with one open, circuit-closed incident ID, for example `ollama:2`;
   - immediately following operator-before observation with the exact same accepted incident and otherwise healthy state.
2. Demonstrate current harness rejects that operator-before continuation even though provider convergence just accepted it.
3. The regression test must fail current harness for the same semantic reason as Task 131.
4. Capture RED commit SHA and exact output.

A source-text `Contains`, regex, or grep assertion may supplement structural smoke but does not count as the required RED.

## Phase C — minimal harness-local repair

Implement the smallest responsibility-local fix in the recovery harness and its contract/self-test support.

Preferred shape:

- create/reuse a harness-owned baseline observation predicate rather than scattering duplicate logic;
- keep ordinary baseline strict;
- add an optional **expected preceding provider incident** parameter/record for the operator-before boundary;
- have `Scenario-Provider` return/store the exact accepted incident identity needed by the next scenario;
- have `Scenario-OperatorStop` consume that identity only when provider-crash directly preceded it in this same suite;
- clear the carried expectation once consumed so it cannot leak to unrelated later checks;
- preserve strict post-start convergence.

Do not broaden `Test-DurableConvergenceObservation` into a generic warning acceptance beyond the already-reviewed provider-crash semantics.

No unrelated refactor.

## Phase D — behavioral GREEN / negative cases

The harness-owned self-test and repository regression test must cover at minimum:

1. ordinary strict READY baseline → PASS;
2. ordinary baseline + any WARN → reject;
3. provider-crash accepted open/circuit-closed sole incident → provider convergence PASS;
4. same exact carried incident at immediate operator-before → PASS;
5. standalone operator-before with the same open incident but no carried same-suite expectation → reject;
6. different incident ID → reject;
7. missing incident → reject when an expected incident is carried;
8. duplicate incident row → reject;
9. circuit open → reject;
10. extra WARN → reject;
11. incident closed/PASS while verdict remains `READY_WITH_WARNINGS` → reject;
12. adapter missing/duplicate/expected=true → reject;
13. host/provider selection mismatch → reject;
14. Gateway/Ollama listener missing → reject;
15. post-operator-start remains strict READY and does not inherit the exception.

The self-test must execute without live disruption.

## Phase E — repository validation

At minimum run and record:

- `tests/test_recovery_harness_contract.py` / new focused regression tests;
- Windows PowerShell 5.1 parse of modified harness;
- harness `-ContractSelfTest`;
- full Python test suite;
- any provider/recovery/harness focused Python tests;
- `python -m compileall` for modified Python if any;
- `git diff --check`;
- plugin test suite;
- plugin validation / package proof validation;
- evaluation suite;
- `npm audit`;
- any other established stabilization gates affected by the change.

No live Windows crash/lifecycle acceptance is allowed in Task 132.

## Phase F — exact-SHA CI and package proof

Push the repaired repository candidate and require exact-SHA CI.

At minimum require:

- `Validate`;
- `PS5.1 v0.9.3 Ollama Recovery V3 Smoke`;
- `PS5.1 Acceptance Smoke` if triggered/affected;
- `Windows Installer Pack Smoke` if triggered/part of established candidate proof.

The dedicated Recovery V3 Smoke must execute the real non-disruptive harness `-ContractSelfTest` on the exact candidate SHA. A grep-only workflow is insufficient.

Produce/record fresh exact-SHA package proof:

- exact source SHA;
- workflow IDs/conclusions;
- artifact ID/name/digest;
- ZIP SHA256;
- tar.gz SHA256;
- payload count;
- plugin/payload fingerprint;
- exact repaired harness Git blob.

If exact-SHA CI/package proof is incomplete, verdict is `BLOCKED`, not PASS.

## Phase G — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`

Report must include:

- Task-131 evidence-derived diagnosis;
- exact self-contradictory old sequence;
- proof provider policy was not weakened;
- RED commit/output;
- repair commit(s) and files;
- behavioral positive/negative cases;
- focused/full validation;
- exact repaired candidate SHA;
- exact repaired harness blob;
- exact-SHA workflow IDs/conclusions;
- package artifact identity/hashes/count/fingerprint;
- explicit statement that no live recovery/lifecycle execution occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`.

Then STOP for independent ChatGPT review.

Do not automatically create or run a new live recovery acceptance.

## Hard fence

Task 132 authorizes repository/source/test/CI/package work only.

Forbidden:

- live recovery suite;
- gateway/provider crash injection;
- live `cnxclaw` start/stop/restart/enable/disable/reset/uninstall;
- install/install-over/reinstall;
- live provider/model/OpenClaw configuration changes;
- process kill;
- scheduled-task/service run/change;
- manual cleanup/normalization;
- reboot;
- credential/secret access;
- Dashboard semantic Send;
- merge/tag/GitHub Release;
- force push.

Final Dashboard durable-delivery acceptance remains prohibited until a repaired exact candidate later passes a separately authorized real-Windows recovery acceptance and independent review.
