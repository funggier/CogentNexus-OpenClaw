# CNX-20260905-265 — First-Turn Lifecycle Admission Ordering Repair

## Objective

Close the remaining Discord manual-session Delete/recreation race identified by ChatGPT review of Task264. A legitimate newly created OpenClaw lifecycle must be admitted on its **first owner turn** even when the fire-and-forget `session_start` hook has not run yet, while stale/different lifecycle IDs remain fail-closed.

## Parent evidence

- Parent Task: `CNX-20260905-264`
- Task264 candidate: `cad96fad3d1cef07fac4173425f15714b33240d6`
- Task264 report: `docs/operations/coordination/reports/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`
- ChatGPT review: `docs/operations/coordination/reviews/CNX-20260905-264-chatgpt-first-turn-lifecycle-ordering-review.md`
- Review verdict: `REWORK_REQUIRED__FIRST_TURN_SESSION_START_ORDERING_RACE`

## Root contract

OpenClaw `session_start` is an asynchronous void hook. Correctness must not rely on it completing before `before_agent_run`.

The exact owner admission boundary must reconcile + decide using `ctx.sessionKey + ctx.sessionId` atomically.

## Required semantics

At `before_agent_run` for non-subagent owner sessions:

1. no row + lifecycle B => establish active B deterministically and admit;
2. deleted A + A => reject, no mutation;
3. deleted A + genuinely new B => activate B exactly once, generation +1, admit;
4. active B + B => admit idempotently, no generation churn;
5. active B + stale A => reject, no mutation;
6. active B + unrelated C => reject, no mutation;
7. deleting row => reject;
8. active legacy `session_id IS NULL` => deterministic first-observed binding without generation increment, preserving Task264 migration contract;
9. delayed/duplicate `session_start(B)` after successful first-turn admission must be idempotent and must not change generation/session_id;
10. stale/different delayed `session_start(A/C)` must not hijack active B;
11. old-generation Ticket/recovery/outbox/assistant-delivery/workflow/synthetic fences remain unchanged.

## TDD requirement

Mandatory sequence:

`RED -> minimal production fix -> focused GREEN -> full GREEN -> exact-SHA CI`

### Required RED

Create a focused regression using the plugin's actually registered hooks:

- prepare A as deleted/tombstoned;
- register plugin;
- invoke `before_agent_run` for new B **without invoking session_start(B)**;
- Task264 baseline must fail because B is blocked/not reconciled;
- after minimal repair, B is admitted and row is exactly active/B with one generation advance;
- then invoke stale A and unrelated C through `before_agent_run`; both block and row remains unchanged;
- finally invoke delayed `session_start(B)` and prove idempotency.

Do not weaken the RED into direct helper-only assertions; it must reproduce the host ordering defect.

## Minimal repair guidance

Prefer one transactional lifecycle admission/reconciliation primitive reused by `before_agent_run` and `session_start`, or an equivalent design with identical atomic semantics. Avoid separate read-then-write races.

`session_start` may eagerly reconcile, but it is not an enforcement boundary and its return value must not be relied on by the design.

## Validation

At minimum:

- focused session ownership/lifecycle tests;
- full plugin tests;
- TypeScript build;
- plugin validation/package checks;
- `git diff --check`;
- exact candidate GitHub Actions required by branch policy.

## Hard fences

Task265 is repository/source/test/docs/CI only.

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

No live proof is authorized in this task.

## Completion

Hermes publishes:

`docs/operations/coordination/reports/CNX-20260905-265-first-turn-lifecycle-admission-ordering-repair.md`

Then update `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop project mutation. ChatGPT is the independent reviewer.
