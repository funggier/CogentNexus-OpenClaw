# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-183_HERMES_QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTANCE`
Task ID: `CNX-20260831-183`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-183-hermes-qualified-harness-reset-fresh-state-reacceptance.md`](tasks/CNX-20260831-183-hermes-qualified-harness-reset-fresh-state-reacceptance.md)

## Accepted state

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Task 181 process hygiene:

`ACCEPTED_PASS — HISTORICAL_TASK178_OUTER_OBSERVER_RETIRED_CLEAN_BOUNDARY_PROVEN`

Task 182 installed-candidate acceptance:

`ACCEPTED_PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACCEPTED`

Required active installed facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Task-183 authorization

Task 183 authorizes one new reset acceptance action only.

After fresh authority/runtime/process/durable preflight, Hermes/Codex may launch exactly one installed `cnxclaw.cmd reset` through the Task-177-qualified incremental character-prompt harness architecture and the Task-179 repaired interactive facade.

The executor may send exactly one literal `y` only after observing the exact real `Continue? [y/N]: ` prompt and durably recording the prompt/input-intent events.

No reset retry is authorized under any timeout, shell disconnect, missing final artifact, or ambiguous completion state.

## Required outcome

PASS requires reset child exit `0`, exact RESET PASS/fresh-install MANAGED markers, active facade/release preservation, MANAGED Ollama route and healthy Gateway/provider, valid ownership/SQLite, zero reset-owned Ticket/delivery/session/model-call data, and preservation of external OpenClaw/Ollama assets.

## Hard fence

Task 183 reset invocation budget: `1`.
Confirmation send budget: `1` literal `y` line.
Semantic/model/recovery action budget: `0`.

No installer/install-over/reinstall, uninstall, second reset, second input send, executor lifecycle helper, Dashboard Send, model/recovery action, manual state repair, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-183 report publication, stop for ChatGPT review. Uninstall remains unauthorized.
