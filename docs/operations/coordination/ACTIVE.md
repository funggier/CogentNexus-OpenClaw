# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK272_SETUP_SETTLEMENT_AND_DELETE`
Current disposition: `BLOCKED_SETUP_TURN_DELIVERY_UNCONFIRMED__NO_DELETE`
Task ID: `CNX-20260906-272`
Parent task: `CNX-20260906-271`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — setup model completed, but durable delivery was not confirmed before deadline; Hermes stopped without Delete and reported the blocker

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Accepted Task271 / Task272 Phase A

Task271 live candidate/cursor repair is accepted. Task272 Phase A discovery was accepted with disposition `ACCEPT_PHASE_A_DISCOVERY__USER_SETUP_MESSAGE_REQUIRED`.

Phase A found no eligible clean active Discord owner session and performed zero Delete/semantic mutation.

## Human setup event

`docs/operations/coordination/reviews/CNX-20260906-272-human-setup-message-submitted.md`

The human has now sent exactly one setup message, `สวัสดีครับ`, in a disposable Discord topology and reported that the reply was still running when continuation was opened.

This message is setup-only. It is not the first-post-delete acceptance message.

## Active continuation

Task:
`docs/operations/coordination/tasks/CNX-20260906-272-live-session-delete-recreation-acceptance.md`

Hermes must:

1. read-only identify the newly created session by diffing against Phase A inventory;
2. if the setup reply is still running, continue bounded read-only rechecks without requiring another human wake-up;
3. prove the exact sacrificial session is terminal and clean: zero nonterminal Tickets, zero pending direct recovery/delivery/outbox/workflow state;
4. prove it is not the owner session of old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`;
5. only then perform exactly one supported OpenClaw session Delete/reset on that proven-clean sacrificial session;
6. prove tombstoning/revocation and stop at `WAITING_FOR_USER_TEST_MESSAGE`;
7. Hermes sends no semantic Discord messages.

If the setup turn fails and leaves ambiguous/nonterminal state, stop without Delete and report.

## Hard fences

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and its owner session remain excluded from deletion. No manual DB/Ticket edits, recovery disposition/replay/redelivery, Scheduled Task mutation, ad-hoc process kill, release/tag promotion, force push, or Hermes-generated semantic send is authorized.
