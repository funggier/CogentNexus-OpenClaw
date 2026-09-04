# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK250_EXACT_ROLLOVER_ATTESTATION_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 250 is repository-only TDD instrumentation; live installer and semantic retries remain unauthorized  
**Active task:** `CNX-20260904-250`  
**Parent:** `CNX-20260904-249`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK249_ACCEPTED_BLOCKED__HISTORICAL_PATH_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_REQUIRED`

## Accepted Task-249 result

Reviewed report HEAD:

`85f7afe25c29db59060dafc2d2ce5f3de80942d6`

Independent review commit:

`67f8865b470fbc7e607b9df4509e1d49c3d3d1d0`

Independent review verdict:

`ACCEPT_BLOCKED_FORENSIC_EVIDENCE_INSUFFICIENT__TRANSIENT_PATH_AND_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_INSTRUMENTATION_REQUIRED__TASK226_FAIL_CLOSED_INVARIANT_PRESERVED`

Task 249 established:

```text
current retired project tree hash = 900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
current Task248 backup tree hash    = 900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
current digest-relevant entries     = 35,693 / 35,693
current content/object differences  = 0
historical exact changed path       = unproven
historical causal actor/process     = unproven
```

The later equality does not reconstruct the exact source and backup inputs at the Task-248 failed attestation instant. Retained USN/log/process evidence cannot prove the historical path/actor.

Task-226 full-tree fail-closed semantics remain accepted and unchanged.

## Active Task 250

Execute:

`docs/operations/coordination/tasks/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`

Task 250 must use TDD to add behavior-preserving mismatch diagnostics at the exact hash-input boundary:

```text
source scan -> source hash + exact entry snapshot
backup scan -> backup hash + exact entry snapshot
compare precomputed hashes
on mismatch -> diff those captured snapshots -> fail closed as before
```

The per-path evidence must come from the same captured scans used to produce the compared hashes. A later re-scan must not be the primary evidence source.

Required TDD topology:

```text
fresh authority
-> test-only deterministic RED
-> minimal production repair
-> focused GREEN
-> full GREEN
-> exact candidate/fingerprint/Actions proof
-> report
-> STOP for independent review
```

## Safety invariants

Task 250 must preserve:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

and MUST NOT:

- ignore/downgrade the mismatch;
- reduce proof to package payload only;
- exclude a path merely to make installation pass;
- add sleeps/retries until equality;
- modify source/backup trees to generate evidence;
- change ownership/backup/transaction/plugin-order/lifecycle/retry semantics;
- run the live installer.

## Hard fences

```text
live scripts/install.ps1 = 0
live installer task registration/start = 0
live rollover prepare/finalize = 0
live plugin/retired-tree/backup mutation = 0
controller/Gateway/provider/model/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
```

Repository source/test changes and normal CI are authorized.

## CI note

Task-249 report HEAD had successful PS5.1 Acceptance Smoke and Windows Installer Pack Smoke. Validate attempt 1 had one Windows/Python 3.11 Vitest 15-second timeout while the other matrix jobs passed. One same-SHA failed-job rerun was authorized because it has no product/semantic side effects; no repeated retry or timeout inflation is authorized without root-cause evidence. No live deployment is authorized from this CI note.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`

Then STOP for independent ChatGPT review. Live installer retry and semantic acceptance remain unauthorized.
