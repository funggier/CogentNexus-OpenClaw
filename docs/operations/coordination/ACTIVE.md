# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK268_READONLY_BUSY_CURSOR_CAUSAL_CORRELATION`
Current disposition: `TASK267_CHATGPT_REVIEW_ACCEPTED__TASK268_OPEN`
Task ID: `CNX-20260905-268`
Parent task: `CNX-20260905-267`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — ChatGPT accepted Task267 read-only diagnostics and opened cursor causal-correlation diagnostic

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Next execution actor after review: `Hermes` if a bounded successor is opened
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## ChatGPT Task267 review

Review:

`docs/operations/coordination/reviews/CNX-20260905-267-chatgpt-readonly-diagnostic-review.md`

Verdict:

`ACCEPT_READONLY_DIAGNOSTIC__BUSY_CURSOR_CAUSAL_PROOF_REQUIRED`

Accepted evidence:

- `CogentNexus-OpenClaw-Supervisor` repeats at `PT1M`;
- natural waves spawn supervisor/lifecycle/gateway-status process trees at roughly one-minute cadence;
- Gateway and Ollama processes stayed stable;
- current Ollama is healthy but durable recovery incident `ollama:1` remains open at 3/3;
- installed plugin payload still differs from accepted Task265 candidate;
- old target Ticket/recovery remains unresolved and read-only.

## Active Task268

Task:

`docs/operations/coordination/tasks/CNX-20260905-268-readonly-busy-cursor-causal-correlation-diagnostic.md`

Objective:

Capture the actual Windows WAIT/APPSTARTING cursor state at high frequency and correlate it with natural supervisor process-start waves over at least five PT1M ticks. Distinguish causal match from mere temporal correlation without disabling or changing the Scheduled Task.

## Hard fences

Task268 is read-only live diagnostics only. No install, service/Gateway/provider mutation, session Delete/reset, semantic send, DB/recovery disposition, Scheduled Task mutation/run, unrelated process termination, input injection, release mutation, or force push is authorized.

## Completion

Hermes publishes:

`docs/operations/coordination/reports/CNX-20260905-268-readonly-busy-cursor-causal-correlation-diagnostic.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.