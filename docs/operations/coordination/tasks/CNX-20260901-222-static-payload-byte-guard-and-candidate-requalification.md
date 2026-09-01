# CNX-20260901-222 — Static Payload Byte Guard and Candidate Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-221`
Repair parent: `CNX-20260831-198`
Executor: Hermes / repository engineer + authenticated Windows verifier
Coordinator / final reviewer: ChatGPT

## Purpose

Close the remaining package-identity boundary after Task 221 proved that the historical static CRLF mismatch was caused by two-stage Git attribute/worktree carry-over rather than direct `core.autocrlf=true` behavior.

Task 222 must establish a fail-closed static package-byte contract, remove the unaccepted `-text` experiment, and produce one exact repository/CI/Windows-equal candidate suitable for later installer requalification.

Task 222 is repository/build/package verification only. It must not touch the live CogentNexus/OpenClaw runtime.

## Immutable authority

Published public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

Task-207 semantic repair base remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Accepted generated-output repair lineage:

`9af329b4de7c02fda35b467d84e76bb0f0bb0944`

Unaccepted static checkout experiment still present in branch history/current tree:

`b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5`

That commit changes only `.gitattributes` from `text eol=lf` to `-text` for four static package paths. It is not an accepted repair.

## Accepted Task-221 result

Report:

`docs/operations/coordination/reports/CNX-20260901-221-task220-exact-first-checkout-control-adjudication.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260901-221-task220-exact-first-checkout-control-adjudication-review.md`

Accepted disposition:

`ACCEPT_PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`

Accepted facts:

- exact `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0` repository objects are LF-only;
- exact-first materialization produces LF-only package static files under inherited/default `core.autocrlf=true`, explicit `true`, and explicit `false`;
- two-stage clone/materialize-newer-then-detach-to-older reproduces CRLF in exactly the historical three static files;
- direct `core.autocrlf=true` alone is not the root cause;
- the defect is two-stage attribute/worktree carry-over;
- npm/build/plugin validation are not the first mutation boundary;
- current package validation does not explicitly reject static CRLF contamination;
- `-text` is not an accepted byte-identity repair.

## Static package identity set

At minimum, Task 222 must guard the static files that participate in plugin payload/package identity:

```text
package.json
README.md
openclaw.plugin.json
scripts/bootstrap-ticket-db.mjs
```

The generated `dist` tree remains governed by the bounded post-emit canonicalizer from Task 219 and must not be broadened to rewrite static tracked files.

## Hard fences

Authorized:

- repository tests and bounded package-validation/build-policy source changes;
- forward-revert/restoration of the four `.gitattributes` entries to `text eol=lf`;
- isolated LF/CRLF test fixtures;
- isolated exact-first Windows checkout/build/package verification;
- authoritative GitHub Actions CI/package-proof retrieval;
- normal commits/pushes to `agent/v0.9.3-full-stabilization`.

Not authorized:

- installer/install-over;
- reset/uninstall/reinstall;
- `cnxclaw enable/disable/start/stop/restart`;
- live OpenClaw plugin/config/Gateway mutation;
- live SQLite/ownership/staging/transaction writes;
- provider/model substitution;
- Discord Send/API semantic traffic;
- Release/tag/asset publication;
- force push/history rewrite.

Discord budget: `0 Sends`.

# Required execution flow

## Phase A — Fresh authority and clean product diff

Before editing:

1. fetch fresh branch HEAD;
2. verify Task 222 is active/READY;
3. compare current product state against `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5` and identify any product/source/test/workflow drift newer than that commit;
4. if unexpected product drift exists, stop `BLOCKED_PRODUCT_DRIFT` rather than stacking changes blindly;
5. confirm live runtime remains preserved read-only: PASSTHROUGH baseline, no installer/lifecycle operation, Discord budget zero.

## Phase B — Genuine RED first

Create a test-only regression that proves the current package-validation path fails open on static newline contamination.

The test must use the real package validation boundary, not a fake helper assertion.

Acceptable pattern:

1. create an isolated copy/fixture of the plugin package sufficient for `verify-package-contents.mjs` / package-content validation;
2. ensure the canonical static fixture is LF;
3. convert at least one identity-bearing static file to CRLF without changing semantic text;
4. invoke the current validation path;
5. assert that validation must reject noncanonical static payload bytes.

Pre-fix expected result:

- current validation exits success / fails to reject the contaminated static file;
- the regression assertion fails for the intended reason: **noncanonical static bytes were accepted**;
- failure must not be dependency/path/module/syntax/harness failure.

Commit the corrected RED test alone before production/build-policy changes.

Required evidence:

- RED commit SHA;
- exact command;
- exit/assertion excerpt proving the intended failure;
- fixture path(s) and newline metrics.

If a genuine RED cannot be established, stop `FAIL_RED_NOT_REPRODUCED`.

## Phase C — Minimal GREEN

Implement the minimum repair satisfying all of the following.

### C1. Restore repository newline declaration

Forward-revert the unaccepted `-text` experiment by restoring:

```gitattributes
plugins/cogentnexus-openclaw/package.json text eol=lf
plugins/cogentnexus-openclaw/README.md text eol=lf
plugins/cogentnexus-openclaw/openclaw.plugin.json text eol=lf
plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs text eol=lf
```

