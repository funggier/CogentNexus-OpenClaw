# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__CHATGPT_ROUTINE_REVIEW`
Current disposition: `TASK263_SOURCE_REPAIR_PASS__CI_GREEN__CHATGPT_REVIEW_REQUIRED`
Task ID: `CNX-20260905-263`
Parent task: `CNX-20260905-262`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT — human switched coordination to single Hermes + ChatGPT review

Assigned executor: `Hermes` (Task263 implementation already complete; historical report actor Luna)
Review owner: `ChatGPT`
Handoff from: `Luna` (historical Task263 executor)
Next execution actor after ChatGPT decision: `Hermes`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`
Human coordination decision: `docs/operations/coordination/reviews/CNX-20260905-single-hermes-chatgpt-coordination-decision.md`

## Current review packet

Task contract:

`docs/operations/coordination/tasks/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

Hermes/Luna historical execution report:

`docs/operations/coordination/reports/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

Reported result:

`PASS_SOURCE_REPAIR__CI_GREEN__LIVE_ACCEPTANCE_REQUIRED`

Exact repair candidate:

`4a5907af212c0b8c6f913036c6853523d7bab872`

Report publication HEAD before coordination-policy transition:

`9c1391d535b14fc4e3ed35f3f9448bdf5e9c0c33`

Reported validation:

- focused ownership suite: 7/7
- full plugin suite: 287/287
- build: PASS
- plugin validation: PASS
- diff check: PASS
- exact candidate GitHub workflows: 3/3 success

## Required semantics under review

- Explicit web-session Delete remains an abandonment boundary for the old generation.
- Old nonterminal Tickets, pending outbox/assistant delivery, direct recovery, workflow completion, and synthetic work are not rebound into a recreated session.
- A genuine new OpenClaw `sessionId` on the same Discord session key may establish a fresh active CogentNexus generation.
- Repeated start for the same new lifecycle is idempotent.
- A stale start from the deleted lifecycle cannot reactivate it.
- Old-generation delivery/recovery remains fenced after recreation.
- Existing reset/new/session-succession behavior does not regress.

## Current authority

Task263 remains source/test/docs only until ChatGPT completes independent review.

No authority currently exists for:

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

ChatGPT must review the exact Task263 candidate/report. If accepted, ChatGPT may open a bounded successor for Hermes. Any successor requiring actual user-session deletion or a Discord semantic message must carry explicit authority; do not infer that authority from this coordination-policy change.

## Single-agent stop rule

Hermes performs no further Task263 mutation while this state is `WAITING_FOR_CHATGPT_REVIEW`. There is no Musethree handoff. ChatGPT owns the next coordination decision.
