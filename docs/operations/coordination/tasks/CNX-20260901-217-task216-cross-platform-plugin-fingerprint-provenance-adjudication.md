# CNX-20260901-217 — Task-216 Cross-Platform Plugin Fingerprint Provenance Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-216`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Determine exactly why the fresh Windows build of Task-207 commit `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` produces payload-v2 fingerprint `3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed` while the accepted Ubuntu CI package proof for the same source commit records `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`.

This task is diagnostic/build-only. It must preserve the live CogentNexus/OpenClaw state and must not install anything.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 source commit under adjudication:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Accepted CI package proof:

```text
Validate run: 33483589170
artifact ID: 9790881384
artifact name: cogentnexus-openclaw-v0.9.3-package-proof-27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
artifact head SHA: 27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
artifact expires: 2026-09-15T07:44:58Z
payload-v2 fingerprint: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload file count: 192
```

Task-216 Windows build result:

`3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed`

## Accepted parent result

Task-216 report:

`docs/operations/coordination/reports/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification-review.md`

Accepted disposition:

`ACCEPT_BLOCKED_AUTHORITY__CROSS_PLATFORM_PAYLOAD_FINGERPRINT_ADJUDICATION_REQUIRED`

## Source facts already proven

- `package.json.files` includes `dist`, `scripts/bootstrap-ticket-db.mjs`, `openclaw.plugin.json`, and `README.md`; `package.json` itself is also included by the ownership fingerprint algorithm.
- `_plugin_payload()` hashes the exact relative path and exact file bytes for the complete installable payload.
- package-dry-run computes `d067...` on `ubuntu-latest` only after `npm ci` and `npm run plugin:validate`.
- Task 216 performed `npm ci` and `npm run plugin:validate` on Windows and produced `3b86...`.
- `tsconfig.json` does not specify `compilerOptions.newLine`.

These facts make generated-byte cross-platform variance a concrete hypothesis, but Task 217 must prove or reject it from exact bytes.

## Hard fence

Task 217 authorizes only:

- read-only live-state preservation checks;
- fresh isolated exact-commit checkouts/copies under `%LOCALAPPDATA%\Temp`;
- download/extraction of the retained package-proof artifact/archive;
- `npm ci`, TypeScript/plugin validation and build experiments inside isolated Task-217 evidence trees only;
- file hashing, byte comparison, newline analysis and payload identity computation inside those evidence trees;
- report publication.

Task 217 does **not** authorize:

- CogentNexus installer/install-over;
- `cnxclaw` lifecycle actions;
- OpenClaw plugin/config mutation;
- Gateway restart;
- ownership/staging/transaction/backup mutation;
- raw SQLite writes;
- provider/model substitution;
- product source/test/workflow commits or edits on the working branch;
- Release/tag/asset mutation;
- force push;
- Discord traffic;
- process termination outside Task-217 isolated build children.

Discord budget: `0`.

## Phase A — fresh authority and live preservation

Fresh-fetch branch HEAD, ACTIVE.md, STATUS.md, Task-216 report/review, and this Task 217.

Capture read-only live state sufficient to prove no product mutation:

- controller mode/generation;
- live plugin fingerprint;
- Gateway health;
- selected provider;
- delivery/recovery state;
- Task-205 cancelled recovery state;
- SQLite integrity;
- relevant installer/lifecycle residue.

Expected preserved live state remains PASSTHROUGH on old fingerprint `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1` unless independently explained drift is observed.

## Phase B — obtain exact CI payload authority

Use artifact `9790881384` while it remains unexpired.

Prove before use:

- artifact ID/name/digest;
- workflow run `33483589170`;
- head SHA exact `27fe0181...`;
- `PACKAGE_IDENTITY.json` sourceCommit/version/fingerprint/fileCount;
- archive SHA-256 values match the accepted Task-207 report.

Extract one retained release archive into the Task-217 evidence root.

Locate the archived plugin root:

`plugins/cogentnexus-openclaw`

Run the repository-supported payload identity/fingerprint algorithm against the extracted CI plugin payload and require it reproduces `d0677581...` and file count `192`.

If the artifact cannot be retrieved or does not reproduce the accepted identity, stop `BLOCKED_CI_ARTIFACT_AUTHORITY`.

## Phase C — reproduce Windows default build

Create a new clean isolated checkout at exact `27fe0181...`.

Require:

```text
HEAD exact
worktree clean before build
npm ci = pass
npm run plugin:validate = pass
```

