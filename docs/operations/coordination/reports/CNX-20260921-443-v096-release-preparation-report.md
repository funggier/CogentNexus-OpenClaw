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

## Live fresh-install activation transient found before publication

The next frozen candidate was:

`a4aa49f8ec1ec290aa0da6b847fed2be70891052`

Its clean-reinstall backup repair worked in the live path: both external application-data junctions were explicitly skipped and the bounded backup completed successfully at `T:\CogentNexus-OpenClaw-Release-Acceptance-Backups\20260921-195319`. The existing managed runtime then disabled to PASSTHROUGH successfully, the plugin and owned paths were removed, and a fresh v0.9.6 installation recreated ownership/plugin/runtime state.

The fresh install then failed before MANAGED authority commit while enabling the CNX plugin. OpenClaw 2026.9.5 returned a transient Gateway `ETIMEDOUT` during `plugins enable`. Transactional activation correctly rolled back to PASSTHROUGH and restored the native Gateway healthy. Post-rollback verification showed OpenClaw/Gateway 2026.9.5 healthy, v0.9.6 ownership/plugin artifacts present, and the CNX plugin disabled.

Root cause: the activation path already had a bounded OpenClaw 2026.9.x native-Gateway readiness primitive, but used it only during native rollback/restore. The normal pre-commit activation path did not wait for Gateway readiness after staging configuration/startup and before `plugin_enabled(True)`.

A RED-first activation contract reproduced the missing readiness call. Minimal repair now requires `_wait_native_gateway_ready()` after startup-adapter staging and before plugin activation. MANAGED authority remains uncommitted during the wait and the path still fails closed if readiness does not converge.

Focused post-repair qualification:

```text
10 passed
```

covering activation safety, single-authority ordering, OpenClaw 2026.9.5 native-Gateway readiness, and plugin mutation timeout behavior. Candidate `a4aa49f8...` is rejected for publication. Full requalification after the readiness repair is now GREEN: full Python `710 passed, 5 skipped, 38 subtests passed`; plugin tests `428/428`; evaluation PASS with evidence SHA-256 `a2e96fbf5d3623385751259273e83576c69f880768cee59ec72066351c0b1e0c`; production audit `0 vulnerabilities`; and `plugin:validate` PASS with 290 packed files. A new exact candidate is required for renewed lifecycle acceptance.

## Renewed clean-reinstall acceptance and reset first-activation transient

Candidate `7c8b5468c0ca2bfb689607dda039b3e19cb14851` passed the full live clean-reinstall path on OpenClaw 2026.9.5. The run completed with `CLEAN REINSTALL: PASS`, rebuilt v0.9.6 from owned fresh state, returned CNX to `active/managed` generation 2, left Gateway/Ollama healthy, restored the hidden supervisor Ready/Enabled with `LastTaskResult=0`, loaded plugin v0.9.6, and retained zero pending outbox. Backup completed at `T:\CogentNexus-OpenClaw-Release-Acceptance-Backups\20260921-202850`.

The subsequent provider-neutral reset acceptance preserved the OpenClaw-owned route `ollama/qwen3.8:27b` but exposed a fourth pre-release lifecycle transient. The first post-reset managed activation failed and the reset correctly ended fail-closed with CNX disabled. OpenClaw logs showed repeated loopback Gateway connectivity timeouts while the Gateway process still owned port 18789, followed by `ETIMEDOUT`. A controlled second enable from the exact same reconstructed state then succeeded fully: MANAGED generation 2, Gateway 2026.9.5 healthy, Ollama healthy, and supervisor Ready.

The repair is intentionally bounded rather than a general retry loop. Reset may perform exactly one additional transactional `enable` only when the first enable fails and a fresh `gateway_health()` proves the native Gateway has recovered. If Gateway health is absent, or if the second enable fails, reset still terminates fail-closed. Provider/model/auth routing remains OpenClaw-owned and unchanged.

A RED-first reset contract reproduced the missing bounded retry. Focused post-repair tests are GREEN (`4 passed`) across provider-neutral reset and the existing pre-plugin activation readiness contract. Full repository requalification after the bounded reset repair is GREEN: Python `711 passed, 5 skipped, 38 subtests passed`; plugin tests `428/428`; evaluation PASS with evidence SHA-256 `55a41c2ff538a07f588c28759bb5e37a20b0bc9756eacddbf95f48adba5191a0`; production audit `0 vulnerabilities`; and `plugin:validate` PASS with 290 packed files.

