# CNX-20260905-258 — Task257 Explicit Pending-Redeliver Disposition

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: Musethree
Parent task: `CNX-20260905-257`
Parent review: `docs/operations/coordination/reviews/CNX-20260905-257-task256-pending-redeliver-recovery-reconciliation-review.md`
Parent umbrella: `CNX-20260831-188`

## Objective

Obtain and prove an explicit, authoritative disposition for the single pending
Direct `redeliver` row identified by Task257:

`CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`

This is a narrow disposition task. It must not perform recovery execution or
installer requalification. The task must first re-fetch GitHub authority,
re-read ACTIVE/STATUS, inspect the live SQLite schema, and preserve fresh
read-only evidence. It must establish current owner intent and genuine owner
session liveness, or use a separately authorized product cancellation path.

## Allowed outcomes

1. `READY_FOR_EXPLICIT_OWNER_DISPOSITION`: fresh evidence proves the owner
   explicitly wants redelivery and the session/generation is genuinely live;
   publish a report and stop. This outcome authorizes no resend by itself.
2. `RECONCILED_CANCEL_AUTHORITY_REQUIRED`: evidence proves the dated request is
   no longer desired, but cancellation still requires a separately authorized
   product operation; publish the finding and stop without cancelling.
3. `BLOCKED_OWNER_INTENT_UNPROVABLE`: intent or liveness cannot be proved;
   preserve the row and stop. Do not guess from gateway health or stale session
   flags.

## Hard fences

```text
DB writes/vacuum/recovery mutation = 0
clear/cancel/reset/claim = 0
replay/resend/semantic send = 0
installer Scheduled Task registration/start = 0
scripts/install.ps1 starts = 0
Gateway restart/lifecycle mutation = 0
release/tag mutation = 0
force push/history rewrite = 0
```

No disposition is to be executed in this task. Any cancellation or one-shot
redelivery requires a later, separately authorized task after this task's
independent review. Installer requalification remains parked throughout.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-258-task257-explicit-pending-redeliver-disposition.md`

Include fresh authority, exact subject-row and session binding, evidence of
explicit owner intent or its absence, exact `dueDirectRecovery()` predicate
posture, delivery/outbox posture, zero-mutation ledger, and the selected
outcome token. Then STOP for independent review.
