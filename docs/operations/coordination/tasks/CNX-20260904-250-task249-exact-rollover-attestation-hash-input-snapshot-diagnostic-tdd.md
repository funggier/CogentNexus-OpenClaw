# CNX-20260904-250 — Task-249 Exact Rollover Attestation Hash-Input Snapshot Diagnostic TDD

## Status

`READY_FOR_HERMES`

## Parent

- Task: `CNX-20260904-249`
- Reviewed report HEAD: `85f7afe25c29db59060dafc2d2ce5f3de80942d6`
- Independent review verdict:
  `ACCEPT_BLOCKED_FORENSIC_EVIDENCE_INSUFFICIENT__TRANSIENT_PATH_AND_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_INSTRUMENTATION_REQUIRED__TASK226_FAIL_CLOSED_INVARIANT_PRESERVED`
- Review commit: `67f8865b470fbc7e607b9df4509e1d49c3d3d1d0`
- Parent umbrella: `CNX-20260831-188`

## Objective

Add repository-only, behavior-preserving diagnostic instrumentation to the plugin-generation rollover prepare attestation so that, if the source and backup full-tree hashes differ again, the failure retains the **exact per-path differences from the same hash-input snapshots that produced those two hashes**.

This task exists to close the evidence gap exposed by Tasks 248–249. It MUST NOT weaken the Task-226 fail-closed invariant and MUST NOT run the live installer.

## Accepted facts

Task 248 proved a real live failure at:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

Task 249 proved that later source/backup equality cannot reconstruct the historical transient difference and that retained post-event USN/log/process evidence cannot identify the historical path or actor.

Current producer logic in `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` computes `_project_tree_sha256()` from a deterministic ordered entry set containing digest-relevant path/type/content identity metadata. Re-scanning after mismatch detection is not sufficient because a transient mutation may already have reverted.

The existing Task-225/226 regression proves that a non-payload source mutation after backup copy MUST remain terminal and fail closed.

## Hard design invariant

The hash and diagnostic evidence MUST share the same scan inputs.

Preferred bounded shape:

```text
scan source once -> source exact entry snapshot + source tree SHA-256
scan backup once -> backup exact entry snapshot + backup tree SHA-256
compare the two precomputed tree hashes
if mismatch:
    diff those already-captured exact entry snapshots
    retain/report bounded deterministic diagnostic evidence
    raise the existing fail-closed mismatch
```

Do not use a fresh post-mismatch re-scan as the primary source of the per-path difference. A later re-scan may be allowed only as explicitly secondary/supporting evidence and must never replace the captured hash-input snapshots.

## TDD requirements

### Phase A — fresh authority and test-only RED

1. Fresh-fetch GitHub branch authority, Task 250, Task-249 report/review, `ACTIVE.md`, `STATUS.md`, public `v0.9.3` tag, and relevant Actions state before editing.
2. Identify the exact Task-226 prepare attestation test seam and current `_project_tree_sha256()` implementation.
3. Add a **test-only RED commit**. Do not edit production code in this commit.
4. The RED must deterministically reproduce a source-vs-backup full-tree mismatch using a controlled mutation/hook; do not use timing sleeps or race probability.
5. The RED must prove the missing behavior, not merely restate the existing generic exception. At minimum it must require that the mismatch evidence identifies the exact changed/missing/extra path and its source-vs-backup digest-relevant identity from the same snapshots used for the failed hash comparison.
6. The RED must still expect the existing terminal fail-closed condition:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

7. Capture and report the exact RED failure output and RED commit SHA.

A RED that passes before production repair is invalid. A RED caused by a harness mistake is invalid.

### Phase B — minimal production repair

Implement the smallest production change needed to make the RED pass.

The repair SHOULD reuse/factor the existing tree enumeration so one deterministic scan can return both:

```text
full-tree SHA-256
exact ordered digest-input entry snapshot
```

or an equivalent immutable representation.

The exact digest contract must remain unchanged. Existing trees must produce the same `_project_tree_sha256()` identity as before.

