# Active Coordination Task

Status: `READY_FOR_WINDOWS_REQUALIFICATION`
Execution mode: `TASK207_DIRECT_DISCORD_NO_REPLY_VISIBLE_FINAL_REPAIR`
Current disposition: `TASK207_REPOSITORY_GREEN__WINDOWS_DISCORD_REQUALIFICATION_REQUIRED`
Task ID: `CNX-20260901-207`
Parent task: `CNX-20260901-206`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: ChatGPT / repository TDD after design approval
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Current repaired product candidate

Repository-GREEN Task-207 candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

The installed/live candidate remains the pre-Task-207 candidate until the separate Windows requalification installs this exact candidate.

## Task 206 accepted result

Task-206 report:

`reports/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md`

Review:

`reviews/CNX-20260901-206-task205-discord-native-delivery-hook-forensics-review.md`

Accepted run-bound facts:

- Task-205 final assistant text was exact bare `NO_REPLY`;
- no messaging-tool send occurred;
- OpenClaw recorded no queued reply payloads for the final Discord channel turn;
- no native Discord message ID or success/failure receipt was retained;
- the direct Ticket reached response readiness but later timed out without delivery confirmation.

The observed `reply_dispatch` missing-correlation diagnostic cannot be bound to the Task-205 run because that observer entry precedes the session start. It is therefore retained as a separate integration risk rather than used as the Task-205 production root cause.

## Proven root cause

Task 191 already protects genuine direct Dashboard Tickets from terminating as bare OpenClaw `NO_REPLY` by requesting one bounded same-run revision in `before_agent_finalize`.

That guard is scoped through `dashboardTicket(path, runId)`. A genuine direct Discord owner Ticket does not enter the guard, so Task 205 allowed the small local model's bare `NO_REPLY` to reach OpenClaw silent suppression and produced no channel payload.

## Task 207 design

Task definition:

`tasks/CNX-20260901-207-direct-discord-no-reply-visible-final-repair.md`

Bounded design:

1. add focused RED for an accepted direct Discord owner Ticket whose final is bare `NO_REPLY`;
2. require exact run ID + exact owner session + accepted direct/non-workflow Ticket + canonical Discord channel session shape;
3. return one bounded same-run finalization revision only for exact bare `NO_REPLY` / `no_reply`;
4. do not synthesize the user answer;
5. preserve Dashboard Task-191 staging/marker/settlement semantics unchanged;
6. do not modify `reply_dispatch` or `message_sent` correlation in Task 207;
7. GREEN through focused/full plugin tests, Validate matrix, Windows installer pack smoke and PS5.1 smoke;
8. only after repository GREEN open a separate one-send Windows/Discord requalification.

## Discord budget

Repository Task 207 authorizes:

`0 Discord sends`

A new live semantic budget may be allocated only in the separate post-GREEN requalification task.

## Hard fence

Until implementation approval: no production/test source mutation.

For Task 207 after approval: no Discord Send, no lifecycle mutation, no live SQLite lock, no provider/model/config/schema change, no installer/uninstall/reset/reinstall, no Release/tag mutation, no force push, and no delivery-correlation production change.
