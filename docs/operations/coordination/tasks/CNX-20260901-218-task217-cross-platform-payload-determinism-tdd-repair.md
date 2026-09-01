# CNX-20260901-218 — Task-217 Cross-Platform Payload Determinism TDD Repair

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-217`
Repair parent: `CNX-20260831-198`
Executor: Hermes / repository engineer
Coordinator / final reviewer: ChatGPT

## Purpose

Repair the proven cross-platform installable-plugin byte nondeterminism using strict RED → minimal GREEN TDD, establish a new repository-GREEN candidate with a new exact package proof, and prove that the exact new candidate produces the same payload fingerprint on Windows as authoritative CI.

Task 218 is repository/build repair only. It must not install or mutate the live Windows CogentNexus/OpenClaw runtime.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

Task-207 semantic repair base:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-217 accepted root cause:

`ACCEPT_PASS_NEWLINE_VARIANCE_PROVEN__TDD_DETERMINISTIC_PAYLOAD_REPAIR_REQUIRED`

Historical exact identities are diagnostic references only:

```text
Task-207 Ubuntu CI payload: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
Task-216 Windows payload:   3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
payload paths: 192 / 192 equal
byte-different files: 43, all under dist/
normalized Windows payload -> historical CI d0677581... exactly
```

Do not treat either historical fingerprint as the required fingerprint for the repaired candidate. Any change to packaged build metadata may legitimately produce a new exact fingerprint.

## Accepted root cause

Task 217 proved:

- installable payload identity hashes exact package bytes;
- the path sets were identical;
- 43 generated `dist` files differed solely by CRLF/LF byte representation;
- explicit `tsc --newLine lf` did not change the Windows output in the controlled test;
- isolated CRLF→LF normalization of generated payload bytes reproduced the Ubuntu CI identity exactly.

Therefore the repair must canonicalize generated/package bytes, not weaken fingerprint semantics.

## Hard fences

Task 218 authorizes:

- product test/build-script changes required for deterministic generated plugin bytes;
- minimal production/build tooling required by the failing test;
- package metadata changes only when required to invoke the canonical build step;
- CI/workflow changes only if required to make the regression an authoritative gate;
- normal repository commits/pushes to `agent/v0.9.3-full-stabilization`;
- isolated Windows builds for post-CI cross-platform proof;
- report publication.

Task 218 does **not** authorize:

- CogentNexus installer/install-over;
- `cnxclaw` lifecycle actions;
- OpenClaw plugin install/enable/disable/config mutation;
- Gateway restart;
- live ownership/staging/transaction/SQLite mutation;
- provider/model substitution;
- Release/tag/asset mutation;
- force push;
- Discord Send/API/bot/injected traffic.

## Phase A — fresh authority and baseline

Fresh-fetch branch HEAD, ACTIVE.md, STATUS.md, Task-217 report/review, and this Task 218.

Confirm there is no existing Task-218 report and no unexplained product source/test/workflow change after Task-207 except the intended Task-218 work.

Use the current branch ancestry based on Task-207 candidate `27fe0181...`; do not rewrite history.

Capture exact pre-change bytes/hashes for at least:

- `plugins/cogentnexus-openclaw/package.json`;
- `plugins/cogentnexus-openclaw/tsconfig.json`;
- existing build/verification scripts used by `plugin:build` / `plugin:validate`;
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` and `plugin_payload_identity.py` as invariant fingerprint authority.

Do not modify the fingerprint algorithm in this task.

## Phase B — RED test first

Create a **test-only** regression that deterministically simulates the proven cross-platform condition on any host OS.

The regression must use real build/package behavior rather than asserting a mock.

Required conceptual fixture:

1. create two isolated temporary plugin fixture roots from the same plugin source/config/package boundary;
2. exclude `node_modules` and prior `dist` from copied fixture state;
3. canonicalize `src/**/*.ts` to LF in fixture A;
4. canonicalize the logically identical `src/**/*.ts` to CRLF in fixture B;
5. execute the plugin's **real normal build path** for each fixture using the same installed TypeScript/toolchain;
6. compute the actual installable payload-v2 identity for each fixture using repository-supported identity logic;
7. assert equal payload path sets, equal file count, equal byte identity/fingerprint, and no CRLF remaining in generated text artifacts after the normal build path.

The test must be platform-independent: it must reproduce the pre-fix failure even when executed on Linux/macOS by constructing CRLF input explicitly.

### Mandatory RED proof

Before any production/build-path repair:

- run the focused new regression;
- observe a genuine assertion failure due to differing generated bytes/fingerprint, not a syntax/import/test-harness error;
- record the two fingerprints and differing generated paths;
- verify the failure is consistent with Task-217 newline variance;
- commit **only the test/test-harness change** as a RED commit.

No production/build script, package build command, fingerprint logic, or canonicalizer may be changed in the RED commit.

If the proposed test passes before the fix, it is not a valid regression; redesign the test until it fails for the proven defect.

## Phase C — minimal GREEN repair

After RED is proven, implement the smallest build-boundary repair that makes generated installable bytes deterministic.

Preferred design:

```text
TypeScript emit
  -> explicit post-emit dist newline canonicalization
  -> schema/package validation
  -> payload fingerprint / npm pack
```

A small dedicated Node build utility is preferred over embedding mutation into the fingerprint algorithm.

