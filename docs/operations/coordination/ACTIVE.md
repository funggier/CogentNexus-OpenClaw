# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_LIVE_TIMEOUT_REQUALIFICATION`
Execution mode: `SINGLE_EXECUTOR`
Task ID: `CNX-340C`
Parent: `CNX-340B`
Base candidate: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
Base candidate HEAD: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
Evidence qualification HEAD: `e42010f826a4707abc217cb4305b7639f76db8f8`
Active branch: `agent/v0.9.6-live-timeout-requalification`

## Objective

Perform one bounded live semantic requalification against the v0.9.6 candidate to prove that CNX-340A's repaired direct model-call lease timeout authority reaches the real runtime durable lease at `2700s / 2700000ms` for the actual provider/model path.

CNX-339 already established the real Dashboard lifecycle chain. CNX-340B independently qualified the `before_agent_run` registration and invocation boundary in isolation. CNX-340C validates only the repaired timeout authority in live runtime state. OpenAI is deliberately excluded and will be tested separately.

## Executor / Reviewer

- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human authority: fresh continuation explicitly authorized by the operator after CNX-340B review.

## Hard fences

- Exactly one fresh Dashboard/Web Session request.
- Do not send an OpenAI request.
- No second semantic request/session.
- No retry, recovery, fallback, resend, duplicate-send, manual dispatch, provider switch, or model switch.
- No runtime configuration mutation.
- No timeout mutation during the test.
- No controller mutation.
- No provider/model/auth/routing mutation.
- No installation/release/tag mutation.
- No force push/history rewrite.
- If UI activation becomes ambiguous, treat it as consumed and resolve by read-only durable inspection.
- Do not wait 2700s solely for the timer; prove the exact durable lease value.

## Required evidence

1. Read-only provenance/health/controller/database preflight.
2. Running installed candidate artifact identity before semantic traffic.
3. Pre-test direct-model-call lease state/counts.
4. One fresh eligible Dashboard/Web Session and exactly one semantic request through the approved Ollama path.
5. Correlated Session/Ticket/Run/model-call lease/Result/Delivery chain.
6. `model_call_started` durable evidence for this exact run with `timeoutMs=2700000` (or an unambiguous 2700s equivalent).
7. Proof the tested lease did not revert to historical `900000ms`.
8. Terminal result and durable delivery settlement; expected outbox final state.
9. Unchanged controller bytes/SHA, provider/model configuration, and published tag.
10. No duplicate owner/run/result/delivery/recovery/fallback.
11. Exact IDs, timestamps, event ordering, duration, hashes, and evidence paths in report.

## PASS criteria

PASS requires exact candidate provenance, real `ollama/qwen3.8:27b` native `ollama` path, durable `model_call_started` timeout `2700000ms`, absence of historical `900000ms` for this lease, complete durable lifecycle correlation, successful terminal delivery settlement, unchanged protected state, and no unresolved failure classification.

Elapsed duration is supporting evidence only; it must not substitute for the exact timeout field.

## Failure classifications

- `ARTIFACT_PROVENANCE_MISMATCH`
- `RUNTIME_TIMEOUT_AUTHORITY_MISMATCH`
- `LEGACY_900S_TIMEOUT_REAPPEARED`
- `MODEL_CALL_EVENT_NOT_CORRELATED`
- `INFERENCE_PATH_NOT_PROVEN`
- `DURABLE_LIFECYCLE_INCOMPLETE`
- `DELIVERY_NOT_SETTLED`
- `PRODUCTION_STATE_MUTATION`
- `UNEXPECTED_DUPLICATE_OWNER`
- `UNEXPECTED_SEMANTIC_TRAFFIC`
- `UI_ACTIVATION_AMBIGUOUS`

## Required report

Publish:
`docs/operations/coordination/reports/CNX-20260914-340C-live-timeout-requalification-report.md`

Then stop for independent ChatGPT review. Hermes must not self-close or self-accept CNX-340C.

## Previous state

- Plan 2 remains closed.
- CNX-339 remains historical evidence and is not replayed as a separate acceptance.
- CNX-340A is the timeout-authority repair.
- CNX-340B closed the hook-evidence gap via isolated executed harness.
