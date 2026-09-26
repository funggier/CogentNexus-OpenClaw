# CNX-20260926-451 — Soft Context Pressure Must Not Block Dashboard Turns

Status: `ACTIVE`
Owner: ChatGPT
Executor: ChatGPT
GitHub issue: `#43`
Baseline SHA: `3a08d06d3b152e347011b6bdafeef985c2ed45ad`
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-451-soft-context-pressure-pass`

## Production evidence

- Dashboard session: `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8`.
- Turn 1 completed normally.
- Turn 2 completed normally after four Ollama model calls.
- Turn 3 Ticket: `CNXT-d4189017-56de-42b2-aec8-a0cf6f0be482`.
- Turn 3 pressure: `21093 / 24576 = 85.8%`, level `soft`, source `fresh-session-counter`.
- Event `context_pressure_deferred` was immediately followed by Ticket `failed/permanent` with `blocked by cogentnexus-openclaw`.
- No model call or inference attempt started for turn 3.

## Root cause

`v091-context-guard.ts` treats every non-normal pressure level as a blocking barrier. OpenClaw 2026.9.5 interprets `before_agent_run outcome=block` as terminal send failure, not as a resumable/deferred turn primitive. The soft-pressure path therefore converts a proactive safety hint into a user-visible permanent failure.

## Required semantics

1. Normal pressure: pass.
2. Soft pressure: pass current owner inference; do not set Ticket interrupted/permanent; do not enqueue Direct recovery; do not create blocking context-maintenance authority.
3. Record durable soft-pressure observation for diagnostics.
4. Hard pressure: preserve the existing barrier/maintenance/recovery behavior in this task.
5. Keep CNX-426 turn-budget/model-switch authority unchanged.
6. Keep CNX-448 terminal authority and CNX-449 long-running lease behavior unchanged.
7. `v0.9.8` remains immutable.

## TDD acceptance

- RED fixture reproduces `21093/24576` soft pressure and currently sees `outcome=block`.
- GREEN returns `outcome=pass`.
- Ticket stays `accepted` with no failure mutation.
- No `cnx_direct_recovery` or `cnx_context_maintenance` row is created for soft pressure.
- Durable `context_pressure_soft_observed` event is recorded.
- Hard-pressure fixture still blocks and queues maintenance/recovery.
- Full plugin/Python/build/CI/install-over/live Dashboard validation.

## Local qualification checkpoint

- RED reproduced the live soft-pressure permanent block.
- GREEN focused CNX-451 + CNX-426: `8/8 PASS`.
- Full Python: `747 passed, 5 skipped, 38 subtests passed`.
- Full Vitest: `95 files / 444 tests PASS`.
- build/evaluation/plugin validation/audit/diff-check: PASS.
- evaluation evidence SHA-256: `3f7aa713ef6987c0d6e72e96ac277dc8b060c18728aa79e15aea1e4b0f7b026a`.

## Current classification

`CNX451_LOCAL_GREEN_CI_PENDING`
