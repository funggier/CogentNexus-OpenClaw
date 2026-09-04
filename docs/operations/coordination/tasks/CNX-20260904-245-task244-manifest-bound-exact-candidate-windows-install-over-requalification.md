# CNX-20260904-245 — Manifest-Bound Exact-Candidate Windows Install-Over Requalification

## Status
`READY_FOR_HERMES`

## Purpose
Correct only the Task-244 Scheduled Task action-binding defect and perform at most one fresh live installer attempt of the accepted exact executable candidate. This task authorizes installer execution only; all semantic sends remain forbidden.

## Authority
- Repo: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Parent: `CNX-20260904-244`
- Runner qualification parent: `CNX-20260904-243`
- Installer evidence parents: `CNX-20260904-241`, `CNX-20260904-244`
- Candidate-validation parent: `CNX-20260904-240`
- Parent umbrella: `CNX-20260831-188`
- Reviewed Task-244 report HEAD: `2da9be61abd1da7ea36c508af640e1732853e2b1`
- Accepted Task-244 review verdict: `ACCEPT_FAIL_CLOSED_PRESTART_ACTION_BINDING_BLOCK__NO_INSTALLER_OR_PRODUCT_EXECUTION__FRESH_MANIFEST_BOUND_SUCCESSOR_AUTHORIZED`
- Exact executable candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Immutable public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Critical design change
Do **not** pass the nested installer child argument vector through Task Scheduler as `-ChildArguments`.

Use this topology instead:

```text
Scheduled Task
  -> Windows PowerShell 5.1
  -> fresh frozen hardened runner
  -> fresh frozen launch manifest JSON
  -> runner resolves child executable + child argument array from manifest
  -> child Windows PowerShell 5.1
  -> -File <exact detached candidate scripts/install.ps1>
```

The Scheduled Task action may contain only the simple runner invocation plus manifest/evidence paths. The installer `-File` target must live in the frozen manifest and must be independently validated before start.

Do not reuse or mutate the Task-244 registered task. Give Task 245 a new unique task name, source path, runner path, manifest path, and evidence root.

## A — Fresh GitHub / candidate gate
Before any live mutation:
1. Fetch branch HEAD, ACTIVE, STATUS, Task 245, Task-244 report/review, and exact-candidate Actions fresh.
2. Require exact SHA `18a51b15768fb3d2196e65f1ef470c34aeef7f36` to have:
   - Validate = SUCCESS
   - Windows Installer Pack Smoke = SUCCESS
   - PS5.1 Acceptance Smoke = SUCCESS
3. Use a fresh clean detached checkout of the exact candidate. Never install from the moving coordination branch.
4. Recompute the candidate plugin fingerprint and require exact `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.
5. Compare post-candidate branch drift. Unexpected product/source/test/workflow drift => `BLOCKED_PREFLIGHT_DRIFT`.

## B — Fresh read-only live inventory
Fresh evidence wins over Task 244. Record:
- controller mode/generation;
- Gateway/provider/model/storage/recovery/delivery health;
- SQLite integrity and pending delivery/outbox state;
- canonical installed plugin path/fingerprint;
- ownership/manifest state;
- pending rollover state;
- existing historical rollover transactions/backups;
- Task-244 registered task state without modifying it;
- retained Task-237 backup token `c6aaf93db7c34f718d01302477a292e1`.

If the candidate is already installed due external drift, stop `BLOCKED_ALREADY_EXACT_EXTERNAL_DRIFT` before creating an installer Scheduled Task.

## C — Re-derive installer state machine
From exact candidate source plus fresh live inventory, record the exact expected classifier/resolver result and intended installer command line.

Do not assume Task-244 state is unchanged. If live state still shows old plugin / no pending rollover, expected topology will likely remain an upgrade requiring rollover, but prove it fresh.

Record whether the invocation should:
- install/replace plugin payload;
- create a new unique rollover transaction/backup;
- finalize rollover;
- call `openclaw plugins install` or not;
- normalize controller/startup state;
- preserve historical transaction/evidence files.

Prove prospective new transaction/backup identities cannot collide with Task-223/237 evidence.

## D — Fresh manifest-bound hardened runner
Create a new unique PowerShell 5.1 runner. It must retain the accepted hardened evidence contract:
- evidence root create/probe before child launch;
- durable `runner-started.json` before child launch;
- identity/PID/CWD/timestamps;
- durable stdout/stderr;
- transcript plus fallback path;
- distinguish `child_nonzero_exit` from `child_launch_exception`;
- `runner-result.json` from `finally`;
- child exit propagated only after durable evidence capture.

Change only the launch-description seam: the runner must accept a launch-manifest path and resolve child executable + argument array from that manifest rather than receiving a nested child-argument string from Task Scheduler.

### D1 — Direct harmless qualification
Before any installer task registration:
1. save runner bytes and initial SHA-256;
2. create a harmless manifest for a synthetic child that writes known stdout/stderr markers and exits `37`;
3. direct-run the exact runner with that manifest and require correct durable evidence + exit `37`;
4. create a harmless manifest pointing to a nonexistent child and require `child_launch_exception` + finally result/fallback evidence;
5. rehash the runner and require byte identity;
6. freeze the runner; no edits after this point.

Safe tooling corrections are allowed only during this direct harmless qualification, before installer registration, and must remain product/semantic side-effect free.

## E — Frozen production launch manifest
Create a separate production manifest containing the resolved installer launch plan. It must include at least:
- schema/version marker;
- child executable absolute path;
- child argument array as distinct elements, not one opaque nested string;
- exact detached candidate installer absolute path;
- exact workspace path and every installer flag/value actually intended;
- source candidate SHA;
- candidate plugin fingerprint;
- generation timestamp / task id for provenance.

Before registration:
1. validate the manifest schema;
2. require child executable to be the intended Windows PowerShell 5.1 executable;
3. locate `-File` in the child argument array;
4. require the value immediately following `-File` to equal the exact detached candidate `scripts/install.ps1` path byte-for-byte after the chosen canonical path normalization;
5. require no second conflicting `-File` occurrence;
6. record manifest SHA-256;
7. freeze the manifest; no edits after this point.

Do **not** execute the production manifest directly during preflight.

## F — One new installer Scheduled Task
Use a unique Task-245 task name and the known-good fully-qualified interactive principal `CDQ-P\CDQ-P`.

Scheduler action must be simple and auditable, conceptually:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <frozen-runner.ps1> -LaunchManifest <frozen-production-manifest.json> -EvidenceRoot <unique-task245-evidence-root>
```

