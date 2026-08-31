# CNX-20260828-107 — v0.9.3 Real-Windows Lifecycle Acceptance Retry

**Status:** `READY_FOR_HERMES`  
**Execution mode:** `MANUAL_REAL_WINDOWS_ACCEPTANCE`  
**Owner / reviewer:** ChatGPT  
**Executor:** Hermes/Codex  
**Branch:** `agent/v0.9.3-full-stabilization`  
**Pinned acceptance source:** `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

## Purpose

Re-run the bounded real-Windows v0.9.3 lifecycle acceptance after the npm 12 installer incompatibility found by Task 105 was repaired and the stale regression assertions were closed by Task 106.

This is a **new pinned acceptance attempt**. It does not alter, replay, or reinterpret the failed Task-105 evidence. Task 105 remains a valid failed attempt against source `c4d37b0005afeffcd183848dfce5476cbe2b85cd` and its old package artifact.

The intended ordered proof is:

`exact provenance -> read-only residue re-entry -> install-over -> reset -> uninstall -> fresh reinstall -> normal lifecycle -> disruptive recovery -> report`

Do **not** perform a Dashboard semantic nonce/Send in this task. Final semantic durable-delivery acceptance remains a separately reviewed follow-up after lifecycle acceptance passes.

## Why a new artifact is mandatory

Task 105 used an immutable package built from `c4d37b0005afeffcd183848dfce5476cbe2b85cd` and failed during Phase 2 because OpenClaw `2026.7.1-2` followed its `npm-pack:` metadata path against npm `12.0.2`.

Accepted repair ancestry after that failure is:

1. `e0b6173d2ed888303bae3e31fd023b24e201c167` — RED installer-path contract;
2. `c676c50cb19378541a8223263a609fb7d18ed5a8` — minimal production fix changing Windows plugin installation to the exact local `.tgz` path;
3. `5e41c0c3a8b9da920571b828c9a863f5591af86b` — production-shaped npm `12.0.2` regression proof;
4. `80a48f73d3c525565a15e07ed1ed37a7c4fc4ad3` — Task-106 test-only stale-assertion repair;
5. `b14a711f24b3fd1cd0aaa51ce636c8502ba42404` — Task-106 report commit and exact source used for this retry package proof.

Do not reuse Task 105 artifact ID `9669312785` or its inner archive hashes. That package predates the accepted production fix and is intentionally rejected for this task.

## Exact acceptance identity

The runtime artifact for Task 107 is immutable evidence even if the development branch advances later.

- source commit: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- CogentNexus-OpenClaw version: `0.9.3`
- OpenClaw operational baseline: `2026.7.1-2`
- managed provider: `Ollama only`
- payload-v2 file count: `178`
- payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- package tar.gz SHA256: `5a010879d6effd3ee0ecbc449a6cffb30ecd26e91b90fb08765636c31d6a3b05`
- package ZIP SHA256: `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b`
- Validate workflow run: `33149370021` — SUCCESS
- PS5.1 Acceptance Smoke run: `33149369996` — SUCCESS
- Windows Installer Pack Smoke run: `33149369983` — SUCCESS
- package-proof Actions artifact ID: `9677072214`
- package-proof artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- package-proof outer artifact digest / SHA256: `sha256:b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`
- recovery harness Git blob SHA: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

The package proof was independently inspected before this task was published. Its `PACKAGE_IDENTITY.json` records the exact source commit above, version `0.9.3`, file count `178`, and the payload-v2 fingerprint above. The packaged `scripts/install.ps1` contains the repaired local-archive invocation:

`openclaw plugins install $packagePath --force`

and does not contain the superseded executable invocation:

`openclaw plugins install ("npm-pack:" + $packagePath) --force`

Coordination commits created after this task is published do **not** change the acceptance target. Do not install branch HEAD merely because it is newer.

## Non-negotiable artifact rule

Use the exact CI package-proof artifact identified above.

1. Download Actions artifact ID `9677072214` using an authenticated GitHub mechanism available to the executor.
2. Verify the downloaded outer ZIP SHA256 is exactly `b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`.
3. Locate the inner `cogentnexus-openclaw-v0.9.3.zip`.
4. Verify its SHA256 is exactly `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b` before extraction or installation.
5. Verify `PACKAGE_IDENTITY.json` records source `b14a711f24b3fd1cd0aaa51ce636c8502ba42404` and the exact identity values above.
6. Use a detached checkout/worktree of exact source commit `b14a711f24b3fd1cd0aaa51ce636c8502ba42404` for source-side harnesses and provenance.
7. Do not rebuild a replacement package locally and treat it as the accepted artifact.

If exact artifact/source identity cannot be established, publish a `BLOCKED` report and stop without live mutation.

## Evidence root

Create a new timestamped evidence directory outside both the normal workspace and the CogentNexus-OpenClaw runtime root, for example:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-107\<timestamp>`

