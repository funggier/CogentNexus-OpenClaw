# CNX-20260905-260 — Deployment Transition Safety Requalification

**Final disposition:** `BLOCKED_DEPLOYMENT_TRANSITION_RISK`

**Authority:** `origin/agent/v0.9.3-full-stabilization`
**Exact HEAD:** `6df1fdd9798b3488613fa817f6c9a3e0fb9e51e5`
**Executor:** Luna
**Next actor:** Musethree (independent review)
**Scope:** repository/source/tests/GitHub Actions and read-only Windows/SQLite inspection only.

## Executive result

The Task259 candidate is source- and CI-valid, and the known stale recovery row is fenced by the repaired 15-minute freshness predicate. However, the supported install-over transition does not prove the required process-boundary proposition: after replacement, the final healthy Gateway process is guaranteed to load the repaired candidate rather than retain the predecessor process/runtime. The task therefore fails closed without installer execution, Gateway restart, recovery disposition, or semantic send.

## Fresh authority and CI

- Fresh remote: `6df1fdd9798b3488613fa817f6c9a3e0fb9e51e5`.
- `git hash-object scripts/install.ps1`: `35a3363a43072c3812e4cb368a81796ee85b3432`.
- GitHub Actions for exact HEAD, all completed success:
  - PS5.1 Acceptance Smoke — run `33955843119`
  - Windows Installer Pack Smoke — run `33955843141`
  - Validate — run `33955843121`
- Disposable exact-HEAD plugin validation: `58/58 files, 286/286 tests`; `plugin:validate` PASS; `plugin:build` PASS; mixed-plugin artifact verification PASS; ticket DB bootstrap PASS; package contents PASS (196 files).

## Candidate identity

After disposable build, canonical payload fingerprints were computed using the repository's `namespace_ownership.plugin_fingerprint()`:

- Candidate source: `C:\Users\CDQ-P\AppData\Local\Temp\cnx260-requal-6df1fdd\plugins\cogentnexus-openclaw`
- Candidate source fingerprint: `fcecb29aa6605a888e262dd9d4b1b398f51e7e520feb59b65b99b7662d7f86b4`
- Current installed extension: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Current installed fingerprint: `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`
- Installed ownership manifest is coherent v0.9.3 and points to the canonical workspace/extension; the fingerprint mismatch is retained as a required preflight transition check, not normalized or overwritten.
- Legacy/foreign npm project candidates were not accepted as payloads; no cleanup was attempted.

## Source lifecycle trace

1. `scripts/install.ps1` invokes the existing native boundary before replacement (`Enter-NativeInstallBoundary`, install script lines 130–139), then stages/replaces the skill/plugin payload (lines 327–349 and 378–468), and invokes managed enable only after ownership/config checks (lines 501–534).
2. `host_v091.disable()` first performs startup disable, removes policy, disables the plugin, cancels lifecycle, restores the native Gateway, and commits passthrough (lines 573–588). This is a useful native safety boundary, but it leaves a healthy native Gateway process running during file/package replacement.
3. `host_v091.enable()` disables the plugin while configuring, applies policy, enables the plugin, calls `legacy.startup(..., "enable")`, and then calls `legacy.runtime(..., "lifecycle", "start", "--provider")` (lines 461–487).
4. The source itself documents the gap in `lifecycle_v092.reset()` (lines 233–238): lifecycle start may skip Gateway start when it is already healthy, so reset explicitly calls `runtime_boundary.activate_current_config()` to force one process boundary before verification.
5. The install-over path has no equivalent mandatory `activate_current_config()`/fresh Gateway process boundary after replacement and before declaring the candidate active. Therefore a healthy native/predecessor process can remain the process observed after install-over while the candidate files have been replaced. A post-stop/final-start guarantee that the repaired direct-recovery code is loaded is not proven.
6. Failure rollback in `host_v091.enable()` is transactional and attempts startup disable, plugin disable, lifecycle cancel, policy restore, native Gateway restore, and passthrough state rollback (lines 488–531), but rollback safety does not repair the missing successful-path process-boundary proof.

## Read-only Windows/runtime/SQLite evidence

- Canonical launcher discovered at `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`; no launcher command was executed.
- Current status/health probes were read-only; Gateway and Ollama listeners were present. No scheduled task registration/start or lifecycle mutation was performed.
- Ownership manifest verification passed for installed v0.9.3 paths.
- SQLite opened with Python `sqlite3` URI `mode=ro`; integrity was `ok`.
- Subject ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`, accepted, recovery `pending/redeliver`, `active_run_id=NULL`.
- Recovery owner: session `active`, generation `1`, `updated_at=2026-09-01T09:23:13.389Z`; model call is ended/completed.
- No `cnx_assistant_delivery` row and no outbox row.
- No live state mutation was observed or performed during this task.

## Freshness determination

Task259's 15-minute session liveness fence compares session `updated_at` against the current cutoff for due/wake selection. The subject timestamp is several days older than the current 2026-09-05 observation window, so the row is stale and would be non-due/non-waking under the candidate predicate at startup. This is a source-predicate conclusion; candidate code was not started to prove it, and no disposition/replay/redelivery was attempted.

## Smallest required repair

Add a mandatory successful-path managed Gateway process boundary to the supported install-over transaction after candidate replacement and before final activation/health verification. Reuse the already-proven `runtime_boundary.activate_current_config()` contract (or an equivalently explicit stop/start boundary) in the install-over path, and add a regression test asserting that a healthy native Gateway cannot satisfy install-over success without a fresh process boundary and candidate fingerprint/plugin verification. The repair must also bind the installed payload fingerprint to the expected candidate fingerprint and fail closed on mismatch.

No live successor is eligible until this source/test repair is published, independently reviewed, and exact-SHA CI is green. A future live install-over task must remain one-shot with preflight identity/ownership/fingerprint gates, bounded transition actions, postflight fresh-process/plugin/fingerprint/health gates, and abort-on-drift.

## Hard-fence ledger

- installer Scheduled Task registration/start: `0`
- `scripts/install.ps1` live starts: `0`
- Gateway/controller/provider lifecycle mutation: `0`
- live DB/recovery mutation: `0`
- claim/dispose/replay/redeliver/resend: `0`
- Dashboard/Discord/API semantic sends: `0`
- release/tag mutation: `0`
- force push/history rewrite: `0`
