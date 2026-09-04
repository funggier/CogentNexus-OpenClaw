# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK250_EXACT_ROLLOVER_ATTESTATION_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD`
Current disposition: `TASK249_ACCEPTED_BLOCKED__HISTORICAL_PATH_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_REQUIRED`
Task ID: `CNX-20260904-250`
Parent task: `CNX-20260904-249`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / repository-capable implementation agent
Coordinator / independent reviewer: ChatGPT

## Accepted Task-249 result

Independent review verdict:

`ACCEPT_BLOCKED_FORENSIC_EVIDENCE_INSUFFICIENT__TRANSIENT_PATH_AND_ACTOR_UNPROVEN__EXACT_HASH_INPUT_SNAPSHOT_TDD_INSTRUMENTATION_REQUIRED__TASK226_FAIL_CLOSED_INVARIANT_PRESERVED`

Reviewed report HEAD:

`85f7afe25c29db59060dafc2d2ce5f3de80942d6`

Review commit:

`67f8865b470fbc7e607b9df4509e1d49c3d3d1d0`

Task 249 proved that the retained Task-248 backup and current retired project are equal now, but the available historical USN/log/process evidence cannot reconstruct the exact per-path difference or causal actor at the Task-248 failed attestation boundary.

The Task-226 full-tree fail-closed invariant remains accepted and MUST NOT be weakened.

## Active Task 250

Execute:

`docs/operations/coordination/tasks/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`

Required flow:

```text
fresh GitHub authority
-> inspect Task226 attestation seam and exact tree-hash producer
-> TEST-ONLY RED with deterministic controlled mutation
-> prove current missing exact hash-input per-path evidence
-> minimal production diagnostic repair
-> source+backup exact entry snapshots from the SAME scans that produce compared hashes
-> mismatch delta from those captured snapshots, not a later primary re-scan
-> preserve exact digest contract + Task226 fail-closed exception
-> focused GREEN
-> full GREEN
-> exact final candidate/fingerprint/Actions evidence
-> report
-> STOP for independent review
```

## Hard fences

```text
live installer/Scheduled Task/rollover invocations = 0
live plugin/retired-project/retained-backup mutation = 0
controller/Gateway/provider/model/DB lifecycle mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
```

Repository source/test changes and ordinary CI are authorized.

Do not ignore/downgrade mismatch, use payload-only fallback, exclude paths merely to pass, retry until equality, or run the live installer.

## CI note inherited from Task 249

Task-249 report-head Validate attempt 1 had one Windows/Python 3.11 Vitest 15-second timeout in `v099-native-restart-ownership.test.ts`; all other matrix jobs passed. One same-SHA failed-job retry was authorized because it has no product/semantic side effects. No repeated retries or timeout inflation are authorized without root-cause evidence. This does not authorize any live deployment.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-250-task249-exact-rollover-attestation-hash-input-snapshot-diagnostic-tdd.md`

Then STOP for independent ChatGPT review. Live installer retry and semantic acceptance remain unauthorized.
