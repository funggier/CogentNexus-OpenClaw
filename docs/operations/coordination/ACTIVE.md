# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `TASK171_EVIDENCE_CONTRACT_COMPLETION_HERMES`
Current authorization: `CNX-20260831-172_HERMES_TASK171_EVIDENCE_CONTRACT_COMPLETION`
Task ID: `CNX-20260831-172`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-172-hermes-task171-evidence-contract-completion.md`](tasks/CNX-20260831-172-hermes-task171-evidence-contract-completion.md)

Task 172 is the evidence-contract completion checkpoint for the already-executed Task-171 exactly-one-Send semantic experiment.

## Task 171 review state

Task-171 report:

`reports/CNX-20260831-171-hermes-dashboard-exactly-one-send-durable-delivery-reacceptance.md`

ChatGPT review:

`reviews/CNX-20260831-171-hermes-dashboard-exactly-one-send-durable-delivery-reacceptance-review.md`

Disposition:

`REWORK_REQUIRED — TASK171_SEMANTIC_RESULT_COHERENT_BUT_VERIFICATION_PACKET_MISSING`

The published Task-171 evidence is substantively consistent with a successful repaired durable-delivery path, but the mandatory acceptance matrix, Reviewer Verification Packet, transcript/marker immutable identities, and several field-level evidence pointers are missing from the report contract.

This is an evidence/report gap, not authorization to repeat the semantic experiment.

## Frozen Task-171 action under review

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- OpenClaw: `2026.7.1-2`
- Nonce: `T171-20260831T020446Z-3142A528`
- Session: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`

The Task-171 semantic Send count for this acceptance attempt is frozen at exactly `1`.

## Current gate

Hermes/Codex must use preserved Task-171 evidence plus read-only inspection only to complete:

- the nine-row Task-171 acceptance matrix;
- 5-10 claim Reviewer Verification Packet;
- transcript SHA-256 and exact native marker/identity binding;
- full model/request identity;
- exact durable-row field binding and text/hash identity;
- run-scoped duplicate/recovery/outbox proof;
- SHA-256 hashes for critical local evidence artifacts;
- residual uncertainty and publication/change fence.

If any property cannot be proven from the existing Task-171 action, mark it `UNPROVEN` or `FAIL`. Do not replay the experiment.

## Hard fence

Task 172 authorizes zero semantic actions.

No Dashboard Send, Enter submission, `chat.inject`, alternate semantic input, manual inference, recovery/regeneration, installer/uninstall/reinstall/reset/rollback, runtime restart/lifecycle mutation, manual DB/Ticket/result/outbox/delivery/transcript mutation, source/product/test/workflow change, OpenClaw/dependency upgrade, release/promotion, merge, or force push.

Task 172 may perform only read-only inspection/hashing and publish its report. Final semantic acceptance remains with ChatGPT review.
