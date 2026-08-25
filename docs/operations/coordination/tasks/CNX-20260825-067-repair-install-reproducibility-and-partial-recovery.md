# CNX-20260825-067 — Repair Install Reproducibility and Partial-Install Recovery

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REPAIR_TDD_INSTALL_REPRODUCIBILITY_AND_RECOVERY`

Current authorization: `INSTALL_REPRODUCIBILITY_AND_RECOVERY_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Correct the two source defects exposed by accepted Task 066 so a clean/fresh Windows install is reproducible across the supported npm toolchains and a failed fresh install before `ownership.json` cannot permanently dead-end the supported installer.

This task is source/tests only. Do not mutate the current live partial-install residue. The machine is currently in native OpenClaw mode with no CogentNexus supervisor/launcher/plugin registration; preserve that stable state until this source repair is independently accepted.

## Accepted predecessor

Task 066 report commit:

`d6812dd90a6ca28557cf18b6008a88dbfe5fe926`

Task 066 review:

Decision `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_FRESH_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY`

Review commit:

`21971ff01142ac98c166dc196c47df7cec60f434`

Reviewed source baseline containing the defects:

`21686f70520c5e0263e8aea4d644d2c87324e872`

## Current live state — hard preservation boundary

Accepted end-of-Task-066 condition:

- no `CogentNexus-OpenClaw-Supervisor` Scheduled Task;
- no `cnxclaw.cmd` launcher;
- no registered/enabled CogentNexus plugin;
- AGENTS managed block absent and baseline restored;
- OpenClaw Gateway native and healthy;
- Ollama healthy with the same four models;
- partial failed-install residue exists only at the reported workspace `.cogentnexus-openclaw` and `skills\cogentnexus-openclaw` roots;
- no valid `ownership.json` exists for that partial attempt.

Task 067 MUST NOT clean, modify, adopt, or complete those live residues. All recovery tests use isolated temporary workspaces/application-data roots.

## Defect D1 — plugin lockfile is not reproducible under npm 12

Independent source inspection confirms:

- `plugins/cogentnexus-openclaw/package-lock.json` has `node_modules/openclaw/node_modules/@types/retry` at `0.12.5`;
- the same lock has `node_modules/openclaw/node_modules/p-retry` at `4.6.2` declaring exact dependency `"@types/retry": "0.12.0"`.

Task 066 reproduced `npm ci` failure with npm 12.0.2:

`Missing: @types/retry@0.12.0 from lock file`

A prior npm 11.16.0 install accepted the lock. This version-dependent permissiveness is not acceptable installation correctness.

### D1 required outcome

Produce a lock/package contract that passes clean `npm ci` under BOTH:

- npm `11.16.0`;
- npm `12.0.2`;

using a Node version compatible with each npm, in isolated clone/test directories.

Do not solve this by making the installer silently select an older permissive npm. The lock itself must be consistent.

Prefer deterministic dependency metadata. If changing the plugin devDependency `openclaw` from `latest` to exact `2026.7.1-2` is necessary to regenerate the lock without drifting the reviewed target, do so and explain why. Do not upgrade OpenClaw or unrelated dependencies as part of this repair.

A surgical lock correction is acceptable only if independently validated by clean installs under both npm versions and by plugin build/test/pack validation.

## Defect D2 — failed fresh install can dead-end before ownership manifest

Independent source inspection confirms `namespace_ownership.py::classify_install()` behaves as follows:

```python
if inventory["new"]:
    verify_manifest(paths["stateRoot"], workspace=workspace)
    return {"mode": "upgrade", **inventory}
```

If a fresh install creates state/skill artifacts and then fails before `ownership.json`, every later install classifies it as new/upgrade and fails ownership verification. Supported uninstall likewise cannot mutate unowned residue.

Task 066 produced exactly this state after `npm ci` failed.

### D2 required architecture

Add a durable, bounded fresh-install transaction/recovery contract. Minimum safety properties:

