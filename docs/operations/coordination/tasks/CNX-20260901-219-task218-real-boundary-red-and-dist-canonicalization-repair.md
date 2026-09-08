# CNX-20260901-219 — Task-218 Real-Boundary RED and Dist Canonicalization Repair

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-218`
Repair parent: `CNX-20260831-198`
Executor: Hermes / repository engineer
Coordinator / final reviewer: ChatGPT

## Purpose

Redo the deterministic-payload repair at the actual proven boundary: first establish a genuine platform-independent RED that reproduces the historical CRLF/LF installable-byte divergence through the real plugin build path, then apply the minimum fail-closed generated-`dist` canonicalization and establish a new repository/CI/Windows-equal candidate.

Task 219 is repository/build only. It must not touch the live CogentNexus/OpenClaw runtime.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 semantic repair base:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-217 proven root cause:

- installable path sets equal at 192 files;
- 43 byte-different files, all under `dist/`;
- every difference CRLF/LF-normalizable;
- Windows LF normalization reproduced historical CI fingerprint `d0677581...` exactly;
- `tsc --newLine lf` alone did not alter the problematic Windows output.

Task-218 experimental candidate:

`e2dede9a0cb16b8b9536a350e018bfbd7c95c39b`

Experimental candidate evidence:

```text
Validate run: 33521283353 success
PS5.1 Acceptance Smoke: 33521283398 success
Windows Installer Pack Smoke: 33521283517 success
artifact: 9805795685
digest: sha256:241846ea60531ebd45f008cf52ff3ebf4689c6887076b5b9bd1f92863c43a5d5
payload files: 192
CI payload fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
fresh Windows fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
```

This candidate is evidence only and is **not installer-authorized**.

## Accepted Task-218 review

Review:

`docs/operations/coordination/reviews/CNX-20260901-218-task217-cross-platform-payload-determinism-tdd-repair-review.md`

Accepted disposition:

`ACCEPT_FAIL_RED_NOT_REPRODUCED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`

Independent findings that Task 219 must correct:

1. the genuine RED was not reproduced;
2. final canonicalization was broadened from generated `dist` to tracked/static package files;
3. committed traversal uses following `statSync`/read operations and does not prove fail-closed symlink/junction rejection;
4. simple LF/CRLF TypeScript fixtures were not representative of the real 43-file historical mechanism.

## Hard fences

Authorized:

- repository/source/test/build-script changes needed for this bounded repair;
- normal commits/pushes to `agent/v0.9.3-full-stabilization`;
- isolated exact-source builds/evidence trees;
- authoritative CI and package-proof retrieval;
- read-only live-state preservation checks.

Not authorized:

- installer/install-over;
- `cnxclaw` lifecycle commands;
- live OpenClaw plugin/config mutation;
- Gateway restart;
- live ownership/staging/transaction/SQLite write;
- provider/model substitution;
- Release/tag/asset mutation;
- force push/history rewrite;
- Discord Send/API/bot/injected traffic.

## Phase A — fresh authority and preserve evidence

Fresh-fetch branch HEAD, ACTIVE.md, STATUS.md, Task-218 report/review, and this task.

Require:

- no Task-219 report exists;
- no unrelated product drift after Task-218 report;
- Task-218 experimental commits remain in history; do not rewrite or erase them;
- live Windows product remains preserved/read-only if checked.

## Phase B — restore an effective pre-fix production boundary without rewriting history

Create one normal commit that reverts only the **unaccepted Task-218 production/build-path effects** needed to restore the effective plugin build behavior before canonicalization.

The target effective pre-fix behavior is:

```text
package build = tsc -p tsconfig.json
no canonicalize-dist production utility invoked
fingerprint algorithm unchanged
```

Do not revert Task-207 Discord semantic repair, coordination docs, Task-217 evidence, or unrelated source.

The prior experimental commits remain in history; this is a forward revert, not reset/rebase/force-push.

Test files may remain until replaced by the corrected RED, provided they are not treated as proof.

Record the exact revert commit SHA and diff.

## Phase C — trace the real historical newline mechanism before writing the RED

Do not guess from a trivial TypeScript fixture.

Use the retained Task-217 evidence if available. If necessary, reproduce an isolated exact `27fe0181...` Windows build and compare it with the retained historical CI payload.

Required evidence:

1. identify at least one of the historical 43 byte-different `dist` paths;
2. show exact CI LF bytes vs Windows CRLF bytes for that file;
3. map that output to the corresponding `src/**/*.ts` input or other exact generation source;
4. identify the construct/output mechanism that preserves or introduces the CRLF bytes despite `tsc --newLine lf` being ineffective in Task 217.

Candidate mechanisms may include preserved source trivia/comments/template content or another real emitter path, but the task must prove the mechanism from exact bytes/source rather than assume it.

Also run a whole-real-source probe:

- create two isolated copies of the same plugin source tree;
- canonicalize all `src/**/*.ts` to LF in copy A;
- canonicalize all `src/**/*.ts` to CRLF in copy B;
- keep static package payload bytes otherwise identical;
- run the **effective pre-fix normal build** in both;
- compare generated `dist` bytes and payload identity.

If A/B remain byte-identical, do not fabricate a RED. Continue tracing the actual Task-217 differing file until a real platform-independent reproduction is found, or stop:

`BLOCKED_RED_MECHANISM_UNPROVEN`.

No production fix is allowed after that disposition.

## Phase D — corrected genuine RED

Only after Phase C proves a reproducible mechanism, replace/refine the payload determinism regression.

The test must:

- run on any OS;
- use the real plugin build boundary, not invoke a not-yet-existing helper directly as the reason for failure;
- create logically equivalent LF and CRLF inputs using the real construct proven in Phase C, preferably the real plugin source tree or a faithful distilled fixture;
- execute the effective pre-fix normal build for both;
- compute/compare generated installable bytes or repository-supported payload identity;
- assert equality.

### Mandatory RED evidence

On the effective pre-fix state the test must **fail an assertion because the two generated payloads differ in CRLF/LF bytes**.

Not acceptable as RED:

- missing module/helper;
- syntax error;
- dependency resolution failure;
- wrong fixture path;
- missing symbol;
- command-not-found;
- test harness crash.

Capture at least one differing path and SHA/byte/newline evidence in the failure.

Commit the corrected RED test separately from GREEN production changes.

## Phase E — minimal GREEN

Implement only what the proven RED requires.

Preferred boundary:

```text
tsc emit
  -> bounded generated-dist canonicalizer
  -> downstream validation / payload fingerprint / npm pack
