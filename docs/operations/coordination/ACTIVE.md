# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK292_RECREATION_PREFLIGHT`
Current disposition: `NEEDS_CHATGPT__TDD_REPAIR_GREEN__ALIGNED_RUNTIME_READONLY_PROBE_PASS__LIVE_WORKER_NOT_INSTALLED`
Task ID: `CNX-20260907-296`
Parent task: `CNX-20260907-295`
Resumes acceptance context: `CNX-20260906-272`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-07 ICT — Task296 assigned to Hermes: TDD runtime alignment then actual worker instrumentation

Assigned executor: `Hermes`
Review owner: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted live candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Active Task296

`docs/operations/coordination/tasks/CNX-20260907-296-align-worker-runtime-then-instrument.md`

Task295 confirmed Node runtime divergence without proving causality. Task296 must first perform TDD runtime alignment, then instrument the actual detached invocation; no delivery mutation.

## Hard fences

No Hermes semantic send, protected Ticket/session mutation, manual SQLite/Ticket/session mutation, replay/redelivery/disposition, installer, uninstall/reset, release promotion, or force push. Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or its owner session.