Candidate `7c8b5468...` is therefore not the final release identity because the reset repair changes production lifecycle source. A new exact candidate is required after full requalification and renewed reset/install-over acceptance.

## Reset enable-timeout acceptance blocker on candidate 5887e29f

Candidate `5887e29f416bc0e410e09b8877ec54a8fe04dd9a` passed v0.9.6 -> v0.9.6 install-over into an active/managed live state on OpenClaw 2026.9.5. Post-install verification showed ownership/plugin version `0.9.6`, Gateway healthy, supervisor Ready/Enabled with `LastTaskResult=0`, pending outbox zero, OpenClaw route still `ollama/qwen3.8:27b`, and exact source/installed SHA-256 parity for `reset_v095.py` and the plugin README.

The subsequent reset acceptance again reproduced the OpenClaw 2026.9.5 first-activation transient. This time the first `enable` did not return a nonzero child result; it exceeded the 300-second Host subprocess budget and raised `subprocess.TimeoutExpired`. The previously added bounded retry handled returned failures but not this exception path, so reset correctly fell through to its outer fail-closed handler instead of performing the allowed retry. Post-failure state was safe: CNX disabled/PASSTHROUGH generation 1, plugin disabled, Gateway healthy, pending outbox zero, and route unchanged at `ollama/qwen3.8:27b`.

A RED-first timeout regression now covers this exact live failure. Minimal repair catches only first-enable `TimeoutExpired`, explicitly re-establishes the disabled/native boundary, requires native Gateway health, and then permits the same single bounded retry. Timeout or failure on the retry remains terminal/fail-closed. Focused coverage is GREEN: `5 passed`.

Candidate `5887e29f...` is rejected for publication because the timeout-aware recovery changes production reset source. A new exact candidate is required after full requalification and renewed live reset acceptance.

## Reset orphaned-quiescence acceptance blocker on candidate 8bd4d6e1

Candidate `8bd4d6e14053752d1ee2a4eaf521a78c9102b7a4` passed v0.9.6 -> v0.9.6 install-over on OpenClaw 2026.9.5 with installer exit code 0. Live verification showed CNX active/managed generation 2, Gateway 2026.9.5 healthy, Ollama healthy, supervisor Ready/Enabled with `LastTaskResult=0`, pending outbox zero, ownership/plugin version `0.9.6`, route unchanged at `ollama/qwen3.8:27b`, and exact source/installed SHA-256 parity for `reset_v095.py`.

The renewed reset acceptance exercised the new timeout-aware path exactly as intended: the first fresh-state enable exceeded the 300-second Host subprocess budget, reset entered the disabled/native safety cleanup instead of escaping directly to the outer failure handler, and then attempted its single bounded retry. That retry was correctly rejected by the quiescence fence with `Supervisor quiescence lease is held by another owner`.

Inspection proved that the active lease owner was `enable:31848:2026-09-21T15:50:32.528397+00:00`, while PID 31848 no longer existed. The timed-out child had therefore been terminated before its `finally` block could release the 900-second supervisor quiescence lease. This was an orphaned dead-owner lease, not an active concurrent owner. The post-failure state remained safe: CNX disabled/PASSTHROUGH generation 1, plugin disabled, Gateway healthy, pending outbox zero, and OpenClaw route unchanged.

A RED-first lease contract now distinguishes three cases: a dead `enable:<pid>` owner may be reclaimed before TTL expiry; a live enable owner may not; and a non-enable owner may not. Reclamation occurs under the existing quiescence operation lock and rechecks the lease before unlinking. The reset timeout path performs this reclamation only after successfully restoring the disabled/native safety boundary and before the single retry. Focused lifecycle/quiescence coverage is GREEN (`17 passed`), and the full Python requalification is GREEN (`715 passed, 5 skipped, 38 subtests passed`).

Candidate `8bd4d6e1...` is rejected for publication because the dead-owner reclaim changes production lifecycle source. A new exact candidate is required for renewed live install/reset acceptance.

## Pre-staging Gateway readiness blocker on candidate 62a970c4

Candidate `62a970c44c91de7eee7d7629f167f76ba397efb0` passed v0.9.6 -> v0.9.6 install-over with installer exit code 0 and exact source/installed parity for both `reset_v095.py` and `supervisor_quiescence.py`. Live state after install-over was active/managed generation 2, Gateway/OpenClaw 2026.9.5 healthy, Ollama healthy, supervisor Ready/Enabled, pending outbox zero, and route unchanged at `ollama/qwen3.8:27b`.

