# CNX-20260906-273 — ChatGPT Review

## Verdict

`REWORK_REQUIRED__CONCURRENT_MESSAGE_SENT_AND_GENERATION_PROOFS_MISSING`

## Accepted evidence

Task273 repaired the production-shaped single-run Discord Direct path on the accepted source candidate `04a566aa66e7812a52385fb70e0e4a5834f2f931`:

- `reply_dispatch` can recover `ctx.runId` when `event.runId` is absent;
- a trusted Discord session key/surface can arm the public `reply_payload_sending` fallback when the abort-aware dispatcher lacks `appendBeforeDeliver`;
- the exact final text is staged into `cnx_assistant_delivery` before native completion is trusted;
- the durable row carries the exact Ticket, owner session, current generation and idempotency identity;
- duplicate same-text observation is idempotent and changed text fails closed;
- the focused test, full plugin suite, build/package validation and exact-SHA GitHub Actions are green.

Exact-SHA CI independently confirmed:

- Validate `34013900111` — success;
- PS5.1 Acceptance Smoke `34013900092` — success;
- Windows Installer Pack Smoke `34013900123` — success.

The repair is therefore promising and should be preserved unless the missing safety proofs expose a real defect.

## Blocking review finding 1 — same-session outbound receipt ambiguity remains

Task273 explicitly required proof that same-session concurrent Direct turns cannot settle the wrong Ticket. That proof is absent from `v273-discord-direct-delivery.test.ts`.

The current generic `index.ts` `message_sent` fallback still does this when outbound `runId` is absent:

1. read `sessionKey`;
2. gather all `runSessions` entries for that session;
3. select `candidates.at(-1)?.[0]` — the newest mapped run;
4. settle that inferred run.

The exact installed OpenClaw contract states outbound `message_sending` / `message_sent` does not reliably plumb `runId`, and sessionKey-only correlation cannot disambiguate concurrent turns in one session. Therefore a late receipt from run A can be attributed to newer run B by the current generic fallback. Task273's new durable path is keyed by exact runId, but it did not prove or fence this still-registered legacy receipt path.

This is a contract blocker, not merely missing documentation.

## Blocking review finding 2 — lifecycle/generation race was asserted, not proven for the new Discord path

Task273 also required proof that stale/deleted/wrong-generation session authority cannot stage or confirm a final. The new focused test exercises only generation 0 active happy path.

Existing lifecycle source is encouraging: session delete/reset increments generation, cancels nonterminal Tickets, removes pending assistant deliveries, and later lifecycle reactivation advances generation. However Task273 must prove the new Discord public-hook fallback respects those transitions when callbacks/waiters arrive late.

At minimum the successor must cover:

- late `reply_payload_sending` for an old run after session delete/reset cannot create a durable row;
- a staged pending row removed by deletion cannot be re-completed by a late `waitForIdle` callback;
- a fresh lifecycle Ticket stages with the new generation only;
- wrong owner/session context cannot arm or consume another run's fallback.

## Additional evidence completion

Task273 required that a later timeout scan cannot clear/regenerate an already durable final. Existing durable-boundary tests may cover the persistence primitive, but the new Discord production-shaped test did not exercise this path. Add a direct Discord regression assertion so the requirement is explicit and local to this repair.

## TDD evidence note

The task required RED -> minimal production repair -> GREEN. The final candidate contains the new test and production change in one commit whose parent is the Task273 opening commit. A separate RED commit was not required by the task text, so this review does not reject solely on commit shape. The successor should nevertheless preserve observable RED evidence before any additional production change.

## Live authority

No live install-over, Gateway/provider mutation, session Delete/reset, Discord semantic send, Ticket/recovery disposition, manual SQLite mutation, Scheduled Task mutation, release promotion or force push is authorized by this review.

Task272 live authority remains parked and unconsumed until the repaired source candidate is independently accepted and separately deployed/requalified.
