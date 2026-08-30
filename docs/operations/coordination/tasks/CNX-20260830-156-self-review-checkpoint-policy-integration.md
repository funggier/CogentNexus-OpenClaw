# CNX-20260830-156 — Self-Review Checkpoint Policy Integration

Status: `DRAFT_DESIGN_CHECKPOINT`
Execution mode: `OFFLINE_COORDINATION_POLICY_DESIGN`
Owner: ChatGPT

## Objective

Integrate the operator-approved workflow rule that ChatGPT may continue execution and perform review itself using durable Task/Review checkpoints, while Hermes remains an optional handoff used only when materially necessary.

## Design gate

This task is currently a durable design checkpoint only. No coordination policy semantics are changed by this file alone.

Before implementation, inspect the existing coordination/review/handoff rules and present the proposed policy design to the operator for approval.

## Hard fence

No live Windows/runtime mutation; no Dashboard semantic Send; no install/reset/uninstall/reinstall; no production code change; no merge/tag/release; no force push.
