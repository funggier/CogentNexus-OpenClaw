# CNX-20260906-273 — Discord Direct Durable Delivery Boundary Repair

## Disposition

`PASS_SOURCE_TEST_CI__WAITING_FOR_CHATGPT_REVIEW`

Task273 repaired the Discord Direct durable-delivery boundary using strict RED -> minimal production fix -> GREEN. No live semantic, session, database, installer, Gateway, recovery, or release mutation was performed.

## Authority and exact candidate

- Task: `CNX-20260906-273`
- Parent: `CNX-20260906-272`
- Executor: Hermes
- Candidate commit: `04a566aa66e7812a52385fb70e0e4a5834f2f931`
- Remote branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD after validation: `04a566aa66e7812a52385fb70e0e4a5834f2f931`
- Worktree: clean after publication

## Root cause repaired

The installed OpenClaw hook shape can provide `runId` on `ctx` rather than on the `reply_dispatch` event, and its abort-aware dispatcher may not expose `appendBeforeDeliver`. The prior public-hook fallback only armed for Dashboard tickets and invoked durable staging without Discord owner/session authority. Consequently, an ordinary Discord Direct final could be visible externally while CNX had no durable final row and later failed closed at the delivery deadline.

The repair:

1. recognizes a trusted Discord ingress (`channel`/`messageProvider` both agree);
2. arms the public-hook fallback using the exact Discord `sessionKey` + `ctx.runId` ticket;
3. carries that exact owner session and ingress surface into durable staging;
4. permits staging only when the ticket owner exactly matches the Discord session key and the session key has the canonical Discord shape;
5. binds the existing durable idempotency key to the exact Ticket and current session generation;
6. keeps Dashboard behavior and the existing marker/settlement primitive unchanged;
7. leaves `message_sent.runId` as non-authoritative for this path.

## TDD evidence

### RED

Added `plugins/cogentnexus-openclaw/src/v273-discord-direct-delivery.test.ts` with a production-shaped hook chain:

- owner key `agent:main:discord:channel:273001`;
- `reply_dispatch` event without `event.runId` and with `ctx.runId`;
- Discord `channel` and `messageProvider` context;
- abort-aware dispatcher without `appendBeforeDeliver`;
- final payload passed through registered `reply_payload_sending`;
- no `message_sent.runId` used.

Before the repair the test failed because the final payload was not staged (`undefined` result), first because Discord fallback was not armed and then because the durable staging owner predicate rejected Discord.

### GREEN

The focused test passed after the minimal fix. It verifies:

- durable `cnx_assistant_delivery` row exists before native transport completion is released;
- row owns the exact Ticket, Discord session key, generation `0`, and final text;
- native marker is present in the outbound text;
- same-text duplicate returns the same marked payload and does not start a second waiter;
- changed text for the same durable identity fails closed;
- releasing the native idle waiter completes the exact Ticket once and marks the exact delivery delivered.

Existing suites cover the preserved Dashboard path, Discord `NO_REPLY` semantics, session ownership/generation fencing, direct recovery, and delivery boundaries.

## Validation evidence

Local focused test:

- `src/v273-discord-direct-delivery.test.ts`: `1 passed`

Local full plugin suite after final changes:

- Test files: `59 passed`
- Tests: `291 passed`

Local build and package validation:

- TypeScript/build: `PASS`
- mixed-plugin artifact/schema verification: `PASS` (`45` config properties, `5` tools)
- ticket DB bootstrap: `PASS` (`9` required tables + v095 registration fence)
- package verification: `PASS` (`openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`, `198` packed files)
- `git diff --check`: `PASS`

Exact-SHA GitHub Actions:

| Workflow | Run ID | Head SHA | Result |
|---|---:|---|---|
| Validate | `34013900111` | `04a566aa66e7812a52385fb70e0e4a5834f2f931` | `success` |
| PS5.1 Acceptance Smoke | `34013900092` | `04a566aa66e7812a52385fb70e0e4a5834f2f931` | `success` |
| Windows Installer Pack Smoke | `34013900123` | `04a566aa66e7812a52385fb70e0e4a5834f2f931` | `success` |

Validate matrix jobs all completed successfully: Windows/macOS/Ubuntu on Python 3.11 and 3.14, plus package dry-run without publish.

## Changed paths

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v273-discord-direct-delivery.test.ts`

## Hard-fence ledger

- live Discord/Dashboard semantic sends: `0`
- live OpenClaw session Delete/reset: `0`
- manual live Ticket/session/SQLite mutation: `0`
- recovery replay/redelivery/disposition: `0`
- installer/install-over/uninstall/reset: `0`
- Gateway/provider/service lifecycle mutation: `0`
- Scheduled Task mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

Task272's parked live Delete/test-message authority remains unconsumed. This Task273 report is source/test/CI evidence only and does not authorize live requalification, installation, session deletion, or semantic acceptance.

## Handoff

Set coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop. A separately reviewed successor task must authorize candidate deployment and live requalification before Task272's parked authority can be considered again.
