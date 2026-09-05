# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK264_LIFECYCLE_IDENTITY_FENCE_REWORK`
Current disposition: `TASK263_CHATGPT_REVIEW_REWORK_REQUIRED__TASK264_OPEN`
Task ID: `CNX-20260905-264`
Parent task: `CNX-20260905-263`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT — ChatGPT reviewed Task263 and opened bounded lifecycle-identity rework

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Next execution actor after review: `Hermes` if successor/rework is opened
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## ChatGPT Task263 review

Review:

`docs/operations/coordination/reviews/CNX-20260905-263-chatgpt-lifecycle-recreation-review.md`

Verdict:

`REWORK_REQUIRED__LIFECYCLE_IDENTITY_FENCE_INCOMPLETE`

Task263 candidate `4a5907af212c0b8c6f913036c6853523d7bab872` remains a useful baseline but is not accepted as complete because active lifecycle `B` does not explicitly reject stale/different lifecycle `A`/`C`; the helper returns current active state for any incoming lifecycle once the owner row is active, and the existing regression does not prove stale identity rejection.

## Active Task264

Task:

`docs/operations/coordination/tasks/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`

Objective:

Add the minimal exact lifecycle-identity fence so that lifecycle acceptance is not inferred from owner state alone. Prove stale/different session IDs are rejected without mutation and enforce the current lifecycle at `before_agent_run` using OpenClaw hook `ctx.sessionId` + `ctx.sessionKey`.

TDD is mandatory: focused RED -> minimal production fix -> focused/full GREEN -> exact-SHA CI.

## Hard fences

Task264 is source/test/docs/CI only.

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

## Completion

Hermes publishes:

`docs/operations/coordination/reports/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`

Then set state to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation. There is no peer-bot handoff.
