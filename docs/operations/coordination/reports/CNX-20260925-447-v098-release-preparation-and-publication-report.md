# CNX-20260925-447 — v0.9.8 Release Preparation and Publication Report

Status: `IN_PROGRESS`
Branch: `cnx-447-v098-release-preparation`
Target release: `v0.9.8`
Task 446 production-code authority: `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`

## Baseline authority

The public v0.9.7 release remains immutable:

- tag: `v0.9.7`;
- tag/release target: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- public, non-draft, non-prerelease;
- TAR.GZ digest: `6af5d0d23606ebd2bfe5f2974d0c237c001fd5e6ec8e0f6867ba24068c65c9bf`;
- ZIP digest: `190b1224fc23f45a662e6e66d15a4e651313e13ee2782ccc2ad8df48674bee12`;
- SHA256SUMS digest: `4e9fdda8c43373366cf3ba18704a8fe0831f77412c1819185407af29771b5485`.

Remote `main` at release-preparation start was `17e60d1f53fce4f37c7bc8cbec6ccb6bca14222e`. That commit is an ancestor of Task 446 production-code authority `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`.

## Release workflow contract

`.github/workflows/release.yml` requires:

- exact X.Y.Z `version`;
- exact lowercase 40-hex `candidate_sha`;
- VERSION/package/manifest/package-lock/root-lock version equality;
- `docs/releases/v<version>.md`;
- candidate identity equality after checkout;
- namespace/baseline/skill/runtime/workflow/Python/plugin gates;
- release archives `.tar.gz` and `.zip`;
- `SHA256SUMS.txt`;
- refusal if the tag or release already exists.

Publication uses `gh release create ... --target <exact candidate SHA>`.

## v0.9.8 preparation

Current release authority was advanced coherently to `0.9.8`:

- root VERSION;
- plugin package metadata;
- OpenClaw plugin manifest;
- package-lock root/package version;
- baseline consistency authority;
- operator CLI banner/current contract;
- ownership manifest version;
- current-facing release/docs/tests/workflow metadata.

Owned v0.9.7 installations are now accepted as an explicit in-place upgrade predecessor.

Current-facing documentation distinguishes:

- current source line: v0.9.8 release candidate;
- latest published release: v0.9.7;
- immutable v0.9.7 public release SHA;
- Task 446 production-code authority for the behavior being released.

Release notes were added at `docs/releases/v0.9.8.md`.

## Candidate dependency lifecycle hardening

A release-preparation RED contract proved that several non-Windows candidate-preparation surfaces still used plain `npm ci`, despite Task 446 proving that the OpenClaw peer/dev dependency lifecycle can hang before classification.

The contract now requires `npm ci --ignore-scripts` on:

- Windows installer candidate preparation;
- POSIX installer candidate preparation;
- local release publication helper;
- Validate workflow dependency preparation;
- Release workflow dependency preparation;
- Windows Installer Pack Smoke dependency preparation.

Explicit `npm test`, `npm run evaluation`, `npm run plugin:validate`, build, and pack steps remain authoritative and unchanged.

Focused lifecycle RED -> GREEN result: `3/3 PASS`.

## Local qualification

Focused release/version/docs/lifecycle contracts:

`40 passed`

Core gates:

- namespace isolation: PASS;
- baseline consistency: `CogentNexus-OpenClaw v0.9.8 baseline consistency: PASS (Bridge v0.9.8)`;
- skill singleton validation: PASS;
- Cogent self-test: PASS;
- runtime self-test: PASS;
- workflow self-test: PASS;
- benchmark validator self-test: PASS.

Full Python:

`745 passed, 5 skipped, 38 subtests passed`

Plugin:

- dependency install: `npm ci --ignore-scripts` PASS;
- Vitest: `93 files / 436 tests PASS`;
- evaluation: PASS;
- evaluation evidence SHA-256: `ce5b0c4148e76fe9fdf6c3e36d8a7c8af6528a2b9418e6b5fd14572f473f6ca4`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS;
- plugin schema: 46 config properties / 5 tools;
- Ticket DB bootstrap: 9 required tables;
- packed file count: 294.

Release metadata/payload:

- VERSION/package/manifest/lock/root-lock: all `0.9.8`;
- payload fingerprint: `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`;
- payload file count: 294.

Platform/static gates:

- PowerShell parser: PASS;
- PS5.1 serializer self-test: PASS;
- exact root-process self-test: PASS;
- POSIX `sh -n scripts/install.sh`: PASS;
- `git diff --check`: PASS.

## Local defect found before freeze

The first v0.9.8 version edit on Windows converted static plugin identity files to CRLF. `plugin:validate` correctly failed with:

`Static package identity contains noncanonical newline bytes: package.json`

The static package identity files were normalized back to canonical LF. The repeated `plugin:validate` then passed with 294 packed files, and the focused release contracts remained 40/40 GREEN.

## Current classification

`CNX447_V098_LOCAL_GREEN_CANDIDATE_COMMIT_PENDING`

No v0.9.8 tag, release, or main mutation has occurred. The next authority boundary is the exact no-force candidate commit/push and exact-SHA GitHub CI.
