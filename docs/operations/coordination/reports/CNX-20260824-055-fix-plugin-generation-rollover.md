# CNX-20260824-055 — Fix Ownership-Safe Plugin Generation Rollover

Status: **PASS**

Result: `PASS_PLUGIN_GENERATION_ROLLOVER_FIXED`

Repository: `funggier/CogentNexus-OpenClaw`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Repository path: `/workspace/scratch/15678548c5c3/cogentnexus-openclaw-task055`  
Fetched start HEAD: `35239c5015288f8cbb852a11315739cfe97c4514`  
Remote implementation HEAD: `6ad87e6f3ae65327a14bab4b5144dda4416d3645`

## Diagnosis and source investigation

Task 054 proved that `openclaw plugins install ... --force` can create a new generation-specific managed npm project without retiring the prior manifest-owned project. Both paths then contain exact v0.9.3 payloads, so the existing resolver correctly rejects ambiguity.

The fix was derived against OpenClaw source commit `b8d6e799a31d469f60277427472b87036b1f9be7`. The inspected source established:

- `src/plugins/install-paths.ts` defines the `__openclaw-generation__g-<16 hex>` project form and exact managed-project boundary;
- `src/plugins/install-managed-npm-state.ts` selects generation-specific roots;
- `src/infra/npm-managed-root.ts` writes private wrapper manifests, package dependencies, OpenClaw-managed peer dependencies, managed overrides, and lockfiles;
- `src/cli/plugins-list-command.ts` and `src/plugins/registry-types.ts` expose the `plugins[]` records used to bind canonical ID, package, version, and `rootDir`;
- `src/plugins/uninstall.ts` independently confirms that destructive npm cleanup must prove canonical package/project ownership.

The Task 054 exit-wrapper defect is independent of plugin rollover. Its retained poststate proves that the exact child terminated while `observedExitCode` was `null`. The prior wrapper depended on a nullable process record without retaining the native handle. On Windows PowerShell 5.1 with redirected fast-exiting children, that can leave `ExitCode` unobserved and later coerce null to zero. The replacement caches `$process.Handle` before waiting, calls `WaitForExit()` and `Refresh()`, rejects null explicitly, and converts only an observed numeric value. Windows CI now proves numeric `0` and `7`, null rejection, and argument round trips containing spaces, quotes, an empty argument, and backslashes.

## Selected design

The ambiguity guard remains unchanged. The installer now performs a narrow active-generation transition only for a coherent upgrade:

1. remain PASSTHROUGH and install/disable the replacement through supported OpenClaw plugin commands;
2. capture `openclaw plugins list --json` and create a machine-readable reviewed plan;
3. prove exactly two canonical payloads: the old ownership-manifest path and the independently active replacement registration;
4. prove each OpenClaw-managed wrapper from its exact project name, private manifest schema, target dependency spec, declared managed peers/overrides, lockfile, package/version, and complete tree SHA-256;
5. bind the full inventory SHA-256 and canonical active-registration SHA-256 into the plan;
6. recapture inventory immediately before apply and reject any change;
7. require a same-volume atomic `os.replace` into the unique external `CogentNexus-OpenClaw/plugin-generation-rollover-backups` boundary;
8. verify the backup tree, atomically update ownership to the replacement, and prove exactly one candidate plus exact ownership;
9. restore the old project and manifest automatically if final verification fails.

Cross-filesystem retirement, unexpected wrapper fields/dependencies, undeclared peer content, missing lock proof, foreign roots, inventory drift, registration drift, plan/hash drift, conflicting fingerprints, and non-PASSTHROUGH mode all fail closed before authority returns.

Windows and POSIX installers now recapture fresh inventory before apply. Both reject linked-install flags; both remove only an existing exact product linked load path before npm-managed installation. Fresh install, legacy migration, and `SkipPlugin` do not invoke generation retirement.

Rejected alternatives:

- deduplicating equal fingerprints or weakening resolver ambiguity;
- broad deletion or substring-based project selection;
- trusting wrapper dependency presence alone;
- reusing stale plan-time plugin inventory at apply;
- `shutil.move` across filesystems, which can degrade into partial copy/delete;
- accepting raw PowerShell string arrays through `Start-Process -ArgumentList` on Windows PowerShell 5.1.

## Recovery interface

Plan:

```text
python namespace_ownership.py rollover-plan --root <state-root> --workspace <workspace> --app-data <CogentNexus-OpenClaw-app-data> --inventory-json <plugins-list.json> --plan <plan.json>
```

Apply:

```text
python namespace_ownership.py rollover-apply --plan <plan.json> --plan-sha256 <reviewed-sha256> --inventory-json <fresh-plugins-list.json>
```

