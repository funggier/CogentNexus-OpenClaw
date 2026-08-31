# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_STDIN_QUALIFICATION_THEN_RESET_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-175_HERMES_STDIN_QUALIFICATION_THEN_RESET_REACCEPTANCE`
Task ID: `CNX-20260831-175`
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

[`tasks/CNX-20260831-175-hermes-stdin-qualification-reset-reacceptance.md`](tasks/CNX-20260831-175-hermes-stdin-qualification-reset-reacceptance.md)

Task 175 resolves the Task-174 confirmation-stdin blocker before any new destructive reset attempt.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task-171 through Task-173: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`

Task-174 did not cross confirmation and did not perform reset-owned destructive mutation. Task-171 semantic Send count remains permanently frozen at `1`.

## Task-175 gate A — harmless stdin qualification

Hermes/Codex must first use a harmless Python `input()` probe through the same executor terminal/process/stdin mechanism intended for reset.

The probe must round-trip a unique token and exit `0` without `OSError`, EOF, invalid-handle, or closed-stdin failure.

If this qualification fails: **do not run reset**. Report the stdin-channel blocker and stop.

No product/source repair is authorized merely to make the probe pass.

## Task-175 gate B/C — reset only after qualification

Only if the harmless stdin probe passes and a fresh critical preflight remains valid, Task 175 authorizes exactly one new installed reset invocation:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`

After the documented prompt is observed, provide exactly one interactive:

`y`

No pre-piped confirmation, no second reset, and no executor-issued lifecycle helper is authorized.

After reset starts, any failure/timeout/uncertainty is evidence to preserve, not permission to retry or repair.

## Required reset success boundary

If reset is run, PASS requires the command itself to return documented `COGENTNEXUS-OPENCLAW RESET: PASS` / `fresh-install MANAGED`, preserve the installed candidate and OpenClaw pin, reconstruct healthy MANAGED controller/plugin/Gateway/Ollama/route state, bootstrap a valid fresh DB, remove the exact old Task-171 reset-owned durable identities, manufacture no semantic/model/recovery work, and preserve external OpenClaw/Ollama/unrelated namespaces.

## Hard fence

Task 175 semantic action count: `0`.

Authorized only: read-only preflight; one harmless stdin probe; if and only if it passes, one reset invocation plus one interactive `y`; implementation-owned reset subprocesses/process boundaries; read-only postflight; Task-175 report publication.

No Dashboard Send, composer input, `chat.inject`, manual model/recovery action, product/source/test/workflow/dependency change, second reset, executor `start/stop/restart/enable/disable`, manual Gateway/Ollama restart, installer/uninstall/reinstall/rollback, manual durable/config/transcript mutation, upgrade, release, merge, or force push.

After Task-175 report publication, stop for ChatGPT review. Uninstall remains unauthorized.