```

Requirements for the canonicalizer:

- scope only to generated `plugins/cogentnexus-openclaw/dist` (or an equivalent exact generated-output root proven by the test);
- deterministic sorted traversal;
- regular text artifacts only, e.g. `.js`, `.d.ts`, `.js.map` as actually present;
- use `lstat`/Dirent no-follow checks before descend/read/write;
- reject symlink/junction/reparse-style indirection rather than following it;
- no writes outside the exact generated root;
- CRLF -> LF canonicalization is idempotent;
- do not normalize inside `_plugin_payload()`;
- do not accept multiple fingerprints;
- do not rewrite tracked static package/source files during normal build;
- no unrelated cleanup/refactor.

If static package payload files independently require checkout normalization, prove that need separately from exact bytes. A broad post-build mutation of `package.json`, README, manifest, or bootstrap source is not the default repair.

### Fresh-worktree cleanliness

After `npm run build` in a fresh checkout, require:

`git diff --exit-code`

for tracked files. Generated ignored artifacts may exist, but normal build must not dirty tracked source/package files.

## Phase F — GREEN verification

Required fresh evidence:

- corrected focused regression GREEN;
- canonicalizer idempotency GREEN;
- indirection rejection test GREEN where platform support permits creating the fixture;
- `npm run build` GREEN;
- `npm test` GREEN;
- `npm run evaluation` GREEN;
- `npm run plugin:validate` GREEN;
- package content count coherent;
- repository-supported payload identity valid;
- tracked-worktree cleanliness after build.

Run the corrected regression against the recorded RED/pre-fix state as a control if needed to prove the failure is specifically removed by GREEN.

## Phase G — establish new exact candidate and authoritative CI

Push the exact GREEN candidate normally.

Record exact candidate SHA.

Require authoritative CI on that exact SHA:

- Validate success;
- Windows Installer Pack Smoke success;
- PS5.1 Acceptance Smoke success.

Retain new Validate package proof and record:

- artifact ID/name/digest;
- sourceCommit;
- packageVersion;
- payload file count;
- exact payload fingerprint;
- tar.gz SHA-256;
- zip SHA-256.

Do not reuse `18a900...` as authority unless it naturally remains the exact fingerprint of the new candidate.

## Phase H — exact Windows reproduction of the new candidate

Fresh clean Windows checkout at the exact new candidate SHA.

Run the normal supported build/validation sequence and compute repository-supported payload identity.

Require:

```text
Windows fingerprint == new CI package-proof fingerprint
Windows path set == CI path set
byte differences == 0
CRLF in generated installable dist == 0
tracked worktree clean after build
```

If not exact, stop `FAIL_CROSS_PLATFORM_DETERMINISM` and do not install.

## Phase I — live preservation

Read-only verify live runtime remains preserved from the previous boundary:

- PASSTHROUGH expected unless independently changed outside this task;
- old live generation remains installed;
- Gateway healthy;
- Delivery/Recovery healthy;
- Task-205 stale recovery cancelled/inert;
- no Task-219 live mutation;
- Discord sends `0`.

## Allowed dispositions

- `PASS`
- `BLOCKED_AUTHORITY`
- `BLOCKED_RED_MECHANISM_UNPROVEN`
- `FAIL_RED_NOT_REPRODUCED`
- `FAIL_GREEN`
- `FAIL_INDIRECTION_BOUNDARY`
- `FAIL_TRACKED_WORKTREE_CLEANLINESS`
- `FAIL_CI`
- `FAIL_CROSS_PLATFORM_DETERMINISM`
- `FAIL_PRODUCT_PRESERVATION`
- `BLOCKED_EVIDENCE`

## Successor rule

Only after independent review of Task-219 PASS may a later task resume Windows installer requalification using:

- the new exact repaired candidate/fingerprint/package proof;
- the direct Scheduled Task-owned PowerShell execution model qualified by Task 215;
- `0 Discord Sends` during installer/provenance/managed-health qualification.

Discord semantic acceptance remains later still.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-219-task218-real-boundary-red-and-dist-canonicalization-repair.md`

Include:

- exact forward-revert commit;
- real Task-217 differing file/source-mechanism trace;
- whole-source LF/CRLF probe;
- corrected RED commit/output;
- minimal GREEN commit/diff;
- no-follow/indirection proof;
- focused/full validation;
- new candidate SHA;
- CI runs and package proof;
- exact Windows reproduction;
- tracked-worktree cleanliness;
- live preservation/mutation ledger;
- final disposition.

Stop after publishing the report for ChatGPT review.