No installer `-File` argument may be encoded directly inside the Scheduled Task action.

Budget:

```text
successful Task-245 installer task registrations: 1 maximum
Task-245 installer task starts: 1 maximum
installer child invocations: 1 maximum
retries after start: 0
```

If registration fails before task creation, prove `TaskPresent=false` and STOP. Do not use a second registration method in Task 245.

## G — Mandatory pre-start readback gate
After successful registration and before start:
1. read back task principal, action executable, full action arguments, execution limit, restart settings, state;
2. require action executable = intended PowerShell 5.1 executable;
3. prove action arguments reference exactly the frozen runner path, frozen production manifest path, and intended evidence root;
4. rehash runner and manifest and require exact frozen SHA matches;
5. re-read the manifest from disk;
6. prove child executable again;
7. prove the unique `-File` target again equals exact detached candidate `scripts/install.ps1`;
8. prove candidate SHA/fingerprint in manifest remain exact;
9. prove task restart count = 0 and no automatic retry policy is enabled.

Any mismatch => `BLOCKED_INSTALLER_ACTION_BINDING` and STOP. Do not update, unregister, repair, or re-register the task in Task 245.

## H — One installer start
Only after all pre-start gates pass, start the Task-245 installer Scheduled Task once.

Immediately close the retry gate:
- no second start;
- no direct `scripts/install.ps1` fallback;
- no manual plugin/rollover repair;
- no task-definition update;
- no process kill to coerce outcome.

Use hardened runner evidence as primary child-boundary authority:
- `runner-started.json`;
- stdout/stderr;
- transcript/fallback;
- `runner-result.json`;
- scheduler `LastTaskResult`.

Classify child launch exception separately from child nonzero exit. A nonzero installer exit is terminal for Task 245; report it and STOP without retry.

## I — Success postflight only if child exit = 0
If and only if the installer child exits `0`, prove all of the following fresh:
- canonical installed plugin fingerprint exactly `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- candidate plugin loaded from canonical managed path;
- expected new rollover transaction/backup exists with unique identity;
- rollover finalized according to exact source contract;
- `pendingRollover=false` after completion;
- historical Task-223/237 evidence unchanged;
- controller/startup state matches the source-derived expected post-install state;
- Gateway/provider/model/storage/recovery/delivery healthy;
- SQLite integrity `ok`;
- no unexpected pending outbox/delivery residue;
- no attributable unexpected Discord/API activity.

Record exact before/after hashes and identities needed to prove the new generation without conflating historical backup hashes.

## Semantic zero budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
```

Semantic durable-delivery requalification remains a separate successor even if Task 245 installer PASSes.

## Hard fences
- No reset/uninstall/reinstall sequence.
- No reuse/mutation/deletion of Task-244 registered task or evidence.
- No manual plugin replacement.
- No manual rollover prepare/finalize.
- No manual controller/Gateway/lifecycle normalization.
- No manual Ticket/outbox/recovery/SQLite writes.
- No provider/model substitution.
- No historical evidence cleanup.
- No release/tag/asset mutation.
- No force push/history rewrite.

## Required report
Publish:

`docs/operations/coordination/reports/CNX-20260904-245-task244-manifest-bound-exact-candidate-windows-install-over-requalification.md`

Report exact:
- fresh authority HEADs;
- exact candidate Actions;
- detached source/fingerprint;
- fresh live preflight;
- source-derived installer state machine;
- runner path/SHA and direct qualification evidence;
- production manifest path/SHA and decoded child argument vector;
- registered task readback;
- pre-start binding proof;
- registration/start/child invocation counts;
- runner/scheduler terminal evidence;
- if exit 0, complete plugin/rollover/runtime/DB postflight;
- semantic/product effect ledger;
- exact final disposition.

Then STOP for independent ChatGPT review.
