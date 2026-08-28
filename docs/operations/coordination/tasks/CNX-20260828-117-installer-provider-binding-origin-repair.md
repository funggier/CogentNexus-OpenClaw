# CNX-20260828-117 — Provider-Neutral Installer Boundary Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_TDD_REPAIR`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the installer failure exposed by Task 116 and establish a cleaner architectural boundary: **the installer must not define, select, validate, default, infer, or otherwise own provider policy unless provider knowledge is genuinely required to perform installation itself.**

Task 116 failed before installer-body execution because PowerShell bound the unrelated value `3D Objects` to the installer's `Provider` parameter and rejected it against `ValidateSet("ollama")`.

The stronger design decision for Task 117 is therefore not merely to patch that binding symptom. The installer must become **provider-neutral**.

This does not mean every provider is supported by the current runtime. It means provider support/policy belongs to the runtime/configuration layer where that information is actually required, rather than to installation.

Task 117 is source/test/CI/package only. No live lifecycle mutation is authorized.

## Authoritative Task-116 evidence

Task-116 report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Accepted live facts:

- Phase 0 PASS;
- OpenClaw exactly `2026.7.1-2`;
- the live runtime's selected provider was Ollama and healthy;
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

## Core architectural invariant — responsibility-local data

**Every subsystem should define only information that is actually necessary for that subsystem's own responsibility.**

Do not carry a value through a layer merely because another layer eventually needs it.

For any candidate field/parameter/default/configuration, ask:

1. Does this layer need the value to perform its own operation?
2. Does this layer need the value to verify its own postcondition?
3. Is this layer the authority that owns the decision represented by the value?

If the answer to all three is no, the value should not exist in that layer.

### Examples

Installer legitimately owns installation concerns such as:

- workspace path;
- package/source identity;
- ownership boundaries;
- transaction/recovery metadata;
- installable skill/plugin/runtime/launcher/state paths;
- generic tool prerequisites actually used by installation;
- generic installation postconditions.

Installer should not own merely because runtime uses them later:

- provider name;
- provider executable;
- provider model;
- provider endpoint;
- provider timeout;
- provider fallback order;
- provider-specific lifecycle policy.

This principle should be applied to future stabilization work beyond provider handling as well: remove unnecessary cross-layer knowledge rather than adding defaults/validation for data a layer does not need.

## Independently confirmed provider coupling in frozen installer

Frozen `scripts/install.ps1` currently contains provider-specific responsibilities that are not intrinsic to installation:

1. `[ValidateSet("ollama")] [string]$Provider = "ollama"`;
2. `Write-Host "Provider: ollama"`;
3. `Require-Command ollama`;
4. final activation via `enable --provider ollama`;
5. provider-specific completion/help wording such as `Ollama-only` and `v0.9.3 will use Ollama`.

Current installation documentation also instructs callers to pass `-Provider ollama`.

Task 117 intentionally retires this installer-level provider API.

## Required boundary after Task 117

The installer must:

- classify ownership safely;
- install/upgrade skill/plugin/runtime/launcher/state;
- preserve external/runtime configuration unless installation explicitly owns a field;
- call generic runtime lifecycle entry points when required;
- verify installation-specific postconditions.

The installer must **not**:

- accept `-Provider`;
- contain a provider `ValidateSet`;
- define a provider default;
- auto-detect/infer provider;
- read provider from filesystem/current directory/pipeline/environment merely to install;
- require `ollama`, `lmstudio`, or another provider binary merely because runtime may use it;
- pass `--provider ...` to lifecycle commands;
- claim installation success for a specific provider;
- add provider fallback/coercion logic.

Provider/runtime modules may remain provider-aware where provider knowledge is genuinely required. Task 117 does not redesign runtime provider policy except where a minimal generic handoff is required to decouple installer.

For example, if `cnxclaw enable` owns provider policy internally, installer should call generic `enable`, not `enable --provider ollama`.

## Phase 0 — fresh repository reconciliation

Before implementation:

1. fetch current branch HEAD;
2. confirm Task 117 is active in both `ACTIVE.md` and `STATUS.md`;
3. confirm no newer authorization supersedes it;
4. compare from Task-116 report/review boundary to current HEAD;
5. ensure no unreviewed production repair already landed.

If unexpected source changes exist, stop for review.

## Phase 1 — complete root-cause trace, read-only

The architectural repair removes the faulty installer input surface, but the Task-116 `3D Objects` value must still be traced as far as preserved evidence permits.

