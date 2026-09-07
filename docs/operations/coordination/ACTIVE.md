# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK304_TDD_INSTALLER_REPAIR`
Current disposition: `PASS_REPOSITORY_TDD_REPAIR_GREEN__LIVE_RETRY_FORBIDDEN`
Task ID: `CNX-20260907-304`
Parent task: `CNX-20260907-303`
Updated: 2026-09-07 ICT — Task304 repository TDD repair GREEN; live retry/enable remain forbidden

Assigned executor: `Hermes`
Review owner: `ChatGPT`

## Active Task304

`docs/operations/coordination/tasks/CNX-20260907-304-repair-skipplugin-installer-contract.md`

Hermes may diagnose and repair the `-SkipPlugin` installer contract, add tests/docs/CI changes, and continue through related repository defects within this contract. Stop at repository GREEN before any live retry.

## Hard fences

No live installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual Ticket/SQLite/session/transcript mutation, protected-state mutation, release promotion, or force push.
