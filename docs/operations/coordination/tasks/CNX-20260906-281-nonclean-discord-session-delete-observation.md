# CNX-20260906-281 — Non-Clean Discord Session Delete Observation

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-280`
Resumes acceptance context: `CNX-20260906-272`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authorization: `docs/operations/coordination/reviews/CNX-20260906-280-human-nonclean-delete-experiment-authorization.md`

## Objective

Observe the real lifecycle consequences of deleting the current disposable Discord session even though its setup Ticket is not durably clean.

This is a diagnostic experiment, not the clean-session acceptance proof.

## Exact target

- session key: `agent:main:discord:channel:1391855033993138217`
- expected OpenClaw session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`

Human observation to preserve:

- the normal assistant reply was visible in Discord;
- CNX durable delivery did not confirm it;
- a later terminal-status announcement appeared in Web Chat only, not Discord.

## Phase A — fresh snapshot

Before mutation, read-only prove:

1. current exact OpenClaw session ID for the target key;
2. CNX session state/generation/session_id;
3. exact setup Ticket current status/failure/delivery confirmation;
4. current assistant-delivery rows, Ticket outbox, Direct recovery and active model-call state for the target;
5. whether the Ticket has transitioned after Task280 to a terminal state and whether a terminal outbox/announcement was scheduled/delivered;
6. protected old Ticket/session remains distinct and untouched;
7. installed candidate fingerprint and MANAGED runtime remain healthy enough for a supported Delete.

If the current target identity no longer matches the expected disposable session, do not guess or delete another session; publish BLOCKED evidence.

## Phase B — one supported Delete

If identity is exact, invoke the supported OpenClaw session Delete/reset exactly once for this target.

Permitted consequences are only product-owned lifecycle effects of this Delete, including:

- old lifecycle state moving deleting/deleted/tombstoned/revoked;
- generation advance;
- session_id revocation/nulling;
- cancellation/revocation of nonterminal Ticket/delivery/recovery state belonging to this exact target when performed transactionally by the supported lifecycle.

No manual mutation is permitted.

## Phase C — post-Delete observation

Read-only capture:

- Delete command/event result and exact identity;
- pre/post generation;
- OpenClaw session inventory result;
- CNX lifecycle row state/session_id;
- setup Ticket terminal/cancelled state and event history;
- assistant-delivery/outbox/recovery rows before and after;
- whether any already-scheduled terminal announcement remains, is revoked, or is delivered after Delete;
- whether any message appears on an unexpected surface from system-owned scheduling;
- Gateway/Ollama/Host/Supervisor health;
- protected old Ticket/session unchanged.

Do not send any post-Delete semantic message in this task.

## Acceptance semantics

Task281 may PASS as an experiment if the single Delete is unambiguous and all resulting lifecycle effects are captured safely. PASS does **not** mean Task272 clean-session recreation acceptance has passed.

## Hard fences

- Hermes semantic send = 0
- extra Delete/reset = 0
- protected old Ticket/session mutation = 0
- prior sacrificial session mutation = 0
- manual SQLite/Ticket/session edits = 0
- recovery replay/redelivery/disposition = 0
- uninstall/reset/broad cleanup = 0
- installer/install-over = 0
- unrelated process/service mutation = 0
- release/tag/default-branch promotion = 0
- force push/history rewrite = 0

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-281-nonclean-discord-session-delete-observation.md`

Then set coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop.
