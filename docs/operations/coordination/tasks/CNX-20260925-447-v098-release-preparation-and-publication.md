# CNX-20260925-447 — v0.9.8 Release Preparation and Publication

Status: `IN_PROGRESS`
Owner: ChatGPT
Executor: ChatGPT
Parent: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Target release: `v0.9.8`
Working branch: `cnx-447-v098-release-preparation`
Production-code authority: `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`

## Objective

Prepare, qualify, publish, and independently verify CogentNexus-OpenClaw v0.9.8 from the production behavior accepted by Task 446, without weakening the terminal-final boundary, Ticket-first semantics, native Ollama behavior, OpenClaw-owned routing, installer recovery, or the immutable v0.9.7 release.

## Why this task exists

Task 446 repaired the Dashboard Direct terminal-final defect and exposed two OpenClaw 2026.9.5 installer compatibility hazards that were also repaired:

1. plugin enable/disable may persist the requested mutation and then fail to exit before the CLI timeout;
2. candidate dependency preparation must not execute unrelated peer/dev lifecycle scripts.

The final production-code candidate `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec` passed exact-SHA CI, real install-over, independent installed/source parity, runtime attestation, supervisor checks, native Ollama acceptance, and fresh installed-candidate Codex progress -> tool -> terminal acceptance.

Release work must now convert that accepted production behavior into a coherent v0.9.8 release candidate, requalify the exact release SHA, publish through the repository release workflow, and independently verify the public artifacts.

## Release invariants

1. v0.9.7 tag/release/history are immutable.
2. Production behavior accepted at `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec` must not change silently.
3. Any production-code change after that SHA requires renewed focused/full qualification and live acceptance.
4. Version/docs/package metadata changes must be internally consistent at v0.9.8.
5. OpenClaw 2026.9.5 remains the validated runtime baseline.
6. Provider/model/auth authority remains OpenClaw-owned.
7. Native Ollama fallback must remain valid; `runTerminal` must not become a global requirement.
8. Release publication must use an exact candidate SHA; no force-push or tag rewrite.
9. Public tag, GitHub release, archives, and checksums must be independently verified after publication.
10. `main` may advance only by proven ancestry/fast-forward after the release candidate is accepted.

## Stage 1 — release baseline and scope audit

Before version mutation:

- verify Task 446 is COMPLETE/PASS;
- verify branch base ancestry includes exact production-code authority `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`;
- verify repository clean except intentional Task 446 closure / Task 447 coordination docs;
- verify v0.9.7 public tag and release remain unchanged;
- inventory every current-facing version reference and OpenClaw baseline reference;
- inspect release workflow inputs and artifact/checksum contract;
- identify any stale documentation that must move from v0.9.7 to v0.9.8.

## Stage 2 — version and release-documentation preparation

Update only the metadata/documentation required for v0.9.8 unless a new defect is proven.

At minimum verify/update as applicable:

- root `VERSION`;
- plugin `package.json` / lockfile metadata;
- plugin manifest/current-version documentation;
- README/install/clean-reinstall/current release references;
- release notes/changelog/history;
- coordination status and report references.

Describe the v0.9.8 changes factually:

- Dashboard Direct terminal-final boundary repair;
- exact mirrored run correlation;
- native/Ollama fallback preservation;
- OpenClaw 2026.9.5 plugin-mutation timeout reconciliation;
- installer dependency lifecycle suppression with `npm ci --ignore-scripts`.

## Stage 3 — local exact-candidate validation

Require at least:

- focused terminal-boundary tests;
- focused plugin-mutation-timeout tests;
- focused installer lifecycle tests;
- full plugin Vitest;
- TypeScript/plugin validation;
- production dependency audit;
- full Python suite;
- repository validation/self-tests used by the current release process;
- PowerShell parser / PS5.1 relevant tests;
- `git diff --check`.

If any production source changes beyond version metadata are introduced, repeat the full Task 446 semantic/live qualification before continuing.

## Stage 4 — exact release-candidate live lifecycle qualification

From the exact release SHA:

- install-over on OpenClaw 2026.9.5;
- prove installed/source production-file SHA-256 parity;
- prove Host active/MANAGED and plugin loaded;
- prove Gateway native health;
- prove v092 supervisor Ready/Enabled and `LastTaskResult=0`;
- prove no non-terminal Tickets/pending outbox residue;
- perform clean reinstall and reset/re-enable acceptance if required by the current release workflow/baseline;
- verify OpenClaw-owned route remains coherent.

