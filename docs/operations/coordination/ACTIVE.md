# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_RESET_PROMPT_CAPTURE_HARNESS_DIAGNOSIS_HERMES`
Current authorization: `CNX-20260831-176_HERMES_RESET_PROMPT_CAPTURE_HARNESS_DIAGNOSIS`
Task ID: `CNX-20260831-176`
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

[`tasks/CNX-20260831-176-hermes-reset-prompt-capture-harness-diagnosis.md`](tasks/CNX-20260831-176-hermes-reset-prompt-capture-harness-diagnosis.md)

Task 176 is a zero-destructive-action executor-harness diagnostic for the Task-175 reset completion-capture blocker.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Task-171 through Task-173: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`
- Task 175: `ACCEPTED_UNPROVEN — RESET_COMPLETION_BOUNDARY_UNAVAILABLE_AFTER_QUALIFIED_STDIN`

## Current diagnosis boundary

Task 175 proved a harmless redirected Python `input()` round trip works, but the reset wrapper timed out before preserving prompt/confirmation/exit evidence.

The accepted lifecycle source confirms the real confirmation uses:

`input("Continue? [y/N]: ")`

which emits a prompt without newline. A line-oriented prompt observer can therefore deadlock while the child waits for input. This is a hypothesis to prove or falsify, not yet an accepted root cause.

## Task-176 authorization

Hermes/Codex must diagnose the Task-175 harness using only disposable harmless Python processes and read-only source/launcher inspection.

Required outcome:

1. recover or reconstruct the Task-175 prompt-observation algorithm;
2. reproduce the exact reset-style no-newline prompt harmlessly;
3. determine whether the prior observer stalls on the no-newline prompt or another boundary;
4. qualify a temporary capture method with at least two harmless runs that proves prompt-before-input, exactly one input event, exact ACK, exit `0`, complete-enough output/result capture, and no orphan/timeout;
5. assess the installed launcher chain read-only for compatibility with the qualified method;
6. publish Task-176 report and stop.

## Hard fence

Task 176 authorizes destructive action count `0` and semantic action count `0`.

No reset, uninstall, installer/reinstall, live lifecycle helper, Gateway/Ollama restart, Dashboard Send, model/recovery action, manual durable/config/transcript mutation, product/source/test/workflow/dependency change, upgrade, release, merge, or force push.

Temporary diagnostic scripts/processes may exist only outside the repository/live product state and must be used solely for harmless prompt/capture qualification.

After Task-176 report publication, stop for ChatGPT review. Another reset is not authorized yet.
