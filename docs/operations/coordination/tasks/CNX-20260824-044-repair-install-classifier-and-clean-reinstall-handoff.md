# CNX-20260824-044 — Repair Install Classification and Clean-Reinstall Handoff

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: AUTO  
Predecessor: CNX-20260824-043 (reviewed BLOCKED; retain accepted ownership hardening)

## Objective

Make the CogentNexus-OpenClaw v0.9.3 fresh-install, install-over, and default backup-enabled clean-reinstall composition deterministic and fail closed without treating unrelated OpenClaw npm projects as product state.

Repair only the four bounded findings in the Task 043 review.

## Required repairs

### 1. Product-specific npm inventory

Separate broad plugin search roots from ownership inventory.

The resolver may inspect reviewed direct and npm-managed locations, but the installation classifier must count an npm project/root as CogentNexus-OpenClaw state only when product-specific evidence exists, such as:

- the exact direct extension path;
- the exact npm package child path;
- a wrapper package whose exact dependency/package metadata identifies `openclaw-plugin-cogentnexus-openclaw`;
- an invalid/old/partial package at the exact product child path that must be treated as partial product state.

An unrelated `.openclaw/npm/projects/<other-plugin>` directory, unrelated wrapper package, or unrelated node_modules content must not make the CogentNexus-OpenClaw inventory non-empty and must remain byte-identical.

Do not recursively scan arbitrary node_modules trees.

### 2. Clean-reinstall backup handoff

Make the default backup-enabled `scripts/clean-reinstall.ps1` path compose with `scripts/install.ps1`.

After the verified installation is backed up and removed, the installer must not reject the clean-reinstall operation merely because its own verified backup exists.

Use a narrow, auditable design, for example:

- hold the backup temporarily outside the active application-data root and move it to the final variant-scoped backup location only after successful reinstall; or
- pass and verify a one-use clean-reinstall handoff bound to the prior manifest/workspace/backup identity.

Do not broadly ignore application-data residue. Unknown or unproven current operational residue must still block fresh adoption.

Define failure behavior: preserve the backup and exact recovery information without falsely claiming a fresh installation.

### 3. Skip-plugin preflight

Preserve or explicitly narrow `-SkipPlugin/--skip-plugin` safely.

If exact ownership cannot be completed without installing a plugin, reject the option before the first filesystem/config/runtime mutation. If allowed only for an already coherent upgrade with an existing exact plugin, enforce and test that condition before handoff/copy/init.

Do not create a normal complete ownership manifest or claim MANAGED authority for an incomplete staging layout.

### 4. Verify newly created ownership before enable

Immediately after manifest creation, run the exact manifest/artifact/plugin verifier and require success before policy/runtime MANAGED enable.

A creation/verification failure must leave/request PASSTHROUGH and must not claim installation success.

## Required deterministic tests

Add behavior-level tests for:

- fresh classification with one and multiple unrelated npm project wrappers;
- unrelated direct/npm plugins and nested node_modules remaining byte-identical;
- an exact product package child with missing, corrupt, old-version, or conflicting payload being classified as partial/ambiguous rather than ignored;
- current valid v0.9.3 direct and npm-managed product layouts remaining valid upgrades;
- default backup-enabled clean-reinstall orchestration reaching the installer without a self-created partial-state rejection;
- backup preservation and recovery accounting when reinstall fails;
- unknown application-data residue still blocking ordinary fresh install;
- `-NoBackup` behavior remaining explicit;
- skip-plugin rejection before mutation on fresh/legacy state and allowed behavior, if any, on coherent upgrade;
- post-create exact verify ordering before any `enable`;
- byte-identical CogentNexus-HermesAgent, unrelated OpenClaw plugins/projects, OpenClaw config/user data, and Ollama sentinels.

Do not satisfy these only with source-string ordering; exercise classifier/orchestration behavior with mocks or temporary layouts.

## Validation

Run and report:

- namespace-isolation lint;
- baseline consistency;
- Python compile/self-tests and full Python suite;
- PowerShell parser validation;
- POSIX syntax validation when a real shell is available;
- plugin install/validation/build/tests/evaluation/production audit;
- `git diff --check`;
- exact changed-path and side-effect accounting.

## Exclusions and safety

Repository-only work in one isolated full clone of freshly fetched branch HEAD.

Do not:

- create/register a Git worktree;
- touch the operator's live workspace, OpenClaw config, Gateway, Ollama, scheduler/service, installation, clean reinstall, reset, uninstall, or retained Procmon evidence;
- repeat the Task 042 rename or Task 043 ownership hardening wholesale;
- touch `CogentNexus-Ecosystem` or `staged-capability-loop`;
- merge, tag, publish a GitHub Release, or create a release archive.

## Acceptance gate

Return `PASS_INSTALL_CLASSIFIER_AND_REINSTALL_HANDOFF` only if all four repairs and all required behavior tests pass with no unrelated change and no live side effect.

Otherwise return:

- `BLOCKED_UNRELATED_NPM_FALSE_POSITIVE`
- `BLOCKED_CLEAN_REINSTALL_SELF_CONFLICT`
- `BLOCKED_SKIP_PLUGIN_PARTIAL_MUTATION`
- `BLOCKED_POST_CREATE_OWNERSHIP_UNVERIFIED`
- `BLOCKED_VALIDATION_FAILURE`
- `BLOCKED_PUBLICATION_UNSAFE`

## Publication

Use a commit message beginning:

`fix: compose CogentNexus-OpenClaw install ownership gates`

Publish one matching report only at:

`docs/operations/coordination/reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`

Report exact changed paths, classifier evidence rules, unrelated npm fixtures, clean-reinstall backup/handoff lifecycle, skip-plugin decision, post-create verification, commands/results, implementation SHA, remaining uncertainty, and side-effect accounting.

## Duplicate fence and progress

Freshly fetch the branch. If the matching Task 044 report already exists, do not repeat implementation or publish a duplicate.

Report meaningful progress approximately every 3 minutes and immediately after classifier repair, clean-reinstall composition, skip-plugin preflight, post-create verification, full validation, and publication/blocker. Progress reports are not pause points.
