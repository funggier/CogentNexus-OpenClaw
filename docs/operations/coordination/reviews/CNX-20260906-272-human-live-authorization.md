# CNX-20260906-272 — Human Live Authorization

## Decision

`AUTHORIZED_BOUNDED_TASK272_EXISTING_CLEAN_SESSION_DELETE_AND_USER_FIRST_MESSAGE`

On 2026-09-06 ICT, the human operator explicitly authorized Task272 and offered to send the required Discord test message.

## Topology correction

A Discord/OpenClaw session cannot be "never used" and simultaneously already exist for deletion: at least one inbound Discord message must have created the session first.

Therefore Task272 must distinguish:

1. an **existing sacrificial session** that has already been created by prior traffic but currently has no nonterminal/pending CNX work; versus
2. a **new sacrificial session that would need a setup message first** before it can be deleted.

The current authorization is sufficient for path (1): read-only discovery, exactly one Delete/reset of a proven-clean existing sacrificial Discord owner session, and exactly one human-sent first message after deletion.

If no proven-clean existing sacrificial session exists, Hermes must stop at `WAITING_FOR_USER_SETUP_MESSAGE`. A separate setup message may then be requested from the human before any deletion; Hermes must not manufacture that semantic message itself.

## Granted authority

Hermes may:

- perform read-only discovery of existing Discord owner sessions and their exact `sessionKey`, `sessionId`, CNX generation, Ticket, recovery, delivery, outbox and workflow state;
- select only a session proven to have zero nonterminal/pending CNX work relevant to deletion;
- perform exactly one supported live OpenClaw session Delete/reset on that proven-clean sacrificial session;
- allow the normal CNX tombstone/revocation state transition caused by that Delete;
- stop at `WAITING_FOR_USER_TEST_MESSAGE` after deletion;
- after the human sends exactly one benign Discord message, observe and verify the first-turn recreation path read-only.

## Explicit exclusions

The session containing old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` is excluded from deletion under this authorization. Its owner intent remains unproven.

Still forbidden:

```text
product uninstall/reset                         = 0
Hermes-generated semantic Discord send          = 0
extra semantic sends beyond the bounded proof   = 0
manual SQLite edits                             = 0
manual Ticket dispose/redeliver/replay           = 0
recovery disposition                            = 0
Scheduled Task mutation                         = 0
ad-hoc process/service kills                    = 0
release/tag/default-branch promotion            = 0
force push/history rewrite                      = 0
```

## Stop conditions

If no existing Discord owner session can be proven clean before mutation, do not delete anything. Set coordination to `WAITING_FOR_USER_SETUP_MESSAGE` and report the exact blocker/topology needed.

If Delete execution is ambiguous or targets a different session than the proven-clean candidate, stop immediately and do not retry.