Do not reuse or overwrite Task-105 evidence. Keep detailed local evidence there. The GitHub report may reference paths, hashes, exit codes, and redacted metadata, but must not publish secrets, credentials, tokens, passwords, private session payloads, or unredacted configuration values.

## Global execution rules

- Execute phases in order.
- Every destructive or externally visible lifecycle operation is single-attempt unless the command itself provides a documented internal recovery path.
- If a phase fails or becomes ambiguous, stop the task, preserve evidence, and report `FAIL` or `BLOCKED`.
- Do not replay side effects merely to obtain a cleaner result.
- Do not patch source/runtime behavior in this task. A discovered product defect becomes a separate TDD repair task after review.
- Preserve externally owned OpenClaw and Ollama installations and user data.
- No LM Studio management or testing.
- Do not expose or request credentials.
- Do not normalize Task-105 residue manually before the read-only re-entry proof.

## Phase 0 — Exact provenance and read-only residue re-entry

Before any mutation:

1. Establish a detached source checkout/worktree at exact commit `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`.
2. Record exact source SHA and verify `scripts/test-v093-ollama-recovery-windows-v3.ps1` has Git blob SHA `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.
3. Download and verify the exact CI artifact as required above.
4. Record installed/runtime tool versions needed for the proof. OpenClaw must be exactly `2026.7.1-2`; record Node, npm, Ollama, and Python versions actually observed.
5. Read the current installed CogentNexus-OpenClaw launcher/status/ownership/plugin/task state without mutation.
6. Capture appropriate read-only checks, including where available:
   - `cnxclaw.cmd status`
   - `cnxclaw.cmd provider status`
   - `cnxclaw.cmd check openclaw`
   - `cnxclaw.cmd check gateway`
   - `cnxclaw.cmd check recovery`
   - `cnxclaw.cmd check delivery`
   - `cnxclaw.cmd check resources`
   - namespace ownership verification
   - read-only SQLite integrity verification
7. Compare the current live state against the preserved Task-105 failure boundary. Task 105 recorded:
   - controller `PASSTHROUGH`;
   - desired provider `unchanged` with selected provider still Ollama;
   - generation `25`;
   - Gateway healthy;
   - Ollama healthy/ready;
   - recovery `READY` for passthrough;
   - SQLite integrity `ok`;
   - ownership manifest still present/coherent;
   - CNX Supervisor task absent after supported native handoff;
   - installer staging/backup residue intentionally preserved.
8. Proceed only if the current state is still coherently attributable to that failed install-over boundary and the fixed installer can safely treat it as an existing CogentNexus-OpenClaw deployment. A generation/state/task/ownership mismatch that cannot be explained from read-only evidence is a `BLOCKED` condition, not permission to clean or repair manually.

Do not assume the old state merely because the Task-105 report says it existed. Verify the machine as it exists at execution time.

## Phase 1 — External evidence/backup boundary

Before install-over mutation:

- finish the new external evidence root;
- capture hashes/listings/state needed to prove what changed from the Task-105 residue boundary;
- preserve any backup required by the documented installer/lifecycle process outside CogentNexus-OpenClaw-owned paths where appropriate;
- keep sensitive configuration content local and redacted from the report;
- do not delete Task-105 residue before the fixed installer is given its single authorized convergence attempt.

This phase does not authorize arbitrary copying of private OpenClaw/session data into the repository.

## Phase 2 — Fixed-candidate install-over proof

Using the exact verified Task-107 candidate archive:

1. Extract/stage it in the new external temporary/evidence location.
2. Run that candidate's normal Windows installer path (`scripts\install.ps1`) exactly once against the coherent Task-105 residue deployment. Do not manually copy plugin/runtime/config files around the installer transaction.
3. Record the root process exit code and installer evidence.
4. Require the fixed local `.tgz` plugin installation path to succeed and the transaction to converge to v0.9.3 with namespace ownership intact.
5. Verify after install-over:
   - installed CogentNexus-OpenClaw source/package identity is the accepted Task-107 candidate;
   - ownership manifest/plugin identity is coherent;
   - state is `MANAGED` with Ollama;
   - Gateway is healthy;
   - Ollama/provider is healthy;
   - recovery verdict is `READY`;
   - canonical CNX Supervisor/startup ownership is coherent;
   - no LM Studio managed path is introduced.
6. Explicitly record whether the prior Task-105 staging/backup residue was retained, superseded, or cleaned by the **documented installer transaction itself**. Do not clean it manually merely for report aesthetics.

If install-over fails, returns non-zero, or leaves ambiguous state, stop and report. Do not rerun the installer.

## Phase 3 — Reset proof

Only if Phase 2 passed:

1. Run `cnxclaw.cmd reset` once.
2. Supply the command's required exact lowercase `y` confirmation once through a controlled interactive/stdin path.
3. Record the exit code and evidence.
4. Verify that CogentNexus-OpenClaw runtime state is recreated as a fresh managed v0.9.3 installation while external OpenClaw and Ollama remain installed/preserved.
5. Require final `MANAGED` / Ollama state, healthy Gateway/provider, coherent ownership/plugin identity, and recovery `READY`.

If reset fails, stop. Do not issue a second reset.

## Phase 4 — Uninstall proof

Only if Phase 3 passed:

1. Run `cnxclaw.cmd uninstall` once.
2. Supply the required exact lowercase `y` confirmation once.
3. Record exit code and all evidence paths.
4. Allow a bounded observation period for the documented delayed Windows self-cleanup to finish; do not rerun uninstall merely because delayed cleanup is still settling.
5. Verify that CogentNexus-OpenClaw-owned launchers, skill/runtime/state paths, startup/task ownership, plugin registration/config, and other owned artifacts are removed or any intentional residue is explicitly identified.
6. Verify that external OpenClaw remains installed and its native route/Gateway remains healthy.
7. Verify Ollama remains installed/preserved.

If ownership residue is ambiguous or uninstall fails, stop and report without ad hoc deletion.

## Phase 5 — Fresh reinstall of the same exact artifact

Only if Phase 4 passed, using the same previously verified Task-107 CI candidate archive:

1. Run the candidate Windows installer once as a fresh reinstall.
2. Record root exit code and evidence.
3. Verify:
   - exact Task-107 v0.9.3 candidate identity;
   - namespace ownership/manifest/plugin identity;
   - `MANAGED` with Ollama;
   - healthy Gateway;
   - healthy Ollama/provider;
   - recovery `READY`;
   - no LM Studio management;
   - no dependency on stale pre-uninstall CogentNexus-OpenClaw state.

If fresh reinstall fails, stop and report. Do not replay it.

## Phase 6 — Normal lifecycle proof

Only if Phase 5 passed, against the freshly reinstalled candidate, exercise each transition once while recording before/after state and checks:

1. `cnxclaw.cmd stop`
2. status/check verification appropriate to the stopped state
3. `cnxclaw.cmd start`
4. status/check verification requiring healthy managed convergence
5. `cnxclaw.cmd restart`
6. status/check verification requiring healthy managed convergence

Do not add undocumented recovery commands merely to make a transition pass. Final pre-recovery state must be coherent `MANAGED` / Ollama with healthy required listeners and recovery `READY`.

## Phase 7 — Real disruptive recovery proof

Only if Phases 0–6 all passed:

1. Reconfirm exact source/harness identity.
2. Run the current v0.9.3 Windows v3 recovery harness exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

3. Supply the harness's explicit lowercase `y` confirmation once.
4. Exact-PID validation and protected-process safety gates remain mandatory.
5. Never use process-tree kill as an injection mechanism.
6. Protected interactive/system processes and harness ancestors must never be targeted.
7. If the harness stops/fails/blocks, preserve its evidence and do not replay it in this task.
8. Final required runtime condition after a PASS is coherent `MANAGED` / Ollama, healthy required listeners/provider, and recovery verdict `READY`.

Timeouts are observation/safety fuses; they are not authority to declare recovery semantics successful.

## Phase 8 — Report and stop

Publish exactly one executor-owned report:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

The report commit message must begin:

`report: CNX-20260828-107`

The report must include:

- final verdict `PASS`, `FAIL`, or `BLOCKED`;
- exact pinned source SHA;
- exact artifact ID/name and verified outer/inner hashes;
- exact CI run IDs used as repository-side gates;
- OpenClaw/Ollama/Node/npm/Python versions observed;
- evidence root path;
- Phase-0 comparison with the preserved Task-105 residue boundary;
- phase-by-phase commands, root exit codes, and first-failure boundary if any;
- before/after lifecycle state summaries;
- ownership/plugin/task/route/Gateway/provider/recovery verdicts;
- reset/uninstall/fresh-reinstall preservation evidence;
- recovery harness verdict and evidence references if Phase 7 is reached;
- explicit confirmation that OpenClaw and Ollama were preserved;
- explicit confirmation that no Dashboard semantic Send occurred;
- any residue, warning, ambiguity, or cleanup performed by documented product behavior;
- exact report commit SHA after publication.

`PASS` is allowed only if every mandatory phase above passes against the same exact Task-107 candidate artifact. If anything required is missing or ambiguous, use `FAIL` or `BLOCKED` and explain the boundary precisely.

After publishing the report, stop for independent ChatGPT review. Do not invent or start the next semantic-delivery task.

## Hard prohibitions

Task 107 does **not** authorize:

- use of the old Task-105 candidate artifact for the retry;
- installing moving branch HEAD instead of pinned source/artifact identity;
- Dashboard semantic nonce/Send, sent sentinel, `chat.send`, semantic artifact reuse, or provider inference;
- source/product behavior fixes;
- direct live SQLite edits or arbitrary config/runtime mutations;
- manual cleanup/normalization of Task-105 residue before or between lifecycle phases;
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

- exact Task-107 source/artifact provenance cannot be proven;
- any of the three pinned CI gates is not SUCCESS for exact source `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`;
- OpenClaw is not exactly `2026.7.1-2`;
- current live state cannot be reconciled read-only with the preserved Task-105 failure boundary;
- existing install-over source state is partial/mixed/ambiguous/unowned;
- the fixed installer does not use/accept the local package archive path as expected;
- a lifecycle command returns non-zero or produces ambiguous ownership/state;
- OpenClaw or Ollama preservation would require undocumented destructive action;
- exact-PID/protected-process safety gates cannot be proven before disruption;
- credentials/secrets would need to be retrieved or re-entered;
- any requested action falls outside this task's explicit scope.
