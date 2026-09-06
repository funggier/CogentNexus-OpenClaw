# CNX-20260906-275 — Discord Direct Owner-Context and Stale-Settlement Proof Completion

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-274`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Close the remaining production-shaped safety proofs from Task274 before any live deployment/requalification. Preserve the accepted Task273/274 repairs unless RED evidence proves a minimal additional source guard is necessary.

## Required TDD work

Use RED -> minimal repair -> GREEN. Record the failing assertion/output before changing production source if any new test is RED.

### A. Consume-time owner/context fence for Discord public-hook fallback

Create a registered-hook production-shaped test that:

1. creates Direct Ticket/run R owned by canonical Discord session A;
2. arms the Task273 public-hook fallback for R through `reply_dispatch` using session A and trusted Discord ingress;
3. invokes `reply_payload_sending` for the same run R but with a different canonical Discord session B, wrong owner context, or conflicting ingress surface;
4. proves the wrong callback cannot stage/mark/settle A's final, cannot start a waiter, and cannot mutate A's Ticket/delivery state;
5. then invokes the correct session A callback and proves normal exact durable staging still works.

The consumer must not rely solely on possession of `runId` if the stored fallback owner and current callback owner/surface disagree.

If RED exposes the current permissive behavior, add the smallest explicit consume-time `sessionKey` + trusted ingress match guard. Do not invent new persistence or duplicate the verified-delivery scheme.

Also prove a wrong session cannot arm a fallback for a Ticket it does not own.

### B. Stale native waiter after Delete/reset

Use the registered Task273 public-hook path, not only `stageDashboardDirectResult()` directly:

1. create and route a Discord Direct Ticket at generation N;
2. arm fallback and stage the exact final through `reply_payload_sending`;
3. hold `dispatcher.waitForIdle()` unresolved;
4. invoke the real session delete/reset lifecycle primitive while the delivery is pending;
5. verify the Ticket is cancelled/suppressed and the pending assistant-delivery row is removed/suppressed according to the lifecycle contract;
6. release the stale waiter;
7. prove the stale waiter cannot complete the cancelled Ticket, cannot recreate a delivery row, cannot emit a second terminal transition, and cannot affect a recreated generation;
8. recreate the lifecycle with a new sessionId, create a fresh Direct Ticket, and prove the new final stages/settles under the new generation only.

### C. Timeout -> later exact settlement exactly once

Extend the Discord-local timeout proof:

1. stage a durable Direct final with a deterministic old timestamp;
2. run the timeout/recovery scan after the deadline and prove no competing inference/recovery is created and the durable row remains pending/authoritative;
3. execute the exact native settlement for that run;
4. prove Ticket becomes `completed`, delivery becomes `delivered`, `delivery_confirmed_at` is set, and terminal/delivery-confirmed events occur once;
5. invoke settlement again and prove it is idempotent/no-op rather than duplicating completion.

### D. Preserve accepted behavior

Keep GREEN:

- Task273 ctx.runId Discord pre-transport staging;
- Task274 no-runId Discord `message_sent` fail-closed behavior;
- exact run/session/generation/idempotency binding;
- duplicate same-text idempotency and changed-text fail closed;
- Discord NO_REPLY/silent-sentinel semantics;
- Dashboard Direct behavior;
- session lifecycle/recreation suites;
- direct recovery and durable-delivery suites;
- non-Discord compatibility where legacy message_sent correlation remains valid.

## Validation

Run focused RED/GREEN tests, neighboring delivery/lifecycle suites, full plugin suite, build/package validation, `git diff --check`, and exact-candidate GitHub Actions if production source changes. If Task275 is test-only because every new negative proof is already GREEN, report that explicitly and still run the focused/full validation appropriate to the touched test surface.

## Hard fences

```text
live Discord/Dashboard semantic sends             = 0
live OpenClaw session Delete/reset                 = 0
manual live Ticket/session/SQLite mutation         = 0
recovery replay/redelivery/disposition              = 0
installer/install-over/uninstall/reset             = 0
Gateway/provider/service lifecycle mutation        = 0
Scheduled Task mutation                            = 0
release/tag/default-branch promotion               = 0
force push/history rewrite                         = 0
```

Task272's parked live Delete/test-message authority remains unconsumed.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-275-discord-direct-owner-context-and-stale-settlement-proof.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
