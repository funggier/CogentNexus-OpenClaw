# CNX-20260906-274 — Discord Direct Concurrent Receipt and Lifecycle Fence Completion

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-273`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Close the safety-contract gaps found in ChatGPT review of Task273 before any live deployment. Preserve Task273's accepted single-run Discord durable staging unless RED evidence proves production changes are necessary.

## Required TDD work

Use RED -> minimal repair -> GREEN.

### A. Same-session concurrent `message_sent` ambiguity

Create a production-shaped regression with two Direct Ticket runs A and B sharing the same canonical Discord session.

The exact installed OpenClaw outbound contract may emit `message_sent` without `runId`. Prove that a late success/failure receipt belonging to A cannot be inferred as B merely because B is the latest `runSessions` entry.

The current generic fallback `candidates.at(-1)` is not acceptable as per-turn authority when more than one candidate can exist for the same session.

Required assertions:

- no receipt without exact per-turn identity may complete/fail/promote the wrong Ticket;
- the Task273 exact run-scoped durable path still settles each run independently;
- cleanup cannot leave stale run/session mappings that make a later turn ambiguous;
- single-turn compatibility is preserved only where correlation is genuinely unambiguous and safe.

Prefer removing/session-fencing non-authoritative Discord `message_sent` settlement rather than inventing guessed correlation. Do not weaken fail-closed semantics.

### B. Delete/reset/generation races for the new Discord path

Prove through registered hooks or the closest production-shaped harness that:

1. stage a Discord Direct final for generation N, then delete/reset the session before the native waiter settles;
2. session revocation cancels/removes the pending delivery;
3. releasing the stale waiter cannot complete the cancelled old Ticket;
4. a late payload callback for the old run cannot recreate a durable row;
5. after genuine lifecycle recreation, a fresh Ticket stages with generation N+1 (or the exact generation produced by the lifecycle contract) and cannot be confused with the prior run;
6. wrong canonical session key / wrong owner context cannot arm or consume another run's public-hook fallback.

### C. Durable timeout boundary local proof

For a staged Discord Direct final, run the delivery-timeout/recovery scan after the normal deadline while native delivery is still pending. Prove:

- the exact durable row remains intact;
- `response_ready_at` is not cleared/refreshed to trigger inference regeneration;
- no competing direct recovery inference is created;
- later exact settlement completes once.

### D. Preserve Task273 behavior

Keep green:

- ctx.runId + Discord public-hook fallback when `event.runId` absent;
- exact Ticket/session/generation/idempotency binding;
- duplicate same-text idempotency;
- changed-text fail closed;
- Discord `NO_REPLY` semantics;
- Dashboard Direct semantics;
- session lifecycle/recreation suites;
- direct recovery/durable delivery suites.

## Validation

Run focused RED/GREEN tests, relevant neighboring suites, full plugin suite, build/package validation, `git diff --check`, and exact-candidate GitHub Actions. Production changes require exact-SHA CI green before report publication.

If all new tests are already GREEN without production changes, report that explicitly with proof. If the concurrency test is RED, repair the smallest authority boundary; do not broaden scope.

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

Task272's parked live Delete/test authority remains unconsumed.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-274-discord-direct-concurrent-receipt-lifecycle-fence-completion.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
