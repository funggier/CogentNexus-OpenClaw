# CNX-20260828-117 — Installer Provider Binding Origin Diagnosis and Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_TDD_REPAIR`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Diagnose and repair the exact Windows PowerShell installer invocation/binding defect exposed by Task 116:

```text
Cannot validate argument on parameter 'Provider'. The argument "3D Objects" does not belong to the set "ollama" specified by the ValidateSet attribute.
```

Task 116 proved the live machine coherent, then stopped correctly after the first install-over attempt failed during PowerShell parameter binding before the installer body executed.

This successor is **source/diagnosis/test/CI/package only**. It does not authorize another live install-over or any lifecycle mutation.

## Authoritative Task-116 evidence

Task-116 report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Accepted live facts:

- Phase 0 PASS;
- OpenClaw exactly `2026.7.1-2`;
- selected provider `ollama`, healthy;
- CNX `passthrough`, generation `25`;
- Gateway healthy;
- SQLite integrity `ok`;
- supported interrupted-reentry classification proven;
- one install-over attempt only;
- parameter-binding failure before installer body;
- no reset/uninstall/reinstall/lifecycle/recovery execution;
- post-failure state remained coherent;
- no Dashboard semantic Send.

Frozen Task-116 source for diagnosis:

`47b069daed90f54feae2c9eb26f38c438493f3c8`

## Key source observation already independently verified

The frozen `scripts/install.ps1` declares:

```powershell
[ValidateSet("ollama")]
[string]$Provider = "ollama"
```

but `$Provider` is otherwise unused by installer behavior. The v0.9.3 installer is already Ollama-only and prints `Provider: ollama` literally.

Therefore the observed `3D Objects` value is not explained by ordinary evaluation of the source default alone. Trace the bad value backward through the actual invocation boundary before changing production code.

## Phase 0 — fresh repository reconciliation

Before any implementation:

1. fetch current branch HEAD;
2. confirm Task 117 is active in both `ACTIVE.md` and `STATUS.md`;
3. confirm no newer task superseded this authorization;
4. compare from Task-116 report/review boundary to current HEAD;
5. ensure no unreviewed production source change already attempts to repair Provider binding.

If source already changed unexpectedly, stop and report for review instead of layering another fix.

## Phase 1 — root-cause investigation, no production edit

Use preserved Task-116 evidence and a non-mutating Windows reproduction environment to trace where `3D Objects` came from.

### 1A. Inspect preserved invocation evidence

