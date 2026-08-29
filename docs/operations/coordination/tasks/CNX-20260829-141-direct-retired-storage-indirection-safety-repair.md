# CNX-20260829-141 — Direct Retired-Storage Filesystem-Indirection Safety Repair

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_RETIRED_STORAGE_INDIRECTION_TDD_REPAIR_ONLY`
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation
Opened: 2026-08-29 ICT

## Objective

Close the root-level filesystem-indirection safety gap identified by the independent Task-140 review without undoing Task 140's valid support for a real direct OpenClaw extension directory.

Use RED -> minimal fix -> GREEN. This task is offline-only and does **not** authorize another live install-over attempt.

## Starting evidence

Task-140 report:

`docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`

Independent Task-140 review:

`docs/operations/coordination/reviews/CNX-20260829-140-installer-ownership-boundary-rollover-repair-review.md`

Review disposition: **REWORK**.

Task-140 production commit under review:

`4d47629edeb8b4e0ab23f1fabee98c05f702d141`

Task 140 correctly established that a legitimate retired payload may be a real directory at:

```text
<openclawState>/extensions/cogentnexus-openclaw
```

and that the old unconditional managed-npm boundary check caused Task 139's failure.

The blocking issue is narrower: `_retired_storage_root()` authorizes the direct layout only after `Path.resolve()`. A lexical canonical direct root that is itself a symlink/junction/reparse point can therefore lose its indirection identity before authorization.

## Required execution discipline

Do not edit production source until a deterministic RED proves the missing invariant against the current Task-140 repair.

Do not broaden this task into general path refactoring. Preserve the already-proven ordinary direct-directory fix.

## Phase 0 — Fresh authority

Before editing:

1. verify fresh branch HEAD and coordination state;
2. verify Task 141 is active and not superseded;
3. inspect Task-140 report/review and production commit `4d47629e...`;
4. keep all investigation and tests offline; do not mutate the user's live Windows runtime.

## Phase 1 — Prove the indirection gap with RED

Create the narrowest deterministic fixture based on the accepted Task-140 direct-retired layout.

Required portable RED:

1. create the canonical direct retired directory as a normal real directory;
2. write a coherent manifest that binds that direct path;
3. move the payload to another directory still inside the OpenClaw state boundary;
4. replace the canonical direct path with a filesystem symlink to that in-state target;
5. keep controller state and all other ownership evidence otherwise valid;
6. call the actual `prepare_plugin_rollover_transaction()` boundary;
7. prove current `4d47629e...` incorrectly proceeds far enough to create/authorize the backup transaction instead of rejecting the root indirection.

The RED must fail for the semantic reason above, not for unavailable symlink privileges or unrelated fixture setup.

### Windows junction/reparse proof

Because the production failure/deployment platform is Windows, also prove the Windows root-indirection contract.

Preferred order:

- use a reliable Windows CI test that creates a junction/reparse root and expects rejection; or
- if privilege/environment constraints make real junction construction nondeterministic, extract/reuse the narrow root-attestation primitive so its Windows `FILE_ATTRIBUTE_REPARSE_POINT` behavior is directly testable, then retain exact Windows CI coverage of that code path.

Do not silently skip the Windows-specific ownership assertion and still claim the invariant proven.

## Phase 2 — Minimal owning-boundary repair

After RED, make the smallest repair that distinguishes:

- the **lexical manifest-owned root** that must itself be an attestable real directory; from
- its resolved/canonical path used for containment and identity comparisons.

The repair should preferably reuse the module's existing non-following metadata/reparse semantics rather than create a second inconsistent filesystem policy.

Required behavior:

- real direct directory at `<openclawState>/extensions/cogentnexus-openclaw` -> accepted;
- direct root that is a symlink -> rejected before backup mutation;
- direct root that is a Windows junction/reparse point -> rejected before backup mutation;
- direct root resolving outside OpenClaw state -> rejected;
- arbitrary sibling/noncanonical direct-looking path -> rejected;
- valid managed npm-project retired payload -> unchanged and accepted;
- foreign/shared/unproven npm wrapper -> unchanged and rejected.

Do not weaken `_npm_project_for_plugin()` and do not permit arbitrary extension directories.

## Phase 3 — GREEN and regression surface

At minimum run:

1. the new portable root-indirection regression;
2. the Windows junction/reparse assertion or its approved narrow Windows-attestation equivalent;
3. the accepted Task-140 real-direct-directory regression;
4. the full `tests/test_plugin_generation_rollover.py` surface;
5. `tests/test_namespace_install_contract.py`;
6. `tests/test_installer_transaction_wiring.py`;
7. other directly affected ownership/installer tests discovered during repair;
8. plugin tests;
9. build;
10. `plugin:validate`;
11. `git diff --check`.

Then verify the normal exact-repair-SHA GitHub Actions set, including Windows Installer Pack Smoke and PS5.1 Acceptance Smoke.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`

The report must include:

- exact root cause;
- genuine RED command/output;
- exact production change;
- symlink/junction/reparse proof;
- preserved positive direct-directory behavior;
- preserved managed-npm behavior;
- negative boundary evidence;
- test/build/plugin validation results;
- exact repair commit SHA;
- exact CI run IDs/results;
- explicit confirmation of zero live runtime/Dashboard mutation.

Then stop for independent ChatGPT review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset; no controller-mode normalization; no manual plugin enable/disable/delete/replace; no live runtime/database/Ticket/workflow/outbox/ack/delivery/recovery mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no recovery/crash injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.

## Acceptance boundary

A Task-141 PASS is still offline/source evidence only. It must be independently reviewed before a later task may authorize a controlled live install-over retry and provenance/health proof.
