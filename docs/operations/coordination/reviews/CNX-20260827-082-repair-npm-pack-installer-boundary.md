# Review — CNX-20260827-082 Repair npm Pack Installer Boundary

Decision: `ACCEPT`

Disposition: `ACCEPT_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

Reviewed report HEAD: `34057308f75cb7334c83e253b3077358d05918fd`

Execution HEAD: `52c86bc756f57cd8ee8c1806ba2f26cc59cb8639`

Implementation HEAD: `df412ed10522d79a722e1b48d681e7553cb79ae2`

## Publication fence

Independent compare confirms:

- execution -> implementation: exactly one commit;
- implementation changes only `scripts/install.ps1`, new `scripts/resolve-npm-pack-artifact.ps1`, and new `tests/test_npm_pack_installer_boundary.py`;
- implementation -> report: exactly one report-only commit;
- no live-state repair, semantic source change, provider change, or unrelated product source is hidden in the publication lineage.

## Root-cause acceptance

Task 081 failed at the supported installer boundary after `npm pack --json` because `install.ps1` treated the parsed value as though the first item directly contained `.filename`.

Task 082 reproduced the exact incompatibility instead of guessing:

- Windows PowerShell `5.1.19041.6456`;
- npm 11.16.0 / Node 24.18.0 emits a one-element array;
- npm 12.0.2 / Node 22.23.2 emits a one-entry object keyed by package name;
- the pre-fix PowerShell parser run against the captured npm-12 output produced one `PSCustomObject` whose direct `.filename` was empty and reproduced the Task-081 failure.

This is consistent with the repository's existing package verifier, which already normalizes the npm-11 array and npm-12 keyed-object shapes.

## Source review

The new `Resolve-NpmPackArtifact` helper is accepted as a sufficiently narrow production boundary.

It:

- parses JSON once through the production Windows PowerShell path;
- accepts exactly one npm-11 array item or exactly one npm-12 keyed-object value;
- rejects null, zero/multiple entries, unsupported shapes, invalid/missing filenames;
- rejects rooted paths, separators, traversal-capable names and unsafe Windows filename characters;
- requires a `.tgz` artifact;
- resolves the candidate under the plugin directory and verifies it exists;
- returns the exact path consumed by `openclaw plugins install`.

`install.ps1` invokes the helper immediately after successful `npm pack --json`, before rollover planning, passes only the helper-returned artifact to `openclaw plugins install`, and preserves exact-artifact cleanup in `finally`.

No arbitrary `*.tgz` directory scan was introduced; stale unrelated tarballs cannot become package authority merely by existing.

## TDD / compatibility evidence accepted

The task recorded RED before production repair and then GREEN through the production helper boundary.

Accepted evidence includes:

- initial focused RED: `4 failed, 2 passed`;
- final focused boundary suite: `6 passed`;
- real PowerShell 5.1 harness accepting captured npm-11 and npm-12 outputs;
- real generated artifact identity under both toolchains;
- identical artifact size/hash across npm-11/npm-12 evidence;
- Node 24/npm 11: 49 plugin files / 257 tests passed + plugin validation;
- Node 22/npm 12: 49 plugin files / 257 tests passed + plugin validation;
- full Python: `362 passed, 2 skipped, 4 subtests passed`;
- targeted installer/recovery/npm-pack: `58 passed`;
- baseline consistency PASS;
- `git diff --check` PASS.

## Minor non-blocking review note

One Python wiring assertion searches `install.ps1` for `Test-Path -LiteralPath $packagePath`; that textual occurrence is in the cleanup boundary rather than the helper's existence validation. This does not invalidate the production contract because missing-artifact behavior is executable-tested through the exact production helper and installer wiring proves that helper is the artifact authority before plugin installation. No rework is required for this test-quality note.

## Live-state preservation

Task 082 correctly did not normalize the Task-081 partial installation.

The reported read-only state remains:

- ownership verification passes;
- recovery preflight `OWNERSHIP_PRESENT`;
- classification `upgrade`;
- controller `passthrough`, generation 13;
- AGENTS managed markers absent;
- canonical v0.9.3 plugin generation disabled;
- Supervisor absent;
- SQLite integrity `ok`, zero Tickets/outbox;
- Gateway remains present.

This state is not MANAGED acceptance. It is the authorized starting state for the next supported recovery task.

## Successor authorization

The corrected production candidate for recovery is now exactly:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

A successor may perform exactly one supported normal install-over from that source onto the current Task-081 partial PASSTHROUGH installation.

It must not uninstall/reset/clean/manual-repair first. It must restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior, prove source/live parity and ownership/runtime/Gateway/Ollama/SQLite health, observe at least five natural PT1M ticks with no-flash evidence, and prove/prepare the Dashboard/WebChat owner surface without sending a semantic prompt.

Final semantic acceptance remains separately gated and must consume exactly one fresh authenticated owner message only after recovery is independently accepted.
