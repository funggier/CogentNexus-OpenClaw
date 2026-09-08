# CNX-20260906-272 — ChatGPT Setup-Settlement Blocker Review

## Verdict

`ACCEPT_BLOCKED_STOP__DISCORD_DIRECT_DELIVERY_BOUNDARY_DEFECT__SOURCE_REPAIR_REQUIRED`

## Review basis

Task272 Phase A2 correctly stopped before consuming the authorized session Delete. The setup Discord lifecycle was distinct from the excluded historical Ticket owner, but it did not reach the required clean durable-delivery state.

Accepted live evidence from the Hermes report:

- sacrificial session key: `agent:main:discord:channel:1366635842554036314`;
- OpenClaw sessionId: `68ad6250-1d3a-4dac-a1b1-f1da84a10cda`;
- CNX generation: `0`;
- setup Ticket: `CNXT-195f626e-88b8-403d-a994-918fee9ec09c`;
- model call ended `completed` after `864107 ms`;
- the human reported a visible Discord reply;
- nevertheless `delivery_confirmed_at` remained null, no `cnx_assistant_delivery` row existed for the session, and the Ticket remained `accepted` with `failure_class='interrupted'` / `Direct response delivery was not confirmed before deadline`;
- Delete/reset, recovery replay/redelivery/disposition, manual DB mutation, and Hermes semantic sends all remained zero.

The stop was therefore correct. A visible Discord reply is not sufficient evidence to waive the durable clean gate.

## Independent source finding

The current CogentNexus delivery layers are semantically split:

1. `plugins/cogentnexus-openclaw/src/index.ts` generic Direct settlement registers `reply_dispatch`, but correlates it from `event.runId` only. Its `message_sent` fallback may recover a run from the session map, but that is a later best-effort observation path.
2. The installed OpenClaw version `2026.7.1-2` at exact upstream commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` explicitly documents that outbound `message_sending` / `message_sent` do **not** yet carry reliable `runId`; plugins are told to correlate by optional `sessionKey`, with the stated caveat that this cannot disambiguate concurrent turns in one session.
3. `v091-dashboard-verified-delivery.ts` has the stronger pre-transport durable staging/marker contract, but the existing regression suite intentionally treats a Discord Direct Ticket as `not-dashboard-direct`. In the current implementation, the ordinary `reply_dispatch` staging call also invokes `stageDashboardDirectResult(path,{runId,text})` without Discord owner/session/surface authority.

This leaves Discord Direct on a weaker legacy settlement path while the response-ready timeout still requires a durable confirmation. Task272 reproduced the consequence: transport was visibly successful to the human, but CNX could not durably prove that exact final and therefore timed out fail-closed.

## Required repair direction

Do not fix this by weakening the timeout, accepting human-visible output as proof, or blindly trusting `message_sent`.

The successor should make Discord Direct use an exact pre-transport durable delivery authority equivalent in strength to the accepted Dashboard boundary, including exact owner session/generation and idempotent final payload identity. `message_sent` may remain supplemental observation, not the sole durable proof.

The repair must preserve:

- Dashboard Direct semantics and existing accepted tests;
- `NO_REPLY`/silent-sentinel handling;
- no duplicate visible output/regeneration after a durable final exists;
- session-generation fencing and deletion semantics;
- fail-closed behavior when final payload identity cannot be durably captured;
- no false correlation between concurrent turns on the same Discord session.

## Live authority

No live Delete, setup/test message, Ticket disposition, replay/redelivery, install-over, Gateway/provider mutation, or manual SQLite mutation is authorized by this review. Task272's Delete authority remains unconsumed and should stay parked until a repaired candidate is reviewed, deployed, and separately requalified.
