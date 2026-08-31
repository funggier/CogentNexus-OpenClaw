# CNX-20260829-143 — Direct In-Place Rollover Finalization Repair

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_IN_PLACE_ROLLOVER_FINALIZATION_TDD_REPAIR_ONLY`
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation
Opened: 2026-08-29 ICT

## Objective

Repair the ownership rollover finalization defect proven by Task 142 for the supported direct OpenClaw extension layout, using RED -> minimal fix -> GREEN, without touching the user's live Windows runtime.

This task does **not** authorize another live installer run and does **not** authorize any Dashboard semantic Send.

## Starting evidence

Task-142 report:

`docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof-review.md`

Reviewed deployment candidate:

`138759d111fe27a0cda75f59ad108d11caf19120`

Task 142 proved that the supported installer can replace the direct extension payload at the exact same canonical path and obtain the expected candidate fingerprint, yet `finalize_plugin_rollover_transaction()` rejects solely because the replacement path equals the recorded retired path.

## Current live-state caution

Task 142 partially transitioned the live installation before failing:

- canonical direct plugin payload now matches candidate fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` matches candidate hash `e51f03553a24ea67037a3131b5ff4edb8aa435fbbc82b19974ae18f0d03df666`;
- exactly one plugin identity remains, disabled;
- controller remains `passthrough`;
- the existing ownership manifest remains present with its pre-attempt `installedAt` value;
- Gateway/Ollama remained healthy;
- recovery/delivery remained READY and read-only;
- SQLite integrity remained `ok` and semantic counts did not change;
- Dashboard semantic Send count remained `0`.

This is evidence only. Task 143 must not normalize, replay, repair, enable, disable, reinstall, or otherwise mutate that live state.

## Phase 0 — Fresh authority

Before work:

1. verify fresh branch HEAD and coordination state;
2. verify Task 143 is active and unsuperseded;
3. inspect Task-142 report/review and exact candidate source;
4. perform all source/test work in a fresh offline clone/worktree;
5. do not invoke the supported installer against the live workspace.

## Phase 1 — Genuine Task-142 RED

Before any production edit, add the narrowest deterministic test that reproduces the factual Task-142 sequence through the actual transaction APIs.

Required fixture sequence:

1. create a coherent owned installation whose retired plugin is a **real canonical direct directory** at `<openclawState>/extensions/cogentnexus-openclaw`;
2. give that retired payload a valid fingerprint `A` and a coherent manifest binding the direct path;
3. place controller mode in the valid `passthrough` rollover state;
4. call `prepare_plugin_rollover_transaction()` with expected replacement fingerprint `B`, where `B != A`, and prove the pre-install backup is exact;
5. simulate the supported OpenClaw `plugins install --force` direct-storage behavior by replacing the valid plugin payload **at the same canonical direct path** with a new valid payload whose fingerprint is exactly `B`;
6. construct one canonical disabled active plugin inventory record pointing to that same direct path;
7. call the actual `finalize_plugin_rollover_transaction()`;
8. before production repair, prove it fails with the Task-142 semantic reason:

```text
replacement still points to the retired generation
```

The RED must fail at this ownership condition, not from fixture setup, fingerprint mismatch, inventory ambiguity, backup mismatch, or manifest drift.

Record the exact RED command/output before editing production code.

## Phase 2 — Root-cause proof

Document the exact distinction between these storage semantics:

### Managed npm generation rollover

The retired payload and active replacement live in distinct attested managed project roots. Path inequality remains meaningful and must remain enforced.

### Canonical direct extension rollover

The retired storage root and replacement storage root may be the same canonical real directory because OpenClaw replaces the package payload in place. Generation identity must therefore be proven by the transaction's old backup/fingerprint versus the current expected payload, not by path inequality alone.

Trace and record:

- how `prepare_plugin_rollover_transaction()` identifies direct retired storage;
- what transaction fields prove the retired path/root/tree/fingerprint;
- how `_active_registered_plugin()` proves the current replacement;
- how the current finalizer decides the replacement is distinct;
- why Task 142 satisfies fingerprint/source evidence while failing only the path guard;
- whether an explicit transaction storage-kind field is required or existing attested fields can distinguish direct versus managed storage safely.

Do not choose the implementation before this proof is complete.

## Phase 3 — Minimal ownership-safe repair

Make the smallest repair at finalization.

Required positive behavior:

