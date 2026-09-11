# Active Coordination Task

Status: `IN_PROGRESS`
State: `V095_PLAN2_SESSION_GENERATION`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260911-PLAN2`
Parent: `CNX-20260909-315`
Base release: `v0.9.4`
Base commit: `1e81b3cb9a8fe31a8e4df90563f15a3cde255c59`
Working branch: `agent/v0.9.5-plan2-delivery-session-identity`

## Objective

Complete the remaining Plan 2 session-generation contract after the verified Plan 1 architecture repair was merged into `main`.

## Current focus

Introduce the pure `shouldAdvanceSessionGeneration()` decision contract with RED-first validation, then route any required lifecycle decisions through it without adding another session authority.

## Completed baseline

- Plan 1 provider/runtime/command repair merged into `main`.
- Canonical InferenceAttempt persistence is present.
- Canonical Delivery Core persistence/state transitions are present.
- Session deletion/recreation generation behavior is already implemented and regression-tested.

## Current RED boundary

`v095-session-generation.test.ts` exists on this branch and intentionally imports a not-yet-created implementation module. The next gate is a fresh Actions run proving the focused RED behavior.

## Hard fences

- Do not modify `main` directly.
- No force push.
- No release/tag/public-version mutation.
- No provider/model/auth routing mutation.
- Preserve exact Ticket, InferenceAttempt, DeliveryAttempt, sessionId and generation ownership semantics.
