# Active Coordination

Status: `ACTIVE`
State: `CNX452_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-452-hard-context-pressure-compact-resume.md`
Assigned executor: `ChatGPT`
Human final authority: `Operator`
Working branch: `cnx-452-hard-context-pressure-compact-resume`
Baseline SHA: `a03dadecc2a95550046978d18ba3590c56ceb615`
Baseline release: `v0.9.8` (immutable)
GitHub issue: `#44`

## Trigger

OpenClaw 2026.9.5 treats `before_agent_run outcome=block` as terminal send failure. The existing hard-context-pressure guard uses that result as a deferred-compaction barrier, causing the accepted user turn to fail permanently before maintenance can resume it.

## Objective

Compact the exact owner session synchronously under durable authority, re-evaluate pressure, and pass the same turn only after a safe post-compaction state is proven. Preserve fail-closed behavior when safety cannot be proven.

## Current classification

`CNX452_RED_TEST_PREPARATION`
