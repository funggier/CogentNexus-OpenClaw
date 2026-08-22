# CogentNexus Project Worklog

This file records meaningful project milestones and investigation results. It is not intended to capture every commit.

Newest entries should normally be added at the top.

---

## 2026-08-22 — Gateway convergence diagnostic introduced

### Why

The first v0.9.3 full disruptive Windows run proved that the OpenClaw Gateway process could recover after an exact-PID hard kill, but the suite still failed because durable recovery diagnostics remained `READY_WITH_WARNINGS` shortly after the replacement Gateway listener appeared.

### Observed evidence

- Gateway before injection: validated OpenClaw `node.exe` listener.
- Exact PID hard-killed; no process-tree kill.
- Replacement Gateway listener appeared with a different PID.
- Ollama remained healthy.
- `cnx check recovery --json` still reported an active maintenance/recovery marker.
- The marker described an externally confirmed unresponsive Gateway with `recoveryPolicy=healthy-runtime`.
- The v3 suite therefore stopped before provider-crash and operator-stop scenarios.
- Best-effort cleanup using `cnx start` returned the system to MANAGED + Ollama + `READY`.

### Interpretation

Gateway **process recovery succeeded**. The unresolved question is durable-state convergence.

A new focused diagnostic was added:

```text
scripts/test-v093-gateway-convergence-windows.ps1
```

It waits for the replacement Gateway and then observes `cnx check recovery --json` without using `cnx start` to force a state transition.

Dedicated PS5.1 convergence smoke CI was also added.

Implementation/evidence head before operations-doc commits:

```text
306b091352a652a898c353aa49323c8d6a389106
```

All eight workflows for that head completed successfully.

---

## 2026-08-22 — v3 baseline accepted on real Windows target

The v3 baseline harness passed after correcting the v2 status-document shape assertion.

Proven baseline properties included:

- `host.state.mode = managed`;
- Host/provider selected provider = `ollama`;
- Gateway listener healthy;
- Ollama listener healthy;
- `cnx check recovery` verdict = `READY`;
- provider event adapter not required for Ollama;
- `requestedArguments=["status"]` correctly persisted in harness evidence.

This established that the installed v0.9.3 Ollama-only candidate itself was healthy before disruptive recovery injection.

---

## 2026-08-22 — v2 harness status-shape bug found

The v2 baseline reported failure even though the runtime was healthy.

Root cause:

```text
harness read:  $status.state.mode
actual shape:  $status.host.state.mode
```

The assertion was corrected in v3 and regression smoke coverage was added so the incorrect status path could not silently return.

No runtime recovery change was required for this failure.

---

## 2026-08-22 — first Recovery Reality harness abandoned after unsafe process behavior

The original automated recovery harness terminated abruptly during its first OpenClaw version probe. The PowerShell window and unrelated Firefox processes were also lost.

Evidence showed the run never reached Gateway/provider failure injection.

Response:

- old harness declared unsafe and not reusable;
- process-tree termination removed from the recovery test strategy;
- exact listener PID validation introduced;
- executable and command-line identity validation introduced;
- harness PID and ancestor protection introduced;
- protected interactive process names introduced;
- active operation/PID evidence persisted before disruptive actions.

This incident is the reason current Recovery Reality tests use strict process-target safety gates.

---

## 2026-08-22 — v0.9.3 direction changed to Ollama-only

The project stopped pursuing LM Studio as a managed provider for v0.9.3.

Reasons included lower operational complexity, lower memory overhead for the intended local setup, and no recovery advantage sufficient to justify maintaining the extra provider surface during continuity development.

v0.9.2 remains unchanged and retains its historical multi-provider behavior.

v0.9.3 changes include:

- Ollama-only provider facade;
- Ollama-only operator CLI surface;
- installers default/restrict managed provider to Ollama;
- Recovery Reality tests use Ollama only;
- v0.9.2 upgrade handoff still respects the installed legacy lifecycle before migration.

---

## 2026-08-22 — v0.9.2 released and frozen

v0.9.2 completed final Windows acceptance and release publication.

Release/base commit:

```text
986f3c7be8389866f3ffe4f9b372ff1264ddbe8e
```

The release is treated as the Golden Baseline and is not to be rewritten while v0.9.3 experiments proceed on a separate branch/PR.

---

## Earlier accepted foundation

The v0.9.1/v0.9.2 line established the durable Ticket/Recovery/Delivery foundation used by current work, including:

- Ticket-first durable admission;
- MANAGED / PASSTHROUGH / MAINTENANCE state semantics;
- external Host recovery authority;
- duplicate/recovery ownership fences;
- durable result/delivery boundaries;
- native OpenClaw handoff/restoration behavior;
- event-driven provider recovery policy rather than timer/cooldown authority.

The current v0.9.3 work should reopen this foundation only when new real failure evidence requires it.