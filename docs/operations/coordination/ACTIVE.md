# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_BOUNDED_REAL_USER_MESSAGE_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`
Current authorization: `FINAL_SEMANTIC_ACCEPTANCE_AUTHORIZED`
Task ID: `CNX-20260826-076`
Updated: 2026-08-26 20:00 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-076-final-semantic-ticket-ollama-delivery-acceptance.md`](tasks/CNX-20260826-076-final-semantic-ticket-ollama-delivery-acceptance.md)

## Task 075 review

Task 075 reported:

`PASS_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`

Install-over source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Report HEAD:

`38a8bfa345ea6bf808870eb4c99efdafa7edf3e2`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`

Review commit:

`665da6c3df05b98aa1a6e06115db80b7ba0967a0`

## Accepted live state

- supported install-over from exact corrected source completed exactly once;
- installed skill tree is byte-for-byte source/live parity with `79b51ed...` for the compared production tree;
- recovery preflight/upgrade path behaved coherently with no fresh transaction;
- exactly one canonical v0.9.3 plugin generation remains active after supported rollover;
- launcher and Supervisor remain CogentNexus-owned runtime bound with no durable Hermes/Codex/temp dependency;
- five post-install-over natural PT1M ticks again proved `NO_FLASH_MULTI_TICK_PROVEN`;
- final MANAGED/Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite health passed;
- no product semantic LLM smoke has yet been executed.

## Authorized Task 076 operation

Exactly one bounded real owner-session semantic message through a supported OpenClaw user-message surface. Prove the installed plugin commits one Ticket before inference, the normal OpenClaw run uses provider Ollama, the direct Ticket records response-ready and confirmed final delivery, the user-visible response contains the unique nonce, and no duplicate Ticket/delivery side effect occurs.

Do not use TicketStore/SQLite/manual hook/model shortcuts as the semantic input. Do not resend the acceptance message if slow.

## Hard fences

No install/install-over/uninstall/reset/cleanup, no manual SQLite mutation, no provider/model/config change, no reboot, no merge/tag/release. Authorized mutation is only the one semantic message and its natural Ticket/session/Ollama/delivery effects.

## Completion gate

If Task 076 reports `PASS_FINAL_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`, ChatGPT must independently review the real user-entry path, Ticket-first runtime ordering, correlated Ollama inference, terminal delivery evidence, idempotency accounting, post-run health and report-only publication fence.

Independent acceptance of that result completes the agreed current v0.9.3 OpenClaw acceptance scope.
