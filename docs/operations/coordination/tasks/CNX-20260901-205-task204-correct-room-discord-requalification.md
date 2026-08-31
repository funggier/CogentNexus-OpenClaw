# CNX-20260901-205 — Task 204 Correct-Room Discord Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-204`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Repeat only the final Discord semantic/durable acceptance in the **correct designated room** after Task 204's single Send was made in the wrong room.

Task 204 already completed stale reset cleanup and restored the exact repaired candidate to healthy MANAGED state. This task must not replay those lifecycle actions unless fresh read-only evidence shows drift; if drift exists, stop for review rather than forcing convergence.

## Immutable authorities

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published `v0.9.3` target remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Correct Discord owner session:

`agent:main:discord:channel:1531199905673252946`

Correct numeric Discord channel ID:

`1531199905673252946`

## Accepted Task-204 starting state

Task 204 ended with:

- Host `managed`;
- startup adapter enabled/Ready;
- plugin enabled/loaded;
- Gateway healthy;
- Ollama selected/reachable/healthy/ready;
- delivery READY / outbox 0;
- recovery READY / no active incident;
- SQLite integrity `ok`;
- exact repaired installed fingerprint;
- stale reset/lifecycle residue absent.

The wrong-room nonce from Task 204 had no Ticket/model/delivery/outbox/recovery match and no durable count delta. It is historical evidence only and must not be reused.

## New semantic budget

The user explicitly requested a new attempt because the prior message was sent in the wrong Discord room.

Task 205 grants a new independent budget:

- human Discord Send: exactly `1 / 1`;
- Hermes/bot/API/injected Send: `0`;
- retry/regenerate: `0`;
- second message: `0`;
- second room: `0`.

This is not a retry under Task 204. It is a new qualification attempt with a new nonce after an explicit operator correction.

## Phase A — fresh read-only runtime gate

Before touching Discord, capture fresh:

1. installed fingerprint — must equal exact repaired candidate;
2. ownership verify — PASS;
3. Host mode — `managed`;
4. desired Gateway/provider — running;
5. startup adapter — installed/enabled/Ready;
6. plugin — enabled/loaded/no error;
7. Gateway — healthy/listening;
8. selected provider — Ollama, healthy/ready;
9. delivery — READY, pending outbox 0;
10. recovery — READY, no active incident/unexpected recovery attempt;
11. SQLite `PRAGMA integrity_check` — `ok`;
12. no reset/uninstall/install/install-over/enable/disable lifecycle residue against the state root.

If any of these materially fails, stop with `FAIL_PRE_SEND_HEALTH`. Do not run lifecycle commands and do not consume the Discord Send budget.

## Phase B — mandatory correct-room identity gate

**Do not generate the nonce until the correct room is proven.**

Hermes must establish that the Discord surface in which the operator will type is the designated numeric channel/session:

`1531199905673252946`

Use authoritative/read-only evidence where available, for example current Discord/session/channel metadata, OpenClaw Discord session mapping, or another exact numeric channel binding.

Rules:

- a room name alone is insufficient;
- a Discord window title alone is insufficient;
- do not infer the numeric ID from visual similarity;
- do not send a probe message to discover the ID;
- do not consume the Send budget while room identity is ambiguous.

Hermes must present the operator with an explicit confirmation line before giving the message, in this shape:

`CONFIRMED TARGET CHANNEL ID: 1531199905673252946`

If exact numeric identity cannot be established, stop with `BLOCKED_CORRECT_ROOM_IDENTITY` and send nothing.

## Phase C — generate one fresh nonce and wait for the human

Only after Phase A and Phase B pass, generate a fresh nonce not used anywhere earlier:

`CNX205-<UTC timestamp>-<short random suffix>`

Tell the user to send manually in the already-confirmed channel exactly:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then stop and wait for the user to say:

`ส่งแล้ว`

Do not send on behalf of the user.

## Phase D — durable correlation

After the user says `ส่งแล้ว`, perform immediate and bounded read-only correlation.

Required accepted shape:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord result -> delivery_confirmed -> completed`

Capture at minimum:

- exact nonce;
- confirmed numeric channel ID;
- owner session key;
- Ticket ID;
- request key / prompt SHA where available;
- run ID;
- direct model-call ID;
- provider/model;
- ordered Ticket events;
- response-ready timestamp;
- delivery-confirmed timestamp;
- terminal Ticket status;
- visible assistant result containing the requested nonce, or authoritative native channel-delivery evidence;
- before/after durable counts;
- outbox and recovery deltas;
- bounded OpenClaw/CNX logs around the run.

## Required negatives

For the Task-205 Send:

- no `before_agent_run hook failed`;
- no duplicate Ticket;
- no duplicate direct model call;
- no duplicate assistant result;
- no Direct Recovery attempt attributable to the Send;
- no retry/regenerate;
- no pending outbox residue;
- no stuck delivery residue;
- no provider substitution;
- no room/session drift away from channel `1531199905673252946`.

Do not fail solely because a Dashboard observer logs `missing-run-correlation` or `missing-append-before-deliver` for a non-Dashboard transport.

A `cnx_assistant_delivery` row is not mandatory for native Discord Direct delivery; Ticket-level `message_sent` / `delivery_confirmed` evidence is accepted.

## Phase E — final health

After correlation, capture read-only:

- Host still managed;
- startup/plugin healthy;
- Gateway healthy;
- Ollama healthy/ready;
- delivery READY / outbox 0;
- recovery READY / no active incident;
- SQLite integrity `ok`;
- exact installed fingerprint unchanged;
- no lifecycle residue.

## Hard fence

Do not:

- rerun installer/install-over;
- run reset/uninstall/reinstall;
- invoke enable/disable/start/stop/restart;
- kill processes;
- mutate config/SQLite/provider/model manually;
- send any Discord message before exact numeric room identity is proven;
- send more than the one authorized human message;
- inject/synthesize Discord traffic;
- edit product/source/test/workflow files;
- mutate Release/tag/assets;
- force push.

## Final dispositions

Use exactly one:

- `PASS`
- `BLOCKED_CORRECT_ROOM_IDENTITY`
- `FAIL_PRE_SEND_HEALTH`
- `FAIL_DISCORD_BEFORE_AGENT`
- `FAIL_DISCORD_SEMANTIC_DELIVERY`
- `FAIL_DURABLE_CORRELATION`
- `FAIL_FINAL_HEALTH`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-205-task204-correct-room-discord-requalification.md`

Include fresh authority SHA, exact room-identity proof, new nonce, one-send ledger, Ticket/model/delivery correlation, negative checks, final health, and mutation ledger. Then stop for ChatGPT review.
