# CNX-346 — Runtime OpenAI Dashboard Admission Provenance Qualification

- Parent: `CNX-345`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Execution mode: `READ_ONLY_RUNTIME_PROVENANCE_INVESTIGATION`

## Objective

Determine which runtime condition caused the CNX-344 Dashboard request to bypass CogentNexus Ticket admission before native OpenAI provider execution.

CNX-344 must not be rerun. Its semantic request must not be resent.

## Historical anchor

- Session: `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`
- Request: `CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`
- CNX-344 report commit: `eff0806e9493437ce74cd9123989396a6aefb609`
- CNX-345 provenance report commit: `414dc569d99fa4b95f1972632cabf4cc2837f4a7`

## Hard fences

- No semantic request.
- No replay/resend/retry/recovery/fallback/manual dispatch.
- No UI interaction.
- No provider/model/config mutation.
- No controller/database mutation.
- No production code changes.
- No test changes.
- No install/reinstall/rebuild/restart.
- No `v0.9.5` mutation.
- No force-push/history rewrite.

Read-only source inspection, installed-runtime inspection, logs/registration inspection, and documentation/report creation are permitted.

## Questions to answer

1. Is the CogentNexus `before_agent_run` hook actually registered and active in the current runtime?
2. What registration priority and handler identity are active?
3. What is the exact loaded plugin artifact/source fingerprint for the admission hook?
4. Does the current runtime load the source containing `durableAdmissionEligible` Dashboard handling and `ticketFirst` admission logic?
5. Can the runtime expose sufficient static/registration evidence to distinguish:
   - hook not active/not registered, versus
   - hook active with `durableAdmissionEligible(...) === false` for Dashboard events?
6. What event/context fields are available at the admission boundary (`sessionKey`, `sessionId`, `runId`, `senderIsOwner`, relevant prompt metadata) without sending a request?
7. Is there any existing diagnostic/logging state from CNX-344 that can establish the historical event predicate without replay?
8. Confirm the native OpenAI passthrough path remains reachable after a CogentNexus `pass`.
9. Identify the narrowest runtime-specific root cause that can guide deterministic remediation.

## Required output

Publish:

`docs/operations/coordination/reports/CNX-20260914-346-runtime-openai-admission-provenance-report.md`

The report must contain:

- exact branch/source/runtime versions inspected;
- installed artifact/module fingerprints where available;
- hook registration and priority evidence;
- admission predicate evidence;
- available event/context evidence;
- distinction between `hook absent` and `hook active + pass`;
- exact first divergence if determinable;
- any remaining uncertainty;
- minimal remediation target, clearly marked **not implemented**;
- explicit fence accounting proving no live request, UI interaction, mutation, restart, rebuild, or install occurred.

## Acceptance

PASS when the current runtime provenance investigation determines a sufficiently specific, evidence-backed cause for the Dashboard→OpenAI admission bypass without new live traffic or protected-state mutation.

BLOCKED when the distinction requires replay/live traffic or protected-state mutation.

Do not self-accept. Stop for independent ChatGPT review after publishing the report.
