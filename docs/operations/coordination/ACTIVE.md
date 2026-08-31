# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `TASK171_READ_ONLY_UI_DUPLICATE_VERIFICATION_HERMES`
Current authorization: `CNX-20260831-173_HERMES_TASK171_READ_ONLY_UI_DUPLICATE_VERIFICATION`
Task ID: `CNX-20260831-173`
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

[`tasks/CNX-20260831-173-hermes-task171-read-only-ui-duplicate-verification.md`](tasks/CNX-20260831-173-hermes-task171-read-only-ui-duplicate-verification.md)

Task 173 is a zero-semantic-action UI verification checkpoint for the already-executed Task-171 experiment.

## Task 171/172 review state

Task-171 semantic Send count remains permanently frozen at exactly `1`.

Task-172 completion report materially proved the native/durable path, including transcript/trajectory hashes, native marker identity, one model call, one durable delivery row, completed Ticket, zero recovery/outbox conflicts, and preserved runtime provenance.

ChatGPT Task-172 review disposition:

`REWORK_REQUIRED — TASK171_NATIVE_DURABLE_PATH_PROVEN_UI_DUPLICATE_CRITERION_UNPROVEN`

The only remaining acceptance gap is the visible Dashboard component of Task-171 criterion 8. Task 172 itself states that final visible Dashboard nonce counts were not proven, so the conjunctive "no duplicate UI/native result" criterion cannot yet be accepted as complete.

## Frozen Task-171 identity

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- OpenClaw: `2026.7.1-2`
- Nonce: `T171-20260831T020446Z-3142A528`
- Expected assistant result: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Session: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`

## Current gate

Hermes/Codex must inspect the existing Dashboard session/history read-only and prove or fail to prove:

- exactly one visible user message containing the frozen nonce;
- exactly one visible assistant message containing the exact expected result;
- no duplicate visible assistant result;
- no duplicate visible user nonce.

Use screenshots plus DOM/accessibility/message-node counting when available. If history virtualization or unavailable UI prevents a complete count, report `UNPROVEN`; do not infer PASS from native evidence.

## Hard fence

Task 173 authorizes semantic action count `0`.

No Send, Enter submission, composer typing/paste, `chat.inject`, alternate semantic input, model invocation, recovery/regeneration, installer/uninstall/reinstall/reset/rollback, runtime restart/lifecycle mutation, manual DB/Ticket/result/outbox/delivery/transcript mutation, source/product/test/workflow change, OpenClaw/dependency upgrade, release/promotion, merge, or force push.

Only read-only Dashboard/history observation, non-semantic scroll/navigation, screenshots/DOM/accessibility extraction, evidence hashing, read-only identity correlation, and Task-173 report publication are authorized.