At minimum rerun a fresh Codex Dashboard progress -> tool -> terminal acceptance if any runtime/package contents differ from the already accepted installed candidate.

## Stage 5 — no-force push and exact-SHA GitHub gates

- commit the exact release candidate;
- push without force;
- prove local/remote SHA equality;
- require Validate GREEN;
- require PS5.1 Acceptance Smoke GREEN;
- require Windows Installer Pack Smoke GREEN;
- require any additional release-required workflow gates GREEN.

## Stage 6 — publish v0.9.8

Only after all prior stages are GREEN:

- dispatch the repository release workflow with `version=0.9.8` and the exact candidate SHA;
- require candidate identity verification and publish jobs GREEN;
- do not manually move an existing tag.

## Stage 7 — independent public verification

After publication:

- verify tag `v0.9.8` points exactly to the accepted release SHA;
- verify GitHub release is public, non-draft, non-prerelease unless the workflow intentionally specifies otherwise;
- enumerate all assets;
- verify archive digests against `SHA256SUMS.txt`;
- independently download/hash release archives when practical;
- verify current-facing public documentation reflects v0.9.8 and OpenClaw 2026.9.5.

## Stage 8 — main convergence and final runtime check

- prove accepted release SHA is a descendant of current `main`;
- fast-forward `main` without force only after public release verification;
- verify remote/local `main` equality;
- re-read public documentation from `main`;
- confirm installed runtime remains healthy and no coordination residue is left.

## PASS criteria

Task 447 is PASS only when:

- exact v0.9.8 candidate is locally and live qualified;
- exact-SHA GitHub gates are GREEN;
- release workflow succeeds;
- public tag/release/assets/checksums independently match the accepted SHA;
- `main` converges by safe fast-forward;
- final runtime remains healthy;
- v0.9.7 remains unchanged.

## FAIL / BLOCKED criteria

Stop and record evidence if:

- candidate identity becomes ambiguous;
- production code changes without renewed qualification;
- install-over/clean lifecycle cannot converge;
- terminal-boundary or native Ollama behavior regresses;
- any required exact-SHA CI gate is not GREEN;
- public tag/release does not match the candidate SHA;
- main cannot be advanced by safe ancestry/fast-forward;
- publication would require history rewrite.

## Evidence required

Record:

- starting base SHA and Task 446 authority;
- complete version/reference inventory;
- exact release-candidate SHA;
- local validation counts;
- live lifecycle evidence and installed/source hashes;
- exact-SHA GitHub workflow IDs/status;
- release workflow run ID;
- public tag/release URL/metadata;
- asset names and SHA-256 values;
- main convergence evidence;
- final runtime/controller/plugin/supervisor/Ticket health.

## Report destination

`docs/operations/coordination/reports/CNX-20260925-447-v098-release-preparation-and-publication-report.md`

## Local candidate qualification checkpoint — 2026-09-25

Release/version preparation is locally GREEN.

Key release-preparation changes:

- VERSION/package/manifest/lock/current CLI/ownership authority advanced coherently to `0.9.8`;
- owned v0.9.7 installations are explicitly accepted as the immediate in-place upgrade predecessor;
- current-facing documentation identifies v0.9.8 as a release candidate while v0.9.7 remains the latest published immutable release;
- release notes `docs/releases/v0.9.8.md` describe the terminal-final and installer hardening changes;
- all candidate dependency-preparation surfaces now use `npm ci --ignore-scripts`, while explicit test/build/evaluation/package validation commands remain authoritative.

Local validation:

