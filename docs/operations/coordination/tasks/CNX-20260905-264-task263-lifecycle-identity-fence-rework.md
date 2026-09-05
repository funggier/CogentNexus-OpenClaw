# CNX-20260905-264 — Task263 Lifecycle Identity Fence Rework

**Status:** `READY_FOR_HERMES`
**Parent:** `CNX-20260905-263`
**Executor:** `Hermes`
**Reviewer after report:** `ChatGPT`

## Objective

Close the Task263 review defect where the recreated owner row is active for lifecycle `B`, but a stale/different lifecycle `A`/`C` can still receive `state="active"` from the lifecycle helper and is not explicitly fenced by the `session_start` / owner run boundary.

Use Task263 candidate `4a5907af212c0b8c6f913036c6853523d7bab872` as the source baseline plus current coordination-only commits. Preserve the valid Task263 delete/recreation work and make the smallest production repair that provides an exact lifecycle-identity fence.

## Authority

Repository/source/test/docs/CI repair is authorized.

TDD is mandatory for production changes:

`RED -> minimal production repair -> GREEN`

No live runtime/semantic/destructive action is authorized in Task264.

## Required semantics

1. A deleted owner lifecycle `A` cannot reactivate itself.
2. A genuinely new lifecycle `B` on the same canonical `sessionKey` reactivates the owner exactly once and increments generation exactly once.
3. Repeated `B` start is idempotently accepted without generation churn.
4. While `B` is current and active, stale/different lifecycle `A` or `C` is explicitly rejected and cannot change `state`, `generation`, or `session_id`.
5. Do not use `state === active` alone as proof that the incoming lifecycle is current. Return or expose an explicit lifecycle match/accepted predicate.
6. `before_agent_run` must use `ctx.sessionId` + `ctx.sessionKey` to fail closed for an owner run whose lifecycle identity does not match the current active `cnx_sessions.session_id`. OpenClaw current hook context is known to carry both fields.
7. A legitimate current lifecycle owner run keeps the existing admission semantics.
8. Pre-existing/migrated active rows with `session_id IS NULL` must have deterministic safe behavior and regression coverage. Prefer one-time binding to the observed current lifecycle without generation increment if evidence supports that as the compatibility path.
9. Delete still cancels/suppresses old nonterminal Tickets, pending outbox/assistant delivery, direct recovery, workflow completion, and synthetic work. Do not rebind old work into the new generation.
10. Reset, same-key `new`, session succession, direct recovery generation fences, and delivery fences must not regress.

## Required RED coverage

At minimum add focused regression tests proving:

- deleted A + A -> rejected;
- deleted A + B -> accepted fresh generation;
- active B + B -> accepted idempotently;
- active B + stale A -> rejected;
- active B + unrelated C -> rejected;
- rejected lifecycle does not mutate generation/session_id;
- stale `before_agent_run` context for A is blocked while B is current;
- current B `before_agent_run` remains pass/eligible under existing policy;
- legacy active NULL session_id behavior is deterministic.

The RED must fail for the intended missing product behavior before production repair.

## Validation

After minimal fix:

- focused lifecycle/session ownership suite;
- any admission/hook suite affected by `before_agent_run`;
- full plugin test suite;
- TypeScript build;
- plugin validation/package checks;
- `git diff --check`;
- exact candidate GitHub Actions required by branch workflows.

If CI is queued/in-progress, Hermes retains Task264 and uses the persistent five-minute delayed recheck policy.

## Hard fences

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`

Report exact RED evidence, production diff, migration behavior, focused/full GREEN, exact candidate SHA, exact-SHA CI, effect ledger, residual uncertainty, and verification packet.

When complete, set coordination state to `WAITING_FOR_CHATGPT_REVIEW`; do not self-accept and do not hand off to another Hermes peer.
