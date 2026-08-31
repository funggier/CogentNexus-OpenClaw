# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_CMD_BATCH_INCREMENTAL_HARNESS_QUALIFICATION_HERMES`
Current authorization: `CNX-20260831-177_HERMES_CMD_BATCH_INCREMENTAL_HARNESS_QUALIFICATION`
Task ID: `CNX-20260831-177`
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

[`tasks/CNX-20260831-177-hermes-cmd-batch-incremental-harness-qualification.md`](tasks/CNX-20260831-177-hermes-cmd-batch-incremental-harness-qualification.md)

Task 177 is a zero-destructive/zero-semantic qualification of the Windows `cmd.exe → .cmd → Python input()` topology and incremental evidence harness intended for a future reset acceptance attempt.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Dashboard/native/durable acceptance: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`
- Task 175: `ACCEPTED_UNPROVEN — RESET_COMPLETION_BOUNDARY_UNAVAILABLE_AFTER_QUALIFIED_STDIN`
- Task 176: `ACCEPTED_DIAGNOSTIC_PASS — CHARACTER_PROMPT_CAPTURE_QUALIFIED_TASK175_ROOT_CAUSE_REMAINS_UNPROVEN`

Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Current gate

Task 176 proved character-level prompt capture with two direct harmless Python runs, but it also proved the Task-175 wrapper already used `read(1)`, so the actual timeout root cause remains unestablished. The remaining unqualified boundary is the Windows process topology and completion chain around `cmd.exe` / `.cmd` / Python child plus durable result finalization.

Task 177 must reproduce that topology harmlessly using disposable temporary files and qualify the exact incremental harness architecture intended for a future reset.

Required minimum:

1. `outer harness → cmd.exe /d /c → disposable .cmd → disposable Python input child`;
2. character/byte prompt detection for `Continue? [y/N]: `;
3. concurrent stdout/stderr draining;
4. incremental durable event ledger written before final child exit;
5. prompt observed before input;
6. exactly one unique token line per run;
7. exact ACK, exit `0`, no timeout, no orphan;
8. at least two independent successful harmless runs;
9. read-only correlation to the installed `cnxclaw.cmd` launcher topology and hashes;
10. no live product/runtime/durable mutation.

## Hard fence

Task 177 destructive action budget: `0`.
Task 177 semantic action budget: `0`.

No reset, uninstall, install/reinstall, start/stop/restart/enable/disable, Gateway/Ollama lifecycle mutation, Dashboard Send, model/recovery action, manual durable/config/transcript mutation, product/source/test/workflow/dependency change, upgrade, release, merge, or force push.

After Task-177 report publication, stop for ChatGPT review. A future reset requires a new separate authorization.
