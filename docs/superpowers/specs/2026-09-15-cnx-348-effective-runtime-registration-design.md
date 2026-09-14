# CNX-348 — Effective Runtime Registration Provenance Design

## Status

**DESIGN APPROVED BY HUMAN OPERATOR — investigation only; no production behavior change is authorized in this phase.**

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-348-effective-runtime-registration`
- Parent/baseline commit: `7c563592625f71c817cc38649caa1047a7efb746`
- Previous investigation: CNX-347
- Previous runtime symptom: CNX-344 OpenAI Dashboard request completed without a durable Ticket/Run/Call/Result/Delivery lifecycle
- GitHub is the authoritative source for task, code, commits, and reports. Local-only files are not accepted as evidence.

## Problem

CNX-347 proved that the canonical `v091-release-entry` source path can register exactly one `before_agent_run` admission handler at priority 2000 under a synthetic Host-authorized API. The test was already GREEN, so it did not reproduce the CNX-344 runtime failure.

The remaining question is therefore not whether the source contains the expected registration code, but whether the **effective OpenClaw runtime** loaded, registered, retained, and invoked that hook for the Dashboard/OpenAI execution path.

## Objective

Determine the first runtime boundary at which the expected admission path diverges from the actual CNX-344 execution, without changing production semantics.

## Boundary model

```text
OpenClaw process
  -> loaded CogentNexus plugin artifact/module identity
  -> v091-release-entry.register()
  -> legacy registration wrapper chain
  -> api.on("before_agent_run")
  -> effective OpenClaw hook registry
  -> Dashboard request
  -> before_agent_run invocation
  -> durable admission decision
  -> Ticket acceptance
```

## Candidate divergence classes

The investigation must distinguish, with evidence, at least these classes:

A. release entry was never invoked.

B. release entry was invoked, but registration did not reach the canonical admission hook.

C. canonical registration executed, but the effective host hook registry did not retain/use the hook.

D. OpenClaw loaded a different/stale plugin artifact or module than the inspected GitHub source.

E. the hook existed but the Dashboard execution path bypassed `before_agent_run`.

F. the hook was invoked, but effective configuration/authority caused admission to pass rather than create a Ticket.

## Investigation method

### Phase 1 — source-to-runtime registration provenance

Build an evidence-only harness around the effective release registration composition. The harness must record:

- module/file identity for the loaded release entry
- registration invocation count
- wrapper-chain traversal where observable
- `before_agent_run` registration count
- handler identity and priority
- relevant effective plugin configuration
- whether registration returns a Promise and when registration becomes observable
- whether the resulting hook record is visible from the simulated effective registry

The harness must test the composition as close as practical to OpenClaw's actual plugin loading boundary, rather than directly calling the canonical handler in isolation.

### Phase 2 — intentional negative control

The test must contain an intentional misregistration/bypass control that would fail when the effective registration boundary is broken. This is required to demonstrate that the harness can actually detect the class of bug being investigated.

A test that only asserts the current source path is correct is insufficient.

### Phase 3 — effective configuration discrimination

Verify that the same effective registration remains admission-enabled when:

- Host authority is schemaVersion 2 / `cnxMode=active`
- `preInferenceAdmission=true`
- `ticketFirst=true`
- Dashboard/webchat session context is represented
- `senderIsOwner=true`

The test must capture the effective values seen at the admission boundary rather than only the input fixture values.

### Phase 4 — runtime artifact provenance

Where supported by the repository test/runtime environment, record enough provenance to compare the module actually loaded by the test/runtime against the GitHub source revision. Do not mutate installation state. Do not restart OpenClaw.

## TDD contract

This phase is diagnostic.

- A RED test must be reproduced before any production fix is proposed.
- If the harness is GREEN but cannot reproduce the failure, report the diagnostic boundary as unresolved and remain BLOCKED.
- Do not modify `durableAdmissionEligible`.
- Do not modify timeout authority.
- Do not add a second admission owner.
- Do not change provider routing.
- Do not change runtime/database state.
- Do not touch v0.9.5 tag/history.

## Required evidence

The final GitHub report must include:

1. remote branch and exact HEAD SHA
2. baseline lineage from CNX-347
3. exact files changed
4. exact test commands and fresh results
5. registration provenance observations
6. negative-control result
7. classification A-F, or an explicit statement that the classification remains unresolved
8. confirmation of whether any production code changed
9. confirmation that no live semantic/UI/provider/runtime/database mutation occurred
10. next recommended boundary if still BLOCKED

## Acceptance criteria

CNX-348 may leave `BLOCKED` when evidence does not reproduce the defect. It may only advance to a repair task when the evidence identifies a specific broken runtime boundary and a regression test fails for that boundary before any production edit.
