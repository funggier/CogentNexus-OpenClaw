# CNX-20260907-305 — Bounded Staging Installer Retry

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-304`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

Hermes may perform one bounded retry of the supported staging installer using the repaired exact candidate. Hermes may choose technical preflight, provenance, backup/readback, and postflight details without micro-confirmation.

## Procedure

1. Fresh-fetch and bind the exact current candidate and Task304 repair.
2. Verify live state, health, target/protected state separation, and no overlapping installer.
3. Invoke the supported staging installer exactly once with the repaired `-SkipPlugin` contract and existing no-restart/no-agent-policy flags.
4. Verify terminal success, exact installed-vs-candidate identities, launcher, Host/Supervisor wiring, rollback/backup state, and health.
5. Stop before `cnxclaw enable`; publish an evidence-rich report.

## Stop conditions

Stop on candidate drift, preflight ambiguity, installer conflict, nonzero exit, postcondition mismatch, health failure, protected-state drift, or any request outside this task. Do not retry within this task.

## Hard fences

No second installer retry, no `cnxclaw enable`, no plugin install/replace, no service/Scheduled Task mutation, no semantic send, no replay/redelivery/disposition, no manual Ticket/SQLite/session/transcript mutation, no protected-state mutation, no release promotion, and no force push.
