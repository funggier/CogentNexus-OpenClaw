# CNX-340B — `before_agent_run` Hook Evidence Qualification

Status: `READY_FOR_HERMES`
Task ID: `CNX-340B`
Parent: `CNX-340A`
Execution mode: `SINGLE_EXECUTOR`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authority: `CNX-340A`

## Objective

Close the remaining `before_agent_run` evidence gap identified during CNX-339/CNX-340 by proving, without another real Dashboard semantic request, that the installed v0.9.6 candidate registers and invokes the canonical Ticket-first admission hook on the eligible owner-session path.

The existing CNX-339 semantic lifecycle already proved durable Ticket admission and downstream Run/Result/Delivery continuity for one real Dashboard request. CNX-340A repaired timeout propagation. This task must qualify the missing direct hook evidence only; it must not repeat the semantic lifecycle merely to obtain a log line.

## Accepted prerequisites

- CNX-339 lifecycle evidence: durable Ticket/Run/Result/Delivery chain exists for a real Dashboard request.
- CNX-340A = PASS.
- Repair branch containing CNX-340A: `agent/v0.9.6-direct-model-call-timeout-authority-repair`.
- CNX-340A HEAD: `460a8cd661d02ba419cc1eff13c0efc721cfa928`.
- Candidate direct-model lease artifact: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`.
- Provider/model reference: `ollama/qwen3.8:27b`.
- Configured provider/agent timeout authority: `2700s`.
- Published `v0.9.5` tag remains immutable at `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

## Scope

1. Read-only inspect the current source and candidate provenance before executing any qualification.
2. Identify the exact production registration path from `v091-release-entry.ts` through `legacyEntry.register(runtimeApi)` to the `before_agent_run` registration in `src/index.ts`.
3. Qualify registration with a deterministic in-process/unit harness using a captured `api.on` callback registry or equivalent existing test seam.
4. Invoke the captured `before_agent_run` handler with a minimal eligible owner-session event/context and prove the handler reaches its canonical admission path (`TicketStore.accept()` or the repository's exact current admission boundary).
5. Prove that the qualification run does not create a Dashboard/model/provider semantic request. Prefer a temporary isolated test database/filesystem fixture or an existing test harness; do not use the production runtime database.
6. Capture exact callback-registration evidence, invocation evidence, admission evidence, and any durable test-fixture evidence needed to establish the boundary.
7. Run the focused test file(s), full test suite, plugin build, and plugin validation after any code/test changes.
8. If an instrumentation or test-only seam is needed, keep it minimal and production-neutral. Do not add persistent runtime logging solely for this task unless source review proves there is no safer deterministic test seam.
9. Publish a report under `docs/operations/coordination/reports/CNX-20260914-340B-hook-evidence-qualification-report.md` and stop for independent review.

## Explicit exclusions

Do **not** send a real Dashboard/Web Session request. Do **not** invoke OpenAI or Ollama inference. Do **not** change provider/model routing, timeout configuration, controller state, installation state, release/tag history, or production databases. Do **not** perform retry, recovery, fallback, resend, duplicate-send, manual dispatch, or second-session tests. Do **not** infer hook execution merely from static source registration; the qualification must include an executed callback invocation in an isolated harness.

## Required evidence

### Registration

- `v091-release-entry.ts` authorizes Host schema v2 and reaches `legacyEntry.register(runtimeApi)`.
- The harness captures a `before_agent_run` callback registration from the registered plugin surface.
- Exactly one relevant admission callback owner is observed for the harness execution.

### Invocation

- The captured callback is explicitly invoked once with a synthetic but structurally valid eligible owner-session event/context.
- Invocation produces the expected admission-path side effect in the isolated fixture.
- No unrelated provider/model call is triggered.

### Admission

- The canonical Ticket-first boundary is reached and identified by exact fixture evidence (e.g. accepted Ticket/event row or existing repository test spy/seam).
- No second Ticket is created by repeated harness setup unless the test intentionally proves idempotency; this task should not add a separate idempotency test.

### Safety / isolation

- Production runtime database is unchanged.
- Production controller bytes/SHA are unchanged if inspected.
- No Dashboard traffic, inference attempt, provider call, or delivery attempt is created.

## PASS criteria

PASS requires all of the following:

1. Source path confirms the authorized release-entry bridge to the canonical admission implementation.
2. Executed harness captures the actual `before_agent_run` callback registration.
3. Executed harness invokes that callback and proves entry into canonical Ticket-first admission in an isolated fixture.
4. Evidence shows no provider/model/inference call was made.
5. Production state remains unchanged.
6. Focused tests, full suite, build, and plugin validation pass.
7. Report is published with exact commit/artifact identities and evidence paths.

Missing, inferred-only, or contradictory evidence is not PASS.

## Failure classifications

Use one or more of these exact classes when applicable:

- `HOOK_REGISTRATION_NOT_OBSERVED`
- `HOOK_INVOCATION_NOT_PROVEN`
- `ADMISSION_BOUNDARY_NOT_REACHED`
- `ISOLATION_FAILURE`
- `UNEXPECTED_SEMANTIC_TRAFFIC`
- `PRODUCTION_STATE_MUTATION`
- `REGRESSION_AFTER_EVIDENCE_SEAM`
- `ARTIFACT_PROVENANCE_MISMATCH`

## Stop/report contract

On PASS or failure, publish the report named above, include the exact tested commit and candidate artifact identity, preserve the no-semantic-traffic fence, and stop for ChatGPT review. Do not self-close the task as accepted; this task remains awaiting independent review after the report is published.
