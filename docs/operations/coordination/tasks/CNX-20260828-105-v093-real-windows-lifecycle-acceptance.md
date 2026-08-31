# CNX-20260828-105 — v0.9.3 Real-Windows Lifecycle Acceptance

**Status:** `READY_FOR_HERMES`  
**Execution mode:** `MANUAL`  
**Owner / reviewer:** ChatGPT  
**Executor:** Hermes/Codex  
**Branch:** `agent/v0.9.3-full-stabilization`  
**Pinned acceptance source:** `c4d37b0005afeffcd183848dfce5476cbe2b85cd`

## Purpose

Prove the real Windows consumer lifecycle for the exact CogentNexus-OpenClaw v0.9.3 acceptance snapshot after repository/package stabilization and the explicit OpenClaw security exception recorded in D-012.

This task is intentionally bounded to lifecycle and recovery acceptance:

`preflight/provenance -> install-over -> reset -> uninstall -> fresh reinstall -> normal lifecycle -> disruptive recovery -> report`

Do **not** perform a new Dashboard semantic nonce/Send in this task. Final semantic durable-delivery acceptance is reserved for a separately reviewed follow-up task.

## Exact acceptance identity

The runtime artifact for this task is immutable as evidence even though the development branch may continue moving.

- source commit: `c4d37b0005afeffcd183848dfce5476cbe2b85cd`
- CogentNexus-OpenClaw version: `0.9.3`
- OpenClaw operational baseline: `2026.7.1-2`
- managed provider: `Ollama only`
- payload-v2 file count: `178`
- payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- package tar.gz SHA256: `c022a5225703311607a2b69a00cdeb3462a0449fd4995d558f67fc99d3d5e625`
- package ZIP SHA256: `c6151fac1cc3b5cd37a2d82aa366bb547adff1f885b9d2b33209c83601606133`
- Validate workflow run: `33128487849` — SUCCESS, package + 6/6 matrix
- PS5.1 Acceptance Smoke run: `33128487814` — SUCCESS
- Windows Installer Pack Smoke run: `33128487825` — SUCCESS
- package-proof Actions artifact ID: `9669312785`
- package-proof artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-c4d37b0005afeffcd183848dfce5476cbe2b85cd`
- package-proof outer artifact digest: `sha256:7e42f79da070bdcfb5f18d2f7f1fbbdb6e21f810915b5bfd84f4b84652d49d44`

Coordination commits created after this task is published will advance the branch. They do **not** change the acceptance target above. Do not install branch HEAD merely because it is newer.

## Non-negotiable artifact rule

Use the exact CI package-proof artifact identified above.

1. Download Actions artifact ID `9669312785` using an authenticated GitHub mechanism available to the executor.
2. Locate the inner `cogentnexus-openclaw-v0.9.3.zip` produced by the package job.
3. Verify its SHA256 is exactly `c6151fac1cc3b5cd37a2d82aa366bb547adff1f885b9d2b33209c83601606133` before extraction or installation.
4. Use a detached checkout/worktree of exact source commit `c4d37b0005afeffcd183848dfce5476cbe2b85cd` for source-side harnesses and provenance.
5. Do not rebuild a replacement package locally and treat it as the accepted artifact.

If exact artifact/source identity cannot be established, publish a `BLOCKED` report and stop without live mutation.

## Evidence root

Create a new timestamped evidence directory outside both the normal workspace and the CogentNexus-OpenClaw runtime root, for example:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-105\<timestamp>`

Keep detailed local evidence there. The GitHub report may reference paths, hashes, exit codes, and redacted metadata, but must not publish secrets, credentials, tokens, passwords, private session payloads, or unredacted configuration values.

## Global execution rules

- Execute phases in order.
- Every destructive or externally visible lifecycle operation is single-attempt unless the command itself provides a documented internal recovery path.
- If a phase fails or becomes ambiguous, stop the task, preserve evidence, and report `FAIL` or `BLOCKED`. Do not replay side effects merely to obtain a cleaner result.
- Do not patch source/runtime behavior in this task. A discovered product defect becomes a separate TDD repair task after review.
- Preserve externally owned OpenClaw and Ollama installations and user data.
- No LM Studio management or testing.
- Do not expose or request credentials.

