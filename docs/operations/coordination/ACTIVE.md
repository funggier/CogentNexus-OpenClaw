# Active Coordination Task

Status: `READY_FOR_EXECUTION`
State: `CNX426_READY_FOR_EXECUTION`
Execution mode: `MODEL_SWITCH_CONTEXT_BUDGET_REPAIR`
Task ID: `CNX-20260919-426`
Parent: `CNX-20260919-425`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Task: `docs/operations/coordination/tasks/CNX-20260919-426-model-switch-aware-context-pressure-budget-repair.md`
Expected report: `docs/operations/coordination/reports/CNX-20260919-426-model-switch-aware-context-pressure-budget-repair-report.md`

## Live evidence

OpenClaw 2026.9.4 provider/model switching is working.

A same-session switch to `ollama/qwen3.8:27b` exposed a false context-pressure block because CNX evaluated the turn with a stale/fallback `32768` context window instead of the host-resolved turn budget.

## Repair invariant

At `before_agent_run`, a valid OpenClaw `ctx.contextTokenBudget` is authoritative for the current turn's context window.

Session counters remain valid token-usage evidence but must not override the turn-local budget after a model switch.
