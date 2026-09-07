# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK305_BOUNDED_STAGING_INSTALLER`
Current disposition: `PASS_STAGING_INSTALLER_RETRY_GREEN__MANAGED_ENABLE_NOT_AUTHORIZED`
Task ID: `CNX-20260907-305`
Parent task: `CNX-20260907-304`
Updated: 2026-09-07 ICT — Task305 staging retry succeeded; managed enable remains separately gated

Assigned executor: `Hermes`
Review owner: `ChatGPT`

## Active Task305

`docs/operations/coordination/tasks/CNX-20260907-305-bounded-staging-installer-retry.md`

Hermes may perform exactly one supported staging installer retry using the repaired candidate, with technical autonomy for preflight/postflight. Stop before `cnxclaw enable`.

## Hard fences

No second installer retry, `cnxclaw enable`, plugin install/replace, service/Scheduled Task mutation, semantic send, replay/redelivery/disposition, manual durable-state mutation, protected-state mutation, release promotion, or force push.