Compute payload identity and require the observed Windows-default fingerprint. If it no longer reproduces `3b86b13f...`, record the actual value and stop `BLOCKED_NONREPRODUCIBLE_WINDOWS_FINGERPRINT` unless the reason is proven.

## Phase D — exact file-by-file payload diff

Using the same payload enumeration rules as `_package_payload_files()`:

1. produce sorted relative-path manifests for CI payload and Windows-default payload;
2. require the path sets and file counts to be compared exactly;
3. record for each file:
   - relative path;
   - byte length;
   - SHA-256 CI;
   - SHA-256 Windows;
   - equal/different;
4. summarize differences by payload area (`dist/`, package.json, manifest, README, bootstrap script, other).

Do not infer from whole-tree fingerprints alone.

If path sets differ, identify every missing/extra path and classify separately.

## Phase E — newline/platform-byte adjudication

For every differing regular text file, perform byte-level newline analysis:

- count CRLF (`\r\n`), lone LF, lone CR on both sides;
- compare `WindowsBytes.replace(b"\r\n", b"\n")` against CI bytes;
- compare CI normalized LF against Windows normalized LF;
- retain any residual byte differences after newline normalization.

Required classifications:

- `LINE_ENDING_ONLY` — byte equality is achieved solely by CRLF/LF normalization;
- `OTHER_GENERATED_BYTE_DIFFERENCE` — bytes still differ after newline normalization;
- `NON_GENERATED_PAYLOAD_DIFFERENCE` — a differing file outside generated `dist/`;
- `PATH_SET_DIFFERENCE`.

## Phase F — controlled canonical-LF build experiment

In a **separate isolated copy** of the exact source commit, do not edit the repository branch.

After `npm ci`, build the plugin with an explicit LF compiler override using the installed TypeScript compiler, for example:

```text
npx tsc -p tsconfig.json --newLine lf
```

Then run the non-rebuilding verification steps needed to validate the generated payload (schema verification/package-content checks) without invoking `npm run plugin:validate` afterward if that command would rebuild with the default newline setting.

Compute payload identity again.

Strong root-cause proof requires all of:

```text
Windows default build fingerprint = 3b86b13f...
CI extracted payload fingerprint = d0677581...
Windows explicit-LF build fingerprint = d0677581...
CI payload file set = explicit-LF payload file set
all payload file bytes CI vs explicit-LF = identical
```

If explicit LF does not reproduce `d067...`, identify residual file differences exactly; do not force the newline conclusion.

Optional corroboration: in another isolated copy, `--newLine crlf` may be used to determine whether it reproduces `3b86...`. This is diagnostic only.

## Phase G — root-cause classification

Allowed dispositions:

1. `PASS_CROSS_PLATFORM_NEWLINE_NONDETERMINISM_PROVEN`
   - CI `d067...` and Windows default `3b86...` are reproduced;
   - differences are generated payload bytes explained by newline policy;
   - explicit LF on Windows reproduces byte-identical `d067...`.

2. `PASS_CROSS_PLATFORM_BUILD_NONDETERMINISM_PROVEN_OTHER`
   - cross-platform generated-byte variance is proven but not solely newline-related; exact residual cause/evidence must be reported.

3. `BLOCKED_CI_ARTIFACT_AUTHORITY`
4. `BLOCKED_NONREPRODUCIBLE_WINDOWS_FINGERPRINT`
5. `BLOCKED_INDETERMINATE_PAYLOAD_DIFFERENCE`
6. `FAIL_PRODUCT_PRESERVATION`
7. `BLOCKED_EVIDENCE`

## Successor rule

If disposition is `PASS_CROSS_PLATFORM_NEWLINE_NONDETERMINISM_PROVEN`, stop after report publication. Do **not** edit source in Task 217.

A separate Task 218 should then perform bounded TDD to canonicalize generated plugin line endings (preferred minimal repair: explicit LF in TypeScript build configuration), add regression protection that fails on platform-dependent generated newlines, run full repository/Windows CI/package proof, and establish a **new** repaired candidate SHA/package fingerprint before installer requalification resumes.

Do not merely relabel Windows fingerprint `3b86...` as equivalent to `d067...`; the payload-v2 invariant is byte-exact by design.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-217-task216-cross-platform-plugin-fingerprint-provenance-adjudication.md`

Report must include:

- fresh authority/live-preservation evidence;
- CI artifact metadata and extracted payload identity;
- Windows default build identity;
- exact file-set comparison;
- per-file diff summary/hashes;
- newline counts/normalization results;
- explicit-LF build identity and byte comparison;
- root-cause classification;
- mutation ledger;
- final disposition.

Stop for ChatGPT review after publishing.
