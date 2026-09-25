# Coordination Status

Status: `IN_PROGRESS`
State: `CNX446_DASHBOARD_DIRECT_TERMINAL_BOUNDARY_RED_PENDING`
Task: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Branch: `cnx-446-dashboard-direct-terminal-final-boundary`
Executor: `ChatGPT`
Target release line: `v0.9.8`

## Current phase

Production defect reproduced from live OpenClaw 2026.9.5 evidence. Implementation has not yet been accepted.

The next authority is RED-to-GREEN regression work on Dashboard Direct terminal-result selection.

## Confirmed facts

- v0.9.7 is the current immutable published baseline.
- Ticket-first admission for the triggering session worked correctly.
- Direct routing worked correctly.
- The defect is downstream at result/delivery terminal selection.
- The false durable payload was the first progress/commentary message, not the final answer.
- `stopReason="stop"` exists on both progress and final and is not sufficient.
- OpenAI/Codex mirrored final evidence exposes `__openclaw.runTerminal=true`.
- Native Ollama terminal messages observed on the same OpenClaw 2026.9.5 runtime do not expose `runTerminal`; the repair must not require it globally.
- Provider/model/auth routing remains OpenClaw-owned.

## Current next gate

Create the CNX-446 RED regression before production code changes.
