# CNX-20260828-119 — Installer Documentation Authority Alignment

- Status: `READY_FOR_HERMES`
- Execution mode: `DOCS_TEST_CONTRACT_REPAIR`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Align the canonical user-facing installation documentation and its automated contract tests with the provider-neutral installer implementation accepted from Tasks 117 and 118.

This is not a new installer-source repair unless a fresh test demonstrates a real implementation defect. The current implementation already has provider-neutral PowerShell and POSIX installer entry points.

## Accepted implementation boundary

Exact Task-118 candidate source:

`9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`

Accepted implementation facts:

- `scripts/install.ps1` has no Provider parameter/default/ValidateSet;
- `scripts/install.sh` has no provider variable/default or `--provider` API;
- neither installer directly requires Ollama/LM Studio merely to install;
- neither installer passes a provider argument in its generic runtime `enable` handoff;
- runtime/provider policy remains provider-aware where runtime actually owns that decision;
- this does not broaden current runtime provider support.

## Independent-review blocker

Task-118 review found that canonical docs still mix installation and runtime responsibilities:

- `docs/INSTALL.md` and `docs/INSTALL.th.md` list Ollama as a general installation requirement;
- they describe installer behavior as including provider preflight;
- canonical POSIX installation command is absent from user-facing installation documentation;
- the Task-118 POSIX command test was changed to read a coordination task document rather than canonical installation docs.

A coordination task is not consumer-facing command authority.

## Architectural invariant

**Every subsystem defines only information required to perform or verify its own responsibility.**

Documentation must preserve this distinction too.

### Installer-owned concerns

Examples:

- workspace path;
- source/package identity;
- ownership/classification;
- transaction/recovery metadata;
- skill/plugin/runtime/launcher/state installation;
- tools actually invoked by installation itself;
- generic installation postconditions.

### Runtime/provider-owned concerns

Examples:

- supported provider set;
- provider executable/runtime availability;
- provider endpoint/model/timeout;
- provider health/readiness;
- provider-specific lifecycle behavior.

Current v0.9.3 runtime may remain documented as Ollama-only where runtime support/readiness is being described. That must not be phrased as an installer input/default/dependency when installation itself does not own it.

## Phase 0 — fresh reconcile

Before edits:

1. fetch current branch HEAD;
2. confirm Task 119 is active in `ACTIVE.md` and `STATUS.md`;
3. confirm no newer task superseded this authorization;
4. confirm no unreviewed installer source change landed after Task 118;
5. preserve Task-116 live state untouched.

## Phase 1 — tests-only RED

First implementation commit must be tests-only.

Create/adjust contract tests against canonical user-facing docs (`docs/INSTALL.md` and `docs/INSTALL.th.md`), not coordination task/report/review files.

RED must fail on the current candidate because documentation still violates the intended contract.

At minimum assert:

1. PowerShell canonical source-install command is provider-free;
2. POSIX canonical source-install command is present and provider-free;
3. canonical install docs do not instruct users to pass installer-level `-Provider`/`--provider`;
4. installer prerequisites are separated from runtime/provider readiness requirements;
5. installer behavior text does not claim provider selection or provider-specific preflight as installer-owned work;
6. current runtime provider support may still be documented in a runtime/post-install section;
7. tests do not use `docs/operations/coordination/tasks/*` as permanent public-install command authority.

Record exact RED output and commit SHA.

## Phase 2 — minimal docs/contract repair

After legitimate RED only:

- update `docs/INSTALL.md`;
- update `docs/INSTALL.th.md`;
- update only closely related current guidance if required for consistency;
- keep historical reports/reviews historical;
- preserve accurate current runtime provider support statements, but move them to runtime/readiness context;
- add canonical POSIX source-install example;
- do not reintroduce provider arguments into either installer command;
- do not change installer source unless tests reveal an implementation defect not already known.

Preferred documentation structure:

- Installation prerequisites;
- Windows source installation;
- POSIX source installation;
- What the installer owns/does;
- Runtime readiness/current provider support;
- Post-install checks;
- lifecycle/reset/uninstall.

## Phase 3 — GREEN and focused validation

Require exact RED suite GREEN.

Also verify:

- provider-neutral installer boundary tests for both PowerShell and POSIX;
- installer wiring/order tests;
- namespace isolation tests;
- current documentation command examples against real command surfaces where practical;
- no stale `-Provider`/`--provider` installer examples remain in current user-facing guidance;
- `git diff --check`.

Do not rewrite historical release notes/reports merely because they contain old commands in historical context.

## Phase 4 — full repository validation

Run the full validation set used by the current candidate, including:

- full `pytest` suite;
- Python compile validation;
- PowerShell installer AST validation;
- POSIX `sh -n scripts/install.sh`;
- namespace isolation checker;
- `npm ci`;
- `npm test`;
- `npm run evaluation`;
- `npm audit --omit=dev`;
- `npm run plugin:validate`;
- `git diff --check`.

Record exact counts/results.

## Phase 5 — exact candidate CI/package proof

Freeze one exact candidate SHA after docs/tests alignment and before report-only commits.

Require all three workflows on the same exact SHA:

1. Validate — success;
2. Windows Installer Pack Smoke — success;
3. PS5.1 Acceptance Smoke — success.

Require a new package-proof artifact for that exact candidate. Record:

- artifact ID/name;
- source SHA;
- package version;
- outer/package hashes;
- ZIP/tar.gz hashes;
- payload count/fingerprint;
- package/payload identity agreement.

Verify packaged current installation docs carry both provider-neutral Windows and POSIX command contracts if those docs are package contents.

## Phase 6 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

Report must include:

- RED commit/output;
- docs/test repair commit(s);
- changed files;
- exact canonical Windows/POSIX commands;
- installer-vs-runtime responsibility wording decision;
- GREEN/focused/full validation;
- exact candidate SHA;
- exact-SHA workflow run IDs/results;
- new artifact identity/hashes;
- candidate-to-report report-only proof;
- verdict `PASS`/`FAIL`/`BLOCKED`;
- remaining live work.

Then stop for independent ChatGPT review.

## Hard fence

Task 119 does **not** authorize:

- live install-over/reset/uninstall/reinstall;
- live POSIX installation;
- Task-116 destructive replay;
- live stop/start/restart/recovery harness;
- manual cleanup/normalization;
- OpenClaw/provider-runtime changes;
- provider/model/endpoint/timeout changes;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/secrets access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/GitHub Release/force push.
