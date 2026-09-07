# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `SINGLE_HERMES_EXECUTOR__TASK305_BOUNDED_STAGING_INSTALLER`
**Updated:** 2026-09-07 ICT — Task305 authorizes one repaired staging installer retry
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260907-305`
**Parent:** `CNX-20260907-304`
**Disposition:** `BOUNDED_STAGING_RETRY__EXACTLY_ONE__HERMES_READY`

**Routine executor:** `Hermes`
**Review owner:** `ChatGPT`

Task304 passed repository TDD validation: focused 10 passed, installer/ownership regression 48 passed, full suite 539 passed, 5 skipped, 4 subtests passed. Task305 authorizes exactly one supported staging installer retry with the repaired `-SkipPlugin` contract. Hermes may choose preflight/postflight details and must report exact identities and outcome. Stop before `cnxclaw enable`.

Still forbidden: second installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual Ticket/SQLite/session/transcript mutation, protected-state mutation, release promotion, and force push.
