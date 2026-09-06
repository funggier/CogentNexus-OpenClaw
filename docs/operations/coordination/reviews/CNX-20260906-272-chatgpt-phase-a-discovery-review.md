# CNX-20260906-272 — ChatGPT Phase A Discovery Review

## Verdict

`ACCEPT_PHASE_A_DISCOVERY__USER_SETUP_MESSAGE_REQUIRED`

## Review

Hermes correctly stopped without live mutation because no existing clean active Discord owner session satisfied the sacrificial-session predicates.

Accepted facts from the Phase A report:

- OpenClaw reported two Discord owner sessions.
- The only active CNX Discord lifecycle owns old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and remains excluded from deletion.
- The other Discord record is already tombstoned/deleted in CNX and is not a valid clean active sacrificial target.
- No session Delete/reset, Hermes semantic Discord send, manual SQLite/Ticket mutation, recovery disposition/replay/redelivery, Scheduled Task mutation, process kill/service mutation, release/tag promotion, or force push occurred.

## Required next action

The human should create a disposable Discord topology with a new channel identifier that the OpenClaw bot can receive, then send exactly one benign setup message. The setup message is only to create a normal previously-used session; it is not the post-delete acceptance message.

After the setup exchange completes, Hermes must fresh-read coordination and live state, prove the new session is clean (no nonterminal Ticket and no pending recovery/delivery/outbox/workflow evidence), then consume the single authorized Delete and stop at `WAITING_FOR_USER_TEST_MESSAGE` before the human sends the actual first post-delete acceptance message.

If the setup session is not clean or does not produce the expected Discord/OpenClaw topology, Hermes must not delete it and must report the blocker.
