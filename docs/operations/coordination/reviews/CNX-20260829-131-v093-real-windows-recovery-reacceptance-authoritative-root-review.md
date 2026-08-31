# Independent Review — CNX-20260829-131

## Verdict

**ACCEPTED FAIL — AUTHORITATIVE-ROOT PREFLIGHT PASSED, GATEWAY-CRASH RECOVERY PASSED, AND PROVIDER-CRASH RECOVERY PASSED UNDER THE REPAIRED FAIL-CLOSED INCIDENT CONTRACT; FULL-SUITE ACCEPTANCE FAILED BEFORE OPERATOR-STOP BECAUSE THE HARNESS REQUIRES STRICT `READY` AT `operator-before` EVEN THOUGH ITS IMMEDIATELY PRECEDING PROVIDER-CRASH CONTRACT INTENTIONALLY PERMITS THE SAME OPEN, CIRCUIT-CLOSED PROVIDER INCIDENT TO REMAIN `READY_WITH_WARNINGS`. THIS IS A HARNESS SCENARIO-SEQUENCING DEFECT, NOT A NEW PROVIDER-RECOVERY PRODUCT FAILURE. OPERATOR-STOP REMAINS UNPROVEN.**

## Scope reviewed

Task-131 report commit:

`c6ecf60a5c12faec2a55a37a12f95b6ba00a7599`

Task-131 start coordination HEAD:

`9d09f485d3f3325c25487b91c79accf2241423d5`

Accepted repository candidate used by the live run:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact harness used:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

The Task-131 repository commit is report-only and its parent is the exact Task-131 activation HEAD. No executor source/harness/runtime change was inserted before publication.

## Accepted live results

### Corrected authoritative preflight — PASS

Task 131 corrected the Task-128 wrong-root defect. Fresh authoritative probes used the installed launcher and its parsed `.cogentnexus-openclaw` root. The preflight established:

- mode `managed`;
- selected provider `ollama`;
- recovery `READY`;
- provider incident/circuit closed;
- exact installed plugin fingerprint;
- OpenClaw `2026.7.1-2`;
- healthy Gateway and Ollama listeners;
- authoritative SQLite read-only `PRAGMA integrity_check = ok`;
- unchanged four-model inventory.

The live suite therefore started from a valid baseline.

### Interactive one-shot discipline — PASS

The exact harness was launched once in a true PowerShell PTY. The literal confirmation prompt appeared and exactly one lowercase `y` plus Enter was supplied. The process exited `1`; the Task-131 one-shot suite authorization is consumed `1 / 1`. No suite or individual scenario rerun occurred.

### Baseline — PASS

The harness baseline passed under strict ordinary `READY` semantics before disruption.

### Gateway-crash — PASS

The exact validated Gateway listener PID was force-killed without process-tree kill. A different listener PID returned and durable convergence passed under strict ordinary `READY` semantics.

### Provider-crash — PASS

The exact validated Ollama listener PID was force-killed without process-tree kill. A different Ollama listener PID returned. The provider recovery circuit remained closed and durable convergence passed in about 3.552 seconds under the Task-127 fail-closed provider-incident exception.

The accepted post-crash state was:

- mode `managed`;
- selected provider `ollama`;
- Gateway/Ollama listeners healthy;
- recovery verdict `READY_WITH_WARNINGS`;
- exactly one permitted WARN: the open `Provider recovery incident` `ollama:2`;
- `incidentOpen=true`;
- `circuitOpen=false`;
- provider event adapter PASS with `expected=false`;
- all other recovery checks PASS.

This is exactly the state the repaired provider-crash convergence contract was designed to accept.

## First failing boundary

The exact failure occurred before the operator-stop lifecycle action:

`Managed Ollama baseline failed at operator-before.`

The harness implementation is internally inconsistent across the provider-crash → operator-stop scenario boundary:

1. `Scenario-Provider` calls `Wait-DurableConvergence ... $true`, which intentionally accepts `READY_WITH_WARNINGS` only when the sole warning is the same open, circuit-closed provider recovery incident.
2. It then marks `scenario-provider-crash` PASS without closing that incident.
3. `Scenario-OperatorStop` immediately calls `Assert-Baseline 'operator-before'`.
4. `Assert-Baseline` requires `recovery.verdict == 'READY'` with no sequence-aware exception.
5. No stable model completion or verified manual transition occurs between those two assertions.

