# Review — CNX-20260824-043

Decision: `BLOCKED`  
Reviewer: ChatGPT  
Reviewed report: [`reports/CNX-20260824-043-harden-namespace-ownership-and-migration.md`](../reports/CNX-20260824-043-harden-namespace-ownership-and-migration.md)  
Implementation commit: `04710b980c6e98fb3a802fa5706a08a22213bd47`

## Accepted implementation

Retain Task 043's improvements:

- exact manifest field, canonical-path, timestamp, version, task/service identity, artifact, plugin-ID/package/payload verification;
- fail-closed partial current-state handling for the tested canonical artifacts;
- exact direct-extension/npm-managed plugin payload resolution and ambiguity rejection;
- checked legacy plugin uninstall and residual registration/config/load-path gates;
- ownership-gated reset/uninstall and clean-reinstall preflight;
- case-insensitive filename/content namespace lint and variant-scoped operational names;
- reported repository suites: 235 Python tests plus 4 subtests and 237 plugin tests;
- no live installation, runtime, destructive, Ecosystem, tag, Release, or merge action.

These repairs must not be reimplemented wholesale.

## Blocking findings

The reported `PASS_NAMESPACE_OWNERSHIP_HARDENED` result is not accepted yet because the installation classifier and clean-reinstall composition contain deterministic false-positive/late-failure paths.

### 1. Unrelated npm projects are classified as CogentNexus-OpenClaw state

`plugin_candidate_roots()` intentionally returns every directory below `.openclaw/npm/projects` plus its possible package child so the resolver can inspect them.

`current_inventory()` then records every returned candidate merely when that directory exists, without first proving that it is a CogentNexus-OpenClaw wrapper or package. Therefore an unrelated OpenClaw npm-managed plugin project makes `inventory["new"]` non-empty. `classify_install()` then attempts CogentNexus-OpenClaw manifest verification and blocks an otherwise valid fresh installation.

The resolver test for a deeply nested unrelated package does not cover this classifier behavior.

### 2. Default clean-reinstall backup blocks its own reinstall

The default clean-reinstall backup is created under:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\clean-reinstall-backups`

The cleanup removes the workspace state/skill/launcher/plugin but preserves that backup. It then invokes `install.ps1`.

The installer classifies the existence of the enclosing `%LOCALAPPDATA%\CogentNexus-OpenClaw` root as a current application-data artifact. With the manifest/state already removed, it treats the post-cleanup state as partial and refuses the reinstall. Thus the default backup-enabled clean-reinstall path can deterministically block itself.

### 3. Skip-plugin staging can fail after mutation

`-SkipPlugin/--skip-plugin` remains advertised as a staging option, but both installers unconditionally run exact plugin resolution after copying/initializing the skill and creating the launcher. On a fresh or legacy source without an already installed exact v0.9.3 plugin, this fails only after repository-owned workspace mutation and leaves a partial installation.

The option must either be rejected before the first mutation for states where exact plugin ownership cannot be completed, or be given an explicitly modeled safe staging contract that cannot claim complete ownership/MANAGED authority.

### 4. Manifest is not verified after creation and before enable

The installers resolve a plugin and write `ownership.json`, then proceed toward `enable` without running the exact verifier against the newly created installation. Task 043's central contract requires the complete exact ownership boundary to be proven before MANAGED authority is claimed.

## Disposition

Preserve implementation commit `04710b980c6e98fb3a802fa5706a08a22213bd47`. Repair only classifier product-identification, backup/reinstall handoff, skip-plugin preflight/staging behavior, and post-create manifest verification.

No live installation, migration, clean reinstall, reset, uninstall, OpenClaw/Ollama action, tag, Release, or Ecosystem work is authorized by this review.

Human decision required: NO
