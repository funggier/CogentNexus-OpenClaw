# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_WITH_HUMAN_GATE`
Current authorization: `PHASE_A_PLAN_ONLY`
Task ID: `CNX-20260825-059`
Updated: 2026-08-25 01:02 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 059 gate.

## Active task

[`tasks/CNX-20260825-059-reprove-rollover-plan-input-binding.md`](tasks/CNX-20260825-059-reprove-rollover-plan-input-binding.md)

## Predecessor disposition

Task 058 report commit:

`1650436aabb5d9c384e44a0e10013047090b7729`

Task 058 reported plan SHA-256:

`360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`

Task 058 is reviewed:

`REWORK_INVENTORY_CAPTURE_BINDING_AMBIGUOUS`

Task 058 review commit:

`0e93970e145c8795d6578b8a4df6d2f198f6b3d9`

The Task 058 plan is not accepted and is not eligible for apply authorization.

## Reason for rework

Task 058 required exactly one `openclaw plugins list --json` invocation, but its report also records an identical-state recapture and retains a `before-recapture` inventory file. This makes the exact raw-byte planner-input binding ambiguous despite the reported normalized equality.

The Task 058 report also omitted the required fresh Task 049 manifest SHA-256 from durable publication.

## Human authorization

The operator asked ChatGPT to continue the coordination workflow and previously selected Hermes as executor.

A manual continuation signal to Hermes authorizes evaluation/execution of this exact Task 059 Phase A checkpoint only. It does not authorize recovery apply or any mutation outside the task fence.

## Authorized operation

Task 059 may perform a fresh read-only preservation checkpoint, exactly one immutable OpenClaw plugin inventory capture, exactly one machine-generated rollover-plan invocation using that exact raw file, complete binding verification, and report-only publication.

For a valid fresh plan, Hermes must stop with `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY` and publish the exact new plan SHA-256 for ChatGPT review and a separate explicit human gate.

## Safety

No Task 058 plan reuse. No `rollover-apply`, installer, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, lifecycle mutation, startup/supervisor enable, controller MANAGED transition, scheduler change, Gateway/Ollama/model mutation, process termination, primary-repository mutation, Procmon/Task 027/038 action, mutation of the separate HermesAgent project/system, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication.
