# CNX-20260824-044 — Repair Install Classification and Clean-Reinstall Handoff

Status: **COMPLETED**  
Result: `PASS_INSTALL_CLASSIFIER_AND_REINSTALL_HANDOFF`  
Start HEAD: `02f22464ed214ca57074519e93ecca211482286c`  
Implementation commit: `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`  
Repository: isolated full clone `C:\Users\CDQ-P\AppData\Local\Temp\cnx043-clone-20260824T002614Z`  
Branch: `agent/v0.9.3-recovery-reality-tests`

## Repairs performed

### Product-specific npm inventory

Broad candidate discovery remains available to the exact resolver, but installation inventory now records only:

- the exact direct extension path;
- an exact `node_modules/openclaw-plugin-cogentnexus-openclaw` child, including incomplete/corrupt/old payloads;
- a top-level npm project whose `package.json` exact name or dependency metadata identifies `openclaw-plugin-cogentnexus-openclaw`.

It does not recursively inspect arbitrary `node_modules`. One and multiple unrelated wrappers, unrelated direct plugins, and deeply nested unrelated package-name directories remain absent from product inventory and byte-identical. Valid direct/npm v0.9.3 installs remain upgrades; a second exact candidate fails as ambiguous.

### Clean-reinstall backup handoff

The default backup root is now external to active application data:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Clean-Reinstall-Backups`

`clean_reinstall_handoff.py` rejects a backup root equal to or contained by `%LOCALAPPDATA%\CogentNexus-OpenClaw`. After ownership verification, clean reinstall backs up and removes the canonical application-data root together with other owned paths, so its backup cannot create the installer's partial-state signal. Unknown application-data residue still blocks an ordinary fresh install.

If reinstall fails, the external backup remains and `clean-reinstall-recovery.json` records the workspace, backup, exact error, UTC time, and human-decision flag. `-NoBackup` remains an explicit switch with its permanent-purge warning and creates no false recovery claim.

### Skip-plugin decision

`-SkipPlugin/--skip-plugin` is retained only for a classifier-proven coherent upgrade whose existing exact v0.9.3 plugin has already passed manifest/plugin verification. Fresh and reviewed legacy modes fail `preflight-skip-plugin` before native handoff, copy, init, config, or runtime mutation. No incomplete staging layout receives a complete manifest.

### Post-create ownership verification

Both installers now invoke exact `namespace_ownership.py verify` immediately after manifest creation and before any `enable`. Failure prevents MANAGED enable; the Windows error explicitly records that the installation remains PASSTHROUGH.

## Behavior evidence

Temporary-layout tests cover unrelated single/multiple npm wrappers, unrelated direct and nested packages, byte preservation, exact product-child missing/corrupt/old payloads, wrapper dependency evidence, direct/npm valid upgrades, conflicting candidates, external backup classification, unsafe backup containment, failure recovery accounting, unknown application data, skip-plugin fresh/legacy rejection, coherent-upgrade allowance, and create/verify/enable ordering. Existing HermesAgent, OpenClaw/Ollama sentinel and ownership tests remain green.

## Exact changed paths

- `scripts/clean-reinstall.ps1`
- `scripts/clean_reinstall_handoff.py`
- `scripts/install.ps1`
- `scripts/install.sh`
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `tests/test_clean_reinstall_handoff.py`
- `tests/test_namespace_install_contract.py`
- `tests/test_namespace_ownership.py`

## Commands and results

- `python -m pytest -q` — exit `0`; `248 passed, 1 skipped, 4 subtests passed`. The skip is the existing platform-conditional test.
- `python scripts/check_namespace_isolation.py` — exit `0`, PASS.
- `python scripts/check_baseline_consistency.py` — exit `0`, PASS.
- `python -m compileall -q scripts skills/cogentnexus-openclaw/scripts tests` — exit `0`.
- `python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/cogent.py self-test` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/runtime.py self-test` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/workflow.py self-test` — exit `0`, PASS.
- PowerShell parser validation for `scripts/install.ps1` and `scripts/clean-reinstall.ps1` — exit `0`, no errors.
- `bash -n scripts/install.sh` — exit `1`; the Windows WSL relay reported `execvpe(/bin/bash) failed: No such file or directory`. No real Bash runtime is installed, so POSIX syntax remains delegated to Linux CI as allowed by the task.
- Plugin `npm ci` — exit `0`.
- Plugin `npm run plugin:validate` — exit `0`; build/schema/bootstrap/package validation passed.
- Plugin `npm run build --if-present` — exit `0`.
- Plugin `npm test` — exit `0`; 49 files, 237 tests passed.
- Plugin `npm run evaluation` — exit `0`; all gates passed.
- Plugin `npm audit --omit=dev` — exit `0`; 0 vulnerabilities. `npm ci` separately displayed development-tree advisories outside the required production audit.
- `git diff --check` — exit `0`.

## Problems and remaining uncertainty

The only validation limitation is the absent real Bash runtime. Blocker type: execution-environment limitation, non-blocking under the task's conditional POSIX validation rule. Narrow safe remedy and recommendation: use the existing Linux CI `sh -n scripts/install.sh` job; do not mutate WSL for this repository-only task.

Live install, clean reinstall, migration, reset, uninstall, Gateway, OpenClaw, and Ollama behavior remain intentionally unproven because this task prohibited live actions.

Human decision required: **NO**.

## Side-effect and duplicate accounting

No matching Task 044 report existed at freshly fetched HEAD. Implementation ran once. No Git worktree was created. No live workspace/config/runtime, plugin registration, installation, clean reinstall, reset, uninstall, Gateway, Ollama, scheduler/service, Procmon evidence, Ecosystem repository, staged-capability-loop, tag, release, archive, or merge was touched. No external side effect was repeated.
