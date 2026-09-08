# CNX-20260831-197 — v0.9.3 Exact-Candidate Credentialed Release Publication

Status: `READY_FOR_HERMES`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Predecessor: `CNX-20260831-196`
Executor: Hermes
Coordinator / final reviewer: ChatGPT

## Purpose

Publish v0.9.3 while preserving the already accepted frozen product target after Task 196 proved that the Actions `GITHUB_TOKEN` cannot create a Release targeting the workflow-divergent frozen candidate.

## Locked identities

Current default branch / repaired workflow execution identity:

`c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

Frozen v0.9.3 release target:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Validated Release workflow run:

`33406148890`

Validated Actions artifact:

- name: `release-assets-0.9.3-26ce64a624255278a3a0266ad38746e0e6ed2e31`
- artifact ID: `9763253683`
- GitHub artifact digest: `sha256:5ca5bf8579754888c355c0976a86fd03c3c79eeed2ecd52293a0d6e5fa24b65d`

## Why the publication path changes

Task 196 reached `POST /repos/funggier/CogentNexus-OpenClaw/releases` and failed with `HTTP 403: Resource not accessible by integration` despite `publish.permissions.contents=write` and explicit `GH_REPO`.

The frozen target predates the Task-195 change to `.github/workflows/release.yml`. GitHub requires workflow-write authorization when creating a release targeting a commit whose workflow files differ from the default branch, and the workflow `GITHUB_TOKEN` cannot provide that authority for this case.

This task therefore authorizes a one-time credential-capable publication using the exact already-validated artifact. It does not authorize a new build or candidate retarget.

## Preconditions — read only

Hermes must fresh-check all of the following before any publication mutation:

1. `main` is still exactly `c70552801ddbb9dc0a49c9cfc64368b9f4820f07` unless a newer coordination-approved release-workflow-only state explicitly supersedes it.
2. tag `v0.9.3` is absent.
3. GitHub Release `v0.9.3` is absent.
4. run `33406148890` exists with `package=success` and retained artifact ID `9763253683`.
5. no other v0.9.3 publication has appeared.
6. Hermes has a user or GitHub-App credential capable of creating a Release for this repository and authorized for the workflow-divergent target. Inspect authentication/scopes/permissions without mutating publication state. If sufficient authority cannot be established, stop `BLOCKED_RELEASE_CREDENTIAL`.

## Exact publication procedure

1. Download the exact artifact from run `33406148890`; do not rebuild archives.
2. Record downloaded file names and sizes.
3. Verify `SHA256SUMS.txt` with an independent checksum command before publication.
4. Verify both archives open/list successfully and contain the required release payload files.
5. Record the archive SHA-256 values and the release notes identity.
6. Fresh-check tag/release absence again immediately before mutation.
7. Perform exactly one authenticated Release creation attempt:
   - repository: `funggier/CogentNexus-OpenClaw`
   - tag: `v0.9.3`
   - target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
   - title: `CogentNexus-OpenClaw v0.9.3`
   - notes: exact validated `RELEASE_NOTES.md` from the artifact
   - assets: `cogentnexus-openclaw-v0.9.3.tar.gz`, `cogentnexus-openclaw-v0.9.3.zip`, `SHA256SUMS.txt`
8. Do not retry automatically if release creation fails.
9. If creation succeeds, fresh-read GitHub authority and prove:
   - tag `v0.9.3` exists;
   - tag resolves exactly to `26ce64a624255278a3a0266ad38746e0e6ed2e31` (dereference annotated tag if necessary);
   - GitHub Release is published and not draft/prerelease unless release notes explicitly require otherwise;
   - exactly the three required public assets exist;
   - public assets can be downloaded;
   - downloaded public assets independently match `SHA256SUMS.txt` and the pre-publication validated files;
   - archives open/list successfully after public download.

## Hard fence

Do not:

- retarget v0.9.3 to `c705528...` merely to bypass authorization;
- rebuild or alter the validated archives;
- create a tag separately before the single release-creation attempt;
- retry release creation after a failure without ChatGPT review;
- dispatch the Release workflow again;
- modify product/runtime/plugin/installer/provider/package bytes;
- reset, uninstall, reinstall, or install-over;
- force push.

## Dispositions

- `PASS`
- `BLOCKED_RELEASE_CREDENTIAL`
- `FAIL_RELEASE_PUBLICATION`
- `FAIL_RELEASE_IDENTITY`
- `FAIL_RELEASE_ASSET_VERIFICATION`
- `BLOCKED_AUTHORITY_DRIFT`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260831-197-v093-exact-candidate-credentialed-release-publication.md`

Include authentication capability evidence without exposing tokens/secrets, exact pre-state, artifact provenance, pre-publication checksums, the single mutation command/action shape with secrets redacted, tag/release identity, public-asset checksums, anomalies, and final disposition. Then stop for ChatGPT review.
