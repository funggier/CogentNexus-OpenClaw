# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK198_DISCORD_INVESTIGATION__TASK199_EXISTING_EVIDENCE_CAPTURE`
Current disposition: `TASK197_PASS_ACCEPTED__V093_PUBLISHED__TASK198_WAITING_READ_ONLY_WINDOWS_EVIDENCE`
Task ID: `CNX-20260831-198`
Active evidence subtask: `CNX-20260831-199`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-08-31 ICT
Executor: Hermes for Task 199 read-only evidence; ChatGPT resumes root-cause/TDD after report
Coordinator / final reviewer: ChatGPT

## Published v0.9.3 authority

Publication is complete. Public tag `v0.9.3` targets exactly:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Do not republish or retarget v0.9.3.

## Active investigation

Parent:

[`tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`](tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md)

Read-only evidence handoff:

[`tasks/CNX-20260831-199-task198-existing-discord-hook-failure-evidence-capture.md`](tasks/CNX-20260831-199-task198-existing-discord-hook-failure-evidence-capture.md)

## Source findings already established

1. `cnx_assistant_delivery` is not required for every native external-channel Direct reply. The base Ticket contract can complete a Direct Ticket through receipt-confirmed `confirmDirectDelivery(runId)` and persist `delivery_confirmed` / `completed` directly on the Ticket.
2. The v0.9.1 Dashboard verified-delivery code explicitly refuses to claim non-Dashboard Direct tickets.
3. Its `missing-run-correlation` / `missing-append-before-deliver` messages are observer diagnostics; those branches return without throwing.
4. OpenClaw treats `before_agent_run` hook exceptions as fail-closed, so Session A's `before_agent_run hook failed; blocking request` represents a separate exception that must be identified.
5. Candidate uncaught boundaries include Ticket admission, recovery-order SQLite work, and context-guard SQLite/runtime work. No one of these is yet accepted as root cause.

## Task 199 objective

Use only existing logs and SQLite state to determine:

- the exact exception/error behind Session A's fail-closed before-agent failure;
- whether Session A created a Ticket and which run ID it used;
- whether Session B followed the expected native `message_sent` receipt path;
- which A/B correlation fields and session-generation state differ.

No new Discord Send is authorized in Task 199.

## After Task 199

ChatGPT will:

1. review the evidence;
2. state the minimum evidence-backed violated invariant;
3. write one focused regression test and observe RED;
4. apply only the minimal production fix;
5. run focused/full validation;
6. authorize at most one bounded human Discord reality test only after repository GREEN if still needed.

## Hard fence

No Discord send/retry/injection, no Gateway/OpenClaw/Ollama restart, no reset/uninstall/reinstall/install-over, no state/config/source mutation during Task 199, no provider/model change, no republish/retarget, and no force push.