Therefore an idle provider crash can correctly PASS `Scenario-Provider` and then deterministically fail `operator-before` solely because the deliberately retained incident has not yet received evidence allowed to close it.

## Why runtime/provider policy must not be weakened

`provider_recovery_v092.py` explicitly states that recovery authority is event-driven and an incident closes only on stable-success evidence or a verified manual provider transition. A successful automatic restart attempt alone does not close the incident.

The policy owner implements:

- `record_stable_success(...)` → closes with reason `stable_success`;
- `clear_after_manual_transition(...)` → closes with reason `verified_manual_transition`.

Changing provider recovery so that listener/process recovery itself closes the incident would collapse the deliberate safety distinction that Tasks 126/127 preserved. Task 131 provides no evidence justifying such a product-policy change.

## Correct repair boundary

Repair the recovery harness scenario sequencing, not the provider recovery runtime.

The next repository task should make `operator-before` sequence-aware while remaining fail-closed:

- when operator-stop runs standalone, it must still require strict `READY` baseline;
- when operator-stop immediately follows a provider-crash scenario that PASSed in the same harness process with an intentionally open, circuit-closed provider incident, the pre-operator gate may accept only that exact preceding incident state;
- bind the allowance to the same incident identity/state observed and accepted by the provider-crash scenario, not merely to any `READY_WITH_WARNINGS` state;
- require exactly one WARN, named `Provider recovery incident`, with `incidentOpen=true`, `circuitOpen=false`, all other checks PASS, healthy Gateway/Ollama, managed mode, and provider `ollama`;
- reject missing/duplicate/different/stale incident IDs, additional WARNs, FAIL/INDETERMINATE checks, circuit-open state, adapter mismatch, listener loss, provider mismatch, or non-managed mode;
- do not manufacture model completion or execute a lifecycle transition merely to clear the incident before operator-stop;
- after the harness-owned `stop`/`start`, strict ordinary `READY` convergence remains required. The verified `start` transition may naturally close the incident according to existing product policy.

## Required TDD quality

Before modifying the harness:

1. Add a deterministic behavioral RED that executes the real PowerShell harness-owned contract/self-test path and demonstrates the Task-131 sequence state: provider-crash accepted incident → operator-before currently rejected.
2. RED must fail current harness for the same reason as Task 131, not by grep/string matching or duplicated Python predicate logic.
3. Add fail-closed negative cases at minimum for:
   - operator-stop standalone + open incident → reject;
   - same-suite provider incident ID/state → accept sequence precondition;
   - different incident ID → reject;
   - extra warning → reject;
   - circuit open → reject;
   - closed/PASS incident paired with `READY_WITH_WARNINGS` → reject;
   - listener/provider/managed-state structural failure → reject.
4. Make the smallest harness-local repair and keep provider runtime policy unchanged unless independent evidence proves otherwise.
5. Run focused tests, full Python suite, PowerShell parse/self-test, plugin tests/validation/evaluation/audit as applicable, `git diff --check`, and the dedicated PS5.1 Recovery V3 Smoke on the exact repaired SHA.
6. Produce fresh exact-SHA package proof and record harness blob/candidate identity before any future live authorization.

## Cleanup/final-state review

After the Task-131 fail-stop, only the exact harness's built-in best-effort reconciliation ran. It returned the machine to managed/Ollama `READY`; final Gateway/Ollama listeners were healthy, SQLite integrity remained `ok`, plugin fingerprint/model inventory were unchanged, and no manual normalization occurred.

This healthy cleanup state does not convert the unexecuted operator-stop scenario into a PASS.

## Ledger

Accepted ledger:

- Task-131 suite: `1 / 1` consumed;
- confirmation: `1 / 1`;
- baseline: PASS;
- gateway-crash: PASS;
- provider-crash: PASS;
- operator-stop: `0`, not reached;
- reruns: `0`;
- manual cleanup/normalization: `0`;
- Dashboard semantic Send: `0`.

Do not replay Task 131. Any new live recovery execution requires a repaired exact candidate, independent repository review, and a separately authorized task.

## Advancement decision

Do **not** open Dashboard durable-delivery acceptance.

Open a repository/source TDD task to repair the provider-crash → operator-stop harness sequencing contract. No live recovery/lifecycle action is authorized by this review.
