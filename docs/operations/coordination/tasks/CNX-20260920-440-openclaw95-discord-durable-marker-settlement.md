# CNX-20260920-440 — OpenClaw 9.5 Discord Durable Marker Settlement

Status: `IMPLEMENTED_AWAITING_LIVE_REQUALIFICATION`

Parent: `CNX-20260919-427`

## Problem

A genuine Discord turn completed model execution and visibly delivered its reply, but its CNX Ticket remained `accepted` and no `cnx_assistant_delivery` row was created.

Exact observed lineage:

- session: `eb063e85-a2c1-4a94-abb7-f1e66a2243c1`
- run: `da30a458-c410-402b-a2ea-a48c5492129a`
- Ticket: `CNXT-71cc73a6-2e05-494b-bde0-c53ccc9757a7`
- exactly one Ticket / model call / inference attempt
- Ticket preceded model authority by about 59 ms
- OpenClaw run ended `done`
- user visibly received the Discord reply
- CNX log: runId-less/ambiguous `message_sent` receipt
- durable delivery row: absent
- Ticket terminal settlement: absent

The session was subsequently deleted through the supported OpenClaw lifecycle, cancelling the residual accepted Ticket.

## Root cause

OpenClaw 2026.9.5 places exact outbound final identity on the `reply_payload_sending` EVENT:

- `event.channel`
- `event.sessionKey`
- `event.runId`

Its `PluginHookMessageContext` exposes `channelId`, not necessarily `channel` or `messageProvider`.

The production v0.9.5 Discord adapter incorrectly gated on `ctx.channel` / `ctx.messageProvider` and primarily consumed identity from context. Therefore the live `reply_payload_sending` path returned before staging a durable delivery.

OpenClaw 2026.9.5 also documents that outbound `message_sent` does not reliably carry `runId`. It does, however, carry the exact sent `content`.

## Repair

`plugins/cogentnexus-openclaw/src/v095-delivery-discord.ts` now:

1. recognizes Discord from `event.channel` first, then context fallbacks including `ctx.channelId`;
2. takes `runId/sessionKey` from the event first for pre-transport staging;
3. stages the exact Ticket/inference/generation before native Discord transport;
4. injects the existing unique CNX delivery marker into native text;
5. settles a runId-less successful `message_sent` only when:
   - the sent content contains one exact pending CNX marker;
   - the marker resolves to exactly one pending Discord delivery in the exact session;
   - owner generation is still current and active;
6. preserves fail-closed behavior when no marker, multiple matches, stale generation, or ambiguous ownership exists.

The adapter never falls back to "latest Ticket" or same-session run inference.

## Validation

TDD RED reproduced the exact OpenClaw 9.5 event/context shape: staging returned undefined before the repair.

GREEN:

- focused adapter: 6/6
- delivery/core/lifecycle affected suite: 19/19 across 6 files
- release-entry integration proves the production `v091-release-entry` wiring keeps the v095 Discord adapter live through legacy fences
- concurrent same-session A/B proof settles only the marker-selected run
- existing runId-less/no-marker receipt remains ignored
- `npm run plugin:validate`: PASS

Implementation commit:

`a4f27ad097e721edfe566a7495864b7e15ae88e8`

## Live qualification blocker

The first supported install-over attempt from the exact implementation commit failed before plugin mutation because the external CNX supervisor restarted an unresponsive Gateway concurrently with the installer native handoff.

That distinct installer/supervisor coordination issue is tracked as CNX-441.

## Classification

Source qualification:

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_SOURCE_GREEN`

Final live classification remains pending supported deployment + one genuine Discord acceptance.
