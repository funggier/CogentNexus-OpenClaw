# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK274_DISCORD_DIRECT_CONCURRENT_RECEIPT_LIFECYCLE_FENCE_COMPLETION`
Current disposition: `TASK273_REWORK_REQUIRED__TASK274_OPEN`
Task ID: `CNX-20260906-274`
Parent task: `CNX-20260906-273`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — ChatGPT reviewed Task273, accepted the single-run repair evidence, found unresolved same-session no-runId receipt ambiguity and missing lifecycle-generation proofs, and opened Task274

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Task273 review

Review:

`docs/operations/coordination/reviews/CNX-20260906-273-chatgpt-discord-direct-durable-delivery-review.md`

Verdict:

`REWORK_REQUIRED__CONCURRENT_MESSAGE_SENT_AND_GENERATION_PROOFS_MISSING`

Task273 candidate `04a566aa66e7812a52385fb70e0e4a5834f2f931` has a promising production-shaped Discord Direct durable staging repair and exact-SHA CI green, but the task's explicit safety contract is not complete.

The generic `message_sent` fallback still infers a no-runId outbound receipt from the latest run mapped to the same session. The exact installed OpenClaw contract cannot guarantee outbound runId and warns sessionKey-only correlation cannot disambiguate concurrent turns. Task273 did not test this two-run case.

Task273 also did not directly prove delete/reset/wrong-generation late-callback behavior or the Discord-local durable timeout boundary.

## Active Task274

Task:

`docs/operations/coordination/tasks/CNX-20260906-274-discord-direct-concurrent-receipt-lifecycle-fence-completion.md`

Objective: close same-session receipt ambiguity, stale lifecycle/generation races, and Discord-local timeout proof using RED -> minimal repair -> GREEN while preserving Task273's accepted single-run durable staging.

Hermes may perform source/test/docs/CI work only. No live semantic send, session Delete/reset, install-over, Gateway/provider mutation, Ticket/recovery disposition, manual SQLite mutation, Scheduled Task mutation, release promotion, or force push is authorized.

Task272 live Delete/test-message authority remains parked and unconsumed.
