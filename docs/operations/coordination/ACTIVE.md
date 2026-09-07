# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK307_SOURCE_TDD`
Task ID: `CNX-20260907-307`
Parent: `CNX-20260907-306`
Assigned executor: `Hermes`
Updated: 2026-09-07T13:55:29Z
Disposition: `REWORK_SOURCE_CONTRACT`

Active task: `docs/operations/coordination/tasks/CNX-20260907-307-activation-safety-contract-tdd.md`
Prior report: `docs/operations/coordination/reports/CNX-20260907-306-authority-identity-activation-preflight.md`

Task306 proved that live enable would select protected work, may activate an old pending delivery, and is not fully quiescence-fenced. Task307 is source-only strict TDD. No live install/enable/lifecycle, semantic send/Delete/cancel/replay/redelivery/disposition, manual durable/config mutation, protected-state mutation, release promotion or force push. Hermes may continue through exact-SHA CI and publish the matching report.
