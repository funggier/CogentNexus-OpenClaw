# CNX-20260907-301 — Build Supported Supervisor Quiescence Mechanism

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-300`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

ChatGPT authorizes Hermes to choose and implement the minimal repository-level technical improvement needed to make Supervisor quiescence safe and bounded. Hermes may decide implementation details within this task without asking micro-confirmations.

This task authorizes repository/source/tests/CI changes only. It does not authorize live deployment, Scheduled Task mutation, service restart, Ticket mutation, or semantic actions.

## Objective

Design and implement a supported task-scoped quiescence/coordination mechanism that prevents the recurring CogentNexus Supervisor from racing the `cnxclaw enable` config transaction, with an explicit restore/readback contract.

## Requirements

- Start with TDD RED.
- Prefer a shared coordinator/lease/lock or existing supported host lifecycle primitive over ad-hoc scheduler disable/enable.
- Scope quiescence only to CogentNexus Supervisor/config writers required for the enable transaction.
- Make stale-owner, timeout, crash, and restore behavior fail closed and observable.
- Preserve protected Ticket/session and delivery semantics.
- Add focused tests for concurrent writer, stale lease, timeout, restoration, and no-op/rollback paths.
- Run focused and relevant repository validation to GREEN.
- Document exact future live invocation and postconditions.

## Prohibited

No live `cnxclaw enable`, no Scheduled Task mutation, no service restart/reload, no installer/uninstall/reset/install-over, no semantic send, no replay/redelivery/disposition, no Ticket/SQLite/session/transcript/config mutation in the live installation, no credential action, no protected-state mutation, no release or force push.

## Completion

Publish an evidence-rich report with design rationale, RED/GREEN tests, files/commits, and the exact bounded live requalification task proposed next. Stop at the repository repair boundary for ChatGPT review.
