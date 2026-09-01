# Independent Review — CNX-20260901-218 Cross-Platform Payload Determinism TDD Repair

## Verdict

`ACCEPT_FAIL_RED_NOT_REPRODUCED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`

Task 218 is not accepted as PASS. The candidate produced a real positive result — authoritative CI and a fresh Windows build agreed on the exact payload fingerprint — but the required genuine pre-fix RED regression was not established, and independent source review found that the final canonicalization boundary is broader and less fail-closed than Task 218 authorized.

## Accepted positive evidence

Candidate:

`e2dede9a0cb16b8b9536a350e018bfbd7c95c39b`

Authoritative CI on that exact SHA:

- Validate `33521283353`: success;
- PS5.1 Acceptance Smoke `33521283398`: success;
- Windows Installer Pack Smoke `33521283517`: success.

Validate retained artifact:

```text
artifact id: 9805795685
artifact digest: sha256:241846ea60531ebd45f008cf52ff3ebf4689c6887076b5b9bd1f92863c43a5d5
head SHA: e2dede9a0cb16b8b9536a350e018bfbd7c95c39b
payload files: 192
payload fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
```

The Task-218 Windows re-build of the same exact SHA reproduced `18a9003b...` and reported no CRLF in the generated installable payload. This is strong evidence that the candidate can produce cross-platform-equal package bytes.

No installer, lifecycle, live plugin/config, Gateway, SQLite, provider/model, Discord, Release/tag/asset mutation occurred.

## Why Task 218 is not accepted

### 1. Genuine RED was not reproduced

The initial test-only commit `96a8a1b59a434c0ed87fd74b32471db26ff2bb31` exercised a helper that did not yet exist. Earlier failures were harness/module/path/dependency failures rather than the required newline-variance assertion failure.

The later real-TypeScript LF/CRLF probe returned `redEqual=true`, with and without source maps. Therefore the synthetic fixture did not model the mechanism that Task 217 had actually observed.

This is a process/evidence failure, not proof that the resulting candidate is wrong.

### 2. The final canonicalizer exceeds the proven mutation boundary

Task 217 proved the historical mismatch was confined to 43 files under generated `dist/`.

The final candidate changed the helper from a `--dist-root` canonicalizer to `--package-root` and enumerates declared package text including `package.json`, `README.md`, `openclaw.plugin.json`, and `scripts/bootstrap-ticket-db.mjs`. That means normal `npm run build` may rewrite tracked static package files, which is broader than the generated-output boundary Task 218 intended.

A deterministic build should not need to normalize unrelated tracked package/source files after checkout when the proven defect is generated payload bytes.

### 3. Filesystem-indirection rejection is not proven by the implementation

The final helper uses `statSync()` and ordinary `readFileSync()` traversal. Those operations follow symlinks/junctions. The implementation does not explicitly `lstat` and reject indirection before traversal/read/write.

Therefore the report statement that the utility provides symlink rejection is not independently supported by the committed source.

### 4. The failed synthetic RED likely targeted the wrong mechanism

Task 217 showed two facts that must be reconciled:

- the Windows exact-source build contained CRLF differences in 43 `dist` files;
- explicit `tsc --newLine lf` did not change those Windows output bytes.

Task 218 then showed that a simple LF-vs-CRLF TypeScript fixture emitted equal bytes. This suggests the fixture omitted a real source construct/trivia/output path responsible for the historical preservation of CRLF. A successor should trace at least one actual Task-217 differing file to its source mechanism before defining the corrected RED.

## Required successor

Open Task 219 as a bounded TDD redo, keeping branch history intact and treating `e2dede9...` as an experimental, unaccepted candidate.

Required flow:

1. revert only the unaccepted Task-218 production/build-path changes so the effective branch returns to the pre-fix build behavior; do not rewrite history or force-push;
2. retain the Task-218 report and experimental commits as evidence;
3. identify at least one real Task-217 differing `dist` file and determine the source/output construct that causes CRLF preservation on the uncanonicalized build;
4. build a corrected platform-independent regression using the real plugin build boundary (prefer the real plugin source tree or a distilled fixture proven from the real differing construct);
5. require the corrected test to fail on the effective pre-fix build because LF/CRLF builds produce different installable bytes/fingerprints — not because a helper/module/path/dependency is missing;
6. commit the corrected RED test separately;
7. implement minimal GREEN limited to generated `dist` text artifacts, using deterministic sorted traversal and no-follow `lstat`/indirection rejection;
8. do not normalize inside the fingerprint algorithm and do not accept multiple fingerprints;
9. do not normalize tracked static package/source files during normal build unless a separate exact-byte proof shows that is required;
10. require `npm run build` not to dirty tracked files in a fresh checkout;
11. run focused/full tests, plugin validation, authoritative CI, retain a new package proof, then fresh-build the exact new candidate on Windows and require exact CI/Windows payload equality.

## Runtime boundary

Task 219 remains repository/build only. No installer, lifecycle command, live plugin/config mutation, Gateway restart, SQLite write, provider/model change, Discord traffic, or Release/tag mutation is authorized.

## Disposition

`ACCEPT_FAIL_RED_NOT_REPRODUCED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`
