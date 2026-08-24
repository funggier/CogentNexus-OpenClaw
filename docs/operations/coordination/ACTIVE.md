# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_WITH_HUMAN_GATE`
Current authorization: `MANAGED_REENTRY_AUTHORIZED`
Task ID: `CNX-20260825-061`
Updated: 2026-08-25 03:15 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a Task 061 execution gate.

## Active task

[`tasks/CNX-20260825-061-return-managed-lifecycle.md`](tasks/CNX-20260825-061-return-managed-lifecycle.md)

## Accepted predecessor

Task 060 result:

`PASS_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`

Task 060 report commit:

`0ae317d51a0efc13ebcfaabab6cb6b9595b2d2c5`

Task 060 review disposition:

`ACCEPT_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`

Task 060 review commit:

`633cefcfe06c83aae8aede17f3bf6b36ed4d3eb7`

Accepted post-rollover ownership-manifest SHA-256:

`0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`

The live installation now has exactly one canonical v0.9.3 payload owned at the active replacement generation. The prior generation is retained at the reviewed external rollover backup. Controller remains PASSTHROUGH, startup disabled, and plugin registration disabled.

## Human authorization

The operator asked ChatGPT to continue after Task 060. ChatGPT reviewed and accepted Task 060 and published Task 061 as the next bounded lifecycle step.

A manual continuation signal to Hermes authorizes execution of exactly Task 061 only.

## Authorized operation

Task 061 may freshly prove the accepted post-rollover state and installed-code identity, then invoke the supported installed command exactly once:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

Only the internal effects of that one supported Host `enable` sequence are authorized: MANAGED controller transition, managed policy application, canonical plugin enable/configuration, startup-adapter enablement, lifecycle/provider start, default-session reconciliation, bounded interrupted-work reconciliation, and one safe supervisor tick.

No individual substep may be reproduced manually.

## Required successful stop state

`PASS_MANAGED_REENTRY_VERIFIED`

A successful Task 061 must prove MANAGED mode, generation 8, desired Gateway/provider running, startup adapter enabled and exact, one loaded canonical v0.9.3 replacement plugin, exact managed configuration, exact managed AGENTS block over the preserved baseline, unchanged ownership/replacement/rollover-backup bindings, healthy Gateway/Ollama, and bounded Ticket/session continuity.

## Safety

No installer, reset, uninstall, rollover plan/apply, manual generation move/delete/copy, rollover-backup mutation, manual ownership edit, separate plugin enable/disable/config mutation, separate startup/lifecycle mutation, process termination, provider/model selection change, primary Git mutation, Procmon Task 027/038 action, HermesAgent mutation, Ecosystem/staged-capability-loop work, merge, tag, release, or archive publication.
