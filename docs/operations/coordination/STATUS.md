# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK235_TASK234_EXACT_TOPOLOGY_TDD_EVIDENCE_CLOSURE`  
**Updated:** 2026-09-03 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 235 is repository/evidence hardening only with zero semantic/live mutation budget  
**Active task:** `CNX-20260903-235`  
**Parent:** `CNX-20260903-234`  
**Failure parent:** `CNX-20260903-233`  
**Installer-requalification parent:** `CNX-20260902-230`  
**Accepted repair parent:** `CNX-20260902-226`  
**Failure lineage:** `CNX-20260902-223`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK234_FUNCTIONAL_REPAIR_GREEN__PASS_REJECTED_PENDING_TDD_AND_EXACT_TOPOLOGY_EVIDENCE_CLOSURE`

## Publication and candidate authority

Public `v0.9.3` remains unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Accepted pre-Task-234 production authority remains:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Task-234 functional candidate repair:

`43fd1d6f988431c7a94d24abc8a6811de46f78fa`

Candidate plugin payload fingerprint:

`964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`

The candidate is not yet authorized for live installation.

## Task 234 adjudication

Task-234 report disposition:

`PASS_DASHBOARD_ORIGIN_DISCORD_SESSION_DURABLE_STAGING_REPAIR_GREEN`

Independent review disposition:

`REJECT_PASS_TDD_EVIDENCE_INCOMPLETE__FUNCTIONAL_REPAIR_GREEN__EXACT_TOPOLOGY_HARDENING_REQUIRED`

The functional repair direction is accepted provisionally:

- framework ingress metadata is carried separately from owner session identity;
- Dashboard-origin context may stage on the Discord-associated owner;
- true Discord-origin context stays outside Dashboard staging;
- `isDashboardSession()` was not globally broadened;
- exact candidate Actions are GREEN.

PASS is withheld because the required TDD and production-shaped settlement proof is incomplete.

## Evidence gaps to close

### Corrected RED provenance

The test-only commit:

`6b1e496fa67b0f09678268ba918a98a824610286`

precedes production repair, but final harness corrections were committed together with production repair in:

`278a235fa9df75990a3ea7f1a8e3930441ead76b`

Task 235 must reconstruct the corrected test against exact predecessor:

`89a0f539c02dfef971cec9b6baa98a1929d2fb13`

in a disposable checkout and prove the intended staging RED with predecessor production unchanged.

### Exact topology settlement

The new Task-234 regression currently proves marker + pending durable row. It must be extended through the real native transcript settlement boundary on the same Discord-associated owner and prove:

```text
direct_result delivered
Ticket completed
delivery_confirmed exactly once
no direct_redelivery_timeout
no recovery regeneration
owner key preserved
```

The same owner under true Discord-origin context must remain outside Dashboard native staging.

### Missing / contradictory ingress context

Task 235 must capture exact OpenClaw `2026.7.1-2` semantics for:

```text
ctx.messageProvider
ctx.channel
ctx.channelId
ctx.sessionKey
ctx.runId
```

and encode missing/ambiguous behavior fail-closed according to that exact contract. No heuristic precedence is authorized.

## Active Task 235

Execute:

`docs/operations/coordination/tasks/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Required sequence:

```text
fresh GitHub authority
-> exact installed OpenClaw 2026.7.1-2 hook-context proof
-> disposable predecessor corrected-RED reconstruction
-> strengthened exact-topology settlement regression
-> same-owner Discord negative control
-> missing/ambiguous ingress contract proof
-> production source unchanged if candidate already passes
-> otherwise fresh test-only RED then minimal fix
-> targeted GREEN
-> full validation + required Actions GREEN
-> report and STOP
```

## Exact candidate CI

For `43fd1d6f988431c7a94d24abc8a6811de46f78fa`:

- Validate `33760819493` — SUCCESS
- Windows Installer Pack Smoke `33760819324` — SUCCESS
- PS5.1 Acceptance Smoke `33760819312` — SUCCESS

These results are accepted but do not waive Task-235 evidence closure.

## Budgets / hard fences

```text
Dashboard semantic Sends: 0
Discord semantic Sends: 0
direct operator Discord/API Sends: 0
semantic retries: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway actions: 0
live plugin mutations: 0
provider/model substitutions: 0
process terminations: 0
Task-223/Task-233 evidence mutations: 0
Release/tag/asset mutations: 0
force push/history rewrite: 0
```

Repository test/source work is authorized only as specified by Task 235. Read-only exact-version OpenClaw inspection and disposable predecessor reconstruction are authorized.

## Stop boundary

Task 235 must publish:

`docs/operations/coordination/reports/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Then stop for independent ChatGPT review before live installation, semantic requalification, Task-233 replay/settlement, historical-evidence cleanup, or public release mutation.
