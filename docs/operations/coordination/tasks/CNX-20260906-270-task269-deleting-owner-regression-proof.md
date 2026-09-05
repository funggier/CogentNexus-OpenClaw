# CNX-20260906-270 — Task269 Deleting-Owner Regression Proof

## Objective

Close the single missing Task269 safety-proof case without broadening production scope.

Parent: `CNX-20260906-269`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Required work

1. Add an explicit regression test where:
   - Ticket is accepted Direct-lane (`workflow_eligible=0`, `workflow_id IS NULL`);
   - Direct recovery is `pending`, exact generation, otherwise due;
   - owner session is fresh but state is `deleting`;
   - `durable_work_hint()` must return `False`.
2. Add/extend a supervisor-level assertion proving healthy Gateway/provider plus this `deleting` Direct shape stays on the `idle` fast path and never invokes the legacy heavy supervisor.
3. Production source change is **not expected**. Do not edit production code unless the new RED test demonstrates a real defect.
4. If production source must change, use RED -> minimal fix -> GREEN and explain why current `s.state='active'` behavior was insufficient.
5. Re-run:
   - the new focused actionability suite;
   - relevant Host/Direct recovery tests;
   - full Python suite appropriate to this branch;
   - `py_compile` for touched Host source if production changes;
   - `git diff --check`;
   - exact-SHA GitHub Actions required by branch policy.
6. Publish exact report and set coordination to `WAITING_FOR_CHATGPT_REVIEW`.

## Preserve accepted Task269 semantics

Do not weaken:
- active exact owner generation requirement;
- 15-minute Direct owner-session liveness fence;
- due `next_attempt_at` requirement;
- model-call active/recovering fence;
- workflow/delivery/context-maintenance actionability;
- one-minute supervisor cadence;
- hard-hang recovery.

## Hard fences

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

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence and must not be mutated.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-270-task269-deleting-owner-regression-proof.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop project mutation.
