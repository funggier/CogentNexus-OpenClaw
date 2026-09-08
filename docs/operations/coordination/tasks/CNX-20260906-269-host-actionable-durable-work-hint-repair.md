# CNX-20260906-269 — Host Actionable Durable-Work Hint Repair

## Objective

Repair the Host supervisor's durable-work wake predicate so healthy steady state remains quiescent when stored durable rows are not actually actionable under the current recovery/delivery contracts.

Parent: `CNX-20260905-268`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Root cause to preserve

Task268 proved the user's APPSTARTING/busy cursor aligns with 6/6 natural `PT1M` supervisor waves. Source review narrowed the wake condition further:

- `host_v091.py::supervisor_tick()` has a lightweight fast path;
- that fast path is bypassed whenever `durable_work_hint(root)` returns true;
- `durable_work_hint()` currently treats any nonterminal Ticket and broad Direct-recovery rows as actionable;
- the event-driven Direct recovery implementation is stricter: pending Direct recovery is due only with accepted Direct-lane shape, active exact owner generation, session freshness within 15 minutes, due time reached, and model-call fence satisfied.

The old target Ticket/recovery must remain untouched. Its stale/non-due state should be sufficient to reproduce the false wake.

## Required TDD

RED must be committed before production repair.

At minimum prove:

1. stale Direct owner session (> `DIRECT_RECOVERY_SESSION_LIVENESS_MS`) + accepted Direct-lane Ticket + pending recovery that is otherwise due does **not** make Host durable work actionable;
2. the same shape with fresh active owner session + exact generation + due recovery **does** wake Host;
3. owner-generation mismatch does not wake;
4. future `next_attempt_at` does not wake;
5. deleted/deleting owner does not wake;
6. an accepted Direct-lane Ticket by itself does not force heavy reconciliation merely because its status is nonterminal;
7. genuinely actionable durable workflow/Ticket state still wakes the heavy path;
8. pending transport/delivery state that the Host contract genuinely owns remains actionable according to its existing due/ownership rules;
9. healthy Gateway/provider + only stale/non-actionable Direct state returns the quiescent `idle` fast path and does not invoke the legacy heavy supervisor;
10. unhealthy Gateway/provider and other proven recovery paths remain unchanged.

Do not copy SQL mechanically if ownership belongs to a shared helper. Prefer one explicit, testable actionability contract and avoid semantic drift between Host and plugin recovery eligibility.

## Design constraints

- Preserve the one-minute supervisor cadence unless evidence shows a separate defect.
- Preserve fast hard-hang detection and recovery responsiveness.
- Do not solve the issue by deleting/terminalizing the old Ticket.
- Do not broaden Direct recovery eligibility.
- Do not weaken owner-generation or session-freshness fences.
- Avoid unrelated refactor.

## Validation

Required:

- focused RED evidence;
- minimal production fix;
- focused GREEN;
- relevant Host/Direct-recovery tests;
- full Python test suite appropriate to touched Host surfaces;
- plugin tests if a shared cross-language contract/helper is changed;
- `git diff --check`;
- exact-SHA GitHub Actions required by current branch policy.

## Hard fences

Task269 is source/test/docs/CI only.

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete/run   = 0
stop/kill/restart unrelated live processes        = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

The old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence. Do not cancel, redeliver, dispose, replay, or reinterpret its owner intent.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-269-host-actionable-durable-work-hint-repair.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
