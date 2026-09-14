# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_RUNTIME_OPENAI_ADMISSION_PROVENANCE`
Execution mode: `READ_ONLY_RUNTIME_PROVENANCE_INVESTIGATION`
Task ID: `CNX-346`
Parent: `CNX-345`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Active branch: `cnx-346-runtime-openai-admission-provenance`

## Objective

Determine which current runtime condition can explain the CNX-344 Dashboard request reaching OpenAI GPT-5.6 Luna without creating a CogentNexus durable Ticket lifecycle.

CNX-344 must not be rerun and its semantic request must not be resent.

## Hard fences

- Read-only source/runtime inspection only.
- No semantic request.
- No UI interaction.
- No resend/retry/recovery/fallback/manual dispatch.
- No provider/model/config/controller/database mutation.
- No production code/test changes.
- No install/reinstall/rebuild/restart.
- No v0.9.5 mutation.
- No force-push/history rewrite.

## Investigation

1. Verify whether the CogentNexus `before_agent_run` hook is currently registered and active.
2. Verify active registration priority and handler identity.
3. Verify the exact installed plugin/module fingerprints for the admission path.
4. Verify the loaded source contains Dashboard-aware `durableAdmissionEligible` and `ticketFirst` logic.
5. Determine whether static/runtime evidence distinguishes hook absence from hook-active-plus-`pass`.
6. Record available event/context fields at the admission boundary without generating traffic: `sessionKey`, `sessionId`, `runId`, `senderIsOwner`, and relevant prompt metadata where available.
7. Search existing CNX-344 logs/diagnostics for historical admission evidence; do not replay the request.
8. Verify source semantics showing that a CogentNexus `pass` returns control to native OpenClaw provider dispatch in passthrough mode.
9. Compare against CNX-343 and identify the narrowest runtime-specific cause sufficient to guide deterministic remediation.

## Required report

Publish:
`docs/operations/coordination/reports/CNX-20260914-346-runtime-openai-admission-provenance-report.md`

Include exact source/runtime fingerprints, hook registration evidence, admission predicate evidence, available historical event evidence, first divergence if determinable, remaining uncertainty, and remediation target (not implemented).

Explicitly account for all hard fences and state that no live request, UI interaction, mutation, restart, rebuild, or install occurred.

## Acceptance

PASS when the current runtime provenance evidence determines a sufficiently specific cause for the Dashboard→OpenAI admission bypass without new live traffic or protected-state mutation.

BLOCKED when the distinction requires replay/live traffic or protected-state mutation.

Stop for independent ChatGPT review. Do not self-accept CNX-346.
