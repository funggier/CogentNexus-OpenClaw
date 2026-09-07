# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK301_SUPPORTED_SUPERVISOR_QUIESCENCE_REPAIR`
Current disposition: `BOUNDED_REPOSITORY_TDD_QUIESCENCE_REPAIR__HERMES_READY`
Task ID: `CNX-20260907-301`
Parent task: `CNX-20260907-300`
Resumes acceptance context: `CNX-20260906-272`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-07 ICT — Task301 authorized repository-level technical improvement; live mutation remains prohibited

Assigned executor: `Hermes`
Review owner: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted live candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e9335`

## Active Task301

`docs/operations/coordination/tasks/CNX-20260907-301-build-supported-supervisor-quiescence.md`

Task300 established that no supported Supervisor quiescence mechanism was available for the requested bounded enable requalification. Task301 authorizes Hermes to design and implement the minimal repository/source/test/CI repair, using TDD, for a supported task-scoped quiescence/coordination mechanism.

## Hard fences

No live `cnxclaw enable`, Scheduled Task mutation, service restart/reload, Hermes semantic send, protected Ticket/session mutation, manual SQLite/Ticket/session/transcript/config mutation in the live installation, replay/redelivery/disposition, installer, uninstall/reset, release promotion, credential action, or force push. Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or its owner session.