- a prepared canonical real direct retired root with fingerprint `A` may finalize when the same canonical direct root now contains the singular expected replacement fingerprint `B`, with `B != A`, the backup is exact, and all other transaction/manifest/inventory proofs hold;
- the ownership manifest is atomically refreshed and remains bound to the canonical direct plugin path;
- the existing Task-140/141 direct-root non-indirection safety remains intact;
- valid managed npm distinct-generation rollover remains unchanged.

Required negative containment behavior:

1. **Do not simply remove the path inequality guard.**
2. Same-path finalization for a managed npm payload must remain rejected.
3. Same-path direct finalization with current fingerprint equal to the retired fingerprint must be rejected/no rollover authority granted.
4. Same-path direct finalization with current fingerprint not equal to the expected source fingerprint must be rejected.
5. Tampered/missing retired backup or backup-tree proof must be rejected.
6. Ownership manifest drift since prepare must be rejected.
7. Noncanonical direct-looking siblings must be rejected.
8. Direct symlink/junction/reparse roots must remain rejected.
9. Multiple/conflicting product registrations or storage evidence must remain rejected.
10. Replacement registration must remain singular, canonical, exact package/version, and payload-attested.
11. No unrelated shared npm wrapper or arbitrary path may gain mutation authority.

If the cleanest proof requires adding an explicit transaction field such as an attested retired storage kind, keep the schema narrowly scoped and test exact validation. Do not introduce generalized path-policy refactoring.

## Phase 4 — Task-142 partial-state re-entry analysis

Offline only, reconstruct the exact post-Task-142 shape:

- manifest still binds the canonical direct path;
- plugin payload at that path already has the candidate plugin fingerprint;
- plugin registration is singular and disabled;
- controller is `passthrough`;
- candidate source plugin fingerprint equals the installed plugin fingerprint.

Run the real attested `classify-install` and lifecycle-action resolution contract against this fixture.

Required proof:

- state classification is deterministic and fail-closed;
- if it classifies `pluginAlreadyExact=true`, the supported installer action plan does not replay plugin installation/rollover unnecessarily;
- remaining install phases can be reasoned/tested without manual normalization;
- no stale rollover transaction, backup, or ownership evidence is silently adopted as authority;
- any cleanup of stale staging evidence, if required, must be separately owned and must not be invented as a live workaround in this task.

This analysis is required before any later live recovery/install-completion task is opened.

## Phase 5 — GREEN validation

At minimum run:

1. new Task-142 same-path direct RED/GREEN regression;
2. unchanged-fingerprint same-path rejection;
3. managed same-path rejection;
4. expected-fingerprint mismatch rejection;
5. manifest-drift and backup-tamper rejection;
6. existing Task-140 real-direct-directory prepare regression;
7. existing Task-141 symlink/junction/reparse regression;
8. full `tests/test_plugin_generation_rollover.py`;
9. `tests/test_namespace_install_contract.py`;
10. `tests/test_installer_transaction_wiring.py`;
11. lifecycle action-resolution/re-entry tests affected by the partial-state analysis;
12. other directly affected installer/ownership tests;
13. plugin tests;
14. build;
15. `plugin:validate`;
16. package verification as applicable;
17. `git diff --check`.

Then verify the normal exact-repair-SHA GitHub Actions set, including:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Windows CI must exercise the ownership/installer test surface; do not rely only on POSIX results.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`

The report must include:

- exact source-level root cause;
- genuine pre-production RED command/output;
- factual direct same-path fixture;
- exact production change;
- explanation of how direct same-path authority is distinguished from managed generation authority;
- negative containment proof;
- Task-142 partial-state re-entry classification evidence;
- full relevant test/build/plugin/package validation results;
- exact repair commit SHA;
- exact CI run IDs/results;
- explicit confirmation that no live runtime or Dashboard semantic mutation occurred.

Then stop for independent ChatGPT review.

## PASS boundary

`PASS` requires all of the following:

- genuine same-path Task-142 RED existed before production edit;
- source root cause is proven;
- direct same-path finalization is narrowly and safely repaired;
- managed generation safety remains strict;
- Task-140/141 root-indirection safety remains strict;
- Task-142 partial-state re-entry behavior is explicitly proven offline;
- relevant full tests/build/package/plugin validation and exact-SHA CI are GREEN;
- no live side effect occurred.

Otherwise report the narrowest truthful failure/blocker and stop.

## Hard fence

No live Windows install/install-over/update/uninstall/reset/clean-reinstall; no live runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
