# CNX-20260829-126 — Static Contract Trace Before Retained-Evidence Diagnosis

Status: `NON_AUTHORITATIVE_HYPOTHESIS`
Date: 2026-08-29 ICT
Task: `CNX-20260829-126`

## Purpose

Record the independent repository-side static trace performed before Task 126 reads the retained Task-125 420-second observation series.

This note is **not** a substitute for the retained JSON/log. The Task-125 observation series remains authoritative for deciding whether the root cause belongs to product recovery logic or the acceptance harness.

## Proven source contract

The frozen Task-125 candidate is:

`01d08cd7c82f542c821e3a60f7fffa036efb1d75`

The exact recovery harness blob is:

`80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

### Provider incident closure

`skills/cogentnexus-openclaw/scripts/provider_recovery_v092.py` defines an explicit durable provider incident.

Important behavior:

- provider failure opens an incident;
- a successful automatic provider start records a recovery attempt but does not by itself prove stable model execution;
- `record_stable_success(...)` records positive model-call evidence and then calls `close_incident(..., "stable_success", ...)`;
- a verified operator transition may also close the incident;
- elapsed time alone does not close/reopen recovery authority.

The repository tests explicitly assert that a durable successful model-call event closes the provider incident.

### Recovery-check verdict

`skills/cogentnexus-openclaw/scripts/checks_v092.py::check_recovery(...)` maps provider incident state as follows:

- no open incident -> `Provider recovery incident = PASS`;
- open incident with circuit closed -> `Provider recovery incident = WARN`;
- open incident with circuit open -> `Provider recovery incident = WARN`.

The generic check aggregator maps any WARN to `READY_WITH_WARNINGS`, not `READY`.

Therefore a provider may be listening and healthy while `check recovery --json` intentionally remains `READY_WITH_WARNINGS` until the incident obtains stable-success or verified-transition closure evidence.

## Exact harness contract under review

`scripts/test-v093-ollama-recovery-windows-v3.ps1::Wait-DurableConvergence(...)` currently requires all of the following simultaneously:

- host mode `managed`;
- host selected provider `ollama`;
- provider selected provider `ollama`;
- recovery verdict exactly `READY`;
- exactly one Provider event adapter row with `details.expected == false`;
- Gateway listener present;
- Ollama listener present;
- when `RequireProviderIncident=true`, exactly one Provider recovery incident row with `details.circuitOpen == false`.

`Scenario-Provider` calls:

`Wait-DurableConvergence 'converge-provider-after' $true`

The provider-crash scenario does not itself create a new stable model completion after the Ollama listener returns before waiting for convergence.

## Contract tension to prove or disprove from retained Task-125 evidence

There is a plausible mismatch:

1. provider crash opens an incident;
2. automatic recovery restores Ollama process/listener;
3. circuit remains closed after the bounded recovery attempt;
4. no stable model completion has yet occurred;
5. recovery incident therefore remains open by policy;
6. recovery check therefore reports WARN / `READY_WITH_WARNINGS`;
7. harness nevertheless requires exact `READY` while also explicitly requiring the provider incident row to exist and have `circuitOpen == false`;
8. without new stable-success evidence, that predicate may be impossible to satisfy regardless of the 420-second fuse.

This is only a hypothesis until the retained Task-125 JSON confirms the actual 420-second state sequence.

## Mandatory evidence decision for Task 126

Before production or harness repair, extract from:

`C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.json`

at minimum:

- first `converge-provider-after` observation;
- last observation;
- every change point;
- recovery verdict over time;
- incident `state`/`incidentOpen`/`circuitOpen`/attempt count when available;
- Gateway and Ollama listener/PID state;
- selected-provider state;
- provider-event-adapter state.

### If retained evidence shows

- Gateway listener healthy;
- Ollama listener recovered;
- host/provider selection remained `ollama`;
- adapter row coherent with `expected == false`;
- circuit remained closed;
- recovery verdict stayed `READY_WITH_WARNINGS` because the incident remained open;
- no stable model completion occurred during the wait;

then classify the deepest proven defect as **acceptance-harness contract mismatch**, not provider recovery failure.

The RED test should prove that the harness rejects the documented post-restart/open-incident state even though the recovery policy defines that state as coherent and awaiting stable-success evidence.

The minimal repair should remain in the acceptance/recovery harness layer. Do **not** weaken recovery policy by treating process health/listener recovery as stable model success.

### If retained evidence shows instead

- provider listener did not recover;
- Gateway did not recover/remain healthy;
- selected-provider state drifted;
- event adapter became inconsistent;
- circuit opened incorrectly after one attempt;
- incident/check data became stale or malformed;
- or another recovery check produced WARN/FAIL unrelated to the expected open incident;

then repair the actual owning product layer and do not change harness semantics merely to make the test pass.

## Safety invariant

Do not implement `healthy provider == stable_success` or `listener present == stable_success` as an incident-closing rule. That would collapse the existing distinction between process recovery and proven successful model execution.

Task 126 remains read-only with respect to the live Windows runtime and authorizes no recovery-suite replay.
