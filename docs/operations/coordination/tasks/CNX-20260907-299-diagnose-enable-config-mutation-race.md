# CNX-20260907-299 — Diagnose Enable Config Mutation Race

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-298`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Determine the root cause and safe recovery boundary for Task298's `ConfigMutationConflictError` during canonical `cnxclaw enable`.

## Evidence

Task298 invoked `cnxclaw enable` exactly once. It failed during host-transition because config changed since last load, then reported transactional rollback. No repair was adopted and no retry is authorized.

## Allowed work

- Read current repository and coordination state.
- Inspect source for config fingerprint/load/commit conflict handling and host-transition ownership.
- Inspect retained Task298 pre/post evidence and read-only current config/state provenance.
- Identify which process/actor changed config and what re-anchor or quiescence precondition is required.
- Propose a minimal, bounded successor deployment task.
- Repository-only tests/analysis are allowed; do not mutate live runtime.

## Prohibited

No `cnxclaw enable` retry, no restart/reload, no installer/uninstall/reset, no manual config/SQLite/Ticket/session/transcript mutation, no semantic send, replay/redelivery/disposition, credential action, protected-state mutation, release, or force push.

## Completion

Publish a root-cause report. If a deterministic repository repair is proven, create a separate TDD repair task; otherwise set `NEEDS_CHATGPT` with exact required authority and preconditions.
