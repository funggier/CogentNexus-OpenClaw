# CNX-20260920-440 — OpenClaw 9.5 Discord Durable Marker Settlement

Status: `COMPLETE`

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

Final live classification: `OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`.

## Supported deployment qualification

The CNX-441 repaired install-over from exact candidate HEAD
`5263b6aed9acf77a4db39be47c4d96fecfe8a431` completed successfully.

Evidence:

- LConnect process session `proc-1789885920190-35`, PID `10220`;
- installer terminal exit code `0`;
- live v095 adapter SHA-256 equals candidate:
  `7809B18C4BAE1209624D5E69112722EF9AD7F5E39A92A2815C6889DFF6C646A1`;
- controller committed active/managed generation `111`;
- Gateway healthy, event loop settled;
- Discord ready/connected;
- supervisor restored Enabled/Ready with Last Result `0`;
- target Discord channel has zero non-terminal CNX Tickets before final acceptance;
- current qwen3.8 context is `24576`, keep-alive `2h`;
- Ollama has no resident model at baseline.

The installed code was live-requalified successfully. CNX-440 final classification is `OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`.

Deployment checkpoint:

`docs/operations/coordination/reports/CNX-20260920-440-openclaw95-discord-durable-marker-deployment-checkpoint.md`

## Final Discord acceptance — GREEN

The operator sent exactly one genuine Discord turn on channel `1391855033993138217`:

`@Ce CNX427_FINAL_ACCEPTANCE_20260920_A1 Reply exactly: CNX427_FINAL_OK_20260920_A1`

Observed lineage:

- physical OpenClaw session: `06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`;
- authoritative run: `e683efcf-b00e-4ee9-bb11-cac0da94a840`;
- CNX Ticket: `CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3`;
- inference attempt: `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- durable delivery: `27`;
- owner generation: `7`.

Ordering and cardinality from the clean pre-send baseline:

- Tickets: `47 -> 48` (+1);
- direct model calls: `35 -> 36` (+1);
- inference attempts: `33 -> 34` (+1);
- assistant deliveries: `26 -> 27` (+1);
- exactly one new target-channel Ticket;
- exactly one Ticket for the authoritative run;
- Ticket accepted at `2026-09-20T07:04:19.655Z`;
- model call started at `2026-09-20T07:04:19.714Z`;
- inference attempt started at `2026-09-20T07:04:19.726Z`;
- Ticket persistence therefore preceded model-call authority by about 59 ms;
- no direct-recovery row exists for the accepted Ticket;
- no duplicate Ticket, duplicate model call, duplicate inference attempt, or stale-generation settlement occurred.

Terminal delivery proof:

- model call ended `completed` at `2026-09-20T07:22:51.387Z`;
- inference attempt ended `completed` at `2026-09-20T07:22:51.396Z`;
- `response_ready` at `2026-09-20T07:22:51.460Z`;
- durable delivery row 27 was created at `2026-09-20T07:22:51.578Z`;
- durable idempotency key:
  `cnx-discord:CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3:g7:cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- delivery settled as `delivered / confirmed`;
- receipt evidence type:
  `discord-message-receipt-marker`;
- `delivery_confirmed` event count = `1`;
- `completed` event count = `1`;
- Ticket terminal status = `completed`;
- exact delivered text:
  `CNX427_FINAL_OK_20260920_A1`.

OpenClaw trajectory independently recorded:

- finalStatus = `success`;
- timedOut = `false`;
- provider/model = `ollama / qwen3.8:27b`;
- input tokens = `12105`;
- output tokens = `19`;
- compaction count = `0`;
- assistant text = `CNX427_FINAL_OK_20260920_A1`;
- target session status = `done`.

The operator supplied visual Discord screenshots confirming exactly one visible assistant response with the exact expected text.

Current local-model policy remains intentionally unchanged:

- primary model `ollama/qwen3.8:27b`;
- `contextWindow=24576`;
- `num_ctx=24576`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

The live acceptance used 24K context successfully. During execution llama-server private memory reached about 21.4 GB and free physical RAM was observed as low as about 1.3 GB, so 24K remains the operator-approved default unless future workload proves insufficient.

Final classifications:

`CNX427_EXTERNAL_INGRESS_TICKET_FIRST_DURABLE_DISCORD_GREEN`

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`

Final acceptance report:

`docs/operations/coordination/reports/CNX-20260920-427-440-final-discord-acceptance-report.md`
