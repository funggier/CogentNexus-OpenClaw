# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_OPENAI_DASHBOARD_ADMISSION_PROVENANCE`
Execution mode: `READ_ONLY_PROVENANCE_INVESTIGATION`
Task ID: `CNX-345`
Parent: `CNX-344`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Active branch: `cnx-345-openai-admission-provenance`

## Objective

Determine the exact boundary where the CNX-344 Dashboard request to OpenAI GPT-5.6 Luna reached the provider and produced a response without creating a CogentNexus durable Ticket lifecycle.

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

1. Trace Dashboard/WebChat send handling into `before_agent_run`.
2. Identify the exact predicates controlling CogentNexus admission.
3. Inspect `durableAdmissionEligible`, `ticketIntakeEligible`, `ticketFirst`, and `decision.lane` behavior on the current candidate source.
4. Determine whether Dashboard/OpenAI can fall through with `before_agent_run` returning `pass` while native OpenClaw provider dispatch proceeds.
5. Compare the proven CNX-343 Ollama lifecycle with the CNX-344 OpenAI Dashboard path and identify the first divergence.
6. Use CNX-344's historical runtime facts as the anchor; do not generate new live traffic.
7. Separate proven cause from remaining uncertainty.

## Required report

Publish:
`docs/operations/coordination/reports/CNX-20260914-345-openai-dashboard-admission-provenance-report.md`

Include exact source paths/commits, relevant predicates and hook priority, first-divergence boundary, CNX-344 historical evidence, remediation hypothesis (not implemented), and an explicit no-live-replay/no-mutation statement.

## Acceptance

PASS when an evidence-backed boundary/cause is identified specifically enough to create a deterministic remediation task without new live traffic.

BLOCKED when source/runtime evidence cannot identify the boundary without new live traffic or protected-state mutation.

Stop for independent ChatGPT review. Do not self-accept CNX-345.
