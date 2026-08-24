# CNX-20260824-043 — Harden Namespace Ownership and Migration Gates

Result: **SUCCESS**  
Acceptance result: `PASS_NAMESPACE_OWNERSHIP_HARDENED`  
Implementation commit: `04710b980c6e98fb3a802fa5706a08a22213bd47`  
Branch: `agent/v0.9.3-recovery-reality-tests`

## Work actually performed

- Replaced non-empty ownership checks with an exact schema, value, UTC timestamp, canonical-location, containment, artifact, task/service identity, plugin identity, package-version, and actual-payload verifier.
- Added a fail-closed installation classifier. Fresh, coherent v0.9.3 upgrade, reviewed legacy migration, partial new state, and mixed state are now distinct outcomes. Any individual or combined current artifact without coherent ownership blocks adoption.
- Added deterministic direct-extension and npm-managed plugin discovery. A candidate must carry the exact plugin ID, package name/version, bootstrap, and ticket-store payload; zero or multiple exact candidates fail closed. The verified actual root is written to `ownership.json`.
- Made the Windows and POSIX installers inspect current registration/service identities before mutation, check legacy uninstall exit status, and reject residual registration, config entry, load path, filesystem path, and task/service identity.
- Made clean reinstall classify and verify ownership before its first backup or deletion, derive the cleanup root from verified ownership, and reject registration/task-only partial state.
- Routed reset/uninstall bootstrap resolution through the exact plugin resolver and added zero-mutation mismatch tests.
- Expanded namespace lint across case variants, content and filenames. Current controller IDs, categories, symbols, services, backups, environment names, cleanup output, and cleanup-script names are variant-scoped; legacy literals are limited to named migration code/tests and v0.9.3 migration evidence.

## Before / after ownership rules

Before, several manifest fields were accepted when merely non-empty, plugin discovery could select among generations, partial state could be mistaken for fresh state, and legacy cleanup did not prove all registration/config boundaries. After this change, all manifest fields and allowed identities are exact; paths must be canonical and constrained; the installed plugin candidate must be unique and exact; every current artifact triggers coherent-manifest verification; and legacy removal is an acceptance gate rather than best-effort cleanup.

## Partial-state and legacy-removal proof

Deterministic tests cover every manifest field, missing/extra fields, non-UTC time, traversal/foreign paths, each current artifact independently and in combinations, coherent upgrades, direct/npm plugin roots, identical and conflicting duplicate candidates, PASSTHROUGH/MANAGED/MAINTENANCE legacy modes, and byte-identical HermesAgent/OpenClaw/Ollama sentinels. Installer contract tests prove the classification occurs before install mutation and clean-reinstall backup/deletion. Reset and uninstall tests inject an ownership mismatch and prove confirmation and mutation functions are never called.

The legacy gate now requires successful native uninstall and an empty result for the old plugin in plugin inventory, `plugins.entries.cogentnexus-rotation`, `plugins.load.paths`, generic launcher/skill/state/plugin paths, and old Windows/systemd/launchd identity before migration success.

## Exact changed paths

