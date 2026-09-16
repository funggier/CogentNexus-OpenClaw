# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX377_COMPOSED_HOOK_REGISTRY_WIRING_REPAIR`
Execution mode: `ROOT_CAUSE_TDD_COMPOSED_REGISTRY_REPAIR`
Task ID: `CNX-20260917-377`
Parent: `CNX-20260917-376`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-377-composed-registry-wiring-repair.md`

## Current position

CNX-377 completed read-only/source tracing and focused validation. Classification: `INCONCLUSIVE`.

The current OpenClaw 2026.7.1-2 loader activates the same registry passed to `initializeGlobalHookRunner`, and its composed facade dynamically composes that registry with live plugin registries. The installed CogentNexus artifact also contains the authorized conversation-hook declaration. The CNX-376 live `hookCount: 0` observation could not be reproduced or causally bound to a repository-side defect without speculative host/runtime mutation.

Report: `docs/operations/coordination/reports/CNX-20260917-377-composed-registry-wiring-repair-report.md`

## Verification

- CNX-374 focused regression: passed (1 test).
- `npm ci --ignore-scripts`: passed.
- Effective installed artifact SHA-256 was freshly computed and recorded in the report.
- Semantic requests: 0.
- Runtime activation/restart: not performed; no validated repair existed.

## Hard fences

No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes, no broad or speculative patch, no force-push, no main/release/tag mutation, no historical CNX-360..376 edits, and no CNX-378 work.

## Handoff

Waiting for ChatGPT review. Stop here.