1. Before the first fresh-install mutation that can leave new-namespace artifacts, write an explicit transaction marker containing enough exact path/provenance data to identify ONLY artifacts created by that fresh install attempt.
2. The marker must be inside a CogentNexus-owned application-data/recovery boundary, not an unrelated user path.
3. The marker must not claim full installed ownership and must be distinguishable from `ownership.json`.
4. On normal successful install, clear/commit the transaction marker only after full ownership has been created and verified.
5. On a caught installer failure, bounded rollback may remove only paths recorded as created by that transaction and restore any explicitly backed-up preexisting product paths; unrelated OpenClaw/Ollama/user state must be untouched.
6. On process crash/power loss where PowerShell trap/finally cannot run, rerunning the supported installer must detect a valid incomplete fresh-install transaction before `classify-install`, prove its marker/path boundary, perform bounded recovery, and return to a coherent fresh classification.
7. Unmarked or ambiguous residue must remain fail-closed. Do not weaken ownership validation to adopt arbitrary partial state.
8. The transaction/recovery mechanism must not permit deleting a path outside the exact CogentNexus workspace/application-data boundaries through a crafted marker; canonical ancestry validation is mandatory.

Equivalent design is allowed if it proves the same crash-recovery and deletion-safety properties. Merely moving `ownership.json` earlier is NOT sufficient if the manifest would claim plugin/launcher artifacts that do not yet exist.

## Required method — strict TDD

Use a fresh isolated worktree/clone at current coordination HEAD. Use `superpowers:using-git-worktrees` at execution time and strict RED → GREEN cycles.

Before any production correction:

1. verify local HEAD == remote branch HEAD and tree clean;
2. verify this task and ACTIVE/STATUS agree;
3. verify Task 066 review `21971ff01142ac98c166dc196c47df7cec60f434` is an ancestor;
4. verify no Task 067 report exists;
5. write D1 and D2 failing tests first;
6. run each against the accepted defective source and capture the intended RED failure;
7. make the smallest cohesive correction;
8. run focused GREEN and full validation.

## Mandatory D1 tests

### L1 — lock consistency under npm 12

From a clean isolated copy of `plugins/cogentnexus-openclaw`, run exact npm `12.0.2` `npm ci` with no preexisting `node_modules`.

RED must reproduce the Task 066 `@types/retry@0.12.0` consistency failure against the defective baseline.

GREEN must exit 0.

### L2 — compatibility under npm 11

Repeat a clean `npm ci` using npm `11.16.0`. GREEN must exit 0 so fixing npm 12 does not regress the machine's established Node 24/npm 11 toolchain.

### L3 — no dependency drift

After correction prove:

- plugin package version remains `0.9.3`;
- installed/dev OpenClaw dependency resolves to exactly `2026.7.1-2` for this acceptance branch;
- no unrelated direct dependency version changed unless forced by the lock correction and explicitly justified;
- `npm ci` leaves the lockfile unchanged (`git diff --exit-code -- package.json package-lock.json` after install where applicable).

### L4 — plugin validation

Run from the clean install:

- `npm run plugin:validate`;
- `npm test`;
- `npm pack --json` plus existing package-content verification.

Record exact pass/fail counts.

## Mandatory D2 executable tests

Create focused tests/harnesses that execute the production recovery surfaces, not duplicated pseudocode.

### R1 — fresh transaction begins before residue-capable mutation

In a temp workspace/application-data root, run/extract the production fresh-install transaction begin surface and prove the marker exists BEFORE creation/copy of live state/skill artifacts that would make `current_inventory()["new"]` non-empty.

Marker must include schema/version, transaction id, exact canonical workspace/product roots, phase/state, and an allowlisted set of recoverable created paths.

### R2 — simulated failure after skill/state creation is recoverable

In a temp workspace:

