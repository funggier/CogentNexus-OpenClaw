# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX392_PRODUCTION_VS_CONFIG_ORIGIN_HOOK_POLICY_REPLAY`
Execution mode: `PRODUCTION_VS_CONFIG_ORIGIN_HOOK_POLICY_REPLAY`
Task ID: `CNX-20260917-392`
Parent: `CNX-20260917-391`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-391-isolated-production-config-hook-registration-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-392-production-vs-config-origin-hook-policy-replay.md`

## Current position

CNX-391 was reviewed and accepted as `PRODUCTION_CONFIG_REPLAY_ACCEPTS_HOOK_POLICY` in isolated evidence. With the relevant production plugin-entry configuration and `hooks.allowConversationAccess=true`, the exact OpenClaw `2026.7.1-2` loader/API path invoked `register(api)` and multiple `api.on("before_agent_run")` calls, and the final typed-hook registry contained six `before_agent_run` entries. A false-policy control omitted `before_agent_run` while retaining other typed hooks. This proves the configuration shape can support host acceptance in an isolated loader/API lifecycle.

Production still reports `origin=global`, `hookCount=0`, `hookNames=[]`, while CNX-390's production-shaped isolated CLI replay reported `origin=config`, `hookCount=0`. CNX-392 isolates this concrete activation-path difference before any further production reasoning.

## Current authorization

CNX-392 is READY for Hermes execution.

First inspect exact installed OpenClaw `2026.7.1-2` source to determine whether plugin `origin` and/or `registrationMode` is causal to `hookPolicy`, `createApi`, or typed-hook registration. Then, only if technically justified and safe, run disposable isolated A/B activation paths using the same production plugin configuration and exact effective artifact:

A. config-origin path;
B. global-origin/discovered-extension equivalent.

Observe `entry?.hooks`, `hookPolicy`, `registrationMode`, `register(api)`, `api.on("before_agent_run")`, host policy decision, and final typed-hook inventory where exposed.

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

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative workaround.
- No new dependency architecture.
- No semantic probe or retry.
- No permanent instrumentation.
- No persistent installation of an isolated test copy into the production extension tree.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-391.
- Do not start CNX-393 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-393.
