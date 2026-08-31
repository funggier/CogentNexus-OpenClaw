# CNX-20260824-043 — Harden Namespace Ownership and Migration Gates

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: AUTO  
Predecessor: CNX-20260824-042 (reviewed BLOCKED; retain its namespace implementation)

## Objective

Repair the narrow acceptance blockers in the CogentNexus-OpenClaw v0.9.3 namespace implementation without repeating the product-wide rename.

Return a repository implementation in which install, migration, clean reinstall, reset, and uninstall prove exact CogentNexus-OpenClaw ownership and fail closed on partial, mixed, corrupt, ambiguous, or foreign state.

## Required repairs

### 1. Exact ownership-manifest validation

Strengthen the manifest schema and verifier so every destructive or ownership-claiming path validates at least:

- schema version;
- exact `productId`, display name, installed version, workspace, state root, skill path, launcher path, plugin ID and actual installed plugin path;
- exact allowed task/service identities;
- a parseable UTC installation timestamp;
- a constrained migration source: null/fresh or the reviewed legacy CogentNexus-OpenClaw source;
- canonical path containment and expected-location rules;
- required owned artifacts appropriate to the action.

A non-empty string is not proof. Reject tampering of every required field. Do not follow a manifest path to delete an arbitrary location.

### 2. Partial-new-state rejection

Inventory both legacy and new namespaces before mutation.

A fresh install is allowed only when no legacy artifact and no existing new operational artifact is present. If any new launcher, skill, state root/manifest, plugin registration/path, task/service identity, or owned application-data residue exists without a coherent verified installation, return a precise partial/mixed-state blocker.

Upgrade of a current v0.9.3 installation requires a valid manifest. Do not silently adopt or replace unowned same-name paths.

### 3. Actual installed plugin identity/path

After plugin installation, resolve the actual installed package root deterministically for both:

- direct extension layout; and
- OpenClaw npm-managed project layout.

Verify the plugin manifest ID, npm package name/version, and non-ambiguous payload. Record the actual verified root in `ownership.json`. Reject missing, conflicting, or ambiguous same-version candidates.

Clean reinstall, reset, repair, and uninstall must use a verified plugin identity boundary and must not remove another npm project or plugin.

### 4. Legacy-removal acceptance gate

Legacy migration must fail if removal of `cogentnexus-rotation` registration/config/load path fails.

After removal, perform a read-only inventory proving the old plugin registration/load path, generic skill, generic launcher, generic state root, and old task/service identity are absent before reporting migration success.

Do not ignore the legacy plugin uninstall exit code. Preserve the versioned migration backup and write an exact recovery report while remaining/requesting PASSTHROUGH if the gate fails.

### 5. Clean-reinstall fail-closed boundary

If any current CogentNexus-OpenClaw artifact exists, require a valid ownership manifest before backup or deletion. Missing state root or manifest while a skill/launcher/plugin/application-data/task artifact exists is a blocker, not a fresh install.

The cleanup set must be derived from reviewed canonical ownership rules and must preserve byte-identical HermesAgent and unrelated OpenClaw/Ollama sentinels.

### 6. Complete current namespace lint

Make the scanner catch case-insensitive bare/generic current product identifiers across operational paths, filenames, user-facing output, backups, temporary cleanup scripts, logs, tasks/services, and package artifacts.

Rename current generic examples, including:

- variant-generic skill backup names;
- the Windows uninstall cleanup script basename;
- `COGENTNEXUS RESET: PASS` and `COGENTNEXUS UNINSTALL: PASS`.

Legacy literals remain allowed only in narrowly named migration code/tests and v0.9.3 migration documentation. Do not broaden the allowlist.

## Required tests

Add deterministic negative and positive tests covering:

- tampering of every manifest field;
- foreign/path-traversal/out-of-bound manifest paths;
- missing/invalid ownership manifest with each partial new artifact independently and in combinations;
- direct-extension and npm-managed plugin layouts, including equal-version conflicting payloads;
- legacy plugin uninstall failure and residual registration/load-path detection;
- clean-reinstall refusal before any backup/deletion when ownership is incomplete;
- reset/uninstall refusal with zero state change on ownership mismatch;
- namespace-lint negative fixtures for case variants and generic operational filenames;
- install-over success from PASSTHROUGH/MANAGED/MAINTENANCE legacy state;
- byte-identical CogentNexus-HermesAgent and unrelated OpenClaw/Ollama sentinels.

Update existing source-contract tests so they prove behavior/results, not only string ordering.

## Validation

Run and report:

- namespace-isolation lint;
- baseline consistency;
- Python compile and all self-tests;
- full Python suite;
- PowerShell parser validation;
- POSIX syntax validation when Bash is available, otherwise state the exact environment limitation;
- plugin `npm ci`, validation/build, full tests, evaluation, and `npm audit --omit=dev`;
- `git diff --check` and changed-path accounting.

## Exclusions and safety

Repository-only work in one isolated full clone of freshly fetched branch HEAD.

Do not:

- create/register a Git worktree;
- touch the operator's live workspace, OpenClaw config, Gateway, Ollama, scheduler/service, reset, uninstall, installation, or retained Procmon evidence;
- repeat Task 041/042 wholesale;
- touch `CogentNexus-Ecosystem` or create/move `staged-capability-loop`;
- create a tag, GitHub Release, or published archive;
- merge the branch.

## Acceptance gate

Return `PASS_NAMESPACE_OWNERSHIP_HARDENED` only if all six required repair groups are implemented, all repository validation is green, the implementation contains no unrelated change, and no live side effect occurred.

Otherwise return an exact blocker:

- `BLOCKED_MANIFEST_VALIDATION_INCOMPLETE`
- `BLOCKED_PARTIAL_STATE_UNSAFE`
- `BLOCKED_PLUGIN_OWNERSHIP_AMBIGUOUS`
- `BLOCKED_LEGACY_REMOVAL_UNPROVEN`
- `BLOCKED_NAMESPACE_LINT_INCOMPLETE`
- `BLOCKED_VALIDATION_FAILURE`
- `BLOCKED_PUBLICATION_UNSAFE`

## Publication

Use a commit message beginning:

`fix: harden CogentNexus-OpenClaw namespace ownership`

Publish one matching report only at:

`docs/operations/coordination/reports/CNX-20260824-043-harden-namespace-ownership-and-migration.md`

Report exact changed paths, before/after ownership rules, actual plugin-path resolution, partial-state matrix, legacy-removal proof, namespace-lint findings, commands/results, implementation commit SHA, remaining uncertainty, and side-effect accounting.

## Duplicate fence and progress

Freshly fetch the branch before work. If the matching Task 043 report already exists, do not repeat implementation or publish a duplicate.

Report meaningful progress approximately every 3 minutes and immediately after ownership schema, partial-state gate, plugin resolution, legacy-removal gate, clean-reinstall boundary, namespace lint, full validation, and publication/blocker. Progress reports are not pause points.
