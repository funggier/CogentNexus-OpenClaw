# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `FINAL_POST_LIFECYCLE_DASHBOARD_SEMANTIC_DURABLE_DELIVERY_HYBRID`
Current authorization: `CNX-20260831-186_HERMES_FINAL_POST_LIFECYCLE_DASHBOARD_SEMANTIC_DURABLE_DELIVERY_ACCEPTANCE`
Task ID: `CNX-20260831-186`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
UI actor: User
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-186-hermes-final-post-lifecycle-dashboard-semantic-durable-delivery-acceptance.md`](tasks/CNX-20260831-186-hermes-final-post-lifecycle-dashboard-semantic-durable-delivery-acceptance.md)

## Accepted state

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact frozen candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Required active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Accepted plugin fingerprint:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

Task 183 reset:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Task 184 uninstall/external preservation:

`ACCEPTED_PASS — QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_ACCEPTED`

Task 185 fresh reinstall:

`ACCEPTED_PASS — FRESH_REINSTALL_POST_UNINSTALL_ACCEPTED`

The live machine is freshly reinstalled on the accepted candidate with OpenClaw `2026.7.1-2`, plugin/runtime health accepted, provider Ollama selected, and the semantic durable baseline clean at zero across tickets/events/outbox/delivery/model/recovery/sessions.

## Task-186 authorization

After a fresh read-only authority/provenance/runtime/durable preflight, Task 186 authorizes exactly one real Dashboard semantic turn to prove:

`one human Send → one Ticket → one model call → one durable assistant delivery → one logical assistant result`

PASS requires unique correlation from a frozen Task-186 nonce through Ticket/session/run/model/delivery/UI evidence, no duplicate logical work, no recovery, outbox drain to zero, and healthy runtime afterwards.

## Human-controlled UI gate

- The user controls Dashboard navigation/New Session/clicks.
- The user focuses/selects the intended composer field.
- Hermes may type/paste only the already frozen Task-186 nonce/test text after that focus exists.
- Hermes must not press Enter as Send, click Send, or use `chat.inject`/semantic injection.
- The user presses Send exactly once.
- Hermes/Codex then performs read-only Ticket/model/durable-delivery/UI correlation.

If the turn becomes slow or ambiguous, do not Send again and do not retry/regenerate/recover. Inspect the same durable turn and report the bounded disposition.

## Hard fence

Human Dashboard Send maximum: `1`.
Hermes/Codex Send: `0`.
Semantic injection/chat.inject: `0`.
Second Send/retry: `0`.
Manual recovery/regeneration: `0`.

No reset, uninstall, install/reinstall/install-over, executor lifecycle helper, manual Gateway/Ollama lifecycle action, manual DB/config/transcript/route repair, source/product/test/workflow/dependency edit, release/tag/merge, or force push.

After Task-186 report publication, stop for ChatGPT review. No second semantic action is authorized.
