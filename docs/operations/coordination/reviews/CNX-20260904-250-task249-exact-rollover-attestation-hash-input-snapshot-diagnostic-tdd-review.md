# CNX-20260904-250 — Independent Review

## Verdict

`ACCEPT_PASS_EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD__TASK226_FAIL_CLOSED_PRESERVED__EXACT_CANDIDATE_READY_FOR_ONE_LIVE_INSTALL_REQUALIFICATION`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed report publication HEAD: `e6e971211cec36af80c66ca3c1f8726ec89d2392`
- Reviewed report: `docs/operations/coordination/reports/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`
- Exact implementation candidate: `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`
- Final test-only RED commit: `ea5d8446c76d24ec01aed29e2f2b0533b0c628ce`
- Task-250 opening authority / RED parent: `e052b59dca03a71ff1405993f90168d5327483b7`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` unchanged

Fresh GitHub branch authority at review opening was exactly the report publication HEAD above.

## TDD chronology adjudication

The final RED commit is a direct child of the Task-250 opening authority and changes only:

`tests/test_task250_hash_input_snapshot_diagnostic.py`

No production/source/workflow file is changed by the RED commit.

The RED deterministically mutates non-payload `runtime-state.txt` immediately after the rollover backup copy. Before the production repair, the expected failure was the intended missing diagnostic behavior:

```text
1 failed
AssertionError: 'runtime-state.txt' not found in
'pre-install backup project-tree attestation mismatch'
```

The test requires more than the generic exception. It requires:

- the exact changed path;
- source and backup identities;
- SHA-256 identity metadata;
- distinct source/backup tree hashes;
- exactly two snapshot calls after the production seam exists;
- no file-content leakage into the exception text.

This is a meaningful test-first RED rather than a harness-only failure.

## Production diff adjudication

The implementation commit is the direct child of the RED commit and changes only:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The repair is bounded to the attestation diagnostic seam:

1. the pre-existing deterministic tree enumeration body is factored into `_project_tree_entries()`;
2. `_project_tree_snapshot()` returns the entry snapshot and `_json_sha256(entries)` from the same scan;
3. `_project_tree_sha256()` remains a compatibility wrapper over the same exact entry digest contract;
4. source and backup are each scanned once after `copytree()`;
5. the compared tree hashes are taken from those two captured snapshots;
6. on mismatch, `_project_tree_snapshot_delta()` compares those already-captured snapshots instead of rescanning the trees;
7. the delta is deterministic and bounded to 64 differing paths;
8. the existing terminal prefix `pre-install backup project-tree attestation mismatch` is preserved;
9. the mismatch still raises `RuntimeError` immediately and does not retry, sleep, weaken the proof, use a payload-only fallback, or exclude mutable paths.

The diagnostic contains digest-relevant identity metadata and hashes, not file contents. No ownership, backup-token, transaction serialization, plugin replacement order, lifecycle, or installer retry semantics are changed by this commit.

## Task-226 invariant

The Task-225/226 non-payload mutation invariant remains intact: mutation after the backup copy still causes a terminal full-tree attestation mismatch. The production change increases evidence at that failure boundary; it does not convert mismatch into success.

The digest producer remains semantically the same ordered entry list passed through `_json_sha256()`, so representative existing tree identities are not redefined by the refactor.

## Verification evidence

Task-250 reported:

```text
focused attestation tests = 61 passed
full Python = 511 passed, 5 skipped, 4 subtests passed
PowerShell parser = PASS
plugin:validate = PASS
mixed-plugin artifact verification = PASS
ticket DB bootstrap = PASS
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
installer SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

Fresh exact-SHA GitHub Actions for `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96` independently show all three deployment gates terminal SUCCESS on attempt 1:

```text
Validate                      33896622009 = SUCCESS
Windows Installer Pack Smoke 33896622084 = SUCCESS
PS5.1 Acceptance Smoke        33896621985 = SUCCESS
```

The exact-SHA check-runs set contains 9 completed/success checks. No same-SHA CI rerun was required for the Task-250 candidate.

### npm audit note

The Task-250 local report separately recorded two high-severity no-fix dependency advisories (`git`, `mime`), while the exact-SHA GitHub `Validate` workflow's `npm audit --omit=dev` step completed successfully on the authoritative candidate. This is retained as an environment/audit-view discrepancy, not hidden or promoted into an unrelated Task-250 product regression. It does not weaken the exact-SHA deployment gate result and should remain observable in later dependency/security work.

## Hard-fence adjudication

The report records zero live installer, rollover, plugin, lifecycle, Ticket/outbox/recovery/SQLite, semantic, replay, and release/tag mutations. Repository changes are limited to the RED test, minimal production diagnostic repair, and report publication. No evidence reviewed contradicts that ledger.

## Disposition

Task 250 is accepted as repository-level PASS.

The exact candidate authorized for the next live requalification is:

`9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`

with expected plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

This review authorizes only a separate, bounded Windows install-over requalification task. It does **not** authorize a Dashboard semantic turn, Discord semantic test, recovery replay, reset/uninstall/fresh reinstall, or release/tag mutation.

The live successor must preserve the Task-237 exact detached-checkout source-binding topology, permit at most one installer invocation, close the retry gate when execution starts, and retain the new Task-250 hash-input delta if the Task-248 mismatch recurs.
