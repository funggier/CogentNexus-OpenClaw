# CNX-345 — OpenAI Dashboard Admission Provenance Investigation

- Parent: `CNX-344`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Execution mode: `READ_ONLY_PROVENANCE_INVESTIGATION`

## Objective

Determine where the real Dashboard → OpenAI GPT-5.6 Luna request from CNX-344 bypassed the CogentNexus durable Ticket lifecycle.

CNX-344 must not be rerun and its semantic request must not be resent.

The investigation must identify the exact boundary responsible for:

```text
Dashboard send → OpenAI response
                    ↘ no CogentNexus Ticket
```

## Evidence boundary

Known CNX-344 session:
`agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`

Known semantic request:
`CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`

Known CNX-344 report commit:
`eff0806e9493437ce74cd9123989396a6aefb609`

Treat CNX-344's single UI send as historical evidence. Do not send another semantic request.

## Hard fences

- No semantic request.
- No resend/retry/recovery/fallback/manual dispatch.
- No UI interaction.
- No provider/model/config mutation.
- No controller/database mutation.
- No production code changes.
- No test changes.
- No install/reinstall/rebuild/restart.
- No changes to v0.9.5.
- No force-push/history rewrite.

Read-only inspection and repository documentation/report creation are permitted.

## Investigation questions

1. Trace the Dashboard/WebChat send path into the OpenClaw `before_agent_run` lifecycle.
2. Identify the exact code predicate(s) that determine whether the event is admitted to CogentNexus Ticket-first handling.
3. Verify the behavior of `durableAdmissionEligible(...)`, `ticketIntakeEligible(...)`, and the surrounding `before_agent_run` flow on the current candidate source.
4. Determine whether Dashboard/OpenAI requests can reach native OpenClaw provider dispatch while CogentNexus admission returns `pass`.
5. Compare the proven CNX-343 Ollama lifecycle path against the CNX-344 OpenAI Dashboard path and identify the first divergence.
6. Correlate source behavior with the CNX-344 runtime facts without modifying or replaying the request.
7. State the narrowest evidence-backed root cause. Do not speculate beyond source/runtime evidence.

## Required checks

- Exact source commit(s) inspected.
- Relevant `before_agent_run` registration and priority.
- Exact `durableAdmissionEligible` behavior for Dashboard sessions.
- Exact `ticketFirst` and `ticketIntakeEligible` conditions.
- Whether `decision.lane` is relevant to Ticket creation.
- Whether provider selection/model choice changes the admission path.
- Whether native OpenClaw provider execution can occur independently of the CogentNexus hook.
- Whether any known event normalization/transport boundary can explain the observed bypass.
- CNX-343 comparison evidence where available.

## Expected output

Publish:

`docs/operations/coordination/reports/CNX-20260914-345-openai-dashboard-admission-provenance-report.md`

The report must include:

- finding classification;
- exact first-divergence boundary;
- source evidence with file paths and line/range references where available;
- CNX-344 runtime evidence used as the historical anchor;
- distinction between proven cause and remaining uncertainty;
- a minimal remediation hypothesis, clearly marked as not implemented;
- explicit statement that no live request was replayed and no protected state was mutated.

## Acceptance

PASS when the investigation identifies an evidence-backed boundary/cause sufficiently specific to guide a deterministic remediation task without another live request.

BLOCKED when the available source/runtime evidence cannot identify the boundary without new live traffic or protected-state mutation.

Do not self-accept. Stop for independent ChatGPT review after publishing the report.
