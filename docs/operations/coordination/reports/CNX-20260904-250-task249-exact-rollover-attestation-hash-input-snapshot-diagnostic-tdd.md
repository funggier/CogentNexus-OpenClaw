# CNX-20260904-250 — Exact Rollover Attestation Hash-Input Snapshot Diagnostic TDD

## Disposition

`PASS_EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_REPAIRED_GREEN`

Task 250 completed as repository-only TDD. The production repair preserves the existing full-tree digest contract and fail-closed exception while attaching a bounded deterministic per-path delta derived from the exact scans that produced the compared hashes. No live installer, rollover, plugin installation, lifecycle mutation, semantic send, or release operation was performed.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh opening authority: `e052b59dca03a71ff1405993f90168d5327483b7`
- Task: `CNX-20260904-250`
- Parent report HEAD: `85f7afe25c29db59060dafc2d2ce5f3de80942d6`
- Parent review commit: `67f8865b470fbc7e607b9df4509e1d49c3d3d1d0`
- Public tag: `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)

The task report did not exist at the fresh opening authority.

## TDD RED

A test-only RED was added before production changes:

```text
Original RED commit: 423ecfc0c6752523591afb43ab8f63d500f5eec4
Final rebased RED commit: ea5d844 test: reproduce missing rollover hash snapshot diagnostics
```

Test:

```text
tests/test_task250_hash_input_snapshot_diagnostic.py
```

The test uses a deterministic controlled mutation: after `copytree()` creates the backup, the source non-payload `runtime-state.txt` is changed before the source snapshot. It requires the exact changed path and source-vs-backup digest identities from the captured snapshots, while still requiring the existing terminal exception.

RED result before production repair:

```text
1 failed
AssertionError: 'runtime-state.txt' not found in
'pre-install backup project-tree attestation mismatch'
```

This demonstrated the missing behavior rather than merely repeating the generic exception. No production file was changed in the RED commit.

## Minimal production repair

Final implementation commit:

```text
9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96
```

Changed production file:

```text
skills/cogentnexus-openclaw/scripts/namespace_ownership.py
```

Implementation changes:

1. Factored the existing deterministic traversal into `_project_tree_entries()`.
2. Added `_project_tree_snapshot()` returning the exact ordered digest-input entries and the digest from that same scan.
3. Kept `_project_tree_sha256()` as a compatibility wrapper returning the same digest.
4. Added bounded deterministic `_project_tree_snapshot_delta()` with a limit of 64 differences.
5. Changed `prepare_plugin_rollover_transaction()` to scan source and backup once each, compare their precomputed hashes, and derive diagnostic differences from those captured snapshots.
6. Preserved the terminal message prefix exactly:

```text
pre-install backup project-tree attestation mismatch
```

The diagnostic includes only relative path, object identity metadata already in the digest contract, source tree SHA-256, and backup tree SHA-256. File contents, credentials, tokens, environment data, and process data are not serialized.

The mismatch path does not retry, sleep, exclude paths, use payload-only fallback, or re-scan after mismatch. Diagnostic construction occurs before the same fail-closed `RuntimeError` is raised.

## Contract and invariant proof

Focused result:

```text
61 passed in 3.37s
```

This included the new Task-250 test and existing Task-225/226 rollover attestation tests.

Final full Python result:

```text
511 passed, 5 skipped, 4 subtests passed in 72.42s
```

The tests prove:

- matching trees retain the existing digest identity;
- the controlled non-payload mutation still fails closed;
- the exact exception remains compatible;
- the delta identifies the changed path and source/backup identities;
- both hashes and the diagnostic use the same captured scan inputs;
- no post-mismatch re-scan is needed;
- no tree contents are stored in the diagnostic;
- ownership, backup, transaction, replacement order, lifecycle, and retry semantics are unchanged.

PowerShell parser:

```text
PS_SYNTAX=PASS
```

Plugin validation:

```text
npm run plugin:validate = PASS
mixed-plugin artifact verification = PASS (45 config properties, 5 tools)
ticket DB bootstrap = PASS (9 required tables + v095 registration fence)
packedFileCount = 196
```

`npm audit --omit=dev` returned a non-blocking dependency finding:

```text
git: high severity code injection, no fix available
mime <1.4.1: high severity ReDoS, no fix available
2 high severity vulnerabilities
```

This audit result is reported separately and did not alter source or live product state.

## Final candidate and Actions

Final candidate source SHA:

```text
9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96
```

Final candidate plugin fingerprint:

```text
1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Exact candidate installer SHA-256:

```text
c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

The GitHub check-runs API reported 9 checks for this exact SHA; all reached terminal `completed/success`:

```text
validate (ubuntu-latest, 3.14)    success
validate (windows-latest, 3.11)   success
validate (ubuntu-latest, 3.11)    success
validate (windows-latest, 3.14)   success
npm-pack                          success
validate (macos-latest, 3.14)     success
validate (macos-latest, 3.11)     success
package dry-run (no publish)      success
serializer                        success
```

No CI rerun was performed. A polling helper was corrected twice after local shell-control mistakes; those mistakes did not invoke workflows or change repository state.

## Hard-fence ledger

```text
live scripts/install.ps1 invocations = 0
live installer Scheduled Task registrations/starts = 0
live rollover prepare/finalize = 0
live plugin install/copy/delete/rename = 0
live retired-project writes = 0
live retained-backup writes/deletes/renames = 0
controller/Gateway/provider/model lifecycle mutation = 0
Ticket/outbox/recovery/SQLite live mutation = 0
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
```

Repository-only source/test edits were limited to the Task-250 RED and minimal production diagnostic repair. The public release tag was not changed.

## Conclusion and stop boundary

The exact hash-input snapshot diagnostic is repaired and GREEN. The Task-226 full-tree attestation remains fail closed with the same terminal exception semantics; only bounded evidence attached to that failure was added.

This repair does not prove that a future live install will succeed and does not authorize live deployment. Live installer retry and semantic acceptance remain unauthorized by Task 250.

Publish this report, verify the report blob and raw bytes, then STOP for independent ChatGPT review.
