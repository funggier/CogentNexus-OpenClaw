# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX409_RUNTIME_ATTESTATION_LOCAL_BUILD_TEST_QUALIFICATION`
Execution mode: `LOCAL_SOURCE_BUILD_TEST_ONLY`
Task ID: `CNX-20260918-409`
Parent: `CNX-20260918-408`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260918-408-live-hook-runner-runtime-attestation-surface-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-409-runtime-attestation-local-build-test-qualification.md`
Product goal: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
Development plan: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`

## Current position

CNX-406 is accepted as `OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`.

CNX-407 architecture review retained `before_agent_run` as the canonical provider-independent Ticket-first gate.

CNX-408 implemented a read-only operator-scoped Gateway RPC, `cogentnexus.runtimeAttestation`, using public OpenClaw plugin-runtime hook surfaces. Repository CI did not run automatically, so local build/test qualification is required before any deployment.

## Current authorization

CNX-409 is READY for Hermes execution.

Run local source/build/test/package validation only. Minimal repository repair is authorized if validation exposes a source defect, using RED -> minimal fix -> GREEN.

## Hard fences

- No production install/install-over.
- No production artifact replacement.
- No Gateway restart/reload.
- No production config/environment/Scheduled Task mutation.
- No live Gateway RPC call.
- No semantic/model/provider request.
- No provider/model/auth/routing change.
- No TicketStore/durable-state mutation.
- No OpenClaw dependency version change/patch.
- No release/tag/main.
- No force-push/history rewrite.
- Do not create/start CNX-410 yourself.

## Closeout

Publish the CNX-409 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact remote/local HEAD and clean worktree, then stop. Do not deploy.
