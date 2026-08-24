# Review — CNX-20260824-042

Decision: `BLOCKED`  
Reviewer: ChatGPT  
Reviewed report: [`reports/CNX-20260824-042-openclaw-namespace-isolation.md`](../reports/CNX-20260824-042-openclaw-namespace-isolation.md)  
Implementation commit: `d0a692331b2e9f29fc9b318fcd7beac5d5acf4bb`

## Accepted implementation

The product-wide rename is substantial and internally coherent:

- the current command, skill, plugin, state root, tool, service/task, package, release archive, and display namespaces identify CogentNexus-OpenClaw;
- root and plugin metadata are v0.9.3;
- release notes document the intentional API/installation-layout break;
- the implementation is one commit directly after the reviewed Task 042 coordination commit;
- repository validation reported 208 Python tests plus 4 subtests and 237 plugin tests passing;
- no live installation, runtime, Procmon evidence, tag, or Release was mutated.

These results are retained and must not be reimplemented wholesale.

## Blocking findings

The task result `PASS_OPENCLAW_NAMESPACE_ISOLATED` is not accepted yet because the destructive and migration boundaries do not fully satisfy the task's fail-closed contract.

1. `namespace_ownership.verify_manifest()` compares only schema, product ID, display name, plugin ID, state root, and optional workspace. It merely checks that version, skill path, plugin path, launcher path, and timestamp are non-empty strings. It does not verify their exact canonical values, supported version, path containment/existence, task/service identities, timestamp validity, or migration-source contract before reset/uninstall mutation.

2. `prove_legacy_ownership()` returns `fresh` whenever no legacy artifact exists, even if one or more incomplete new-namespace artifacts already exist. A new skill, launcher, state fragment, or plugin without a valid ownership manifest can therefore be treated as fresh and replaced.

3. `scripts/clean-reinstall.ps1` verifies the ownership manifest only when `.cogentnexus-openclaw` exists. If the root/manifest is absent but the new skill, launcher, or extension exists, the script can back up and remove those paths without proven ownership.

4. Both installers hard-code the manifest plugin path as `.openclaw/extensions/cogentnexus-openclaw`. The repository itself supports OpenClaw npm-managed installations below `.openclaw/npm/projects/.../node_modules/openclaw-plugin-cogentnexus-openclaw`; therefore the recorded ownership path can be false for the normal npm-pack layout.

5. Legacy plugin removal is not acceptance-gated. PowerShell does not check the legacy uninstall exit code, POSIX explicitly ignores it with `|| true`, and neither path proves that the legacy plugin/config/load path is absent before reporting migration success and deleting legacy files.

6. The namespace lint is too narrow and case-sensitive for the task contract. Current operational examples that escape the explicit variant name still pass, including `cogentnexus-<timestamp>` backup names, `cogentnexus-uninstall-<pid>.cmd`, and user-facing `COGENTNEXUS RESET/UNINSTALL: PASS`.

These are acceptance blockers because Task 042 explicitly requires ownership-manifest-bounded destructive actions, rejection of partial/mixed state, exact plugin/path ownership, verified legacy removal, and complete current namespace linting.

## Disposition

Preserve implementation commit `d0a692331b2e9f29fc9b318fcd7beac5d5acf4bb`. Repair only the bounded ownership, partial-state, plugin-path, legacy-removal, and lint defects in the successor task.

No live install, migration, reset, uninstall, OpenClaw/Ollama lifecycle action, tag, Release, or Ecosystem work is authorized by this review.

Human decision required: NO
