# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK275_DISCORD_DIRECT_OWNER_CONTEXT_STALE_SETTLEMENT_PROOF`
Current disposition: `BLOCKED_CI_UNRESOLVED__WAITING_FOR_CHATGPT_REVIEW`
Task ID: `CNX-20260906-275`
Parent task: `CNX-20260906-274`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — Task275 source/test proofs passed; exact-SHA Validate remains blocked by two unrelated Windows matrix test timeouts

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Task274 review

Review:

`docs/operations/coordination/reviews/CNX-20260906-274-chatgpt-discord-direct-safety-completion-review.md`

Verdict:

`REWORK_REQUIRED__OWNER_CONTEXT_AND_STALE_SETTLEMENT_PROOFS_INCOMPLETE`

Accepted from Task274:

- canonical Discord `message_sent` without exact runId now fails closed instead of selecting the newest session run;
- two-run ambiguity regression passes;
- helper-level delete/recreation and durable-timeout evidence is directionally correct;
- exact candidate `35839a26673b35866334a36891a12d1c6d12e8ed` passed Validate, PS5.1 Acceptance Smoke and Windows Installer Pack Smoke.

Remaining blockers before live deployment:

- `reply_payload_sending` consume-time owner/session/surface mismatch is not explicitly fenced/proven;
- stale registered native waiter released after session Delete/reset is not directly proven unable to complete old work;
- timeout-local proof does not yet perform later exact settlement and prove exactly-once completion.

## Active Task275

Task:

`docs/operations/coordination/tasks/CNX-20260906-275-discord-direct-owner-context-and-stale-settlement-proof.md`

Objective: close those final production-shaped Discord Direct authority proofs using RED -> minimal repair -> GREEN while preserving the accepted Task273/274 behavior.

Hermes may perform source/test/docs/CI work only. No live semantic send, live session Delete/reset, install-over, Gateway/provider mutation, Ticket/recovery disposition, manual SQLite mutation, Scheduled Task mutation, release promotion, or force push is authorized.

Task272 live Delete/test-message authority remains parked and unconsumed.
