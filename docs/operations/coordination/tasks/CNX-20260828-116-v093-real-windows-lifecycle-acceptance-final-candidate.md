# CNX-20260828-116 — v0.9.3 Real-Windows Lifecycle Acceptance on Reviewed Final Candidate

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Perform the first real-Windows lifecycle acceptance after repository/source/test/CI/package stabilization passed independent review.

This task is deliberately **read-only first**. The historical Task-107 machine state is not assumed to still exist. No mutation is authorized until the current machine is freshly proven coherent and safely attributable to a supported Task-107-style interrupted rollover or another exact state that the reviewed installer can classify without generic adoption or cleanup.

## Frozen reviewed candidate

Use exactly:

- Source candidate: `47b069daed90f54feae2c9eb26f38c438493f3c8`
- Version: `0.9.3`
- Package-proof artifact ID: `9687249771`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-47b069daed90f54feae2c9eb26f38c438493f3c8`
- Outer artifact SHA256: `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`
- Inner ZIP SHA256: `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`
- tar.gz SHA256: `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Recovery harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Recovery harness Git blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

Task-115 independent review:

`docs/operations/coordination/reviews/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening-review.md`

Review verdict:

`ACCEPTED PASS — SEMANTIC MATRIX COMPLETE; EXACT CANDIDATE MAY ADVANCE TO A SEPARATE READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE TASK`

Do not substitute a newer branch HEAD, another artifact, another package build, or a locally repacked archive.

## Historical context — evidence only, not an assumption

Task 107 last observed after its one failed install-over:

- CNX mode `passthrough`, generation `25`;
- OpenClaw exactly `2026.7.1-2`;
- selected provider Ollama, healthy/ready;
- Gateway healthy on loopback;
- recovery READY for passthrough;
- delivery no pending terminal deliveries;
- SQLite integrity `ok`;
- Supervisor absent;
- supported OpenClaw plugin install had placed the active replacement at `~\.openclaw\extensions\cogentnexus-openclaw`;
- old manifest-owned npm-generation plugin path had been removed;
- ownership manifest still referenced that retired path;
- installer backup/staging residue was retained.

Tasks 108-115 did not authorize live mutation. Nevertheless, Phase 0 must re-prove the machine now.

## Global safety invariant

Once mutation begins:

- each destructive lifecycle phase is single-attempt;
- stop immediately on the first non-zero root exit code, contradictory evidence, ambiguous ownership state, unexpected external dependency mutation, or loss of health that is outside the phase's expected transition;
- do not rerun the failed destructive command;
- do not manually delete, rename, edit, normalize, repair, or rebaseline live state;
- collect read-only post-failure evidence and publish `FAIL`/`BLOCKED`.

No success may be inferred from terminal state alone; verify durable state, ownership, validators, process/service state, and artifacts after each phase.

## Phase 0 — fresh provenance and read-only machine reconciliation

### 0A. Repository/provenance

Before touching the live machine:

1. fetch current remote coordination branch;
2. confirm Task 116 is active in both `ACTIVE.md` and `STATUS.md`;
3. confirm no later coordination change revoked or replaced this task;
4. obtain a detached/read-only checkout of exact source `47b069daed90f54feae2c9eb26f38c438493f3c8` in an external temporary/evidence location;
5. verify `git rev-parse HEAD` equals the pinned SHA;
6. verify Git blob of `scripts/test-v093-ollama-recovery-windows-v3.ps1` equals `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`;
7. download artifact `9687249771` freshly from GitHub Actions;
8. verify outer/inner archive SHA256, package identity source/version, payload count/fingerprint, and `SHA256SUMS.txt` before extraction/use;
9. verify packaged installer still contains exactly `openclaw plugins install $packagePath --force` for actual installation and not the superseded `npm-pack:` invocation.

If any provenance check differs: `BLOCKED`; no live mutation.

### 0B. External evidence root

Create a new Task-116 evidence directory outside all owned installation paths, for example under:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\<UTC-stamp>`

Record every command, root exit code, stdout/stderr, relevant file hashes/listings, and before/after observations there. Do not store credentials/tokens/passwords.

### 0C. Tool/version baseline

Read-only capture:

- Windows version;
- PowerShell version;
- Node version;
- npm version;
- Python version;
- `openclaw --version`;
- `ollama --version`.

Required OpenClaw baseline remains exactly `2026.7.1-2`. If OpenClaw differs, stop `BLOCKED`; do not update/downgrade/rebaseline it in this task.

Ollama must remain the selected managed provider. Record its current version; do not update it.

### 0D. CNX/OpenClaw/provider health

From the live workspace, capture read-only results and root exit codes for at least:

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider status
.\cnxclaw.cmd check openclaw
.\cnxclaw.cmd check gateway
.\cnxclaw.cmd check recovery
.\cnxclaw.cmd check delivery
.\cnxclaw.cmd check resources
openclaw gateway status
ollama ps
```