On mismatch, derive a deterministic bounded per-path delta from the two already-captured snapshots. Distinguish at least where applicable:

```text
changed path
missing from source
missing from backup
object/type change
regular-file size/content SHA-256 change
symlink/junction target change
```

Do not store file contents.

### Diagnostic privacy and location

Diagnostic evidence may include only identity metadata needed for adjudication, such as:

```text
relative path
object type
size
content SHA-256
symlink/junction target identity where already part of the digest contract
source tree SHA-256
backup tree SHA-256
```

Do not serialize file contents, credentials, environment secrets, tokens, or unrelated process data.

If a durable artifact is emitted, it MUST be outside both the retired source tree and rollover backup tree, using an existing CogentNexus-OpenClaw state/staging/forensics location appropriate to installer diagnostics. Evidence creation itself must not change either attested tree.

Diagnostic persistence failure MUST NOT convert the original mismatch into installer success. Preserve fail-closed behavior and expose the diagnostic-persistence failure in a bounded way if applicable.

### Phase C — behavior-neutrality and invariant tests

Prove all of the following:

1. matching source/backup trees still pass exactly as before;
2. existing full-tree digest identity is byte-for-byte/hex-for-hex unchanged for representative fixtures;
3. the Task-225/226 non-payload mutation still fails closed;
4. the exact terminal mismatch message remains compatible:
   `pre-install backup project-tree attestation mismatch`;
5. exact per-path diagnostic comes from the same captured snapshots that generated the compared hashes;
6. no post-mismatch re-scan is required to identify the changed path;
7. diagnostic generation does not modify either source or backup tree;
8. no retry-until-equality behavior is introduced;
9. no payload-only fallback/path exclusion is introduced;
10. ownership, backup path/token, transaction serialization, plugin replacement order, lifecycle, and installer retry cardinality semantics remain unchanged.

### Phase D — GREEN and exact candidate proof

Run focused tests first, then the full relevant repository validation.

At minimum report:

- focused Python attestation tests;
- full Python suite;
- plugin tests if repository validation invokes them;
- installer/PowerShell smoke coverage relevant to the changed source;
- `npm audit --omit=dev` result when part of the normal validation path;
- exact final candidate SHA;
- exact plugin payload fingerprint computed from the final candidate, even if expected unchanged;
- public `v0.9.3` tag identity;
- exact-SHA GitHub Actions state.

Before any future live deployment task is authorized, the final candidate must have terminal SUCCESS for:

```text
Validate
Windows Installer Pack Smoke
PS5.1 Acceptance Smoke
```

If a CI timing/harness anomaly occurs, classify it separately. Do not hide it by increasing timeouts without root-cause evidence and do not rerun repeatedly.

## Forbidden repairs

Task 250 MUST NOT:

- ignore or downgrade a full-tree mismatch;
- reduce attestation to package payload files;
- exclude `node_modules` or any other path merely to make installation pass;
- add sleeps/retries until hashes converge;
- hash only after stopping arbitrary processes unless separately proven necessary;
- delete retained rollover backups;
- run the live installer to test the production change;
- change the public release tag;
- change semantic delivery behavior;
- alter ownership, generation-rollover transaction, plugin installation order, controller/Gateway/provider lifecycle, or retry policy except where unavoidable for pure diagnostic plumbing and independently justified.

## Hard fences / effect budget

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

Repository source/test changes and ordinary CI are authorized inside this task.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`

The report must include:

- fresh opening authority;
- test-only RED commit and exact intended RED failure;
- minimal production repair commit(s) and file-level diff summary;
- explanation of how hash and diagnostic share the exact same captured scan inputs;
- proof that the digest contract did not change;
- proof Task-226 fail-closed semantics remain intact;
- focused and full GREEN evidence;
- exact final candidate SHA and plugin fingerprint;
- exact-SHA Actions state;
- hard-fence effect ledger;
- PASS/FAIL/BLOCKED classification;
- explicit statement that no live installer retry is authorized by Task 250.

Then STOP for independent ChatGPT review.
