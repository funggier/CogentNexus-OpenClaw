# CNX-20260902-226 — Rollover-Prepare Attestation Fail-Closed Repair

Status: `IN_PROGRESS`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-225`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Executor: ChatGPT repository repair
Coordinator / final reviewer: ChatGPT

## Purpose

Implement the minimum repository-side TDD repair for the Task-225 proven `SOURCE_DEFECT_NONATOMIC_ATTESTATION` defect.

`prepare_plugin_rollover_transaction()` must fail closed before returning success whenever the newly-created backup full-tree attestation differs from the retired source full-tree attestation required by the finalizer contract.

## Accepted parent authority

Task-225 report:

`docs/operations/coordination/reports/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause.md`

Task-225 review:

`docs/operations/coordination/reviews/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause-review.md`

Accepted review disposition:

`ACCEPT_PASS_PRODUCER_ROOT_CAUSE_PROVEN__AUTHORIZE_BOUNDED_TDD_REPAIR`

Accepted RED lineage:

- rejected harness attempt: `007d6bfd24f8fdd00e7d36b4adb468dfaf8cdcb9`;
- valid deterministic RED: `f93d78324decf44cdccdeae3a9efe30636b681a8`;
- Validate run: `33616947769`;
- Ubuntu/Python 3.11 job: `100204920420`.

## Hard fences

Authorized:

- repository test refinement;
- minimal production repair in `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- relevant repository regression tests;
- GitHub Actions validation;
- coordination report/review publication.

Forbidden:

- live installer invocation;
- live rollover prepare/finalize;
- manual ownership/transaction/backup repair;
- cnxclaw lifecycle action;
- OpenClaw plugin mutation;
- Gateway restart;
- SQLite write;
- provider/model substitution;
- process termination;
- Discord Send/API semantic traffic;
- Release/tag/asset mutation;
- force push/history rewrite.

Discord budget: `0 Sends`.

## Required flow

### Phase A — Fresh authority

1. Fetch fresh branch HEAD and coordination state before every repository write.
2. Stop if unrelated product/source drift supersedes Task 226.

### Phase B — Contract RED

Refine the Task-225 regression test so desired behavior is explicit:

- arrange valid direct plugin state;
- mutate only a non-payload file after top-level backup copy;
- assert source/backup payload fingerprints remain equal as an observation when useful;
- require `prepare_plugin_rollover_transaction()` to raise a fail-closed `RuntimeError` rather than return an inconsistent transaction.

Run/observe current source RED. Failure must be `DID NOT RAISE` or equivalent target behavior, not harness/setup failure.

### Phase C — Minimal production repair

After genuine contract RED:

1. preserve current finalizer predicates;
2. after backup creation, compute `retired_project_tree_sha256` and `backup_project_tree_sha256` exactly once each;
3. compare them before constructing/returning the transaction;
4. if unequal, raise a clear `RuntimeError` indicating backup/source project-tree attestation mismatch;
5. serialize the already-computed matching hashes when equal;
6. do not weaken `_project_tree_sha256()` coverage;
7. do not exclude non-payload entries from full-tree proof;
8. do not broaden to link-preserving copy semantics unless a separate deterministic regression requires it.

### Phase D — GREEN

At minimum validate:

- targeted Task-226 regression test GREEN;
- Task-143 direct-in-place finalization regression tests GREEN;
- relevant namespace ownership tests GREEN;
- full `python -m pytest -q` GREEN on supported CI matrix;
- py_compile/source validation GREEN;
- GitHub Validate workflow GREEN;
- PS5.1 Acceptance Smoke GREEN;
- Windows Installer Pack Smoke GREEN.

Any unrelated failure must be classified before repair expansion.

### Phase E — Report and stop

Publish:

`docs/operations/coordination/reports/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair.md`

Record exact HEAD, commits/files, tests/workflows, PASS/FAIL/BLOCKED, mutation ledger, and next action.

No live Windows installer retry is authorized by Task 226.
