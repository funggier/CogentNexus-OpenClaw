# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK281_NONCLEAN_DISCORD_SESSION_DELETE_OBSERVATION`
Current disposition: `HUMAN_AUTHORIZED__NONCLEAN_DELETE_EXPERIMENT_READY`
Task ID: `CNX-20260906-281`
Parent task: `CNX-20260906-280`
Resumes acceptance context: `CNX-20260906-272`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — human confirmed normal reply reached Discord while later CNX terminal announcement appeared only in Web Chat, and explicitly authorized one bounded Delete experiment on the current non-clean disposable session

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted live candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Human authorization

`docs/operations/coordination/reviews/CNX-20260906-280-human-nonclean-delete-experiment-authorization.md`

## Active Task281

`docs/operations/coordination/tasks/CNX-20260906-281-nonclean-discord-session-delete-observation.md`

Hermes shall first capture a fresh read-only snapshot because Task280's report may predate the later terminal transition/announcement. If and only if the current OpenClaw session identity still exactly matches `agent:main:discord:channel:1391855033993138217` / `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`, Hermes may perform exactly one supported Delete/reset on that disposable session even though its Ticket is non-clean, then observe lifecycle consequences read-only and stop.

This experiment does not count as the original clean-session Task272 acceptance proof. No Hermes semantic send, protected Ticket/session mutation, manual SQLite/Ticket mutation, replay/redelivery, installer, uninstall/reset, release promotion, or force push is authorized.
