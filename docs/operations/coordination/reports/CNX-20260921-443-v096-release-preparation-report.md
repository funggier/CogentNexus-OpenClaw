# CNX-20260921-443 — v0.9.6 Release Preparation Report

Status: `LOCAL_GATES_GREEN / PRE_CANDIDATE_FREEZE`

Classification:

`CNX443_V096_LOCAL_RELEASE_GATES_GREEN`

Date: 2026-09-21

Repository: `funggier/CogentNexus-OpenClaw`

Working branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Pre-freeze committed HEAD at qualification start:

`6dfa126ef267f934bfffb78a617e547ecc473d98`

## Objective

Prepare the complete CogentNexus-OpenClaw v0.9.6 release candidate without losing the existing uncommitted release work, converge current-facing documentation, add MIT licensing, validate source/runtime/package contracts, then freeze one exact candidate for GitHub validation and publication.

This report is a pre-publication checkpoint. It does **not** classify v0.9.6 as published.

## Worktree preservation

At the start of this continuation the release-preparation work remained intentionally uncommitted:

- 56 modified tracked files;
- 3 untracked files;
- 0 staged files;
- 0 conflicts.

The untracked release files were:

- `LICENSE`;
- `docs/releases/v0.9.6.md`;
- `docs/operations/coordination/tasks/CNX-20260921-443-documentation-license-v096-release.md`.

No `git reset`, `git checkout`, or `git restore` was used to reconstruct or discard the v0.9.6 worktree.

## Manifest diff cleanup

`plugins/cogentnexus-openclaw/openclaw.plugin.json` initially showed a large formatting diff after JSON rewriting.

A normalized semantic comparison against committed HEAD proved exactly one semantic difference:

```text
SEMANTIC_DIFF_COUNT=1
version: 0.9.5 -> 0.9.6
```

The file was rewritten from the committed textual layout with only that version literal changed. The resulting manifest diff is one deletion plus one insertion and retains all prior schema content.

## Documentation and release-state convergence

Current-facing documentation now consistently distinguishes:

- current source/release line: v0.9.6;
- latest physical OpenClaw acceptance: `2026.9.5 (ec9c1a1)`;
- regression/dev dependency pin: `2026.7.1-2`;
- managed local-provider ownership: Ollama;
- Cloud/provider/model/auth routing: OpenClaw-owned pass-through;
- current CNX-443 coordination from preserved historical evidence;
- retired `CogentNexus coordination watch` from current execution authority.

Historical v0.9.4/v0.9.5 tasks, reports, reviews, and releases remain historical evidence rather than being rewritten as if they were created for v0.9.6.

The root MIT `LICENSE` is present with:

`Copyright (c) 2026 funggier`

and current README/license references have been updated.

## Version identity

Local metadata verification reports:

```text
VERSION=0.9.6
package=0.9.6
manifest=0.9.6
lock=0.9.6
lockRoot=0.9.6
openclawDev=2026.7.1-2
RELEASE_NOTES_EXISTS=True
```

The OpenClaw development dependency was intentionally **not** changed to 2026.9.5. The newer 2026.9.5 value is physical runtime acceptance evidence, not the regression/dev dependency baseline.

## Namespace compatibility repair

The runtime attestation RPC literal:

`cogentnexus.runtimeAttestation`

remains intact because it is a real compatibility identifier.

The namespace checker exception remains narrow:

- `plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.ts`;
- `plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.test.ts`.

A regression test proves the literal remains rejected outside those exact surfaces.

## CNX-383 release repair

The supported Windows installer now projects the executable conversation-hook requirement into OpenClaw configuration:

```text
openclaw config set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess true
```

and fails closed if that enforcement fails.

The historical intentionally RED CNX-383 projection test was converted into a real contract that verifies both executable policy and supported installer projection.

Fresh plugin validation proves this release no longer carries the old `427 PASS / 1 RED` baseline.

## Deterministic test repairs

The v0.9.6 worktree also carries release-relevant deterministic test maintenance:

- OpenClaw 2026.9.x startup-grace unit tests explicitly mock inactive startup grace rather than reading live boot state;
- single-authority source assertion follows the production `effectiveMode` boundary;
- namespace/plugin-generation fixtures use `ownership.INSTALLED_VERSION` instead of hard-coded v0.9.5 where appropriate;
- lifecycle/current-doc/provider/install contracts were updated for the v0.9.6 current-state model.

These changes were reviewed rather than reverted blindly.

## Local qualification evidence

### Python and repository gates

Full Python suite:

```text
708 passed, 5 skipped, 38 subtests passed
```

Repository gates:

- namespace isolation: PASS;
- v0.9.6 baseline consistency: PASS;
- skill validation: PASS;
- Cogent self-test: PASS;
- runtime self-test: PASS;
- workflow self-test: PASS;
- Python compile set from current validation workflow: PASS;
- benchmark validator self-test: PASS;
- Windows PowerShell syntax validation: PASS;
- PowerShell 5.1 acceptance serializer self-test: PASS;
- exact numeric root-process exit capture self-test: PASS.

