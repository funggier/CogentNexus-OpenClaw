# CNX-20260905-257 — Task256 Pending-Redeliver Recovery Reconciliation (Forensic/Diagnostic)

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: Musethree (independent review of Task256)
Parent task: `CNX-20260905-256`
Parent review: `docs/operations/coordination/reviews/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification-review.md`
Parent umbrella: `CNX-20260831-188`

## Objective

Reconcile the pending direct-recovery row that blocks installer
requalification. This is a read-only forensic/diagnostic task. It must explain
the row, not resolve it by mutation.

Subject row (confirmed independently read-only at Task256 review):

```text
ticket_id        = CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
recovery state   = pending
recovery mode    = redeliver
Ticket status    = accepted
attempt_count    = 0
active_run_id    = NULL
next_attempt_at  = 2026-09-03T01:49:59.316Z (past due)
owner_generation = 1
session state    = active, generation = 1
workflow_eligible = 0
workflow_id      = NULL
model-call fence = one row, state 'ended' (does NOT block dueDirectRecovery)
```

## Required investigation (all read-only)

1. Fetch fresh GitHub authority; require Task257 still active and
   `READY_FOR_HERMES`; verify public tag `v0.9.3 = 26ce64a...2e31` unchanged.
2. Re-open the live SQLite database with `file:<path>?mode=ro` only. Inspect
   schema before querying. Never write, vacuum, replay, or mutate.
3. Determine for the subject row, with exact evidence:
   - what payload/mode `redeliver` would emit and through which transport
     (trace `launchV093DirectRecovery` and the redeliver path at the exact
     candidate `6822af4`, `plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts`);
   - which owner session owns it and whether that session is genuinely live or
     stale-but-active;
   - why the row has been pending since `2026-09-03` (service history, wake
     scheduling, prior attempts — `attempt_count = 0` with a past-due timestamp
     needs an explanation, not an assumption);
   - whether the redelivery is still desired by the Ticket owner, and what the
     safe disposition options are (each with exact predicate and authorizing
     contract — do NOT execute any of them);
   - the exact `dueDirectRecovery()` predicate set a future live task must
     require (row absent, cancelled via proper authority, fence `active`, or
     other proven-non-emittable state), so the installer gate can be armed
     without guessing.
4. Record the model-call fence row state and the `cnx_assistant_delivery` /
   outbox posture for the same Ticket without mutating them.
5. Preserve all observations under a durable evidence root
   (`%LOCALAPPDATA%\CogentNexus-OpenClaw\forensics\CNX-20260905-257`) with exact
   commands, exit codes, and read-only proofs.

## Reference authority

- Exact candidate source: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`
  (`core.autocrlf=false` for any byte proof; canonical installer
  `9d53a427...`, runner `729fba45...`).
- Prior recovery adjudications for method precedent (do not re-litigate their
  verdicts): Task205/208/209 recovery-executability records.

## Cardinality / hard fences

```text
DB writes/vacuum/replay/resend = 0
recovery row mutation (clear/cancel/reset) = 0
installer Scheduled Task registrations = 0
installer Scheduled Task starts = 0
scripts/install.ps1 starts = 0
Dashboard/Discord/API semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Do NOT clear, cancel, replay, resend, or otherwise mutate the pending recovery
row in this task. Do NOT register/start the installer. Do NOT perform semantic
acceptance. Any disposition of the row requires a separately authorized task
after this forensic is independently reviewed.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-257-task256-pending-redeliver-recovery-reconciliation.md`

Include: fresh authority; exact row evidence (full predicate binding +
fence-row state); redeliver payload/transport trace with source lines;
owner-session liveness finding; why-pending-since-09-03 analysis;
desired-or-not assessment with disposition options (unexecuted); exact predicate
set for a future live gate; zero-mutation ledger; tag immutability; final
disposition (`RECONCILED_*` with recommendation, or `BLOCKED_*` with cause).

Then STOP for independent review. Installer requalification stays parked until
reconciliation is accepted.
