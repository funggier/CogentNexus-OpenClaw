# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `SINGLE_HERMES_EXECUTOR__TASK304_TDD_INSTALLER_REPAIR`
**Updated:** 2026-09-07 ICT — Task304 authorized bounded repository TDD repair with Hermes technical autonomy
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260907-304`
**Parent:** `CNX-20260907-303`
**Disposition:** `BOUNDED_REPOSITORY_REPAIR__HERMES_TECHNICAL_AUTONOMY`

**Routine executor:** `Hermes`
**Review owner:** `ChatGPT`

Task303 adopted the Task301 wiring through the supported staging installer, but exposed a null-fingerprint defect at `install.ps1:506` when `-SkipPlugin` is used. Task304 authorizes Hermes to repair this contract with TDD, make bounded technical decisions, and continue through related repository defects within scope. After GREEN, Hermes must stop before live retry or `cnxclaw enable`.

Still forbidden: live installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual Ticket/SQLite/session/transcript mutation, protected-state mutation, release promotion, and force push.
