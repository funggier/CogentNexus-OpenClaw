# CNX-20260904-241 — Task-240 Exact-Candidate Windows Install-Over Requalification

## Status

`READY_FOR_HERMES`

## Purpose

Perform one bounded live Windows install-over requalification of the exact repository candidate whose production diagnostic repair and cross-platform test harness are now accepted.

This task is installer-only. It does not authorize Dashboard, Discord, API, or recovery semantic acceptance.

## Authority

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-full-stabilization`

Parent Task: `CNX-20260904-240`

Diagnostic parent: `CNX-20260904-239`

Forensic parent: `CNX-20260904-238`

Prior installer failure: `CNX-20260904-237`

Parent umbrella: `CNX-20260831-188`

Accepted Task-240 independent review verdict:

`ACCEPT_PASS_TEST_HARNESS_PORTABILITY_REPAIRED__TASK239_PRODUCTION_DIAGNOSTIC_REPAIR_VALIDATED__EXACT_CANDIDATE_READY_FOR_BOUNDED_LIVE_INSTALL_REQUALIFICATION`

Exact candidate SHA:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Production diagnostic repair contained in candidate lineage:

`ec29020632091aae3b50149b51303a36fde26310`

Expected candidate plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-237 retained orphan backup token:

`c6aaf93db7c34f718d01302477a292e1`

Do not clean, alter, finalize, rename, or otherwise mutate that retained evidence.

## Fresh-authority rule

Before every phase and before any repository write:

1. Fetch current branch HEAD, `ACTIVE.md`, `STATUS.md`, this task, Task-240 report/review, and relevant Actions fresh from GitHub.
2. Fresh GitHub/repository evidence wins over prose in this task if newer.
3. If product/source/test/workflow drift appears after the accepted candidate without explicit reviewed authority, stop `BLOCKED_PREFLIGHT_DRIFT`.
4. Do not force-push or rewrite history.

## Exact source-binding contract

Do not use or invent an unsupported `--install-source-commit` parameter.

Create/materialize a clean detached checkout/worktree of exact commit:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Before installer registration/start prove:

```text
git HEAD = exact candidate
detached source/worktree clean = true
scripts/install.ps1 is from exact candidate
Task-239 diagnostic preservation is present
Task-240 test-only change is present
candidate plugin payload fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Invoke `scripts/install.ps1` from that exact detached source path using the installer's real supported parameter contract only.

## Phase A — Fresh read-only preflight

Before any product execution, collect and record:

- current branch/repository authority;
- exact detached source identity and clean state;
- current controller mode/generation;
- current installed plugin location and fingerprint;
- startup policy and Scheduled Task identity/status/LastTaskResult;
- Gateway health/address;
- Ollama/provider health;
- Delivery status/pending count;
- Recovery status;
- SQLite integrity;
- current Ticket/outbox/recovery counts sufficient to prove no semantic side effects;
- inventory of retained rollover backups and install-staging transactions, including Task-237 token `c6aaf93db7c34f718d01302477a292e1`;
- current public tag identity.

Expected retained live boundary from Tasks 237/238, unless fresh evidence supersedes it:

```text
controller = passthrough
generation = 39
candidate plugin not installed
live predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Gateway healthy
provider = ollama
Delivery READY / pending 0
Recovery READY
SQLite integrity = ok
```

If fresh live state differs materially, investigate read-only and stop if the difference invalidates safe one-shot execution. Do not normalize it manually.

## Phase B — Installer execution budget

Maximum product-side installer budget:

```text
installer Scheduled Task registrations: 1
installer Scheduled Task starts: 1
installer invocations: 1
installer execution retries after start: 0
manual plugin lifecycle mutations: 0
manual controller/managed/Gateway repair: 0
manual rollover-prepare/finalize calls: 0
```

Harmless pre-start observer/tooling retries may use the repository retry policy only when they cannot produce product or semantic side effects. Each retry must be evidence-driven and materially different.

The moment the installer begins product execution:

`INSTALLER_RETRY_GATE=CLOSED`

No rerun or second start is authorized regardless of outcome.

## Phase C — Rollover diagnostic boundary

The exact candidate contains Task-239 diagnostic preservation. If `plugin-rollover-prepare` exits nonzero:

1. Preserve the complete installer-stage markers and the bounded `child diagnostic` emitted by the installer.
2. Record the exact new rollover ID / backup token if one was allocated.
3. Read-only inventory matching backup directory and transaction path.
4. Hash/read evidence sufficient to localize the failing invariant without modifying evidence.
5. Stop immediately with `FAIL_INSTALLER_TERMINAL` or `BLOCKED_EVIDENCE` as appropriate.
6. Do **not** rerun installer, run `rollover-prepare` manually, clean an orphan backup, or attempt a manual repair.

If any later installer stage fails, retain equivalent exact stage/output/cardinality evidence and stop without retry.

## Phase D — Success proof

Only if the one installer invocation returns success, prove all of the following from fresh live evidence:

```text
installer exit = 0
Scheduled Task LastTaskResult = 0
installed canonical plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
candidate source identity coherent
plugin rollover/finalization, if required by classifier = completed exactly once and ownership-safe
no unexpected duplicate plugin generations/direct-extension ambiguity
controller = managed
startup policy = enabled
startup adapter/Scheduled Task = installed + Ready/healthy
Gateway healthy
provider = ollama and healthy
Delivery = READY / pending 0
Recovery = READY
SQLite integrity = ok
no unexpected Ticket/outbox/recovery duplicate or replay
Task-237 retained backup evidence unchanged
public v0.9.3 tag unchanged
```

Record whether the installer classifier selected upgrade/rollover/already-exact behavior and the exact cardinality of:

- `openclaw plugins install`;
- `rollover-prepare`;
- `rollover-finalize`;
- Gateway restart, if installer-owned;
- controller convergence.

Do not infer success from exit code alone.

## Semantic / recovery hard fence

This task authorizes no semantic turn.

```text
Dashboard human semantic submissions: 0
Dashboard automated/native/computer-use submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
provider/model substitution: 0
process termination: 0
```

Existing ordinary historical conversation data may be observed read-only. No new acceptance message is permitted.

## Additional hard fences

Do not perform:

- reset;
- uninstall/fresh reinstall;
- release/tag/asset mutation;
- force push/history rewrite;
- product/source/test/workflow edits during the live execution task;
- Task-237 orphan-backup cleanup;
- Task-223/Task-233 historical evidence cleanup/finalization;
- manual plugin copying/deletion/replacement;
- manual lifecycle normalization after installer failure.

## Report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`

The report must contain:

- fresh starting GitHub authority;
- exact detached source proof;
- preflight live state;
- installer registration/start/invocation cardinality;
- exact installer stage timeline and exit/LastTaskResult;
- rollover ID/backup/transaction/child diagnostic evidence if failure occurs;
- installed plugin/fingerprint/ownership proof if success occurs;
- final runtime health;
- zero-semantic-effect ledger;
- retry ledger;
- exact report commit/HEAD and relevant Actions state.

Then STOP for independent ChatGPT review.

## Allowed final dispositions

- `PASS_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_ROLLOVER_PREPARE`
- `FAIL_ROLLOVER_FINALIZE`
- `FAIL_PLUGIN_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

Even after PASS, do not perform semantic acceptance without a separate reviewed successor task.
