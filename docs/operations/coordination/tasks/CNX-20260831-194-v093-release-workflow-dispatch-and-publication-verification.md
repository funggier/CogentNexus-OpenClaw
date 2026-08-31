# CNX-20260831-194 — v0.9.3 Release Workflow Dispatch and Publication Verification

Status: `READY_FOR_HERMES`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Executor: Hermes / authenticated GitHub operator
Coordinator / reviewer: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Coordination branch: `agent/v0.9.3-full-stabilization`
Release branch: `main`

## Purpose

Complete the final publication boundary for CogentNexus-OpenClaw v0.9.3 after PR #26 was successfully merged and all exact-head release gates passed.

This task is publication-only. It does not authorize product/runtime/plugin/test/installer/provider changes.

## Frozen publication identity

Authoritative merged `main` SHA:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

PR #26:

- state: merged;
- head before merge: `66fdba1c6dc2ee0997c5764bc56a52f543741bdc`;
- merge commit / current `main`: `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Accepted repaired product candidate used for real-Windows qualification:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Accepted installable plugin payload:

`b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files.

Current v0.9.3 provider responsibility boundary remains:

- managed runtime/operator provider: Ollama only;
- installer: provider-neutral.

## Preconditions — fresh-check before dispatch

Hermes must read GitHub authority fresh and prove all of the following immediately before dispatch:

1. `main` is exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
2. PR #26 is merged and its merge SHA is exactly that same SHA;
3. tag `v0.9.3` does not already exist;
4. GitHub Release `v0.9.3` does not already exist;
5. no existing/in-progress Release workflow run is already publishing v0.9.3.

If any precondition differs, **STOP** and report `BLOCKED_PUBLICATION_AUTHORITY_DRIFT`. Do not guess, retarget, or dispatch against a different SHA.

## Exact dispatch

Dispatch `.github/workflows/release.yml` exactly once from the repository with:

- ref: `main`
- `version=0.9.3`
- `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`

Preferred authenticated CLI shape when available:

```powershell
gh workflow run release.yml --repo funggier/CogentNexus-OpenClaw --ref main -f version=0.9.3 -f candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31
```

Equivalent authenticated GitHub Actions UI dispatch is allowed only with the exact same ref and inputs.

Do not dispatch twice if the first request is slow or its run is not immediately visible. Locate the first run before considering any further action. A second dispatch is not authorized by this task.

## Workflow contract to verify

The merged `release.yml` is expected to:

1. validate exact input shape;
2. checkout exact `candidate_sha`;
3. prove checked-out SHA equality;
4. run namespace/baseline/runtime/workflow/Python/pytest/npm/evaluation/audit/plugin validation;
5. verify exact v0.9.3 metadata;
6. build tar/zip archives and `SHA256SUMS.txt`;
7. retain validated release assets;
8. refuse duplicate release publication;
9. create GitHub Release/tag `v0.9.3` targeting the exact candidate SHA;
10. publish exactly these public assets:
   - `cogentnexus-openclaw-v0.9.3.tar.gz`
   - `cogentnexus-openclaw-v0.9.3.zip`
   - `SHA256SUMS.txt`.

## Required post-publication proof

After the Release workflow reaches terminal state, record:

### Workflow

- run ID and URL;
- event must be `workflow_dispatch`;
- requested version;
- requested candidate SHA;
- package job conclusion;
- publish job conclusion;
- overall conclusion.

### Tag/release identity

- tag `v0.9.3` exists;
- resolve tag target fully if annotated;
- final target commit must be exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- GitHub Release title/tag/draft/prerelease state;
- release target must not differ from frozen main SHA.

### Release assets

Public release must contain exactly the required publication assets:

1. `cogentnexus-openclaw-v0.9.3.tar.gz`
2. `cogentnexus-openclaw-v0.9.3.zip`
3. `SHA256SUMS.txt`

Download all three release assets independently after publication.

Run SHA-256 verification using the downloaded `SHA256SUMS.txt`. Record actual SHA-256 values and prove both archives match the release checksum file.

Also inspect archive integrity/listing sufficiently to prove the archives are readable and include required plugin payload files, including:

- `plugins/cogentnexus-openclaw/dist/v091-release-entry.js`
- `plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs`
- `plugins/cogentnexus-openclaw/openclaw.plugin.json`
- `plugins/cogentnexus-openclaw/README.md`
- `plugins/cogentnexus-openclaw/package.json`

### Repository authority after publication

- re-read `main`;
- record exact `main` SHA;
- publication is acceptable only if tag/release target remains the frozen release SHA even if coordination branch later advances.

## Failure dispositions

Use one of these exact dispositions when applicable:

- `BLOCKED_PUBLICATION_AUTHORITY_DRIFT`
- `FAIL_RELEASE_WORKFLOW`
- `FAIL_RELEASE_TARGET_IDENTITY`
- `FAIL_RELEASE_ASSET_SET`
- `FAIL_RELEASE_CHECKSUM_VERIFICATION`
- `PASS`

Do not repair product/source/workflow behavior under this task if publication fails. Stop with evidence so a separate repair task can be opened.

## Hard fences

Forbidden:

- any force push;
- any source/runtime/plugin/test/installer/provider change;
- any commit to `main` before publication;
- changing the frozen `candidate_sha`;
- creating the release manually outside the approved Release workflow;
- creating a second v0.9.3 release/tag;
- dispatching the Release workflow more than once;
- deleting/recreating a failed release/tag to hide evidence.

## Report

Publish the final Hermes report to:

`docs/operations/coordination/reports/CNX-20260831-194-v093-release-workflow-dispatch-and-publication-verification.md`

The report must include exact commands/actions, timestamps, workflow run ID, exact SHA identities, tag/release evidence, asset names/sizes, checksum values, checksum verification result, final disposition, and any anomaly.

Commit/push the report only to `agent/v0.9.3-full-stabilization` (or another coordination-only branch explicitly derived from it), not to `main`.

After publishing the report, stop for ChatGPT review. Do not make any further release/product changes.