Required behavior:

- canonicalize generated `dist` text bytes to LF (`\n`) after emit;
- operate only inside the plugin's generated `dist` root;
- use deterministic sorted traversal;
- do not follow symlinks/junctions/reparse-point indirection;
- fail closed on unexpected filesystem indirection or unsupported generated artifact type rather than escaping the generated boundary;
- preserve all non-newline bytes exactly;
- be idempotent: a second canonicalization run must produce zero further byte changes;
- run automatically in the normal build path used by `plugin:validate`, installer preflight, CI package proof, tests/evaluation as appropriate;
- do not normalize repository source files in place;
- do not normalize during fingerprint calculation;
- do not allow multiple accepted fingerprints for equivalent payloads.

A `.gitattributes`-only repair is insufficient because deterministic package bytes must not depend on checkout policy. It may be added as defense-in-depth only if justified by tests, not as the sole fix.

If changing `package.json` is necessary to invoke the canonicalizer, update `package-lock.json` coherently if npm requires it. Do not add the build-only canonicalizer to the published plugin `files` payload unless there is a concrete runtime requirement.

## Phase D — GREEN and local regression matrix

Run the focused regression and require GREEN.

Then prove:

1. LF-source fixture and CRLF-source fixture have identical generated path sets;
2. generated `dist` bytes are byte-identical;
3. payload-v2 fingerprints are identical;
4. generated regular text artifacts contain no CRLF;
5. canonicalizer second pass is idempotent;
6. `npm run build` passes;
7. `npm test` passes;
8. `npm run evaluation` passes;
9. `npm run plugin:validate` passes;
10. package dry-run retains the required package contents and coherent file count.

Run the repository validations affected by build/package changes. Preserve exact command outputs and exit codes.

## Phase E — candidate commit and authoritative CI

Commit the minimal GREEN repair separately from the RED commit.

Push normally; no force push.

The resulting exact product candidate SHA is a **new candidate** and supersedes `27fe0181...` for future installer requalification only after this Task-218 evidence is complete.

Require the normal authoritative CI gates for the exact GREEN candidate:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

All required jobs must complete successfully on the exact candidate SHA.

The Validate package-dry-run must retain a new package-proof artifact containing at minimum:

```text
sourceCommit = exact GREEN candidate SHA
packageVersion = 0.9.3
payloadV2Fingerprint = <new exact 64-hex fingerprint>
payloadFileCount = coherent positive count
archive SHA-256 values = exact
```

Record artifact ID/digest and archive hashes.

Do not assume the repaired fingerprint equals historical `d067...`; use the exact value proven for the repaired candidate.

## Phase F — independent Windows reproduction of the new CI authority

After CI package proof exists, create a **fresh clean isolated Windows checkout** at the exact GREEN candidate SHA.

Run the same normal preparation used before installer fingerprinting:

```text
npm ci
npm run plugin:validate
repository-supported plugin-fingerprint / payload identity
```

Require:

- fresh Windows HEAD equals exact GREEN candidate SHA;
- worktree was clean before build;
- Windows payload file count equals the new CI package proof;
- Windows payload fingerprint equals the new CI package-proof fingerprint **exactly**;
- no CRLF is present in the generated installable `dist` text artifacts;
- file-by-file payload comparison against extracted CI proof has zero byte differences, where practical; if archive extraction is used, record exact path-set equality and differing-file count `0`.

This is the critical acceptance gate. CI GREEN alone is insufficient if fresh Windows identity still differs.

## Phase G — live preservation

Repeat read-only live checks only; require no semantic/product mutation from Task 218:

```text
controller remains passthrough
startup adapter remains absent/disabled
live old plugin generation remains unchanged
Gateway healthy
selected provider ollama
Delivery READY
Recovery READY
Task-205 historical recovery cancelled/inert
SQLite integrity ok
Discord traffic 0
```

Do not attempt installer requalification in Task 218 even if all repository/build gates pass.

## Allowed dispositions

- `PASS_REPOSITORY__CROSS_PLATFORM_PAYLOAD_DETERMINISM_PROVEN`
- `FAIL_RED_NOT_REPRODUCED`
- `FAIL_GREEN_FOCUSED`
- `FAIL_FULL_VALIDATION`
- `FAIL_CI`
- `FAIL_WINDOWS_CI_FINGERPRINT_MATCH`
- `FAIL_LIVE_PRESERVATION`
- `BLOCKED_EVIDENCE`

## Successor rule

Only after independent review of Task-218 PASS may a successor Task 219 authorize installer requalification using:

- the exact new GREEN candidate SHA;
- its new exact package-proof fingerprint;
- the direct Scheduled Task execution topology already qualified by Task 215;
- one installer invocation maximum;
- zero Discord Sends until installer/provenance/managed health passes.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-218-task217-cross-platform-payload-determinism-tdd-repair.md`

Include:

- RED test path/commit/command/failure;
- minimal GREEN files/commit and rationale;
- canonicalizer boundary/idempotency proof;
- focused/full local validation results;
- exact GREEN candidate SHA;
- CI run IDs/results;
- new package-proof artifact ID/digest/fingerprint/file count/archive hashes;
- fresh Windows reproduction fingerprint and file-by-file/path-set comparison;
- live preservation proof;
- mutation ledger;
- final disposition.

Stop after publishing the report for ChatGPT review.
