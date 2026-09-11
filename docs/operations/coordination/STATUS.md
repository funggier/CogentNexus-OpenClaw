# Coordination Channel Status

Status: `IN_PROGRESS`
State: `V095_PROVIDER_RUNTIME_COMMAND_REPAIR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260909-315`
Parent: `CNX-20260907-314`
Base release: `v0.9.4`
Base commit: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
Working branch: `agent/v0.9.5-architecture-repair`

## Current authority

v0.9.4 is the current public baseline. Task315 is the active v0.9.5 architecture-repair line.

## Current invariant

OpenClaw owns provider/model/auth/routing. CogentNexus owns Ticket, workflow, context continuity, recovery authority, durable delivery, and session ownership while active. Local Ollama is an optional local adapter and must not mutate OpenClaw routing.

## Current Plan 1 position

Core provider/runtime repair is implemented and the public CNX CLI no longer acts as a provider-routing authority. The public reset path is now provider-neutral through `reset_v095.py`; the canonical local-adapter interface is exposed by `local_adapters_v095.py` with the older `local_adapter.py` retained only as a compatibility facade.

Focused invariant tests cover CNX lifecycle/provider routing separation, local-adapter routing separation, legacy `--provider` rejection, reset provider neutrality, and provider-switch state invariants.

The last exact-head full validation before the most recent reset/adapter/doc changes passed. A fresh exact-head Actions run is required after the current changes.

## Current next step

Wait for fresh exact-HEAD Actions evidence. If all required workflows pass, update the Plan 1 closeout checklist/checkpoint and authorize Plan 2. If a new failure appears, diagnose the exact failing boundary before any further production change.

## Hard fences

- No force push.
- No release/tag/public-version mutation before Plans 1-3 are green.
- No live provider/model/auth route mutation during source repair.
- No provider selection in normal CNX lifecycle or reset authority.
- Preserve exact-delivery, terminal, owner-generation, config-race, stale-wake, and recovery safety fences.
