# CNX-20260906-272 — Live Session Delete/Recreation Acceptance

## Status

`READY_FOR_HERMES_PHASE_A_DISCOVERY`

Parent: `CNX-20260906-271`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authorization: `docs/operations/coordination/reviews/CNX-20260906-272-human-live-authorization.md`

## Objective

Live-accept the Tasks263–265 lifecycle repair on Windows/OpenClaw by proving that a manually deleted OpenClaw Discord owner session is tombstoned safely and that the first owner message in the genuinely new lifecycle is admitted successfully without requiring a second-message workaround.

## Correct Discord topology

Do not assume an unused/never-used Discord session can already exist. A Discord/OpenClaw session necessarily exists because at least one inbound message created it.

The preferred sacrificial target is therefore an **existing previously-used Discord owner session that is now clean**:

- current exact `sessionKey` and `sessionId` are observable;
- CNX session authority is known;
- nonterminal Tickets = 0;
- pending direct recovery = 0;
- pending assistant/Ticket delivery or outbox = 0;
- active workflow/durable completion awaiting delivery = 0;
- it is not the session that owns old unproven-intent Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`.

If no such existing clean session exists, do not manufacture one silently and do not delete the old-Ticket session. Stop at `WAITING_FOR_USER_SETUP_MESSAGE`; the human can then send a setup message in a suitable disposable Discord topology to create a sacrificial session first.

## Phase A — discovery and bounded Delete

1. Fresh-read branch, ACTIVE/STATUS, this task and authorization.
2. Read-only enumerate supported Discord owner sessions and correlate OpenClaw session identity with CNX session/Ticket/recovery/delivery/workflow state.
3. Select a sacrificial session only if all clean-session predicates above are proven.
4. Capture pre-state exact `sessionKey`, current `sessionId`, CNX generation and relevant zero/pending counts.
5. Perform exactly one supported live OpenClaw session Delete/reset on that exact proven-clean sacrificial session.
6. Prove the old lifecycle became tombstoned/revoked and cannot regain authority.
7. Do not send any semantic message on behalf of the human.
8. Set coordination to `WAITING_FOR_USER_TEST_MESSAGE` and publish enough evidence for ChatGPT/human to know exactly where to send the message.

If no clean session is found, set `WAITING_FOR_USER_SETUP_MESSAGE` without any Delete.

## Phase B — human first message and verification

After coordination explicitly reaches `WAITING_FOR_USER_TEST_MESSAGE`, the human sends exactly one benign Discord message in the same canonical Discord topology/key.

Hermes then verifies read-only that:

1. the message creates/uses a genuinely new OpenClaw `sessionId` on the same canonical key;
2. the very first message is admitted on its first attempt and receives a fresh Ticket/reply path;
3. no second-message workaround occurs;
4. CNX generation advances exactly once for the new lifecycle;
5. delayed/stale old lifecycle identity cannot hijack the new active lifecycle;
6. no old recovery/delivery/workflow evidence leaks into the new lifecycle;
7. Gateway/provider remain healthy.

## Hard fences

The old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and its current owner session remain excluded from deletion.

```text
product uninstall/reset                         = 0
Hermes-generated semantic Discord send          = 0
extra semantic sends beyond bounded proof       = 0
manual SQLite edits                             = 0
manual Ticket dispose/redeliver/replay           = 0
recovery disposition                            = 0
Scheduled Task cadence/enablement changes       = 0
ad-hoc process/service kills                    = 0
release/tag/default-branch promotion            = 0
force push/history rewrite                      = 0
```

## Completion

After Phase B evidence is complete, publish:

`docs/operations/coordination/reports/CNX-20260906-272-live-session-delete-recreation-acceptance.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
