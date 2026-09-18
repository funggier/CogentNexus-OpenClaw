# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX418_PRESERVED_SESSION_OLLAMA_SEMANTIC_VERTICAL_SLICE`
Execution mode: `ONE_SEMANTIC_PRESERVED_DASHBOARD_TICKET_FIRST_OLLAMA_ACCEPTANCE`
Task ID: `CNX-20260918-418`
Parent: `CNX-20260918-417`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Installed source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`
Preserved target session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`
Preserved target session ID: `18fab7b9-2fb1-409f-9aed-d79168aaffdc`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-417-chatgpt-review.md`
Parent report: `docs/operations/coordination/reports/CNX-20260918-417-first-post-attestation-ollama-dashboard-semantic-vertical-slice-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-418-preserved-session-ollama-semantic-vertical-slice.md`
Product goal: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
Development plan: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`

## Current position

CNX-417 is accepted as correctly blocked at `BLOCKED_FRESH_DASHBOARD_TARGET`.

CNX-417 created exactly one fresh, semantically empty Dashboard session, but that target inherited the previous parent session's OpenAI/Luna execution selection. No nonce or semantic message was sent.

After CNX-417 closeout, the Operator explicitly changed the model selection to `qwen3.8:27b`.

CNX-418 must re-prove that the exact preserved fresh session now resolves to `ollama/qwen3.8:27b`, while remaining semantically empty and having produced no Ticket/model/delivery effect from the selection change itself.

## Current authorization

CNX-418 is READY for Hermes execution.

Do not create another session.

If the exact preserved session is still empty and now resolves to `ollama/qwen3.8:27b`, exactly one semantic Dashboard/WebChat message is authorized.

If the target/session/selection state is not exact, stop without sending.

## Hard fences

- New Session/New Chat actions: 0.
- Dashboard semantic sends: max 1.
- Semantic retry/resend: 0.
- Direct Ollama/model probes: 0.
- OpenAI semantic requests: 0.
- Provider/model selection changes by executor: 0.
- Provider/model/auth config mutation: 0.
- Installer/install-over: 0.
- Plugin lifecycle mutation: 0.
- Gateway restart/reload/repair: 0.
- Lifecycle start/stop/restart: 0.
- Manual Ticket/outbox/recovery/SQLite mutation: 0.
- Manual durable replay/delivery: 0.
- Session reset/delete/compact: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-419 yourself.

## Closeout

Publish the CNX-418 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD and clean publication worktree, preserve the exact session if PASS, and stop.
