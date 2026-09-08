# CNX-20260906-271 — Live Candidate Deployment and Busy-Cursor Requalification

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-270`
Executor: `Hermes`
Reviewer: `ChatGPT`
Authorization: `docs/operations/coordination/reviews/CNX-20260906-271-human-live-authorization.md`

## Objective

Deploy the accepted source/test candidate to the live Windows installation in one bounded install-over, establish a verified fresh managed runtime boundary, and re-run the natural one-minute cursor/process observation to prove whether the Task269 Host actionability repair removes the recurring APPSTARTING/busy-cursor symptom without weakening supervisor recovery.

## Exact candidate

`6a491d1a95394bba7b70735fbaf9cebf4d619ea6`

## Required live sequence

1. Fresh-read branch, ACTIVE/STATUS, this task, authorization, candidate commit and exact-SHA Actions before mutation.
2. Capture pre-state read-only evidence: installed fingerprint/payload identity, Gateway PID/start time, Ollama PID/health, supervisor task definition/state, current Ticket/recovery counts and old target Ticket read-only state.
3. Perform exactly one supported install-over of the exact candidate. Do not blind-retry after ambiguity or partial failure.
4. Require a verified fresh Gateway/process boundary and exact candidate fingerprint binding.
5. Do not mutate/cancel/redeliver/dispose/replay the old Ticket.
6. Observe at least 5 natural `PT1M` supervisor ticks (prefer 6 minutes) with the same Win32 cursor-state/process-correlation method used in Task268.
7. PASS cursor acceptance requires no recurring APPSTARTING wave caused by healthy steady-state supervisor ticks. Natural supervisor ticks may remain; they should stay on the lightweight path when only stale/non-actionable Direct evidence exists.
8. Verify Gateway/Ollama remain healthy and stable; verify no unauthorized semantic send, recovery replay, Ticket mutation, or session deletion occurred.
9. If APPSTARTING persists, capture exact process tree and fail closed for source diagnosis rather than changing cadence or disabling the Scheduled Task ad hoc.

## Authorized live scope

Allowed:
- exactly one supported install-over of the exact candidate;
- supported managed Gateway process boundary that is part of install-over;
- candidate/runtime verification and read-only cursor/process observation.

Still forbidden:

```text
uninstall/reset                                  = 0
live OpenClaw session delete/reset               = 0
Discord/Dashboard/API semantic send              = 0
manual Ticket/session/SQLite mutation            = 0
recovery replay/redelivery/disposition           = 0
Scheduled Task disable/delete/cadence change     = 0
ad-hoc process/service kill outside install-over = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-271-live-candidate-deployment-busy-cursor-requalification.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
