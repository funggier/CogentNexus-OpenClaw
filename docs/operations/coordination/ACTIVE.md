# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX415_TICKET_DB_NATIVE_STDERR_LOCAL_VALIDATION`
Execution mode: `LOCAL_INSTALLER_SOURCE_TEST_VALIDATION_ONLY`
Task ID: `CNX-20260918-415`
Parent: `CNX-20260918-414`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Exact product/source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-413-chatgpt-review.md`
Parent report: `docs/operations/coordination/reports/CNX-20260918-414-ticket-db-bootstrap-native-stderr-installer-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-415-ticket-db-native-stderr-repair-local-validation.md`

## Current position

CNX-413 is accepted as correctly failed at the installer terminal boundary.

The one-time stale maintenance bootstrap converged successfully. The installer then failed only because the ticket DB bootstrap used a bare Node invocation under Windows PowerShell 5.1 `ErrorActionPreference=Stop`, allowing benign Node SQLite stderr to become a terminating `NativeCommandError`.

CNX-414 reuses the existing proven `Invoke-NativeInstallerDiagnostic` helper for this stage and preserves native exit-code fail-closed behavior.

## Current authorization

CNX-415 is READY for Hermes execution.

Run local source/test/PowerShell 5.1 validation only. A bounded source/test repair is allowed if CNX-414 validation exposes a directly related defect.

## Production state

Production remains in the safe partial state left by CNX-413:

- controller passthrough/disabled generation 106;
- plugin disabled;
- Gateway healthy;
- Recovery/Delivery READY;
- pending outbox 0;
- SQLite integrity OK.

Do not manually enable, restart, deploy, or retry the installer during CNX-415.

## Hard fences

- Production installer invocation: 0.
- Production install/install-over: 0.
- Gateway restart/reload: 0.
- Production lifecycle command: 0.
- Plugin enable/disable mutation: 0.
- Production config/state mutation: 0.
- Ticket/outbox/recovery/SQLite production mutation: 0.
- Semantic/model/provider requests: 0.
- Provider/model/auth/routing mutation: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-416 yourself.

## Closeout

Publish the CNX-415 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact local/remote HEAD equality and clean worktree, then stop.

Do not retry production installation.