Read-only inspect:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\20260828-210020`

Determine whether `3D Objects` originated from:

- caller argument construction/splatting;
- an extra positional token;
- `$PSDefaultParameterValues` or ambient PowerShell binding state;
- wrapper/helper value resolution;
- pipeline/enumeration output;
- another concrete evidenced source.

Record the deepest proven data flow. If evidence cannot establish the origin completely, state exactly where provenance ends rather than inventing a root cause.

No live mutation is authorized during diagnosis.

## Phase 2 — TDD RED, tests only

**No production edit before semantic RED.**

The first implementation commit must change tests/diagnostic harnesses only.

RED must encode the provider-neutral installer contract and fail on current production.

At minimum assert against real installer AST/text/isolated command metadata that:

1. installer parameter list contains no `Provider`;
2. installer contains no provider `ValidateSet`;
3. installer defines no provider default;
4. installer does not directly require `ollama`, `lmstudio`, or another provider executable as an installation prerequisite;
5. installer does not pass `--provider` to `enable`, start, restart, reset, or another lifecycle command;
6. installer installation/completion messages do not assert a provider selection;
7. canonical installation documentation/examples contain no `-Provider` argument;
8. canonical Task-116 install command is provider-free;
9. unrelated ambient/positional values cannot become a provider because no installer provider parameter exists.

The RED must fail because production still violates these boundaries, not because of malformed test setup.

Commit RED separately and record exact failing output.

## Phase 3 — minimal production repair

After legitimate RED only:

1. remove `Provider` from `scripts/install.ps1` parameters;
2. remove provider `ValidateSet` and provider default;
3. remove provider-specific installation output;
4. remove direct provider executable prerequisite checks unless installer actually invokes that provider executable for an installation-owned operation;
5. replace provider-specific lifecycle invocation with a generic lifecycle handoff, e.g. `enable` without `--provider` when runtime owns that choice;
6. update canonical installation documentation/examples to remove `-Provider`;
7. update installer-focused tests/smokes/workflows that pass `-Provider`;
8. preserve runtime provider policy in the runtime layer unless a minimal generic interface change is required for the handoff;
9. do not add provider auto-detection, fallback, coercion, or a replacement provider abstraction to the installer.

### Canonical install command

The canonical install/install-over shape becomes:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No provider argument exists.

## Phase 4 — GREEN and focused regression validation

Run the exact RED test and require GREEN.

Also validate at minimum:

1. PowerShell 5.1 parser/AST syntax;
2. installer parameter metadata contains only installation-relevant parameters;
3. provider-free Task-116 command shape in isolated non-mutating smoke;
4. hostile ambient/positional values cannot bind as Provider because no Provider parameter exists;
5. installer does not require an Ollama/LM Studio executable merely to bind/start installation;
6. generic post-install lifecycle handoff uses no provider argument;
7. runtime/provider tests continue to prove provider behavior where runtime genuinely owns it;
8. plugin lifecycle action resolver;
9. npm12 installer boundary;
10. interrupted-reentry/ownership semantic matrix;
11. fresh transaction rollback/recovery suites;
12. package installer still contains the supported local package invocation:

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
- packaged installer contains no provider parameter/default/ValidateSet/provider-specific prerequisite/provider-specific lifecycle argument;
- packaged installation docs contain provider-free command shape;
- packaged installer still uses `openclaw plugins install $packagePath --force`;
- Task-113 conflicting-product rejection remains packaged;
- Task-112 active-wrapper proof remains packaged;
- Task-110 retired exactness proof remains packaged;
- recovery harness blob remains unchanged unless separately justified.

## Phase 7 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Report must include:

- deepest proven Task-116 `3D Objects` data-flow origin;
- preserved Task-116 evidence used;
- RED commit and exact failing output;
- production repair commit and changed files;
- provider-neutral installer boundary proof;
- any runtime handoff change and why that layer owns provider policy;
- GREEN/targeted/full validation;
- exact candidate SHA;
- exact-SHA workflow run IDs/results;
- new artifact ID/hashes/identity;
- documentation changes;
- candidate-to-report report-only proof;
- verdict `PASS`/`FAIL`/`BLOCKED`;
- remaining live work.

Then stop for independent ChatGPT review. Do not create or execute a new lifecycle retry task automatically.

## Hard fence

Task 117 does **not** authorize:

- real Windows install-over against live workspace;
- reset/uninstall/fresh reinstall;
- live stop/start/restart;
- recovery-reality disruptive harness;
- manual cleanup/normalization of Task-107/116 residue;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- Ollama/LM Studio update/reinstall/stop/reconfigure;
- provider/model/endpoint/timeout changes on the live machine;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/tokens/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot or generic process-tree kill;
- merge/tag/GitHub Release/force push.

Read-only inspection of preserved Task-116 evidence and isolated Windows diagnostic reproduction is authorized.
