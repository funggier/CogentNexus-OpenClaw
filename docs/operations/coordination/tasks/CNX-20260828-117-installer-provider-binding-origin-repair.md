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

## Key source + compatibility observations already independently verified

Frozen `scripts/install.ps1` declares:

```powershell
[ValidateSet("ollama")]
[string]$Provider = "ollama"
```

but `$Provider` is otherwise unused by installer behavior. The v0.9.3 installer is already Ollama-only and prints `Provider: ollama` literally.

However, `docs/INSTALL.md`, `docs/INSTALL.th.md`, README/recovery guidance, and historical accepted commands still document the public invocation:

```powershell
.\scripts\install.ps1 -Provider ollama
```

Therefore `Provider` is a dead **behavioral** input but still a current **compatibility/API** surface. Do not remove it casually. Preserve explicit `-Provider ollama` compatibility unless root-cause evidence plus tests justify an intentional contract change and all current documentation/callers are updated consistently.

The observed `3D Objects` value is not explained by ordinary evaluation of the source default alone. Trace the bad value backward through the actual invocation boundary before changing production code.

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

Read-only inspect:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\20260828-210020`

Locate the exact install-over invocation record and any executor-generated script/wrapper/argument array.

Capture, if present:

- raw command line;
- caller script source/hash;
- splatted hashtable/argument-array construction;
- current directory;
- caller PowerShell edition/version;
- whether `-Provider` was present explicitly, implicitly, or positionally;
- any value-resolution command used to derive provider;
- any prior command/pipeline whose output could have populated the value;
- any extra positional token after named `-Workspace`.

Do not modify preserved evidence or live CNX/OpenClaw/Ollama state.

### 1B. PowerShell binding context

In an isolated/non-mutating Windows process, record relevant binding state:

```powershell
$PSVersionTable
$PSDefaultParameterValues
(Get-Command .\scripts\install.ps1).Parameters.Keys
```

Also determine the effective positional-binding behavior of this advanced script and whether an unexpected positional token can bind to `Provider` when `-Provider` is omitted.

This is a hypothesis to test, not an assumed root cause.

If a caller wrapper exists, instrument only the caller boundary to show exactly which arguments enter `install.ps1`.

### 1C. Trace one exact data flow

The diagnosis must name the concrete path, for example:

`source value -> caller variable/command -> argument construction/splat/position -> install.ps1 Provider binding -> ValidateSet failure`

Do not stop at “Provider resolved incorrectly.”

If preserved evidence is insufficient, reproduce the same binding behavior in an isolated Windows test workspace using stubs/fakes for all external commands so no live CNX/OpenClaw/Ollama mutation occurs.

## Phase 2 — TDD RED

**No production edit before semantic RED.**

The first implementation commit must change tests/diagnostic harnesses only.

The RED must reproduce the real root cause from Phase 1.

Requirements:

- fail on Task-116 production source/caller;
- fail because the actual unexpected bad-value path remains possible;
- do not merely call `install.ps1 -Provider "3D Objects"` explicitly and call that reproduction complete;
- exercise the real repository caller/binding surface or a faithful isolated reproduction of the same PowerShell mechanism;
- record exact RED command/output and commit SHA.

If the test is GREEN before production change, fix the test/diagnosis rather than fabricating RED history.

## Phase 3 — minimal production repair

After legitimate RED only, make one minimal repair at the actual source of the bad value.

### Design invariants

1. v0.9.3 remains Ollama-only.
2. No provider auto-detection from filesystem/home-directory/current-location content.
3. No LM Studio fallback or multi-provider behavior.
4. Explicit documented `-Provider ollama` should continue to work unless an intentional reviewed compatibility change is proven necessary.
5. Omitting `-Provider` must deterministically select Ollama and must not let unrelated positional/ambient output become Provider.

If the defect is caller argument construction, fix the caller.

If the defect is PowerShell positional/ambient binding through the installer parameter surface, harden the parameter contract minimally while preserving explicit `-Provider ollama` compatibility where possible. For example, evaluate named-only/positional-binding hardening only after RED proves that is the actual mechanism.

Do not add a provider resolver merely to sanitize arbitrary unrelated values into Ollama; reject invalid explicit input and eliminate unintended implicit input instead.

### Required post-repair command contracts

Both must behave deterministically in isolated non-mutating smoke tests:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

and the currently documented compatibility form:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace" -Provider ollama
```

Neither may depend on home-directory listing order, ambient pipeline output, current directory contents, or unrelated PowerShell provider values.

## Phase 4 — GREEN and focused regression validation

Run exact RED -> require GREEN.

Also validate at minimum:

1. PowerShell 5.1 parser/AST syntax;
2. installer parameter metadata/command-shape behavior;
3. omitted-Provider Task-116 shape in isolated non-mutating smoke;
4. explicit `-Provider ollama` compatibility shape;
5. the exact hostile/ambient/positional condition that reproduced Task 116 no longer injects `3D Objects`;
6. explicit invalid provider still fails closed rather than silently coercing;
7. Ollama-only invariant;
8. plugin lifecycle action resolver;
9. npm12 installer boundary;
10. interrupted-reentry/ownership semantic matrix;
11. fresh transaction rollback/recovery;
12. package installer still contains:

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

Require a **new** package-proof artifact; do not reuse Task-116 artifact `9687249771`.

Independently verify:

- outer artifact SHA256;
- inner ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- `PAYLOAD_IDENTITY.json` payload count/fingerprint;
- `SHA256SUMS.txt`;
- packaged installer has repaired binding behavior and intended compatibility contract;
- packaged installer still uses `openclaw plugins install $packagePath --force`;
- Task-113 conflicting-product rejection remains packaged;
- Task-112 active-wrapper proof remains packaged;
- Task-110 retired exactness remains packaged;
- recovery harness blob remains unchanged unless separately justified.

## Phase 7 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Report must include:

- exact root cause/data flow producing `3D Objects`;
- preserved Task-116 evidence used;
- RED commit/output;
- production repair commit/files;
- GREEN/targeted/full validation;
- exact candidate SHA;
- exact-SHA workflow run IDs/results;
- new artifact ID/hashes/identity;
- provider compatibility decision and documentation impact;
- candidate-to-report report-only proof;
- verdict `PASS`/`FAIL`/`BLOCKED`;
- remaining live work.

Then stop for independent ChatGPT review. Do not create or execute a lifecycle retry task automatically.

## Hard fence

Task 117 does **not** authorize:

- real Windows install-over against live workspace;
- reset/uninstall/fresh reinstall;
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