- focused release/version/docs/lifecycle contracts: `40 passed`;
- namespace isolation: PASS;
- baseline consistency: `v0.9.8 / Bridge v0.9.8` PASS;
- skill/workspace singleton validation: PASS;
- Cogent/runtime/workflow self-tests: PASS;
- benchmark validator self-test: PASS;
- full Python: `745 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `93 files / 436 tests PASS`;
- evaluation: PASS, evidence SHA-256 `ce5b0c4148e76fe9fdf6c3e36d8a7c8af6528a2b9418e6b5fd14572f473f6ca4`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 46 config properties, 5 tools, 9 required Ticket DB tables, 294 packed files;
- exact release metadata: VERSION/package/manifest/lock/root-lock all `0.9.8`;
- payload identity: SHA-256 `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`, 294 files;
- PowerShell parser: PASS;
- PS5.1 serializer and root-process self-tests: PASS;
- POSIX `sh -n scripts/install.sh`: PASS;
- `git diff --check`: PASS.

One local release-preparation defect was found and repaired before candidate freeze: Windows version editing had converted static package identity files to CRLF, and `plugin:validate` correctly rejected `package.json`. The static package identity files were normalized back to canonical LF and `plugin:validate` then passed.

## Current classification

`CNX447_V098_LOCAL_GREEN_CANDIDATE_COMMIT_PENDING`

## Exact candidate / CI / live checkpoint — 2026-09-25

Exact release candidate:

`4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`

The branch was pushed without force and local/remote SHA equality was proven.

Exact-SHA GitHub gates:

- Validate `36144053827`: SUCCESS;
- PS5.1 Acceptance Smoke `36144053553`: SUCCESS;
- Windows Installer Pack Smoke `36144053896`: SUCCESS.

Real v0.9.7 -> v0.9.8 install-over on OpenClaw 2026.9.5 completed once with exit code 0. Independent post-install evidence proves:

- ownership/plugin version: `0.9.8`;
- controller: active/MANAGED, generation `32`, provider ownership `openclaw`;
- Gateway: OpenClaw 2026.9.5, running and connectivity healthy;
- plugin: enabled / loaded / diagnostics empty;
- runtime attestation: `runnerReady=true`, `globalHookCount=7`;
- supervisor: Ready / Enabled / Hidden / `LastTaskResult=0`;
- SQLite integrity: `ok`;
- non-terminal Tickets: `0`;
- pending outbox: `0`;
- source/installed payload identity: exact match, `294` files, SHA-256 `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`.

Fresh installed-candidate Codex/App-Server acceptance:

- session: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`;
- run: `cnx447-v098-codex-terminal-acceptance-v1`;
- Ticket: `CNXT-d029a929-d280-4b43-af52-bfb31ce062eb`;
- commentary seq 49: no `runTerminal`;
- tool call seq 50: no `runTerminal`;
- tool result seq 51;
- true final seq 52: `runTerminal=true`, exact durable text `CNX447_V098_TERMINAL_FINAL`;
- Ticket terminal events began only after the true final;
- one delivered direct-result row, attempt count 0;
- no outbox row.

Clean reinstall/reset were reviewed against the actual release baseline. They are not required by `.github/workflows/release.yml` and were not universal v0.9.7 release gates. The four-stage physical lifecycle used for v0.9.6 was task-specific because that release repaired clean-reinstall/reset behavior. No destructive clean/reset cycle is repeated for v0.9.8 without a defect or release requirement.

Current pre-publication classification:

`CNX447_V098_PREPUBLICATION_GREEN`

## Publication checkpoint — 2026-09-25

A first Release dispatch (`36159246629`) was cancelled before publication because it used the older workflow definition from default `main`; it produced no tag/release side effect.

The accepted dispatch explicitly used workflow ref `cnx-447-v098-release-preparation`:

- Release run `36159455993`: SUCCESS;
- package: SUCCESS;
- publish: SUCCESS;
- public tag `v0.9.8` -> `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- public/non-draft/non-prerelease: PASS;
- independently downloaded TAR/ZIP hashes match `SHA256SUMS.txt` and GitHub asset digests;
- v0.9.7 tag/assets remain unchanged.

Current classification:

`CNX447_V098_PUBLISHED_MAIN_CONVERGENCE_PENDING`

## Post-release main CI contract repair — 2026-09-25

Post-release docs commit:

`8d2204a6f1f0978873ef6c00bc3035cf3e664dc6`

was pushed and `main` fast-forwarded without force. Public current-facing docs were reread from GitHub `main` and matched the published v0.9.8 authority.

Final live verification after main convergence remained GREEN:

- installed ownership/plugin version `0.9.8`;
- controller active/MANAGED generation 32;
- Gateway OpenClaw 2026.9.5 running / connectivity OK;
- plugin enabled/loaded with empty diagnostics;
- runtime `runnerReady=true`, global hook count 7;
- supervisor Ready/Enabled/Hidden / `LastTaskResult=0`;
- SQLite integrity `ok`;
- non-terminal Tickets 0;
- pending outbox 0.

Main Validate run `36160610790` failed only because `tests/test_install_docs_authority.py` still expected the pre-publication heading `Development-candidate source install` / Thai equivalent. The published docs correctly renamed that section to `Exact release/source-tree install`.

The test contract was updated to the published heading with no production/runtime/workflow change.

Post-repair local validation:

- focused docs/release contracts: `15 passed`;
- full Python: `745 passed, 5 skipped, 38 subtests passed`.

Current classification:

`CNX447_V098_POST_RELEASE_CI_REPAIR_PENDING`
