# CNX-20260906-272 — Live Session Delete/Recreation Acceptance

## Status

`READY_FOR_HERMES_SETUP_SETTLEMENT_AND_DELETE`

Parent: `CNX-20260906-271`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authorization: `docs/operations/coordination/reviews/CNX-20260906-272-human-live-authorization.md`
Setup event: `docs/operations/coordination/reviews/CNX-20260906-272-human-setup-message-submitted.md`

## Objective

Live-accept the Tasks263–265 lifecycle repair on Windows/OpenClaw by proving that a manually deleted OpenClaw Discord owner session is tombstoned safely and that the first owner message in the genuinely new lifecycle is admitted successfully without requiring a second-message workaround.

## Current topology state

Task272 Phase A found no eligible clean active Discord owner session. The human has now sent exactly one setup message, `สวัสดีครับ`, through a disposable Discord topology and reported that the OpenClaw/LLM reply was still in progress when this continuation was opened.

The setup message exists only to create the sacrificial OpenClaw/CNX session. It is **not** the first-post-delete acceptance message.

## Phase A2 — setup settlement, clean proof, bounded Delete

1. Fresh-read branch, ACTIVE/STATUS, this task, the human authorization, Phase A report, and setup-event artifact.
2. Read-only enumerate current OpenClaw Discord owner sessions and correlate them with CNX session/Ticket/recovery/delivery/outbox/workflow state.
3. Identify the newly created sacrificial session by comparing against the Phase A inventory. Do not select the old-Ticket owner session.
4. If the setup reply/turn is still in progress, perform read-only bounded rechecks until the setup turn reaches a terminal state. Do not require another human wake-up merely because inference/reply is still running.
5. Before Delete, prove for that exact session/key:
   - OpenClaw turn/session is no longer actively running;
   - CNX nonterminal Tickets = 0;
   - pending direct recovery = 0;
   - pending assistant/Ticket delivery/outbox = 0;
   - active workflow/durable completion awaiting delivery = 0;
   - exact `sessionKey`, current `sessionId`, and CNX generation are recorded;
   - it is not the session owning old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`.
6. If the setup turn terminates unsuccessfully but leaves any nonterminal/pending state, or the session identity is ambiguous, stop and report. Do not Delete through ambiguity.
7. Once all clean predicates are proven, consume exactly one already-authorized supported OpenClaw session Delete/reset on that sacrificial session.
8. Prove the old lifecycle became tombstoned/revoked and cannot regain authority.
9. Hermes must not send any semantic Discord message.
10. Set coordination to `WAITING_FOR_USER_TEST_MESSAGE`, state the exact Discord channel/session key to use, and stop mutation.

## Phase B — human first post-delete message and verification

Only after coordination explicitly reaches `WAITING_FOR_USER_TEST_MESSAGE`, the human sends exactly one benign Discord message in the same canonical Discord topology/key.

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

After Phase A2 Delete proof, stop at `WAITING_FOR_USER_TEST_MESSAGE`.

After Phase B evidence is complete, publish/update:

`docs/operations/coordination/reports/CNX-20260906-272-live-session-delete-recreation-acceptance.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
