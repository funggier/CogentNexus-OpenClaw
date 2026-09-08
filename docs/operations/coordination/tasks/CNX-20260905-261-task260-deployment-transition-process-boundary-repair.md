# CNX-20260905-261 — Task260 Deployment-Transition Process-Boundary Repair

Status: `READY_FOR_LUNA`
Executor: Luna
Coordinator / independent reviewer: Musethree
Parent task: `CNX-20260905-260`
Parent review: `docs/operations/coordination/reviews/CNX-20260905-260-task259-candidate-deployment-transition-safety-requalification-review.md`
Parent umbrella: `CNX-20260831-188`

## Authority and boundary

Task260 proved (and independent review accepted) that the supported
install-over path has no mandatory fresh Gateway process boundary after
replacement: a healthy predecessor process can remain the observed runtime
while candidate files are replaced, because lifecycle `start` deliberately
skips Gateway start when already healthy.

That finding authorizes repository/source/test diagnosis and repair needed
to close the transition gap. It does **not** authorize running the
installer against the live installation, restarting the live Gateway,
mutating the live database or subject recovery row, performing any
recovery disposition/redelivery, or any semantic acceptance.

Task259/Task260 forensic verdicts remain authoritative:

- reviewed candidate: `d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6`
- subject Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
  (`pending / redeliver`, still emittable under predecessor code)
- current owner intent: unproven; owner session: stale-but-active

## Objective

Add a mandatory successful-path managed Gateway process boundary to the
supported install-over transaction after candidate replacement and before
final activation/health verification, so install-over success proves the
running Gateway loaded the repaired candidate.

Reuse the already-proven `runtime_boundary.activate_current_config()`
contract (or an equivalently explicit stop/start boundary) in the
install-over path. Bind the installed payload fingerprint to the expected
candidate fingerprint and fail closed on mismatch.

## Required work

1. Fetch fresh GitHub authority before work. Require this Task261 to
   remain the active `READY_FOR_LUNA` task with linear ancestry from the
   review commit that opened it.
2. Re-open the Task260 lifecycle trace from exact source (do not trust
   memory): preflight, stop behavior, replacement point, intermediate
   start paths, final Gateway start, rollback branches.
3. TDD repair:
   - **RED** — add the smallest regression test(s) proving the defect: a
     healthy native/predecessor Gateway must NOT satisfy install-over
     success without a fresh process boundary and without candidate
     fingerprint/plugin verification.
   - **Minimal repair** — add the mandatory post-replacement boundary call
     plus fingerprint binding on the install-over success path only. Do
     not bundle unrelated refactors.
   - **GREEN** — rerun the targeted regression, surrounding
     lifecycle/installer/host tests, plugin build, and relevant
     package/serializer validation.
4. Record exact commands, exit codes, changed paths, and hashes.

## Required invariants

- a healthy predecessor Gateway alone must never satisfy install-over
  success;
- the boundary must execute after file/package replacement and before
  final health verification declares the candidate active;
- installed payload fingerprint must equal the expected candidate
  fingerprint; mismatch fails closed;
- rollback branches stay transactional and must not gain new live side
  effects;
- `-SkipGatewayRestart` semantics stay explicit and must not silently
  become a verified managed transition;
- no repair step starts the candidate against live state to prove itself;
- crash/restart behavior must not resurrect an unverified runtime as
  verified.

## Candidate identity boundary

`d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6` remains the accepted
**baseline reference** for the Task259 contract repair.

If Task261 changes production source, `d153140...` is no longer an
executable candidate for live install-over. The post-repair commit becomes
a new candidate requiring independent review, authoritative CI, exact SHA
binding, and fresh Windows proof before any live successor can be armed.

No Task261 source change may be copied directly into the live installation.

## Live hard fences

```text
installer Scheduled Task registration/start = 0
scripts/install.ps1 live starts = 0
Gateway/controller/provider lifecycle mutation = 0
live DB/recovery row mutation = 0
recovery dispose/claim/replay/redeliver/resend = 0
Dashboard/Discord/API semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository/source/test/docs writes and non-live test/build/CI execution are
allowed when required by the investigation and TDD repair.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-261-task260-deployment-transition-process-boundary-repair.md`

Include: fresh opening/final authority and ancestry; exact root-cause
confirmation; RED -> minimal repair -> GREEN evidence; changed
files/commits and exact tests/workflows; effect ledger proving all live
hard-fence counts stayed zero; candidate identity consequence; one final
disposition:

- `REPAIRED_DEPLOYMENT_TRANSITION_BOUNDARY__NEW_CANDIDATE_REVIEW_REQUIRED`, or
- `BLOCKED_<exact-cause>`.

Then STOP for independent review. Task261 itself must not open or execute
a live install-over, recovery disposition, Gateway restart, or semantic
acceptance action.
