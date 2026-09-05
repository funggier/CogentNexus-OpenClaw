# Active Coordination Task

Status: `TASK263_REPAIRED__REVIEW_REQUIRED`
Execution mode: `TASK263_DISCORD_MANUAL_SESSION_DELETE_RECREATION_SOURCE_REPAIR`
Current disposition: `TASK263_SOURCE_REPAIR_PASS__CI_GREEN__LIVE_ACCEPTANCE_REQUIRED`
Task ID: `CNX-20260905-263`
Parent task: `CNX-20260905-262`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT — Task263 report published

Assigned executor: `Luna`
Handoff from: `ChatGPT`
Next actor after report: `Musethree`
Coordination protocol: `docs/operations/coordination/HERMES_DUAL_AGENT_BATON_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Completed objective

Repair the lifecycle gap where OpenClaw `sessions.delete` correctly emits
`session_end(reason="deleted")` and CogentNexus tombstones/cancels the old
owner generation, but a later Discord message can recreate the OpenClaw
session at the same canonical session key with a new `sessionId` while the
CogentNexus owner row remains permanently tombstoned.

Task contract:

`docs/operations/coordination/tasks/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

Report:

`docs/operations/coordination/reports/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

Result: `PASS_SOURCE_REPAIR__CI_GREEN__LIVE_ACCEPTANCE_REQUIRED`. Exact repair
candidate `4a5907af212c0b8c6f913036c6853523d7bab872` passed local focused/full
validation and 3/3 exact-SHA GitHub workflows. Baton is handed to Musethree;
no live acceptance is authorized by Task263.

## Required semantics

- Explicit web-session Delete remains an abandonment boundary for the old
  generation: old nonterminal Tickets, pending outbox/assistant delivery,
  direct recovery, owned workflow completion and synthetic work must not be
  rebound into the recreated session.
- A genuine new OpenClaw lifecycle instance on the same Discord session key
  must be able to become a fresh active CogentNexus owner generation.
- Reactivation must be lifecycle-identity-aware and idempotent. A stale or
  duplicate `session_start` from the deleted lifecycle must not reopen it.
- Old-generation recovery/delivery must remain permanently fenced after the
  new generation becomes active.
- Normal `reset`, same-key `new`, and explicit deletion semantics must not
  regress.

## Authority

Repository/source/test/docs diagnosis and repair are authorized. TDD is
mandatory: focused RED -> minimal production repair -> focused/full GREEN.

Live runtime mutation is not authorized in Task263. In particular:

```text
live OpenClaw session delete/reset = 0
live Discord/Dashboard semantic sends = 0
live Ticket/session/SQLite mutation = 0
installer/install-over/uninstall/reset = 0
Gateway restart/stop/start = 0
release/tag/default-branch mutation = 0
force push/history rewrite = 0
```

If source repair and CI are accepted, Musethree should review and then open or
propose a separate bounded live acceptance successor. If that successor needs
actual user-session deletion or a semantic Discord message and existing
contract does not already authorize it, fail closed and escalate to ChatGPT.

## Baton

Luna owns Task263 implementation/report. When the report is published, Luna
must hand off to Musethree. Musethree independently reviews exact source diff,
RED/GREEN evidence and exact-SHA CI. CI waits use the persistent five-minute
recheck queue; do not stop merely because Actions are queued/in-progress.
