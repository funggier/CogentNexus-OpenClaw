# CNX-20260906-273 — Discord Direct Durable Delivery Boundary Repair

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-272`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Repair the Discord Direct delivery contract exposed by Task272: a Discord final can be visibly delivered while CNX fails to durably bind/confirm that exact final before the direct-delivery deadline.

The repair must give Discord Direct a pre-transport durable final-payload authority with exact owner-session/generation/idempotency semantics, instead of depending on best-effort `message_sent` correlation.

## Root-cause constraints to preserve

Treat these as required design facts unless fresh source evidence disproves them:

1. Installed OpenClaw is `2026.7.1-2` / `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`.
2. Its outbound `message_sending` / `message_sent` contract does not reliably carry `runId`; `sessionKey` correlation is optional and cannot safely disambiguate concurrent turns.
3. CNX generic `reply_dispatch` currently consumes `event.runId` only.
4. The stronger `v091-dashboard-verified-delivery` staging/marker path currently excludes ordinary Discord Direct from durable ownership.
5. Task272 live evidence produced a visible Discord reply with zero `cnx_assistant_delivery` rows and no `delivery_confirmed_at`, followed by fail-closed timeout.

## TDD requirements

Use RED -> minimal production repair -> GREEN.

At minimum, RED tests must reproduce the production-shaped Discord Direct path through registered hooks rather than only calling a helper directly:

- owner key shaped `agent:<agent>:discord:channel:<id>`;
- exact Direct Ticket/run/session/generation;
- `reply_dispatch` where `event.runId` is absent but `ctx.runId` is present when that is the installed OpenClaw contract observed by the harness;
- one final text payload;
- durable row must exist **before** native transport completion is trusted;
- marker/idempotency identity must be bound to that exact Ticket + generation;
- final settlement must terminal the correct Ticket exactly once;
- a later timeout scan must not clear/regenerate an already durable final.

Also prove:

1. Discord Direct does not depend on `message_sent.runId`.
2. Same-session concurrent/direct-turn ambiguity cannot settle the wrong Ticket.
3. Stale/deleted/wrong-generation session authority cannot stage or confirm the final.
4. Duplicate same-text final observation is idempotent; changed text for the same durable identity fails closed.
5. `NO_REPLY`/silent-sentinel semantics remain correct for Discord.
6. Dashboard Direct regression coverage remains GREEN and semantically unchanged.
7. Existing direct recovery, session recreation/generation, and durable-delivery boundary suites remain GREEN.

Prefer reusing/generalizing the proven verified-delivery primitive instead of creating a second Discord-only persistence scheme.

## Validation

Run focused tests for the modified delivery modules, then the full plugin suite, build/package/validation checks, `git diff --check`, and exact-candidate GitHub Actions. If production source changes, exact-SHA CI must be green before report publication.

## Hard fences

```text
live Discord/Dashboard semantic sends             = 0
live OpenClaw session Delete/reset                 = 0
manual live Ticket/session/SQLite mutation         = 0
recovery replay/redelivery/disposition              = 0
installer/install-over/uninstall/reset             = 0
Gateway/provider/service lifecycle mutation        = 0
Scheduled Task mutation                            = 0
release/tag/default-branch promotion               = 0
force push/history rewrite                         = 0
```

Task272's live Delete/test authority is parked and must not be consumed inside Task273.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-273-discord-direct-durable-delivery-boundary-repair.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