Also capture the loopback Gateway listener/owning process without killing anything.

### 0E. Durable database and service state

Read-only:

- locate the active CogentNexus SQLite DB through the product's own configured/known state path;
- execute SQLite `PRAGMA integrity_check` read-only and require `ok`;
- record relevant CNX mode/generation/desired-provider state;
- query the CogentNexus/OpenClaw Supervisor/Scheduled Task state without creating/deleting/changing it;
- record whether a supervisor task is absent/present and its exact registration if present.

### 0F. Ownership/product inventory and interrupted-reentry classification

Using the **pinned candidate's** read-only ownership code, capture exact current filesystem/product evidence before installer mutation:

- ownership manifest bytes + SHA256 if present;
- manifest `pluginPath` and whether it exists;
- canonical direct extension presence and plugin fingerprint;
- npm project/product wrapper/package evidence;
- legacy namespace evidence;
- skill/launcher/state-root existence;
- controller mode;
- OpenClaw active plugin registration/inventory for CogentNexus;
- any installer transaction/rollover marker or backup/staging residue.

Capture the current OpenClaw plugin inventory in JSON using the same supported OpenClaw interface/shape consumed by the installer; do not fabricate inventory records.

Then run the candidate's `namespace_ownership.py classify-install` read-only with:

- live workspace;
- live application-data path;
- captured real OpenClaw plugin inventory JSON;
- expected replacement fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

The classification itself must not mutate state.

### Phase-0 mutation gate

Proceed to Phase 1 only if all evidence is coherent and one supported path is proven.

For the historical Task-107-shaped interrupted re-entry, expected classification is:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": true,
  "interruptedRolloverReentry": true
}
```

and the replacement must be exactly the canonical direct extension, with the missing retired manifest path bound as expected and no additional conflicting CogentNexus storage/legacy evidence.

A different state may proceed only if the candidate's exact classifier/ownership checks prove it unambiguously safe without adoption or cleanup and the installer action is understood. If evidence is surprising, contradictory, or classification fails: stop `BLOCKED` and report. Do not improvise.

## Phase 1 — preserve pre-mutation evidence

Before the first live mutation:

1. copy/hash the ownership manifest and any installer transaction/rollover metadata into the external evidence root;
2. record product inventory and relevant owned-path tree hashes/listings;
3. record external OpenClaw/Ollama/Gateway baseline state;
4. record SQLite integrity and relevant DB/state hashes where safe and meaningful;
5. never back up secrets into the report/repository.

This evidence is for proof/diagnosis only; do not use it to manually restore/normalize the live installation during this task.

## Phase 2 — install-over once using exact reviewed package

Run the extracted pinned package installer exactly once against the live workspace:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

Use the normal/native Node/npm path; do not switch package managers or introduce alternate OpenClaw installations.

### Expected Task-107 re-entry behavior

If Phase 0 proved the historical direct-extension interrupted-reentry shape:

- classification must select `pluginAlreadyExact=true`;
- installer action must not execute a second external `openclaw plugins install` for the already-exact active replacement;
- installer must converge ownership through the supported resolve/create/verify path;
- no foreign/shared wrapper or unrelated user-owned data may be adopted/deleted;
- CNX may transition as required by the normal installer but external OpenClaw/Ollama versions/configuration must remain preserved.

Require root exit code `0`.

On non-zero/ambiguity: stop immediately. Do not rerun install-over.

### Phase-2 postconditions

Read-only verify at minimum:

- `cnxclaw status` coherent;
- ownership manifest verifies with candidate ownership script;
- exactly one accepted active plugin payload and registration;
- no conflicting CogentNexus product evidence;
- OpenClaw still exactly `2026.7.1-2`;
- Ollama/provider remains selected and healthy;
- Gateway health as expected;
- SQLite integrity `ok`;
- no unexpected user-owned deletion or external package mutation.

## Phase 3 — `cnxclaw reset` acceptance

Execute reset once and explicitly provide the required `y` confirmation through the command's normal confirmation interface. Do not bypass the confirmation contract in production code.

Verify reset semantics:

- product state/configuration is returned to fresh-install defaults as designed;
- external OpenClaw remains installed and at exact baseline version;
- Ollama remains installed and untouched;
- user credentials/secrets are not exposed in evidence;
- ownership remains coherent for the installed product;
- SQLite/state reset behavior matches documented contract;
- status/check commands and SQLite integrity pass.

Any non-zero/ambiguous result -> stop; do not retry reset.

## Phase 4 — `cnxclaw uninstall` acceptance

Execute uninstall once and explicitly provide `y` confirmation through the normal command interface.

Verify clean product removal without collateral damage:

- CogentNexus owned state/skill/launcher/plugin ownership is removed according to contract;
- product-owned application data targeted by uninstall is removed according to contract;
- no generic/legacy/unrelated user-owned paths are removed;
- OpenClaw remains installed at `2026.7.1-2`;
- OpenClaw non-CogentNexus configuration/plugins remain preserved;
- Ollama remains installed/healthy;
- no CogentNexus task/service/ownership residue remains except external Task-116 evidence and deliberately retained package/source evidence outside owned paths.

If uninstallation leaves ambiguous owned residue or returns non-zero, stop. Do not manually clean it.

## Phase 5 — fresh reinstall from the same exact artifact

From the same hash-verified extracted artifact used above, run the installer once against the same workspace.

Require:

- clean fresh-install classification/transaction path;
- root exit code `0`;
- coherent ownership manifest and exact plugin payload;
- normal `cnxclaw` launcher/skill/state creation;
- OpenClaw version unchanged;
- Ollama/provider preserved;
- SQLite integrity `ok`;
- no unexpected legacy/shared-product evidence.

Do not use another build or artifact.

## Phase 6 — normal lifecycle commands

Exercise normal lifecycle commands one time each with postcondition checks:

1. `cnxclaw stop`
2. `cnxclaw start`
3. `cnxclaw restart`

For each command:

- capture root exit code/output;
- verify CNX desired/actual state and Gateway/provider behavior expected by the command;
- ensure intentional stop is not immediately countermanded by recovery logic;
- ensure start/restart converges without duplicate authorities/processes;
- preserve OpenClaw/Ollama versions and provider selection;
- verify recovery/delivery/SQLite health after convergence.

Stop on first non-zero/ambiguous result; no command replay.

## Phase 7 — recovery reality harness once

Run the reviewed recovery harness from the exact detached candidate once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Use the harness defaults unless a documented machine-safe reason requires changing only its observation/fuse timing. Do not edit the harness.

The harness may perform its explicitly designed gateway/provider crash and operator-stop scenarios. Those are the only destructive process actions authorized here.

Require an overall PASS/result proving:

- baseline health;
- Gateway crash recovery;
- managed Ollama/provider recovery;
- intentional operator stop remains respected;
- one recovery authority, bounded convergence, and no uncontrolled hot loop;
- external OpenClaw/Ollama remain preserved.

Do not run the harness twice after failure.

## Phase 8 — final read-only acceptance snapshot

After all lifecycle/recovery phases pass, capture fresh:

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider status
.\cnxclaw.cmd check openclaw
.\cnxclaw.cmd check gateway
.\cnxclaw.cmd check recovery
.\cnxclaw.cmd check delivery
.\cnxclaw.cmd check resources
openclaw gateway status
ollama ps
```

