# CNX-20260829-140 — Installer Ownership-Boundary Rollover Diagnosis and Repair

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_INSTALLER_OWNERSHIP_BOUNDARY_TDD_REPAIR_ONLY`
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation
Opened: 2026-08-29 ICT

## Objective

Prove the exact source-level cause of the Task-139 install-over failure at the ownership-safe plugin generation-rollover boundary, add a deterministic RED regression that reproduces the factual installed topology/caller contract, implement the smallest safe production repair, and return the relevant offline test/build/package/CI surface to GREEN.

This task does **not** authorize another live install-over attempt.

## Starting evidence

Accepted predecessor review:

`docs/operations/coordination/reviews/CNX-20260829-139-repaired-candidate-install-over-and-health-proof-review.md`

Task-139 report:

`docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`

Accepted Task-139 execution verdict:

`FAIL_INSTALL_OVER`

Exact repaired Dashboard candidate that Task 139 attempted to deploy:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

Observed installed plugin path at the failure boundary:

```text
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
```

Observed fail-closed error:

```text
RuntimeError: plugin is not inside the managed npm projects boundary:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ownership-safe plugin generation rollover pre-install proof failed
```

After the failed live attempt, the effective installed payload remained the pre-repair fingerprint and the controller remained in `passthrough` with the one plugin identity disabled. Task 140 must not alter that live state.

## Required execution discipline

Use RED -> minimal fix -> GREEN.

Do not edit production source until the Task-139 failure is reproduced deterministically by a meaningful offline test at the narrowest trustworthy operational boundary.

Do not assume from the error string alone that `namespace_ownership.py` is wrong. First prove the actual caller/path/state-root contract that reaches the rejection.

## Phase 0 — Fresh repository authority

Before editing:

1. verify fresh branch HEAD and coordination state;
2. verify Task 140 is still active and not superseded;
3. inspect the accepted Task-139 report/review;
4. identify the exact installer entry/caller chain used by Task 139;
5. keep all investigation offline — no Windows runtime mutation.

If coordination has advanced or the task is superseded, stop rather than publishing competing work.

## Phase 1 — Reconstruct the ownership contract

Trace the exact operational path from the supported installer entry through ownership/generation rollover preparation.

At minimum establish, with source references and testable values:

- how `scripts/install.ps1` derives the OpenClaw state root;
- how it derives/passes the currently installed plugin path;
- how it invokes the ownership helper and rollover operation;
- how `namespace_ownership.py` derives the managed npm projects boundary;
- which paths are lexical versus resolved/canonical;
- whether the installed extension path is expected to be a direct directory, link/junction, generated package projection, or another managed OpenClaw layout;
- what ownership metadata/generation relationship is expected before replacement;
- why the exact valid or invalid Task-139 topology reaches the observed rejection.

Explicitly distinguish among possible categories rather than collapsing them into one guess:

- caller-supplied plugin path mismatch;
- incorrect managed-projects-root model;
- path normalization/canonicalization defect;
- package-manager/OpenClaw layout mismatch;
- symlink/junction resolution semantics;
- stale or inconsistent generation/ownership metadata;
- genuinely unmanaged path that the installer should never have attempted to roll over;
- another source-proven cause.

## Phase 2 — Genuine RED

Before any production edit, add a deterministic regression that represents the factual Task-139 topology and exercises the same ownership/rollover contract or the closest trustworthy boundary that can reproduce it without touching the live runtime.

The RED must fail for the same semantic reason as Task 139, not because of an unrelated harness/setup error.

The test evidence must record:

- exact fixture topology;
- effective state root;
- managed npm projects path;
- installed plugin path presented to the helper/caller;
- link/junction/realpath semantics if applicable;
- expected ownership result;
- actual pre-fix failure.

If the factual Task-139 topology proves genuinely unmanaged under the intended contract, do **not** weaken the ownership boundary merely to make the install pass. Instead prove the upstream installer/path-selection defect with RED at that boundary.

## Phase 3 — Minimal production repair

Only after a meaningful RED exists:

1. state the proven root cause;
2. change the smallest production surface that owns that defect;
3. avoid unrelated installer/refactor cleanup;
4. preserve existing fail-closed behavior for unproven ownership.

The repair must preserve all of these invariants:

- genuinely unmanaged plugin locations remain rejected;
- `..`/boundary escapes remain rejected;
- symlink/junction tricks must not permit escape from the intended authority boundary;
- no plugin deletion/replacement may occur before ownership is proven;
- exactly one effective plugin ownership/generation authority is preserved;
- rollback/cleanup semantics are not weakened;
- no manual runtime normalization is encoded as a workaround;
- no Dashboard delivery semantics are changed by this installer repair.

## Phase 4 — GREEN validation

Run the narrowest tests first, then the complete relevant surface.

Required evidence, where applicable to the touched files:

1. the new Task-139 topology regression GREEN;
2. existing namespace-ownership tests GREEN;
3. existing generation-rollover tests GREEN;
4. installer PowerShell tests/smoke GREEN;
5. relevant package/install artifact verification GREEN;
6. plugin/build validation GREEN if the packaging/install surface requires it;
7. `git diff --check` GREEN;
8. exact-repair-SHA CI workflows GREEN for all repository-required validation workflows affected by the production change.

Record commands, counts, exit codes, and workflow run IDs/links or equivalent exact evidence.

## Phase 5 — Scope and provenance proof

Before reporting:

- show exact repair commit SHA;
- show changed files;
- show the RED test commit/order or equivalent durable proof that RED preceded production repair;
- show production/test blob hashes where useful;
- prove no live Windows install/install-over/uninstall/reset occurred during Task 140;
- prove no Dashboard semantic Send occurred;
- prove no merge/tag/release/force push occurred.

## PASS criteria

Task 140 is `PASS` only if all are true:

1. the exact Task-139 ownership failure is reproduced offline by a meaningful RED;
2. exact source-level root cause is proven rather than inferred;
3. the production repair is minimal and located at the owning boundary;
4. ownership containment/fail-closed invariants remain explicitly tested;
5. relevant offline validation is GREEN;
6. exact repair SHA CI is GREEN where required;
7. no live runtime or semantic side effect occurred.

If root cause remains ambiguous, report `BLOCKED_ROOT_CAUSE_NOT_PROVEN` rather than guessing.

If a safe minimal repair cannot preserve ownership containment, report `BLOCKED_OWNERSHIP_SAFETY_CONFLICT`.

If tests or CI remain red, report `FAIL_VALIDATION` with exact evidence.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`

Then stop for independent ChatGPT review.

A Task-140 PASS does **not** itself authorize live install-over retry. A separate reviewed deployment-proof task must be opened afterward.

## Hard fence

No live Windows install/install-over/update/uninstall/reset; no runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Gateway/provider/OpenClaw configuration mutation; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no recovery/crash injection; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.
