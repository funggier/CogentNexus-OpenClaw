# CNX-20260828-118 — POSIX Installer Provider-Neutrality Alignment

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_TDD_REPAIR`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Complete the installer-subsystem responsibility boundary after Task 117 successfully made `scripts/install.ps1` provider-neutral but left `scripts/install.sh` provider-coupled.

This task is source/test/CI/package only. It does not authorize any live lifecycle mutation.

## Authoritative predecessor

Task-117 report:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Task-117 independent review:

`docs/operations/coordination/reviews/CNX-20260828-117-installer-provider-binding-origin-repair-review.md`

Review verdict:

`REJECTED FOR CANDIDATE ADVANCEMENT — WINDOWS POWERSHELL REPAIR IS VALID, BUT THE INSTALLER SUBSYSTEM IS NOT YET PROVIDER-NEUTRAL`

Accepted Task-117 facts:

- PowerShell installer provider-neutral repair is valid and must be preserved;
- Task-116 `3D Objects` failure surface is eliminated from `install.ps1`;
- exact Task-117 candidate `2a519904ce6f2ea22caa943529dc4710ccf7214c` passed its reported exact-SHA CI;
- no live mutation was replayed;
- candidate cannot advance because current `scripts/install.sh` still owns provider policy.

## Architectural invariant

**Every subsystem defines only information genuinely required to perform or verify that subsystem's own responsibility.**

For installation, provider name/model/endpoint/timeout/provider executable/provider selection are not installation-owned data unless a concrete installation-owned operation truly requires them.

The installer subsystem must therefore be consistent across platforms.

Provider-neutral installation does **not** imply that every provider is supported by runtime. Runtime/configuration modules remain free to enforce the currently supported provider policy where provider knowledge is actually required.

## Confirmed current POSIX coupling

At Task-117 candidate `2a519904ce6f2ea22caa943529dc4710ccf7214c`, `scripts/install.sh` contains:

- `PROVIDER="ollama"`;
- usage text with `--provider ollama`;
- `--provider` parser/validation;
- direct install prerequisite `ollama`;
- provider-specific install output;
- provider-specific migration/policy comments;
- final `enable --provider ollama` handoff.

Current test `tests/test_v091_install_wiring.py` explicitly asserts `PROVIDER="ollama"` remains in `install.sh`.

## Phase 0 — fresh repository reconciliation

Before implementation:

1. fetch current branch HEAD;
2. confirm Task 118 is active in both `ACTIVE.md` and `STATUS.md`;
3. confirm no newer authorization supersedes it;
4. compare from Task-117 report/review boundary to current HEAD;
5. ensure no unreviewed production edit has already altered `scripts/install.sh` provider ownership.

If unexpected source changes exist, stop for independent review.

## Phase 1 — TDD RED, tests only

No production edit before RED.

First implementation commit must change tests/diagnostic harnesses only and prove that the current POSIX installer violates the provider-neutral installer contract.

At minimum the RED must assert against real `scripts/install.sh` behavior/text that:

1. no `PROVIDER` variable/default exists;
2. no `--provider` install argument exists in usage or parser;
3. installer does not validate/select a provider;
4. installer does not require `ollama`, `lmstudio`, or another provider executable merely to install;
5. installer messages do not claim provider selection/Ollama-only installation;
6. installer lifecycle handoff does not pass `--provider`;
7. canonical POSIX install command is provider-free;
8. current tests no longer intentionally preserve POSIX provider coupling.

Run the focused test on unchanged production and capture exact failing output. Commit RED separately.

## Phase 2 — minimal production repair

After legitimate RED only:

1. remove `PROVIDER="ollama"` from `scripts/install.sh`;
2. remove `--provider` from usage/parser/validation;
3. remove provider executable prerequisite checks that installation itself does not need;
4. remove provider-specific install/start/success output and comments that assert installer-owned provider policy;
5. replace `enable --provider ollama` with generic `enable`;
6. update only current documentation/tests/workflows that describe or enforce POSIX installer provider coupling;
7. preserve the accepted Task-117 `scripts/install.ps1` provider-neutral implementation;
8. do not redesign `cnxclaw_v093.py`, provider modules, runtime selection, model behavior, endpoint behavior, fallback policy, or provider support unless a minimal interface correction is strictly required for generic installer handoff;
9. do not add provider auto-detection or a provider abstraction to the installer.

### Canonical POSIX installation shape

A canonical provider-free invocation should be equivalent to:

```sh
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

No provider argument exists at installation boundary.

## Phase 3 — GREEN and focused validation

Run exact RED -> require GREEN.

Also validate at minimum:

- shell syntax/parsing checks available in repository/CI;
- `install.sh` parameter/usage contract;
- provider-free generic lifecycle handoff;
- PowerShell Task-117 provider-neutral tests remain GREEN;
- current installer wiring tests no longer preserve POSIX provider policy;
- namespace/ownership semantic matrix;
- plugin lifecycle action resolver;
- npm12 installer boundary tests;
- fresh transaction/recovery tests where relevant;
- package installer contract remains intact.

No unrelated production refactor.

## Phase 4 — full repository validation

Require current-source success for the same stabilization gate used for Task 117:

- full `pytest` suite;
- Python `py_compile` set used by Validate;
- PowerShell installer AST validation;
- namespace isolation checker;
- shell/install smoke tests available in repository;
- `npm ci`;
- `npm test`;
- `npm run evaluation`;
- `npm audit --omit=dev`;
- `npm run plugin:validate`;
- `git diff --check`.

Record exact results/counts.

## Phase 5 — exact candidate CI/package proof

Freeze one exact repaired candidate SHA after production/test changes and before report-only commits.

Require all three authoritative workflows on that exact SHA:

1. Validate — success;
2. Windows Installer Pack Smoke — success;
3. PS5.1 Acceptance Smoke — success.

If repository has a POSIX-specific installer smoke/workflow relevant to the changed file, require it too.

Require a new package-proof artifact; do not reuse Task-117 artifact `9690067077`.

Independently verify:

- source identity/version;
- outer artifact SHA256;
- inner ZIP SHA256;
- tar.gz SHA256;
- payload identity/count/fingerprint;
- `SHA256SUMS.txt`;
- packaged `install.ps1` remains provider-neutral;
- packaged `install.sh` is provider-neutral;
- neither installer carries provider selection/default/validation/provider executable prerequisite/provider lifecycle argument;
- packaged installers retain supported plugin installation/ownership contracts;
- Task-113 conflict rejection, Task-112 active-wrapper proof, Task-110 retired exactness proof remain present;
- recovery harness is unchanged unless separately justified.

## Phase 6 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`

Report must include:

- RED commit + exact failing output;
- production repair commit/files;
- proof both Windows and POSIX installers now share provider-neutral responsibility boundary;
- focused/full validation;
- exact candidate SHA;
- exact-SHA workflow run IDs/results;
- new artifact ID/hashes/identity;
- candidate-to-report report-only proof;
- verdict `PASS`/`FAIL`/`BLOCKED`;
- remaining live work.

Then stop for independent ChatGPT review.

Do not create or execute a real-Windows lifecycle retry automatically.

## Hard fence

Task 118 does **not** authorize:

- live Windows install-over/reset/uninstall/reinstall;
- live POSIX installation on user machines;
- Task-116 destructive command replay;
- live stop/start/restart/recovery-reality harness;
- manual cleanup/normalization of live residue;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/stop/reconfigure;
- provider/model/endpoint/timeout changes;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/tokens/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot/process-tree kill;
- merge/tag/GitHub Release/force push.
