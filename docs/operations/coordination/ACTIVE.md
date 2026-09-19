# Active Coordination Task

Status: `IN_PROGRESS`
State: `CNX427_SECOND_STAGE_DISCORD_TICKET_FIRST_REPAIR`
Execution mode: `TDD_AND_CONTROLLED_LIVE_REQUALIFICATION`
Task ID: `CNX-20260919-427`
Parent: `CNX-20260919-426`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Task: `docs/operations/coordination/tasks/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair.md`
Report: `docs/operations/coordination/reports/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair-report.md`

## Current state

Track B (Tailscale owner profile) remains GREEN.

Track A acceptance attempt #1 proved the early missing-run-id drop is repaired, but it also proved a second-stage Ticket-first bypass: OpenClaw created run `a0660423-e586-4e89-a5c9-fca25d842e1d`, executed the model, and delivered `CNX427_OK` without a CNX Ticket.

## Current objective

Add and qualify a narrow pre-inference second-stage admission adapter at the OpenClaw 2026.9.4 boundary where authoritative run identity exists. Do not synthesize run IDs, do not weaken Ticket-first, and do not move admission after inference.
