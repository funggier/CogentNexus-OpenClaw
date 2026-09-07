# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK304_TDD_INSTALLER_REPAIR`
Current disposition: `BOUNDED_REPOSITORY_REPAIR__HERMES_TECHNICAL_AUTONOMY`
Task ID: `CNX-20260907-304`
Parent task: `CNX-20260907-303`
Updated: 2026-09-07 ICT — Task303 found supported staging installer null-fingerprint defect; Task304 authorized TDD repair

Assigned executor: `Hermes`
Review owner: `ChatGPT`

## Active Task304

`docs/operations/coordination/tasks/CNX-20260907-304-repair-skipplugin-installer-contract.md`

Hermes may diagnose and repair the `-SkipPlugin` installer contract, add tests/docs/CI changes, and continue through related repository defects within this contract. Stop at repository GREEN before any live retry.

## Hard fences

No live installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual Ticket/SQLite/session/transcript mutation, protected-state mutation, release promotion, or force push.