1. start fresh transaction;
2. create the same bounded state/skill residue shape seen in Task 066;
3. omit `ownership.json`;
4. simulate installer termination before normal rollback;
5. invoke the production resume/recovery preflight used by rerun installer;
6. prove only marker-authorized residue is removed/restored;
7. prove `classify_install()` then returns `fresh`.

RED against current source must demonstrate the dead end.

### R3 — normal caught failure rolls back

Simulate a production installer failure after state/skill mutation but before manifest commit. Prove the supported rollback surface leaves the temp workspace/application-data in coherent fresh state and clears/archives the transaction marker according to the implemented contract.

### R4 — successful commit transition

Simulate/execute the transaction through successful ownership creation/verification. Prove the incomplete marker no longer authorizes cleanup and the installation classifies as coherent `upgrade`/installed state using valid `ownership.json`.

### R5 — malicious/out-of-bound marker rejected

Construct marker paths pointing to:

- workspace parent;
- unrelated sibling skill;
- arbitrary `%USERPROFILE%`/temp path;
- OpenClaw root outside the exact allowlisted CNX paths.

Recovery must reject before deletion and must not modify any sentinel files.

### R6 — unmarked partial state remains fail-closed

Reproduce the Task 066 residue without a valid transaction marker. `classify_install()` / recovery must NOT silently adopt or delete it. This preserves strict ownership safety.

### R7 — current Task-066 residue compatibility plan

Source design/report must state explicitly how the later live successor will handle the already-existing Task-066 residue, which predates the new transaction marker. Do NOT clean it in Task 067.

The expected later live approach is a one-time bounded cleanup authorized only after re-proving:

- exactly the two reported Task-066-created residue roots;
- no `ownership.json`;
- no launcher/task/plugin registration;
- hashes/tree shape consistent with Task 066 evidence;
- no unrelated content inside those roots.

Then the fixed installer starts from true fresh state and all future partial installs use the new recovery contract.

## Full verification

Use isolated developer environments only. Required fresh evidence:

1. D1 RED under npm 12 before fix;
2. D2 RED for partial-install retry before fix;
3. focused GREEN for all L/R tests;
4. clean npm 11.16.0 `npm ci`;
5. clean npm 12.0.2 `npm ci`;
6. plugin build/validate/test/pack verification;
7. Python/PowerShell installer-recovery focused tests;
8. full `pytest tests/ -q` with `requirements-dev.txt` installed in isolated dev venv;
9. any canonical Node/plugin tests used by repository CI;
10. `python scripts/check_baseline_consistency.py`;
11. `git diff --check`;
12. clean worktree after implementation commit.

Any skipped test must be explained. No PASS if the npm 12 reproduction is not actually exercised.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. final report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260825-067-repair-install-reproducibility-and-partial-recovery.md`

Report must include:

- fetched execution HEAD;
- implementation HEAD;
- npm 11/npm 12 exact versions and clean-install results;
- RED/GREEN evidence;
- exact transaction/recovery contract;
- malicious-marker rejection evidence;
- full test counts;
- explicit no-live-mutation accounting;
- independent report-only publication fence.

## Live hard fence

No live cleanup of Task-066 residue; no install/install-over/uninstall/reset; no lifecycle command; no Scheduled Task create/update/delete/run/end; no Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no primary workspace mutation; no reboot; no HermesAgent project mutation; no merge/tag/release.

## Result tokens

Use exactly one:

- `PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`
- `BLOCKED_LOCKFILE_REPRODUCIBILITY`
- `BLOCKED_PARTIAL_INSTALL_RECOVERY_DESIGN`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If ChatGPT independently accepts `PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`, proceed to a separate live Task 068 without another conceptual redesign. Task 068 may first perform one-time bounded cleanup of exactly the proven Task-066-created residue roots, then fresh-install the accepted source and complete the remaining Task-066 Phases C-F: exact owned-runtime binding, at least three natural PT1M no-flash ticks, and final MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health.