## Phase 0 — Exact provenance and read-only live preflight

Before any mutation:

1. Establish a detached source checkout/worktree at exact commit `c4d37b0005afeffcd183848dfce5476cbe2b85cd`.
2. Record the exact source SHA and verify the recovery harness at `scripts/test-v093-ollama-recovery-windows-v3.ps1` comes from that source. Expected Git blob SHA: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.
3. Download and verify the exact CI artifact as required above.
4. Record installed/runtime tool versions needed for the proof, including OpenClaw and Ollama. OpenClaw must be exactly `2026.7.1-2` for this acceptance run.
5. Read the current installed CogentNexus-OpenClaw launcher/status/ownership/plugin state without mutation.
6. Capture appropriate read-only checks, including where available:
   - `cnxclaw.cmd status`
   - `cnxclaw.cmd provider status`
   - `cnxclaw.cmd check openclaw`
   - `cnxclaw.cmd check gateway`
   - `cnxclaw.cmd check recovery`
   - `cnxclaw.cmd check delivery`
   - `cnxclaw.cmd check resources`
7. Confirm that the existing deployment is coherent enough to support an install-over proof. If it is absent, partial, mixed, ambiguous, or ownership cannot be proven, do not improvise a destructive cleanup. Report `BLOCKED` with the read-only evidence and stop.

## Phase 1 — External evidence/backup boundary

Before install-over mutation:

- finish the external evidence root;
- capture hashes/listings/state needed to prove what changed;
- preserve any backup required by the documented installer/lifecycle process outside CogentNexus-OpenClaw-owned paths;
- keep all sensitive configuration content local and redacted from the report.

This phase does not authorize arbitrary copying of private OpenClaw/session data into the repository.

## Phase 2 — Install-over proof

Using the exact verified candidate archive:

1. Extract/stage it in an external temporary/evidence location.
2. Run that candidate's normal Windows installer path (`scripts\install.ps1`) exactly once against the existing coherent deployment. Do not manually copy plugin/runtime/config files around the installer transaction.
3. Record the root process exit code and installer evidence.
4. Require successful convergence to v0.9.3 with namespace ownership intact.
5. Verify after install-over:
   - installed CogentNexus-OpenClaw version/identity is the accepted candidate;
   - ownership manifest/plugin identity is coherent;
   - state is `MANAGED` with Ollama;
   - Gateway is healthy;
   - Ollama/provider is healthy;
   - recovery verdict is `READY`;
   - no LM Studio managed path is introduced.

If install-over fails or leaves ambiguous state, stop and report. Do not rerun the installer to hide the first result.

## Phase 3 — Reset proof

From the installed candidate:

1. Run `cnxclaw.cmd reset` once.
2. Supply the command's required exact lowercase `y` confirmation once through a controlled interactive/stdin path.
3. Record the exit code and evidence.
4. Verify that CogentNexus-OpenClaw runtime state is recreated as a fresh managed v0.9.3 installation while external OpenClaw and Ollama remain installed/preserved.
5. Require final `MANAGED` / Ollama state, healthy Gateway/provider, coherent ownership/plugin identity, and recovery `READY`.

If reset fails, stop. Do not issue a second reset.

## Phase 4 — Uninstall proof

1. Run `cnxclaw.cmd uninstall` once.
2. Supply the required exact lowercase `y` confirmation once.
3. Record exit code and all evidence paths.
4. Allow a bounded observation period for the documented delayed Windows self-cleanup to finish; do not rerun uninstall merely because delayed cleanup is still settling.
5. Verify that CogentNexus-OpenClaw-owned launchers, skill/runtime/state paths, startup/task ownership, plugin registration/config, and other owned artifacts are removed or any intentional residue is explicitly identified.
6. Verify that external OpenClaw remains installed and its native route/Gateway remains healthy.
7. Verify Ollama remains installed/preserved.

If ownership residue is ambiguous or uninstall fails, stop and report without ad hoc deletion.

## Phase 5 — Fresh reinstall of the same exact artifact

Using the same previously verified CI candidate archive:

