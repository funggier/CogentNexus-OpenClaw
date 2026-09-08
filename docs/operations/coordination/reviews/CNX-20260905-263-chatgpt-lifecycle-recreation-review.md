# CNX-20260905-263 — ChatGPT Independent Review

**Verdict:** `REWORK_REQUIRED__LIFECYCLE_IDENTITY_FENCE_INCOMPLETE`

**Reviewed candidate:** `4a5907af212c0b8c6f913036c6853523d7bab872`
**Reviewed report:** `docs/operations/coordination/reports/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`
**Review authority:** ChatGPT under `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted evidence

The review accepts the following as valid evidence:

- Task263 followed a real RED -> production repair sequence.
- Candidate adds migration-safe `cnx_sessions.session_id` storage.
- Delete records the deleted OpenClaw lifecycle identity when `sessionId` is available.
- A deleted row with old lifecycle `A` can be reactivated by a different lifecycle `B` with one generation increment.
- Repeated `B` activation is idempotent.
- Old Ticket cancellation/suppression behavior is retained by the delete path.
- Local focused/full tests, build, plugin validation, and exact-candidate GitHub Actions were reported green; exact candidate workflows were independently observed terminal success 3/3.
- Task263 respected the no-live/no-semantic hard fences.

## Blocking review finding

The candidate does not fully implement the required lifecycle-identity fence after a new lifecycle is active.

`reactivateSessionForLifecycle()` currently returns the row's current authority whenever `row.state !== "deleted"`, regardless of whether the incoming `sessionId` matches the stored active lifecycle identity.

Consequently, after deleted lifecycle `A` is replaced by active lifecycle `B`, a later stale call for lifecycle `A` returns `state="active"` without any explicit rejection signal.

The `session_start` hook interprets only `authority.state !== "active"` as refusal. Therefore a stale/different lifecycle arriving while `B` is active is not distinguishable from the legitimate active lifecycle at that hook boundary.

This is not merely a test wording issue: the Task263 contract required lifecycle-identity-aware stale rejection, and OpenClaw's `before_agent_run` hook context carries both `sessionKey` and `sessionId`, so a run-level identity fence is technically available.

## Regression-test gap

The Task263 regression test explicitly performs:

```text
A deleted
B reactivates
B repeated -> active
A called again -> expected state active
```

That final assertion does not prove `A` is rejected. It only proves that the owner row remains active after `B` became current.

The test therefore does not establish the report claim that stale lifecycle `A` cannot be accepted after recreation.

## Required rework

A bounded source/test repair must establish an explicit current-lifecycle predicate, not infer lifecycle acceptance from owner state alone.

Required semantics:

1. deleted `A` + start `A` -> rejected; no generation change;
2. deleted `A` + start `B` -> accepted, active, generation increments exactly once, current lifecycle becomes `B`;
3. active `B` + repeated start `B` -> accepted idempotently; no generation change;
4. active `B` + stale/different start `A`/`C` -> rejected; no state/session_id/generation mutation;
5. `before_agent_run` for owner session must fail closed when `ctx.sessionId` does not match the current lifecycle identity for that `sessionKey`;
6. legitimate current `B` owner run remains admitted under the existing owner/admission policy;
7. migration-safe handling for pre-existing active rows with `session_id IS NULL` must be explicit and tested; binding the observed current lifecycle without unnecessary generation churn is preferred when it can be proven safe;
8. old-generation Ticket/recovery/outbox/assistant-delivery/workflow/synthetic suppression remains unchanged and no rebind occurs;
9. reset/new/session succession regression suites stay green.

## Disposition

Task263 is **not accepted** as final source repair. Its useful work remains the base for a narrow Task264 rework.

No live session deletion, Discord semantic send, installer/Gateway action, or manual live DB mutation is authorized by this review.
