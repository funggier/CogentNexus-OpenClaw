# CNX-20260905-260 — Independent Review

## Verdict

`ACCEPT_BLOCKED_TRANSITION_RISK__CI_GREEN_VERIFIED__REPAIR_SUCCESSOR_REQUIRED`

Task260 is accepted as a correct read-only deployment-transition safety
requalification. The `BLOCKED_DEPLOYMENT_TRANSITION_RISK` outcome is proven:
the supported install-over path has no mandatory fresh Gateway process
boundary after replacement, so a healthy predecessor process can remain the
observed runtime while candidate files are replaced. No installer execution,
Gateway restart, recovery disposition, or semantic send was performed.

## Exact authority and publication

- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed report commit: `74fc4ae713c8e61b9730942e2c4b2d37f5907eb6`
- Re-anchor HEAD at review time: `bbfd43408282a94a76c7d3aa69953f6dcc0d09e8`
  (coordination-docs-only advancement; ACTIVE/STATUS still Task260,
  required report SHA unchanged)
- Ancestry verified linear: `6df1fdd` -> `74fc4ae` -> `bbfd434`, no rewrite
- Report blob: `8b4abc97435990fe37c74611490ba126f9eb71a8`
- Report raw SHA-256 (LF bytes): `4d59e9ff1d4250636e6b4089c3512c4de4ca6ab63da681a3b7ddfcb2d98a4e96`
- Opening HEAD: `6df1fdd9798b3488613fa817f6c9a3e0fb9e51e5`
- `scripts/install.ps1` hash-object: `35a3363a43072c3812e4cb368a81796ee85b3432`
- Public tag: `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)
- Reviewed candidate: `d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6` (unchanged)

## CI gate (independently verified via GitHub API)

Report-commit `74fc4ae` is terminal success, 9/9 check-runs:

- `PS5.1 Acceptance Smoke` run `33956884883`: success
- `Windows Installer Pack Smoke` run `33956884917`: success
- `Validate` run `33956885025`: success
- check-runs: npm-pack, package dry-run, serializer + six validate matrix
  jobs, all `completed success`. No corrective rerun.

Opening HEAD `6df1fdd` CI also verified green (`33955843119`,
`33955843141`, `33955843121`). The executor's local validation
(58/58 files, 286/286 tests, `plugin:validate`, `plugin:build`) is
consistent with green CI; the reviewer did not rerun tests because Task260
is a read-only task with no product mutation to exercise.

## Independent critical-claim checks

1. `skills/cogentnexus-openclaw/scripts/lifecycle_v092.py:233-238`
   documents the gap and forces one process boundary via
   `runtime_boundary.activate_current_config()` in the reset path.
2. `activate_current_config()` is defined in
   `openclaw_runtime_boundary_v092.py:59` and used only by
   `host_control_v092.py:99` and `lifecycle_v092.py:236` — it is absent
   from `scripts/install.ps1` and from the `host_v091.py` enable path,
   confirming the install-over gap.
3. `skills/cogentnexus-openclaw/scripts/cnxclaw.py:241` documents that
   lifecycle `start` deliberately skips Gateway start when already healthy.
4. `host_v091.enable()` (from line 440) runs startup, then
   `lifecycle start --provider`, then health verification — a healthy
   predecessor Gateway satisfies this without loading candidate code.
5. `scripts/install.ps1` managed-enable region verifies ownership, then
   runs enable unless `-SkipGatewayRestart`; no fresh-boundary call exists
   on the success path. Rollback is transactional but does not repair the
   missing success-path proof.
6. Candidate fingerprint `fcecb29a...` vs installed `e3bcce04...` mismatch
   was retained as a preflight check, not normalized. Correct.
7. Subject row binding reconfirmed read-only: accepted `pending/redeliver`,
   `active_run_id=NULL`, session `active/gen1` with stale
   `updated_at=2026-09-01T09:23:13.389Z`, model `ended/completed`, zero
   delivery/outbox rows. The 15-minute fence makes it non-due/non-waking
   at candidate startup by predicate; candidate code was not started.
8. Smallest repair (mandatory post-replacement process boundary reusing the
   proven contract + regression test + fingerprint binding fail-closed) is
   narrow and complete. No live successor is eligible until it is
   published, reviewed, and exact-SHA CI green.

## Scope and effect ledger

The report commit changed only `ACTIVE.md`, `STATUS.md`, and the Task260
report: no source/test/plugin/script changes, no installer registration or
start, no Gateway/controller/provider lifecycle mutation, no live DB or
recovery mutation, no dispose/replay/redeliver/resend, no semantic sends,
no release/tag mutation, no force-push. All live counts are zero.

## Anomalies

- At baton handoff the report-commit CI was still `in_progress`
  (Installer + Validate); it has since reached 9/9 success with no rerun.
  The conditional review hold is therefore released by this review.
- `bbfd434` advanced HEAD with coordination docs only; it does not change
  the required Task260 report SHA or CI binding.

## Disposition and successor boundary

Task260 is accepted but blocked. The pending row stays untouched and
installer requalification stays parked. Task261 is opened separately for
the install-over process-boundary repair. It must not run the installer,
restart the Gateway, mutate live state, or perform semantic acceptance.
