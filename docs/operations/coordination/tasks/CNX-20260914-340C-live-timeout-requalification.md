# CNX-340C — Live Direct Model-Call Timeout Requalification

Status: `READY_FOR_HERMES`
Task ID: `CNX-340C`
Parent: `CNX-340B`
Execution mode: `SINGLE_EXECUTOR`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authority: `CNX-340B`

## Objective

Perform one bounded live semantic requalification against the v0.9.6 candidate to prove that CNX-340A's repaired direct model-call lease timeout authority reaches the real runtime durable lease at `2700s / 2700000ms` for the actual provider/model path.

CNX-339 already established the real Dashboard lifecycle chain. CNX-340B independently qualified the `before_agent_run` registration and invocation boundary in isolation. CNX-340C exists only to validate the repaired timeout authority in live runtime state; do not reopen the hook investigation and do not test OpenAI in this task.

## Candidate / provenance

- Candidate branch: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
- CNX-340A HEAD: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- CNX-340B evidence branch/report HEAD: `e42010f826a4707abc217cb4305b7639f76db8f8`
- Live requalification branch: `agent/v0.9.6-live-timeout-requalification`
- Candidate artifact: `dist/v091-release-entry.js`
- Candidate artifact SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Provider/model: `ollama/qwen3.8:27b`
- Native provider API: `ollama`
- Agent/provider timeout authority: `2700s`
- Published `v0.9.5`: `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` (immutable)

## Scope

1. Perform read-only provenance/health/controller/database preflight.
2. Confirm the running installed candidate artifact identity before semantic traffic.
3. Record production direct-model-call lease state immediately before the test, including relevant counts and existing active leases.
4. Use one fresh eligible Dashboard/Web Session and submit exactly one semantic request to the already-approved Ollama model path.
5. Correlate the resulting Session/Ticket/Run/model-call lease/Result/Delivery chain.
6. Capture the `model_call_started` durable event for this exact run and prove `timeoutMs=2700000` (or the exact equivalent durable field proving 2700 seconds), not the historical `900000ms` default.
7. Observe read-only until the request reaches terminal/result state and durable delivery settles.
8. Prove outbox final state is 0 for the tested lifecycle, subject to existing unrelated outbox ownership being explicitly distinguished rather than silently ignored.
9. Prove controller bytes/SHA, provider/model configuration, and published tag remain unchanged.
10. Prove no duplicate owner/run/result/delivery/recovery/fallback was created.
11. Publish exact timestamps, IDs, event ordering, timeout evidence, provenance, and all pre/post state.

## Explicit exclusions

- Exactly one semantic Dashboard/Web Session request only.
- Do not send an OpenAI request; OpenAI smoke is a separate task.
- Do not press Send/Enter twice.
- No retry, recovery, fallback, resend, manual dispatch, duplicate-send, second session, provider switch, or model switch.
- No runtime configuration mutation.
- No provider/model/auth/routing mutation.
- No timeout mutation during the test.
- No controller mutation.
- No installation/release/tag mutation.
- No force push or history rewrite.
- If the first UI activation becomes ambiguous, treat it as consumed and resolve by read-only durable inspection.
- Do not manually change timeout values to make the assertion pass.

## PASS criteria

PASS requires all of the following for the one tested lifecycle:

1. Installed candidate provenance matches `c15b2f61...` and tested source lineage includes CNX-340A.
2. Real provider/model route is `ollama/qwen3.8:27b` using native `ollama` API.
3. Durable `model_call_started` evidence for this exact run records `timeoutMs=2700000` (or an unambiguous equivalent of 2700s).
4. The historical `timeoutMs=900000` is absent for the tested model-call lease.
5. The request crosses the previously observed long-running region without the 900s lease governing it.
6. Complete durable Session/Ticket/Run/model-call/Result/Delivery correlation exists for the same lifecycle.
7. Terminal result and delivery settle successfully; outbox reaches the expected final state.
8. Controller/config/provider/model/tag are unchanged.
9. No duplicate owner, retry, recovery, fallback, or competing lifecycle is created.
10. No failure classification remains unresolved.

## Important distinction

The task is not required to wait 2700 seconds merely because the configured timeout is 2700 seconds. The proof target is the durable lease authority recorded at model-call start. Actual elapsed duration should be reported, but elapsed time alone must not be used as a substitute for the exact timeout field.

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

## Stop/report contract

Publish:
`docs/operations/coordination/reports/CNX-20260914-340C-live-timeout-requalification-report.md`

Include the exact tested run/session/ticket IDs, model-call identity, recorded timeout, event timestamps, artifact SHA, controller/config hashes, pre/post database counts, and verification commands. Then stop for independent ChatGPT review. Hermes must not self-close or self-accept CNX-340C.
