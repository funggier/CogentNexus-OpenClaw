# CNX-20260905-256 — Independent Review

## Verdict

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__FAIL_CLOSED_CORRECT__PENDING_REDELIVER_EMITTABLE__RECOVERY_RECONCILIATION_REQUIRED`

The executor's `BLOCKED_PREFLIGHT_DRIFT` disposition is accepted. The one-shot
installer was correctly never started. Independent read-only verification
strengthens the finding: the pending redeliver row is not merely "potentially"
emittable — the model-call fence affirmatively does not block it.

## Reviewed authority

- Task: `docs/operations/coordination/tasks/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`
- Report: `docs/operations/coordination/reports/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`
- Report HEAD: `5b4baa5145e8d245608291923b279184d9fb12bd`
- Opening remote HEAD for the task: `d6e1d86395d1bd60d110a2a905d1c9518ba9064e`
- Exact candidate: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`
- Reviewer checkout: fresh fetch, `LOCAL_HEAD == REMOTE_HEAD == 5b4baa5`, clean worktree.

## Independent verification

1. Ancestry: `d6e1d86` is an ancestor of `5b4baa5` (fast-forward, no history
   rewrite). Publication adds exactly one file at the matching report path
   (`116` insertions, no source/test changes). Report blob `3bd37b97...` matches
   the executor's claim.
2. Canonical identities recomputed from the reviewer clone:
   installer `git show 6822af4:scripts/install.ps1` = `9d53a427...e17b57b`;
   runner = `729fba45...a6250f3e`. Both match the reconciled Task256 contract.
   The CRLF-materialized `c0779d...` was correctly kept diagnosis-only. The
   Task255 identity-contract defect stays fixed.
3. Candidate plugin fingerprint `1ff69c45...babb5f` is consistent with the
   accepted lineage across Task254/255/256 records. It was not independently
   rebuilt (executor-evidenced via `a02/a03/a04`); recorded as consistent, not
   re-proven.
4. Live SQLite re-opened read-only (`mode=ro`, SELECT + `pragma` only, zero
   mutations, `integrity_check = ok`). The `CNXT-dc11c9a0` row is confirmed
   exactly as reported: `pending / redeliver / accepted`, `attempt_count = 0`,
   `active_run_id = NULL`, `next_attempt_at = 2026-09-03T01:49:59.316Z` (past
   due), `owner_generation = 1`, session `active` generation `1`,
   `workflow_eligible = 0`, `workflow_id = NULL`. Every static predicate of
   `dueDirectRecovery()` (`v091-direct-recovery.ts:81-83`) holds.
5. New reviewer evidence — model-call fence affirmatively open: the
   `cnx_direct_model_call` row for this Ticket has `state = 'ended'`, which is
   NOT in `('active','recovering')`, so `modelCallRecoveryFence()` (`:47-51`,
   applied at `:77,83`) does not exclude it. `dueDirectRecovery()` returns this
   Ticket today. Combined with the entrypoint that runs recovery at service
   start (`createEventDrivenDirectRecoveryService`, `:190-251`, immediate
   `run()` at `:250` → `launchV093DirectRecovery` at `:234-236`), a Gateway
   restart from install-over would fire this redelivery. The fail-closed STOP
   was therefore mandatory, not merely cautious.
6. Scheduler read-only check: no Task255/Task256 installer task exists, matching
   the reported `registrations = 0 / starts = 0` ledger. Pre-existing residues
   from older tasks (`Task237/241/242-Canary/243/244/245/248/251`, all `Ready`)
   remain; they were not created or started by Task256 and are flagged as
   hygiene only, outside this verdict.
7. Exact-candidate CI: zero non-success check-runs on `6822af4` (nine `success`,
   IDs match prior pre-gate). Report-HEAD workflows: PS5.1 Acceptance Smoke
   `success`; Validate + Windows Installer Pack Smoke `in_progress` at review
   time (docs-only commit; non-terminal CI is noted, not a product gate for a
   BLOCKED report). Public `v0.9.3` remains `26ce64a...2e31`.
8. Hard fences: `installer starts = 0`, `retries = 0`, `semantic sends = 0`,
   `recovery replay/resend = 0`, `DB/manual lifecycle mutation = 0`,
   `release/tag = 0`, no force-push. The single harness path error (exit `2`,
   corrected with absolute path) and npm audit warnings were preserved as
   harness evidence without product effect — correctly handled.

## Provenance note

The blocking row predates Task256 (due since `2026-09-03`) and is unrelated to
the Task255 canonical-vs-CRLF contract defect. No installer, recovery, or
semantic action in Tasks 255/256 created it. Its disposition belongs to a
recovery-reconciliation authority, not to the installer executor.

## Successor authorization boundary

No live installer successor is authorized while the emittable redeliver row
stands: any install-over restarts the Gateway and fires the pending redelivery,
breaking the semantic-zero budget. The separately published Task257 is a
read-only forensic/diagnostic task that must determine the row's payload and
ownership, why it has been pending since `2026-09-03`, whether redelivery is
still desired, and the exact predicate set a future live task must require —
without clearing, cancelling, replaying, or mutating it. Installer
requalification remains parked until that reconciliation is independently
reviewed and accepted. Semantic acceptance remains unauthorized throughout.

## Effect ledger adjudication

Reviewer performed read-only verification (GitHub API, `git show` recomputation,
`mode=ro` SQLite SELECTs, read-only scheduler list) plus four coordination-doc
writes (review + successor task + ACTIVE + STATUS) in one report-only publication
commit. No installer execution, scheduler/DB/lifecycle mutation, replay, semantic
send, release/tag mutation, or force-push was performed or authorized by this
review.
