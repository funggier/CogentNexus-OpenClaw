# CNX-339 — Dashboard End-to-End Durable Lifecycle Acceptance

Status: `READY_FOR_HERMES`
Task ID: `CNX-339`
Parent: `CNX-339A`
Execution mode: `SINGLE_EXECUTOR`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authority: `CNX-339A`

## Objective

Perform one bounded, real Dashboard/Web Session lifecycle acceptance against the already-approved installed candidate and production controller. Prove the complete durable lifecycle from one fresh Dashboard session and one semantic request through inference, result, delivery, and outbox settlement.

This task is authorized only after `CNX-339A = PASS`. It is not an authorization to alter runtime, release, provider, model, or controller configuration.

## Accepted prerequisites

- `CNX-338A = PASS`
- `CNX-338R.1 = PASS`
- `CNX-338R = PASS`
- Installed candidate SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Production controller: `schemaVersion=2`, `cnxMode=active`, `generation=101`, SHA-256 `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98`
- Provider/model: `ollama/qwen3.8:27b`
- Provider timeout: `2700s`; agent timeout: `2700s`
- Published tag `v0.9.5`: `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`

## Exact live-test scope

1. Complete the fresh read-only provenance, health, controller-integrity, database, and duplicate-owner preflight.
2. Create exactly one fresh Dashboard/Web Session. Prove its new session identity, empty rendered conversation, and empty composer before typing.
3. Submit exactly one semantic request through the real Dashboard UI. Do not press Enter or use another semantic surface.
4. Prove Ticket admission and bind the admitted Ticket to the fresh Session.
5. Correlate Session, Ticket, Run, Result, and Delivery identities independently from durable evidence.
6. Prove real `ollama/qwen3.8:27b` inference for this exact lifecycle, including the model-call identity and generation binding.
7. Observe read-only until the exact run reaches its terminal/result state and durable delivery settles.
8. Prove durable Result evidence, durable Delivery evidence, and completed outbox state for this same Ticket/Run/Session chain.
9. Prove controller bytes and SHA-256 are unchanged before versus after the test.
10. Prove duplicate-owner exclusion: no duplicate lifecycle owner, Ticket, Run, Result, Delivery, recovery, or competing outbox owner was created.
11. Record exact timestamps, identifiers, event order, bounded logs, pre/post counts, and evidence paths.

## Explicit exclusions

This is one acceptance attempt only. Do not test or invoke retry, recovery, fallback, resend, manual dispatch, duplicate Send, alternate transport, or any second Dashboard session. Do not mutate runtime configuration, provider/model, timeouts, controller state, plugin installation, services, release history, or the `v0.9.5` tag. If the first UI activation is ambiguous, treat it as consumed and resolve only by read-only durable inspection.

## PASS criteria

PASS requires all scope items to be proven for one fresh Session and one semantic request, with Ticket-first admission, real Ollama inference, complete durable identity correlation, durable result and delivery, completed outbox, unchanged controller integrity, and duplicate-owner exclusion. Missing or contradictory evidence is not PASS.

## Stop/report contract

Publish the matching report under `docs/operations/coordination/reports/`, bind every claim to the exact tested runtime/candidate identity, and stop for independent ChatGPT review. Do not execute this task during CNX-339A.