Do not rewrite history. Do not reset/rebase away Task 219/220/221 evidence.

### C2. Fail-closed static package-byte validation

Extend package validation minimally so it rejects CRLF/noncanonical newline bytes in the four static package identity files before package identity/packing is accepted.

Requirements:

- validation only; do **not** silently normalize or rewrite tracked static files;
- error must identify the offending relative path without dumping semantic file contents;
- LF-only canonical files pass;
- CRLF-contaminated files fail;
- binary/unsupported indirection must not be followed as a side effect of this check;
- generated `dist` canonicalization remains separate and generated-only;
- payload fingerprint algorithm remains byte-exact and unchanged;
- no multiple-fingerprint acceptance.

Prefer a small reusable validation function or bounded script rather than broad refactoring.

### C3. RED → GREEN proof

Run the exact RED regression after implementation and require GREEN.

Also prove a two-stage contaminated fixture/worktree is rejected by package validation before fingerprint/package acceptance.

## Phase D — Repository validation

On the final candidate:

1. focused static-byte regression: PASS;
2. Task-219 real-boundary LF/CRLF generated-output regression: PASS;
3. `npm run build`: PASS;
4. `npm test`: PASS;
5. `npm run evaluation`: PASS;
6. `npm run plugin:validate`: PASS;
7. packed file count remains expected (`192` unless an independently justified package-surface change is made; Task 222 should not change package surface);
8. second generated-dist canonicalization pass reports zero changes;
9. fresh exact-first checkout/build leaves tracked worktree clean.

No unrelated product refactor is authorized.

## Phase E — Establish exact final candidate

After all repository GREEN checks, push the exact final candidate SHA.

Record:

- exact 40-hex candidate SHA;
- changed production/build-policy/test files;
- relation to `9af329b4...`, `4e31dbd...`, `b081d55...`, and Task-207 base `27fe0181...`;
- explicit statement that public `v0.9.3` tag remains unchanged.

## Phase F — Authoritative CI and package proof

Require authoritative GitHub Actions on the **exact final candidate SHA**:

- Validate: success;
- Windows Installer Pack Smoke: success;
- PS5.1 Acceptance Smoke: success.

Retrieve the Validate package-proof artifact and record:

- artifact ID/name;
- artifact digest;
- exact head SHA/sourceCommit;
- package version;
- payload file count;
- payload-v2 fingerprint;
- tar.gz SHA-256;
- zip SHA-256.

Do not reuse package proof from `e2dede9...`, `4e31dbd...`, `9af329b4...`, or any other prior candidate as final authority.

## Phase G — Fresh Windows exact-first candidate reproduction

This gate must avoid the proven two-stage carry-over topology.

Use an independent disposable Windows repository where **the final candidate SHA is selected before any working-tree materialization**, for example:

```text
git clone --no-tags --no-checkout <repo> <dir>
git checkout --detach <FINAL_CANDIDATE_SHA>
```

Do not first materialize branch HEAD and then detach to the candidate.

Under the inherited Windows Git configuration (including the system `core.autocrlf=true` if still present), record immediately after first checkout:

- exact HEAD;
- `git config --show-origin --get-all core.autocrlf`;
- `git check-attr -a` for all four static paths;
- `git ls-files --eol` for all four static paths;
- SHA-256/size/CRLF/LF counts for all four static paths;
- `git status --porcelain=v2`.

Required immediate result:

- all four static paths LF-only;
- `i/lf w/lf attr/text eol=lf` or equivalent exact evidence;
- clean tracked status.

Then run:

- `npm ci`;
- `npm run build` / `npm run plugin:validate` as required by the normal candidate path;
- repository-supported `plugin_payload_identity.py` on the exact candidate.

Compare the resulting Windows plugin payload against the exact CI package-proof payload file-by-file.

Required PASS:

- path sets equal;
- payload file count `192`;
- `dist` differences `0`;
- static differences `0`;
- total byte differences `0`;
- Windows fingerprint exactly equals CI fingerprint;
- tracked worktree remains clean after validation.

If any mismatch remains, stop `FAIL_CROSS_PLATFORM_DETERMINISM` and do not authorize installer.

## Phase H — Report and stop

Publish:

`docs/operations/coordination/reports/CNX-20260901-222-static-payload-byte-guard-and-candidate-requalification.md`

Allowed PASS disposition:

`PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL`

Possible non-PASS dispositions include:

- `FAIL_RED_NOT_REPRODUCED`
- `FAIL_STATIC_BYTE_GUARD`
- `FAIL_REPOSITORY_VALIDATION`
- `FAIL_CI`
- `FAIL_CROSS_PLATFORM_DETERMINISM`
- `BLOCKED_PRODUCT_DRIFT`
- `BLOCKED_EVIDENCE`

A Task-222 PASS is **repository/package provenance closure only**. It does not itself install the candidate.

After report publication, stop for ChatGPT independent review.

## Successor boundary

Only after Task 222 receives an independent PASS review may the next task resume **one exact Windows install-over** using:

- the exact Task-222 candidate and fingerprint;
- exact-first candidate materialization/provenance;
- the direct Windows Scheduled Task terminal execution topology qualified in Task 215;
- zero Discord Sends until installer/provenance/managed-health PASS.
