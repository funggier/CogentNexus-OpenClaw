# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX368_TICKET_FIRST_ADMISSION_ROOT_CAUSE_REPAIR`
Execution mode: `ROOT_CAUSE_INVESTIGATION_AND_MINIMAL_REPAIR`
Task ID: `CNX-20260916-368`
Parent: `CNX-20260916-367`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-367-openai-dashboard-ticket-first-semantic-requalification-report.md`

## Current position

CNX-367 is completed with classification `CURRENT_RED`. The original Dashboard Ticket-first bypass is reproduced and evidenced: for the exact CNX-367 execution, the runtime proceeds from `prompt.submitted` directly to `model.completed`, with no `before_agent_run`, admission trace, durable Ticket, Ticket lifecycle, or Ticket-linked Run/Call/Inference/Result/Delivery evidence.

## Next authorized task

`CNX-20260916-368` is the successor root-cause investigation and repair task. It must trace the failing boundary, add diagnostic-only instrumentation if needed, then use TDD for one minimal repair. It may not send another Dashboard/model request or perform live semantic requalification. Any live semantic requalification requires a separate later authorization after CNX-368 stops.

## Hard fences

- Do not modify historical CNX-360 through CNX-367 task/report files.
- Do not send another Dashboard/model request or semantic test.
- Do not mutate runtime state or reinstall.
- Do not edit controller/provider/auth/routing/hooks/main until the root cause is proven and the task's TDD gate is satisfied.
- Do not release/tag, force-push, or rewrite history.