Also require:

- ownership manifest verification PASS;
- exact plugin payload/fingerprint and unique registration;
- SQLite `PRAGMA integrity_check = ok`;
- expected Supervisor/task state;
- OpenClaw exactly `2026.7.1-2`;
- no unexpected CogentNexus legacy/conflicting product evidence;
- final CNX mode/state coherent for normal installed operation.

## Dashboard semantic-delivery fence

**Do not send any new Dashboard semantic message/nonce in Task 116.**

Task 116 ends after lifecycle/recovery acceptance and reporting. The final durable-delivery semantic Dashboard test must be a separate later task so a lifecycle failure cannot be obscured by a new user-visible side effect.

## Failure handling

For any failure after mutation begins:

1. stop at the failing phase;
2. do not replay the failed external side effect;
3. do not manually repair/normalize/delete live state;
4. gather only read-only post-failure status/ownership/product inventory/provider/Gateway/SQLite/process/service evidence;
5. preserve external evidence;
6. publish `FAIL` or `BLOCKED` with exact phase, command, exit code, and live boundary.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Report must include:

- exact source/artifact/hashes/harness blob;
- exact Phase-0 live state and classification;
- every root command/exit code by phase;
- install-over outcome and whether redundant external plugin installation was avoided;
- reset/uninstall/fresh-reinstall results;
- stop/start/restart results;
- recovery-harness result/evidence paths;
- OpenClaw/Ollama preservation proof;
- ownership/product inventory and SQLite integrity before/after;
- exact final machine boundary;
- `PASS`, `FAIL`, or `BLOCKED`;
- explicit statement that no Dashboard semantic Send occurred.

After publishing the report, stop for independent ChatGPT review. Do not open or execute the final Dashboard semantic-delivery task yourself.

## Hard fence — not authorized

Task 116 does **not** authorize:

- OpenClaw update/downgrade/reinstall/uninstall;
- Ollama update/reinstall/uninstall except the harness's managed provider stop/crash/recovery behavior specifically under test;
- provider/model changes or fallback to another provider;
- timeout/model/config tuning;
- LM Studio management;
- credential/token/password access or re-entry;
- manual SQLite edits;
- manual ownership/manifest/plugin/config normalization;
- generic process-tree kills outside the exact recovery harness;
- reboot;
- force push, merge, tag, or GitHub Release;
- Dashboard semantic nonce/message/Send;
- repeated destructive commands after a failed attempt.

If safe state cannot be proven, stop `BLOCKED` rather than weakening the boundary.
