# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_DASHBOARD_EXACTLY_ONE_SEND_DURABLE_DELIVERY_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-171_HERMES_DASHBOARD_EXACTLY_ONE_SEND_REACCEPTANCE`
Task ID: `CNX-20260831-171`
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

[`tasks/CNX-20260831-171-hermes-dashboard-exactly-one-send-durable-delivery-reacceptance.md`](tasks/CNX-20260831-171-hermes-dashboard-exactly-one-send-durable-delivery-reacceptance.md)

Task 171 is the bounded live semantic durable-delivery reacceptance checkpoint.

## Accepted installed checkpoint

Accepted product repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Installed candidate fingerprint accepted by Task 170:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

Task-170 package SHA-256:

`8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`

Pinned OpenClaw:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

Task-170 disposition:

`ACCEPTED_PASS — REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_PROVENANCE_HEALTH_ACCEPTED`

## Current gate

Hermes/Codex must perform preflight against the accepted installed checkpoint, generate one unique nonce, issue exactly one Dashboard semantic Send, and then collect native transcript/durable delivery/Ticket/model/recovery/post-health evidence.

After the Send is issued, retry is prohibited regardless of timeout, failure, missing evidence, or ambiguity.

## Hard fence

Authorized: read-only preflight; exactly one Dashboard semantic Send; read-only post-action observation; Task-171 report publication.

Prohibited: second Send; `chat.inject`; alternate semantic surface; manual model/recovery invocation; installer/uninstall/reinstall/reset/rollback; runtime restart/lifecycle mutation; manual DB/Ticket/result/outbox/delivery/transcript mutation; production repair; OpenClaw/dependency upgrade; release/promotion; merge; force push.

If the experiment fails or remains unproven, preserve the state and report it. No successor action is authorized before ChatGPT review.