### Plugin dependency install

A first local dependency-install path encountered a Windows `EBUSY` lock under generated `node_modules/openclaw`.

Investigation bound the stale process tree to the LConnect-owned `npm ci` invocation. Only that process tree and generated plugin `node_modules` directory were removed.

Git status entry count was checked immediately before and after generated-dependency cleanup:

```text
before = 59
after  = 59
```

No tracked/untracked v0.9.6 source or documentation work was removed.

A clean managed `npm ci` then completed:

```text
added 352 packages, and audited 353 packages
exit 0
```

### Plugin tests

Fresh v0.9.6 Vitest result:

```text
Test Files  91 passed (91)
Tests       428 passed (428)
exit 0
```

CNX-383 is included in the GREEN suite.

### Evaluation

`npm run evaluation` completed successfully.

Measured gate summary:

- database integrity: true;
- interruption recovery: true;
- bounded retry: true;
- duplicate suppression: true;
- retrieval precision: true;
- retrieval recall: true;
- provenance: true;
- latency: true;
- overall `passed`: true.

Evaluation evidence SHA-256:

`c389b7abead0acf07457fb6e8e0a22e87eb616f166dad9fe0f977f209f9308ea`

### Production dependency audit

```text
npm audit --omit=dev
found 0 vulnerabilities
```

### Plugin/package validation

`npm run plugin:validate` completed with exit 0:

- TypeScript/plugin build: PASS;
- canonical dist text normalization: PASS;
- mixed-plugin artifact/schema verification: PASS;
- 46 config properties;
- 5 tools;
- Ticket DB bootstrap: PASS;
- 9 required tables plus v0.9.5 registration fence;
- package-content verification: PASS;
- internal `npm pack --dry-run --json`: PASS;
- packed file count: 290;
- required release plugin files present.

### Markdown local-link audit

A read-only audit covered 28 current-facing Markdown files, including the root/operator/current-state/installation/provider/coordination/plugin/skill/release/task surfaces.

Result:

```text
CURRENT_FACING_FILES=28
BROKEN_CURRENT_LOCAL_LINKS=0
```

### Whitespace gate

The first final `git diff --check` found Markdown trailing spaces in six current-facing files. Those exact trailing spaces were removed without changing document semantics.

Rerun result:

```text
DIFFCHECK_EXIT=0
```

Windows LF/CRLF conversion warnings are informational and are not whitespace errors.

## Release topology review

Historical v0.9.5 publication used a merged `main` commit:

`50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`

The current v0.9.6 authority is different:

- CNX-443 requires an exact frozen candidate SHA;
- the current roadmap requires freeze/push, exact-candidate GitHub checks, then publication against that candidate;
- current project status says release publication uses `.github/workflows/release.yml` with an exact validated candidate SHA;
- `release.yml` validates a 40-hex `candidate_sha`, checks out that exact SHA, reruns release gates, and creates `v0.9.6` with `--target` set to that SHA;
- no current v0.9.6 authority requires a PR or merge to `main` before publication.

Therefore this preparation does not introduce an unrequired PR/merge merely to reproduce v0.9.5 history. The authoritative publication identity will be the exact committed/pushed candidate that passes GitHub validation.

## Local verdict

All currently executable local release gates are GREEN. A final candidate-sensitive rerun after adding this CNX-443 evidence also completed GREEN: full Python remained `708 passed, 5 skipped, 38 subtests passed`; plugin tests remained `428/428`; evaluation remained passed; production audit remained `0 vulnerabilities`; and `plugin:validate` remained PASS with 290 packed files.

Classification:

`CNX443_V096_LOCAL_RELEASE_GATES_GREEN`

This is **not** the final CNX-443 success classification because the candidate has not yet been committed/pushed, GitHub exact-candidate CI has not yet been accepted, and v0.9.6 has not yet been published or independently verified.

## Remaining exact-candidate sequence

1. include this report/task checkpoint in the release-preparation worktree;
2. rerun candidate-sensitive validation affected by final documentation edits;
3. commit the complete v0.9.6 release candidate;
4. verify a clean candidate worktree and freeze exact SHA;
5. push without force;
6. verify local HEAD equals remote branch HEAD;
7. require exact-candidate GitHub validation to complete GREEN;
8. dispatch `.github/workflows/release.yml` with `version=0.9.6` and the exact candidate SHA;
9. verify public tag target, release state, tar.gz, zip, `SHA256SUMS.txt`, and release notes;
10. independently download and verify release checksums;
11. only after public verification update CNX-443, `ACTIVE.md`, and `STATUS.md` to COMPLETE in a post-release coordination commit newer than the immutable v0.9.6 tag.
