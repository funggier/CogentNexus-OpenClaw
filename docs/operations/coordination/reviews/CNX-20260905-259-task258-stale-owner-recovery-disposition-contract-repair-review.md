# CNX-20260905-259 — Review

## Verdict

`ACCEPT_CONTRACT_REPAIR__CI_GREEN_VERIFIED__LIVE_SUCCESSOR_REVIEW_REQUIRED`

Task259 is accepted as a valid repository/source/test contract repair. The
repair is review-approved for the new candidate, but this review does not
authorize live recovery disposition, redelivery, Gateway/installer activity,
or semantic acceptance. Those remain parked behind a separately authorized
successor task.

## Exact authority and publication

- Fresh remote branch: `agent/v0.9.3-full-stabilization`.
- Re-anchor result: local and origin both `d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6`.
- Required Task258 ancestor: `500f74d3c6b00de0add6311f75d784b0d45f1dfd`; linear ancestry verified.
- Executor report is present on the remote tree at:
  `docs/operations/coordination/reports/CNX-20260905-259-task258-stale-owner-recovery-disposition-contract-repair.md`.
- Report raw SHA-256 on remote: `4e06ed09f3bf46d164974da5f028ec3b9058a55b668252008f569e51b6d8d52f`.
- Reviewed source raw SHA-256 on remote:
  `v090.ts` = `b76acab40ce75d617ec1728572740f646d066eee2b5d7ab9fc6d610bed572420`;
  `v091-direct-recovery.ts` = `f49c776e7647c5ae1df136c35fdc500f9e5323080fc1d6a09e8039d9848abb6e`.

## Independent critical-claim checks

1. `dueDirectRecovery()` now requires active matching generation plus
   `cnx_sessions.updated_at` within the fixed 15-minute liveness window; stale
   active state is not sufficient.
2. `nextDirectRecoveryWakeMs()` applies the same freshness predicate to pending
   recovery wake selection, preventing indefinite stale wake scheduling.
3. `disposeDirectRecoveryTicket()` binds exact Ticket, owner session, and owner
   generation, requires an existing recovery row, uses `BEGIN IMMEDIATE`, and
   makes the recovery predicate false by dispositioning the exact Ticket/row.
4. The disposition clears only exact-ticket pending outbox/assistant-delivery
   records, emits `direct_recovery_dispositioned`, and does not call workflow,
   delivery, Discord, Gateway, or installer paths.
5. Repeat disposition is idempotent and reports `alreadyDispositioned`; sibling
   Tickets remain untouched in the regression test.
6. Baseline `6822af4…` was correctly retired as executable candidate because
   production source changed; `d153140…` is the new candidate.

## CI and validation

GitHub Actions on exact HEAD `d153140…` were independently checked through the
GitHub API: **9/9 check-runs completed success** — serializer, six validate
matrix jobs, npm-pack, and package dry-run. The three workflow runs were also
terminal success:

- PS5.1 Acceptance Smoke `33953878910`
- Windows Installer Pack Smoke `33953878911`
- Validate `33953878916`

The executor's local validation evidence is consistent with the published
candidate: full Vitest 58/58 files and 286/286 tests, targeted 12/12 tests,
TypeScript/plugin build, schema verification, DB bootstrap, and package-content
validation all passed.

## Scope, anomalies, and hard fences

No live subject row, live database, recovery execution, replay/resend, Gateway,
installer Scheduled Task, semantic send, release/tag, or force-push was touched.
All live hard-fence counts remain **0**. The earlier wrong-root test command,
initial dependency installation, and Windows fixture-lock cleanup are recorded
as transient execution issues in the executor report and do not alter product
outcome.

No unresolved product blocker was found for the repository repair. Residual
uncertainty is intentionally unchanged: current owner intent and genuine live
session liveness for the old Discord response remain unproven, and this review
has not inspected or mutated that live row.

## Reviewer verification packet

- Remote ref and exact HEAD equality.
- Linear ancestry from `500f74d…`.
- Remote report presence and raw SHA-256.
- Remote source raw SHA-256 for both production files.
- GitHub API check-runs count/conclusion for exact HEAD.
- Exact binding/idempotency/no-replay source and regression claims.
- Hard-fence and candidate-identity boundary.

## Next boundary

Keep baseline `6822af4…` parked and do not install or exercise `d153140…` live.
A separately authorized successor may define live disposition or another safe
coordination action; this review does not create that authority.
