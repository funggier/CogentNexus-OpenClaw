# CNX-20260906-280 — Task272 Post-Repair Clean Sacrificial Session Bootstrap

## Status

`WAITING_FOR_USER_SETUP_MESSAGE`

Parent acceptance: `CNX-20260906-279`
Resumes live acceptance: `CNX-20260906-272`
Executor after setup message: `Hermes`
Reviewer: `ChatGPT`

## Objective

Create one fresh disposable Discord owner session under the repaired live candidate, prove the setup turn becomes durably clean, then consume the already-authorized Task272 session Delete exactly once and continue the original post-Delete first-turn recreation acceptance.

## Human setup action required

Create or choose a NEW disposable Discord channel/thread that the bot can receive from and that has a new canonical Discord owner key. Do not use:

- protected old owner session `agent:main:discord:channel:1531199905673252946`;
- previous non-clean sacrificial session `agent:main:discord:channel:1366635842554036314`.

Send exactly one benign setup message, for example:

`สวัสดีครับ`

This is a setup message only. It is NOT the post-Delete Task272 acceptance message.

## Hermes continuation after setup message

After the human reports that the setup message was sent, Hermes shall:

1. fresh-read `ACTIVE.md`, `STATUS.md`, Task272 authorization, Task279 review, and this task;
2. enumerate Discord/OpenClaw sessions and identify the new session by diff from prior known keys;
3. perform bounded read-only rechecks while the setup turn is actively running;
4. before Delete, prove the new session is clean:
   - exact sessionKey/sessionId/CNX generation captured;
   - setup Ticket is terminal `completed` rather than accepted/interrupted;
   - durable delivery confirmation exists for the setup reply;
   - no nonterminal Ticket for the new session;
   - no pending Direct recovery for the new session;
   - no pending assistant/Ticket delivery or outbox;
   - no active workflow/durable completion awaiting delivery;
   - no active/recovering model call;
   - session is not owner of the protected old Ticket and is not the prior non-clean sacrificial key;
5. if any clean predicate fails or remains ambiguous, perform NO Delete and publish BLOCKED evidence;
6. if all predicates pass, consume the existing Task272 authority for exactly one supported OpenClaw session Delete/reset on this proven-clean sacrificial session;
7. prove the old lifecycle is tombstoned/revoked/deleted and capture pre-Delete generation `G`;
8. perform zero Hermes-generated semantic sends;
9. set coordination to `WAITING_FOR_USER_TEST_MESSAGE` with the exact disposable Discord destination and stop.

## Phase after Delete

After the human sends exactly one benign post-Delete message in the same disposable Discord destination, Hermes must verify read-only:

- same canonical sessionKey;
- new OpenClaw sessionId differs from the deleted sessionId;
- CNX generation is exactly `G+1`;
- the first post-Delete turn is admitted on its first attempt without a second-message workaround;
- fresh Ticket completes normally with durable delivery confirmation;
- stale old lifecycle cannot reactivate or hijack;
- no stale recovery/outbox/workflow leaks across generations;
- protected old Ticket and prior non-clean sacrificial lineage remain untouched;
- Gateway/Ollama/Host/Supervisor remain healthy.

Then publish the final Task272 acceptance report and stop for ChatGPT review.

## Hard fences

Still forbidden unless separately authorized:

- Hermes-generated Discord/Dashboard semantic sends;
- mutation of the protected old Ticket or its owner session;
- mutation/disposition of the prior non-clean sacrificial Ticket/session solely to make it clean;
- manual SQLite edits;
- recovery replay/redelivery/disposition;
- product uninstall/reset or broad cleanup;
- Scheduled Task mutation outside supported lifecycle behavior;
- release/tag/default-branch promotion before final acceptance;
- force push/history rewrite.

The human's conditional final-release direction remains parked until Task272 and final repository acceptance pass.
