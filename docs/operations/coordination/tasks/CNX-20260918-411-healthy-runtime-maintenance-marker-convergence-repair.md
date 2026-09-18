# CNX-20260918-411 — Healthy-Runtime Maintenance Marker Convergence Repair

Status: `IN_PROGRESS_CHATGPT`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-410`
- Executor: `ChatGPT`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-410-chatgpt-review.md`

## Objective

Repair the v0.9.5 Supervisor convergence defect in which an active `healthy-runtime` maintenance marker can survive after Gateway health returns because the provider-neutral idle fast path returns before supported maintenance retirement runs.

The repair must preserve provider-neutral ownership and the single-wake idle architecture.

## Root cause

Current `host_v091.py::supervisor_tick`:

- verifies Gateway health;
- classifies durable wake authority;
- returns lightweight `idle` when no work is actionable.

It does not check for an active recoverable maintenance marker before that idle return.

The hard-hang path creates a marker with:

`recoveryPolicy=healthy-runtime`

through `lifecycle restart`.

If Gateway recovery completes between Supervisor invocations, a later healthy/no-work tick can remain forever on the idle path and never retire the marker.

## Required behavior

### Read-only tick

If:

- Gateway is healthy;
- active maintenance marker exists;
- `recoveryPolicy=healthy-runtime`;
- `execute_safe=false`;

then:

- do not mutate the marker;
- do not enter legacy/provider-heavy reconciliation;
- report a bounded recovery-pending result.

### Execute-safe tick

If:

- Gateway is healthy;
- active maintenance marker exists;
- `recoveryPolicy=healthy-runtime`;
- `execute_safe=true`;

then:

1. invoke the existing supported provider-neutral lifecycle verification:
   `lifecycle start`
   without `--provider`;
2. require successful lifecycle result;
3. require the marker to be retired by that supported path;
4. continue normal wake classification;
5. if no durable work is actionable, return idle with evidence that maintenance was reconciled.

### Failure

If lifecycle verification fails or the marker remains active afterward:

- do not claim healthy convergence;
- return a bounded `maintenance-recovery-incomplete` classification/result;
- do not manually unlink/edit the marker;
- do not invoke provider routing/lifecycle.

## TDD

1. Add RED tests covering:
   - healthy/no-work/execute-safe + healthy-runtime marker -> supported lifecycle start invoked exactly once and marker reconciled;
   - healthy/no-work/read-only + healthy-runtime marker -> no mutation and no legacy heavy path;
   - ordinary healthy/no-marker/no-work -> remains lightweight idle and does not invoke lifecycle start.
2. Implement smallest repair in `host_v091.py`.
3. Preserve existing idle/single-wake/provider-neutral tests.

## Scope

Expected files:

- `skills/cogentnexus-openclaw/scripts/host_v091.py`
- `tests/test_v091_idle_recovery_hint.py`
- coordination report/docs only.

## Hard fences

- Repository/source/test only.
- No production install/deploy.
- No Gateway restart.
- No live lifecycle command.
- No Ticket/outbox/recovery/SQLite mutation on the operator machine.
- No provider/model/auth/routing changes.
- No semantic/model request.
- No OpenClaw dependency patch.
- No release/tag/main.
- No force push/history rewrite.
- Do not start CNX-412 before local validation is delegated.

## Exit

Use:

- `HEALTHY_RUNTIME_MARKER_CONVERGENCE_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`
- `REPAIR_BLOCKED_BY_CONTRACT_CONFLICT`
