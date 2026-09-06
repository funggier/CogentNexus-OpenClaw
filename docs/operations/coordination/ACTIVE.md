# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK285_FENCED_DELETE_WITHOUT_LIFECYCLE_REVISION`
Current disposition: `BLOCKED_PREFLIGHT_GATEWAY_CLIENT_MISSING_OPERATOR_ADMIN__NO_LIVE_DELETE__WAITING_FOR_CHATGPT_REVIEW`
Task ID: `CNX-20260906-285`
Parent task: `CNX-20260906-284`
Resumes acceptance context: `CNX-20260906-272`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — Task285 preflight blocked: Gateway client connected without operator scope; no live Delete; awaiting ChatGPT review

Assigned executor: `Hermes`
Review owner: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted live candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Active Task285

`docs/operations/coordination/tasks/CNX-20260906-285-fenced-delete-without-lifecycle-revision.md`

Task281 is accepted as a no-op supported cancel observation: exactly one `cnxclaw.cmd session cancel` invocation returned `cancelled=[]`; it did not delete the OpenClaw session. Do not retry it as a Delete substitute.

Task285 authorizes exactly one supported Gateway sessions.delete attempt using fresh expectedSessionId and expectedSessionUpdatedAt; lifecycleRevision must remain absent. Any mismatch/error/timeout means stop without retry. No reset or post-delete semantic send is authorized.

## Hard fences

No Hermes semantic send, protected Ticket/session mutation, manual SQLite/Ticket/session mutation, replay/redelivery/disposition, installer, uninstall/reset, release promotion, or force push. Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or its owner session.
