# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_QUALIFIED_HARNESS_RESET_REACCEPTANCE_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-178`

## Active work

[`tasks/CNX-20260831-178-hermes-qualified-harness-reset-reacceptance.md`](tasks/CNX-20260831-178-hermes-qualified-harness-reset-reacceptance.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted baseline

- Accepted product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed candidate fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Dashboard/native/durable result: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`

## Reset acceptance history

- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`
- Task 175: `ACCEPTED_UNPROVEN — RESET_COMPLETION_BOUNDARY_UNAVAILABLE_AFTER_QUALIFIED_STDIN`
- Task 176: `ACCEPTED_DIAGNOSTIC_PASS — CHARACTER_PROMPT_CAPTURE_QUALIFIED_TASK175_ROOT_CAUSE_REMAINS_UNPROVEN`
- Task 177: `ACCEPTED_DIAGNOSTIC_PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`

Task 177 closed the remaining executor-harness qualification gap. Two harmless cmd/batch/Python runs proved prompt-before-input, one input, concurrent stdout/stderr draining, flushed/fsync'd incremental event ledger, exact ACK, exit `0`, and no timeout/orphan.

## Task 178 objective

Use that qualified architecture for one new bounded live reset attempt.

Fresh preflight must pass first. Then exactly one installed `cnxclaw.cmd reset` may be started. The harness must durably record the real prompt before confirmation intent, send exactly one `y`, and retain event/output/process evidence incrementally rather than relying on a post-completion-only artifact.

If the observer times out or disconnects, do not relaunch reset, resend `y`, kill for a cleaner result, or issue helper lifecycle commands. Preserve the ledger and report the exact boundary.

## PASS boundary

A Task-178 PASS requires all of:

- exactly one reset invocation;
- real prompt observed before exactly one `y`;
- no retry/helper/kill/repair;
- exit `0` and documented reset PASS / `fresh-install MANAGED` markers;
- accepted installed fingerprint/release preserved;
- OpenClaw remains `2026.7.1-2`;
- healthy fresh MANAGED controller/plugin/Gateway/Ollama/route state produced by reset itself;
- fresh SQLite integrity/schema valid;
- exact old Task-171 reset-owned Ticket/run/model/delivery identities removed;
- zero semantic/model/recovery work manufactured;
- external OpenClaw/Ollama/unrelated namespaces preserved within contract.

Any materially unproven required condition invalidates PASS.

## Hard fence

Task 178 semantic action budget is `0`.

No Dashboard Send, composer submission, `chat.inject`, manual model/recovery action, second reset, second `y`, process kill for cleanup, executor start/stop/restart/enable/disable, manual Gateway/Ollama restart, installer/uninstall/reinstall/rollback, manual route/config/DB/durable/transcript repair, source/product/test/workflow/dependency change, upgrade, release, merge, or force push.

After Task-178 report publication, stop for ChatGPT review. Uninstall is not authorized yet.
