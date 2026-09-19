# Active Coordination Task

Status: `IN_PROGRESS`
State: `CNX427_EXTERNAL_INGRESS_AND_TAILSCALE_PROFILE_REPAIR`
Execution mode: `TDD_AND_BOUNDED_LIVE_REPAIR`
Task ID: `CNX-20260919-427`
Parent: `CNX-20260919-426`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Task: `docs/operations/coordination/tasks/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair.md`
Report: `docs/operations/coordination/reports/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair-report.md`

## Current objective

Repair two OpenClaw 2026.9.4 compatibility defects proven live:

1. Discord external ingress reaches `reply_dispatch` before an authoritative run ID exists, and CNX currently fails closed too early with `missing-run-id`.
2. Tailscale remote Control UI reaches the Gateway but remains in pending authenticated-profile verification, causing session RPCs to fail closed with `AUTHENTICATED_PROFILE_UNAVAILABLE`.

Track A must defer early missing-run-id admission to `before_agent_run` without synthesizing identity or weakening Ticket-first semantics.

Track B must make remote owner-profile resolution converge without bypassing authentication/profile verification.

See the task document for exact evidence, constraints, TDD requirements, and acceptance criteria.
