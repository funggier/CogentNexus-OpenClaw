# CNX-20260904-249 — Independent Review

## Verdict

`ACCEPT_BLOCKED_FORENSIC_EVIDENCE_INSUFFICIENT__TRANSIENT_PATH_AND_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_INSTRUMENTATION_REQUIRED__TASK226_FAIL_CLOSED_INVARIANT_PRESERVED`

## Authority reviewed

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task-249 opening authority: `5fc7ebaab6a4be042518246d7e6ef96e9319ff03`
- Task-249 report HEAD: `85f7afe25c29db59060dafc2d2ce5f3de80942d6`
- Parent Task-248 report HEAD: `06b7bc01161efe2c8bbb97fe0e0511d79ff8d62b`
- Public `v0.9.3` tag: `26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Independent findings

### 1. Scope and publication are clean

Task 249 stayed inside its read-only forensic boundary. The effect ledger records zero installer, rollover, protected-tree write, lifecycle, Ticket/outbox/recovery/SQLite, semantic-send, replay/resend, process-termination, production/source/test/workflow, and release/tag/history mutations.

The repository comparison from `5fc7eba...` to `85f7afe...` contains exactly one commit and exactly one added file: the Task-249 report. No production/test/workflow/coordination-state drift accompanied the report publication.

### 2. Current equality cannot reconstruct the historical failed attestation boundary

The current retired project and the retained Task-248 backup both hash to:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

with 35,693 digest-relevant entries each. Current comparison shows zero regular-file/symlink/object-content differences and zero missing/extra object paths.

The 2,037 directory-metadata differences are not part of `_project_tree_sha256()` and therefore cannot explain the Task-248 full-tree mismatch.

Post-failure equality is not evidence that the two hash inputs were equal at the historical instant when Task 248 raised `pre-install backup project-tree attestation mismatch`.

### 3. Historical path and actor remain unproven

The bounded NTFS/USN query, Windows event logs, post-event process snapshot, OpenClaw/npm/Defender evidence, and retained Task-248 evidence do not establish a historical path-plus-causal-actor pair.

The passive observation produced six identical tree hashes across roughly 120 seconds. That is valid negative evidence for that observation window only; it cannot exclude an operation-coupled transient mutation during Task 248.

Task 249 correctly did not infer an actor from `node_modules`, directory metadata, gateway presence, or a post-event process snapshot.

### 4. Task-226 fail-closed behavior remains correct

Nothing in Task 249 disproves the safety invariant introduced by Task 226. A source/backup full-tree mismatch must continue to fail closed.

A successor must not ignore the mismatch, reduce attestation to package payloads, exclude paths merely to make installation pass, retry until equality, or delete/replace retained evidence.

### 5. Missing evidence belongs at the exact hash-input boundary

`_project_tree_sha256()` derives a deterministic ordered entry set containing path/type and content identity metadata, then hashes that entry set. Therefore the most reliable diagnostic successor is to retain the exact source and backup entry sets used to derive the two attestation hashes in the same pass and diff those captured entry sets if the hashes differ.

Re-scanning either tree only after mismatch detection is insufficient because a transient mutation may already have reverted.

Any diagnostic artifact must be written outside both the retired source tree and the rollover backup tree so evidence capture cannot contaminate either attested input.

### 6. CI retry is classified separately from the forensic result

At report HEAD `85f7afe...`:

- PS5.1 Acceptance Smoke `33893680991` — SUCCESS
- Windows Installer Pack Smoke `33893680938` — SUCCESS
- Validate `33893681021` attempt 1 — FAILURE only in `validate (windows-latest, 3.11)` because `src/v099-native-restart-ownership.test.ts` timed out at 15 seconds during `npm test`.

The same job had already passed the Python suite (`512 passed, 3 skipped, 4 subtests passed`), and Windows/Python 3.14 plus Ubuntu/macOS matrix jobs passed. Because Task 249 changed only its report, this does not constitute evidence of a Task-249 product regression.

One same-SHA failed-job rerun was authorized under the bounded retry policy because it has no product or semantic side effect. At the time this review was published, that single retry was still running. No second retry is authorized. This review therefore does not assert all-green Actions and does not authorize live deployment.

## Required successor

Open a separate repository-only TDD task to add exact hash-input snapshot diagnostics to rollover prepare while preserving Task-226 semantics.

Required properties:

1. meaningful test-only RED first;
2. deterministic controlled mutation, not timing-based flakiness;
3. source and backup hash plus exact entry snapshots derived from the same scan/attestation pass;
4. deterministic per-path delta on mismatch using those captured snapshots, without re-scanning as the primary evidence source;
5. no content bytes or secrets in diagnostics—path/type/size/content hashes/targets only as applicable;
6. diagnostic location outside source and backup trees;
7. preserve exact fail-closed terminal condition `RuntimeError: pre-install backup project-tree attestation mismatch`;
8. diagnostic persistence failure must never convert a mismatch into installer success;
9. no path exclusions, payload-only fallback, retry-until-equality, ownership/backup/transaction/plugin-order/lifecycle/retry semantic changes;
10. focused GREEN, full GREEN, and exact-candidate Actions evidence before any future live installer task.

## Final adjudication

Task 249 is accepted as a correctly bounded `BLOCKED` forensic result. The historical transient path and causal actor cannot be proven from retained evidence. The next valid move is repository-only TDD instrumentation at the exact hash-input boundary, not another live installer attempt.
