# CNX-20260901-205 Review — Correct-Room Discord Requalification

Disposition: `ACCEPT_FAIL_DURABLE_CORRELATION__FORENSIC_FOLLOWUP_REQUIRED`

## Accepted result

Task 205 correctly proved the designated Discord channel numerically before the one authorized human Send:

- channel ID: `1531199905673252946`
- owner session: `agent:main:discord:channel:1531199905673252946`
- frozen repaired candidate: `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- installed fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Fresh managed health passed before the Send. Exactly one human Discord Send was consumed, with no retry, regenerate, second message, second room, bot/API send, lifecycle mutation, or manual state repair.

The nonce produced exactly one Ticket and one direct Ollama model call. The model call completed and the Ticket recorded `response_ready`, but the Ticket remained `accepted`, `delivery_confirmed_at` remained null, and no matching delivery confirmation was recorded during the bounded settlement window. Runtime health remained green.

Therefore Task 205 disposition `FAIL_DURABLE_CORRELATION` is accepted.

## What is proven

The live failure boundary is now clean:

`human Discord Send -> Ticket -> direct model call -> response_ready -> [missing delivery settlement]`

The earlier SQLite admission defect is not reproduced by this Send. No `before_agent_run` failure occurred. No recovery or outbox residue was created.

## What is not yet proven

Task 205 did not independently prove whether:

1. the native Discord reply was actually transmitted but CogentNexus failed to correlate the outbound receipt;
2. the Discord reply was never transmitted;
3. `reply_dispatch` fired without usable run correlation;
4. `message_sent` fired without usable `runId`/`sessionKey` correlation; or
5. another delivery-path condition prevented settlement.

No product repair is authorized until this distinction is resolved.

## OpenClaw baseline contract relevant to follow-up

Accepted OpenClaw baseline: `2026.7.1-2 (0790d9f)`.

The baseline plugin hook type contract explicitly states that outbound `message_sending` / `message_sent` must not rely on `runId`; it is not plumbed through the outbound path. Outbound `sessionKey` is optional and is present only when the outbound dispatch has a resolvable `OutboundSessionContext`.

CogentNexus currently resolves `message_sent` delivery by:

1. using `event.runId` when present;
2. otherwise matching `event.sessionKey` exactly against its in-memory `runSessions` map;
3. otherwise returning without settlement.

The baseline also defines `reply_dispatch.runId` as optional.

These contracts make a missing-correlation mechanism plausible, but Task 205 alone does not prove which hook/event shape occurred on the live Discord path.

## Successor boundary

A successor task must be read-only against the existing Task-205 evidence window first. It must not consume a new Discord Send.

It should inspect retained OpenClaw/Gateway logs, session transcript/outbound traces and CogentNexus diagnostics around the exact Task-205 run:

- Ticket: `CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6`
- run: `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5`
- call: `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1`
- channel: `1531199905673252946`
- response_ready: `2026-08-31T19:06:52.333Z`

Only after the exact native-delivery/hook shape is classified may repository TDD begin.