The plan binds state/workspace/application-data boundaries, old/new payload and wrapper roots, backup destination, both payload fingerprints, wrapper/package/lock proofs, both complete project-tree hashes, manifest before/after, complete inventory hash, and canonical active registration. Apply never enables MANAGED mode; Task 056 remains the separately reviewed live-repair/lifecycle task.

## TDD evidence

Before production changes:

- focused existing namespace/install tests: `47 passed`;
- full Python baseline: `253 passed, 4 subtests passed`;
- initial rollover/installer RED: `11 failed` for the absent recovery interface and ordering;
- additional application-data-boundary and CI-self-test RED cases failed before their implementations;
- review-hardening RED: `8 failed, 16 passed, 1 skipped`, covering foreign/shared wrappers, inventory drift, rename failure, POSIX parity, and PowerShell argument/null contracts.

GREEN progression:

- first focused implementation: `19 passed, 1 skipped`;
- review-hardening focused tests: `24 passed, 1 skipped`;
- final local full suite: `273 passed, 1 skipped, 4 subtests passed`.

The one local skip was the Windows-only PowerShell runtime test on the Linux work host. It was subsequently executed successfully by Windows GitHub Actions.

## Local verification

Executed successfully:

- `.venv/bin/python -m pytest -q` — `273 passed, 1 skipped, 4 subtests passed`;
- `.venv/bin/python scripts/check_namespace_isolation.py` — PASS;
- `.venv/bin/python scripts/check_baseline_consistency.py` — PASS;
- `.venv/bin/python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton` — PASS;
- Cogent, runtime, and workflow self-tests — PASS;
- benchmark validator self-test — PASS;
- plugin-path migration helper contract — PASS;
- `python -m py_compile ... namespace_ownership.py` — PASS;
- `sh -n scripts/install.sh` — PASS;
- `git diff --check` — PASS;
- independent code re-review — READY, no remaining Critical or Important issue.

Direct local `npm test` could not start because the work sandbox blocked the npm invocation and its local `node_modules` was incomplete. No PASS was inferred. The complete Node checks later passed in GitHub Actions.

## Exact-head GitHub verification

All workflows associated with remote implementation HEAD `6ad87e6f3ae65327a14bab4b5144dda4416d3645` completed successfully:

- Validate `32743333976` — all Ubuntu, macOS, and Windows jobs on Python 3.11/3.14 plus package dry-run;
- Windows Installer Pack Smoke `32743334579`;
- PS5.1 Acceptance Smoke `32743333958`;
- PS5.1 Live Runner Smoke `32743334481`;
- PS5.1 Partial Repair Smoke `32743334555`;
- PS5.1 v0.9.3 Gateway Convergence Smoke `32743334806`;
- PS5.1 v0.9.3 Ollama Recovery V2 Smoke `32743334051`;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `32743333918`;
- PS5.1 v0.9.3 Ollama Recovery Reality Smoke `32743334261`.

Validate included PowerShell parsing, the exact numeric/null/argument root-process self-test, Python compile and full pytest, POSIX syntax, `npm ci`, plugin tests, evaluation, audit, plugin validation, and release archive dry-run.

An earlier exact-tree run exposed a stale pre-Task-042 CI assertion that still required `cnx_v093.py`; it was corrected to `cnxclaw_v093.py` with a regression test. A following run exposed test-platform assumptions (`pwsh` on non-Windows and Windows path case); those tests were corrected without production changes. The final exact-head run above is fully green.

## Changed paths and remote commits

Implementation commit `c29a1975396dbf532a3e16c422f7dc09fa68f21f`:

- `.github/workflows/validate.yml`;
- `requirements-dev.txt`;
- `scripts/install.ps1`;
- `scripts/install.sh`;
- `scripts/invoke-root-process-exact.ps1`;
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `tests/test_namespace_install_contract.py`;
- `tests/test_plugin_generation_rollover.py`;
- `tests/test_windows_root_process_exit.py`.

CI/test follow-ups:

- `44056d0f8bcd6a9faf80645eaceafd21f7cfdfdd` — variant-scoped recovery-smoke CLI assertion;
- `6ad87e6f3ae65327a14bab4b5144dda4416d3645` — platform-correct rollover tests.

The connector-published implementation tree matched the tested local tree exactly before publication. Publication used non-force ref updates only. The direct shell push failed before authentication and changed no remote state.

## Safety and remaining work

- live installer invocations: **0**;
- live plugin install/uninstall/retirement/recovery apply: **0**;
- lifecycle, Gateway, Ollama, model, scheduler, AGENTS, process, Procmon, primary-repository, and excluded-system actions: **0**;
- `ACTIVE.md` / `STATUS.md` edits: **0**;
- Task 054 evidence/clone access or mutation: **0**.

The repository fix and recovery primitive are proved. The Task 054 live two-root state intentionally remains unchanged in PASSTHROUGH/startup-disabled mode. Applying the reviewed plan and returning to MANAGED require the separate Task 056 authorization and machine evidence.
