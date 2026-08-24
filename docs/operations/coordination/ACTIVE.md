# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_WITH_HUMAN_GATE`
Current authorization: `PHASE_B_APPLY_AUTHORIZED`
Task ID: `CNX-20260825-060`
Updated: 2026-08-25 01:27 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a Task 060 execution gate.

## Active task

[`tasks/CNX-20260825-060-apply-approved-plugin-generation-rollover.md`](tasks/CNX-20260825-060-apply-approved-plugin-generation-rollover.md)

## Explicit human authorization

At 2026-08-25 01:27 ICT, the operator explicitly approved this exact accepted Task 059 plan SHA-256 for Phase B:

`f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`

This satisfies the human gate required by the accepted Task 059 review.

## Accepted predecessor

Task 059 report commit:

`d832d5d9a0566f122817c32401d847739ba8ebb1`

Task 059 review decision:

`ACCEPT_ROLLOVER_PLAN_INPUT_BINDING_REPROVED`

Task 059 review commit:

`756a1f96164d95e82d694fd062878092f2ac74fe`

Accepted local plan path:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json`

## Authorized operation

A manual continuation signal to Hermes now authorizes execution of the exact Task 060 only.

Task 060 may:

- create its bounded evidence directory;
- perform the required read-only drift/preflight checks;
- capture one fresh pre-apply OpenClaw inventory;
- verify the exact approved plan SHA and apply-time normalized inventory/registration bindings;
- run the accepted root-process exit-code self-test;
- invoke the reviewed `rollover-apply` primitive exactly once using the exact approved Task 059 plan/SHA and fresh Task 060 inventory;
- perform read-only post-apply ownership/runtime/plugin verification;
- publish only the matching Task 060 report.

The reviewed apply may perform only its internal exact-path backup/atomic retirement and ownership-manifest atomic update. If its verification fails, its built-in rollback semantics apply. No manual repair or retry is authorized.

## Required successful stop state

A successful Task 060 must stop with:

`PASS_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`

Controller must remain PASSTHROUGH and startup must remain disabled. No lifecycle return to MANAGED is authorized in Task 060.

## Safety

No plan regeneration, no Task 058 plan reuse, no second `rollover-apply`, no manual generation move/delete/copy, no manual ownership rewrite, no plugin install/uninstall/enable/disable, no installer/reset/uninstall/lifecycle mutation, no controller MANAGED transition, no startup/supervisor/scheduler mutation, no Gateway/Ollama/model/process mutation, no primary Git repository checkout/reset/clean/source edit, no Procmon/Task 027/038 action, no HermesAgent mutation, no Ecosystem/staged-capability-loop work, and no merge/tag/release/archive publication.

The rejected Task 058 plan SHA-256 `360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c` remains permanently ineligible.
