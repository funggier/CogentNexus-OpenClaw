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

Full Python suite before live install-over repair:

```text
708 passed, 5 skipped, 38 subtests passed
```

Full Python suite after the v0.9.5 -> v0.9.6 upgrade-source repair:

```text
709 passed, 5 skipped, 38 subtests passed
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

`11b6183a25fdb31436527672aacf1efd5e4e98a1252c429763f9ce179b773279`

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

## Live install-over defect found before publication

The first frozen local candidate was:

`12cdea0473146bd114826e496f51ca8a8b93518c`

It was intentionally **not pushed** after live install-over qualification found a real v0.9.6 upgrade blocker. Installing over the accepted live v0.9.5 runtime failed before mutation with:

```text
ownership manifest mismatch; refusing mutation:
installedVersion actual 0.9.5 expected 0.9.6
```

The live runtime remained on the accepted v0.9.5 installation and the installer failed closed.

TDD reproduction added an exact v0.9.5-owned installation fixture. The new test reproduced the same mismatch RED. Root cause was that v0.9.6 updated `INSTALLED_VERSION` to `0.9.6` while `UPGRADE_FROM_VERSIONS` still contained only `0.9.4`.

Minimal repair:

```python
UPGRADE_FROM_VERSIONS = ("0.9.4", "0.9.5")
```

Focused post-repair qualification:

```text
117 passed, 1 skipped
```

covering namespace ownership, namespace install contract, and plugin generation rollover.

Candidate `12cdea04...` is therefore rejected and must never be used for v0.9.6 publication. Full requalification after the repair is now GREEN: repository gates PASS, Python `709 passed, 5 skipped, 38 subtests passed`, plugin tests `428/428`, evaluation passed, production audit `0 vulnerabilities`, and `plugin:validate` PASS. A new exact candidate will be frozen next and must pass live install-over / clean-reinstall / reset acceptance before publication.

## Live clean-reinstall backup defect found before publication

The next frozen candidate was:

`ade5fa7faac5f592246f58816c5f580de4ec04f7`

Live install-over from the accepted v0.9.5 installation to this v0.9.6 candidate completed successfully on OpenClaw 2026.9.5. Installed ownership and plugin metadata both reported v0.9.6, selected installed plugin artifacts matched repository SHA-256 values, controller mode returned to `active/managed`, generation advanced to 131, Gateway and Ollama were healthy, supervisor startup was Ready, and pending outbox was zero.

The subsequent clean-reinstall acceptance exposed a second pre-release blocker in the backup stage. The live application-data root contains external archive junctions:

- `backups -> T:\CogentNexus\CogentNexus-OpenClaw\backups`
- `plugin-generation-rollover-backups -> T:\CogentNexus\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

The original `Copy-Item -Recurse` application-data backup followed those junctions and began copying already-external T: backup archives into a new T: clean-reinstall backup. The run was stopped before `Backup created` and before any destructive mutation. Post-stop live verification still showed v0.9.6 `active/managed`, generation 131, healthy Gateway, and pending outbox zero.

A regression contract was added RED-first. The minimal repair adds an application-data backup helper that copies active top-level children while explicitly skipping `[IO.FileAttributes]::ReparsePoint` entries. Focused post-repair qualification is GREEN:

```text
122 passed, 1 skipped
```

covering clean-reinstall, namespace install/ownership, and plugin rollover contracts. Candidate `ade5fa7f...` is therefore rejected for publication and a new exact candidate is required after full requalification and renewed live lifecycle acceptance.

## Local verdict

All currently executable local release gates are GREEN after both live-found repairs. The current requalification completed with focused clean-reinstall/namespace/rollover coverage `122 passed, 1 skipped`, full Python `709 passed, 5 skipped, 38 subtests passed`, plugin tests `428/428`, evaluation passed with evidence SHA-256 `8f50eaefe8ecce4f0c94fdfefc15d04e46df61d7985f5a673cfe2e84838f5cb2`, production audit `0 vulnerabilities`, and `plugin:validate` PASS with 290 packed files.

Classification:

`CNX443_V096_LOCAL_RELEASE_GATES_GREEN`

This is **not** the final CNX-443 success classification because a new post-repair candidate has not yet been frozen, renewed live install-over / clean-reinstall / reset acceptance is still required, GitHub exact-candidate CI has not yet been accepted, and v0.9.6 has not yet been published or independently verified.

## Remaining exact-candidate sequence

1. include this report/task checkpoint in the release-preparation worktree;
2. rerun final candidate-sensitive validation affected by the evidence edits;
3. commit the complete post-repair v0.9.6 release candidate and freeze exact SHA;
4. require renewed live install-over / clean-reinstall / reset lifecycle acceptance against that exact SHA;
5. verify the live installed artifacts and OpenClaw 2026.9.5 health after each destructive lifecycle stage;
6. push the exact accepted candidate without force;
7. verify local HEAD equals remote branch HEAD;
8. require exact-candidate GitHub validation to complete GREEN;
9. dispatch `.github/workflows/release.yml` with `version=0.9.6` and the exact candidate SHA;
10. verify public tag target, release state, tar.gz, zip, `SHA256SUMS.txt`, and release notes;
11. independently download and verify release checksums;
12. only after public verification update CNX-443, `ACTIVE.md`, and `STATUS.md` to COMPLETE in a post-release coordination commit newer than the immutable v0.9.6 tag.
