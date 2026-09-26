# Coordination Status

Status: `ACTIVE`
State: `CNX448_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-448-native-ollama-terminal-boundary-and-long-running-semantics.md`
Branch: `cnx-448-native-ollama-terminal-boundary`
Executor: `ChatGPT`
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

## Current classification

`CNX448_LOCAL_GREEN_CI_PENDING`

## Next gate

Commit/push exact candidate SHA, require GitHub CI GREEN, then perform physical install-over/source-parity and fresh native Ollama acceptance.
