# Coordination Status

Status: `IDLE`
State: `CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`
Task: none
Branch: `cnx-448-native-ollama-terminal-boundary`
Executor: none
Baseline release: `v0.9.8` (immutable)
Baseline SHA: `49915000ecbec131112937cd44ec7a5f0effa00a`

## Accepted predecessor

CNX-447 / v0.9.8 is complete and remains immutable.

CNX-446 proved the terminal-authority pattern for Codex/App-Server mirrored messages: progress/tool writes cannot settle Direct delivery; exact mirrored `runTerminal=true` final authority is required.

## New live defect

Native Ollama session `4e97d1d4-2007-43d0-838d-0a929f1e8140` demonstrated that the preserved native fallback is too permissive:

- `ollama/qwen3.8:27b`;
- exact run `189e1a24-8230-4d50-90fc-d24d25ca1acc`;
- assistant `stopReason="toolUse"` with tool calls;
- intermediate text was incorrectly staged/delivered;
- Ticket completed before tool continuation;
- later host state was `interrupted`, yielding `host_terminal_conflict`.

## Local repair result

The production topology was reproduced RED before source changes. The repair now classifies native OpenClaw terminal authority before the existing Direct settlement boundary:

- `toolUse` / tool-call-bearing assistant writes: non-terminal;
- aborted/error/timeout/interrupted writes: not terminal success;
- native exact `__openclaw.runId`: exact Ticket/session fence;
- true native terminal success: existing durable settlement remains valid;
- Codex/App-Server CNX-446 behavior: unchanged.

Validation: focused `20/20`, full Vitest `94/441`, full Python `745 passed / 5 skipped / 38 subtests`, build/evaluation/plugin validation/audit/diff-check PASS.

GitHub issue: `#40`.

## Final qualification

- implementation SHA: `d6cf9e9c532da00880c16a700495edb833658cb4`;
- focused contracts: `20/20 PASS`;
- full plugin Vitest: `94 files / 441 tests PASS`;
- full Python: `745 passed, 5 skipped, 38 subtests passed`;
- build/evaluation/plugin validation/audit/diff-check: PASS;
- exact-SHA GitHub CI: Validate `36214305293`, PS5.1 `36214305250`, Windows Installer Pack `36214305241` — all SUCCESS;
- physical install-over: exit `0`, MANAGED generation `34`;
- package/installed parity: `296/296` exact, manifest SHA-256 `9559891cbdb63bf58b4b2b3fd05068ee0013fd7d65f2342d9ced7eee8c298b29`;
- fresh native Ollama tool-use continuation: PASS;
- SQLite integrity: `ok`;
- non-terminal Tickets: `0`;
- pending outbox: `0`;
- pending assistant delivery: `0`.

The long-running qwen3.8 control exercised the existing recovery path under memory pressure and completed exactly once. Timeout/recovery policy remains unchanged.

## Current classification

`CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`

No active task.
