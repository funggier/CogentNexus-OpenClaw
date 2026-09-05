# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK265_FIRST_TURN_LIFECYCLE_ORDERING_REPAIR`
Current disposition: `TASK265_HERMES_REPORT_PUBLISHED__AWAITING_CHATGPT_REVIEW`
Task ID: `CNX-20260905-265`
Parent task: `CNX-20260905-264`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT — Hermes published Task265 first-turn lifecycle ordering repair report; awaiting ChatGPT review

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Next execution actor after review: `Hermes` if successor/rework is opened
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## ChatGPT Task264 review

Review:

`docs/operations/coordination/reviews/CNX-20260905-264-chatgpt-first-turn-lifecycle-ordering-review.md`

Verdict:

`REWORK_REQUIRED__FIRST_TURN_SESSION_START_ORDERING_RACE`

Task264 candidate `cad96fad3d1cef07fac4173425f15714b33240d6`
correctly added exact lifecycle identity rejection after binding and passed exact-SHA CI 3/3, but OpenClaw `session_start` is a fire-and-forget void hook. Task264's `before_agent_run` only reads current identity, so the legitimate first turn of recreated lifecycle B can race ahead of `session_start(B)` and be blocked before CNX binds B.

## Active Task265

Task:

`docs/operations/coordination/tasks/CNX-20260905-265-first-turn-lifecycle-admission-ordering-repair.md`

Objective:

Make the actual `before_agent_run` owner boundary atomically reconcile + decide exact lifecycle identity so correctness does not depend on prior completion of `session_start`.

Required first-turn contract:

- deleted A + first `before_agent_run(B)` before any `session_start(B)` => activate B once and admit;
- active B + B => admit idempotently;
- active B + stale A/C => reject without mutation;
- delayed/duplicate `session_start(B)` => idempotent;
- deleting/deleted same lifecycle => reject;
- legacy active NULL => deterministic binding without generation churn;
- existing old-generation Ticket/recovery/delivery/workflow/synthetic fences remain green.

TDD is mandatory: focused RED reproducing host ordering -> minimal production fix -> focused/full GREEN -> exact-SHA CI.

## Hard fences

Task265 is source/test/docs/CI only.

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

`docs/operations/coordination/reports/CNX-20260905-265-first-turn-lifecycle-admission-ordering-repair.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation. There is no peer-bot handoff.

## Task265 Hermes report handoff

Report: `docs/operations/coordination/reports/CNX-20260905-265-first-turn-lifecycle-admission-ordering-repair.md`

Candidate/source SHA: `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`

Exact-SHA CI: PS5.1 `33977733180`, Windows Pack `33977733182`, Validate `33977733191` — all success

Hard fences: all zero; no live/runtime/semantic/destructive action performed

Next authority: ChatGPT independent review; Hermes must perform no further Task265 mutation.
