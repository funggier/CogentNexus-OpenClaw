# Active Coordination Task

Status: `NEEDS_CHATGPT`
Execution mode: `ALTERNATING_SUNA_DIRECT_PREFLIGHT_LUNA_DELETE__TASK289_290`
Current disposition: `NEEDS_CHATGPT__DIRECT_PATH_REQUIRES_CREDENTIAL_AND_FENCE_DRIFT__NO_DELETE`
Task ID: `CNX-20260907-289`
Parent task: `CNX-20260907-288`
Resumes acceptance context: `CNX-20260906-272`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-07 ICT — Task289 stopped by Suna: direct path requires credential and inherited session fence drifted; ChatGPT review required

Assigned executor: `Hermes`
Review owner: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted live candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Active Task289

`docs/operations/coordination/tasks/CNX-20260907-289-suna-direct-gateway-invocation-preflight.md`

Task281 is accepted as a no-op supported cancel observation: exactly one `cnxclaw.cmd session cancel` invocation returned `cancelled=[]`; it did not delete the OpenClaw session. Do not retry it as a Delete substitute.

Task287 preflight passed. Task288 did not call sessions.delete because browser navigation was misrouted into Chat and rejected. Task289 direct Gateway preflight found stale immutable fence values and no non-secret operator-admin CLI path. Stop and require ChatGPT; Task290 is not authorized.

## Hard fences

No Hermes semantic send, protected Ticket/session mutation, manual SQLite/Ticket/session mutation, replay/redelivery/disposition, installer, uninstall/reset, release promotion, or force push. Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or its owner session.
