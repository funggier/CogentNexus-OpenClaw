# CNX-20260918-407 — Pre-Inference Admission Hook Strategy Review

Status: `IN_PROGRESS_CHATGPT`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-406`
- Executor: `ChatGPT`
- Reviewer: `ChatGPT architectural review with Operator final authority`
- Human final authority: `Operator`
- Product goal: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
- Development plan: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-406-chatgpt-review.md`

## Objective

Select the correct OpenClaw 2026.7.1-2 pre-inference boundary for CogentNexus Ticket-first admission without creating a competing provider router and without repeating CNX-380 through CNX-405 registry/cache forensics.

The review must determine whether CogentNexus should:

1. retain `before_agent_run` as the canonical enforcement gate;
2. move admission to another existing typed hook;
3. split early observation and final enforcement across two hooks; or
4. retain the current gate but add explicit runtime attestation/diagnostics before the next live qualification.

## Required comparison

Compare at least:

- `before_model_resolve`
- `before_prompt_build`
- `before_agent_reply`
- `before_agent_run`
- `inbound_claim`
- `model_call_started` as an observation/fence candidate, not assumed to be pre-call

For each boundary evaluate:

- exact dispatch location;
- ordering relative to session/history load;
- ordering relative to provider/model resolution;
- ordering relative to provider invocation;
- Web Chat applicability;
- direct/embedded/CLI applicability where relevant;
- access to session/run/owner identity;
- access to prompt/history;
- whether it can synchronously block inference;
- failure policy;
- provider independence;
- duplication/idempotency risk;
- migration cost.

## Evidence requirements

Use exact-version OpenClaw source corresponding to the installed 2026.7.1 family plus exact installed-module evidence already recorded in CNX-380 through CNX-405. Current upstream documentation may be supporting context only, not exact-runtime authority.

Also inspect the current CogentNexus admission handler and prove whether any pre-trace early-return can explain prior no-Ticket runs.

## Non-goals

- No provider router.
- No provider/model/auth changes.
- No production mutation.
- No Gateway restart/reload.
- No semantic request.
- No OpenClaw dependency patch.
- No CogentNexus production repair in this task.
- No TicketStore redesign.
- No release/tag/main.
- Do not create/start CNX-408 before the architectural disposition is recorded.

## Exit classification

Use one:

- `BEFORE_AGENT_RUN_RETAINED_WITH_RUNTIME_ATTESTATION_NEXT`
- `ADMISSION_BOUNDARY_MIGRATION_JUSTIFIED`
- `SPLIT_BOUNDARY_JUSTIFIED`
- `ARCHITECTURE_EVIDENCE_INSUFFICIENT`

## Closeout

Publish the architectural review report and update ACTIVE/STATUS to the resulting review-ready or successor-ready state. Do not perform live runtime mutation.
