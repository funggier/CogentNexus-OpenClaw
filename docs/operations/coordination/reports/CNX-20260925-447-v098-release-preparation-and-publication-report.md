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

## Exact candidate and exact-SHA CI

Exact release candidate:

`4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`

Commit subject:

`release: prepare CogentNexus-OpenClaw v0.9.8`

The branch was pushed without force and local/remote SHA equality was proven.

Exact-SHA GitHub gates:

- Validate `36144053827`: SUCCESS;
- PS5.1 Acceptance Smoke `36144053553`: SUCCESS;
- Windows Installer Pack Smoke `36144053896`: SUCCESS.

## Real v0.9.7 -> v0.9.8 install-over

A single supported install-over from the published v0.9.7 installation to exact candidate `4f9b07d6...` completed with exit code 0 on OpenClaw 2026.9.5.

The transaction:

- quiesced the supervisor before handoff;
- entered transactional PASSTHROUGH/native authority;
- restarted and re-proved the native Gateway;
- advanced controller generation 30 -> 31 during handoff;
- backed up the installed skill;
- bootstrapped the Ticket DB with zero pending outbox;
- packed and installed exact `openclaw-plugin-cogentnexus-openclaw-0.9.8.tgz`;
- finalized plugin rollover;
- restored the owned runtime/launcher;
- re-enabled the plugin and returned to MANAGED authority;
- completed with controller generation 32.

Independent post-install verification:

- ownership installedVersion: `0.9.8`;
- plugin package version: `0.9.8`;
- controller: active / desired Gateway running / generation 32 / provider ownership OpenClaw;
- Gateway: OpenClaw 2026.9.5, runtime running, connectivity probe OK;
- plugin: enabled / loaded / diagnostics `[]`;
- runtime attestation: `runnerReady=true`, `globalHookCount=7`;
- `classification=AMBIGUOUS` remains the known public-SDK limitation because OpenClaw 2026.9.5 does not expose the per-plugin hook count;
- v092 supervisor: Ready / Enabled / Hidden / `LastTaskResult=0`;
- SQLite integrity: `ok`;
- non-terminal Tickets: zero;
- pending outbox: zero.

Full source/installed payload identity is byte-contract equal:

- source: 294 files / `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`;
- installed: 294 files / same fingerprint.

## Fresh installed-candidate Codex terminal-final acceptance

One controlled Dashboard `chat.send` was executed on the existing authenticated owner session:

- session: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`;
- run: `cnx447-v098-codex-terminal-acceptance-v1`;
- Ticket: `CNXT-d029a929-d280-4b43-af52-bfb31ce062eb`;
- provider/model: `openai/gpt-5.6-luna`;
- runtime: `codex`;
- route: Direct.

Transcript order:

- seq 49: assistant commentary/progress, exact run id, Codex/App-Server mirror, no `runTerminal`;
- seq 50: tool call reading `AGENTS.md`, exact run id, no `runTerminal`;
- seq 51: successful tool result;
- seq 52: exact final `CNX447_V098_TERMINAL_FINAL`, same run id, `runTerminal=true`.

The final transcript row was recorded at approximately `2026-09-25T16:07:52.523Z`. Ticket terminal authority followed:

- `response_ready`: `2026-09-25T16:07:52.516Z` from the terminal-final staging boundary;
- `direct_response_durable`: same timestamp;
- `delivery_confirmed`: `2026-09-25T16:07:52.526Z`;
- `completed`: `2026-09-25T16:07:52.526Z`.

The stored direct-result text is exactly `CNX447_V098_TERMINAL_FINAL`; delivery status is `delivered`, attempt count is 0, and there is no outbox row. No commentary/tool row became the durable result.

## Clean-reinstall/reset disposition

No additional destructive clean-reinstall/reset cycle is required for this release candidate.

Reason:

- the current Release workflow does not require either operation;
- v0.9.7's accepted release contract required exact install-over/source parity plus its task-specific live interruption acceptance, not universal clean/reset acceptance;
- the v0.9.6 four-stage lifecycle was explicitly task-specific because CNX-443 was repairing clean-reinstall/reset lifecycle behavior;
- v0.9.8 introduces no clean-reinstall/reset production repair requiring renewed destructive qualification.

Therefore Stage 4's conditional clean/reset clause is satisfied by baseline review rather than an unnecessary destructive mutation.

## Current classification

`CNX447_V098_PREPUBLICATION_GREEN`

## Release workflow provenance correction

The first workflow dispatch, run `36159246629`, was intentionally rejected and force-cancelled before archive staging or publication. It was dispatched without an explicit workflow ref, so GitHub executed the older `release.yml` definition from default branch `main`. That definition still labeled/executed plain `npm ci`, while the exact candidate workflow had already been hardened to `npm ci --ignore-scripts`.

Evidence:

- run `36159246629`: conclusion `cancelled`;
- package stopped during `npm test`;
- evaluation/audit/plugin validation/release metadata/archive staging were skipped;
- publish job never ran;
- remote `refs/tags/v0.9.8` remained absent.

The accepted release dispatch explicitly bound the workflow definition to branch `cnx-447-v098-release-preparation`, whose remote HEAD was the exact release candidate `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`.

## Publication and independent public verification

Accepted Release workflow:

- run: `36159455993`;
- event: `workflow_dispatch`;
- workflow ref: `cnx-447-v098-release-preparation`;
- run head SHA: `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- package job: SUCCESS;
- publish job: SUCCESS;
- overall conclusion: SUCCESS.

Published release:

- tag: `v0.9.8`;
- exact target: `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- draft: false;
- prerelease: false;
- published: `2026-09-25T16:16:45Z`.

Independent verification downloaded all public assets to:

`T:\CNX-release-verify\v0.9.8-36159455993`

Recomputed SHA-256:

- `cogentnexus-openclaw-v0.9.8.tar.gz`: `de2b4dcee696ca48cf9521e6844a350cd79f4f2336499bd5fc64c6fc0a551143`;
- `cogentnexus-openclaw-v0.9.8.zip`: `2c9f9214feb7d90b9a1b3d89c71a4dcd4ecacfa425618baaeb8e8d97a2a1e4f3`;
- `SHA256SUMS.txt`: `8693865c7d0feb91628e71c9e808392cb84dc65f662b6340f37a70ef7bcc0c61`.

The TAR/ZIP hashes exactly match the downloaded `SHA256SUMS.txt` and GitHub asset digests. Both archives contain the required plugin release identity files and each contains 2,171 entries.

v0.9.7 immutability was re-proven after v0.9.8 publication:

- tag still targets `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- prior TAR/ZIP/checksum asset digests are unchanged.

## Current classification

`CNX447_V098_PUBLISHED_MAIN_CONVERGENCE_PENDING`

The immutable v0.9.8 tag is complete. Current-facing docs have been converged locally to the published state; safe ancestry proof and no-force `main` fast-forward remain.