1. Run the candidate Windows installer once as a fresh reinstall.
2. Record root exit code and evidence.
3. Verify:
   - v0.9.3 candidate identity;
   - namespace ownership/manifest/plugin identity;
   - `MANAGED` with Ollama;
   - healthy Gateway;
   - healthy Ollama/provider;
   - recovery `READY`;
   - no LM Studio management;
   - no dependency on stale pre-uninstall CogentNexus-OpenClaw state.

If fresh reinstall fails, stop and report. Do not replay it.

## Phase 6 — Normal lifecycle proof

Against the freshly reinstalled candidate, exercise each normal lifecycle transition once, recording state/check evidence around each transition:

1. `cnxclaw.cmd stop`
2. status/check verification appropriate to the stopped state
3. `cnxclaw.cmd start`
4. status/check verification requiring healthy managed convergence
5. `cnxclaw.cmd restart`
6. status/check verification requiring healthy managed convergence

Do not add undocumented recovery commands merely to make a transition pass. Final pre-recovery state must be coherent `MANAGED` / Ollama with healthy listeners and recovery `READY`.

## Phase 7 — Real disruptive recovery proof

Only if Phases 0–6 all passed:

1. Reconfirm the exact source/harness identity.
2. Run the current v0.9.3 Windows v3 recovery harness exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

3. Supply the harness's explicit lowercase `y` confirmation once.
4. Exact-PID validation and protected-process safety gates from D-004 are mandatory.
5. Never use process-tree kill as an injection mechanism.
6. Protected interactive/system processes and harness ancestors must never be targeted.
7. If the harness stops/fails/blocks, preserve its evidence and do not replay it in this task.
8. Final required runtime condition after a PASS is coherent `MANAGED` / Ollama, healthy required listeners/provider, and recovery verdict `READY`.

Timeouts are observation/safety fuses; they are not authority to declare recovery semantics successful.

## Phase 8 — Report and stop

Publish exactly one executor-owned report:

`docs/operations/coordination/reports/CNX-20260828-105-v093-real-windows-lifecycle-acceptance.md`

The report commit message must begin:

`report: CNX-20260828-105`

The report must include:

- exact pinned source SHA;
- exact artifact identity and verified hashes;
- OpenClaw/Ollama versions used;
- evidence root path;
- phase-by-phase commands and root exit codes;
- before/after lifecycle state summaries;
- ownership/plugin/route/Gateway/provider/recovery verdicts;
- recovery harness verdict and evidence references;
- explicit confirmation that OpenClaw/Ollama were preserved;
- explicit confirmation that no Dashboard semantic Send occurred;
- any residue, warning, or ambiguity;
- final verdict `PASS`, `FAIL`, or `BLOCKED`.

`PASS` is allowed only if every mandatory phase above passed against the same exact candidate artifact. If anything required is missing or ambiguous, use `FAIL` or `BLOCKED` and explain the boundary precisely.

After publishing the report, stop for independent ChatGPT review. Do not invent Task 106.

## Hard prohibitions

Task 105 does **not** authorize:

- a Dashboard semantic nonce/Send, sent sentinel, or semantic artifact reuse;
- source/product behavior fixes;
- direct live SQLite edits or arbitrary config/runtime mutations;
- session cleanup or normalization;
- credential/token/password access or re-entry;
- model/provider/timeout changes;
- OpenClaw update/reinstall/uninstall/rebaseline;
- Ollama update/reinstall/uninstall;
- LM Studio management;
- process-tree kills;
- reboot;
- merge, tag, GitHub Release publication, or force push;
- repeating a destructive phase after its first attempt failed or already completed.

## Stop conditions

Stop immediately and report rather than improvise if any of these occurs:

- exact source/artifact provenance cannot be proven;
- OpenClaw is not exactly `2026.7.1-2`;
- existing install-over source state is partial/mixed/ambiguous/unowned;
- a lifecycle command returns non-zero or produces ambiguous ownership/state;
- OpenClaw or Ollama preservation would require undocumented destructive action;
- exact-PID/protected-process safety gates cannot be proven before disruption;
- credentials/secrets would need to be retrieved or re-entered;
- any requested action falls outside this task's explicit scope.
