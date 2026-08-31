# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_STDIN_QUALIFICATION_THEN_RESET_REACCEPTANCE_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-175`

## Active work

[`tasks/CNX-20260831-175-hermes-stdin-qualification-reset-reacceptance.md`](tasks/CNX-20260831-175-hermes-stdin-qualification-reset-reacceptance.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted baseline

- Accepted product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed candidate fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Dashboard/native/durable acceptance: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`

## Task 174 reviewed

Disposition:

`ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`

Task 174 started one normal installed reset process, reached the confirmation prompt, then Python `input()` raised `OSError: [Errno 9] Bad file descriptor` before any `y` was supplied.

Important boundaries:

- Task-174 reset invocation: `1`;
- explicit `y`: `0`;
- destructive reset transaction reached: `0`;
- second reset/helper lifecycle: `0`;
- semantic/model/recovery actions: `0`;
- original controller/runtime/DB state remained intact after the blocked attempt.

The evidence establishes the failure boundary but does not yet distinguish executor stdin/PTY failure from a launcher/product-specific stdin problem.

## Task 175 objective

Qualify the interactive stdin path before attempting another destructive action.

### Gate A

Run one harmless Python `input()` round-trip probe through the same terminal/process/stdin mechanism intended for reset.

If the probe cannot accept and echo a unique token with exit `0`, Task 175 must stop `BLOCKED`; reset is not authorized.

### Gates B/C

Only after the stdin probe passes, re-check the critical installed/runtime/DB baseline. If still valid, Task 175 authorizes exactly one new `cnxclaw.cmd reset` invocation and exactly one `y` after the real prompt is observed.

This new authorization is not a retry under Task 174. Task 174 remains closed.

No pre-piped confirmation is accepted as the interactive reset proof.

## Success boundary if reset runs

A PASS requires reset itself to reconstruct fresh `MANAGED` state without executor repair, preserve installed fingerprint/release and OpenClaw pin, produce healthy controller/plugin/Gateway/Ollama/route state, create a valid fresh SQLite state, remove the exact old Task-171 reset-owned Ticket/run/model/delivery identities, manufacture no semantic/model/recovery work, and preserve external OpenClaw/Ollama/unrelated namespaces.

## Hard fence

Task 175 semantic action budget is `0`.

No Dashboard Send, composer submission, `chat.inject`, model inference, recovery/regeneration, source/product/test/workflow/dependency change, second reset, executor-issued lifecycle helper, manual Gateway/Ollama restart, installer/uninstall/reinstall/rollback, manual durable/config/transcript mutation, upgrade, release, merge, or force push.

After Task-175 report publication, stop for ChatGPT review. Uninstall is not authorized yet.
