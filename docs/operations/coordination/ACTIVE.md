# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-182_HERMES_REPAIRED_CANDIDATE_INSTALL_OVER_REACCEPTANCE`
Task ID: `CNX-20260831-182`
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

[`tasks/CNX-20260831-182-hermes-repaired-candidate-windows-install-over-reacceptance.md`](tasks/CNX-20260831-182-hermes-repaired-candidate-windows-install-over-reacceptance.md)

## Accepted state

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate active-facade target SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Task 181 clean process boundary:

`ACCEPTED_PASS — HISTORICAL_TASK178_OUTER_OBSERVER_RETIRED_CLEAN_BOUNDARY_PROVEN`

Task 180 was blocked before installer invocation and performed zero product lifecycle mutation.

## Task-182 authorization

After a fresh clean-boundary/runtime/durable preflight, Hermes/Codex may perform exactly one supported Windows install-over from exact candidate `f6392da3...`.

Primary acceptance proof is byte identity between the clean candidate `skills/cogentnexus-openclaw/scripts/cnxclaw.py` and the actual installed facade reached by the active `cnxclaw.cmd` chain. Required installed facade SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`.

## Hard fence

Task 182 semantic action budget: `0`.

No reset, uninstall, second installer/retry, executor lifecycle helper, manual Gateway/Ollama restart, Dashboard Send, model/recovery action, manual state repair, source/product/test/workflow edit, release/tag/merge, or force push.

Installer-owned internal lifecycle stages are authorized only inside the one supported install-over.

After Task-182 report publication, stop for ChatGPT review. Another reset remains unauthorized.
