# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK271_LIVE_DEPLOYMENT_CURSOR_REQUALIFICATION`
Current disposition: `TASK271_HUMAN_AUTHORIZED__READY_FOR_BOUNDED_LIVE_EXECUTION`
Task ID: `CNX-20260906-271`
Parent task: `CNX-20260906-270`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — human explicitly authorized bounded Task271 live install-over and cursor requalification

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Accepted Task269/270 review

`docs/operations/coordination/reviews/CNX-20260906-270-chatgpt-final-source-review.md`

Verdict:

`ACCEPT_TASK269_270_SOURCE_TEST_CI__LIVE_DEPLOYMENT_AUTHORITY_REQUIRED`

Accepted exact candidate:

`6a491d1a95394bba7b70735fbaf9cebf4d619ea6`

## Human authorization

`docs/operations/coordination/reviews/CNX-20260906-271-human-live-authorization.md`

Decision:

`AUTHORIZED_BOUNDED_LIVE_INSTALL_OVER_AND_CURSOR_REQUALIFICATION`

## Active Task271

`docs/operations/coordination/tasks/CNX-20260906-271-live-candidate-deployment-busy-cursor-requalification.md`

Hermes is authorized to execute exactly one supported install-over of the exact candidate, require/verify the supported fresh Gateway process boundary, and perform read-only natural `PT1M` cursor/process requalification.

No blind live retry. If installer/process-boundary proof is ambiguous, stop and report.

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence. No cancel/redeliver/dispose/replay, session Delete/reset, or semantic-send authority exists.

After completion Hermes publishes the Task271 report, sets `WAITING_FOR_CHATGPT_REVIEW`, and stops mutation.
