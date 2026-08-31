# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_QUALIFIED_HARNESS_RESET_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-178_HERMES_QUALIFIED_HARNESS_RESET_REACCEPTANCE`
Task ID: `CNX-20260831-178`
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

[`tasks/CNX-20260831-178-hermes-qualified-harness-reset-reacceptance.md`](tasks/CNX-20260831-178-hermes-qualified-harness-reset-reacceptance.md)

Task 178 is the next bounded real-Windows reset reacceptance using the Task-177-qualified cmd/batch incremental evidence harness.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Task 171–173: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task 177: `ACCEPTED_DIAGNOSTIC_PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`

Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Task-178 authorization

After fresh preflight, Hermes/Codex may run exactly one new installed reset invocation:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`

It must be executed through the Task-177-qualified architecture: character/byte prompt detection, concurrent stdout/stderr drain, append-only flushed/fsync'd event ledger, prompt recorded before input intent, exactly one `y` line, and incremental completion evidence.

No pre-piped confirmation is allowed. No second reset or second `y` is authorized.

## Required success boundary

PASS requires reset itself to return exit `0` with the documented reset PASS / `fresh-install MANAGED` markers, preserve the accepted installed candidate and OpenClaw pin, reconstruct healthy MANAGED plugin/controller/Gateway/Ollama/route state, bootstrap a valid fresh DB, remove the exact old Task-171 reset-owned Ticket/run/model/delivery identities, manufacture no semantic/model/recovery work, and preserve external OpenClaw/Ollama/unrelated namespaces within contract.

## Hard fence

Task 178 semantic action budget: `0`.

After reset starts: no retry, second `y`, process kill for cleanup, start/stop/restart/enable/disable, manual Gateway/Ollama restart, installer/uninstall/reinstall/rollback, route/config/DB repair, recovery/regeneration, Dashboard Send, model invocation, manual durable/config/transcript mutation, source/product/test/workflow/dependency change, upgrade, release, merge, or force push.

Implementation-owned reset subprocesses/process boundaries are authorized only as part of the single reset command.

After Task-178 report publication, stop for ChatGPT review. Uninstall remains unauthorized.
