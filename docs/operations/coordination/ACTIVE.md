# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK305_BOUNDED_STAGING_INSTALLER`
Current disposition: `BOUNDED_STAGING_RETRY__EXACTLY_ONE__HERMES_READY`
Task ID: `CNX-20260907-305`
Parent task: `CNX-20260907-304`
Updated: 2026-09-07 ICT — Task304 GREEN; Task305 authorizes one repaired staging installer retry

Assigned executor: `Hermes`
Review owner: `ChatGPT`

## Active Task305

`docs/operations/coordination/tasks/CNX-20260907-305-bounded-staging-installer-retry.md`

Hermes may perform exactly one supported staging installer retry using the repaired candidate, with technical autonomy for preflight/postflight. Stop before `cnxclaw enable`.

## Hard fences

No second installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual durable-state mutation, protected-state mutation, release promotion, or force push.
