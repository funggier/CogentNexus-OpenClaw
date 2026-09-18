# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX406_REAL_PROVIDER_RUNTIME_BASELINE_OLLAMA_WEB_CHAT_TRACE`
Execution mode: `READ_ONLY_PROVIDER_RUNTIME_ARCHAEOLOGY`
Task ID: `CNX-20260918-406`
Parent: `CNX-20260918-405`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260918-405-production-repeated-registration-caller-lifecycle-correlation-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-406-real-provider-runtime-baseline-ollama-web-chat-end-to-end-trace.md`
Product goal: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
Development plan: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`

## Current position

CNX-405 is accepted as `PRODUCTION_REGISTRY_LIFECYCLE_PATH_MAPPED`. The registry-lifecycle investigation is sufficient for its stated read-only boundary and should not continue as the primary workstream.

The Operator has explicitly authorized continued work toward the real provider/model runtime goal. That authorization supersedes the prior CNX-405 closeout fence that prohibited self-starting CNX-406.

The next practical boundary is to map the known-good Ollama Web Chat vertical slice before changing provider architecture.

## Current authorization

CNX-406 is READY for Hermes execution.

Trace the existing Ollama path end-to-end from Web Chat provider/model state through session lookup, provider/model resolution, agent execution, Ollama invocation, streaming/result handling, persistence, and the next turn.

The purpose is to identify the smallest real ownership boundary for runtime provider/model switching while preserving working OpenClaw behavior.

## Hard fences

- Read-only provider/runtime archaeology only.
- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No provider credential changes.
- No provider/model selection mutation in production.
- No semantic/model/provider/Dashboard request during CNX-406.
- No OpenAI live request.
- No new Ollama semantic request solely for CNX-406.
- No TicketStore/admission/routing/auth mutation.
- No production extension/artifact deploy.
- No OpenClaw dependency patch.
- No CogentNexus production repair.
- No release/tag/main.
- No force-push/history rewrite.
- Do not create or start CNX-407 yourself.

## Closeout

Publish the CNX-406 report with exact source/runtime ownership evidence, target gap matrix, and smallest recommended RED test.

Set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify branch HEAD and clean worktree, then stop. Do not create/start CNX-407.