Read-only inspect the Task-116 external evidence root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\20260828-210020`

Locate the exact install-over invocation record and any executor-generated script/wrapper/argument array used for the call.

Capture, if present:

- raw command line;
- caller script source/hash;
- splatted hashtable/argument-array construction;
- current directory;
- caller PowerShell edition/version;
- whether `-Provider` was present implicitly or explicitly in the actual invocation layer;
- any value-resolution command used to derive provider;
- any prior pipeline whose output could have populated that value.

Do not modify the evidence directory or live CNX/OpenClaw/Ollama state.

### 1B. PowerShell binding context

In an isolated/non-mutating reproduction process, record relevant binding state:

```powershell
$PSVersionTable
$PSDefaultParameterValues
(Get-Command .\scripts\install.ps1).Parameters.Keys
```

If a caller wrapper exists, instrument the caller boundary to show exactly what arguments enter `install.ps1`.

Do not expose secrets or unrelated user data.

### 1C. Trace the bad value to one concrete origin

The diagnosis must name the exact data-flow origin, for example:

`source value -> caller variable/command -> argument construction/splat -> install.ps1 Provider binding -> ValidateSet failure`

Do not stop at “Provider resolved incorrectly.”

If the preserved Task-116 evidence is insufficient, reproduce the same binding behavior in an isolated Windows test workspace using stubs/fakes for external commands so no live CNX/OpenClaw/Ollama mutation occurs.

## Phase 2 — TDD RED

**No production edit before semantic RED.**

The first implementation commit must change tests/diagnostic harnesses only.

The RED must reproduce the real root cause discovered in Phase 1.

Requirements:

- it must fail on the Task-116 production source/caller;
- failure must be because the actual bad-value path remains possible;
- it must not merely invoke `install.ps1 -Provider "3D Objects"` explicitly and call that reproduction complete;
- it must exercise the real repository caller/binding surface implicated by Phase 1, or a faithful isolated reproduction of the same PowerShell binding mechanism;
- record exact RED command/output and commit SHA.

If the test is GREEN before production change, it does not prove the Task-116 defect. Correct the test/diagnosis before proceeding.

## Phase 3 — minimal production repair

After legitimate RED only, make one minimal repair at the actual source of the bad value.

### Preferred design invariant

v0.9.3 is Ollama-only. The installer should not expose or resolve a provider-selection input that has no behavioral use.

Because `$Provider` is currently a dead parameter, **removing the unnecessary `Provider` parameter is preferred if Phase-1 evidence shows that this exposed binding surface participated in the actual failure**.

If instead the real defect is a repository caller/helper that erroneously supplies `Provider`, fix that caller at source. Do not retain unnecessary provider auto-detection/resolution logic merely to accommodate a broken caller.

Do not introduce multi-provider behavior, LM Studio support, provider fallback, or user provider selection.

### Required behavior after repair

The normal Task-116 command shape:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

must have deterministic Ollama-only semantics and must not depend on home-directory listing order, ambient pipeline output, current directory contents, or unrelated PowerShell provider values.

## Phase 4 — GREEN and focused regression validation

Run the exact RED test and require GREEN.

Also validate at minimum:

1. PowerShell 5.1 parser/AST syntax for installer;
2. installer parameter metadata/command-shape test;
3. exact no-Provider Task-116 invocation shape in isolated non-mutating smoke;
4. any hostile/ambient binding context that reproduced Task 116 no longer injects an unrelated value;
5. Ollama-only invariant remains explicit;
6. plugin lifecycle action resolver tests;
7. npm12 installer boundary tests;
8. interrupted-reentry/ownership semantic matrix;
9. fresh transaction rollback/recovery suites;
10. package installer contract still contains supported local archive invocation:

```text
openclaw plugins install $packagePath --force
```

No unrelated production refactor.

## Phase 5 — full repository validation

Require current-source success for:

- full `pytest` suite;
- Python `py_compile` set used by Validate;
- PowerShell installer AST validation;
- namespace isolation checker;
- `npm ci`;
- `npm test`;
- `npm run evaluation`;
- `npm audit --omit=dev`;
- `npm run plugin:validate`;
- `git diff --check`.

Record exact counts/results.

## Phase 6 — exact candidate CI/package proof

Freeze one exact repaired candidate SHA after tests+production repair and before report-only commits.

Require all three workflows on that exact SHA:

1. Validate — success;
2. Windows Installer Pack Smoke — success;
3. PS5.1 Acceptance Smoke — success.

Do not combine statuses from different SHAs.

Require a **new** package-proof artifact. Do not reuse Task-116 artifact `9687249771`.

Independently verify:

- outer artifact SHA256;
- inner ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- `PAYLOAD_IDENTITY.json` payload count/fingerprint;
- `SHA256SUMS.txt`;
- packaged installer contains the repaired provider-binding surface/absence as intended;
- packaged installer still uses `openclaw plugins install $packagePath --force`;
- Task-113 conflicting-product rejection remains packaged;
- Task-112 active wrapper proof remains packaged;
- Task-110 retired exactness proof remains packaged;
- recovery harness blob remains unchanged unless a separately proven reason requires otherwise.

## Phase 7 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Report must include:

- exact root cause/data flow producing `3D Objects`;
- preserved Task-116 evidence used;
- RED commit and exact failing output;
- production repair commit and files;
- GREEN/targeted/full validation;
- exact candidate SHA;
- all exact-SHA workflow run IDs/results;
- new artifact ID and hashes/identity;
- candidate-to-report diff proving report-only closure;
- verdict `PASS`/`FAIL`/`BLOCKED`;
- remaining live work.

Then stop for independent ChatGPT review.

Do not create or execute a lifecycle retry task automatically.

## Hard fence

Task 117 does **not** authorize:

- real Windows install-over against the live workspace;
- `cnxclaw reset`;
- `cnxclaw uninstall`;
- fresh live reinstall;
- live stop/start/restart;
- recovery-reality disruptive harness;
- manual cleanup/normalization of Task-107/116 residue;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- Ollama update/reinstall/stop/reconfigure;
- provider/model/timeout changes;
- LM Studio management;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/tokens/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot or generic process-tree kill;
- merge/tag/GitHub Release/force push.

Read-only inspection of preserved Task-116 evidence and isolated Windows diagnostic reproduction is authorized.
