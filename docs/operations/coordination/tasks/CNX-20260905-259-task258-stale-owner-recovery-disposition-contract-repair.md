# CNX-20260905-259 — Task258 Stale-Owner Recovery Disposition Contract Repair

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated repository operator
Coordinator / independent reviewer: Musethree
Parent task: `CNX-20260905-258`
Parent umbrella: `CNX-20260831-188`

## New authority and boundary

The user explicitly requested inspection and repair of the coordination dead-end
where Task258 was accepted `STOPPED` with no successor. That instruction
authorizes repository/source/test diagnosis and repair needed to restore a safe
coordination path.

It does **not** constitute owner authorization to redeliver the old Discord
response, cancel the subject recovery row, mutate the live database, restart the
Gateway, run the installer, or perform semantic acceptance.

Task258's forensic verdict remains authoritative:

- reviewed report: `f44cf675bcbd9e6944cd6635861236637f3eb22f`
- review commit / opening authority: `500f74d3c6b00de0add6311f75d784b0d45f1dfd`
- review verdict: `ACCEPT_FORENSIC_BLOCKED__PENDING_EXACT_SHA_CI_GREEN`
- subject Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- recovery posture: `pending / redeliver`, still emittable by the currently
  proven `dueDirectRecovery()` predicate set
- current owner intent: unproven
- genuine owner-session liveness: unproven; durable session is stale-but-active

## Objective

Root-cause and repair the **product/coordination contract gap** that leaves a
stale-owner pending redelivery indefinitely emittable while no safe successor
can proceed.

Do not assume the correct repair is cancellation. Determine first, from source,
tests, schema, and prior adjudications, whether the system already has a proper
auditable disposition mechanism and whether the recovery liveness predicate is
correct for stale durable sessions.

This task is allowed to change repository source/tests/docs under TDD when a
production defect is proven. It is not allowed to exercise that repair against
the live subject row.

## Required investigation

1. Fetch fresh GitHub authority before work. Require this Task259 to remain the
   active `READY_FOR_HERMES` task and require linear ancestry from `500f74d3...`.
2. Re-open and preserve the accepted Task257/Task258 forensic lineage. Do not
   reclassify unknown owner intent as consent to send or cancel.
3. Inspect the current branch and the previously parked baseline candidate
   `6822af464fe7a5cb3f93305d0263dfc86b56ac68` for all relevant contracts,
   including:
   - `dueDirectRecovery()` selection and wake behavior;
   - owner-session state/generation and any freshness/liveness semantics;
   - recovery claim, completion, cancellation, expiry, abandonment, or
     disposition APIs/commands/services;
   - durable audit/event requirements;
   - assistant-delivery/outbox coupling and idempotency;
   - prior recovery adjudication precedent (including Task205/208/209 where
     applicable).
4. Answer two independent root-cause questions with exact source/test evidence:
   - **Liveness contract:** should a durable session whose row is still
     `state='active'` but demonstrably stale remain sufficient authority for
     automatic redelivery forever?
   - **Disposition contract:** when current owner intent cannot be proven, does
     the product expose a proper exact-ticket, auditable, idempotent way to make
     a stale recovery non-emittable without direct SQL and without causing a
     replay/resend side effect?
5. Distinguish an existing-but-unused mechanism from a missing/defective
   production contract. Do not invent a one-off database command to get past the
   installer gate.

## Required invariants

Any accepted existing mechanism or source repair must preserve all of these:

- stale durable state alone must not be silently promoted to fresh owner intent;
- redelivery and cancellation/disposition authorities remain explicit and
  distinguishable;
- exact Ticket and owner generation are bound, not wildcarded;
- transition is idempotent and durably auditable;
- a disposition transition has a deterministic postcondition that makes the
  relevant `dueDirectRecovery()` predicate false;
- no direct SQL `UPDATE`/`DELETE` is the product contract;
- no cancel/disposition operation may replay, resend, or create semantic output
  as a hidden side effect;
- delivery/outbox state remains internally consistent;
- crash/restart behavior cannot resurrect a dispositioned row unexpectedly.

## TDD / repair rule

If source behavior is defective or the required product disposition path is
missing:

1. **RED** — add the smallest regression test(s) that reproduce the proven
   contract defect. The test must fail for the intended reason before production
   code is changed.
2. **Minimal repair** — change only the necessary source/schema/CLI/service
   contract. Do not bundle unrelated refactors.
3. **GREEN** — rerun the targeted regression, surrounding recovery/delivery
   tests, plugin build, and relevant package/serializer/installer-independent
   validation.
4. Record exact commands, exit codes, changed paths, and hashes in the report.

If the existing product already has a compliant mechanism, do not rewrite it;
prove the path with source/tests and document its exact authority and
postconditions instead.

## Candidate identity boundary

`6822af464fe7a5cb3f93305d0263dfc86b56ac68` remains the accepted **baseline
reference** for the Task254–258 lineage.

If Task259 changes production source, it is no longer permissible to treat
`6822af4...` as the executable candidate for a later live install-over. A new
post-repair exact candidate must be independently reviewed, pass its required CI,
and be frozen before any live Windows successor can be armed.

No Task259 source change may be copied directly into the live installation.

## Live hard fences

```text
subject live DB/recovery row mutation = 0
live recovery clear/cancel/reset/claim = 0
recovery execution/replay/resend = 0
Gateway restart/lifecycle mutation = 0
installer Scheduled Task registration/start = 0
scripts/install.ps1 start = 0
Dashboard/Discord/API semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository/source/test/docs writes and non-live test/build/CI execution are
allowed when required by the investigation and TDD repair.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-259-task258-stale-owner-recovery-disposition-contract-repair.md`

The report must include:

- fresh opening/final authority and ancestry;
- exact root cause for both liveness and disposition questions;
- existing mechanism proof **or** RED → minimal repair → GREEN evidence;
- changed files/commits and exact tests/workflows;
- effect ledger proving all live hard-fence counts stayed zero;
- candidate identity consequence (baseline unchanged vs new candidate required);
- one final disposition:
  - `PROVEN_EXISTING_DISPOSITION_CONTRACT__LIVE_SUCCESSOR_REVIEW_REQUIRED`, or
  - `REPAIRED_STALE_OWNER_RECOVERY_CONTRACT__NEW_CANDIDATE_REVIEW_REQUIRED`, or
  - `BLOCKED_<exact-cause>`.

Then STOP for independent review. Task259 itself must not open or execute a live
redelivery, cancellation, recovery, installer, Gateway restart, or semantic
acceptance action.
