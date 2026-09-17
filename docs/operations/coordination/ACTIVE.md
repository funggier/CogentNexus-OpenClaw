# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX391_ISOLATED_PRODUCTION_CONFIG_HOOK_REGISTRATION_TRACE`
Execution mode: `ISOLATED_PRODUCTION_CONFIG_HOOK_REGISTRATION_TRACE`
Task ID: `CNX-20260917-391`
Parent: `CNX-20260917-390`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-390-production-config-isolated-hook-policy-replay-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-391-isolated-production-config-hook-registration-trace.md`

## Current position

CNX-390 was reviewed and accepted as `PRODUCTION_CONFIG_REPLAY_DIAGNOSTICALLY_BLOCKED`. The production-shaped isolated fixture loaded and activated through the real OpenClaw CLI, but the supported CLI did not expose `register(api)`, `api.on("before_agent_run")`, the host `registerTypedHook` decision, typed-hook inventory, or `hasHooks`. Therefore CNX-390 could not distinguish host acceptance from rejection. CNX-389 found no relevant User/Machine environment override; CNX-388 materially corroborates the production config source; CNX-381/382 provide the exact isolated loader/API and policy-gate mechanism for comparison.

## Current authorization

CNX-391 is READY for Hermes execution.

Use the exact relevant production plugin-entry configuration from `C:\Users\CDQ-P\.openclaw\openclaw.json` to construct a disposable isolated fixture. Execute the real installed OpenClaw `2026.7.1-2` loader/plugin lifecycle and use disposable instrumentation only outside production to observe the registration boundary directly: `register(api)` → `api.on("before_agent_run")` → host `registerTypedHook` → policy decision → final typed-hook registry / `hasHooks` where exposed.

This task is an isolated reproduction only. Do not present the result as production memory observation or direct production root-cause proof.

No production restart/reload.
No production configuration mutation.
No environment mutation.
No Scheduled Task mutation.
No OpenClaw dependency patch.
No CogentNexus source repair.
No production artifact deployment/rebuild.
No debugger/inspector attachment to production.
No semantic/model/provider request.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment-variable mutation.
- No Scheduled Task mutation.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No production artifact replacement/deploy.
- No debugger/inspector attachment to production.
- No semantic/model/provider/Dashboard requests.
- No TicketStore/admission/routing/auth changes.
- No speculative workaround.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-390.
- Do not start CNX-392 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-392.
