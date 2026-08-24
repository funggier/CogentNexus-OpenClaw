# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_WITH_HUMAN_GATE`
Current authorization: `PHASE_A_PLAN_ONLY`
Task ID: `CNX-20260824-058`
Updated: 2026-08-24 23:50 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 058 gate.

## Active task

[`tasks/CNX-20260824-058-fresh-rollover-plan-checkpoint.md`](tasks/CNX-20260824-058-fresh-rollover-plan-checkpoint.md)

## Predecessor disposition

Task 057 is reviewed `ACCEPT` as:

`ACCEPT_OPENCLAW_INVENTORY_SCHEMA_COMPAT_FIXED`

Accepted implementation commit:

`f379e5c5d8dddb144cb0d1991b645b16055e1303`

Accepted report commit:

`da3525c38c24f76e19c977e28446603b8c7c7063`

Task 057 review commit:

`0bfeefe9e889a4f336f8860efc9dcae0f73af7ad`

The repository compatibility fix is accepted. It made zero live mutations.

## Human authorization

The operator explicitly selected Hermes to continue Task 058 instead of Codex.

A manual continuation signal to Hermes authorizes evaluation/execution of this exact Phase A task only. It does not authorize recovery apply or any mutation outside the task fence.

## Authorized operation

Fresh read-only preservation preflight, one fresh supported OpenClaw plugin inventory capture, machine-generated rollover plan creation with the accepted Task 057 implementation, exact plan verification, and report-only checkpoint publication.

For a valid plan, Hermes must stop with `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY` and publish the exact plan SHA-256 for later ChatGPT review and a separate human gate.

## Executor/safety clarification

Hermes is the selected executor. The safety exclusion for `HermesAgent` refers to the separate HermesAgent project/system and does not prohibit Hermes from executing this CogentNexus-OpenClaw task.

## Safety

No `rollover-apply`, installer, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, lifecycle mutation, startup/supervisor enable, controller MANAGED transition, scheduler change, Gateway/Ollama/model mutation, process termination, primary-repository mutation, Procmon/Task 027/038 action, mutation of the separate HermesAgent project/system, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication.

Task 056 is terminal. Do not reuse its raw inventory or failed planning attempt as Task 058 planning input.
