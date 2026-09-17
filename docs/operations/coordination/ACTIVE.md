# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX380_EXACT_ISOLATED_OPENCLAW_REGISTRY_TRACE`
Execution mode: `EXACT_ISOLATED_OPENCLAW_REGISTRY_DIAGNOSIS`
Task ID: `CNX-20260917-380`
Parent: `CNX-20260917-379`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-379-disposable-registry-trace-harness-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-380-exact-isolated-openclaw-registry-trace.md`

## Current position

CNX-376 proved the Dashboard dispatch boundary. CNX-377 found the current OpenClaw source model dynamically composes live registries but could not reproduce the divergence as a proven repository-side defect. CNX-378 correlated the production PID/build/effective artifact/plugin inventory but could not expose JavaScript object identity. CNX-379 proved disposable identity instrumentation and controlled failure-mode discrimination, but did not execute the exact OpenClaw/plugin lifecycle.

## Next authorized task

`CNX-20260917-380` is authorized to execute the exact installed OpenClaw `2026.7.1-2` module graph and effective CogentNexus plugin artifact in a non-production isolated process with temporary instrumentation, to observe real registry identities, lifecycle ordering, composition, and `hasHooks("before_agent_run")` visibility.

Diagnosis only. No repair is authorized.

## Authorization boundary

No Dashboard semantic request.
No production Gateway restart/reload.
No production configuration mutation.
No production OpenClaw dependency patch.
No permanent CogentNexus source patch.
Temporary instrumentation is allowed only in an isolated disposable environment and must not be committed.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No production runtime mutation.
- No production configuration mutation.
- No production Gateway restart/reload.
- No OpenClaw dependency patch.
- No CogentNexus source patch.
- No semantic request.
- No speculative repair.
- No permanent instrumentation.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-379.
- Do not start CNX-381 yourself.

## Closeout

Required classification:
`EXACT_REGISTRY_LIFECYCLE_CAUSE_REPRODUCED`, `EXACT_LIFECYCLE_STILL_CONTRADICTORY`, or `EXACT_ISOLATION_NOT_ACHIEVED`.

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
