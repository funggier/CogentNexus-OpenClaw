# CNX-20260831-196 — v0.9.3 Second Release Dispatch and Publication Verification

Status: `READY_FOR_HERMES`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Executor: Hermes
Coordinator / final reviewer: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`

## Purpose

Publish v0.9.3 after Task 195 repaired the checkout-free GitHub Release publish job.

This task authorizes exactly one **second** Release workflow dispatch. The first dispatch was Task 194 run `33399493141` and failed before tag/release creation because the publish job lacked explicit repository context.

## Frozen identities

### Workflow execution ref

Authoritative repaired `main` SHA after PR #27 merge:

`c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

This SHA contains the Task 195 workflow repair and is the ref from which `.github/workflows/release.yml` must be dispatched.

### Release target / accepted candidate

The v0.9.3 release target remains exactly:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

**Do not substitute `c705528...` for `candidate_sha`.** The repaired main SHA is workflow-execution identity only. The release tag must target the already accepted candidate `26ce64a...`.

## Pre-dispatch authority gate

Before dispatch, fresh-check GitHub and require all of the following:

1. `main == c70552801ddbb9dc0a49c9cfc64368b9f4820f07`;
2. PR #27 is merged;
3. tag `v0.9.3` is absent;
4. GitHub Release `v0.9.3` is absent;
5. no successful second Release publication run already exists;
6. `.github/workflows/release.yml` on `main` contains repository-explicit publish context (`GH_REPO: ${{ github.repository }}` or equivalent).

If any identity differs, STOP and report `BLOCKED_AUTHORITY_DRIFT` without dispatching.

## Authorized action — exactly one dispatch

Dispatch `.github/workflows/release.yml` from `main` with:

- `version = 0.9.3`
- `candidate_sha = 26ce64a624255278a3a0266ad38746e0e6ed2e31`

Dispatch count authorized in this task: **1**.

Do not create tag/release manually. Do not rerun/retry automatically if the workflow fails. A failed second dispatch must be reported and stopped for review.

## Required workflow verification

Monitor the exact dispatched Release run to terminal state.

Require:

- `package` job PASS;
- `publish` job PASS;
- overall workflow `completed/success`.

The package job must still checkout and verify the exact candidate SHA `26ce64a...`, not repaired workflow SHA `c705528...`.

## Required publication verification

After workflow success, verify from GitHub authority:

1. tag `v0.9.3` exists;
2. tag/release target resolves exactly to `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
3. GitHub Release `v0.9.3` exists and is published, not draft/prerelease unless release notes explicitly require otherwise;
4. release includes exactly the required public assets:
   - `cogentnexus-openclaw-v0.9.3.tar.gz`
   - `cogentnexus-openclaw-v0.9.3.zip`
   - `SHA256SUMS.txt`
5. download all three assets from the published Release;
6. independently compute SHA-256 of both archives;
7. parse `SHA256SUMS.txt` and prove both computed hashes match the published checksum file;
8. archive files are non-empty and open/list successfully;
9. no duplicate or unexpected second `v0.9.3` release/tag exists.

## Scope fence

Do not:

- run `cnxclaw.cmd reset`;
- uninstall or reinstall CogentNexus-OpenClaw;
- install-over;
- modify product/runtime/plugin/installer/provider/package bytes;
- change `main`;
- create or edit release metadata manually outside the workflow;
- retarget candidate SHA;
- retry a failed Release dispatch;
- force push.

The user explicitly chose to publish first; lifecycle clean uninstall/fresh reinstall/reset testing is deferred until after release publication.

## Report

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260831-196-v093-second-release-dispatch-and-publication-verification.md`

The report must include:

- pre-dispatch main/tag/release authority;
- exact workflow execution ref;
- exact candidate SHA input;
- dispatch count;
- Release run ID/URL/status/conclusion;
- package and publish job conclusions;
- tag target proof;
- release metadata;
- asset names/sizes;
- published SHA256SUMS contents;
- independently computed archive SHA-256 values;
- checksum equality result;
- final disposition `PASS`, `FAIL_RELEASE_WORKFLOW`, `FAIL_PUBLICATION_IDENTITY`, or `BLOCKED_AUTHORITY_DRIFT`.

After publishing the report, STOP for ChatGPT review.