- `docs/CHECK_SYSTEM.md`
- `scripts/check_namespace_isolation.py`, `scripts/clean-reinstall.ps1`, `scripts/install.ps1`, `scripts/install.sh`, `scripts/manage_agents_policy.py`
- `skills/cogentnexus-openclaw/scripts/host_delivery.py`, `host_stall_v091.py`, `lifecycle_v091.py`, `lifecycle_v092.py`, `namespace_ownership.py`, `validate.py`
- `skills/cogentnexus-openclaw/templates/lifecycle/README.md`, `start-cogentnexus-openclaw.cmd`, `start-cogentnexus-openclaw.sh`, `stop-cogentnexus-openclaw.cmd`, `stop-cogentnexus-openclaw.sh`
- `plugins/cogentnexus-openclaw/scripts/evaluate.mjs`
- `plugins/cogentnexus-openclaw/src/index.ts`, `index.test.ts`, `v084-entry.ts`, `v084.ts`, `v090-abort-authority.ts`, `v090-context-guard.ts`, `v090-context-guard.test.ts`, `v090-entry.ts`, `v090-final-entry.ts`, `v090-native-restart-boundary.ts`, `v090-native-restart-boundary.test.ts`, `v090-owner-reconcile.ts`, `v090-recovery-order.ts`, `v090-recovery-order.test.ts`, `v090-synthetic-payload.ts`, `v090.ts`, `v091-context-guard.ts`, `v091-dashboard-verified-delivery.ts`, `v091-direct-model-call-lease.ts`, `v091-direct-recovery.ts`, `v091-final-entry.ts`, `v091-wiring.test.ts`, `v092-durable-delivery-boundary.ts`, `v095-direct-recovery.ts`, `v095-direct-recovery.test.ts`, `v097-direct-recovery-liveness.ts`, `v098-owner-reconcile-residue.test.ts`, `v099-native-restart-ownership.ts`, `v099-native-restart-ownership.test.ts`
- `tests/test_lifecycle_v092.py`, `tests/test_namespace_install_contract.py`, `tests/test_namespace_lint.py`, `tests/test_namespace_ownership.py`

## Commands and exit codes

- `python scripts/check_namespace_isolation.py` — exit `0`, PASS.
- `python scripts/check_baseline_consistency.py` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/cogent.py self-test` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/runtime.py self-test` — exit `0`, PASS.
- `python skills/cogentnexus-openclaw/scripts/workflow.py self-test` — exit `0`, PASS.
- `python -m compileall -q scripts skills/cogentnexus-openclaw/scripts tests` — exit `0`.
- `python -m pytest -q` — exit `0`; `235 passed, 1 skipped, 4 subtests passed`. The skip is the pre-existing platform-conditional test.
- PowerShell parser over `scripts/install.ps1` and `scripts/clean-reinstall.ps1` — exit `0`, no parser errors.
- `bash -n scripts/install.sh` — exit `1` because the Windows `bash.exe` WSL relay reported `/bin/bash` absent. Bash is not available in this execution environment; no POSIX behavior was claimed from this result.
- `npm ci` — exit `0`.
- `npm run plugin:validate` — exit `0`; build, schema, ticket DB bootstrap, and packed-content validation passed.
- `npm run build --if-present` — exit `0`.
- `npm test` — exit `0`; 49 files and 237 tests passed.
- `npm run evaluation` — exit `0`; all evaluation gates passed.
- `npm audit --omit=dev` — exit `0`; 0 vulnerabilities. (`npm ci` separately displayed development-tree advisories, which are outside the required omit-dev audit.)
- `git diff --check` — exit `0`.

## Proven, failed, skipped, or unproven

Proven: all six required repair groups, deterministic negative/positive behavior, exact installed-path resolution, mutation ordering, namespace isolation, Python/plugin validation, Windows syntax, and repository-only side-effect boundaries.

Failed: none of the acceptance gates.

Skipped/limited: POSIX syntax execution was not possible because this Windows environment has no usable Bash runtime. The exact failed command and evidence are reported above. No live POSIX installation was attempted.

Unproven: live OpenClaw installation/migration/reset/uninstall behavior, intentionally excluded by the repository-only safety gate.

## Problems, blocker classification, and recommendation

Problem observed: unavailable Bash runtime (`WSL ... execvpe(/bin/bash) failed: No such file or directory`).  
Blocker type: environment/tooling limitation, non-blocking under the task's explicit “when Bash is available” rule.  
Narrow safe remedy: let CI execute `sh -n scripts/install.sh` on Linux; do not install or mutate WSL for this task.  
Recommended method: rely on the branch validation workflow's Linux syntax job after publication.  
Human decision required: **NO**.

## Side-effect accounting

All work occurred in the isolated full clone `C:\Users\CDQ-P\AppData\Local\Temp\cnx043-clone-20260824T002614Z`. No Git worktree was created. No live workspace, OpenClaw configuration, Gateway, Ollama, scheduler/service, installation, reset, uninstall, Procmon evidence, Ecosystem repository, tag, release, archive, or merge was touched. The implementation was executed once; no matching report existed at the duplicate fence, and no side effect was repeated.