The subsequent reset acceptance proved the dead-owner reclaim repair: after the first fresh-state enable failed and reset entered its bounded retry, the retry no longer hit `Supervisor quiescence lease is held by another owner`. Instead it advanced into transactional staging. The retry then failed before authority commit because `openclaw plugins disable cogentnexus-openclaw` hit Gateway `ETIMEDOUT`. Rollback completed to native passthrough, including a healthy native Gateway restore after six readiness attempts / about 90 seconds.

Code inspection showed the existing OpenClaw 2026.9.x readiness guard was positioned only before `plugin_enabled(True)`. The earlier `plugin_enabled(False)` staging mutation still traverses OpenClaw's Gateway control path and therefore remained exposed to the same cold-start transient. A RED-first activation-ordering contract now requires two distinct readiness fences: one before any plugin/config staging mutation and one before inference-capable plugin activation. Focused activation/quiescence/reset coverage is GREEN (`17 passed`).

Candidate `62a970c4...` is rejected for publication because the pre-staging readiness repair changes production Host activation source. A new exact candidate is required after full requalification and renewed live reset acceptance.

## Reset Host enable-budget blocker on candidate e41f4ddc

Candidate `e41f4ddc31ee9ea53eb46f7c40ec5a5c7ffbc57a` passed exact install-over and exact clean-reinstall acceptance on OpenClaw 2026.9.5. The clean reinstall completed with exit code 0 and `CLEAN REINSTALL: PASS`, with backup preserved at `T:\CogentNexus-OpenClaw-Release-Acceptance-Backups\20260922-000700`. Fresh installation returned to active/MANAGED generation 2 with Gateway healthy, supervisor Ready/Enabled, plugin v0.9.6 enabled, Ollama healthy, and pending outbox zero.

The subsequent exact-candidate reset acceptance exercised the full timeout-recovery path. The first fresh-state enable reached the fixed 300-second subprocess budget and was safely rolled back through the disabled/native boundary. Dead-owner lease reclamation succeeded and the one permitted retry began without a quiescence fence. The retry passed pre-staging readiness, plugin-disable staging, managed config staging, second readiness, plugin enable, MANAGED authority commit, and entered post-commit `runtime lifecycle start`. It then reached the same fixed 300-second parent subprocess budget before the post-commit health path returned, despite having already committed MANAGED authority.

Terminal result was therefore FAIL:
`CogentNexus-OpenClaw enable timed out after the one bounded provider-neutral reset retry (300 seconds)`.

Post-failure state remained safe: CNX disabled/PASSTHROUGH generation 3, plugin disabled, Gateway healthy, pending outbox zero, and OpenClaw route unchanged at `ollama/qwen3.8:27b`. The timed-out retry left an orphaned quiescence lease owned by dead PID 15716 until its 900-second TTL, confirming that retry-timeout cleanup also needs explicit dead-owner reclamation.

This evidence shows that 300 seconds is not a valid Host-enable budget on the validated OpenClaw 2026.9.5 runtime: a normal activation can legitimately spend time in two Gateway readiness fences, multiple OpenClaw config mutations, plugin activation, MANAGED reload, and post-commit lifecycle verification. RED-first regressions now require a command-specific Host budget of 600 seconds for `enable` while ordinary Host commands remain at 300 seconds, and require a timed-out bounded retry to reclaim only a provably dead `enable:<pid>` lease before fail-closed cleanup. Focused reset/quiescence/activation coverage is GREEN (`19 passed`).

Candidate `e41f4ddc...` is rejected for publication because the reset Host-budget repair changes production reset source. A new exact candidate is required after full requalification and renewed lifecycle acceptance.

## Local verdict

All currently executable local release gates are GREEN after the live-found lifecycle repairs. The latest requalification completed with focused activation/quiescence/reset coverage `19 passed`, full Python `717 passed, 5 skipped, 38 subtests passed`, plugin tests `428/428`, evaluation passed with evidence SHA-256 `2f674506a55a63c9e8b8c02371a32326b5d77490cce02922ec86917add71c909`, production audit `0 vulnerabilities`, and `plugin:validate` PASS with 290 packed files.

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
